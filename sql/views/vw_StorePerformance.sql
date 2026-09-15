-- ============================================================================
-- CLARIVENS INVENTORY INTELLIGENCE
-- View: vw_StorePerformance
-- Description: Aggregates revenue, margin, sales velocity, and inventory metrics by store and geography
-- Author: Himanshu Bagde (Azure Data Engineer & Cloud Analytics Architect)
-- Organization: CLARIVENS RETAIL GROUP
-- ============================================================================

CREATE OR ALTER VIEW dw.vw_StorePerformance
AS
WITH StoreSalesSummary AS (
    SELECT 
        fs.StoreSK,
        COUNT(DISTINCT fs.SaleID) AS TotalTransactions,
        SUM(fs.Quantity) AS TotalUnitsSold,
        SUM(fs.Revenue) AS TotalRevenue,
        SUM(fs.Cost) AS TotalCost,
        SUM(fs.GrossProfit) AS TotalGrossProfit,
        ROUND(CASE WHEN SUM(fs.Revenue) > 0 THEN (SUM(fs.GrossProfit) / SUM(fs.Revenue)) * 100.0 ELSE 0.0 END, 2) AS GrossMarginPct
    FROM dw.FactSales fs
    GROUP BY fs.StoreSK
),
StoreInventorySummary AS (
    SELECT 
        fi.StoreSK,
        SUM(fi.InventoryValue) AS CurrentInventoryValue,
        SUM(fi.ClosingStock) AS CurrentStockUnits,
        SUM(CASE WHEN fi.StockoutRiskLevel = 'CRITICAL' THEN 1 ELSE 0 END) AS CriticalStockoutAlerts,
        SUM(CASE WHEN fi.ReorderRequired = 1 THEN 1 ELSE 0 END) AS ReorderAlertCount
    FROM dw.FactInventory fi
    WHERE fi.DateKey = (SELECT MAX(DateKey) FROM dw.FactInventory)
    GROUP BY fi.StoreSK
),
StoreReturnsSummary AS (
    SELECT 
        fr.StoreSK,
        COUNT(DISTINCT fr.ReturnID) AS TotalReturns,
        SUM(fr.RefundAmount) AS TotalRefundAmount
    FROM dw.FactReturns fr
    GROUP BY fr.StoreSK
)
SELECT 
    ds.StoreSK,
    ds.StoreID,
    ds.StoreName,
    ds.City,
    ds.State,
    ds.Region,
    ds.StoreType,
    ds.SquareFeet,
    ds.Manager,
    ds.OpeningDate,
    -- Sales Performance
    ISNULL(ss.TotalTransactions, 0) AS TotalTransactions,
    ISNULL(ss.TotalUnitsSold, 0) AS TotalUnitsSold,
    ISNULL(ss.TotalRevenue, 0.00) AS TotalRevenue,
    ISNULL(ss.TotalCost, 0.00) AS TotalCost,
    ISNULL(ss.TotalGrossProfit, 0.00) AS TotalGrossProfit,
    ISNULL(ss.GrossMarginPct, 0.00) AS GrossMarginPct,
    -- Revenue per square foot efficiency
    ROUND(ISNULL(ss.TotalRevenue, 0.00) / NULLIF(ds.SquareFeet, 0), 2) AS RevenuePerSqFt,
    -- Inventory Health
    ISNULL(inv.CurrentInventoryValue, 0.00) AS CurrentInventoryValue,
    ISNULL(inv.CurrentStockUnits, 0) AS CurrentStockUnits,
    ISNULL(inv.CriticalStockoutAlerts, 0) AS CriticalStockoutAlerts,
    ISNULL(inv.ReorderAlertCount, 0) AS ReorderAlertCount,
    -- Returns & Service Quality
    ISNULL(ret.TotalReturns, 0) AS TotalReturns,
    ISNULL(ret.TotalRefundAmount, 0.00) AS TotalRefundAmount,
    ROUND(CASE WHEN ISNULL(ss.TotalUnitsSold, 0) > 0 THEN (CAST(ISNULL(ret.TotalReturns, 0) AS DECIMAL(10,2)) / ss.TotalUnitsSold) * 100.0 ELSE 0.0 END, 2) AS ReturnRatePct
FROM dw.DimStore ds
LEFT JOIN StoreSalesSummary ss ON ds.StoreSK = ss.StoreSK
LEFT JOIN StoreInventorySummary inv ON ds.StoreSK = inv.StoreSK
LEFT JOIN StoreReturnsSummary ret ON ds.StoreSK = ret.StoreSK;
GO
