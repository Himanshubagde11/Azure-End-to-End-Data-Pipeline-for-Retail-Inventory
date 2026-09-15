-- ============================================================================
-- CLARIVENS INVENTORY INTELLIGENCE
-- Procedure: sp_Load_DimDate
-- Description: Generates calendar dates from 2024-01-01 to 2026-12-31 with retail attributes
-- Author: Himanshu Bagde (Azure Data Engineer & Cloud Analytics Architect)
-- Organization: CLARIVENS RETAIL GROUP
-- ============================================================================

CREATE OR ALTER PROCEDURE dw.sp_Load_DimDate
    @StartDate DATE = '2024-01-01',
    @EndDate DATE = '2026-12-31'
AS
BEGIN
    SET NOCOUNT ON;

    PRINT 'Populating dw.DimDate from ' + CAST(@StartDate AS VARCHAR(20)) + ' to ' + CAST(@EndDate AS VARCHAR(20));

    ;WITH DateSeries AS (
        SELECT @StartDate AS CurrentDate
        UNION ALL
        SELECT DATEADD(DAY, 1, CurrentDate)
        FROM DateSeries
        WHERE CurrentDate < @EndDate
    )
    MERGE dw.DimDate AS Target
    USING (
        SELECT 
            CAST(FORMAT(CurrentDate, 'yyyyMMdd') AS INT) AS DateKey,
            CurrentDate AS FullDate,
            DATEPART(WEEKDAY, CurrentDate) AS DayNumberOfWeek,
            DATENAME(WEEKDAY, CurrentDate) AS DayName,
            DAY(CurrentDate) AS DayNumberOfMonth,
            DATEPART(DAYOFYEAR, CurrentDate) AS DayNumberOfYear,
            DATEPART(WEEK, CurrentDate) AS WeekNumberOfYear,
            DATENAME(MONTH, CurrentDate) AS MonthName,
            MONTH(CurrentDate) AS MonthNumberOfYear,
            DATEPART(QUARTER, CurrentDate) AS CalendarQuarter,
            YEAR(CurrentDate) AS CalendarYear,
            CASE 
                WHEN MONTH(CurrentDate) >= 4 THEN YEAR(CurrentDate)
                ELSE YEAR(CurrentDate) - 1
            END AS FiscalYear,
            CASE 
                WHEN MONTH(CurrentDate) BETWEEN 4 AND 6 THEN 1
                WHEN MONTH(CurrentDate) BETWEEN 7 AND 9 THEN 2
                WHEN MONTH(CurrentDate) BETWEEN 10 AND 12 THEN 3
                ELSE 4
            END AS FiscalQuarter,
            CASE 
                WHEN DATEPART(WEEKDAY, CurrentDate) IN (1, 7) THEN 1 
                ELSE 0 
            END AS IsWeekend,
            CASE 
                -- Diwali and festive peak season in Indian retail (Oct - Nov)
                WHEN MONTH(CurrentDate) IN (10, 11) THEN 1 
                ELSE 0 
            END AS IsFestivalSeason
        FROM DateSeries
    ) AS Source
    ON Target.DateKey = Source.DateKey
    WHEN NOT MATCHED THEN
        INSERT (
            DateKey, FullDate, DayNumberOfWeek, DayName, DayNumberOfMonth, 
            DayNumberOfYear, WeekNumberOfYear, MonthName, MonthNumberOfYear, 
            CalendarQuarter, CalendarYear, FiscalYear, FiscalQuarter, IsWeekend, IsFestivalSeason
        )
        VALUES (
            Source.DateKey, Source.FullDate, Source.DayNumberOfWeek, Source.DayName, Source.DayNumberOfMonth,
            Source.DayNumberOfYear, Source.WeekNumberOfYear, Source.MonthName, Source.MonthNumberOfYear,
            Source.CalendarQuarter, Source.CalendarYear, Source.FiscalYear, Source.FiscalQuarter, Source.IsWeekend, Source.IsFestivalSeason
        )
    OPTION (MAXRECURSION 1200);

    PRINT 'dw.DimDate populated successfully.';
END
GO
