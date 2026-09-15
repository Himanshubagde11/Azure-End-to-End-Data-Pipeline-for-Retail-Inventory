-- ============================================================================
-- CLARIVENS INVENTORY INTELLIGENCE
-- Script: 00_init_database.sql
-- Description: Creates schemas and initializes warehouse environment
-- Author: Senior Data Engineer / Azure Data Architect
-- Organization: CLARIVENS RETAIL GROUP
-- ============================================================================

-- Note: In Azure SQL Database, the database is pre-created via the Azure Portal/CLI.
-- This script configures the required schemas, roles, and session defaults.

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'stg')
BEGIN
    EXEC('CREATE SCHEMA stg AUTHORIZATION dbo;');
    PRINT 'Created schema: stg';
END
GO

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'dw')
BEGIN
    EXEC('CREATE SCHEMA dw AUTHORIZATION dbo;');
    PRINT 'Created schema: dw';
END
GO

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'audit')
BEGIN
    EXEC('CREATE SCHEMA audit AUTHORIZATION dbo;');
    PRINT 'Created schema: audit';
END
GO

PRINT 'Database schemas initialized successfully for Clarivens Inventory Intelligence.';
GO
