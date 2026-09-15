"""
CLARIVENS ENTERPRISE DATA INTELLIGENCE
High-Fidelity Power BI Dashboard Mockup Generator
Author: Senior Data Engineer / Azure Data Architect / Power BI Specialist
Organization: CLARIVENS DATA PLATFORMS

Renders pixel-perfect, dark enterprise dashboard screenshots for all 6 Power BI pages:
1. Executive Overview (CLARIVENS EXECUTIVE INTELLIGENCE)
2. Inventory Intelligence (CLARIVENS INVENTORY INTELLIGENCE)
3. Sales Analytics (CLARIVENS SALES ANALYTICS)
4. Store Performance (CLARIVENS STORE PERFORMANCE)
5. Product & Supplier (CLARIVENS PRODUCT & SUPPLIER INTELLIGENCE)
6. Data Pipeline Health (CLARIVENS DATA PIPELINE OBSERVABILITY)

Theme: Clarivens Black + Orange + Liquid Glassmorphism (16:9 Aspect Ratio)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Clarivens Enterprise Color System
BG_COLOR = "#050505"
NAV_BG = "#0A0A0D"
CARD_BG = "#0E0E12"
CARD_INNER = "#141418"
CARD_BORDER = "#222226"
CARD_BORDER_ORANGE = "rgba(255, 106, 0, 0.4)"

ORANGE = "#FF6A00"
ORANGE_BRIGHT = "#FF7A00"
ORANGE_SOFT = "#FF8A1F"
ORANGE_HIGHLIGHT = "#FFB067"

GRAY_DARK = "#27272A"
GRAY_MID = "#3F3F46"
GRAY_MUTED = "#71717A"
GRAY_LIGHT = "#A1A1AA"
TEXT_WHITE = "#FFFFFF"
TEXT_MUTED = "#8E8E93"

# Semantic Indicators
COLOR_PASS = "#10B981"
COLOR_WARN = "#F59E0B"
COLOR_FAIL = "#EF4444"

def draw_header(ax, title, subtitle):
    # Top navbar
    rect = patches.Rectangle((0, 0.925), 1, 0.075, transform=ax.transAxes, facecolor=NAV_BG, edgecolor=CARD_BORDER, linewidth=1)
    ax.add_patch(rect)
    
    # Minimal Geometric C logo mark
    logo_bg = patches.FancyBboxPatch((0.015, 0.938), 0.018, 0.05, boxstyle="round,pad=0.003,rounding_size=0.005",
                                     transform=ax.transAxes, facecolor="#141418", edgecolor=ORANGE, linewidth=1.2)
    ax.add_patch(logo_bg)
    ax.text(0.024, 0.963, "C", transform=ax.transAxes, color=ORANGE_BRIGHT, fontsize=12, fontweight="heavy", ha="center", va="center")

    # Wordmark & Header
    ax.text(0.038, 0.966, "CLARIVENS", transform=ax.transAxes, color=TEXT_WHITE, fontsize=12, fontweight="heavy", va="center")
    ax.text(0.098, 0.966, "ENTERPRISE DATA INTELLIGENCE", transform=ax.transAxes, color=ORANGE, fontsize=9.5, fontweight="bold", va="center")
    ax.text(0.038, 0.942, f"{title.upper()}  •  {subtitle}", transform=ax.transAxes, color=TEXT_MUTED, fontsize=8, va="center")
    
    # Right telemetry
    ax.text(0.985, 0.962, "DATA AS OF: 2025-12-31  •  REFRESH: AUTOMATED (AZURE DATA FACTORY)", transform=ax.transAxes, color=GRAY_LIGHT, fontsize=8, fontweight="bold", ha="right", va="center")
    ax.text(0.985, 0.942, "ENVIRONMENT: PRODUCTION WAREHOUSE  •  SQL DW (dw schema)", transform=ax.transAxes, color=TEXT_MUTED, fontsize=7.5, ha="right", va="center")

def draw_slicer_bar(ax, slicers):
    """Draws realistic enterprise Power BI slicers/filters"""
    s_y = 0.885
    s_h = 0.032
    s_rect = patches.Rectangle((0, s_y), 1, s_h, transform=ax.transAxes, facecolor="#09090C", edgecolor=CARD_BORDER, linewidth=0.5)
    ax.add_patch(s_rect)
    
    ax.text(0.015, s_y + 0.016, "FILTERS:", transform=ax.transAxes, color=TEXT_MUTED, fontsize=7.5, fontweight="bold", va="center")
    
    curr_x = 0.065
    for label, val, is_active in slicers:
        box_w = 0.125
        bg_col = "#18181C" if is_active else "#101014"
        b_col = ORANGE if is_active else CARD_BORDER
        pill = patches.FancyBboxPatch((curr_x, s_y + 0.004), box_w, s_h - 0.008,
                                      boxstyle="round,pad=0.002,rounding_size=0.004",
                                      transform=ax.transAxes, facecolor=bg_col, edgecolor=b_col, linewidth=0.8)
        ax.add_patch(pill)
        
        ax.text(curr_x + 0.006, s_y + 0.016, label + ":", transform=ax.transAxes, color=TEXT_MUTED, fontsize=7, va="center")
        val_col = ORANGE_BRIGHT if is_active else TEXT_WHITE
        ax.text(curr_x + box_w - 0.012, s_y + 0.016, val, transform=ax.transAxes, color=val_col, fontsize=7.5, fontweight="bold", ha="right", va="center")
        curr_x += box_w + 0.015

def draw_kpi_card(ax, x, y, w, h, label, value, subtext="", status_color=ORANGE):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.008,rounding_size=0.012",
                                  transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER, linewidth=1)
    ax.add_patch(rect)
    
    # Top orange ambient highlight line
    highlight = patches.Rectangle((x + 0.01, y + h - 0.002), w - 0.02, 0.002, transform=ax.transAxes, facecolor=ORANGE, alpha=0.8)
    ax.add_patch(highlight)
    
    ax.text(x + 0.012, y + h - 0.024, label.upper(), transform=ax.transAxes, color=TEXT_MUTED, fontsize=7.5, fontweight="bold")
    ax.text(x + 0.012, y + 0.038, value, transform=ax.transAxes, color=status_color, fontsize=15, fontweight="heavy")
    if subtext:
        ax.text(x + 0.012, y + 0.014, subtext, transform=ax.transAxes, color=GRAY_LIGHT, fontsize=7)

def create_page_1():
    print("Generating Page 1: Clarivens Executive Intelligence...")
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    draw_header(ax, "Clarivens Executive Intelligence", "Enterprise Sales & Inventory High-Level KPIs")
    draw_slicer_bar(ax, [("Fiscal Year", "FY2025", True), ("Region", "All India (36 Stores)", False), ("Channel", "Omni-Channel", False), ("Currency", "INR (₹)", True)])

    # Top KPI row (6 cards)
    kpis = [
        ("Total Sales Revenue", "₹142.8M", "+18.4% YoY Growth", ORANGE_BRIGHT),
        ("Units Sold", "284,520", "+12.1% YoY Volume", TEXT_WHITE),
        ("Gross Profit", "₹48.6M", "34.0% Gross Margin", ORANGE),
        ("Inventory Valuation", "₹64.2M", "42,640 Snapshots", GRAY_LIGHT),
        ("Days of Inventory", "18.4 Days", "Target: 15-20 Days (Healthy)", TEXT_WHITE),
        ("Stockout Risk Alerts", "148 SKUs", "Critical: 42 | High: 106", COLOR_WARN)
    ]
    for i, (lbl, val, sub, col) in enumerate(kpis):
        draw_kpi_card(ax, 0.018 + i * 0.163, 0.74, 0.153, 0.125, lbl, val, sub, col)

    # Chart 1: Monthly Revenue & Gross Profit Trend (left half)
    rect1 = patches.FancyBboxPatch((0.018, 0.37), 0.58, 0.35, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect1)
    ax.text(0.035, 0.69, "2025 MONTHLY REVENUE & PROFIT TRAJECTORY (INR MILLIONS)", transform=ax.transAxes, color=TEXT_WHITE, fontsize=9.5, fontweight="bold")
    ax.text(0.035, 0.67, "Primary: Clarivens Revenue (Orange) | Secondary: Gross Profit (Neutral Surface)", transform=ax.transAxes, color=TEXT_MUTED, fontsize=7.5)

    sub_ax1 = fig.add_axes([0.05, 0.40, 0.53, 0.25], facecolor=CARD_BG)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    rev = [9.8, 10.2, 10.8, 12.4, 11.2, 12.9, 10.5, 11.1, 13.2, 14.8, 16.2, 12.1]
    profit = [3.3, 3.5, 3.7, 4.2, 3.8, 4.4, 3.6, 3.8, 4.5, 5.0, 5.5, 4.1]
    
    sub_ax1.bar(np.arange(12) - 0.18, rev, width=0.36, color=ORANGE, label="Revenue")
    sub_ax1.bar(np.arange(12) + 0.18, profit, width=0.36, color=GRAY_MID, edgecolor=CARD_BORDER, label="Gross Profit")
    sub_ax1.set_xticks(range(12))
    sub_ax1.set_xticklabels(months, color=TEXT_MUTED, fontsize=8)
    sub_ax1.tick_params(colors=TEXT_MUTED, labelsize=8)
    sub_ax1.legend(facecolor=CARD_INNER, edgecolor=CARD_BORDER, labelcolor=TEXT_WHITE, fontsize=8)
    sub_ax1.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    # Chart 2: Revenue by Category (right half)
    rect2 = patches.FancyBboxPatch((0.615, 0.37), 0.365, 0.35, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect2)
    ax.text(0.63, 0.69, "REVENUE CONTRIBUTION BY MERCHANDISE CATEGORY", transform=ax.transAxes, color=TEXT_WHITE, fontsize=9.5, fontweight="bold")
    ax.text(0.63, 0.67, "Categorical rank sorted by total sales volume", transform=ax.transAxes, color=TEXT_MUTED, fontsize=7.5)

    sub_ax2 = fig.add_axes([0.64, 0.40, 0.32, 0.25], facecolor=CARD_BG)
    cats = ["Electronics", "Home Appl.", "Personal Care", "Grocery", "Beverages", "Home/Kitchen", "Sports"]
    cat_rev = [38.4, 26.2, 18.5, 19.8, 14.2, 15.1, 10.6]
    cat_colors = [ORANGE_BRIGHT, ORANGE, ORANGE_SOFT, GRAY_LIGHT, GRAY_MUTED, GRAY_MID, GRAY_DARK]
    y_pos = np.arange(len(cats))
    sub_ax2.barh(y_pos, cat_rev, color=cat_colors)
    sub_ax2.set_yticks(y_pos)
    sub_ax2.set_yticklabels(cats, color=TEXT_WHITE, fontsize=8)
    sub_ax2.invert_yaxis()
    sub_ax2.tick_params(colors=TEXT_MUTED, labelsize=8)
    sub_ax2.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    # Bottom Row: Regional Store Performance & Inventory Stockout Status
    rect3 = patches.FancyBboxPatch((0.018, 0.03), 0.47, 0.32, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect3)
    ax.text(0.035, 0.32, "TOP 5 REGIONAL STORE CLUSTERS (INR MILLIONS)", transform=ax.transAxes, color=TEXT_WHITE, fontsize=9.5, fontweight="bold")

    sub_ax3 = fig.add_axes([0.05, 0.06, 0.41, 0.23], facecolor=CARD_BG)
    regions = ["West (Mumbai/Pune)", "South (Bengaluru/Hyd)", "North (Delhi/Jaipur)", "East (Kolkata)", "Central (Nagpur)"]
    reg_sales = [52.4, 46.1, 28.5, 11.2, 4.6]
    reg_colors = [ORANGE_BRIGHT, ORANGE, GRAY_LIGHT, GRAY_MUTED, GRAY_MID]
    sub_ax3.barh(range(len(regions)), reg_sales, color=reg_colors)
    sub_ax3.set_yticks(range(len(regions)))
    sub_ax3.set_yticklabels(regions, color=TEXT_WHITE, fontsize=8)
    sub_ax3.invert_yaxis()
    sub_ax3.tick_params(colors=TEXT_MUTED, labelsize=8)
    sub_ax3.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    rect4 = patches.FancyBboxPatch((0.505, 0.03), 0.475, 0.32, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect4)
    ax.text(0.525, 0.32, "INVENTORY STOCKOUT RISK LEVEL DISTRIBUTION", transform=ax.transAxes, color=TEXT_WHITE, fontsize=9.5, fontweight="bold")

    sub_ax4 = fig.add_axes([0.55, 0.05, 0.38, 0.24], facecolor=CARD_BG)
    risk_labels = ["Low Risk (>14d)", "Medium (8-14d)", "High Risk (4-7d)", "Critical (<=3d)"]
    risk_counts = [28450, 9420, 3120, 1650]
    risk_colors = [GRAY_DARK, GRAY_MID, COLOR_WARN, ORANGE]
    sub_ax4.pie(risk_counts, labels=risk_labels, colors=risk_colors, autopct="%1.1f%%",
                textprops={"color": TEXT_WHITE, "fontsize": 8}, startangle=140,
                wedgeprops={"edgecolor": CARD_BORDER, "linewidth": 1})

    plt.savefig(os.path.join(OUTPUT_DIR, "01_executive_overview.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print("  -> Saved 01_executive_overview.png")

def create_page_2():
    print("Generating Page 2: Clarivens Inventory Intelligence...")
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    draw_header(ax, "Clarivens Inventory Intelligence", "Stockout Risk, Replenishment Velocity & Reorder Alerts")
    draw_slicer_bar(ax, [("Risk Tier", "All Tiers", False), ("Category", "Electronics & FMCG", True), ("Store Format", "Flagship & Hyper", True), ("Replenishment", "Alerts Active", True)])

    kpis = [
        ("Current On-Hand", "412,800 Units", "Across 36 Active Stores", TEXT_WHITE),
        ("Inventory Valuation", "₹64.25M", "Valued at Standard UnitCost", ORANGE_BRIGHT),
        ("Days of Inventory", "18.4 Days", "Demand Coverage Ratio", ORANGE),
        ("Critical Stock (<=3d)", "42 Items", "Immediate Stockout Risk", COLOR_FAIL),
        ("High Risk (4-7d)", "106 Items", "Expedite Reorder Workflow", COLOR_WARN),
        ("Reorder Required", "248 Alerts", "Stock <= Safety Threshold", ORANGE_SOFT)
    ]
    for i, (lbl, val, sub, col) in enumerate(kpis):
        draw_kpi_card(ax, 0.018 + i * 0.163, 0.74, 0.153, 0.125, lbl, val, sub, col)

    # Main Grid: Inventory Risk Action Table
    rect_table = patches.FancyBboxPatch((0.018, 0.03), 0.65, 0.69, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect_table)
    ax.text(0.035, 0.695, "CRITICAL & HIGH STOCKOUT RISK ACTION MATRIX", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10.5, fontweight="bold")
    ax.text(0.035, 0.675, "Active product/store combinations requiring immediate procurement intervention", transform=ax.transAxes, color=TEXT_MUTED, fontsize=8)

    headers = ["Product Name", "Store Location", "Stock", "ADS", "Days Left", "Risk Tier", "Reorder Qty"]
    col_x = [0.035, 0.28, 0.40, 0.46, 0.51, 0.57, 0.62]
    for h_name, hx in zip(headers, col_x):
        ax.text(hx, 0.64, h_name.upper(), transform=ax.transAxes, color=ORANGE, fontsize=8, fontweight="bold")

    table_rows = [
        ("Sony UltraHD Smart LED TV Pro 420", "Bengaluru Flagship #1", "4", "2.8", "1.4 d", "CRITICAL", "50 units", COLOR_FAIL),
        ("boAt Wireless Headphones Elite 88", "Mumbai Supermarket #3", "6", "3.4", "1.8 d", "CRITICAL", "120 units", COLOR_FAIL),
        ("Real Cold Pressed Juice Mango 1L", "Pune Express #2", "12", "5.1", "2.4 d", "CRITICAL", "180 units", COLOR_FAIL),
        ("Mamaearth Face Moisturizer 100ml", "Delhi Hypermarket #1", "18", "6.2", "2.9 d", "CRITICAL", "100 units", COLOR_FAIL),
        ("Tata Sampann Toor Dal 1kg", "Ahmedabad Flagship #1", "25", "5.8", "4.3 d", "HIGH", "250 units", COLOR_WARN),
        ("Prestige Induction Cooktop 2000W", "Hyderabad Supermarket #2", "14", "2.9", "4.8 d", "HIGH", "75 units", COLOR_WARN),
        ("Decathlon Yoga Mat High Density", "Chennai Hypermarket #1", "16", "3.1", "5.2 d", "HIGH", "80 units", COLOR_WARN),
        ("Casio Scientific Calculator 417", "Kolkata Express #1", "22", "3.9", "5.6 d", "HIGH", "60 units", COLOR_WARN),
        ("Titan Analog Stainless Watch Max", "Jaipur Flagship #1", "11", "1.8", "6.1 d", "HIGH", "40 units", COLOR_WARN),
        ("Classmate Executive Notebook A5", "Lucknow Supermarket #1", "35", "5.2", "6.7 d", "HIGH", "150 units", COLOR_WARN),
    ]

    y_start = 0.60
    for r in table_rows:
        prod, store, stock, ads, days, tier, reorder, color = r
        ax.text(col_x[0], y_start, prod[:32], transform=ax.transAxes, color=TEXT_WHITE, fontsize=8)
        ax.text(col_x[1], y_start, store[:18], transform=ax.transAxes, color=GRAY_LIGHT, fontsize=8)
        ax.text(col_x[2], y_start, stock, transform=ax.transAxes, color=TEXT_WHITE, fontsize=8)
        ax.text(col_x[3], y_start, ads, transform=ax.transAxes, color=GRAY_LIGHT, fontsize=8)
        ax.text(col_x[4], y_start, days, transform=ax.transAxes, color=color, fontsize=8, fontweight="bold")
        ax.text(col_x[5], y_start, tier, transform=ax.transAxes, color=color, fontsize=8, fontweight="bold")
        ax.text(col_x[6], y_start, reorder, transform=ax.transAxes, color=ORANGE_BRIGHT, fontsize=8)
        y_start -= 0.054

    # Right side: Days of Inventory by Category & Turnover
    rect_r1 = patches.FancyBboxPatch((0.685, 0.37), 0.295, 0.35, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect_r1)
    ax.text(0.70, 0.695, "AVG DAYS OF INVENTORY BY CATEGORY", transform=ax.transAxes, color=TEXT_WHITE, fontsize=9.5, fontweight="bold")

    sub_ax_doi = fig.add_axes([0.72, 0.40, 0.24, 0.26], facecolor=CARD_BG)
    c_names = ["Beverages", "Grocery", "Electronics", "Personal Care", "Stationery", "Home Appl."]
    c_doi = [9.4, 12.8, 16.5, 21.2, 24.8, 28.1]
    c_colors = [COLOR_FAIL, COLOR_WARN, ORANGE_BRIGHT, ORANGE, GRAY_MUTED, GRAY_DARK]
    sub_ax_doi.barh(range(len(c_names)), c_doi, color=c_colors)
    sub_ax_doi.set_yticks(range(len(c_names)))
    sub_ax_doi.set_yticklabels(c_names, color=TEXT_WHITE, fontsize=8)
    sub_ax_doi.invert_yaxis()
    sub_ax_doi.tick_params(colors=TEXT_MUTED, labelsize=8)
    sub_ax_doi.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    rect_r2 = patches.FancyBboxPatch((0.685, 0.03), 0.295, 0.32, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect_r2)
    ax.text(0.70, 0.32, "INVENTORY TURNOVER BY STORE FORMAT", transform=ax.transAxes, color=TEXT_WHITE, fontsize=9.5, fontweight="bold")

    sub_ax_turn = fig.add_axes([0.72, 0.06, 0.24, 0.23], facecolor=CARD_BG)
    stypes = ["Flagship", "Hypermarket", "Supermarket", "Express"]
    turns = [6.8, 5.9, 4.4, 3.2]
    sub_ax_turn.bar(stypes, turns, color=ORANGE, width=0.45)
    sub_ax_turn.set_ylabel("Turnover (x/yr)", color=TEXT_MUTED, fontsize=8)
    sub_ax_turn.tick_params(colors=TEXT_MUTED, labelsize=8)
    sub_ax_turn.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    plt.savefig(os.path.join(OUTPUT_DIR, "02_inventory_intelligence.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print("  -> Saved 02_inventory_intelligence.png")

def create_page_3():
    print("Generating Page 3: Clarivens Sales Analytics...")
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    draw_header(ax, "Clarivens Sales Analytics", "Customer Segments, Tender Types & Product Velocity")
    draw_slicer_bar(ax, [("Tender Type", "All Modes", False), ("Customer Segment", "All Segments", False), ("Promotion", "Active Campaigns", True), ("Sales Channel", "Store POS", True)])

    kpis = [
        ("Total Sales Volume", "120,462 Orders", "+14.2% MoM Surge", ORANGE_BRIGHT),
        ("Average Order Value", "₹1,185.80", "+4.8% vs Prior Year", TEXT_WHITE),
        ("Top Category", "Electronics", "26.9% Total Revenue Share", ORANGE),
        ("UPI Penetration", "45.2%", "Leading Digital Payment", ORANGE_SOFT),
        ("Promotional Sales", "24.8%", "Festival Campaign Surge", GRAY_LIGHT),
        ("Gross Margin", "34.02%", "34.0% Target Achieved", TEXT_WHITE)
    ]
    for i, (lbl, val, sub, col) in enumerate(kpis):
        draw_kpi_card(ax, 0.018 + i * 0.163, 0.74, 0.153, 0.125, lbl, val, sub, col)

    # Chart 1: Payment Method Breakdown (Donut)
    rect1 = patches.FancyBboxPatch((0.018, 0.37), 0.30, 0.35, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect1)
    ax.text(0.035, 0.695, "SALES BY PAYMENT METHOD", transform=ax.transAxes, color=TEXT_WHITE, fontsize=9.5, fontweight="bold")
    sub_ax1 = fig.add_axes([0.04, 0.40, 0.25, 0.26], facecolor=CARD_BG)
    sub_ax1.pie([45, 25, 15, 10, 5], labels=["UPI", "Credit", "Debit", "Cash", "NetBank"],
                colors=[ORANGE_BRIGHT, ORANGE, GRAY_LIGHT, GRAY_MUTED, GRAY_DARK],
                autopct="%1.0f%%", textprops={"color": TEXT_WHITE, "fontsize": 8},
                wedgeprops={"edgecolor": CARD_BORDER, "linewidth": 1})

    # Chart 2: Customer Segment Performance (Bar)
    rect2 = patches.FancyBboxPatch((0.335, 0.37), 0.31, 0.35, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect2)
    ax.text(0.35, 0.695, "REVENUE BY CUSTOMER SEGMENT", transform=ax.transAxes, color=TEXT_WHITE, fontsize=9.5, fontweight="bold")
    sub_ax2 = fig.add_axes([0.36, 0.41, 0.26, 0.24], facecolor=CARD_BG)
    segs = ["Regular", "Walk-in", "Premium", "Corporate"]
    seg_rev = [64.2, 49.8, 21.4, 7.4]
    sub_ax2.bar(segs, seg_rev, color=[ORANGE_BRIGHT, ORANGE, GRAY_LIGHT, GRAY_DARK], width=0.45)
    sub_ax2.set_ylabel("INR Millions", color=TEXT_MUTED, fontsize=8)
    sub_ax2.tick_params(colors=TEXT_MUTED, labelsize=8)
    sub_ax2.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    # Chart 3: Regional Sales Distribution (Donut)
    rect3 = patches.FancyBboxPatch((0.662, 0.37), 0.32, 0.35, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect3)
    ax.text(0.68, 0.695, "REGIONAL REVENUE CONTRIBUTION", transform=ax.transAxes, color=TEXT_WHITE, fontsize=9.5, fontweight="bold")
    sub_ax3 = fig.add_axes([0.70, 0.40, 0.24, 0.26], facecolor=CARD_BG)
    sub_ax3.pie([36.7, 32.3, 20.0, 7.8, 3.2], labels=["West", "South", "North", "East", "Central"],
                colors=[ORANGE_BRIGHT, ORANGE, ORANGE_HIGHLIGHT, GRAY_MUTED, GRAY_DARK],
                autopct="%1.1f%%", textprops={"color": TEXT_WHITE, "fontsize": 8},
                wedgeprops={"width": 0.5, "edgecolor": CARD_BORDER, "linewidth": 1})

    # Bottom Table / Bar: Top 10 Revenue Generating Products
    rect4 = patches.FancyBboxPatch((0.018, 0.03), 0.964, 0.32, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect4)
    ax.text(0.035, 0.32, "TOP 10 BEST SELLING PRODUCTS BY ANNUAL REVENUE (INR MILLIONS)", transform=ax.transAxes, color=TEXT_WHITE, fontsize=9.5, fontweight="bold")
    sub_ax4 = fig.add_axes([0.05, 0.06, 0.91, 0.22], facecolor=CARD_BG)
    prods = [
        "Sony UltraHD TV", "Samsung Air Fryer", "OnePlus Earbuds", "Philips Microwave",
        "Prestige Cooker", "Mamaearth Cream", "Tata Tea Gold", "Decathlon Mat", "Titan Watch", "Classmate A5"
    ]
    p_rev = [8.4, 6.2, 5.8, 4.9, 4.2, 3.8, 3.4, 2.9, 2.7, 2.1]
    p_cols = [ORANGE_BRIGHT, ORANGE, ORANGE, ORANGE_SOFT, GRAY_LIGHT, GRAY_LIGHT, GRAY_MUTED, GRAY_MUTED, GRAY_DARK, GRAY_DARK]
    sub_ax4.bar(prods, p_rev, color=p_cols, width=0.5)
    sub_ax4.set_ylabel("Revenue (₹M)", color=TEXT_MUTED, fontsize=8)
    sub_ax4.tick_params(colors=TEXT_MUTED, labelsize=8)
    sub_ax4.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    plt.savefig(os.path.join(OUTPUT_DIR, "03_sales_analytics.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print("  -> Saved 03_sales_analytics.png")

def create_page_4():
    print("Generating Page 4: Clarivens Store Performance...")
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    draw_header(ax, "Clarivens Store Performance", "Benchmarking 36 Retail Stores Across 9 Indian States")
    draw_slicer_bar(ax, [("Store Cluster", "All 36 Stores", False), ("Tier City", "Tier 1 & Metro", True), ("Format", "All Formats", False), ("Metric Focus", "Revenue & Margin", True)])

    kpis = [
        ("Total Operating Stores", "36 Locations", "4 Operating Formats", TEXT_WHITE),
        ("Average Revenue / Store", "₹3.97M", "Annual Sales Velocity", ORANGE_BRIGHT),
        ("Average Rev / Sq Ft", "₹182.40", "Retail Floor Density", ORANGE),
        ("Top City by Sales", "Mumbai", "6 Stores / ₹28.4M Total", ORANGE_SOFT),
        ("Fastest Growing", "Bengaluru", "+24.2% YoY Growth", COLOR_PASS),
        ("Avg Return Rate", "1.84%", "Under 3.0% Enterprise Limit", COLOR_WARN)
    ]
    for i, (lbl, val, sub, col) in enumerate(kpis):
        draw_kpi_card(ax, 0.018 + i * 0.163, 0.74, 0.153, 0.125, lbl, val, sub, col)

    # Left: Store Ranking Bar Chart
    rect1 = patches.FancyBboxPatch((0.018, 0.03), 0.48, 0.69, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect1)
    ax.text(0.035, 0.695, "TOP 12 STORES BY REVENUE & MARGIN EFFICIENCY", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10.5, fontweight="bold")
    sub_ax1 = fig.add_axes([0.05, 0.07, 0.42, 0.58], facecolor=CARD_BG)
    top_stores = [
        "Mumbai Flagship #1", "Bengaluru Flagship #1", "Delhi Hypermarket #1", "Pune Flagship #1",
        "Hyderabad Flagship #1", "Ahmedabad Hypermarket #1", "Mumbai Hypermarket #2", "Chennai Hypermarket #1",
        "Kolkata Flagship #1", "Jaipur Supermarket #1", "Lucknow Supermarket #1", "Nagpur Express #1"
    ]
    store_sales = [7.8, 7.4, 6.9, 6.2, 5.8, 5.1, 4.9, 4.4, 3.8, 3.2, 2.8, 1.9]
    store_cols = [ORANGE_BRIGHT, ORANGE, ORANGE, ORANGE_SOFT, GRAY_LIGHT, GRAY_LIGHT, GRAY_MUTED, GRAY_MUTED, GRAY_MID, GRAY_MID, GRAY_DARK, GRAY_DARK]
    y_pos = np.arange(len(top_stores))
    sub_ax1.barh(y_pos, store_sales, color=store_cols)
    sub_ax1.set_yticks(y_pos)
    sub_ax1.set_yticklabels(top_stores, color=TEXT_WHITE, fontsize=8)
    sub_ax1.invert_yaxis()
    sub_ax1.set_xlabel("Revenue (INR Millions)", color=TEXT_MUTED, fontsize=8)
    sub_ax1.tick_params(colors=TEXT_MUTED, labelsize=8)
    sub_ax1.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    # Right: Format Distribution and State Scatter
    rect2 = patches.FancyBboxPatch((0.515, 0.37), 0.467, 0.35, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect2)
    ax.text(0.53, 0.695, "REVENUE & MARGIN BY STORE FORMAT", transform=ax.transAxes, color=TEXT_WHITE, fontsize=9.5, fontweight="bold")
    sub_ax2 = fig.add_axes([0.55, 0.41, 0.41, 0.24], facecolor=CARD_BG)
    formats = ["Flagship", "Hypermarket", "Supermarket", "Express"]
    f_rev = [44.2, 51.6, 34.8, 12.2]
    f_margin = [36.2, 34.8, 33.1, 31.4]
    sub_ax2.bar(np.arange(4) - 0.15, f_rev, width=0.3, color=ORANGE, label="Revenue (₹M)")
    ax2_twin = sub_ax2.twinx()
    ax2_twin.plot(np.arange(4) + 0.15, f_margin, color=ORANGE_HIGHLIGHT, marker="o", linewidth=2, label="Gross Margin %")
    sub_ax2.set_xticks(range(4))
    sub_ax2.set_xticklabels(formats, color=TEXT_WHITE, fontsize=8)
    sub_ax2.tick_params(colors=TEXT_MUTED, labelsize=8)
    ax2_twin.tick_params(colors=TEXT_MUTED, labelsize=8)
    sub_ax2.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    rect3 = patches.FancyBboxPatch((0.515, 0.03), 0.467, 0.32, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect3)
    ax.text(0.53, 0.32, "STORE FOOTPRINT & DENSITY MATRIX (SQ FT vs SALES)", transform=ax.transAxes, color=TEXT_WHITE, fontsize=9.5, fontweight="bold")
    sub_ax3 = fig.add_axes([0.55, 0.06, 0.41, 0.22], facecolor=CARD_BG)
    sqft_vals = [45000, 52000, 38000, 41000, 32000, 28000, 18000, 15000, 8000, 6000]
    rev_vals = [7.8, 7.4, 6.9, 6.2, 5.8, 5.1, 3.8, 3.2, 1.9, 1.4]
    sub_ax3.scatter(sqft_vals, rev_vals, color=ORANGE, s=110, edgecolors=TEXT_WHITE, linewidth=1, alpha=0.9)
    sub_ax3.set_xlabel("Store Floor Area (Sq Ft)", color=TEXT_MUTED, fontsize=8)
    sub_ax3.set_ylabel("Revenue (₹M)", color=TEXT_MUTED, fontsize=8)
    sub_ax3.tick_params(colors=TEXT_MUTED, labelsize=8)
    sub_ax3.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    plt.savefig(os.path.join(OUTPUT_DIR, "04_store_performance.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print("  -> Saved 04_store_performance.png")

def create_page_5():
    print("Generating Page 5: Clarivens Product & Supplier Intelligence...")
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    draw_header(ax, "Clarivens Product & Supplier Intelligence", "Procurement Fulfillment, Vendor SLAs & Product Defect Rates")
    draw_slicer_bar(ax, [("Vendor Rating", "All Ratings", False), ("SLA Tier", "Standard & Fast-Track", True), ("PO Status", "All Purchase Orders", False), ("Lead Time", "Pan-India", False)])

    kpis = [
        ("Cataloged SKUs", "1,200 Products", "9 Core Retail Categories", TEXT_WHITE),
        ("Active Suppliers", "60 Vendors", "Pan-India Sourcing Network", ORANGE_SOFT),
        ("Purchase Orders", "10,500 POs", "Total Spend: ₹38.2M", ORANGE_BRIGHT),
        ("On-Time Delivery", "88.4%", "Within Contracted SLA", COLOR_PASS),
        ("Delayed PO Rate", "7.6%", "Avg Delay: 4.8 Days", COLOR_WARN),
        ("Merchandise Return Rate", "1.84%", "5,249 Defect Records", COLOR_FAIL)
    ]
    for i, (lbl, val, sub, col) in enumerate(kpis):
        draw_kpi_card(ax, 0.018 + i * 0.163, 0.74, 0.153, 0.125, lbl, val, sub, col)

    # Left: Supplier Lead Time vs Delivery Performance
    rect1 = patches.FancyBboxPatch((0.018, 0.03), 0.48, 0.69, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect1)
    ax.text(0.035, 0.695, "TOP 10 SUPPLIERS BY PURCHASE VOLUME & SLA SCORE", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10.5, fontweight="bold")
    sub_ax1 = fig.add_axes([0.05, 0.07, 0.42, 0.58], facecolor=CARD_BG)
    sups = [
        "Aura Consumer Brands", "Apex Electronics Ltd", "Vanguard Appliances", "Lotus Personal Care",
        "Himalayan Spring Beverages", "Sovereign Kitchenwares", "Velocity Sports Equipment",
        "Indus Valley Staples", "Zenith Audio & Tech", "BlueStar Home Comfort"
    ]
    po_vol = [4.8, 4.2, 3.9, 3.5, 3.1, 2.9, 2.6, 2.4, 2.1, 1.9]
    sup_cols = [ORANGE_BRIGHT, ORANGE, ORANGE, ORANGE_SOFT, GRAY_LIGHT, GRAY_LIGHT, GRAY_MUTED, GRAY_MUTED, GRAY_MID, GRAY_DARK]
    sub_ax1.barh(range(len(sups)), po_vol, color=sup_cols)
    sub_ax1.set_yticks(range(len(sups)))
    sub_ax1.set_yticklabels(sups, color=TEXT_WHITE, fontsize=8)
    sub_ax1.invert_yaxis()
    sub_ax1.set_xlabel("Purchase Order Spend (₹M)", color=TEXT_MUTED, fontsize=8)
    sub_ax1.tick_params(colors=TEXT_MUTED, labelsize=8)
    sub_ax1.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    # Right Top: PO Status Breakdown
    rect2 = patches.FancyBboxPatch((0.515, 0.37), 0.467, 0.35, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect2)
    ax.text(0.53, 0.695, "PURCHASE ORDER FULFILLMENT STATUS", transform=ax.transAxes, color=TEXT_WHITE, fontsize=9.5, fontweight="bold")
    sub_ax2 = fig.add_axes([0.56, 0.40, 0.38, 0.26], facecolor=CARD_BG)
    sub_ax2.pie([8840, 760, 520, 380], labels=["Completed", "Delayed", "In-Transit", "Cancelled"],
                colors=[COLOR_PASS, COLOR_WARN, ORANGE, COLOR_FAIL],
                autopct="%1.1f%%", textprops={"color": TEXT_WHITE, "fontsize": 8},
                wedgeprops={"edgecolor": CARD_BORDER, "linewidth": 1})

    # Right Bottom: Customer Return Reasons
    rect3 = patches.FancyBboxPatch((0.515, 0.03), 0.467, 0.32, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect3)
    ax.text(0.53, 0.32, "CUSTOMER RETURN ROOT CAUSE CLASSIFICATION", transform=ax.transAxes, color=TEXT_WHITE, fontsize=9.5, fontweight="bold")
    sub_ax3 = fig.add_axes([0.55, 0.06, 0.41, 0.22], facecolor=CARD_BG)
    reasons = ["Defective Item", "Wrong Item Delivered", "Size / Fit Issue", "Changed Mind", "Transit Damage"]
    pcts = [35.2, 20.4, 19.8, 14.5, 10.1]
    sub_ax3.bar(reasons, pcts, color=[COLOR_FAIL, COLOR_WARN, ORANGE, GRAY_MUTED, GRAY_DARK], width=0.45)
    sub_ax3.set_ylabel("% of Total Returns", color=TEXT_MUTED, fontsize=8)
    sub_ax3.tick_params(colors=TEXT_MUTED, labelsize=7.5)
    sub_ax3.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    plt.savefig(os.path.join(OUTPUT_DIR, "05_product_supplier_analysis.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print("  -> Saved 05_product_supplier_analysis.png")

def create_page_6():
    print("Generating Page 6: Clarivens Data Pipeline Observability...")
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    draw_header(ax, "Clarivens Data Pipeline Observability", "ADF Telemetry, Data Quality Gates & Audit Logging")
    draw_slicer_bar(ax, [("Pipeline Scope", "All 11 Pipelines", False), ("Run Environment", "Production", True), ("Quality Tier", "Tiers 1 to 4", True), ("Status Filter", "Success & Warnings", True)])

    # Top Status Badges
    kpis = [
        ("ADF Master Pipeline", "SUCCESS", "All 11 Pipelines Active", COLOR_PASS),
        ("SQL Warehouse Load", "SUCCESS", "Incremental Load 100%", COLOR_PASS),
        ("Python Validation", "SUCCESS", "59 Passed / 16 Warnings", COLOR_PASS),
        ("Data Quality Score", "99.93%", "Enterprise Gate >= 98.0%", ORANGE_BRIGHT),
        ("Records Ingested", "178,851 Rows", "Sales, Inventory & POs", TEXT_WHITE),
        ("Controlled Anomalies", "1,112 Rows", "Caught & Cleansed", COLOR_WARN)
    ]
    for i, (lbl, val, sub, col) in enumerate(kpis):
        draw_kpi_card(ax, 0.018 + i * 0.163, 0.74, 0.153, 0.125, lbl, val, sub, col)

    # Activity Execution Grid (left side)
    rect1 = patches.FancyBboxPatch((0.018, 0.03), 0.54, 0.69, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect1)
    ax.text(0.035, 0.695, "AZURE DATA FACTORY PIPELINE EXECUTION TELEMETRY", transform=ax.transAxes, color=TEXT_WHITE, fontsize=10.5, fontweight="bold")
    ax.text(0.035, 0.675, "Activity execution telemetry captured live from audit.PipelineExecutionLog", transform=ax.transAxes, color=TEXT_MUTED, fontsize=8)

    headers = ["Pipeline Name", "Activity Name", "Duration", "Rows Ingested", "Status"]
    col_x = [0.035, 0.22, 0.37, 0.44, 0.50]
    for h_name, hx in zip(headers, col_x):
        ax.text(hx, 0.64, h_name.upper(), transform=ax.transAxes, color=ORANGE, fontsize=8, fontweight="bold")

    adf_logs = [
        ("PL_Master_Retail_Inventory", "Master_Orchestrator_Complete", "12m 45s", "178,851", "SUCCESS", COLOR_PASS),
        ("PL_Load_Sales", "Copy_Sales_To_Staging", "4m 12s", "120,462", "SUCCESS", COLOR_PASS),
        ("PL_Load_Inventory", "Copy_Inventory_To_Staging", "2m 18s", "42,640", "SUCCESS", COLOR_PASS),
        ("PL_Load_Purchases", "Copy_Purchases_To_Staging", "1m 05s", "10,500", "SUCCESS", COLOR_PASS),
        ("PL_Load_Returns", "Copy_Returns_To_Staging", "0m 42s", "5,249", "SUCCESS", COLOR_PASS),
        ("PL_Load_REST_API", "Copy_REST_Catalog_To_Staging", "0m 35s", "1,200", "SUCCESS", COLOR_PASS),
        ("PL_Data_Quality_Check", "Execute_Python_Validation_Engine", "0m 18s", "178,851", "SUCCESS", COLOR_PASS),
        ("PL_Transform_Warehouse", "sp_Load_FactSales", "1m 24s", "120,186", "SUCCESS", COLOR_PASS),
        ("PL_Transform_Warehouse", "sp_Load_FactInventory", "0m 52s", "42,420", "SUCCESS", COLOR_PASS),
        ("PL_Transform_Warehouse", "sp_Update_InventoryMetrics", "0m 38s", "42,420", "SUCCESS", COLOR_PASS),
    ]

    y_pos = 0.60
    for row in adf_logs:
        pname, act, dur, rows, status, col = row
        ax.text(col_x[0], y_pos, pname[:22], transform=ax.transAxes, color=TEXT_WHITE, fontsize=8)
        ax.text(col_x[1], y_pos, act[:19], transform=ax.transAxes, color=GRAY_LIGHT, fontsize=8)
        ax.text(col_x[2], y_pos, dur, transform=ax.transAxes, color=GRAY_MUTED, fontsize=8)
        ax.text(col_x[3], y_pos, rows, transform=ax.transAxes, color=TEXT_WHITE, fontsize=8)
        ax.text(col_x[4], y_pos, f"● {status}", transform=ax.transAxes, color=col, fontsize=8, fontweight="bold")
        y_pos -= 0.054

    # Right Top: Python Data Quality Rule Compliance
    rect2 = patches.FancyBboxPatch((0.575, 0.37), 0.407, 0.35, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect2)
    ax.text(0.59, 0.695, "DATA QUALITY CHECK TIER COMPLIANCE", transform=ax.transAxes, color=TEXT_WHITE, fontsize=9.5, fontweight="bold")

    sub_ax2 = fig.add_axes([0.61, 0.41, 0.35, 0.24], facecolor=CARD_BG)
    tiers = ["Tier 1: Schema", "Tier 2: Nulls", "Tier 3: Duplicate Keys", "Tier 4: Business Rules"]
    scores = [100.0, 99.85, 99.85, 99.62]
    sub_ax2.barh(tiers, scores, color=[COLOR_PASS, ORANGE_BRIGHT, ORANGE, ORANGE_SOFT])
    sub_ax2.set_xlim(95, 101)
    sub_ax2.set_xlabel("Compliance Rate (%)", color=TEXT_MUTED, fontsize=8)
    sub_ax2.tick_params(colors=TEXT_MUTED, labelsize=8)
    sub_ax2.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    # Right Bottom: Cleansed vs Ingested Record Breakdown
    rect3 = patches.FancyBboxPatch((0.575, 0.03), 0.407, 0.32, boxstyle="round,pad=0.008", transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER)
    ax.add_patch(rect3)
    ax.text(0.59, 0.32, "CONTROLLED DEFECTS RECONCILED (ROWS)", transform=ax.transAxes, color=TEXT_WHITE, fontsize=9.5, fontweight="bold")

    sub_ax3 = fig.add_axes([0.61, 0.06, 0.35, 0.22], facecolor=CARD_BG)
    anom_types = ["Null FKs", "Duplicates", "Negative Qty", "Bad Dates", "Equation Fix"]
    anom_counts = [300, 180, 96, 72, 180]
    sub_ax3.bar(anom_types, anom_counts, color=ORANGE, width=0.45)
    sub_ax3.set_ylabel("Cleansed Rows", color=TEXT_MUTED, fontsize=8)
    sub_ax3.tick_params(colors=TEXT_MUTED, labelsize=8)
    sub_ax3.grid(color=CARD_BORDER, linestyle="--", linewidth=0.5, alpha=0.5)

    plt.savefig(os.path.join(OUTPUT_DIR, "06_data_pipeline_health.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print("  -> Saved 06_data_pipeline_health.png")

def main():
    print("==========================================================================")
    print(" CLARIVENS ENTERPRISE DATA INTELLIGENCE — POWER BI MOCKUP GENERATOR")
    print(" Rendering High-Fidelity Black & Orange Screenshots for All 6 Analytics Pages")
    print("==========================================================================")
    create_page_1()
    create_page_2()
    create_page_3()
    create_page_4()
    create_page_5()
    create_page_6()
    print("==========================================================================")
    print(f" All 6 Clarivens Power BI screenshots generated in {OUTPUT_DIR}")
    print("==========================================================================")

if __name__ == "__main__":
    main()
