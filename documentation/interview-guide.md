# CLARIVENS INVENTORY INTELLIGENCE — SENIOR INTERVIEW GUIDE
**Project Author & Architect:** Himanshu Bagde (Azure Data Engineer & Cloud Analytics Architect)  
**Role Focus:** Senior Data Engineer / Azure Data Architect / Analytics Engineer  
**Organization:** CLARIVENS RETAIL GROUP  
**Platform:** Azure Retail Inventory Data Pipeline & Analytics Platform

---

## 1. Architectural & Technology Selection

### Q1: Why did you choose Azure Data Factory instead of Apache Spark or Databricks?
**Answer:**
> "Our ingestion and transformation pipeline processes approximately 180,000 to 500,000 records daily across 36 stores. At this data volume, spinning up a multi-node Apache Spark or Databricks cluster introduces massive cold-start cluster latency (3–5 minutes), unnecessary operational complexity, and disproportionate compute costs.
>
> Azure Data Factory provides a fully managed, serverless orchestration layer that can bulk copy files from ADLS Gen2 directly into Azure SQL Database staging tables in seconds with built-in retries, native parameterization, and Managed Identity authentication. Transformations are pushed down directly to Azure SQL Database via T-SQL stored procedures, taking advantage of SQL Server's query optimizer and columnstore indexing without paying cluster runtime premiums."

---

### Q2: Why choose Azure SQL Database instead of Snowflake, Synapse Dedicated Pool, or Fabric?
**Answer:**
> "For our operational retail warehouse size (~120k sales per year, ~42k inventory snapshots, ~1,200 products), Azure SQL Database General Purpose (vCore model) is exceptionally well-suited. MPP (Massively Parallel Processing) engines like Synapse Dedicated SQL Pools or Snowflake require distributed data distributions (Hash/Round-Robin/Replicated) and are architected for multi-terabyte datasets. On datasets under a few hundred gigabytes, MPP engines often suffer from distribution overhead and concurrency limits.
>
> Azure SQL Database provides ACID compliance, row-level locking, clustered columnstore indexes, and direct integration with Power BI DirectQuery/Import at a fraction of the cost, while remaining easily upgradeable to Azure SQL Managed Instance or Hyperscale if data volume reaches tens of millions of rows."

---

### Q3: Why is a dedicated Staging schema (`stg`) necessary? Why not write directly to the Warehouse (`dw`)?
**Answer:**
> "Writing raw files directly to dimensional tables is an anti-pattern for three critical reasons:
> 1. **Decoupling Ingestion from Transformation:** Copy activities in ADF need to move data as quickly as possible without failing due to foreign key constraints, data type coercion errors, or business rule violations.
> 2. **Enabling Automated Quality Gates:** Staging tables provide a landing zone where our Python validation framework inspects the batch for schema drift, null rates, duplicate primary keys, and stock balance equations before any record touches production facts.
> 3. **Isolation & Rollback:** If a raw CSV is malformed (e.g. 10% corrupted prices), staging isolates the bad batch. We can truncate or quarantine staging without corrupting historical analytics or taking downtime on `dw.FactSales`."

---

### Q4: Why implement a Star Schema instead of One Big Table (OBT)?
**Answer:**
> "While One Big Table (OBT) works well for ad-hoc queries in ClickHouse or BigQuery, a Kimball-style Star Schema is superior for an enterprise retail Power BI platform:
> - **Storage Efficiency & Memory Footprint:** Product attributes, store locations, and supplier details are stored once in dimension tables rather than repeated across 120,000+ transactional sales rows. Power BI's VertiPaq engine compresses normalized dimensions significantly better.
> - **Role-Playing Dimensions:** A single `dw.DimDate` dimension can serve `OrderDate`, `ExpectedDeliveryDate`, and `ActualDeliveryDate` simultaneously in `dw.FactPurchases` using active and inactive relationships (`USERELATIONSHIP`).
> - **Business Consistency:** Changes to store management or product categories are updated in one place (or tracked via SCD Type 2) without needing to update millions of historical fact records."

---

## 2. Ingestion, Watermarking & Incremental Loading

### Q5: How does incremental loading work in this pipeline?
**Answer:**
> "We implement a high-watermark control mechanism governed by `audit.ETL_Control`:
> 1. At the start of `PL_Load_Sales`, ADF executes a Lookup activity querying `audit.ETL_Control` for `LastWatermarkValue` associated with `dw.FactSales` (e.g. `'2025-10-31'`).
> 2. The pipeline stages the delta files and executes stored procedure `dw.sp_Load_FactSales`.
> 3. In the stored procedure, a CTE filters records where `SaleDate > @LastWatermark`, resolves dimension surrogate keys (`ProductSK`, `StoreSK`, `DateKey`), and deduplicates on `SaleID` using `ROW_NUMBER()`.
> 4. After successfully inserting only new records, the procedure updates `audit.ETL_Control` with `MAX(SaleDate)` from the ingested batch (e.g. `'2025-11-30'`) and commits the transaction."

---

### Q6: How did you handle duplicate records and malformed data in the pipeline?
**Answer:**
> "We handle duplicates at two distinct architectural levels:
> 1. **Detection in Python Quality Gate:** `duplicate_validator.py` checks uniqueness on primary keys (`SaleID`, `InventoryID`, `PurchaseOrderID`). If duplicate rates exceed 5%, the pipeline raises a critical alert.
> 2. **Resolution in SQL Stored Procedures:** During the load into `dw.FactSales`, we use a window function:
>    ```sql
>    ROW_NUMBER() OVER (PARTITION BY SaleID ORDER BY _IngestionTimestamp DESC) AS DeduplicationRank
>    ```
>    We filter strictly where `DeduplicationRank = 1` and wrap the insert with `WHERE NOT EXISTS (SELECT 1 FROM dw.FactSales fs WHERE fs.SaleID = rs.SaleID)`. This guarantees idempotent re-runs without duplicating transaction metrics."

---

### Q7: How does the pipeline handle unexpected failures or corrupted batches?
**Answer:**
> "We implement a three-tiered error handling and resilience pattern:
> 1. **ADF Retry Policies:** Every Copy Activity and Stored Procedure activity is configured with 3 retries at 30-second intervals to handle transient cloud networking blips.
> 2. **Pre-Copy Truncate on Staging:** Staging tables are truncated before new copy activities execute, preventing partial duplicate loads if an activity fails midway.
> 3. **Centralized Audit Logging:** Every activity wraps its execution with calls to `audit.sp_Log_PipelineExecution`. If an activity fails, ADF routes to `Log_Pipeline_Failure`, capturing the exact RunID, failed activity name, and SQL exception message, which immediately triggers a notification to DataOps."

---

## 3. Data Quality & Business Logic

### Q8: Why did you build a Python validation framework instead of relying purely on SQL check constraints?
**Answer:**
> "SQL constraints (`CHECK`, `NOT NULL`, `FOREIGN KEY`) are binary: they either succeed or abort the entire batch. In real-world enterprise retail data, third-party vendor feeds and POS terminals frequently produce minor anomalies (1–2% corrupted records).
>
> A modular Python framework offers substantial advantages:
> - **Granular Telemetry & Scoring:** It evaluates records without failing the pipeline immediately, computing a quantitative **Data Quality Score (0–100%)** and logging pass/fail percentages per rule.
> - **Complex Cross-Field Math:** Python can easily validate complex multi-column conservation equations, such as $ClosingStock = OpeningStock + Received - Sold + Returns - Damaged$, and flag broken equations before data enters the warehouse.
> - **Quality Gate Automation:** It enables configurable threshold policies (e.g., pass if $\ge 98\%$, warning if $95-98\%$, halt only if $< 95\%$), giving management visibility into data health rather than opaque pipeline crashes."

---

### Q9: How does the Stockout Risk algorithm work?
**Answer:**
> "The stockout calculation is implemented in `dw.sp_Update_InventoryMetrics`:
> 1. First, we compute the **Average Daily Sales (ADS)** for each Product and Store over the last 30 calendar days:
>    $$\text{ADS} = \frac{\sum_{t=-30}^{0} \text{QuantitySold}}{30}$$
> 2. We calculate **Days of Inventory (DOI)**:
>    $$\text{DOI} = \frac{\text{ClosingStock}}{\text{ADS}}$$
> 3. We classify each inventory line into actionable risk tiers:
>    - `CRITICAL`: $\text{DOI} \le 3$ days or $\text{ClosingStock} = 0$ (Immediate stockout risk; expedite stock transfer).
>    - `HIGH`: $\text{DOI} \in (3, 7]$ days (Trigger procurement replenishment PO).
>    - `MEDIUM`: $\text{DOI} \in (7, 14]$ days (Adequate safety buffer).
>    - `LOW`: $\text{DOI} > 14$ days (Healthy stock position).
> 4. Finally, `ReorderRequired` is flagged as `1` whenever $\text{ClosingStock} \le \text{ReorderLevel}$."

---

## 4. Scaling, Security & Power BI

### Q10: How would this architecture scale if sales volume grew from 120k rows to 100M+ rows?
**Answer:**
> "If data volume increased to 100M+ rows, I would evolve the architecture through the following optimizations:
> 1. **Partitioning:** Implement monthly table partitioning in Azure SQL Database on `dw.FactSales` using `DateKey` and partition switching for fast data retirement.
> 2. **Clustered Columnstore Indexes:** Switch `dw.FactSales` from a B-Tree clustered index to a Clustered Columnstore Index (CCI). CCIs provide 10x data compression and vector batch-mode query execution for analytical aggregations.
> 3. **ADF File Partitioning:** Ingest using ADF binary partition slices (`sales/year=2025/month=10/*.parquet`) rather than scanning monolithic folders.
> 4. **Compute Tier:** Scale Azure SQL Database to **Business Critical** or **Hyperscale** with Read Scale-Out replicas, routing Power BI reporting queries to read replicas to eliminate resource contention with ETL write loads."

---

### Q11: Why shouldn't Power BI connect directly to raw source CSV files?
**Answer:**
> "Connecting Power BI directly to raw CSV files is a classic junior mistake that creates significant production liabilities:
> 1. **Performance & Memory Overhead:** Parsing and transforming raw CSVs inside Power Query consumes massive client RAM and slows down report refresh times exponentially as row counts grow.
> 2. **Lack of Data Governance & Single Source of Truth:** Business logic, currency conversions, and deduplication rules become trapped inside `.pbix` M queries, unavailable to other systems or SQL consumers.
> 3. **No Quality Gate:** Corrupted CSV rows directly break dashboard visuals or distort executive revenue numbers with zero audit trail.
> By connecting Power BI to curated `dw.*` Star Schema tables in Azure SQL Database, we ensure Power BI queries pre-aggregated, validated, and indexed datasets with sub-second response times."
