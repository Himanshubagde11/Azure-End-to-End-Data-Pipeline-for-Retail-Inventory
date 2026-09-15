-- ============================================================================
-- CLARIVENS INVENTORY INTELLIGENCE
-- Procedure: sp_Load_DimStore
-- Description: Merges raw store records from stg.Stores into dw.DimStore
-- Author: Himanshu Bagde (Azure Data Engineer & Cloud Analytics Architect)
-- Organization: CLARIVENS RETAIL GROUP
-- ============================================================================

CREATE OR ALTER PROCEDURE dw.sp_Load_DimStore
    @RunID VARCHAR(64) = 'MANUAL_RUN'
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @StartTime DATETIME2 = SYSUTCDATETIME();
    DECLARE @RowsAffected INT = 0;

    BEGIN TRY
        MERGE dw.DimStore AS Target
        USING (
            SELECT 
                TRIM(StoreID) AS StoreID,
                TRIM(StoreName) AS StoreName,
                TRIM(City) AS City,
                TRIM(State) AS State,
                TRIM(Region) AS Region,
                TRIM(StoreType) AS StoreType,
                ISNULL(SquareFeet, 10000) AS SquareFeet,
                TRIM(Manager) AS Manager,
                CAST(OpeningDate AS DATE) AS OpeningDate,
                ISNULL(IsActive, 1) AS IsActive
            FROM stg.Stores
            WHERE StoreID IS NOT NULL AND TRIM(StoreID) <> ''
        ) AS Source
        ON Target.StoreID = Source.StoreID
        WHEN MATCHED AND (
            Target.StoreName <> Source.StoreName OR
            Target.StoreType <> Source.StoreType OR
            Target.Manager <> Source.Manager OR
            Target.SquareFeet <> Source.SquareFeet OR
            Target.IsActive <> Source.IsActive
        ) THEN
            UPDATE SET 
                Target.StoreName = Source.StoreName,
                Target.City = Source.City,
                Target.State = Source.State,
                Target.Region = Source.Region,
                Target.StoreType = Source.StoreType,
                Target.SquareFeet = Source.SquareFeet,
                Target.Manager = Source.Manager,
                Target.OpeningDate = Source.OpeningDate,
                Target.IsActive = Source.IsActive,
                Target.ModifiedDate = SYSUTCDATETIME()
        WHEN NOT MATCHED THEN
            INSERT (
                StoreID, StoreName, City, State, Region, StoreType, 
                SquareFeet, Manager, OpeningDate, IsActive, 
                CreatedDate, ModifiedDate
            )
            VALUES (
                Source.StoreID, Source.StoreName, Source.City, Source.State, Source.Region, Source.StoreType,
                Source.SquareFeet, Source.Manager, Source.OpeningDate, Source.IsActive,
                SYSUTCDATETIME(), SYSUTCDATETIME()
            );

        SET @RowsAffected = @@ROWCOUNT;

        EXEC audit.sp_Log_PipelineExecution 
            @RunID = @RunID, 
            @PipelineName = 'PL_Transform_Warehouse', 
            @ActivityName = 'sp_Load_DimStore', 
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
            @ActivityName = 'sp_Load_DimStore', 
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
