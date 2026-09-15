-- ============================================================================
-- NEXORA INVENTORY INTELLIGENCE
-- Procedure: sp_Load_DimProduct
-- Description: Transforms and loads products from stg.Products and stg.RestApi_ProductEnrichment into dw.DimProduct
-- Author: Senior Data Engineer / Azure Data Architect
-- Organization: NEXORA RETAIL GROUP
-- ============================================================================

CREATE OR ALTER PROCEDURE dw.sp_Load_DimProduct
    @RunID VARCHAR(64) = 'MANUAL_RUN'
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @StartTime DATETIME2 = SYSUTCDATETIME();
    DECLARE @RowsAffected INT = 0;

    BEGIN TRY
        -- Cleanse and standardize raw products
        ;WITH CleanProducts AS (
            SELECT 
                TRIM(p.ProductID) AS ProductID,
                TRIM(p.ProductName) AS ProductName,
                TRIM(p.CategoryID) AS CategoryID,
                -- Standardize CategoryName from dw.DimCategory to fix intentional data quality flaws
                ISNULL(c.CategoryName, TRIM(p.CategoryName)) AS CategoryName,
                ISNULL(c.Department, 'Retail Merchandise') AS Department,
                -- Fix invalid/corrupted SupplierID by verifying with dw.DimSupplier
                CASE 
                    WHEN s.SupplierID IS NOT NULL THEN TRIM(p.SupplierID)
                    ELSE 'SUP001' -- Fallback to default trusted primary supplier
                END AS SupplierID,
                ISNULL(TRIM(p.Brand), 'Nexora Select') AS Brand,
                ISNULL(p.UnitCost, 150.00) AS UnitCost,
                -- Handle null unit price by applying standard markup on unit cost
                ISNULL(p.UnitPrice, ROUND(ISNULL(p.UnitCost, 150.00) * 1.35, 2)) AS UnitPrice,
                -- Overlay live replenishment recommendations from REST API if available
                ISNULL(api.RecommendedSafetyStock, ISNULL(p.ReorderLevel, 50)) AS ReorderLevel,
                ISNULL(p.ReorderQuantity, 100) AS ReorderQuantity,
                TRY_CAST(p.LaunchDate AS DATE) AS LaunchDate,
                ISNULL(p.IsActive, 1) AS IsActive
            FROM stg.Products p
            LEFT JOIN dw.DimCategory c ON TRIM(p.CategoryID) = c.CategoryID
            LEFT JOIN dw.DimSupplier s ON TRIM(p.SupplierID) = s.SupplierID
            LEFT JOIN stg.RestApi_ProductEnrichment api ON TRIM(p.ProductID) = TRIM(api.ProductID)
            WHERE p.ProductID IS NOT NULL AND TRIM(p.ProductID) <> ''
        )
        MERGE dw.DimProduct AS Target
        USING CleanProducts AS Source
        ON Target.ProductID = Source.ProductID AND Target.IsCurrent = 1
        WHEN MATCHED AND (
            Target.ProductName <> Source.ProductName OR
            Target.UnitCost <> Source.UnitCost OR
            Target.UnitPrice <> Source.UnitPrice OR
            Target.ReorderLevel <> Source.ReorderLevel OR
            Target.ReorderQuantity <> Source.ReorderQuantity OR
            Target.IsActive <> Source.IsActive
        ) THEN
            UPDATE SET 
                Target.ProductName = Source.ProductName,
                Target.CategoryID = Source.CategoryID,
                Target.CategoryName = Source.CategoryName,
                Target.Department = Source.Department,
                Target.SupplierID = Source.SupplierID,
                Target.Brand = Source.Brand,
                Target.UnitCost = Source.UnitCost,
                Target.UnitPrice = Source.UnitPrice,
                Target.ReorderLevel = Source.ReorderLevel,
                Target.ReorderQuantity = Source.ReorderQuantity,
                Target.IsActive = Source.IsActive,
                Target.ModifiedDate = SYSUTCDATETIME()
        WHEN NOT MATCHED THEN
            INSERT (
                ProductID, ProductName, CategoryID, CategoryName, Department, 
                SupplierID, Brand, UnitCost, UnitPrice, ReorderLevel, 
                ReorderQuantity, LaunchDate, IsActive, EffectiveDate, ExpiryDate, 
                IsCurrent, CreatedDate, ModifiedDate
            )
            VALUES (
                Source.ProductID, Source.ProductName, Source.CategoryID, Source.CategoryName, Source.Department,
                Source.SupplierID, Source.Brand, Source.UnitCost, Source.UnitPrice, Source.ReorderLevel,
                Source.ReorderQuantity, Source.LaunchDate, Source.IsActive, '2025-01-01 00:00:00', '9999-12-31 23:59:59',
                1, SYSUTCDATETIME(), SYSUTCDATETIME()
            );

        SET @RowsAffected = @@ROWCOUNT;

        EXEC audit.sp_Log_PipelineExecution 
            @RunID = @RunID, 
            @PipelineName = 'PL_Transform_Warehouse', 
            @ActivityName = 'sp_Load_DimProduct', 
            @StartTime = @StartTime, 
            @EndTime = SYSUTCDATETIME(), 
            @Status = 'SUCCESS', 
            @RowsProcessed = @RowsAffected, 
            @RowsFailed = 0, 
            @ErrorMessage = NULL;

    END TRY
    BEGIN CATCH
        DECLARE @ErrMsg NVARCHAR(MAX) = ERROR_MESSAGE();
        EXEC audit.sp_Log_PipelineExecution 
            @RunID = @RunID, 
            @PipelineName = 'PL_Transform_Warehouse', 
            @ActivityName = 'sp_Load_DimProduct', 
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
