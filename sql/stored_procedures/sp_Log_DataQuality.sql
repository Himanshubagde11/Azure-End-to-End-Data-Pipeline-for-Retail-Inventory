-- ============================================================================
-- NEXORA INVENTORY INTELLIGENCE
-- Procedure: sp_Log_DataQuality
-- Description: Records structured validation results from the Python Data Quality Engine
-- Author: Senior Data Engineer / Azure Data Architect
-- Organization: NEXORA RETAIL GROUP
-- ============================================================================

CREATE OR ALTER PROCEDURE audit.sp_Log_DataQuality
    @RunID          VARCHAR(64),
    @TableName      VARCHAR(50),
    @CheckType      VARCHAR(50),
    @RuleName       VARCHAR(100),
    @TotalRecords   BIGINT,
    @FailedRecords  BIGINT,
    @PassPercentage DECIMAL(5,2),
    @Status         VARCHAR(20),
    @ErrorMessage   NVARCHAR(MAX) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO audit.DataQualityLog (
        RunID, TableName, CheckType, RuleName, TotalRecords, 
        FailedRecords, PassPercentage, Status, ExecutionTime, ErrorMessage
    )
    VALUES (
        @RunID, @TableName, @CheckType, @RuleName, @TotalRecords, 
        @FailedRecords, @PassPercentage, @Status, SYSUTCDATETIME(), @ErrorMessage
    );
END
GO
