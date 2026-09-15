-- ============================================================================
-- CLARIVENS INVENTORY INTELLIGENCE
-- Test Suite: test_warehouse_integrity.sql
-- Description: Automated SQL test suite validating dimensional integrity,
--              surrogate key uniqueness, zero orphan foreign keys, and business bounds
-- Author: Senior Data Engineer / Azure Data Architect
-- Organization: CLARIVENS RETAIL GROUP
-- ============================================================================

SET NOCOUNT ON;
PRINT '==========================================================================';
PRINT ' CLARIVENS INVENTORY INTELLIGENCE — WAREHOUSE INTEGRITY TEST SUITE';
PRINT '==========================================================================';

-- Test 1: Dimension Table Row Counts (Must not be empty)
SELECT 'TEST 1: DimDate Row Count' AS TestName, COUNT(*) AS ActualRows, CASE WHEN COUNT(*) >= 1000 THEN 'PASS' ELSE 'FAIL' END AS Status FROM dw.DimDate;
SELECT 'TEST 1: DimCategory Row Count' AS TestName, COUNT(*) AS ActualRows, CASE WHEN COUNT(*) >= 9 THEN 'PASS' ELSE 'FAIL' END AS Status FROM dw.DimCategory;
SELECT 'TEST 1: DimStore Row Count' AS TestName, COUNT(*) AS ActualRows, CASE WHEN COUNT(*) >= 30 THEN 'PASS' ELSE 'FAIL' END AS Status FROM dw.DimStore;
SELECT 'TEST 1: DimSupplier Row Count' AS TestName, COUNT(*) AS ActualRows, CASE WHEN COUNT(*) >= 50 THEN 'PASS' ELSE 'FAIL' END AS Status FROM dw.DimSupplier;
SELECT 'TEST 1: DimProduct Row Count' AS TestName, COUNT(*) AS ActualRows, CASE WHEN COUNT(*) >= 1000 THEN 'PASS' ELSE 'FAIL' END AS Status FROM dw.DimProduct WHERE IsCurrent = 1;

-- Test 2: Surrogate Key Uniqueness (Must be 0 duplicates)
SELECT 'TEST 2: DimProduct SK Uniqueness' AS TestName, COUNT(*) - COUNT(DISTINCT ProductSK) AS DuplicateSKs, CASE WHEN COUNT(*) = COUNT(DISTINCT ProductSK) THEN 'PASS' ELSE 'FAIL' END AS Status FROM dw.DimProduct;
SELECT 'TEST 2: DimStore SK Uniqueness' AS TestName, COUNT(*) - COUNT(DISTINCT StoreSK) AS DuplicateSKs, CASE WHEN COUNT(*) = COUNT(DISTINCT StoreSK) THEN 'PASS' ELSE 'FAIL' END AS Status FROM dw.DimStore;
SELECT 'TEST 2: FactSales SK Uniqueness' AS TestName, COUNT(*) - COUNT(DISTINCT SalesSK) AS DuplicateSKs, CASE WHEN COUNT(*) = COUNT(DISTINCT SalesSK) THEN 'PASS' ELSE 'FAIL' END AS Status FROM dw.FactSales;
SELECT 'TEST 2: FactInventory SK Uniqueness' AS TestName, COUNT(*) - COUNT(DISTINCT InventorySK) AS DuplicateSKs, CASE WHEN COUNT(*) = COUNT(DISTINCT InventorySK) THEN 'PASS' ELSE 'FAIL' END AS Status FROM dw.FactInventory;

-- Test 3: Referential Integrity - Zero Orphan Foreign Keys in FactSales
SELECT 'TEST 3: FactSales Orphan DateKeys' AS TestName, COUNT(*) AS OrphanRows, CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS Status
FROM dw.FactSales fs LEFT JOIN dw.DimDate d ON fs.DateKey = d.DateKey WHERE d.DateKey IS NULL;

SELECT 'TEST 3: FactSales Orphan ProductSKs' AS TestName, COUNT(*) AS OrphanRows, CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS Status
FROM dw.FactSales fs LEFT JOIN dw.DimProduct p ON fs.ProductSK = p.ProductSK WHERE p.ProductSK IS NULL;

SELECT 'TEST 3: FactSales Orphan StoreSKs' AS TestName, COUNT(*) AS OrphanRows, CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS Status
FROM dw.FactSales fs LEFT JOIN dw.DimStore s ON fs.StoreSK = s.StoreSK WHERE s.StoreSK IS NULL;

-- Test 4: Referential Integrity - Zero Orphan Foreign Keys in FactInventory
SELECT 'TEST 4: FactInventory Orphan DateKeys' AS TestName, COUNT(*) AS OrphanRows, CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS Status
FROM dw.FactInventory fi LEFT JOIN dw.DimDate d ON fi.DateKey = d.DateKey WHERE d.DateKey IS NULL;

SELECT 'TEST 4: FactInventory Orphan ProductSKs' AS TestName, COUNT(*) AS OrphanRows, CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS Status
FROM dw.FactInventory fi LEFT JOIN dw.DimProduct p ON fi.ProductSK = p.ProductSK WHERE p.ProductSK IS NULL;

SELECT 'TEST 4: FactInventory Orphan StoreSKs' AS TestName, COUNT(*) AS OrphanRows, CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS Status
FROM dw.FactInventory fi LEFT JOIN dw.DimStore s ON fi.StoreSK = s.StoreSK WHERE s.StoreSK IS NULL;

-- Test 5: Domain Consistency - Non-Negative Quantities & Stock
SELECT 'TEST 5: FactSales Negative Quantities' AS TestName, COUNT(*) AS Violations, CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS Status
FROM dw.FactSales WHERE Quantity <= 0;

SELECT 'TEST 5: FactInventory Negative Closing Stock' AS TestName, COUNT(*) AS Violations, CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS Status
FROM dw.FactInventory WHERE ClosingStock < 0;

SELECT 'TEST 5: FactInventory Negative Valuation' AS TestName, COUNT(*) AS Violations, CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS Status
FROM dw.FactInventory WHERE InventoryValue < 0.00;

-- Test 6: Mathematical Inventory Balance Reconciliation
SELECT 'TEST 6: FactInventory Balance Equation' AS TestName, COUNT(*) AS Violations, CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS Status
FROM dw.FactInventory
WHERE ClosingStock <> (OpeningStock + ReceivedQuantity - SoldQuantity + ReturnQuantity - DamagedQuantity)
  AND (OpeningStock + ReceivedQuantity - SoldQuantity + ReturnQuantity - DamagedQuantity) >= 0;

-- Test 7: Incremental Watermark State in audit.ETL_Control
SELECT 'TEST 7: ETL_Control Watermarks' AS TestName, COUNT(*) AS PopulatedPipelines, CASE WHEN COUNT(*) >= 4 THEN 'PASS' ELSE 'FAIL' END AS Status
FROM audit.ETL_Control WHERE LastWatermarkValue <> '1900-01-01';

PRINT '==========================================================================';
PRINT ' Automated SQL Warehouse Integrity Tests Complete.';
PRINT '==========================================================================';
