# CLARIVENS INVENTORY INTELLIGENCE — PIPELINE DOCUMENTATION
**Organization:** CLARIVENS RETAIL GROUP  
**Platform:** Azure Data Factory (ADF) & Azure SQL Warehouse  
**Version:** 1.0.0 (Production Architecture)

---

## 1. Pipeline Architecture Overview

The **Clarivens Inventory Intelligence** ingestion and transformation engine is built upon **Azure Data Factory v2 (ADF)**. The platform orchestrates multi-source ingestion (Cloud Storage CSVs & REST API), triggers automated Python Data Quality gates, drives incremental watermarked loading into Azure SQL Database, and updates analytical warehouse dimensions and facts in strict dependency order.

```mermaid
flowchart TD
    subgraph Source["Source Layer"]
        CSV_Sales["sales/*.csv (ADLS Gen2)"]
        CSV_Inv["inventory/*.csv (ADLS Gen2)"]
        CSV_Master["products, stores, suppliers (ADLS Gen2)"]
        REST_API["Mock REST API (Catalog/Replenishment)"]
    end

    subgraph ADF["Azure Data Factory (PL_Master_Retail_Inventory)"]
        TR_Schedule["TR_Daily_Inventory_Schedule"]
        TR_Tumbling["TR_Monthly_Sales_TumblingWindow"]
        
        subgraph StageLoad["1. Staging Ingestion"]
            PL_M["PL_Load_Products / Stores / Suppliers"]
            PL_S["PL_Load_Sales (Watermark Parameterized)"]
            PL_I["PL_Load_Inventory"]
            PL_P["PL_Load_Purchases / Returns"]
            PL_R["PL_Load_REST_API (Paginated Copy)"]
        end

        subgraph QualityGate["2. Data Quality Gate"]
            PL_DQ["PL_Data_Quality_Check (Python Validation Engine)"]
            Gate_Cond{"DQ Score >= 95%?"}
        end

        subgraph Warehouse["3. Star Schema Transformation"]
            PL_WH["PL_Transform_Warehouse"]
            Dims["sp_Load_DimDate -> DimCategory -> DimSupplier -> DimStore -> DimProduct"]
            Facts["sp_Load_FactSales -> FactInventory -> FactPurchases -> FactReturns"]
            Metrics["sp_Update_InventoryMetrics"]
        end

        subgraph Logging["4. Telemetry & Observability"]
            Log_Start["Log_Pipeline_Start"]
            Log_Success["Log_Pipeline_Success"]
            Log_Fail["Log_Pipeline_Failure"]
        end
    end

    subgraph Target["Azure SQL Database"]
        STG["stg.* Tables"]
        AUDIT["audit.PipelineExecutionLog / audit.DataQualityLog / audit.ETL_Control"]
        DW["dw.* Dimensions & Facts"]
    end

    TR_Schedule --> Log_Start
    TR_Tumbling --> PL_S
    Log_Start --> StageLoad
    CSV_Master --> PL_M --> STG
    CSV_Sales --> PL_S --> STG
    CSV_Inv --> PL_I --> STG
    CSV_Master --> PL_P --> STG
    REST_API --> PL_R --> STG

    StageLoad --> PL_DQ
    PL_DQ --> AUDIT
    PL_DQ --> Gate_Cond
    Gate_Cond -- Yes --> PL_WH
    Gate_Cond -- No --> Log_Fail

    PL_WH --> Dims --> Facts --> Metrics --> DW
    PL_WH --> Log_Success --> AUDIT
    Log_Fail --> AUDIT
```

---

## 2. Pipeline Inventory

| Pipeline Name | Type | Ingestion Source | Target Object | Purpose & Schedule |
| :--- | :--- | :--- | :--- | :--- |
| `PL_Master_Retail_Inventory` | Orchestrator | Controller | Multi-Table | End-to-end master controller; scheduled daily at 23:30 IST. |
| `PL_Load_Products` | Ingestion | `products.csv` | `stg.Products` | Full truncation and ingestion of product master catalog. |
| `PL_Load_Stores` | Ingestion | `stores.csv` | `stg.Stores` | Full truncation and ingestion of store master directory. |
| `PL_Load_Suppliers` | Ingestion | `suppliers.csv` | `stg.Suppliers` | Ingestion of vendor directory and SLA terms. |
| `PL_Load_Sales` | Incremental | `sales/*.csv` | `stg.Sales` | Generic parameterized incremental loader based on high-watermark. |
| `PL_Load_Inventory` | Ingestion | `inventory/*.csv` | `stg.Inventory` | Weekly inventory snapshot ingestion across all stores. |
| `PL_Load_Purchases` | Ingestion | `purchases/purchase_orders.csv` | `stg.Purchases` | Procurement PO status and fulfillment ingestion. |
| `PL_Load_Returns` | Ingestion | `returns/returns.csv` | `stg.Returns` | Customer return transaction ingestion. |
| `PL_Load_REST_API` | Ingestion | REST Endpoint | `stg.RestApi_ProductEnrichment` | Paginated HTTP REST copy activity with live replenishment recommendations. |
| `PL_Data_Quality_Check` | Validation | Web / Custom | `audit.DataQualityLog` | Executes Python Data Quality Engine; halts pipeline if score < 95%. |
| `PL_Transform_Warehouse` | Transformation | SQL Stored Procs | `dw.*` Star Schema | Transforms cleansed staging into Dimensions, Facts, and calculated metrics. |

---

## 3. Parameterization & Reusability Pattern

To avoid creating duplicate pipelines for every new entity, `PL_Load_Sales` implements the **Generic Parameterized Ingestion Pattern**:

```json
{
  "p_Container": "raw-data",
  "p_SourceFolder": "sales",
  "p_SourceFile": "sales_2025_*.csv",
  "p_TargetTable": "Sales",
  "p_RunID": "@pipeline().RunId"
}
```

### Dataset Level Parameterization (`DS_CSV_Generic`):
- `p_Container`: Dynamically targets storage container (`raw-data`, `archive`, `test`).
- `p_FolderPath`: Subdirectory path (`sales`, `inventory`, `purchases`).
- `p_FileName`: Specific filename or wildcard pattern (`sales_2025_01.csv`, `*.csv`).
- `p_Delimiter`: Comma, tab, pipe, or semicolon delimiter.

### Dataset Level Parameterization (`DS_SQL_Generic`):
- `p_SchemaName`: Dynamic schema target (`stg`, `dw`, `audit`).
- `p_TableName`: Dynamic table sink (`Sales`, `Inventory`, `Products`).

---

## 4. Incremental Watermark Loading (`audit.ETL_Control`)

Clarivens Inventory Intelligence avoids full historical table scans by using a dedicated **High-Watermark Control Table**:

```sql
SELECT 
    PipelineName, TableName, WatermarkColumn, 
    LastWatermarkValue, LastSuccessfulLoad 
FROM audit.ETL_Control;
```

### Incremental Ingestion Workflow:
1. **Lookup Activity**: Queries `audit.ETL_Control` to fetch `LastWatermarkValue` for `PL_Load_Sales` (e.g. `'2025-10-31'`).
2. **Delta Extraction**: Ingests new records where `SaleDate > LastWatermarkValue`.
3. **Key Resolution**: Stored procedure `dw.sp_Load_FactSales` joins with current active dimensions (`IsCurrent = 1`).
4. **Watermark Update**: Upon successful commit, `audit.ETL_Control` is updated with `MAX(SaleDate)` from the ingested batch (e.g. `'2025-11-30'`).

---

## 5. REST API Ingestion Details

The REST API component ingests live market pricing and recommended safety stock from external vendor feeds:

- **Endpoint:** `http://127.0.0.1:8080/api/v1/products/enrichment`
- **Method:** `GET`
- **Authentication:** HTTP Header `Authorization: Bearer clarivens-api-prod-key-2025`
- **Pagination Strategy:**
  - Response payload includes `nextPageUrl` in the metadata header.
  - ADF REST Source uses dynamic `paginationRules`:
    ```json
    "paginationRules": {
      "AbsoluteUrl": "$.metadata.nextPageUrl"
    }
    ```
- **Error Handling & Retries:** 3 retries at 30-second intervals.
- **Mapping:** Tabular translator unpacks nested `$['data']` JSON arrays into `stg.RestApi_ProductEnrichment`.

---

## 6. Centralized Logging & Error Handling

All activities log execution telemetry directly to `audit.PipelineExecutionLog` via stored procedure `audit.sp_Log_PipelineExecution`:

- **Execution States:**
  - `RUNNING`: Emitted when pipeline or activity begins.
  - `SUCCESS`: Emitted upon clean completion with row counts (`RowsProcessed`).
  - `WARNING`: Emitted if data quality issues are detected but within acceptable thresholds.
  - `FAILED`: Emitted on activity failure with SQL error message or HTTP failure details.
- **Alert Notification:** When `Log_Pipeline_Failure` fires, ADF publishes an event trigger to the DataOps operations team.
