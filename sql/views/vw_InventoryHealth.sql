-- ============================================================================
-- CLARIVENS INVENTORY INTELLIGENCE
-- View: vw_InventoryHealth
-- Description: Consolidated semantic view combining inventory snapshots, product dimensions,
--              and store locations with stockout risk indicators for Power BI
-- Author: Senior Data Engineer / Azure Data Architect
-- Organization: CLARIVENS RETAIL GROUP
-- ============================================================================

CREATE OR ALTER VIEW dw.vw_InventoryHealth
AS
WITH LatestSnapshotPerStoreProduct AS (
    SELECT 
        fi.StoreSK,
        fi.ProductSK,
        MAX(fi.DateKey) AS MaxDateKey
    FROM dw.FactInventory fi
    GROUP BY fi.StoreSK, fi.ProductSK
)
SELECT 
    fi.InventorySK,
    fi.InventoryID,
    d.FullDate AS SnapshotDate,
    d.CalendarYear,
    d.MonthName,
    d.WeekNumberOfYear,
    -- Store Attributes
    ds.StoreID,
    ds.StoreName,
    ds.City AS StoreCity,
    ds.State AS StoreState,
    ds.Region AS StoreRegion,
    ds.StoreType,
    -- Product Attributes
    dp.ProductID,
    dp.ProductName,
    dp.CategoryID,
    dp.CategoryName,
    dp.Department,
    dp.Brand,
    dp.UnitCost,
    dp.UnitPrice,
    dp.ReorderLevel,
    dp.ReorderQuantity,
    -- Stock Quantities
    fi.OpeningStock,
    fi.ReceivedQuantity,
    fi.SoldQuantity,
    fi.ReturnQuantity,
    fi.DamagedQuantity,
    fi.ClosingStock,
    fi.InventoryValue,
    -- Replenishment Velocity & Risk Metrics
    fi.AverageDailySales,
    fi.DaysOfInventory,
    fi.StockoutRiskLevel,
    fi.ReorderRequired,
    -- Flag for current latest available snapshot
    CASE 
        WHEN l.MaxDateKey IS NOT NULL THEN 1 
        ELSE 0 
    END AS IsCurrentSnapshot
FROM dw.FactInventory fi
INNER JOIN dw.DimDate d ON fi.DateKey = d.DateKey
INNER JOIN dw.DimProduct dp ON fi.ProductSK = dp.ProductSK
INNER JOIN dw.DimStore ds ON fi.StoreSK = ds.StoreSK
LEFT JOIN LatestSnapshotPerStoreProduct l 
    ON fi.StoreSK = l.StoreSK 
   AND fi.ProductSK = l.ProductSK 
   AND fi.DateKey = l.MaxDateKey;
GO
