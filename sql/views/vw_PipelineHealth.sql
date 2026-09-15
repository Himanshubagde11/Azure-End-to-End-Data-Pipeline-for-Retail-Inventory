-- ============================================================================
-- NEXORA INVENTORY INTELLIGENCE
-- View: vw_PipelineHealth
-- Description: Aggregates pipeline execution statuses, data quality pass rates,
--              and rejected record metrics for Power BI Page 6 (Pipeline Health)
-- Author: Senior Data Engineer / Azure Data Architect
-- Organization: NEXORA RETAIL GROUP
-- ============================================================================

CREATE OR ALTER VIEW audit.vw_PipelineHealth
AS
WITH LatestExecutionPerPipeline AS (
    SELECT 
        PipelineName,
        MAX(StartTime) AS LastRunTime
    FROM audit.PipelineExecutionLog
    GROUP BY PipelineName
),
DataQualityMetrics AS (
    SELECT 
        RunID,
        COUNT(*) AS TotalChecksExecuted,
        SUM(CASE WHEN Status = 'PASS' THEN 1 ELSE 0 END) AS PassedChecks,
        SUM(CASE WHEN Status = 'WARNING' THEN 1 ELSE 0 END) AS WarningChecks,
        SUM(CASE WHEN Status = 'FAIL' THEN 1 ELSE 0 END) AS FailedChecks,
        ROUND(AVG(PassPercentage), 2) AS AverageDataQualityScore,
        SUM(TotalRecords) AS TotalEvaluatedRecords,
        SUM(FailedRecords) AS TotalDefectiveRecords
    FROM audit.DataQualityLog
    GROUP BY RunID
)
SELECT 
    pel.LogID,
    pel.RunID,
    pel.PipelineName,
    pel.ActivityName,
    pel.StartTime,
    pel.EndTime,
    DATEDIFF(SECOND, pel.StartTime, ISNULL(pel.EndTime, SYSUTCDATETIME())) AS DurationSeconds,
    pel.Status AS ExecutionStatus,
    pel.RowsProcessed,
    pel.RowsFailed,
    pel.ErrorMessage,
    CASE WHEN lep.LastRunTime IS NOT NULL THEN 1 ELSE 0 END AS IsLatestRun,
    -- Data Quality Score linkage
    ISNULL(dq.AverageDataQualityScore, 100.00) AS RunDataQualityScore,
    ISNULL(dq.PassedChecks, 0) AS DQPassedChecks,
    ISNULL(dq.FailedChecks, 0) AS DQFailedChecks,
    ISNULL(dq.TotalDefectiveRecords, 0) AS DQDefectiveRecords
FROM audit.PipelineExecutionLog pel
LEFT JOIN LatestExecutionPerPipeline lep 
    ON pel.PipelineName = lep.PipelineName 
   AND pel.StartTime = lep.LastRunTime
LEFT JOIN DataQualityMetrics dq 
    ON pel.RunID = dq.RunID;
GO
