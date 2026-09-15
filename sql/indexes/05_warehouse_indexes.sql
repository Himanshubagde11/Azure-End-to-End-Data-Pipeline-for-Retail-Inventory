-- ============================================================================
-- CLARIVENS INVENTORY INTELLIGENCE
-- Script: 05_warehouse_indexes.sql
-- Description: Creates performance indexes on Star Schema facts and dimensions
-- Author: Himanshu Bagde (Azure Data Engineer & Cloud Analytics Architect)
-- Organization: CLARIVENS RETAIL GROUP
-- ============================================================================

-- FactSales Indexes
CREATE NONCLUSTERED INDEX IX_FactSales_DateKey 
    ON dw.FactSales (DateKey) 
    INCLUDE (ProductSK, StoreSK, Quantity, Revenue, Cost, GrossProfit);

CREATE NONCLUSTERED INDEX IX_FactSales_ProductSK 
    ON dw.FactSales (ProductSK) 
    INCLUDE (DateKey, StoreSK, Quantity, Revenue);

CREATE NONCLUSTERED INDEX IX_FactSales_StoreSK 
    ON dw.FactSales (StoreSK) 
    INCLUDE (DateKey, ProductSK, Quantity, Revenue);

-- FactInventory Indexes
CREATE NONCLUSTERED INDEX IX_FactInventory_DateKey_StoreSK 
    ON dw.FactInventory (DateKey, StoreSK) 
    INCLUDE (ProductSK, ClosingStock, InventoryValue, DaysOfInventory, StockoutRiskLevel);

CREATE NONCLUSTERED INDEX IX_FactInventory_ProductSK_Risk 
    ON dw.FactInventory (ProductSK, StockoutRiskLevel) 
    INCLUDE (StoreSK, ClosingStock, DaysOfInventory, ReorderRequired);

CREATE NONCLUSTERED INDEX IX_FactInventory_ReorderRequired 
    ON dw.FactInventory (ReorderRequired) 
    WHERE ReorderRequired = 1;

-- FactPurchases Indexes
CREATE NONCLUSTERED INDEX IX_FactPurchases_OrderDateKey 
    ON dw.FactPurchases (OrderDateKey) 
    INCLUDE (SupplierSK, StoreSK, ProductSK, OrderedQuantity, ReceivedQuantity, Status);

CREATE NONCLUSTERED INDEX IX_FactPurchases_SupplierSK_Status 
    ON dw.FactPurchases (SupplierSK, Status) 
    INCLUDE (OrderDateKey, OrderedQuantity, ReceivedQuantity, DeliveryVarianceDays);

-- FactReturns Indexes
CREATE NONCLUSTERED INDEX IX_FactReturns_DateKey_ProductSK 
    ON dw.FactReturns (DateKey, ProductSK) 
    INCLUDE (StoreSK, Quantity, RefundAmount, ReturnReason);

-- Audit Table Indexes
CREATE NONCLUSTERED INDEX IX_PipelineExecutionLog_RunID_Status 
    ON audit.PipelineExecutionLog (RunID, Status) 
    INCLUDE (PipelineName, ActivityName, StartTime, EndTime);

CREATE NONCLUSTERED INDEX IX_DataQualityLog_RunID_Table 
    ON audit.DataQualityLog (RunID, TableName) 
    INCLUDE (CheckType, RuleName, PassPercentage, Status);

PRINT 'Performance non-clustered indexes created successfully across all Star Schema tables.';
GO
