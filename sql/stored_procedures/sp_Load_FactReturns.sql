-- ============================================================================
-- CLARIVENS INVENTORY INTELLIGENCE
-- Procedure: sp_Load_FactReturns
-- Description: Transforms and loads customer returns from stg.Returns into dw.FactReturns
-- Author: Himanshu Bagde (Azure Data Engineer & Cloud Analytics Architect)
-- Organization: CLARIVENS RETAIL GROUP
-- ============================================================================

CREATE OR ALTER PROCEDURE dw.sp_Load_FactReturns
    @RunID VARCHAR(64) = 'MANUAL_RUN'
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @StartTime DATETIME2 = SYSUTCDATETIME();
    DECLARE @RowsInserted INT = 0;
    DECLARE @RowsRejected INT = 0;

    BEGIN TRY
        ;WITH CleanReturns AS (
            SELECT 
                r.ReturnID,
                d.DateKey,
                dp.ProductSK,
                dst.StoreSK,
                TRIM(r.SaleID) AS SaleID,
                ISNULL(r.Quantity, 1) AS Quantity,
                -- Cleanse negative refund amounts
                ABS(ISNULL(r.RefundAmount, dp.UnitPrice)) AS RefundAmount,
                ISNULL(TRIM(r.ReturnReason), 'Defective Item') AS ReturnReason
            FROM stg.Returns r
            INNER JOIN dw.DimDate d ON TRY_CAST(r.ReturnDate AS DATE) = d.FullDate
            INNER JOIN dw.DimProduct dp ON TRIM(r.ProductID) = dp.ProductID AND dp.IsCurrent = 1
            INNER JOIN dw.DimStore dst ON TRIM(r.StoreID) = dst.StoreID
            WHERE r.ReturnID IS NOT NULL AND TRIM(r.ReturnID) <> ''
        )
        INSERT INTO dw.FactReturns (
            ReturnID, DateKey, ProductSK, StoreSK, 
            SaleID, Quantity, RefundAmount, ReturnReason, ETL_LoadTime
        )
        SELECT 
            cr.ReturnID,
            cr.DateKey,
            cr.ProductSK,
            cr.StoreSK,
            cr.SaleID,
            cr.Quantity,
            cr.RefundAmount,
            cr.ReturnReason,
            SYSUTCDATETIME()
        FROM CleanReturns cr
        WHERE NOT EXISTS (
            SELECT 1 FROM dw.FactReturns fr WHERE fr.ReturnID = cr.ReturnID
        );

        SET @RowsInserted = @@ROWCOUNT;

        SELECT @RowsRejected = COUNT(*)
        FROM stg.Returns r
        WHERE r.ProductID IS NULL OR r.StoreID IS NULL OR TRY_CAST(r.ReturnDate AS DATE) IS NULL;

        EXEC audit.sp_Log_PipelineExecution 
            @RunID = @RunID, 
            @PipelineName = 'PL_Load_Returns', 
            @ActivityName = 'sp_Load_FactReturns', 
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
            @PipelineName = 'PL_Load_Returns', 
            @ActivityName = 'sp_Load_FactReturns', 
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
