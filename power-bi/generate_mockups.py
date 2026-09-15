"""
NEXORA INVENTORY INTELLIGENCE
High-Fidelity Power BI Dashboard Mockup Generator
Author: Senior Data Engineer / Azure Data Architect / Power BI Specialist
Organization: NEXORA RETAIL GROUP

Renders pixel-perfect, dark enterprise dashboard screenshots for all 6 Power BI pages:
1. Executive Overview
2. Inventory Intelligence
3. Sales Analytics
4. Store Performance
5. Product & Supplier Analysis
6. Data Pipeline Health
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Brand Color Palette
BG_COLOR = "#0B132B"
CARD_BG = "#1C2541"
CARD_BORDER = "#2E3D5C"
ACCENT_CYAN = "#48CAE4"
ACCENT_BLUE = "#0077B6"
ACCENT_TEAL = "#2EC4B6"
ACCENT_AMBER = "#FFB703"
ACCENT_RED = "#E63946"
TEXT_WHITE = "#F8F9FA"
TEXT_MUTED = "#8D99AE"

def draw_header(ax, title, subtitle):
    # Top navbar
    rect = patches.Rectangle((0, 0.92), 1, 0.08, transform=ax.transAxes, facecolor="#141E33", edgecolor="#2E3D5C", linewidth=1)
    ax.add_patch(rect)
    ax.text(0.02, 0.965, "NEXORA INVENTORY INTELLIGENCE", transform=ax.transAxes, color=ACCENT_CYAN, fontsize=14, fontweight="bold", va="center")
    ax.text(0.02, 0.935, f"NEXORA RETAIL GROUP  |  {title.upper()}  |  {subtitle}", transform=ax.transAxes, color=TEXT_MUTED, fontsize=9, va="center")
    ax.text(0.98, 0.95, "Data As Of: 2025-12-31 | Refresh: Automated (ADF)", transform=ax.transAxes, color=TEXT_WHITE, fontsize=9, ha="right", va="center")

def draw_kpi_card(ax, x, y, w, h, label, value, subtext="", status_color=ACCENT_CYAN):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.015",
                                  transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER, linewidth=1)
    ax.add_patch(rect)
    ax.text(x + 0.012, y + h - 0.028, label.upper(), transform=ax.transAxes, color=TEXT_MUTED, fontsize=8, fontweight="bold")
    ax.text(x + 0.012, y + 0.038, value, transform=ax.transAxes, color=status_color, fontsize=16, fontweight="bold")
    if subtext:
        ax.text(x + 0.012, y + 0.015, subtext, transform=ax.transAxes, color=TEXT_WHITE, fontsize=7)

def create_page_1():
    print("Generating Page 1: Executive Overview...")
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    draw_header(ax, "Executive Overview", "Enterprise Sales & Inventory High-Level KPIs")

    # Top KPI row
    kpis = [
        ("Total Revenue", "₹142.8M", "+18.4% YoY", ACCENT_CYAN),
        ("Units Sold", "284,520", "+12.1% YoY", ACCENT_TEAL),
        ("Gross Profit", "₹48.6M", "34.0% Gross Margin", ACCENT_CYAN),
        ("Inventory Value", "₹64.2M", "42,640 Snapshots", ACCENT_BLUE),
        ("Days of Inventory", "18.4 Days", "Target: 15-20 Days", ACCENT_TEAL),
        ("Stockout Risk Alerts", "148 SKUs", "Critical: 42 | High: 106", ACCENT_RED)
    ]
    for i, (lbl, val, sub, col) in enumerate(kpis):
        draw_kpi_card(ax, 0.02 + i * 0.162, 0.77, 0.152, 0.12, lbl, val, sub, col)

    # Chart 1: Monthly Revenue Trend (left half)
    rect1 = patches.FancyBboxPatch((0.02, 0.38), 0.58, 0.36, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect1)
    ax.text(0.04, 0.71, "2025 MONTHLY REVENUE & GROSS PROFIT TREND (INR Millions)", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10, fontweight="bold")

    sub_ax1 = fig.add_axes([0.06, 0.42, 0.52, 0.26], facecolor=CARD_BG)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    rev = [9.8, 10.2, 10.8, 12.4, 11.2, 12.9, 10.5, 11.1, 13.2, 14.8, 16.2, 12.1]
    profit = [3.3, 3.5, 3.7, 4.2, 3.8, 4.4, 3.6, 3.8, 4.5, 5.0, 5.5, 4.1]
    
    sub_ax1.bar(np.arange(12) - 0.18, rev, width=0.36, color=ACCENT_CYAN, label="Revenue")
    sub_ax1.bar(np.arange(12) + 0.18, profit, width=0.36, color=ACCENT_TEAL, label="Gross Profit")
    sub_ax1.set_xticks(range(12))
    sub_ax1.set_xticklabels(months, color=TEXT_WHITE, fontsize=8)
    sub_ax1.tick_params(colors=TEXT_WHITE, labelsize=8)
    sub_ax1.legend(facecolor=CARD_BG, edgecolor=CARD_BORDER, labelcolor=TEXT_WHITE, fontsize=8)
    sub_ax1.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    # Chart 2: Revenue by Category (right half)
    rect2 = patches.FancyBboxPatch((0.62, 0.38), 0.36, 0.36, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect2)
    ax.text(0.64, 0.71, "REVENUE SHARE BY CATEGORY", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10, fontweight="bold")

    sub_ax2 = fig.add_axes([0.64, 0.41, 0.32, 0.28], facecolor=CARD_BG)
    cats = ["Electronics", "Home Appl.", "Personal Care", "Grocery", "Beverages", "Home/Kitchen", "Sports"]
    cat_rev = [38.4, 26.2, 18.5, 19.8, 14.2, 15.1, 10.6]
    y_pos = np.arange(len(cats))
    sub_ax2.barh(y_pos, cat_rev, color=ACCENT_BLUE)
    sub_ax2.set_yticks(y_pos)
    sub_ax2.set_yticklabels(cats, color=TEXT_WHITE, fontsize=8)
    sub_ax2.invert_yaxis()
    sub_ax2.tick_params(colors=TEXT_WHITE, labelsize=8)
    sub_ax2.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    # Bottom Row: Regional Store Performance & Inventory Stockout Status
    rect3 = patches.FancyBboxPatch((0.02, 0.03), 0.46, 0.32, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect3)
    ax.text(0.04, 0.32, "TOP 5 PERFORMING REGIONAL CLUSTERS", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10, fontweight="bold")

    sub_ax3 = fig.add_axes([0.06, 0.06, 0.40, 0.23], facecolor=CARD_BG)
    regions = ["West (Mumbai/Pune)", "South (Bengaluru/Hyd)", "North (Delhi/Jaipur)", "East (Kolkata)", "Central (Nagpur)"]
    reg_sales = [52.4, 46.1, 28.5, 11.2, 4.6]
    sub_ax3.barh(range(len(regions)), reg_sales, color=ACCENT_TEAL)
    sub_ax3.set_yticks(range(len(regions)))
    sub_ax3.set_yticklabels(regions, color=TEXT_WHITE, fontsize=8)
    sub_ax3.invert_yaxis()
    sub_ax3.tick_params(colors=TEXT_WHITE, labelsize=8)
    sub_ax3.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    rect4 = patches.FancyBboxPatch((0.50, 0.03), 0.48, 0.32, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect4)
    ax.text(0.52, 0.32, "INVENTORY STOCKOUT RISK LEVEL DISTRIBUTION", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10, fontweight="bold")

    sub_ax4 = fig.add_axes([0.55, 0.05, 0.38, 0.24], facecolor=CARD_BG)
    risk_labels = ["Low Risk (>14d)", "Medium (8-14d)", "High Risk (4-7d)", "Critical (<=3d)"]
    risk_counts = [28450, 9420, 3120, 1650]
    risk_colors = [ACCENT_TEAL, ACCENT_BLUE, ACCENT_AMBER, ACCENT_RED]
    sub_ax4.pie(risk_counts, labels=risk_labels, colors=risk_colors, autopct="%1.1f%%",
                textprops={"color": TEXT_WHITE, "fontsize": 8}, startangle=140)

    plt.savefig(os.path.join(OUTPUT_DIR, "01_executive_overview.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print("  -> Saved 01_executive_overview.png")

def create_page_2():
    print("Generating Page 2: Inventory Intelligence...")
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    draw_header(ax, "Inventory Intelligence", "Stockout Risk, Replenishment Velocity & Reorder Alerts")

    kpis = [
        ("Current On-Hand", "412,800 Units", "Across 36 Stores", ACCENT_CYAN),
        ("Inventory Value", "₹64.25M", "Valued at UnitCost", ACCENT_BLUE),
        ("Days of Inventory", "18.4 Days", "Demand Coverage", ACCENT_TEAL),
        ("Critical Stock (<=3d)", "42 Items", "Immediate Stockout Risk", ACCENT_RED),
        ("High Risk (4-7d)", "106 Items", "Expedite Reorder", ACCENT_AMBER),
        ("Reorder Required", "248 Alerts", "Stock <= ReorderLevel", ACCENT_RED)
    ]
    for i, (lbl, val, sub, col) in enumerate(kpis):
        draw_kpi_card(ax, 0.02 + i * 0.162, 0.77, 0.152, 0.12, lbl, val, sub, col)

    # Main Grid: Inventory Risk Action Table (Mocked layout)
    rect_table = patches.FancyBboxPatch((0.02, 0.03), 0.65, 0.71, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect_table)
    ax.text(0.04, 0.71, "CRITICAL & HIGH STOCKOUT RISK ACTION MATRIX", transform=ax.transAxes, color=TEXT_WHITE, fontsize=11, fontweight="bold")
    ax.text(0.04, 0.685, "Showing active product/store combinations with immediate stockout vulnerability", transform=ax.transAxes, color=TEXT_MUTED, fontsize=8)

    # Draw tabular mock data
    headers = ["Product Name", "Store Location", "Stock", "ADS", "Days Left", "Risk Tier", "Reorder Qty"]
    col_x = [0.04, 0.28, 0.40, 0.46, 0.51, 0.57, 0.63]
    for h_idx, (h_name, hx) in enumerate(zip(headers, col_x)):
        ax.text(hx, 0.65, h_name.upper(), transform=ax.transAxes, color=ACCENT_CYAN, fontsize=8, fontweight="bold")

    # Sample critical items
    table_rows = [
        ("Sony UltraHD Smart LED TV Pro 420", "Bengaluru Flagship #1", "4", "2.8", "1.4 d", "CRITICAL", "50 units", ACCENT_RED),
        ("boAt Wireless Headphones Elite 88", "Mumbai Supermarket #3", "6", "3.4", "1.8 d", "CRITICAL", "120 units", ACCENT_RED),
        ("Real Cold Pressed Juice Mango 1L", "Pune Express #2", "12", "5.1", "2.4 d", "CRITICAL", "180 units", ACCENT_RED),
        ("Mamaearth Face Moisturizer 100ml", "Delhi Hypermarket #1", "18", "6.2", "2.9 d", "CRITICAL", "100 units", ACCENT_RED),
        ("Tata Sampann Toor Dal 1kg", "Ahmedabad Flagship #1", "25", "5.8", "4.3 d", "HIGH", "250 units", ACCENT_AMBER),
        ("Prestige Induction Cooktop 2000W", "Hyderabad Supermarket #2", "14", "2.9", "4.8 d", "HIGH", "75 units", ACCENT_AMBER),
        ("Decathlon Yoga Mat High Density", "Chennai Hypermarket #1", "16", "3.1", "5.2 d", "HIGH", "80 units", ACCENT_AMBER),
        ("Casio Scientific Calculator 417", "Kolkata Express #1", "22", "3.9", "5.6 d", "HIGH", "60 units", ACCENT_AMBER),
        ("Titan Analog Stainless Watch Max", "Jaipur Flagship #1", "11", "1.8", "6.1 d", "HIGH", "40 units", ACCENT_AMBER),
        ("Classmate Executive Notebook A5", "Lucknow Supermarket #1", "35", "5.2", "6.7 d", "HIGH", "150 units", ACCENT_AMBER),
    ]

    y_start = 0.61
    for r in table_rows:
        prod, store, stock, ads, days, tier, reorder, color = r
        ax.text(col_x[0], y_start, prod[:30], transform=ax.transAxes, color=TEXT_WHITE, fontsize=8)
        ax.text(col_x[1], y_start, store[:18], transform=ax.transAxes, color=TEXT_MUTED, fontsize=8)
        ax.text(col_x[2], y_start, stock, transform=ax.transAxes, color=TEXT_WHITE, fontsize=8)
        ax.text(col_x[3], y_start, ads, transform=ax.transAxes, color=TEXT_WHITE, fontsize=8)
        ax.text(col_x[4], y_start, days, transform=ax.transAxes, color=color, fontsize=8, fontweight="bold")
        ax.text(col_x[5], y_start, tier, transform=ax.transAxes, color=color, fontsize=8, fontweight="bold")
        ax.text(col_x[6], y_start, reorder, transform=ax.transAxes, color=ACCENT_CYAN, fontsize=8)
        y_start -= 0.055

    # Right side: Days of Inventory by Category & Reorder Pipeline Volume
    rect_r1 = patches.FancyBboxPatch((0.69, 0.38), 0.29, 0.36, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect_r1)
    ax.text(0.71, 0.71, "AVG DAYS OF INVENTORY BY CATEGORY", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10, fontweight="bold")

    sub_ax_doi = fig.add_axes([0.72, 0.42, 0.24, 0.26], facecolor=CARD_BG)
    c_names = ["Beverages", "Grocery", "Electronics", "Personal Care", "Stationery", "Home Appl."]
    c_doi = [9.4, 12.8, 16.5, 21.2, 24.8, 28.1]
    colors = [ACCENT_RED, ACCENT_AMBER, ACCENT_CYAN, ACCENT_TEAL, ACCENT_BLUE, ACCENT_BLUE]
    sub_ax_doi.barh(range(len(c_names)), c_doi, color=colors)
    sub_ax_doi.set_yticks(range(len(c_names)))
    sub_ax_doi.set_yticklabels(c_names, color=TEXT_WHITE, fontsize=8)
    sub_ax_doi.invert_yaxis()
    sub_ax_doi.tick_params(colors=TEXT_WHITE, labelsize=8)
    sub_ax_doi.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    rect_r2 = patches.FancyBboxPatch((0.69, 0.03), 0.29, 0.33, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect_r2)
    ax.text(0.71, 0.33, "INVENTORY TURNOVER BY STORE TYPE", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10, fontweight="bold")

    sub_ax_turn = fig.add_axes([0.72, 0.07, 0.24, 0.23], facecolor=CARD_BG)
    stypes = ["Flagship", "Hypermarket", "Supermarket", "Express"]
    turns = [6.8, 5.9, 4.4, 3.2]
    sub_ax_turn.bar(stypes, turns, color=ACCENT_CYAN, width=0.5)
    sub_ax_turn.set_ylabel("Turnover (x/yr)", color=TEXT_WHITE, fontsize=8)
    sub_ax_turn.tick_params(colors=TEXT_WHITE, labelsize=8)
    sub_ax_turn.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    plt.savefig(os.path.join(OUTPUT_DIR, "02_inventory_intelligence.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print("  -> Saved 02_inventory_intelligence.png")

def create_page_3():
    print("Generating Page 3: Sales Analytics...")
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    draw_header(ax, "Sales Analytics", "Customer Segments, Tender Types & Product Velocity")

    kpis = [
        ("Total Sales Volume", "120,462 Orders", "+14.2% MoM", ACCENT_CYAN),
        ("Average Order Value", "₹1,185.80", "+4.8% vs LY", ACCENT_TEAL),
        ("Top Category", "Electronics", "26.9% Total Share", ACCENT_CYAN),
        ("UPI Penetration", "45.2%", "Leading Payment Mode", ACCENT_BLUE),
        ("Promotional Sales", "24.8%", "Festival Campaign Surge", ACCENT_AMBER),
        ("Gross Margin", "34.02%", "Stable YoY (+0.6%)", ACCENT_TEAL)
    ]
    for i, (lbl, val, sub, col) in enumerate(kpis):
        draw_kpi_card(ax, 0.02 + i * 0.162, 0.77, 0.152, 0.12, lbl, val, sub, col)

    # Chart 1: Payment Method Breakdown (Pie)
    rect1 = patches.FancyBboxPatch((0.02, 0.38), 0.30, 0.36, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect1)
    ax.text(0.04, 0.71, "SALES BY PAYMENT METHOD", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10, fontweight="bold")
    sub_ax1 = fig.add_axes([0.05, 0.41, 0.24, 0.27], facecolor=CARD_BG)
    sub_ax1.pie([45, 25, 15, 10, 5], labels=["UPI", "Credit", "Debit", "Cash", "NetBank"],
                colors=[ACCENT_CYAN, ACCENT_BLUE, ACCENT_TEAL, ACCENT_AMBER, TEXT_MUTED],
                autopct="%1.0f%%", textprops={"color": TEXT_WHITE, "fontsize": 8})

    # Chart 2: Customer Segment Performance (Bar)
    rect2 = patches.FancyBboxPatch((0.34, 0.38), 0.30, 0.36, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect2)
    ax.text(0.36, 0.71, "REVENUE BY CUSTOMER SEGMENT", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10, fontweight="bold")
    sub_ax2 = fig.add_axes([0.37, 0.43, 0.25, 0.24], facecolor=CARD_BG)
    segs = ["Regular", "Walk-in", "Premium", "Corporate"]
    seg_rev = [64.2, 49.8, 21.4, 7.4]
    sub_ax2.bar(segs, seg_rev, color=[ACCENT_CYAN, ACCENT_BLUE, ACCENT_TEAL, ACCENT_AMBER], width=0.5)
    sub_ax2.set_ylabel("INR Millions", color=TEXT_WHITE, fontsize=8)
    sub_ax2.tick_params(colors=TEXT_WHITE, labelsize=8)
    sub_ax2.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    # Chart 3: Regional Sales Distribution (Donut)
    rect3 = patches.FancyBboxPatch((0.66, 0.38), 0.32, 0.36, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect3)
    ax.text(0.68, 0.71, "REGIONAL REVENUE CONTRIBUTION", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10, fontweight="bold")
    sub_ax3 = fig.add_axes([0.70, 0.41, 0.24, 0.27], facecolor=CARD_BG)
    sub_ax3.pie([36.7, 32.3, 20.0, 7.8, 3.2], labels=["West", "South", "North", "East", "Central"],
                colors=[ACCENT_CYAN, ACCENT_BLUE, ACCENT_TEAL, ACCENT_AMBER, "#7209B7"],
                autopct="%1.1f%%", textprops={"color": TEXT_WHITE, "fontsize": 8},
                wedgeprops={"width": 0.5})

    # Bottom Table / Bar: Top 10 Revenue Generating Products
    rect4 = patches.FancyBboxPatch((0.02, 0.03), 0.96, 0.32, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect4)
    ax.text(0.04, 0.32, "TOP 10 BEST SELLING PRODUCTS BY ANNUAL REVENUE", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10, fontweight="bold")
    sub_ax4 = fig.add_axes([0.06, 0.06, 0.90, 0.22], facecolor=CARD_BG)
    prods = [
        "Sony UltraHD TV", "Samsung Air Fryer", "OnePlus Earbuds", "Philips Microwave",
        "Prestige Cooker", "Mamaearth Cream", "Tata Tea Gold", "Decathlon Mat", "Titan Watch", "Classmate A5"
    ]
    p_rev = [8.4, 6.2, 5.8, 4.9, 4.2, 3.8, 3.4, 2.9, 2.7, 2.1]
    sub_ax4.bar(prods, p_rev, color=ACCENT_CYAN, width=0.55)
    sub_ax4.set_ylabel("Revenue (₹M)", color=TEXT_WHITE, fontsize=8)
    sub_ax4.tick_params(colors=TEXT_WHITE, labelsize=8)
    sub_ax4.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    plt.savefig(os.path.join(OUTPUT_DIR, "03_sales_analytics.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print("  -> Saved 03_sales_analytics.png")

def create_page_4():
    print("Generating Page 4: Store Performance...")
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    draw_header(ax, "Store Performance", "Benchmarking 36 Retail Stores Across 9 Indian States")

    kpis = [
        ("Total Operating Stores", "36 Locations", "4 Formats", ACCENT_CYAN),
        ("Average Revenue / Store", "₹3.97M", "Annual Velocity", ACCENT_TEAL),
        ("Average Rev / Sq Ft", "₹182.40", "Retail Density", ACCENT_CYAN),
        ("Top City by Sales", "Mumbai", "6 Stores / ₹28.4M", ACCENT_BLUE),
        ("Fastest Growing", "Bengaluru", "+24.2% YoY", ACCENT_TEAL),
        ("Avg Return Rate", "1.84%", "Well Within <3% Target", ACCENT_AMBER)
    ]
    for i, (lbl, val, sub, col) in enumerate(kpis):
        draw_kpi_card(ax, 0.02 + i * 0.162, 0.77, 0.152, 0.12, lbl, val, sub, col)

    # Left: Store Ranking Bar Chart
    rect1 = patches.FancyBboxPatch((0.02, 0.03), 0.48, 0.71, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect1)
    ax.text(0.04, 0.71, "TOP 12 STORES BY REVENUE & MARGIN EFFICIENCY", transform=ax.transAxes, color=TEXT_WHITE, fontsize=11, fontweight="bold")
    sub_ax1 = fig.add_axes([0.06, 0.07, 0.42, 0.60], facecolor=CARD_BG)
    top_stores = [
        "Mumbai Flagship #1", "Bengaluru Flagship #1", "Delhi Hypermarket #1", "Pune Flagship #1",
        "Hyderabad Flagship #1", "Ahmedabad Hypermarket #1", "Mumbai Hypermarket #2", "Chennai Hypermarket #1",
        "Kolkata Flagship #1", "Jaipur Supermarket #1", "Lucknow Supermarket #1", "Nagpur Express #1"
    ]
    store_sales = [7.8, 7.4, 6.9, 6.2, 5.8, 5.1, 4.9, 4.4, 3.8, 3.2, 2.8, 1.9]
    y_pos = np.arange(len(top_stores))
    sub_ax1.barh(y_pos, store_sales, color=ACCENT_CYAN)
    sub_ax1.set_yticks(y_pos)
    sub_ax1.set_yticklabels(top_stores, color=TEXT_WHITE, fontsize=8)
    sub_ax1.invert_yaxis()
    sub_ax1.set_xlabel("Revenue (INR Millions)", color=TEXT_WHITE, fontsize=8)
    sub_ax1.tick_params(colors=TEXT_WHITE, labelsize=8)
    sub_ax1.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    # Right: Format Distribution and State Scatter / Bubble
    rect2 = patches.FancyBboxPatch((0.52, 0.38), 0.46, 0.36, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect2)
    ax.text(0.54, 0.71, "REVENUE & MARGIN BY STORE FORMAT", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10, fontweight="bold")
    sub_ax2 = fig.add_axes([0.56, 0.43, 0.40, 0.24], facecolor=CARD_BG)
    formats = ["Flagship", "Hypermarket", "Supermarket", "Express"]
    f_rev = [44.2, 51.6, 34.8, 12.2]
    f_margin = [36.2, 34.8, 33.1, 31.4]
    sub_ax2.bar(np.arange(4) - 0.15, f_rev, width=0.3, color=ACCENT_CYAN, label="Revenue (₹M)")
    ax2_twin = sub_ax2.twinx()
    ax2_twin.plot(np.arange(4) + 0.15, f_margin, color=ACCENT_AMBER, marker="o", linewidth=2, label="Gross Margin %")
    sub_ax2.set_xticks(range(4))
    sub_ax2.set_xticklabels(formats, color=TEXT_WHITE, fontsize=8)
    sub_ax2.tick_params(colors=TEXT_WHITE, labelsize=8)
    ax2_twin.tick_params(colors=TEXT_WHITE, labelsize=8)
    sub_ax2.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    rect3 = patches.FancyBboxPatch((0.52, 0.03), 0.46, 0.32, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect3)
    ax.text(0.54, 0.32, "STORE FOOTPRINT & DENSITY MATRIX (SQ FT vs SALES)", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10, fontweight="bold")
    sub_ax3 = fig.add_axes([0.56, 0.07, 0.40, 0.22], facecolor=CARD_BG)
    sqft_vals = [45000, 52000, 38000, 41000, 32000, 28000, 18000, 15000, 8000, 6000]
    rev_vals = [7.8, 7.4, 6.9, 6.2, 5.8, 5.1, 3.8, 3.2, 1.9, 1.4]
    sub_ax3.scatter(sqft_vals, rev_vals, color=ACCENT_TEAL, s=120, edgecolors=TEXT_WHITE, alpha=0.85)
    sub_ax3.set_xlabel("Store Floor Area (Sq Ft)", color=TEXT_WHITE, fontsize=8)
    sub_ax3.set_ylabel("Revenue (₹M)", color=TEXT_WHITE, fontsize=8)
    sub_ax3.tick_params(colors=TEXT_WHITE, labelsize=8)
    sub_ax3.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    plt.savefig(os.path.join(OUTPUT_DIR, "04_store_performance.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print("  -> Saved 04_store_performance.png")

def create_page_5():
    print("Generating Page 5: Product & Supplier Analysis...")
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    draw_header(ax, "Product & Supplier Analysis", "Procurement Fulfillment, Vendor SLAs & Product Defect Rates")

    kpis = [
        ("Cataloged SKUs", "1,200 Products", "9 Core Categories", ACCENT_CYAN),
        ("Active Suppliers", "60 Vendors", "Pan-India Sourcing", ACCENT_BLUE),
        ("Purchase Orders", "10,500 POs", "Total PO Spend ₹38.2M", ACCENT_TEAL),
        ("On-Time Delivery", "88.4%", "Within SLA Commitments", ACCENT_TEAL),
        ("Delayed PO Rate", "7.6%", "Avg Delay: 4.8 Days", ACCENT_AMBER),
        ("Merchandise Return Rate", "1.84%", "5,249 Return Records", ACCENT_RED)
    ]
    for i, (lbl, val, sub, col) in enumerate(kpis):
        draw_kpi_card(ax, 0.02 + i * 0.162, 0.77, 0.152, 0.12, lbl, val, sub, col)

    # Left: Supplier Lead Time vs Delivery Performance
    rect1 = patches.FancyBboxPatch((0.02, 0.03), 0.48, 0.71, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect1)
    ax.text(0.04, 0.71, "TOP 10 SUPPLIERS BY PURCHASE VOLUME & SLA SCORE", transform=ax.transAxes, color=TEXT_WHITE, fontsize=11, fontweight="bold")
    sub_ax1 = fig.add_axes([0.06, 0.07, 0.42, 0.60], facecolor=CARD_BG)
    sups = [
        "Aura Consumer Brands", "Apex Electronics Ltd", "Vanguard Appliances", "Lotus Personal Care",
        "Himalayan Spring Beverages", "Sovereign Kitchenwares", "Velocity Sports Equipment",
        "Indus Valley Staples", "Zenith Audio & Tech", "BlueStar Home Comfort"
    ]
    po_vol = [4.8, 4.2, 3.9, 3.5, 3.1, 2.9, 2.6, 2.4, 2.1, 1.9]
    sub_ax1.barh(range(len(sups)), po_vol, color=ACCENT_BLUE)
    sub_ax1.set_yticks(range(len(sups)))
    sub_ax1.set_yticklabels(sups, color=TEXT_WHITE, fontsize=8)
    sub_ax1.invert_yaxis()
    sub_ax1.set_xlabel("Purchase Order Spend (₹M)", color=TEXT_WHITE, fontsize=8)
    sub_ax1.tick_params(colors=TEXT_WHITE, labelsize=8)
    sub_ax1.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    # Right Top: PO Status Breakdown
    rect2 = patches.FancyBboxPatch((0.52, 0.38), 0.46, 0.36, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect2)
    ax.text(0.54, 0.71, "PURCHASE ORDER FULFILLMENT STATUS", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10, fontweight="bold")
    sub_ax2 = fig.add_axes([0.56, 0.41, 0.38, 0.27], facecolor=CARD_BG)
    sub_ax2.pie([8840, 760, 520, 380], labels=["Completed", "Delayed", "In-Transit", "Cancelled"],
                colors=[ACCENT_TEAL, ACCENT_AMBER, ACCENT_CYAN, ACCENT_RED],
                autopct="%1.1f%%", textprops={"color": TEXT_WHITE, "fontsize": 8})

    # Right Bottom: Customer Return Reasons
    rect3 = patches.FancyBboxPatch((0.52, 0.03), 0.46, 0.32, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect3)
    ax.text(0.54, 0.32, "CUSTOMER RETURN ROOT CAUSE CLASSIFICATION", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10, fontweight="bold")
    sub_ax3 = fig.add_axes([0.56, 0.07, 0.40, 0.22], facecolor=CARD_BG)
    reasons = ["Defective Item", "Wrong Item Delivered", "Size / Fit Issue", "Changed Mind", "Transit Damage"]
    pcts = [35.2, 20.4, 19.8, 14.5, 10.1]
    sub_ax3.bar(reasons, pcts, color=[ACCENT_RED, ACCENT_AMBER, ACCENT_BLUE, TEXT_MUTED, ACCENT_RED], width=0.5)
    sub_ax3.set_ylabel("% of Total Returns", color=TEXT_WHITE, fontsize=8)
    sub_ax3.tick_params(colors=TEXT_WHITE, labelsize=7)
    sub_ax3.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    plt.savefig(os.path.join(OUTPUT_DIR, "05_product_supplier_analysis.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print("  -> Saved 05_product_supplier_analysis.png")

def create_page_6():
    print("Generating Page 6: Data Pipeline Health...")
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    draw_header(ax, "Data Pipeline Health & Governance", "ADF Telemetry, Data Quality Gates & Audit Logging")

    # Top Status Badges
    kpis = [
        ("ADF Master Pipeline", "SUCCESS", "All 11 Pipelines Active", ACCENT_TEAL),
        ("SQL Warehouse Load", "SUCCESS", "Incremental Load 100%", ACCENT_TEAL),
        ("Python Validation", "SUCCESS", "59 Rules Passed / 16 Warn", ACCENT_TEAL),
        ("Data Quality Score", "99.93%", "Enterprise Target >= 98%", ACCENT_CYAN),
        ("Records Ingested", "178,851 Rows", "Across Sales, Inv & PO", ACCENT_BLUE),
        ("Rejected / Cleansed", "1,112 Rows", "1.5% Controlled Anomaly", ACCENT_AMBER)
    ]
    for i, (lbl, val, sub, col) in enumerate(kpis):
        draw_kpi_card(ax, 0.02 + i * 0.162, 0.77, 0.152, 0.12, lbl, val, sub, col)

    # Activity Execution Grid (left side)
    rect1 = patches.FancyBboxPatch((0.02, 0.03), 0.54, 0.71, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect1)
    ax.text(0.04, 0.71, "AZURE DATA FACTORY PIPELINE EXECUTION TELEMETRY", transform=ax.transAxes, color=TEXT_WHITE, fontsize=11, fontweight="bold")
    ax.text(0.04, 0.685, "Live activity logs captured directly from audit.PipelineExecutionLog", transform=ax.transAxes, color=TEXT_MUTED, fontsize=8)

    headers = ["Pipeline Name", "Activity Name", "Duration", "Rows Ingested", "Status"]
    col_x = [0.04, 0.23, 0.38, 0.45, 0.51]
    for h_name, hx in zip(headers, col_x):
        ax.text(hx, 0.65, h_name.upper(), transform=ax.transAxes, color=ACCENT_CYAN, fontsize=8, fontweight="bold")

    adf_logs = [
        ("PL_Master_Retail_Inventory", "Master_Orchestrator_Complete", "12m 45s", "178,851", "SUCCESS", ACCENT_TEAL),
        ("PL_Load_Sales", "Copy_Sales_To_Staging", "4m 12s", "120,462", "SUCCESS", ACCENT_TEAL),
        ("PL_Load_Inventory", "Copy_Inventory_To_Staging", "2m 18s", "42,640", "SUCCESS", ACCENT_TEAL),
        ("PL_Load_Purchases", "Copy_Purchases_To_Staging", "1m 05s", "10,500", "SUCCESS", ACCENT_TEAL),
        ("PL_Load_Returns", "Copy_Returns_To_Staging", "0m 42s", "5,249", "SUCCESS", ACCENT_TEAL),
        ("PL_Load_REST_API", "Copy_REST_Catalog_To_Staging", "0m 35s", "1,200", "SUCCESS", ACCENT_TEAL),
        ("PL_Data_Quality_Check", "Execute_Python_Validation_Engine", "0m 18s", "178,851", "SUCCESS", ACCENT_TEAL),
        ("PL_Transform_Warehouse", "sp_Load_FactSales", "1m 24s", "120,186", "SUCCESS", ACCENT_TEAL),
        ("PL_Transform_Warehouse", "sp_Load_FactInventory", "0m 52s", "42,420", "SUCCESS", ACCENT_TEAL),
        ("PL_Transform_Warehouse", "sp_Update_InventoryMetrics", "0m 38s", "42,420", "SUCCESS", ACCENT_TEAL),
    ]

    y_pos = 0.61
    for row in adf_logs:
        pname, act, dur, rows, status, col = row
        ax.text(col_x[0], y_pos, pname[:22], transform=ax.transAxes, color=TEXT_WHITE, fontsize=8)
        ax.text(col_x[1], y_pos, act[:20], transform=ax.transAxes, color=TEXT_MUTED, fontsize=8)
        ax.text(col_x[2], y_pos, dur, transform=ax.transAxes, color=TEXT_WHITE, fontsize=8)
        ax.text(col_x[3], y_pos, rows, transform=ax.transAxes, color=TEXT_WHITE, fontsize=8)
        ax.text(col_x[4], y_pos, f"● {status}", transform=ax.transAxes, color=col, fontsize=8, fontweight="bold")
        y_pos -= 0.055

    # Right Top: Python Data Quality Rule Compliance
    rect2 = patches.FancyBboxPatch((0.58, 0.38), 0.40, 0.36, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect2)
    ax.text(0.60, 0.71, "DATA QUALITY CHECK TIER PERFORMANCE", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10, fontweight="bold")

    sub_ax2 = fig.add_axes([0.62, 0.43, 0.34, 0.24], facecolor=CARD_BG)
    tiers = ["Tier 1: Schema", "Tier 2: Nulls", "Tier 3: Duplicate Keys", "Tier 4: Business Rules"]
    scores = [100.0, 99.85, 99.85, 99.62]
    sub_ax2.barh(tiers, scores, color=[ACCENT_TEAL, ACCENT_CYAN, ACCENT_CYAN, ACCENT_BLUE])
    sub_ax2.set_xlim(95, 101)
    sub_ax2.set_xlabel("Compliance Rate (%)", color=TEXT_WHITE, fontsize=8)
    sub_ax2.tick_params(colors=TEXT_WHITE, labelsize=8)
    sub_ax2.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    # Right Bottom: Cleansed vs Ingested Record Breakdown
    rect3 = patches.FancyBboxPatch((0.58, 0.03), 0.40, 0.32, boxstyle="round,pad=0.01", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect3)
    ax.text(0.60, 0.32, "CONTROLLED DEFECTS CAUGHT & RECONCILED", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10, fontweight="bold")

    sub_ax3 = fig.add_axes([0.62, 0.07, 0.34, 0.22], facecolor=CARD_BG)
    anom_types = ["Null FKs", "Duplicates", "Negative Qty", "Bad Dates", "Equation Fix"]
    anom_counts = [300, 180, 96, 72, 180]
    sub_ax3.bar(anom_types, anom_counts, color=ACCENT_AMBER, width=0.5)
    sub_ax3.set_ylabel("Defect Rows Cleansed", color=TEXT_WHITE, fontsize=8)
    sub_ax3.tick_params(colors=TEXT_WHITE, labelsize=8)
    sub_ax3.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    plt.savefig(os.path.join(OUTPUT_DIR, "06_data_pipeline_health.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print("  -> Saved 06_data_pipeline_health.png")

def main():
    print("==========================================================================")
    print(" NEXORA INVENTORY INTELLIGENCE — POWER BI MOCKUP GENERATOR")
    print(" Rendering High-Fidelity Screenshots for All 6 Analytics Pages")
    print("==========================================================================")
    create_page_1()
    create_page_2()
    create_page_3()
    create_page_4()
    create_page_5()
    create_page_6()
    print("==========================================================================")
    print(f" All 6 Power BI screenshots generated in {OUTPUT_DIR}")
    print("==========================================================================")

if __name__ == "__main__":
    main()
