-- ============================================================================
-- CLARIVENS INVENTORY INTELLIGENCE
-- Procedure: sp_Load_FactSales
-- Description: Incrementally loads clean sales records from stg.Sales into dw.FactSales
-- Author: Himanshu Bagde (Azure Data Engineer & Cloud Analytics Architect)
-- Organization: CLARIVENS RETAIL GROUP
-- ============================================================================

CREATE OR ALTER PROCEDURE dw.sp_Load_FactSales
    @RunID VARCHAR(64) = 'MANUAL_RUN',
    @ForceFullReload BIT = 0
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @StartTime DATETIME2 = SYSUTCDATETIME();
    DECLARE @LastWatermark VARCHAR(100);
    DECLARE @NewWatermark VARCHAR(100);
    DECLARE @RowsInserted INT = 0;
    DECLARE @RowsRejected INT = 0;

    BEGIN TRY
        -- Retrieve high-watermark
        SELECT @LastWatermark = LastWatermarkValue
        FROM audit.ETL_Control
        WHERE PipelineName = 'PL_Load_Sales' AND TableName = 'dw.FactSales';

        IF @LastWatermark IS NULL OR @ForceFullReload = 1
        BEGIN
            SET @LastWatermark = '1900-01-01';
        END

        -- Determine the maximum SaleDate in staging
        SELECT @NewWatermark = MAX(TRY_CAST(SaleDate AS VARCHAR(100)))
        FROM stg.Sales
        WHERE TRY_CAST(SaleDate AS DATE) IS NOT NULL 
          AND TRY_CAST(SaleDate AS DATE) <= '2025-12-31';

        -- CTE for deduplication and dimensional resolution
        ;WITH StagedSales AS (
            SELECT 
                s.SaleID,
                TRY_CAST(s.SaleDate AS DATE) AS ValidSaleDate,
                TRIM(s.StoreID) AS StoreID,
                TRIM(s.ProductID) AS ProductID,
                s.Quantity,
                s.UnitPrice,
                ISNULL(s.Discount, 0.00) AS Discount,
                s.Revenue,
                s.Cost,
                ISNULL(TRIM(s.PaymentMethod), 'Cash') AS PaymentMethod,
                ISNULL(TRIM(s.CustomerSegment), 'Regular') AS CustomerSegment,
                ROW_NUMBER() OVER (
                    PARTITION BY s.SaleID 
                    ORDER BY s._IngestionTimestamp DESC
                ) AS DeduplicationRank
            FROM stg.Sales s
            WHERE s.SaleDate > @LastWatermark
              AND TRY_CAST(s.SaleDate AS DATE) IS NOT NULL
              AND TRY_CAST(s.SaleDate AS DATE) <= '2025-12-31'
              AND s.Quantity > 0
              AND s.ProductID IS NOT NULL AND TRIM(s.ProductID) <> ''
              AND s.StoreID IS NOT NULL AND TRIM(s.StoreID) <> ''
        ),
        ResolvedSales AS (
            SELECT 
                ss.SaleID,
                d.DateKey,
                dp.ProductSK,
                ds.StoreSK,
                ss.Quantity,
                ss.UnitPrice,
                ss.Discount,
                ss.Revenue,
                ss.Cost,
                ROUND(ss.Revenue - ss.Cost, 2) AS GrossProfit,
                ss.PaymentMethod,
                ss.CustomerSegment
            FROM StagedSales ss
            INNER JOIN dw.DimDate d ON ss.ValidSaleDate = d.FullDate
            INNER JOIN dw.DimProduct dp ON ss.ProductID = dp.ProductID AND dp.IsCurrent = 1
            INNER JOIN dw.DimStore ds ON ss.StoreID = ds.StoreID
            WHERE ss.DeduplicationRank = 1
        )
        INSERT INTO dw.FactSales (
            SaleID, DateKey, ProductSK, StoreSK, Quantity, 
            UnitPrice, Discount, Revenue, Cost, GrossProfit, 
            PaymentMethod, CustomerSegment, ETL_LoadTime
        )
        SELECT 
            rs.SaleID,
            rs.DateKey,
            rs.ProductSK,
            rs.StoreSK,
            rs.Quantity,
            rs.UnitPrice,
            rs.Discount,
            rs.Revenue,
            rs.Cost,
            rs.GrossProfit,
            rs.PaymentMethod,
            rs.CustomerSegment,
            SYSUTCDATETIME()
        FROM ResolvedSales rs
        WHERE NOT EXISTS (
            SELECT 1 FROM dw.FactSales fs WHERE fs.SaleID = rs.SaleID
        );

        SET @RowsInserted = @@ROWCOUNT;

        -- Count rejected records for telemetry
        SELECT @RowsRejected = COUNT(*)
        FROM stg.Sales
        WHERE SaleDate > @LastWatermark
          AND (
              TRY_CAST(SaleDate AS DATE) IS NULL 
              OR TRY_CAST(SaleDate AS DATE) > '2025-12-31'
              OR Quantity <= 0
              OR ProductID IS NULL
              OR StoreID IS NULL
          );

        -- Update incremental watermark in audit control
        IF @NewWatermark IS NOT NULL AND @NewWatermark > @LastWatermark
        BEGIN
            UPDATE audit.ETL_Control
            SET LastWatermarkValue = @NewWatermark,
                LastSuccessfulLoad = SYSUTCDATETIME(),
                LastRunID = @RunID,
                LastRunStatus = 'SUCCESS',
                UpdatedAt = SYSUTCDATETIME()
            WHERE PipelineName = 'PL_Load_Sales' AND TableName = 'dw.FactSales';
        END

        -- Log pipeline execution
        EXEC audit.sp_Log_PipelineExecution 
            @RunID = @RunID, 
            @PipelineName = 'PL_Load_Sales', 
            @ActivityName = 'sp_Load_FactSales', 
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
            @PipelineName = 'PL_Load_Sales', 
            @ActivityName = 'sp_Load_FactSales', 
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
