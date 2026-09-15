-- ============================================================================
-- CLARIVENS INVENTORY INTELLIGENCE
-- Procedure: sp_Update_InventoryMetrics
-- Description: Computes rolling 30-day Average Daily Sales, Days of Inventory, 
--              Stockout Risk classification (CRITICAL, HIGH, MEDIUM, LOW), and Reorder triggers
-- Author: Himanshu Bagde (Azure Data Engineer & Cloud Analytics Architect)
-- Organization: CLARIVENS RETAIL GROUP
-- ============================================================================

CREATE OR ALTER PROCEDURE dw.sp_Update_InventoryMetrics
    @RunID VARCHAR(64) = 'MANUAL_RUN'
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @StartTime DATETIME2 = SYSUTCDATETIME();
    DECLARE @RowsUpdated INT = 0;

    BEGIN TRY
        -- Compute 30-day average daily sales for each product and store
        ;WITH ProductStoreVelocity AS (
            SELECT 
                fs.ProductSK,
                fs.StoreSK,
                ROUND(CAST(SUM(fs.Quantity) AS DECIMAL(12,4)) / 30.0, 2) AS ADS_30Day
            FROM dw.FactSales fs
            INNER JOIN dw.DimDate d ON fs.DateKey = d.DateKey
            -- Consider sales within the last 30 calendar days of recorded transactions
            WHERE d.FullDate >= (
                SELECT DATEADD(DAY, -30, MAX(FullDate)) FROM dw.DimDate WHERE DateKey IN (SELECT DateKey FROM dw.FactSales)
            )
            GROUP BY fs.ProductSK, fs.StoreSK
        ),
        CalculatedMetrics AS (
            SELECT 
                fi.InventorySK,
                ISNULL(vel.ADS_30Day, 0.50) AS CalcADS,
                -- Days of Inventory = ClosingStock / ADS (capped at 999 days)
                CASE 
                    WHEN fi.ClosingStock <= 0 THEN 0.00
                    WHEN ISNULL(vel.ADS_30Day, 0.00) = 0.00 THEN 90.00 -- Low-velocity safety buffer
                    ELSE ROUND(CAST(fi.ClosingStock AS DECIMAL(12,2)) / vel.ADS_30Day, 2)
                END AS CalcDaysRemaining,
                dp.ReorderLevel
            FROM dw.FactInventory fi
            INNER JOIN dw.DimProduct dp ON fi.ProductSK = dp.ProductSK
            LEFT JOIN ProductStoreVelocity vel ON fi.ProductSK = vel.ProductSK AND fi.StoreSK = vel.StoreSK
        )
        UPDATE fi
        SET 
            fi.AverageDailySales = cm.CalcADS,
            fi.DaysOfInventory = cm.CalcDaysRemaining,
            fi.StockoutRiskLevel = CASE 
                WHEN cm.CalcDaysRemaining <= 3.0 OR fi.ClosingStock = 0 THEN 'CRITICAL'
                WHEN cm.CalcDaysRemaining > 3.0 AND cm.CalcDaysRemaining <= 7.0 THEN 'HIGH'
                WHEN cm.CalcDaysRemaining > 7.0 AND cm.CalcDaysRemaining <= 14.0 THEN 'MEDIUM'
                ELSE 'LOW'
            END,
            fi.ReorderRequired = CASE 
                WHEN fi.ClosingStock <= cm.ReorderLevel THEN 1 
                ELSE 0 
            END
        FROM dw.FactInventory fi
        INNER JOIN CalculatedMetrics cm ON fi.InventorySK = cm.InventorySK;

        SET @RowsUpdated = @@ROWCOUNT;

        EXEC audit.sp_Log_PipelineExecution 
            @RunID = @RunID, 
            @PipelineName = 'PL_Transform_Warehouse', 
            @ActivityName = 'sp_Update_InventoryMetrics', 
            @StartTime = @StartTime, 
            @EndTime = SYSUTCDATETIME(), 
            @Status = 'SUCCESS', 
            @RowsProcessed = @RowsUpdated, 
            @RowsFailed = 0, 
            @ErrorMessage = NULL;

    END TRY
    BEGIN CATCH
        DECLARE @ErrMsg NVARCHAR(MAX) = ERROR_MESSAGE();
        EXEC audit.sp_Log_PipelineExecution 
            @RunID = @RunID, 
            @PipelineName = 'PL_Transform_Warehouse', 
            @ActivityName = 'sp_Update_InventoryMetrics', 
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
