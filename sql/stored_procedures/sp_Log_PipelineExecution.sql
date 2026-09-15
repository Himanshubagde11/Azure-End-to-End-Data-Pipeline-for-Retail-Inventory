-- ============================================================================
-- CLARIVENS INVENTORY INTELLIGENCE
-- Procedure: sp_Log_PipelineExecution
-- Description: Centralized procedure to log execution state from ADF, Python, or SQL procedures
-- Author: Senior Data Engineer / Azure Data Architect
-- Organization: CLARIVENS RETAIL GROUP
-- ============================================================================

CREATE OR ALTER PROCEDURE audit.sp_Log_PipelineExecution
    @RunID          VARCHAR(64),
    @PipelineName   VARCHAR(100),
    @ActivityName   VARCHAR(100),
    @StartTime      DATETIME2,
    @EndTime        DATETIME2 = NULL,
    @Status         VARCHAR(20),
    @RowsProcessed  BIGINT = 0,
    @RowsFailed     BIGINT = 0,
    @ErrorMessage   NVARCHAR(MAX) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO audit.PipelineExecutionLog (
        RunID, PipelineName, ActivityName, StartTime, EndTime, 
        Status, RowsProcessed, RowsFailed, ErrorMessage, CreatedDate
    )
    VALUES (
        @RunID, @PipelineName, @ActivityName, @StartTime, @EndTime, 
        @Status, @RowsProcessed, @RowsFailed, @ErrorMessage, SYSUTCDATETIME()
    );
END
GO
