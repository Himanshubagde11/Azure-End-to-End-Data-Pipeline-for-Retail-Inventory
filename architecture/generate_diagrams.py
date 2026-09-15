"""
NEXORA INVENTORY INTELLIGENCE
Architecture & Flow Diagram Generator
Author: Senior Data Engineer / Azure Data Architect
Organization: NEXORA RETAIL GROUP

Generates 3 presentation-ready architectural diagrams:
1. architecture-diagram.png: Full Cloud Architecture (ADLS, ADF, Azure SQL, Python DQ, Power BI, Monitoring)
2. data-flow.png: End-to-End Data Pipeline Flow & Quality Gates
3. star-schema.png: Star Schema Dimensional Model ERD
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = os.path.dirname(__file__)

BG_COLOR = "#0B132B"
CARD_BG = "#1C2541"
BORDER_COLOR = "#2E3D5C"
CYAN = "#48CAE4"
BLUE = "#0077B6"
TEAL = "#2EC4B6"
AMBER = "#FFB703"
RED = "#E63946"
WHITE = "#F8F9FA"
MUTED = "#8D99AE"

def create_architecture_diagram():
    print("Generating architecture-diagram.png...")
    fig, ax = plt.subplots(figsize=(16, 10), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    # Header
    ax.text(0.04, 0.95, "NEXORA INVENTORY INTELLIGENCE", color=CYAN, fontsize=16, fontweight="bold")
    ax.text(0.04, 0.92, "Production End-to-End Architecture: Azure Data Factory, Azure SQL Database, Python DQ & Power BI", color=MUTED, fontsize=10)

    # 4 Architecture Columns / Swimlanes
    columns = [
        ("1. INGESTION & SOURCES", 0.04, 0.20, [
            ("CSV Files (ADLS Gen2)", "12 Monthly Sales (120k+ rows)\n12 Weekly Inventory (42k+ rows)\nProducts, Stores, Suppliers\nPurchases & Returns"),
            ("Mock REST API", "Supplier Catalog & SLAs\nDynamic Replenishment Feed\nBearer Token Auth & Pagination")
        ]),
        ("2. ORCHESTRATION & DQ", 0.27, 0.22, [
            ("Azure Data Factory v2", "PL_Master_Retail_Inventory\n11 Parameterized Child Pipelines\nSchedule & Tumbling Triggers\nCopy Activities with Retries"),
            ("Python Data Quality Gate", "12 Validation Rules\nSchema, Nulls, Duplicates\nMath Stock Balance Equation\nCalculates DQ Score (Gate >= 95%)")
        ]),
        ("3. STORAGE & WAREHOUSE", 0.52, 0.22, [
            ("Staging Layer (stg.*)", "Raw Landing Tables\nIngestion Auditing Timestamps\nPre-Copy Truncate & Bulk Insert"),
            ("Star Schema Warehouse (dw.*)", "FactSales, FactInventory, FactPurchases\nDimDate, DimProduct, DimStore\nDimSupplier, DimCategory\nSCD Type 1/2 & Surrogate Keys")
        ]),
        ("4. ANALYTICS & OBSERVABILITY", 0.77, 0.20, [
            ("Power BI Analytics Suite", "6 Executive & Operational Pages\nInventory Intelligence Risk Matrix\n25+ DAX Measures & Themes\nDrillthrough & Slicers"),
            ("Centralized Audit & Control", "audit.PipelineExecutionLog\naudit.DataQualityLog\naudit.ETL_Control (Watermarking)")
        ])
    ]

    for col_title, x, w, boxes in columns:
        # Outer container
        rect_col = patches.FancyBboxPatch((x, 0.05), w, 0.83, boxstyle="round,pad=0.015",
                                         facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1.5)
        ax.add_patch(rect_col)
        ax.text(x + 0.015, 0.84, col_title, color=CYAN, fontsize=10, fontweight="bold")

        # Inner components
        y_box = 0.50
        for title, desc in boxes:
            rect_b = patches.FancyBboxPatch((x + 0.012, y_box), w - 0.024, 0.30, boxstyle="round,pad=0.01",
                                           facecolor="#141E33", edgecolor=BORDER_COLOR, linewidth=1)
            ax.add_patch(rect_b)
            ax.text(x + 0.022, y_box + 0.25, title, color=WHITE, fontsize=10, fontweight="bold")
            ax.text(x + 0.022, y_box + 0.04, desc, color=MUTED, fontsize=8, linespacing=1.6)
            y_box -= 0.38

    # Connecting Arrows
    arrow_props = dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=CYAN, lw=2)
    ax.annotate("", xy=(0.27, 0.65), xytext=(0.24, 0.65), arrowprops=arrow_props)
    ax.annotate("", xy=(0.52, 0.65), xytext=(0.49, 0.65), arrowprops=arrow_props)
    ax.annotate("", xy=(0.77, 0.65), xytext=(0.74, 0.65), arrowprops=arrow_props)

    # Bottom Audit feedback loop arrow
    ax.annotate("", xy=(0.38, 0.20), xytext=(0.77, 0.20),
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=AMBER, lw=1.5, ls="--"))
    ax.text(0.55, 0.22, "Telemetry & Watermark Feedback", color=AMBER, fontsize=8, ha="center")

    plt.savefig(os.path.join(OUTPUT_DIR, "architecture-diagram.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print("  -> Saved architecture-diagram.png")

def create_data_flow_diagram():
    print("Generating data-flow.png...")
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    ax.text(0.04, 0.95, "NEXORA INVENTORY INTELLIGENCE — END-TO-END DATA FLOW", color=CYAN, fontsize=16, fontweight="bold")
    ax.text(0.04, 0.92, "Sequential Ingestion, Quality Evaluation, Incremental Watermarking & Star Schema Load", color=MUTED, fontsize=10)

    steps = [
        ("Step 1: Ingestion", "ADLS Gen2 CSVs & REST API\nIngested into stg.* tables\nADF Copy Activities with retries", 0.05, 0.50, CYAN),
        ("Step 2: Quality Gate", "Python Validation Engine\nEvaluates 12 core rules\nScore >= 95% required to pass", 0.28, 0.50, AMBER),
        ("Step 3: Stored Procs", "dw.sp_Load_FactSales\ndw.sp_Load_FactInventory\nCleanses & links surrogate keys", 0.51, 0.50, BLUE),
        ("Step 4: Metric Engine", "sp_Update_InventoryMetrics\nCalculates ADS & Days of Inventory\nTags Critical / High Risk", 0.74, 0.50, TEAL)
    ]

    for title, desc, x, y, col in steps:
        rect = patches.FancyBboxPatch((x, y - 0.12), 0.20, 0.28, boxstyle="round,pad=0.015",
                                     facecolor=CARD_BG, edgecolor=col, linewidth=2)
        ax.add_patch(rect)
        ax.text(x + 0.015, y + 0.11, title, color=col, fontsize=11, fontweight="bold")
        ax.text(x + 0.015, y - 0.08, desc, color=WHITE, fontsize=8.5, linespacing=1.6)

    # Arrows between main steps
    for start_x in [0.25, 0.48, 0.71]:
        ax.annotate("", xy=(start_x + 0.03, 0.52), xytext=(start_x, 0.52),
                    arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=CYAN, lw=2.5))

    # Lower Observability Box
    rect_obs = patches.FancyBboxPatch((0.05, 0.10), 0.89, 0.20, boxstyle="round,pad=0.015",
                                      facecolor="#141E33", edgecolor=BORDER_COLOR, linewidth=1.5)
    ax.add_patch(rect_obs)
    ax.text(0.07, 0.25, "CENTRALIZED OBSERVABILITY & HIGH-WATERMARK CONTROLS", color=CYAN, fontsize=11, fontweight="bold")
    ax.text(0.07, 0.15,
            "• audit.ETL_Control: High-watermark mechanism tracking LastWatermarkValue (SaleDate) to ensure only Delta transactions are ingested.\n"
            "• audit.DataQualityLog: Structured record of every validation check (RuleName, TotalRecords, FailedRecords, PassPercentage, Status).\n"
            "• audit.PipelineExecutionLog: Full activity execution telemetry (RunID, ActivityName, RowsProcessed, RowsFailed, ErrorMessage).",
            color=MUTED, fontsize=9, linespacing=1.5)

    plt.savefig(os.path.join(OUTPUT_DIR, "data-flow.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print("  -> Saved data-flow.png")

def create_star_schema_diagram():
    print("Generating star-schema.png...")
    fig, ax = plt.subplots(figsize=(16, 10), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    ax.text(0.04, 0.95, "NEXORA INVENTORY INTELLIGENCE — STAR SCHEMA DATA MODEL", color=CYAN, fontsize=16, fontweight="bold")
    ax.text(0.04, 0.92, "Enterprise Dimensional Architecture in Azure SQL Database (dw schema)", color=MUTED, fontsize=10)

    # Central Fact Tables
    facts = [
        ("dw.FactSales", 0.38, 0.55, 0.24, 0.32, [
            ("SalesSK (PK)", True), ("SaleID", False), ("DateKey (FK)", True),
            ("ProductSK (FK)", True), ("StoreSK (FK)", True), ("Quantity", False),
            ("Revenue", False), ("Cost", False), ("GrossProfit", False), ("PaymentMethod", False)
        ]),
        ("dw.FactInventory", 0.38, 0.12, 0.24, 0.36, [
            ("InventorySK (PK)", True), ("InventoryID", False), ("DateKey (FK)", True),
            ("ProductSK (FK)", True), ("StoreSK (FK)", True), ("OpeningStock", False),
            ("ReceivedQuantity", False), ("ClosingStock", False), ("InventoryValue", False),
            ("DaysOfInventory", False), ("StockoutRiskLevel", False), ("ReorderRequired", False)
        ])
    ]

    # Surrounding Dimension Tables
    dimensions = [
        ("dw.DimProduct", 0.06, 0.55, 0.22, 0.32, [
            ("ProductSK (PK)", True), ("ProductID", False), ("ProductName", False),
            ("CategoryID (FK)", True), ("CategoryName", False), ("Brand", False),
            ("UnitCost", False), ("UnitPrice", False), ("ReorderLevel", False), ("IsCurrent", False)
        ]),
        ("dw.DimStore", 0.06, 0.15, 0.22, 0.28, [
            ("StoreSK (PK)", True), ("StoreID", False), ("StoreName", False),
            ("City", False), ("State", False), ("Region", False), ("StoreType", False), ("SquareFeet", False)
        ]),
        ("dw.DimDate", 0.72, 0.55, 0.22, 0.32, [
            ("DateKey (PK)", True), ("FullDate", False), ("DayName", False),
            ("MonthName", False), ("CalendarQuarter", False), ("CalendarYear", False),
            ("FiscalQuarter", False), ("IsFestivalSeason", False), ("IsWeekend", False)
        ]),
        ("dw.DimSupplier", 0.72, 0.15, 0.22, 0.28, [
            ("SupplierSK (PK)", True), ("SupplierID", False), ("SupplierName", False),
            ("City", False), ("State", False), ("Rating", False), ("LeadTimeDays", False), ("PaymentTerms", False)
        ])
    ]

    def draw_table_card(title, x, y, w, h, cols, is_fact=False):
        header_col = BLUE if is_fact else BORDER_COLOR
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01",
                                     facecolor=CARD_BG, edgecolor=CYAN if is_fact else BORDER_COLOR, linewidth=1.5)
        ax.add_patch(rect)
        rect_hdr = patches.Rectangle((x, y + h - 0.04), w, 0.04, facecolor="#141E33", edgecolor=BORDER_COLOR)
        ax.add_patch(rect_hdr)
        ax.text(x + 0.01, y + h - 0.025, title, color=CYAN if is_fact else WHITE, fontsize=9.5, fontweight="bold")

        curr_y = y + h - 0.07
        for cname, is_key in cols:
            k_col = CYAN if is_key else WHITE
            fontw = "bold" if is_key else "normal"
            ax.text(x + 0.015, curr_y, cname, color=k_col, fontsize=8, fontweight=fontw)
            curr_y -= 0.027

    for title, x, y, w, h, cols in facts:
        draw_table_card(title, x, y, w, h, cols, is_fact=True)

    for title, x, y, w, h, cols in dimensions:
        draw_table_card(title, x, y, w, h, cols, is_fact=False)

    # Relationship connectors
    conn_props = dict(arrowstyle="<->", color=CYAN, lw=1.5, ls="--")
    # DimProduct to FactSales
    ax.annotate("", xy=(0.38, 0.72), xytext=(0.28, 0.72), arrowprops=conn_props)
    # DimDate to FactSales
    ax.annotate("", xy=(0.62, 0.72), xytext=(0.72, 0.72), arrowprops=conn_props)
    # DimStore to FactSales
    ax.annotate("", xy=(0.38, 0.60), xytext=(0.28, 0.30), arrowprops=conn_props)
    # DimProduct to FactInventory
    ax.annotate("", xy=(0.38, 0.28), xytext=(0.28, 0.60), arrowprops=conn_props)
    # DimStore to FactInventory
    ax.annotate("", xy=(0.38, 0.22), xytext=(0.28, 0.22), arrowprops=conn_props)
    # DimDate to FactInventory
    ax.annotate("", xy=(0.62, 0.28), xytext=(0.72, 0.60), arrowprops=conn_props)

    plt.savefig(os.path.join(OUTPUT_DIR, "star-schema.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print("  -> Saved star-schema.png")

def main():
    print("==========================================================================")
    print(" NEXORA INVENTORY INTELLIGENCE — ARCHITECTURE DIAGRAM GENERATOR")
    print(" Rendering Presentation-Ready Architecture Diagrams")
    print("==========================================================================")
    create_architecture_diagram()
    create_data_flow_diagram()
    create_star_schema_diagram()
    print("==========================================================================")
    print(f" All 3 Architecture Diagrams saved in {OUTPUT_DIR}")
    print("==========================================================================")

if __name__ == "__main__":
    main()
