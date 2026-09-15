-- ============================================================================
-- CLARIVENS INVENTORY INTELLIGENCE
-- Procedure: sp_Load_FactInventory
-- Description: Loads and reconciles inventory snapshots from stg.Inventory into dw.FactInventory
-- Author: Himanshu Bagde (Azure Data Engineer & Cloud Analytics Architect)
-- Organization: CLARIVENS RETAIL GROUP
-- ============================================================================

CREATE OR ALTER PROCEDURE dw.sp_Load_FactInventory
    @RunID VARCHAR(64) = 'MANUAL_RUN'
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @StartTime DATETIME2 = SYSUTCDATETIME();
    DECLARE @RowsInserted INT = 0;
    DECLARE @RowsRejected INT = 0;

    BEGIN TRY
        ;WITH CleanInventory AS (
            SELECT 
                inv.InventoryID,
                d.DateKey,
                dp.ProductSK,
                ds.StoreSK,
                ISNULL(inv.OpeningStock, 0) AS OpeningStock,
                ISNULL(inv.ReceivedQuantity, 0) AS ReceivedQuantity,
                ISNULL(inv.SoldQuantity, 0) AS SoldQuantity,
                ISNULL(inv.ReturnQuantity, 0) AS ReturnQuantity,
                ISNULL(inv.DamagedQuantity, 0) AS DamagedQuantity,
                -- Reconcile mathematically verified closing stock
                CASE 
                    WHEN (ISNULL(inv.OpeningStock, 0) + ISNULL(inv.ReceivedQuantity, 0) - ISNULL(inv.SoldQuantity, 0) + ISNULL(inv.ReturnQuantity, 0) - ISNULL(inv.DamagedQuantity, 0)) >= 0
                    THEN (ISNULL(inv.OpeningStock, 0) + ISNULL(inv.ReceivedQuantity, 0) - ISNULL(inv.SoldQuantity, 0) + ISNULL(inv.ReturnQuantity, 0) - ISNULL(inv.DamagedQuantity, 0))
                    ELSE 0
                END AS ReconciledClosingStock,
                dp.UnitCost,
                dp.ReorderLevel
            FROM stg.Inventory inv
            INNER JOIN dw.DimDate d ON TRY_CAST(inv.SnapshotDate AS DATE) = d.FullDate
            INNER JOIN dw.DimProduct dp ON TRIM(inv.ProductID) = dp.ProductID AND dp.IsCurrent = 1
            INNER JOIN dw.DimStore ds ON TRIM(inv.StoreID) = ds.StoreID
            WHERE inv.InventoryID IS NOT NULL AND TRIM(inv.InventoryID) <> ''
        )
        INSERT INTO dw.FactInventory (
            InventoryID, DateKey, ProductSK, StoreSK, 
            OpeningStock, ReceivedQuantity, SoldQuantity, ReturnQuantity, DamagedQuantity, 
            ClosingStock, InventoryValue, ReorderRequired, ETL_LoadTime
        )
        SELECT 
            ci.InventoryID,
            ci.DateKey,
            ci.ProductSK,
            ci.StoreSK,
            ci.OpeningStock,
            ci.ReceivedQuantity,
            ci.SoldQuantity,
            ci.ReturnQuantity,
            ci.DamagedQuantity,
            ci.ReconciledClosingStock,
            ROUND(ci.ReconciledClosingStock * ci.UnitCost, 2) AS InventoryValue,
            CASE WHEN ci.ReconciledClosingStock <= ci.ReorderLevel THEN 1 ELSE 0 END AS ReorderRequired,
            SYSUTCDATETIME()
        FROM CleanInventory ci
        WHERE NOT EXISTS (
            SELECT 1 FROM dw.FactInventory fi WHERE fi.InventoryID = ci.InventoryID
        );

        SET @RowsInserted = @@ROWCOUNT;

        -- Count rejected records (unmatched dimensions or null keys)
        SELECT @RowsRejected = COUNT(*)
        FROM stg.Inventory inv
        WHERE inv.ProductID IS NULL 
           OR inv.StoreID IS NULL 
           OR TRY_CAST(inv.SnapshotDate AS DATE) IS NULL;

        -- Trigger metric update for stockout risk classification
        EXEC dw.sp_Update_InventoryMetrics @RunID = @RunID;

        -- Log pipeline execution
        EXEC audit.sp_Log_PipelineExecution 
            @RunID = @RunID, 
            @PipelineName = 'PL_Load_Inventory', 
            @ActivityName = 'sp_Load_FactInventory', 
            @StartTime = @StartTime, 
            @EndTime = SYSUTCDATETIME(), 
            @Status = 'SUCCESS', 
            @RowsProcessed = @RowsInserted, 
            @RowsFailed = @RowsRejected, 
            @ErrorMessage = NULL;

    END TRY
    BEGIN CATCH
        DECLARE @ErrMsg NVARCHAR(MAX) = ERROR_MESSAGE();
        EXEC audit.sp_Log_PipelineExecution 
            @RunID = @RunID, 
            @PipelineName = 'PL_Load_Inventory', 
            @ActivityName = 'sp_Load_FactInventory', 
            @StartTime = @StartTime, 
            @EndTime = SYSUTCDATETIME(), 
            @Status = 'FAILED', 
            @RowsProcessed = 0, 
            @RowsFailed = 0, 
            @ErrorMessage = @ErrMsg;
        THROW;
    END CATCH
END
GO
