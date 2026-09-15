-- ============================================================================
-- CLARIVENS INVENTORY INTELLIGENCE
-- Script: 04_audit_tables.sql
-- Description: Creates centralized observability and ETL watermark control tables
-- Author: Himanshu Bagde (Azure Data Engineer & Cloud Analytics Architect)
-- Organization: CLARIVENS RETAIL GROUP
-- ============================================================================

DROP TABLE IF EXISTS audit.DataQualityLog;
DROP TABLE IF EXISTS audit.PipelineExecutionLog;
DROP TABLE IF EXISTS audit.ETL_Control;
GO

-- 1. Centralized Pipeline Execution Log
CREATE TABLE audit.PipelineExecutionLog (
    LogID           BIGINT IDENTITY(1,1) NOT NULL,
    RunID           VARCHAR(64)          NOT NULL,
    PipelineName    VARCHAR(100)         NOT NULL,
    ActivityName    VARCHAR(100)         NOT NULL,
    StartTime       DATETIME2            NOT NULL,
    EndTime         DATETIME2            NULL,
    Status          VARCHAR(20)          NOT NULL, -- 'SUCCESS', 'FAILED', 'WARNING', 'RUNNING'
    RowsProcessed   BIGINT               NULL,
    RowsFailed      BIGINT               NULL,
    ErrorMessage    NVARCHAR(MAX)        NULL,
    CreatedDate     DATETIME2            DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_PipelineExecutionLog PRIMARY KEY CLUSTERED (LogID)
);
GO

-- 2. Data Quality Log
CREATE TABLE audit.DataQualityLog (
    QualityCheckID  BIGINT IDENTITY(1,1) NOT NULL,
    RunID           VARCHAR(64)          NOT NULL,
    TableName       VARCHAR(50)          NOT NULL,
    CheckType       VARCHAR(50)          NOT NULL, -- 'SCHEMA', 'NULL', 'DUPLICATE', 'BUSINESS_RULE'
    RuleName        VARCHAR(100)         NOT NULL,
    TotalRecords    BIGINT               NOT NULL,
    FailedRecords   BIGINT               NOT NULL,
    PassPercentage  DECIMAL(5,2)         NOT NULL,
    Status          VARCHAR(20)          NOT NULL, -- 'PASS', 'WARNING', 'FAIL'
    ExecutionTime   DATETIME2            NOT NULL DEFAULT SYSUTCDATETIME(),
    ErrorMessage    NVARCHAR(MAX)        NULL,
    CONSTRAINT PK_DataQualityLog PRIMARY KEY CLUSTERED (QualityCheckID)
);
GO

-- 3. ETL Watermark / Incremental Loading Control Table
CREATE TABLE audit.ETL_Control (
    ControlID           INT IDENTITY(1,1) NOT NULL,
    PipelineName        VARCHAR(100)      NOT NULL,
    TableName           VARCHAR(100)      NOT NULL,
    WatermarkColumn     VARCHAR(50)       NOT NULL,
    LastWatermarkValue  VARCHAR(100)      NOT NULL,
    LastSuccessfulLoad  DATETIME2         NOT NULL,
    LastRunID           VARCHAR(64)       NOT NULL,
    LastRunStatus       VARCHAR(20)       NOT NULL,
    UpdatedAt           DATETIME2         NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_ETL_Control PRIMARY KEY CLUSTERED (ControlID),
    CONSTRAINT UQ_ETL_Control_Pipeline_Table UNIQUE (PipelineName, TableName)
);
GO

-- Seed default watermark baseline values
INSERT INTO audit.ETL_Control (PipelineName, TableName, WatermarkColumn, LastWatermarkValue, LastSuccessfulLoad, LastRunID, LastRunStatus)
VALUES 
('PL_Load_Sales', 'dw.FactSales', 'SaleDate', '1900-01-01', '1900-01-01 00:00:00', 'INIT_SEED', 'SUCCESS'),
('PL_Load_Inventory', 'dw.FactInventory', 'SnapshotDate', '1900-01-01', '1900-01-01 00:00:00', 'INIT_SEED', 'SUCCESS'),
('PL_Load_Purchases', 'dw.FactPurchases', 'OrderDate', '1900-01-01', '1900-01-01 00:00:00', 'INIT_SEED', 'SUCCESS'),
('PL_Load_Returns', 'dw.FactReturns', 'ReturnDate', '1900-01-01', '1900-01-01 00:00:00', 'INIT_SEED', 'SUCCESS');
GO

PRINT 'Audit and ETL Control tables in [audit] schema created and initialized successfully.';
GO
