-- ============================================================================
-- CLARIVENS INVENTORY INTELLIGENCE
-- Procedure: sp_Load_FactPurchases
-- Description: Transforms and loads procurement orders from stg.Purchases into dw.FactPurchases
-- Author: Himanshu Bagde (Azure Data Engineer & Cloud Analytics Architect)
-- Organization: CLARIVENS RETAIL GROUP
-- ============================================================================

CREATE OR ALTER PROCEDURE dw.sp_Load_FactPurchases
    @RunID VARCHAR(64) = 'MANUAL_RUN'
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @StartTime DATETIME2 = SYSUTCDATETIME();
    DECLARE @RowsInserted INT = 0;
    DECLARE @RowsRejected INT = 0;

    BEGIN TRY
        ;WITH CleanPurchases AS (
            SELECT 
                p.PurchaseOrderID,
                d_ord.DateKey AS OrderDateKey,
                d_exp.DateKey AS ExpectedDeliveryDateKey,
                d_act.DateKey AS ActualDeliveryDateKey,
                dsup.SupplierSK,
                dst.StoreSK,
                dp.ProductSK,
                p.OrderedQuantity,
                -- Cap received quantity to ordered quantity if unreasonable defect
                CASE 
                    WHEN p.ReceivedQuantity > (p.OrderedQuantity * 2) THEN p.OrderedQuantity
                    ELSE ISNULL(p.ReceivedQuantity, 0)
                END AS ReceivedQuantity,
                ISNULL(p.UnitCost, dp.UnitCost) AS UnitCost,
                TRIM(p.Status) AS Status,
                CASE 
                    WHEN TRY_CAST(p.ActualDeliveryDate AS DATE) IS NOT NULL AND TRY_CAST(p.ExpectedDeliveryDate AS DATE) IS NOT NULL
                    THEN DATEDIFF(DAY, TRY_CAST(p.ExpectedDeliveryDate AS DATE), TRY_CAST(p.ActualDeliveryDate AS DATE))
                    ELSE NULL
                END AS DeliveryVarianceDays
            FROM stg.Purchases p
            INNER JOIN dw.DimDate d_ord ON TRY_CAST(p.OrderDate AS DATE) = d_ord.FullDate
            INNER JOIN dw.DimDate d_exp ON TRY_CAST(p.ExpectedDeliveryDate AS DATE) = d_exp.FullDate
            LEFT JOIN dw.DimDate d_act ON TRY_CAST(p.ActualDeliveryDate AS DATE) = d_act.FullDate
            INNER JOIN dw.DimSupplier dsup ON TRIM(p.SupplierID) = dsup.SupplierID
            INNER JOIN dw.DimStore dst ON TRIM(p.StoreID) = dst.StoreID
            INNER JOIN dw.DimProduct dp ON TRIM(p.ProductID) = dp.ProductID AND dp.IsCurrent = 1
            WHERE p.PurchaseOrderID IS NOT NULL AND TRIM(p.PurchaseOrderID) <> ''
        )
        INSERT INTO dw.FactPurchases (
            PurchaseOrderID, OrderDateKey, ExpectedDeliveryDateKey, ActualDeliveryDateKey, 
            SupplierSK, StoreSK, ProductSK, OrderedQuantity, ReceivedQuantity, 
            UnitCost, TotalCost, Status, DeliveryVarianceDays, ETL_LoadTime
        )
        SELECT 
            cp.PurchaseOrderID,
            cp.OrderDateKey,
            cp.ExpectedDeliveryDateKey,
            cp.ActualDeliveryDateKey,
            cp.SupplierSK,
            cp.StoreSK,
            cp.ProductSK,
            cp.OrderedQuantity,
            cp.ReceivedQuantity,
            cp.UnitCost,
            ROUND(cp.OrderedQuantity * cp.UnitCost, 2) AS TotalCost,
            cp.Status,
            cp.DeliveryVarianceDays,
            SYSUTCDATETIME()
        FROM CleanPurchases cp
        WHERE NOT EXISTS (
            SELECT 1 FROM dw.FactPurchases fp WHERE fp.PurchaseOrderID = cp.PurchaseOrderID
        );

        SET @RowsInserted = @@ROWCOUNT;

        SELECT @RowsRejected = COUNT(*)
        FROM stg.Purchases p
        WHERE p.SupplierID IS NULL OR p.StoreID IS NULL OR p.ProductID IS NULL;

        EXEC audit.sp_Log_PipelineExecution 
            @RunID = @RunID, 
            @PipelineName = 'PL_Load_Purchases', 
            @ActivityName = 'sp_Load_FactPurchases', 
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
            @PipelineName = 'PL_Load_Purchases', 
            @ActivityName = 'sp_Load_FactPurchases', 
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
