-- ============================================================================
-- CLARIVENS INVENTORY INTELLIGENCE
-- Script: 03_fact_tables.sql
-- Description: Creates Star Schema fact tables in the 'dw' schema
-- Author: Senior Data Engineer / Azure Data Architect
-- Organization: CLARIVENS RETAIL GROUP
-- ============================================================================

DROP TABLE IF EXISTS dw.FactReturns;
DROP TABLE IF EXISTS dw.FactPurchases;
DROP TABLE IF EXISTS dw.FactInventory;
DROP TABLE IF EXISTS dw.FactSales;
GO

-- 1. Fact Sales Table
CREATE TABLE dw.FactSales (
    SalesSK             BIGINT IDENTITY(1,1) NOT NULL,
    SaleID              VARCHAR(30)          NOT NULL,
    DateKey             INT                  NOT NULL,
    ProductSK           INT                  NOT NULL,
    StoreSK             INT                  NOT NULL,
    Quantity            INT                  NOT NULL,
    UnitPrice           DECIMAL(18,2)        NOT NULL,
    Discount            DECIMAL(5,2)         NOT NULL DEFAULT 0.00,
    Revenue             DECIMAL(18,2)        NOT NULL,
    Cost                DECIMAL(18,2)        NOT NULL,
    GrossProfit         DECIMAL(18,2)        NOT NULL,
    PaymentMethod       VARCHAR(30)          NOT NULL,
    CustomerSegment     VARCHAR(30)          NOT NULL,
    ETL_LoadTime        DATETIME2            NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_FactSales PRIMARY KEY CLUSTERED (SalesSK),
    CONSTRAINT FK_FactSales_DateKey FOREIGN KEY (DateKey) REFERENCES dw.DimDate(DateKey),
    CONSTRAINT FK_FactSales_ProductSK FOREIGN KEY (ProductSK) REFERENCES dw.DimProduct(ProductSK),
    CONSTRAINT FK_FactSales_StoreSK FOREIGN KEY (StoreSK) REFERENCES dw.DimStore(StoreSK)
);
GO

-- 2. Fact Inventory Snapshots Table
CREATE TABLE dw.FactInventory (
    InventorySK         BIGINT IDENTITY(1,1) NOT NULL,
    InventoryID         VARCHAR(30)          NOT NULL,
    DateKey             INT                  NOT NULL,
    ProductSK           INT                  NOT NULL,
    StoreSK             INT                  NOT NULL,
    OpeningStock        INT                  NOT NULL,
    ReceivedQuantity    INT                  NOT NULL DEFAULT 0,
    SoldQuantity        INT                  NOT NULL DEFAULT 0,
    ReturnQuantity      INT                  NOT NULL DEFAULT 0,
    DamagedQuantity     INT                  NOT NULL DEFAULT 0,
    ClosingStock        INT                  NOT NULL,
    InventoryValue      DECIMAL(18,2)        NOT NULL,
    AverageDailySales   DECIMAL(10,2)        NOT NULL DEFAULT 0.00,
    DaysOfInventory     DECIMAL(10,2)        NOT NULL DEFAULT 0.00,
    StockoutRiskLevel   VARCHAR(15)          NOT NULL DEFAULT 'LOW',
    ReorderRequired     BIT                  NOT NULL DEFAULT 0,
    ETL_LoadTime        DATETIME2            NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_FactInventory PRIMARY KEY CLUSTERED (InventorySK),
    CONSTRAINT FK_FactInventory_DateKey FOREIGN KEY (DateKey) REFERENCES dw.DimDate(DateKey),
    CONSTRAINT FK_FactInventory_ProductSK FOREIGN KEY (ProductSK) REFERENCES dw.DimProduct(ProductSK),
    CONSTRAINT FK_FactInventory_StoreSK FOREIGN KEY (StoreSK) REFERENCES dw.DimStore(StoreSK)
);
GO

-- 3. Fact Purchases Table
CREATE TABLE dw.FactPurchases (
    PurchaseSK              BIGINT IDENTITY(1,1) NOT NULL,
    PurchaseOrderID         VARCHAR(30)          NOT NULL,
    OrderDateKey            INT                  NOT NULL,
    ExpectedDeliveryDateKey INT                  NOT NULL,
    ActualDeliveryDateKey   INT                  NULL,
    SupplierSK              INT                  NOT NULL,
    StoreSK                 INT                  NOT NULL,
    ProductSK               INT                  NOT NULL,
    OrderedQuantity         INT                  NOT NULL,
    ReceivedQuantity        INT                  NOT NULL,
    UnitCost                DECIMAL(18,2)        NOT NULL,
    TotalCost               DECIMAL(18,2)        NOT NULL,
    Status                  VARCHAR(20)          NOT NULL,
    DeliveryVarianceDays    INT                  NULL,
    ETL_LoadTime            DATETIME2            NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_FactPurchases PRIMARY KEY CLUSTERED (PurchaseSK),
    CONSTRAINT FK_FactPurchases_OrderDateKey FOREIGN KEY (OrderDateKey) REFERENCES dw.DimDate(DateKey),
    CONSTRAINT FK_FactPurchases_ExpectedDelivery FOREIGN KEY (ExpectedDeliveryDateKey) REFERENCES dw.DimDate(DateKey),
    CONSTRAINT FK_FactPurchases_SupplierSK FOREIGN KEY (SupplierSK) REFERENCES dw.DimSupplier(SupplierSK),
    CONSTRAINT FK_FactPurchases_StoreSK FOREIGN KEY (StoreSK) REFERENCES dw.DimStore(StoreSK),
    CONSTRAINT FK_FactPurchases_ProductSK FOREIGN KEY (ProductSK) REFERENCES dw.DimProduct(ProductSK)
);
GO

-- 4. Fact Returns Table
CREATE TABLE dw.FactReturns (
    ReturnSK            BIGINT IDENTITY(1,1) NOT NULL,
    ReturnID            VARCHAR(30)          NOT NULL,
    DateKey             INT                  NOT NULL,
    ProductSK           INT                  NOT NULL,
    StoreSK             INT                  NOT NULL,
    SaleID              VARCHAR(30)          NOT NULL,
    Quantity            INT                  NOT NULL,
    RefundAmount        DECIMAL(18,2)        NOT NULL,
    ReturnReason        VARCHAR(50)          NOT NULL,
    ETL_LoadTime        DATETIME2            NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_FactReturns PRIMARY KEY CLUSTERED (ReturnSK),
    CONSTRAINT FK_FactReturns_DateKey FOREIGN KEY (DateKey) REFERENCES dw.DimDate(DateKey),
    CONSTRAINT FK_FactReturns_ProductSK FOREIGN KEY (ProductSK) REFERENCES dw.DimProduct(ProductSK),
    CONSTRAINT FK_FactReturns_StoreSK FOREIGN KEY (StoreSK) REFERENCES dw.DimStore(StoreSK)
);
GO

PRINT 'Fact tables in [dw] schema created successfully with full referential integrity.';
GO
