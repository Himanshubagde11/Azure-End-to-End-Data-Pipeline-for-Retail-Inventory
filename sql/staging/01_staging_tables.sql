-- ============================================================================
-- NEXORA INVENTORY INTELLIGENCE
-- Script: 01_staging_tables.sql
-- Description: Creates raw ingestion staging tables in the 'stg' schema
-- Author: Senior Data Engineer / Azure Data Architect
-- Organization: NEXORA RETAIL GROUP
-- ============================================================================

-- Drop existing staging tables if recreating
DROP TABLE IF EXISTS stg.Categories;
DROP TABLE IF EXISTS stg.Products;
DROP TABLE IF EXISTS stg.Stores;
DROP TABLE IF EXISTS stg.Suppliers;
DROP TABLE IF EXISTS stg.Sales;
DROP TABLE IF EXISTS stg.Inventory;
DROP TABLE IF EXISTS stg.Purchases;
DROP TABLE IF EXISTS stg.Returns;
DROP TABLE IF EXISTS stg.RestApi_ProductEnrichment;
GO

-- 1. Staging Categories
CREATE TABLE stg.Categories (
    CategoryID      VARCHAR(50)  NULL,
    CategoryName    VARCHAR(100) NULL,
    Department      VARCHAR(100) NULL,
    _IngestionTimestamp DATETIME2 DEFAULT SYSUTCDATETIME()
);
GO

-- 2. Staging Products
CREATE TABLE stg.Products (
    ProductID       VARCHAR(50)  NULL,
    ProductName     VARCHAR(255) NULL,
    CategoryID      VARCHAR(50)  NULL,
    CategoryName    VARCHAR(100) NULL,
    SupplierID      VARCHAR(50)  NULL,
    Brand           VARCHAR(100) NULL,
    UnitCost        DECIMAL(18,4) NULL,
    UnitPrice       DECIMAL(18,4) NULL,
    ReorderLevel    INT          NULL,
    ReorderQuantity INT          NULL,
    LaunchDate      VARCHAR(50)  NULL,
    IsActive        INT          NULL,
    _IngestionTimestamp DATETIME2 DEFAULT SYSUTCDATETIME()
);
GO

-- 3. Staging Stores
CREATE TABLE stg.Stores (
    StoreID         VARCHAR(50)  NULL,
    StoreName       VARCHAR(150) NULL,
    City            VARCHAR(100) NULL,
    State           VARCHAR(100) NULL,
    Region          VARCHAR(50)  NULL,
    StoreType       VARCHAR(50)  NULL,
    OpeningDate     VARCHAR(50)  NULL,
    Manager         VARCHAR(150) NULL,
    SquareFeet      INT          NULL,
    IsActive        INT          NULL,
    _IngestionTimestamp DATETIME2 DEFAULT SYSUTCDATETIME()
);
GO

-- 4. Staging Suppliers
CREATE TABLE stg.Suppliers (
    SupplierID      VARCHAR(50)  NULL,
    SupplierName    VARCHAR(150) NULL,
    ContactName     VARCHAR(150) NULL,
    Email           VARCHAR(150) NULL,
    Phone           VARCHAR(50)  NULL,
    City            VARCHAR(100) NULL,
    State           VARCHAR(100) NULL,
    Rating          DECIMAL(4,2) NULL,
    PaymentTerms    VARCHAR(50)  NULL,
    LeadTimeDays    INT          NULL,
    IsActive        INT          NULL,
    _IngestionTimestamp DATETIME2 DEFAULT SYSUTCDATETIME()
);
GO

-- 5. Staging Sales
CREATE TABLE stg.Sales (
    SaleID          VARCHAR(50)   NULL,
    SaleDate        VARCHAR(50)   NULL,
    StoreID         VARCHAR(50)   NULL,
    ProductID       VARCHAR(50)   NULL,
    Quantity        INT           NULL,
    UnitPrice       DECIMAL(18,4) NULL,
    Discount        DECIMAL(5,2)  NULL,
    Revenue         DECIMAL(18,4) NULL,
    Cost            DECIMAL(18,4) NULL,
    PaymentMethod   VARCHAR(50)   NULL,
    CustomerSegment VARCHAR(50)   NULL,
    _IngestionTimestamp DATETIME2 DEFAULT SYSUTCDATETIME()
);
GO

-- 6. Staging Inventory Snapshots
CREATE TABLE stg.Inventory (
    InventoryID      VARCHAR(50)   NULL,
    SnapshotDate     VARCHAR(50)   NULL,
    StoreID          VARCHAR(50)   NULL,
    ProductID        VARCHAR(50)   NULL,
    OpeningStock     INT           NULL,
    ReceivedQuantity INT           NULL,
    SoldQuantity     INT           NULL,
    ReturnQuantity   INT           NULL,
    ClosingStock     INT           NULL,
    DamagedQuantity  INT           NULL,
    InventoryValue   DECIMAL(18,4) NULL,
    _IngestionTimestamp DATETIME2 DEFAULT SYSUTCDATETIME()
);
GO

-- 7. Staging Purchases
CREATE TABLE stg.Purchases (
    PurchaseOrderID      VARCHAR(50)   NULL,
    OrderDate            VARCHAR(50)   NULL,
    SupplierID           VARCHAR(50)   NULL,
    StoreID              VARCHAR(50)   NULL,
    ProductID            VARCHAR(50)   NULL,
    OrderedQuantity      INT           NULL,
    ReceivedQuantity     INT           NULL,
    UnitCost             DECIMAL(18,4) NULL,
    ExpectedDeliveryDate VARCHAR(50)   NULL,
    ActualDeliveryDate   VARCHAR(50)   NULL,
    Status               VARCHAR(50)   NULL,
    _IngestionTimestamp  DATETIME2 DEFAULT SYSUTCDATETIME()
);
GO

-- 8. Staging Returns
CREATE TABLE stg.Returns (
    ReturnID        VARCHAR(50)   NULL,
    ReturnDate      VARCHAR(50)   NULL,
    SaleID          VARCHAR(50)   NULL,
    StoreID         VARCHAR(50)   NULL,
    ProductID       VARCHAR(50)   NULL,
    Quantity        INT           NULL,
    ReturnReason    VARCHAR(100)  NULL,
    RefundAmount    DECIMAL(18,4) NULL,
    _IngestionTimestamp DATETIME2 DEFAULT SYSUTCDATETIME()
);
GO

-- 9. Staging REST API Product / Replenishment Enrichment
CREATE TABLE stg.RestApi_ProductEnrichment (
    ProductID               VARCHAR(50)   NULL,
    SupplierID              VARCHAR(50)   NULL,
    LiveReplenishmentPrice  DECIMAL(18,4) NULL,
    RecommendedSafetyStock  INT           NULL,
    VendorLeadTimeDays      INT           NULL,
    SupplyChainRiskScore    DECIMAL(4,2)  NULL,
    LastEvaluatedDate       VARCHAR(50)   NULL,
    _IngestionTimestamp     DATETIME2 DEFAULT SYSUTCDATETIME()
);
GO

PRINT 'Staging tables in [stg] schema created successfully.';
GO
