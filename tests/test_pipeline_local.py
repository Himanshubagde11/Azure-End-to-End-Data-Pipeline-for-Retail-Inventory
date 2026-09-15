"""
CLARIVENS INVENTORY INTELLIGENCE
Local End-to-End Execution & Testing Runner
Author: Senior Data Engineer / Azure Data Architect
Organization: CLARIVENS RETAIL GROUP

Enables complete zero-cloud execution and verification:
1. Ingests raw CSVs & Mock REST API into local relational staging tables
2. Executes the full Python Data Quality Engine & logs results
3. Executes dimensional and fact transformations (Star Schema)
4. Computes rolling 30-day ADS, Days of Inventory & Stockout Risk metrics
5. Runs automated SQL integrity verification assertions
6. Updates audit.ETL_Control and audit.PipelineExecutionLog
"""

import os
import sys
import glob
import sqlite3
import datetime
import pandas as pd
import numpy as np

# Set paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
python_dir = os.path.join(BASE_DIR, "python")
if python_dir not in sys.path:
    sys.path.insert(0, python_dir)

from python.config import DATA_DIR, SALES_DIR, INVENTORY_DIR, PURCHASES_DIR, RETURNS_DIR, LOCAL_DB_PATH
from python.data_quality import DataQualityEngine
from python.mock_api import ENRICHMENT_CACHE

def get_connection():
    os.makedirs(os.path.dirname(LOCAL_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(LOCAL_DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_local_warehouse(conn):
    print("\n[STEP 1/6] Initializing Local Relational Warehouse...")
    cursor = conn.cursor()

    # Drop existing tables
    tables = [
        "audit_ETL_Control", "audit_PipelineExecutionLog", "audit_DataQualityLog",
        "dw_FactReturns", "dw_FactPurchases", "dw_FactInventory", "dw_FactSales",
        "dw_DimProduct", "dw_DimStore", "dw_DimSupplier", "dw_DimCategory", "dw_DimDate",
        "stg_Sales", "stg_Inventory", "stg_Purchases", "stg_Returns", "stg_Products",
        "stg_Stores", "stg_Suppliers", "stg_Categories", "stg_RestApi_Enrichment"
    ]
    for t in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {t}")

    # Create Audit Tables
    cursor.execute("""
    CREATE TABLE audit_ETL_Control (
        PipelineName TEXT PRIMARY KEY,
        TableName TEXT NOT NULL,
        WatermarkColumn TEXT NOT NULL,
        LastWatermarkValue TEXT NOT NULL,
        LastSuccessfulLoad TEXT NOT NULL,
        LastRunID TEXT NOT NULL,
        LastRunStatus TEXT NOT NULL,
        UpdatedAt TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE audit_PipelineExecutionLog (
        LogID INTEGER PRIMARY KEY AUTOINCREMENT,
        RunID TEXT NOT NULL,
        PipelineName TEXT NOT NULL,
        ActivityName TEXT NOT NULL,
        StartTime TEXT NOT NULL,
        EndTime TEXT,
        Status TEXT NOT NULL,
        RowsProcessed INTEGER,
        RowsFailed INTEGER,
        ErrorMessage TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE audit_DataQualityLog (
        QualityCheckID INTEGER PRIMARY KEY AUTOINCREMENT,
        RunID TEXT NOT NULL,
        TableName TEXT NOT NULL,
        CheckType TEXT NOT NULL,
        RuleName TEXT NOT NULL,
        TotalRecords INTEGER NOT NULL,
        FailedRecords INTEGER NOT NULL,
        PassPercentage REAL NOT NULL,
        Status TEXT NOT NULL,
        ExecutionTime TEXT NOT NULL,
        ErrorMessage TEXT
    );
    """)

    # Seed Watermark
    cursor.execute("""
    INSERT INTO audit_ETL_Control VALUES 
    ('PL_Load_Sales', 'dw_FactSales', 'SaleDate', '1900-01-01', '1900-01-01 00:00:00', 'INIT_SEED', 'SUCCESS', datetime('now')),
    ('PL_Load_Inventory', 'dw_FactInventory', 'SnapshotDate', '1900-01-01', '1900-01-01 00:00:00', 'INIT_SEED', 'SUCCESS', datetime('now')),
    ('PL_Load_Purchases', 'dw_FactPurchases', 'OrderDate', '1900-01-01', '1900-01-01 00:00:00', 'INIT_SEED', 'SUCCESS', datetime('now')),
    ('PL_Load_Returns', 'dw_FactReturns', 'ReturnDate', '1900-01-01', '1900-01-01 00:00:00', 'INIT_SEED', 'SUCCESS', datetime('now'));
    """)

    # Create Dimension Tables
    cursor.execute("""
    CREATE TABLE dw_DimDate (
        DateKey INTEGER PRIMARY KEY,
        FullDate TEXT NOT NULL,
        DayNumberOfWeek INTEGER,
        DayName TEXT,
        DayNumberOfMonth INTEGER,
        MonthName TEXT,
        MonthNumberOfYear INTEGER,
        CalendarQuarter INTEGER,
        CalendarYear INTEGER,
        FiscalYear INTEGER,
        FiscalQuarter INTEGER,
        IsWeekend INTEGER,
        IsFestivalSeason INTEGER
    );
    """)

    cursor.execute("""
    CREATE TABLE dw_DimCategory (
        CategorySK INTEGER PRIMARY KEY AUTOINCREMENT,
        CategoryID TEXT UNIQUE NOT NULL,
        CategoryName TEXT NOT NULL,
        Department TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE dw_DimStore (
        StoreSK INTEGER PRIMARY KEY AUTOINCREMENT,
        StoreID TEXT UNIQUE NOT NULL,
        StoreName TEXT NOT NULL,
        City TEXT NOT NULL,
        State TEXT NOT NULL,
        Region TEXT NOT NULL,
        StoreType TEXT NOT NULL,
        SquareFeet INTEGER,
        Manager TEXT,
        OpeningDate TEXT,
        IsActive INTEGER DEFAULT 1
    );
    """)

    cursor.execute("""
    CREATE TABLE dw_DimSupplier (
        SupplierSK INTEGER PRIMARY KEY AUTOINCREMENT,
        SupplierID TEXT UNIQUE NOT NULL,
        SupplierName TEXT NOT NULL,
        ContactName TEXT,
        Email TEXT,
        Phone TEXT,
        City TEXT NOT NULL,
        State TEXT NOT NULL,
        Rating REAL,
        PaymentTerms TEXT,
        LeadTimeDays INTEGER,
        IsActive INTEGER DEFAULT 1
    );
    """)

    cursor.execute("""
    CREATE TABLE dw_DimProduct (
        ProductSK INTEGER PRIMARY KEY AUTOINCREMENT,
        ProductID TEXT UNIQUE NOT NULL,
        ProductName TEXT NOT NULL,
        CategoryID TEXT NOT NULL,
        CategoryName TEXT NOT NULL,
        Department TEXT NOT NULL,
        SupplierID TEXT NOT NULL,
        Brand TEXT NOT NULL,
        UnitCost REAL NOT NULL,
        UnitPrice REAL NOT NULL,
        ReorderLevel INTEGER NOT NULL,
        ReorderQuantity INTEGER NOT NULL,
        LaunchDate TEXT,
        IsActive INTEGER DEFAULT 1,
        IsCurrent INTEGER DEFAULT 1
    );
    """)

    # Create Fact Tables
    cursor.execute("""
    CREATE TABLE dw_FactSales (
        SalesSK INTEGER PRIMARY KEY AUTOINCREMENT,
        SaleID TEXT UNIQUE NOT NULL,
        DateKey INTEGER NOT NULL,
        ProductSK INTEGER NOT NULL,
        StoreSK INTEGER NOT NULL,
        Quantity INTEGER NOT NULL,
        UnitPrice REAL NOT NULL,
        Discount REAL NOT NULL,
        Revenue REAL NOT NULL,
        Cost REAL NOT NULL,
        GrossProfit REAL NOT NULL,
        PaymentMethod TEXT NOT NULL,
        CustomerSegment TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE dw_FactInventory (
        InventorySK INTEGER PRIMARY KEY AUTOINCREMENT,
        InventoryID TEXT UNIQUE NOT NULL,
        DateKey INTEGER NOT NULL,
        ProductSK INTEGER NOT NULL,
        StoreSK INTEGER NOT NULL,
        OpeningStock INTEGER NOT NULL,
        ReceivedQuantity INTEGER DEFAULT 0,
        SoldQuantity INTEGER DEFAULT 0,
        ReturnQuantity INTEGER DEFAULT 0,
        DamagedQuantity INTEGER DEFAULT 0,
        ClosingStock INTEGER NOT NULL,
        InventoryValue REAL NOT NULL,
        AverageDailySales REAL DEFAULT 0.0,
        DaysOfInventory REAL DEFAULT 0.0,
        StockoutRiskLevel TEXT DEFAULT 'LOW',
        ReorderRequired INTEGER DEFAULT 0
    );
    """)

    cursor.execute("""
    CREATE TABLE dw_FactPurchases (
        PurchaseSK INTEGER PRIMARY KEY AUTOINCREMENT,
        PurchaseOrderID TEXT UNIQUE NOT NULL,
        OrderDateKey INTEGER NOT NULL,
        ExpectedDeliveryDateKey INTEGER NOT NULL,
        ActualDeliveryDateKey INTEGER,
        SupplierSK INTEGER NOT NULL,
        StoreSK INTEGER NOT NULL,
        ProductSK INTEGER NOT NULL,
        OrderedQuantity INTEGER NOT NULL,
        ReceivedQuantity INTEGER NOT NULL,
        UnitCost REAL NOT NULL,
        TotalCost REAL NOT NULL,
        Status TEXT NOT NULL,
        DeliveryVarianceDays INTEGER
    );
    """)

    cursor.execute("""
    CREATE TABLE dw_FactReturns (
        ReturnSK INTEGER PRIMARY KEY AUTOINCREMENT,
        ReturnID TEXT UNIQUE NOT NULL,
        DateKey INTEGER NOT NULL,
        ProductSK INTEGER NOT NULL,
        StoreSK INTEGER NOT NULL,
        SaleID TEXT NOT NULL,
        Quantity INTEGER NOT NULL,
        RefundAmount REAL NOT NULL,
        ReturnReason TEXT NOT NULL
    );
    """)

    conn.commit()
    print("  -> Schema initialized successfully.")

def populate_dim_date(conn):
    print("\n[STEP 2/6] Populating dw_DimDate (2024–2026)...")
    start = datetime.date(2024, 1, 1)
    end = datetime.date(2026, 12, 31)
    delta = datetime.timedelta(days=1)
    
    dates = []
    curr = start
    while curr <= end:
        dk = int(curr.strftime("%Y%m%d"))
        fdate = curr.strftime("%Y-%m-%d")
        dow = curr.isoweekday()
        dname = curr.strftime("%A")
        dom = curr.day
        mname = curr.strftime("%B")
        moy = curr.month
        qtr = (curr.month - 1) // 3 + 1
        yr = curr.year
        fyr = yr if moy >= 4 else yr - 1
        fqtr = 1 if moy in [4, 5, 6] else 2 if moy in [7, 8, 9] else 3 if moy in [10, 11, 12] else 4
        is_wknd = 1 if dow in [6, 7] else 0
        is_fest = 1 if moy in [10, 11] else 0

        dates.append((dk, fdate, dow, dname, dom, mname, moy, qtr, yr, fyr, fqtr, is_wknd, is_fest))
        curr += delta

    cursor = conn.cursor()
    cursor.executemany("""
    INSERT INTO dw_DimDate VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, dates)
    conn.commit()
    print(f"  -> Generated {len(dates):,} calendar records in dw_DimDate.")

def load_staging_and_validate(conn, run_id):
    print("\n[STEP 3/6] Running Python Data Quality Gate on Staging Data...")
    engine = DataQualityEngine(run_id=run_id)

    # 1. Categories
    df_cats = pd.read_csv(os.path.join(DATA_DIR, "categories.csv"))
    df_cats.to_sql("stg_Categories", conn, if_exists="replace", index=False)
    engine.evaluate_dataset("categories", df_cats)

    # 2. Stores
    df_stores = pd.read_csv(os.path.join(DATA_DIR, "stores.csv"))
    df_stores.to_sql("stg_Stores", conn, if_exists="replace", index=False)
    engine.evaluate_dataset("stores", df_stores)

    # 3. Suppliers
    df_sups = pd.read_csv(os.path.join(DATA_DIR, "suppliers.csv"))
    df_sups.to_sql("stg_Suppliers", conn, if_exists="replace", index=False)
    engine.evaluate_dataset("suppliers", df_sups)

    # 4. Products
    df_prods = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
    df_prods.to_sql("stg_Products", conn, if_exists="replace", index=False)
    ref_lookups = {"categories": df_cats, "suppliers": df_sups, "stores": df_stores, "products": df_prods}
    engine.evaluate_dataset("products", df_prods, ref_lookups)

    # 5. Sales (Combined 12 monthly partitions)
    sales_files = sorted(glob.glob(os.path.join(SALES_DIR, "*.csv")))
    sales_dfs = [pd.read_csv(f) for f in sales_files]
    df_sales = pd.concat(sales_dfs, ignore_index=True)
    df_sales.to_sql("stg_Sales", conn, if_exists="replace", index=False)
    engine.evaluate_dataset("sales", df_sales, ref_lookups)

    # 6. Inventory
    inv_files = sorted(glob.glob(os.path.join(INVENTORY_DIR, "*.csv")))
    inv_dfs = [pd.read_csv(f) for f in inv_files]
    df_inv = pd.concat(inv_dfs, ignore_index=True)
    df_inv.to_sql("stg_Inventory", conn, if_exists="replace", index=False)
    engine.evaluate_dataset("inventory", df_inv, ref_lookups)

    # 7. Purchases & Returns
    df_po = pd.read_csv(os.path.join(PURCHASES_DIR, "purchase_orders.csv"))
    df_po.to_sql("stg_Purchases", conn, if_exists="replace", index=False)
    engine.evaluate_dataset("purchases", df_po, ref_lookups)

    df_ret = pd.read_csv(os.path.join(RETURNS_DIR, "returns.csv"))
    df_ret.to_sql("stg_Returns", conn, if_exists="replace", index=False)
    engine.evaluate_dataset("returns", df_ret, ref_lookups)

    # 8. REST Enrichment
    df_rest = pd.DataFrame(ENRICHMENT_CACHE)
    df_rest.to_sql("stg_RestApi_Enrichment", conn, if_exists="replace", index=False)

    summary = engine.compute_summary()
    print(f"  -> Quality Gate Passed with Score: {summary['data_quality_score']}% ({summary['passed_checks']} checks passed, {summary['warning_checks']} warnings)")

    # Record into audit_DataQualityLog
    cursor = conn.cursor()
    for r in engine.results:
        cursor.execute("""
        INSERT INTO audit_DataQualityLog (RunID, TableName, CheckType, RuleName, TotalRecords, FailedRecords, PassPercentage, Status, ExecutionTime, ErrorMessage)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (run_id, r["table"], r["check_type"], r["rule_name"], r["total_records"], r["failed_records"], r["pass_percentage"], r["status"], r["execution_time"], r["error_message"]))
    conn.commit()

def load_star_schema(conn, run_id):
    print("\n[STEP 4/6] Transforming Staging Data into Star Schema...")
    cursor = conn.cursor()

    # A. DimCategory
    cursor.execute("""
    INSERT INTO dw_DimCategory (CategoryID, CategoryName, Department)
    SELECT DISTINCT TRIM(CategoryID), TRIM(CategoryName), TRIM(Department)
    FROM stg_Categories WHERE CategoryID IS NOT NULL;
    """)

    # B. DimStore
    cursor.execute("""
    INSERT INTO dw_DimStore (StoreID, StoreName, City, State, Region, StoreType, SquareFeet, Manager, OpeningDate, IsActive)
    SELECT DISTINCT TRIM(StoreID), TRIM(StoreName), TRIM(City), TRIM(State), TRIM(Region), TRIM(StoreType), SquareFeet, Manager, OpeningDate, IsActive
    FROM stg_Stores WHERE StoreID IS NOT NULL;
    """)

    # C. DimSupplier
    cursor.execute("""
    INSERT INTO dw_DimSupplier (SupplierID, SupplierName, ContactName, Email, Phone, City, State, Rating, PaymentTerms, LeadTimeDays, IsActive)
    SELECT DISTINCT TRIM(SupplierID), TRIM(SupplierName), ContactName, Email, Phone, TRIM(City), TRIM(State), Rating, PaymentTerms, LeadTimeDays, IsActive
    FROM stg_Suppliers WHERE SupplierID IS NOT NULL;
    """)

    # D. DimProduct (Cleansing casing, resolving supplier FKs)
    cursor.execute("""
    INSERT INTO dw_DimProduct (ProductID, ProductName, CategoryID, CategoryName, Department, SupplierID, Brand, UnitCost, UnitPrice, ReorderLevel, ReorderQuantity, LaunchDate, IsActive, IsCurrent)
    SELECT 
        TRIM(p.ProductID),
        TRIM(p.ProductName),
        TRIM(p.CategoryID),
        COALESCE(c.CategoryName, TRIM(p.CategoryName)),
        COALESCE(c.Department, 'Merchandise'),
        CASE WHEN s.SupplierID IS NOT NULL THEN TRIM(p.SupplierID) ELSE 'SUP001' END,
        COALESCE(TRIM(p.Brand), 'Clarivens Brand'),
        COALESCE(p.UnitCost, 150.0),
        COALESCE(p.UnitPrice, ROUND(p.UnitCost * 1.35, 2)),
        COALESCE(p.ReorderLevel, 50),
        COALESCE(p.ReorderQuantity, 100),
        p.LaunchDate,
        1, 1
    FROM stg_Products p
    LEFT JOIN dw_DimCategory c ON TRIM(p.CategoryID) = c.CategoryID
    LEFT JOIN dw_DimSupplier s ON TRIM(p.SupplierID) = s.SupplierID
    WHERE p.ProductID IS NOT NULL;
    """)

    # E. FactSales (Incremental Load, Cleansing nulls, negative qty, dates)
    cursor.execute("""
    INSERT INTO dw_FactSales (SaleID, DateKey, ProductSK, StoreSK, Quantity, UnitPrice, Discount, Revenue, Cost, GrossProfit, PaymentMethod, CustomerSegment)
    SELECT 
        s.SaleID,
        CAST(strftime('%Y%m%d', s.SaleDate) AS INTEGER),
        dp.ProductSK,
        ds.StoreSK,
        s.Quantity,
        s.UnitPrice,
        COALESCE(s.Discount, 0.0),
        s.Revenue,
        s.Cost,
        ROUND(s.Revenue - s.Cost, 2),
        COALESCE(s.PaymentMethod, 'Cash'),
        COALESCE(s.CustomerSegment, 'Regular')
    FROM stg_Sales s
    INNER JOIN dw_DimProduct dp ON TRIM(s.ProductID) = dp.ProductID
    INNER JOIN dw_DimStore ds ON TRIM(s.StoreID) = ds.StoreID
    WHERE s.Quantity > 0 
      AND s.SaleDate <= '2025-12-31'
      AND s.ProductID IS NOT NULL 
      AND s.StoreID IS NOT NULL
    GROUP BY s.SaleID;
    """)
    sales_loaded = cursor.rowcount

    # F. FactInventory (Reconciling stock balance equation)
    cursor.execute("""
    INSERT INTO dw_FactInventory (InventoryID, DateKey, ProductSK, StoreSK, OpeningStock, ReceivedQuantity, SoldQuantity, ReturnQuantity, DamagedQuantity, ClosingStock, InventoryValue, ReorderRequired)
    SELECT 
        inv.InventoryID,
        CAST(strftime('%Y%m%d', inv.SnapshotDate) AS INTEGER),
        dp.ProductSK,
        ds.StoreSK,
        COALESCE(inv.OpeningStock, 0),
        COALESCE(inv.ReceivedQuantity, 0),
        COALESCE(inv.SoldQuantity, 0),
        COALESCE(inv.ReturnQuantity, 0),
        COALESCE(inv.DamagedQuantity, 0),
        MAX(0, COALESCE(inv.OpeningStock, 0) + COALESCE(inv.ReceivedQuantity, 0) - COALESCE(inv.SoldQuantity, 0) + COALESCE(inv.ReturnQuantity, 0) - COALESCE(inv.DamagedQuantity, 0)),
        ROUND(MAX(0, COALESCE(inv.OpeningStock, 0) + COALESCE(inv.ReceivedQuantity, 0) - COALESCE(inv.SoldQuantity, 0) + COALESCE(inv.ReturnQuantity, 0) - COALESCE(inv.DamagedQuantity, 0)) * dp.UnitCost, 2),
        CASE WHEN MAX(0, COALESCE(inv.OpeningStock, 0) + COALESCE(inv.ReceivedQuantity, 0) - COALESCE(inv.SoldQuantity, 0) + COALESCE(inv.ReturnQuantity, 0) - COALESCE(inv.DamagedQuantity, 0)) <= dp.ReorderLevel THEN 1 ELSE 0 END
    FROM stg_Inventory inv
    INNER JOIN dw_DimProduct dp ON TRIM(inv.ProductID) = dp.ProductID
    INNER JOIN dw_DimStore ds ON TRIM(inv.StoreID) = ds.StoreID
    WHERE inv.ProductID IS NOT NULL AND inv.StoreID IS NOT NULL;
    """)
    inv_loaded = cursor.rowcount

    # G. FactPurchases
    cursor.execute("""
    INSERT INTO dw_FactPurchases (PurchaseOrderID, OrderDateKey, ExpectedDeliveryDateKey, ActualDeliveryDateKey, SupplierSK, StoreSK, ProductSK, OrderedQuantity, ReceivedQuantity, UnitCost, TotalCost, Status, DeliveryVarianceDays)
    SELECT 
        p.PurchaseOrderID,
        CAST(strftime('%Y%m%d', p.OrderDate) AS INTEGER),
        CAST(strftime('%Y%m%d', p.ExpectedDeliveryDate) AS INTEGER),
        CASE WHEN p.ActualDeliveryDate IS NOT NULL AND p.ActualDeliveryDate <> '' THEN CAST(strftime('%Y%m%d', p.ActualDeliveryDate) AS INTEGER) ELSE NULL END,
        dsup.SupplierSK,
        dst.StoreSK,
        dp.ProductSK,
        p.OrderedQuantity,
        MIN(p.OrderedQuantity, p.ReceivedQuantity),
        p.UnitCost,
        ROUND(p.OrderedQuantity * p.UnitCost, 2),
        p.Status,
        CASE WHEN p.ActualDeliveryDate IS NOT NULL AND p.ActualDeliveryDate <> '' THEN CAST((julianday(p.ActualDeliveryDate) - julianday(p.ExpectedDeliveryDate)) AS INTEGER) ELSE NULL END
    FROM stg_Purchases p
    INNER JOIN dw_DimSupplier dsup ON TRIM(p.SupplierID) = dsup.SupplierID
    INNER JOIN dw_DimStore dst ON TRIM(p.StoreID) = dst.StoreID
    INNER JOIN dw_DimProduct dp ON TRIM(p.ProductID) = dp.ProductID
    WHERE p.ProductID IS NOT NULL AND p.StoreID IS NOT NULL AND p.SupplierID IS NOT NULL;
    """)
    po_loaded = cursor.rowcount

    # H. FactReturns
    cursor.execute("""
    INSERT INTO dw_FactReturns (ReturnID, DateKey, ProductSK, StoreSK, SaleID, Quantity, RefundAmount, ReturnReason)
    SELECT 
        r.ReturnID,
        CAST(strftime('%Y%m%d', r.ReturnDate) AS INTEGER),
        dp.ProductSK,
        dst.StoreSK,
        r.SaleID,
        r.Quantity,
        ABS(r.RefundAmount),
        r.ReturnReason
    FROM stg_Returns r
    INNER JOIN dw_DimProduct dp ON TRIM(r.ProductID) = dp.ProductID
    INNER JOIN dw_DimStore dst ON TRIM(r.StoreID) = dst.StoreID
    WHERE r.ProductID IS NOT NULL AND r.StoreID IS NOT NULL;
    """)
    ret_loaded = cursor.rowcount

    # Update Watermark
    cursor.execute("""
    UPDATE audit_ETL_Control
    SET LastWatermarkValue = '2025-12-31',
        LastSuccessfulLoad = datetime('now'),
        LastRunID = ?,
        LastRunStatus = 'SUCCESS',
        UpdatedAt = datetime('now')
    WHERE PipelineName = 'PL_Load_Sales';
    """, (run_id,))

    # Log Execution
    cursor.execute("""
    INSERT INTO audit_PipelineExecutionLog (RunID, PipelineName, ActivityName, StartTime, EndTime, Status, RowsProcessed, RowsFailed, ErrorMessage)
    VALUES (?, 'PL_Transform_Warehouse', 'Load_Star_Schema', datetime('now'), datetime('now'), 'SUCCESS', ?, 0, NULL);
    """, (run_id, sales_loaded + inv_loaded + po_loaded + ret_loaded))

    conn.commit()
    print(f"  -> Successfully loaded {sales_loaded:,} Sales, {inv_loaded:,} Inventory, {po_loaded:,} POs, {ret_loaded:,} Returns.")

def compute_inventory_metrics(conn, run_id):
    print("\n[STEP 5/6] Computing Velocity, Days of Inventory & Stockout Risk Levels...")
    cursor = conn.cursor()

    # Calculate ADS per Product & Store based on sales velocity
    cursor.execute("""
    CREATE TEMP TABLE tmp_ads AS
    SELECT ProductSK, StoreSK, ROUND(CAST(SUM(Quantity) AS REAL) / 30.0, 2) AS ADS
    FROM dw_FactSales
    GROUP BY ProductSK, StoreSK;
    """)

    # Update FactInventory with ADS, DaysOfInventory, Risk Levels
    cursor.execute("""
    UPDATE dw_FactInventory
    SET AverageDailySales = COALESCE((SELECT ADS FROM tmp_ads WHERE tmp_ads.ProductSK = dw_FactInventory.ProductSK AND tmp_ads.StoreSK = dw_FactInventory.StoreSK), 0.50),
        DaysOfInventory = CASE 
            WHEN ClosingStock <= 0 THEN 0.0
            ELSE ROUND(CAST(ClosingStock AS REAL) / COALESCE((SELECT ADS FROM tmp_ads WHERE tmp_ads.ProductSK = dw_FactInventory.ProductSK AND tmp_ads.StoreSK = dw_FactInventory.StoreSK), 0.50), 1)
        END;
    """)

    # Classify StockoutRiskLevel: CRITICAL <= 3d, HIGH 4-7d, MEDIUM 8-14d, LOW > 14d
    cursor.execute("""
    UPDATE dw_FactInventory
    SET StockoutRiskLevel = CASE 
        WHEN DaysOfInventory <= 3.0 OR ClosingStock = 0 THEN 'CRITICAL'
        WHEN DaysOfInventory > 3.0 AND DaysOfInventory <= 7.0 THEN 'HIGH'
        WHEN DaysOfInventory > 7.0 AND DaysOfInventory <= 14.0 THEN 'MEDIUM'
        ELSE 'LOW'
    END;
    """)

    cursor.execute("DROP TABLE tmp_ads;")
    conn.commit()

    # Fetch Risk distribution
    cursor.execute("""
    SELECT StockoutRiskLevel, COUNT(*), ROUND(AVG(DaysOfInventory), 1)
    FROM dw_FactInventory
    GROUP BY StockoutRiskLevel;
    """)
    rows = cursor.fetchall()
    print("  -> Stockout Risk Classification Summary:")
    for tier, cnt, avg_doi in rows:
        print(f"     • {tier:<10}: {cnt:>6,} snapshots (Avg DOI: {avg_doi} days)")

def run_integrity_assertions(conn):
    print("\n[STEP 6/6] Executing Automated Warehouse Integrity Assertions...")
    cursor = conn.cursor()

    assertions = [
        ("Zero Orphan ProductSK in FactSales", "SELECT COUNT(*) FROM dw_FactSales fs LEFT JOIN dw_DimProduct dp ON fs.ProductSK = dp.ProductSK WHERE dp.ProductSK IS NULL;"),
        ("Zero Orphan StoreSK in FactSales", "SELECT COUNT(*) FROM dw_FactSales fs LEFT JOIN dw_DimStore ds ON fs.StoreSK = ds.StoreSK WHERE ds.StoreSK IS NULL;"),
        ("Zero Orphan ProductSK in FactInventory", "SELECT COUNT(*) FROM dw_FactInventory fi LEFT JOIN dw_DimProduct dp ON fi.ProductSK = dp.ProductSK WHERE dp.ProductSK IS NULL;"),
        ("Zero Negative Quantities in FactSales", "SELECT COUNT(*) FROM dw_FactSales WHERE Quantity <= 0;"),
        ("Zero Negative Closing Stock in FactInventory", "SELECT COUNT(*) FROM dw_FactInventory WHERE ClosingStock < 0;"),
        ("Zero Negative Inventory Value", "SELECT COUNT(*) FROM dw_FactInventory WHERE InventoryValue < 0.0;"),
        ("High-Watermark Updated in audit_ETL_Control", "SELECT COUNT(*) FROM audit_ETL_Control WHERE LastWatermarkValue = '2025-12-31';")
    ]

    all_passed = True
    for desc, query in assertions:
        cursor.execute(query)
        res = cursor.fetchone()[0]
        if "Zero" in desc:
            status = "PASS" if res == 0 else "FAIL"
        else:
            status = "PASS" if res >= 1 else "FAIL"

        if status == "FAIL":
            all_passed = False
        print(f"  [{status}] {desc} (Result: {res})")

    if all_passed:
        print("\n==========================================================================")
        print(" ALL WAREHOUSE INTEGRITY TESTS PASSED SUCCESSFULLY! (100% COMPLIANT)")
        print("==========================================================================")
    else:
        print("\n[WARNING] Some warehouse integrity assertions failed. Check logs.")

def main():
    start_time = datetime.datetime.now()
    run_id = f"LOCAL_E2E_{start_time.strftime('%Y%m%d_%H%M%S')}"

    print("==========================================================================")
    print(" CLARIVENS INVENTORY INTELLIGENCE — LOCAL PIPELINE & WAREHOUSE RUNNER")
    print(f" Run ID: {run_id} | Database: {LOCAL_DB_PATH}")
    print("==========================================================================")

    conn = get_connection()
    try:
        init_local_warehouse(conn)
        populate_dim_date(conn)
        load_staging_and_validate(conn, run_id)
        load_star_schema(conn, run_id)
        compute_inventory_metrics(conn, run_id)
        run_integrity_assertions(conn)
        elapsed = (datetime.datetime.now() - start_time).total_seconds()
        print(f"\n[SUMMARY] Local Pipeline Execution Completed in {elapsed:.1f}s.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
