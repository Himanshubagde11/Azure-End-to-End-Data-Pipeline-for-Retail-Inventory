-- ============================================================================
-- CLARIVENS INVENTORY INTELLIGENCE
-- Procedure: sp_Load_DimSupplier
-- Description: Merges raw supplier data from stg.Suppliers into dw.DimSupplier
-- Author: Senior Data Engineer / Azure Data Architect
-- Organization: CLARIVENS RETAIL GROUP
-- ============================================================================

CREATE OR ALTER PROCEDURE dw.sp_Load_DimSupplier
    @RunID VARCHAR(64) = 'MANUAL_RUN'
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @StartTime DATETIME2 = SYSUTCDATETIME();
    DECLARE @RowsAffected INT = 0;

    BEGIN TRY
        MERGE dw.DimSupplier AS Target
        USING (
            SELECT 
                TRIM(SupplierID) AS SupplierID,
                TRIM(SupplierName) AS SupplierName,
                TRIM(ContactName) AS ContactName,
                TRIM(Email) AS Email,
                TRIM(Phone) AS Phone,
                TRIM(City) AS City,
                TRIM(State) AS State,
                ISNULL(Rating, 3.50) AS Rating,
                ISNULL(TRIM(PaymentTerms), 'Net 30') AS PaymentTerms,
                ISNULL(LeadTimeDays, 7) AS LeadTimeDays,
                ISNULL(IsActive, 1) AS IsActive
            FROM stg.Suppliers
            WHERE SupplierID IS NOT NULL AND TRIM(SupplierID) <> ''
        ) AS Source
        ON Target.SupplierID = Source.SupplierID
        WHEN MATCHED AND (
            Target.SupplierName <> Source.SupplierName OR
            Target.Rating <> Source.Rating OR
            Target.LeadTimeDays <> Source.LeadTimeDays OR
            Target.PaymentTerms <> Source.PaymentTerms OR
            Target.IsActive <> Source.IsActive
        ) THEN
            UPDATE SET 
                Target.SupplierName = Source.SupplierName,
                Target.ContactName = Source.ContactName,
                Target.Email = Source.Email,
                Target.Phone = Source.Phone,
                Target.City = Source.City,
                Target.State = Source.State,
                Target.Rating = Source.Rating,
                Target.PaymentTerms = Source.PaymentTerms,
                Target.LeadTimeDays = Source.LeadTimeDays,
                Target.IsActive = Source.IsActive,
                Target.ModifiedDate = SYSUTCDATETIME()
        WHEN NOT MATCHED THEN
            INSERT (
                SupplierID, SupplierName, ContactName, Email, Phone, 
                City, State, Rating, PaymentTerms, LeadTimeDays, IsActive, 
                CreatedDate, ModifiedDate
            )
            VALUES (
                Source.SupplierID, Source.SupplierName, Source.ContactName, Source.Email, Source.Phone,
                Source.City, Source.State, Source.Rating, Source.PaymentTerms, Source.LeadTimeDays, Source.IsActive,
                SYSUTCDATETIME(), SYSUTCDATETIME()
            );

        SET @RowsAffected = @@ROWCOUNT;

        EXEC audit.sp_Log_PipelineExecution 
            @RunID = @RunID, 
            @PipelineName = 'PL_Transform_Warehouse', 
            @ActivityName = 'sp_Load_DimSupplier', 
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
            @ActivityName = 'sp_Load_DimSupplier', 
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
