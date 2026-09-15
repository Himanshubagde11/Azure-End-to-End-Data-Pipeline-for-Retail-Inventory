-- ============================================================================
-- NEXORA INVENTORY INTELLIGENCE
-- Procedure: sp_Load_DimCategory
-- Description: Merges raw categories from stg.Categories into dw.DimCategory
-- Author: Senior Data Engineer / Azure Data Architect
-- Organization: NEXORA RETAIL GROUP
-- ============================================================================

CREATE OR ALTER PROCEDURE dw.sp_Load_DimCategory
    @RunID VARCHAR(64) = 'MANUAL_RUN'
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @StartTime DATETIME2 = SYSUTCDATETIME();
    DECLARE @RowsAffected INT = 0;

    BEGIN TRY
        MERGE dw.DimCategory AS Target
        USING (
            SELECT DISTINCT
                TRIM(CategoryID) AS CategoryID,
                TRIM(CategoryName) AS CategoryName,
                TRIM(Department) AS Department
            FROM stg.Categories
            WHERE CategoryID IS NOT NULL AND TRIM(CategoryID) <> ''
        ) AS Source
        ON Target.CategoryID = Source.CategoryID
        WHEN MATCHED AND (
            Target.CategoryName <> Source.CategoryName OR
            Target.Department <> Source.Department
        ) THEN
            UPDATE SET 
                Target.CategoryName = Source.CategoryName,
                Target.Department = Source.Department,
                Target.ModifiedDate = SYSUTCDATETIME()
        WHEN NOT MATCHED THEN
            INSERT (CategoryID, CategoryName, Department, CreatedDate, ModifiedDate)
            VALUES (Source.CategoryID, Source.CategoryName, Source.Department, SYSUTCDATETIME(), SYSUTCDATETIME());

        SET @RowsAffected = @@ROWCOUNT;

        EXEC audit.sp_Log_PipelineExecution 
            @RunID = @RunID, 
            @PipelineName = 'PL_Transform_Warehouse', 
            @ActivityName = 'sp_Load_DimCategory', 
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
            @ActivityName = 'sp_Load_DimCategory', 
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
