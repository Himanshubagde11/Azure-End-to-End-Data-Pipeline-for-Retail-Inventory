-- ============================================================================
-- CLARIVENS INVENTORY INTELLIGENCE
-- Script: 02_dim_tables.sql
-- Description: Creates Star Schema dimension tables in the 'dw' schema
-- Author: Himanshu Bagde (Azure Data Engineer & Cloud Analytics Architect)
-- Organization: CLARIVENS RETAIL GROUP
-- ============================================================================

DROP TABLE IF EXISTS dw.DimProduct;
DROP TABLE IF EXISTS dw.DimStore;
DROP TABLE IF EXISTS dw.DimSupplier;
DROP TABLE IF EXISTS dw.DimCategory;
DROP TABLE IF EXISTS dw.DimDate;
GO

-- 1. Date Dimension
CREATE TABLE dw.DimDate (
    DateKey             INT          NOT NULL,
    FullDate            DATE         NOT NULL,
    DayNumberOfWeek     TINYINT      NOT NULL,
    DayName             VARCHAR(10)  NOT NULL,
    DayNumberOfMonth    TINYINT      NOT NULL,
    DayNumberOfYear     SMALLINT     NOT NULL,
    WeekNumberOfYear    TINYINT      NOT NULL,
    MonthName           VARCHAR(10)  NOT NULL,
    MonthNumberOfYear   TINYINT      NOT NULL,
    CalendarQuarter     TINYINT      NOT NULL,
    CalendarYear        SMALLINT     NOT NULL,
    FiscalYear          SMALLINT     NOT NULL,
    FiscalQuarter       TINYINT      NOT NULL,
    IsWeekend           BIT          NOT NULL,
    IsFestivalSeason    BIT          NOT NULL,
    CONSTRAINT PK_DimDate PRIMARY KEY CLUSTERED (DateKey)
);
GO

-- 2. Category Dimension
CREATE TABLE dw.DimCategory (
    CategorySK          INT IDENTITY(1,1) NOT NULL,
    CategoryID          VARCHAR(20)       NOT NULL,
    CategoryName        VARCHAR(50)       NOT NULL,
    Department          VARCHAR(50)       NOT NULL,
    CreatedDate         DATETIME2         DEFAULT SYSUTCDATETIME(),
    ModifiedDate        DATETIME2         DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_DimCategory PRIMARY KEY CLUSTERED (CategorySK),
    CONSTRAINT UQ_DimCategory_CategoryID UNIQUE (CategoryID)
);
GO

-- 3. Supplier Dimension
CREATE TABLE dw.DimSupplier (
    SupplierSK          INT IDENTITY(1,1) NOT NULL,
    SupplierID          VARCHAR(20)       NOT NULL,
    SupplierName        VARCHAR(100)      NOT NULL,
    ContactName         VARCHAR(100)      NULL,
    Email               VARCHAR(100)      NULL,
    Phone               VARCHAR(30)       NULL,
    City                VARCHAR(50)       NOT NULL,
    State               VARCHAR(50)       NOT NULL,
    Rating              DECIMAL(3,2)      NOT NULL,
    PaymentTerms        VARCHAR(30)       NOT NULL,
    LeadTimeDays        INT               NOT NULL,
    IsActive            BIT               NOT NULL DEFAULT 1,
    CreatedDate         DATETIME2         DEFAULT SYSUTCDATETIME(),
    ModifiedDate        DATETIME2         DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_DimSupplier PRIMARY KEY CLUSTERED (SupplierSK),
    CONSTRAINT UQ_DimSupplier_SupplierID UNIQUE (SupplierID)
);
GO

-- 4. Store Dimension
CREATE TABLE dw.DimStore (
    StoreSK             INT IDENTITY(1,1) NOT NULL,
    StoreID             VARCHAR(20)       NOT NULL,
    StoreName           VARCHAR(100)      NOT NULL,
    City                VARCHAR(50)       NOT NULL,
    State               VARCHAR(50)       NOT NULL,
    Region              VARCHAR(20)       NOT NULL,
    StoreType           VARCHAR(30)       NOT NULL,
    SquareFeet          INT               NOT NULL,
    Manager             VARCHAR(100)      NULL,
    OpeningDate         DATE              NOT NULL,
    IsActive            BIT               NOT NULL DEFAULT 1,
    CreatedDate         DATETIME2         DEFAULT SYSUTCDATETIME(),
    ModifiedDate        DATETIME2         DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_DimStore PRIMARY KEY CLUSTERED (StoreSK),
    CONSTRAINT UQ_DimStore_StoreID UNIQUE (StoreID)
);
GO

-- 5. Product Dimension (SCD Type 1 & Type 2 Support)
CREATE TABLE dw.DimProduct (
    ProductSK           INT IDENTITY(1,1) NOT NULL,
    ProductID           VARCHAR(20)       NOT NULL,
    ProductName         VARCHAR(150)      NOT NULL,
    CategoryID          VARCHAR(20)       NOT NULL,
    CategoryName        VARCHAR(50)       NOT NULL,
    Department          VARCHAR(50)       NOT NULL,
    SupplierID          VARCHAR(20)       NOT NULL,
    Brand               VARCHAR(50)       NOT NULL,
    UnitCost            DECIMAL(18,2)     NOT NULL,
    UnitPrice           DECIMAL(18,2)     NOT NULL,
    ReorderLevel        INT               NOT NULL,
    ReorderQuantity     INT               NOT NULL,
    LaunchDate          DATE              NULL,
    IsActive            BIT               NOT NULL DEFAULT 1,
    EffectiveDate       DATETIME2         NOT NULL DEFAULT '2025-01-01 00:00:00',
    ExpiryDate          DATETIME2         NULL DEFAULT '9999-12-31 23:59:59',
    IsCurrent           BIT               NOT NULL DEFAULT 1,
    CreatedDate         DATETIME2         DEFAULT SYSUTCDATETIME(),
    ModifiedDate        DATETIME2         DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_DimProduct PRIMARY KEY CLUSTERED (ProductSK),
    CONSTRAINT UQ_DimProduct_ProductID_IsCurrent UNIQUE (ProductID, IsCurrent)
);
GO

PRINT 'Dimension tables in [dw] schema created successfully.';
GO
