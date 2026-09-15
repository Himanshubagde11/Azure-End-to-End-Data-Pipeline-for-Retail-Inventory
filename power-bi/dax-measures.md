# CLARIVENS INVENTORY INTELLIGENCE — PRODUCTION DAX MEASURES SPECIFICATION
**Organization:** CLARIVENS RETAIL GROUP  
**Platform:** Power BI DAX Calculation Engine  
**Version:** 1.0.0 (Production Architecture)

---

## 1. Core Sales & Financial Measures

### `Total Revenue`
Calculates total gross sales revenue in INR across all completed POS transactions.
```dax
Total Revenue = 
SUM ( dw.FactSales[Revenue] )
```
*Format: Currency (`₹#,##0.00`)*

---

### `Total Units Sold`
Total quantity of physical retail units purchased by customers.
```dax
Total Units Sold = 
SUM ( dw.FactSales[Quantity] )
```
*Format: Whole Number (`#,##0`)*

---

### `Total Cost`
Total Cost of Goods Sold (COGS) incurred for merchandise sold.
```dax
Total Cost = 
SUM ( dw.FactSales[Cost] )
```
*Format: Currency (`₹#,##0.00`)*

---

### `Gross Profit`
Gross dollar profit realized after deducting cost of merchandise from net revenue.
```dax
Gross Profit = 
[Total Revenue] - [Total Cost]
```
*Format: Currency (`₹#,##0.00`)*

---

### `Gross Margin %`
The percentage of sales revenue retained as gross profit.
```dax
Gross Margin % = 
DIVIDE (
    [Gross Profit],
    [Total Revenue],
    0.00
)
```
*Format: Percentage (`0.0%`)*

---

### `Average Selling Price (ASP)`
Average realized price per unit sold after promotional discounts.
```dax
Average Selling Price = 
DIVIDE (
    [Total Revenue],
    [Total Units Sold],
    0.00
)
```
*Format: Currency (`₹#,##0.00`)*

---

### `Average Order Value (AOV)`
Average transaction value across individual customer receipts.
```dax
Average Order Value = 
DIVIDE (
    [Total Revenue],
    DISTINCTCOUNT ( dw.FactSales[SaleID] ),
    0.00
)
```
*Format: Currency (`₹#,##0.00`)*

---

## 2. Inventory Health, Stockout Risk & Replenishment Measures

### `Current Stock Units`
Total physical units currently on hand in store warehouses based on the most recent inventory snapshot.
```dax
Current Stock Units = 
VAR LatestDateKey = 
    CALCULATE ( 
        MAX ( dw.FactInventory[DateKey] ), 
        ALL ( dw.DimDate ) 
    )
RETURN
    CALCULATE (
        SUM ( dw.FactInventory[ClosingStock] ),
        dw.FactInventory[DateKey] = LatestDateKey
    )
```
*Format: Whole Number (`#,##0`)*

---

### `Current Inventory Value`
Total monetary valuation of current on-hand retail inventory in INR.
```dax
Current Inventory Value = 
VAR LatestDateKey = 
    CALCULATE ( 
        MAX ( dw.FactInventory[DateKey] ), 
        ALL ( dw.DimDate ) 
    )
RETURN
    CALCULATE (
        SUM ( dw.FactInventory[InventoryValue] ),
        dw.FactInventory[DateKey] = LatestDateKey
    )
```
*Format: Currency (`₹#,##0.00`)*

---

### `Average Daily Sales (ADS)`
Average daily sales volume over the last 30 calendar days of recorded sales.
```dax
Average Daily Sales = 
VAR LastSaleDate = 
    CALCULATE ( 
        MAX ( dw.DimDate[FullDate] ), 
        ALL ( dw.FactSales ) 
    )
VAR StartWindowDate = LastSaleDate - 30
VAR UnitsSoldInWindow = 
    CALCULATE (
        SUM ( dw.FactSales[Quantity] ),
        DATESBETWEEN ( dw.DimDate[FullDate], StartWindowDate, LastSaleDate )
    )
RETURN
    DIVIDE ( UnitsSoldInWindow, 30.0, 0.50 )
```
*Format: Decimal (`#,##0.00`)*

---

### `Days of Inventory (DOI)`
Number of days of customer demand supported by current on-hand stock.
```dax
Days of Inventory = 
DIVIDE (
    [Current Stock Units],
    [Average Daily Sales],
    0.00
)
```
*Format: Decimal (`#,##0.0`)*

---

### `Stockout Products`
Count of product SKUs with 0 on-hand stock in the current snapshot cycle.
```dax
Stockout Products = 
VAR LatestDateKey = 
    CALCULATE ( MAX ( dw.FactInventory[DateKey] ), ALL ( dw.DimDate ) )
RETURN
    CALCULATE (
        DISTINCTCOUNT ( dw.FactInventory[ProductSK] ),
        dw.FactInventory[DateKey] = LatestDateKey,
        dw.FactInventory[ClosingStock] = 0
    )
```
*Format: Whole Number (`#,##0`)*

---

### `Critical Stock Products`
Count of product-store combinations with 3 days or fewer of inventory remaining ($\text{DOI} \le 3$).
```dax
Critical Stock Products = 
VAR LatestDateKey = 
    CALCULATE ( MAX ( dw.FactInventory[DateKey] ), ALL ( dw.DimDate ) )
RETURN
    CALCULATE (
        COUNTROWS ( dw.FactInventory ),
        dw.FactInventory[DateKey] = LatestDateKey,
        dw.FactInventory[StockoutRiskLevel] = "CRITICAL"
    )
```
*Format: Whole Number (`#,##0`)*

---

### `High Risk Products`
Count of product-store combinations with 4 to 7 days of inventory remaining.
```dax
High Risk Products = 
VAR LatestDateKey = 
    CALCULATE ( MAX ( dw.FactInventory[DateKey] ), ALL ( dw.DimDate ) )
RETURN
    CALCULATE (
        COUNTROWS ( dw.FactInventory ),
        dw.FactInventory[DateKey] = LatestDateKey,
        dw.FactInventory[StockoutRiskLevel] = "HIGH"
    )
```
*Format: Whole Number (`#,##0`)*

---

### `Low Stock Products`
Total count of items in either CRITICAL or HIGH risk tiers ($\text{DOI} \le 7$).
```dax
Low Stock Products = 
[Critical Stock Products] + [High Risk Products]
```
*Format: Whole Number (`#,##0`)*

---

### `Reorder Required Products`
Count of product-store combinations where current stock has dropped at or below the SKU's safety reorder level.
```dax
Reorder Required Products = 
VAR LatestDateKey = 
    CALCULATE ( MAX ( dw.FactInventory[DateKey] ), ALL ( dw.DimDate ) )
RETURN
    CALCULATE (
        COUNTROWS ( dw.FactInventory ),
        dw.FactInventory[DateKey] = LatestDateKey,
        dw.FactInventory[ReorderRequired] = 1
    )
```
*Format: Whole Number (`#,##0`)*

---

### `Stockout Rate %`
Proportion of active inventory lines currently in a total stockout state.
```dax
Stockout Rate % = 
VAR LatestDateKey = 
    CALCULATE ( MAX ( dw.FactInventory[DateKey] ), ALL ( dw.DimDate ) )
VAR TotalLines = 
    CALCULATE ( COUNTROWS ( dw.FactInventory ), dw.FactInventory[DateKey] = LatestDateKey )
RETURN
    DIVIDE ( [Stockout Products], TotalLines, 0.00 )
```
*Format: Percentage (`0.0%`)*

---

### `Reorder Rate %`
Proportion of inventory items currently requiring purchase orders.
```dax
Reorder Rate % = 
VAR LatestDateKey = 
    CALCULATE ( MAX ( dw.FactInventory[DateKey] ), ALL ( dw.DimDate ) )
VAR TotalLines = 
    CALCULATE ( COUNTROWS ( dw.FactInventory ), dw.FactInventory[DateKey] = LatestDateKey )
RETURN
    DIVIDE ( [Reorder Required Products], TotalLines, 0.00 )
```
*Format: Percentage (`0.0%`)*

---

### `Inventory Turnover Ratio`
Measures how many times inventory is sold and replaced over an annualized cycle.
```dax
Inventory Turnover = 
VAR AnnualizedCost = [Total Cost]
VAR AvgInvValue = [Current Inventory Value]
RETURN
    DIVIDE ( AnnualizedCost, AvgInvValue, 0.00 )
```
*Format: Decimal (`0.00x`)*

---

## 3. Time Intelligence Measures

### `Revenue MoM`
Month-over-Month absolute change in sales revenue.
```dax
Revenue MoM = 
VAR CurrentMonthRev = [Total Revenue]
VAR PrevMonthRev = 
    CALCULATE (
        [Total Revenue],
        DATEADD ( dw.DimDate[FullDate], -1, MONTH )
    )
RETURN
    IF (
        ISBLANK ( CurrentMonthRev ) || ISBLANK ( PrevMonthRev ),
        BLANK (),
        CurrentMonthRev - PrevMonthRev
    )
```
*Format: Currency (`₹#,##0.00`)*

---

### `Revenue MoM %`
Month-over-Month percentage growth in sales revenue.
```dax
Revenue MoM % = 
VAR CurrentMonthRev = [Total Revenue]
VAR PrevMonthRev = 
    CALCULATE (
        [Total Revenue],
        DATEADD ( dw.DimDate[FullDate], -1, MONTH )
    )
RETURN
    DIVIDE ( CurrentMonthRev - PrevMonthRev, PrevMonthRev, 0.00 )
```
*Format: Percentage (`+0.0%;-0.0%;0.0%`)*

---

### `Revenue YoY`
Year-over-Year change in revenue comparing current period against the same period prior year.
```dax
Revenue YoY = 
VAR CurrentRev = [Total Revenue]
VAR PriorYearRev = 
    CALCULATE (
        [Total Revenue],
        SAMEPERIODLASTYEAR ( dw.DimDate[FullDate] )
    )
RETURN
    CurrentRev - PriorYearRev
```
*Format: Currency (`₹#,##0.00`)*

---

### `Units Sold MoM`
Month-over-Month change in physical units sold volume.
```dax
Units Sold MoM = 
VAR CurrentUnits = [Total Units Sold]
VAR PrevUnits = 
    CALCULATE (
        [Total Units Sold],
        DATEADD ( dw.DimDate[FullDate], -1, MONTH )
    )
RETURN
    CurrentUnits - PrevUnits
```
*Format: Whole Number (`+#,##0;-#,##0;0`)*

---

### `Inventory MoM`
Month-over-Month change in ending physical inventory units.
```dax
Inventory MoM = 
VAR CurrentStock = [Current Stock Units]
VAR PriorMonthStock = 
    CALCULATE (
        [Current Stock Units],
        DATEADD ( dw.DimDate[FullDate], -1, MONTH )
    )
RETURN
    CurrentStock - PriorMonthStock
```
*Format: Whole Number (`+#,##0;-#,##0;0`)*

---

## 4. Procurement, Customer Returns & Pipeline Health

### `Total Returns`
Total count of customer return transactions processed at store service desks.
```dax
Total Returns = 
COUNTROWS ( dw.FactReturns )
```
*Format: Whole Number (`#,##0`)*

---

### `Total Refund Amount`
Total monetary refunds credited to customers for returned merchandise.
```dax
Total Refund Amount = 
SUM ( dw.FactReturns[RefundAmount] )
```
*Format: Currency (`₹#,##0.00`)*

---

### `Return Rate %`
Ratio of returned merchandise units relative to total units sold.
```dax
Return Rate % = 
DIVIDE (
    SUM ( dw.FactReturns[Quantity] ),
    [Total Units Sold],
    0.00
)
```
*Format: Percentage (`0.00%`)*

---

### `Supplier On-Time Delivery %`
Percentage of procurement purchase orders delivered on or prior to the contractual expected delivery date.
```dax
Supplier On-Time Delivery % = 
VAR CompletedPOs = 
    CALCULATE (
        COUNTROWS ( dw.FactPurchases ),
        dw.FactPurchases[Status] IN { "Completed", "Delayed" }
    )
VAR OnTimePOs = 
    CALCULATE (
        COUNTROWS ( dw.FactPurchases ),
        dw.FactPurchases[DeliveryVarianceDays] <= 0,
        dw.FactPurchases[Status] = "Completed"
    )
RETURN
    DIVIDE ( OnTimePOs, CompletedPOs, 0.00 )
```
*Format: Percentage (`0.0%`)*

---

### `Data Quality Score`
Overall platform Data Quality Score derived from the automated Python evaluation engine logs in `audit.DataQualityLog`.
```dax
Data Quality Score = 
VAR LatestRunID = 
    CALCULATE ( 
        MAX ( audit.DataQualityLog[RunID] ), 
        ALL ( audit.DataQualityLog ) 
    )
RETURN
    CALCULATE (
        ROUND ( AVG ( audit.DataQualityLog[PassPercentage] ), 2 ),
        audit.DataQualityLog[RunID] = LatestRunID
    )
```
*Format: Percentage (`0.00%`)*

---

### `Pipeline Health Score`
Execution success rate of all Azure Data Factory and warehouse transformation activities over the last 30 runs.
```dax
Pipeline Health Score = 
VAR TotalRuns = COUNTROWS ( audit.PipelineExecutionLog )
VAR SuccessfulRuns = 
    CALCULATE (
        COUNTROWS ( audit.PipelineExecutionLog ),
        audit.PipelineExecutionLog[Status] = "SUCCESS"
    )
RETURN
    DIVIDE ( SuccessfulRuns, TotalRuns, 1.00 )
```
*Format: Percentage (`0.0%`)*
