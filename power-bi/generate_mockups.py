"""
CLARIVENS ENTERPRISE DATA INTELLIGENCE
High-Fidelity Power BI Dashboard Mockup Generator
Author: Himanshu Bagde (Azure Data Engineer & Cloud Analytics Architect)
Organization: CLARIVENS DATA PLATFORMS

Renders pixel-perfect, dark enterprise dashboard screenshots for all 6 Power BI pages:
1. Executive Overview (CLARIVENS EXECUTIVE INTELLIGENCE)
2. Inventory Intelligence (CLARIVENS INVENTORY INTELLIGENCE)
3. Sales Analytics (CLARIVENS SALES ANALYTICS)
4. Store Performance (CLARIVENS STORE PERFORMANCE)
5. Product & Supplier (CLARIVENS PRODUCT & SUPPLIER INTELLIGENCE)
6. Data Pipeline Health (CLARIVENS DATA PIPELINE OBSERVABILITY)

Theme: Clarivens Black + Orange + Liquid Glassmorphism (16:9 Aspect Ratio)
Full Canvas Frame (0, 0, 1, 1) to eliminate all coordinate mismatch and clipping.
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
GRID_COLOR = "#222228"

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

COLOR_PASS = "#10B981"
COLOR_WARN = "#F59E0B"
COLOR_FAIL = "#EF4444"

def init_canvas():
    fig = plt.figure(figsize=(16, 9), facecolor=BG_COLOR)
    ax = fig.add_axes([0, 0, 1, 1], facecolor=BG_COLOR)
    ax.axis("off")
    return fig, ax

def style_axes(sax):
    sax.set_facecolor(CARD_BG)
    for sp in ["top", "right"]:
        sax.spines[sp].set_visible(False)
    for sp in ["left", "bottom"]:
        sax.spines[sp].set_color(CARD_BORDER)
        sax.spines[sp].set_linewidth(0.8)
    sax.tick_params(colors=TEXT_MUTED, labelsize=7.5, length=3)
    sax.grid(color=GRID_COLOR, linestyle="--", linewidth=0.5, alpha=0.35)

def draw_header(ax, title, subtitle):
    # Top navbar rectangle
    rect = patches.Rectangle((0, 0.930), 1, 0.070, transform=ax.transAxes, facecolor=NAV_BG, edgecolor=CARD_BORDER, linewidth=1)
    ax.add_patch(rect)
    
    # Clarivens 3D Ribbon Logo Mark
    logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "clarivens_icon.png")
    if os.path.exists(logo_path):
        import matplotlib.image as mpimg
        logo_img = mpimg.imread(logo_path)
        logo_ax = ax.figure.add_axes([0.016, 0.938, 0.024, 0.052])
        logo_ax.imshow(logo_img, aspect="equal")
        logo_ax.axis("off")
    else:
        logo_bg = patches.FancyBboxPatch((0.020, 0.944), 0.016, 0.042, boxstyle="round,pad=0.002,rounding_size=0.004",
                                         transform=ax.transAxes, facecolor="#141418", edgecolor=ORANGE, linewidth=1.2)
        ax.add_patch(logo_bg)
        ax.text(0.028, 0.965, "C", transform=ax.transAxes, color=ORANGE_BRIGHT, fontsize=11, fontweight="bold", ha="center", va="center")

    # Wordmark with generous spacing to avoid ANY overlap
    ax.text(0.044, 0.965, "CLARIVENS", transform=ax.transAxes, color=TEXT_WHITE, fontsize=11.5, fontweight="bold", va="center")
    ax.text(0.128, 0.965, "|   ENTERPRISE DATA INTELLIGENCE", transform=ax.transAxes, color=ORANGE, fontsize=9.2, fontweight="bold", va="center")
    ax.text(0.044, 0.944, f"{title.upper()}   •   {subtitle}", transform=ax.transAxes, color=TEXT_MUTED, fontsize=7.5, va="center")
    
    # Right telemetry
    ax.text(0.980, 0.965, "DATA AS OF: 2025-12-31   •   REFRESH: AUTOMATED (AZURE DATA FACTORY)", transform=ax.transAxes, color=GRAY_LIGHT, fontsize=7.5, fontweight="bold", ha="right", va="center")
    ax.text(0.980, 0.944, "ENVIRONMENT: PRODUCTION WAREHOUSE   •   AZURE SQL DW (dw schema)", transform=ax.transAxes, color=TEXT_MUTED, fontsize=7, ha="right", va="center")

def draw_slicer_bar(ax, slicers):
    s_y = 0.888
    s_h = 0.034
    s_rect = patches.Rectangle((0, s_y), 1, s_h, transform=ax.transAxes, facecolor="#09090C", edgecolor=CARD_BORDER, linewidth=0.5)
    ax.add_patch(s_rect)
    
    ax.text(0.020, s_y + 0.017, "FILTERS:", transform=ax.transAxes, color=TEXT_MUTED, fontsize=7.5, fontweight="bold", va="center")
    
    curr_x = 0.072
    box_w = 0.165
    for label, val, is_active in slicers:
        bg_col = "#18181C" if is_active else "#101014"
        b_col = ORANGE if is_active else CARD_BORDER
        pill = patches.FancyBboxPatch((curr_x, s_y + 0.004), box_w, s_h - 0.008,
                                      boxstyle="round,pad=0.002,rounding_size=0.004",
                                      transform=ax.transAxes, facecolor=bg_col, edgecolor=b_col, linewidth=0.8)
        ax.add_patch(pill)
        
        ax.text(curr_x + 0.008, s_y + 0.017, label + ":", transform=ax.transAxes, color=TEXT_MUTED, fontsize=7, va="center")
        val_col = ORANGE_BRIGHT if is_active else TEXT_WHITE
        ax.text(curr_x + box_w - 0.008, s_y + 0.017, val, transform=ax.transAxes, color=val_col, fontsize=7.5, fontweight="bold", ha="right", va="center")
        curr_x += box_w + 0.015

def draw_kpi_card(ax, x, y, w, h, label, value, subtext="", status_color=ORANGE):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.010",
                                  transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER, linewidth=1)
    ax.add_patch(rect)
    
    highlight = patches.Rectangle((x + 0.008, y + h - 0.002), w - 0.016, 0.002, transform=ax.transAxes, facecolor=ORANGE, alpha=0.8)
    ax.add_patch(highlight)
    
    ax.text(x + 0.010, y + h - 0.022, label.upper(), transform=ax.transAxes, color=TEXT_MUTED, fontsize=7.2, fontweight="bold")
    ax.text(x + 0.010, y + 0.038, value, transform=ax.transAxes, color=status_color, fontsize=14, fontweight="bold")
    if subtext:
        ax.text(x + 0.010, y + 0.014, subtext, transform=ax.transAxes, color=GRAY_LIGHT, fontsize=6.8)

def draw_card_frame(ax, x, y, w, h, title, subtitle=""):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.010",
                                  transform=ax.transAxes, facecolor=CARD_BG, edgecolor=CARD_BORDER, linewidth=1)
    ax.add_patch(rect)
    ax.text(x + 0.016, y + h - 0.024, title.upper(), transform=ax.transAxes, color=TEXT_WHITE, fontsize=8.8, fontweight="bold")
    if subtitle:
        ax.text(x + 0.016, y + h - 0.044, subtitle, transform=ax.transAxes, color=TEXT_MUTED, fontsize=7)

def create_page_1():
    print("Generating Page 1: Clarivens Executive Intelligence...")
    fig, ax = init_canvas()

    draw_header(ax, "Clarivens Executive Intelligence", "Enterprise Sales & Inventory High-Level KPIs")
    draw_slicer_bar(ax, [("Fiscal Year", "FY2025", True), ("Region", "All Stores (36)", False), ("Channel", "Omni-Channel", False), ("Currency", "INR (₹)", True)])

    # Top KPI row (6 cards)
    kpis = [
        ("Total Sales Revenue", "₹142.8M", "+18.4% YoY Growth", ORANGE_BRIGHT),
        ("Units Sold", "284,520", "+12.1% YoY Volume", TEXT_WHITE),
        ("Gross Profit", "₹48.6M", "34.0% Gross Margin", ORANGE),
        ("Inventory Valuation", "₹64.2M", "42,640 Snapshots", GRAY_LIGHT),
        ("Days of Inventory", "18.4 Days", "Target: 15-20 Days", TEXT_WHITE),
        ("Stockout Risk Alerts", "148 SKUs", "Critical: 42 | High: 106", COLOR_WARN)
    ]
    for i, (lbl, val, sub, col) in enumerate(kpis):
        draw_kpi_card(ax, 0.020 + i * 0.162, 0.755, 0.148, 0.115, lbl, val, sub, col)

    # Chart 1: Monthly Revenue & Gross Profit Trend (left half)
    draw_card_frame(ax, 0.020, 0.395, 0.575, 0.340,
                    "2025 Monthly Revenue & Profit Trajectory (INR Millions)",
                    "Clarivens Revenue (Orange) vs Gross Profit (Charcoal Surface)")

    sub_ax1 = fig.add_axes([0.065, 0.435, 0.515, 0.230])
    style_axes(sub_ax1)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    rev = [9.8, 10.2, 10.8, 12.4, 11.2, 12.9, 10.5, 11.1, 13.2, 14.8, 16.2, 12.1]
    profit = [3.3, 3.5, 3.7, 4.2, 3.8, 4.4, 3.6, 3.8, 4.5, 5.0, 5.5, 4.1]
    
    sub_ax1.bar(np.arange(12) - 0.18, rev, width=0.36, color=ORANGE, label="Revenue")
    sub_ax1.bar(np.arange(12) + 0.18, profit, width=0.36, color=GRAY_MID, edgecolor=CARD_BORDER, label="Gross Profit")
    sub_ax1.set_xticks(range(12))
    sub_ax1.set_xticklabels(months, color=TEXT_MUTED, fontsize=7.5)
    sub_ax1.set_ylim(0, 18)
    sub_ax1.legend(facecolor=CARD_INNER, edgecolor=CARD_BORDER, labelcolor=TEXT_WHITE, fontsize=7.5, loc="upper left")

    # Chart 2: Revenue by Category (right half)
    draw_card_frame(ax, 0.615, 0.395, 0.365, 0.340,
                    "Revenue Contribution by Merchandise Category",
                    "Ranked by total annual gross revenue contribution")

    sub_ax2 = fig.add_axes([0.725, 0.435, 0.235, 0.230])
    style_axes(sub_ax2)
    cats = ["Electronics", "Home Appl.", "Personal Care", "Grocery", "Beverages", "Home/Kitchen", "Sports"]
    cat_rev = [38.4, 26.2, 18.5, 19.8, 14.2, 15.1, 10.6]
    cat_colors = [ORANGE_BRIGHT, ORANGE, ORANGE_SOFT, GRAY_LIGHT, GRAY_MUTED, GRAY_MID, GRAY_DARK]
    y_pos = np.arange(len(cats))
    sub_ax2.barh(y_pos, cat_rev, color=cat_colors, height=0.58)
    sub_ax2.set_yticks(y_pos)
    sub_ax2.set_yticklabels(cats, color=TEXT_WHITE, fontsize=7.5)
    sub_ax2.invert_yaxis()
    sub_ax2.set_xlim(0, 46)
    sub_ax2.set_xlabel("Revenue (₹M)", color=TEXT_MUTED, fontsize=7)

    # Bottom Left: Regional Store Performance
    draw_card_frame(ax, 0.020, 0.035, 0.470, 0.340,
                    "Top 5 Regional Store Clusters (INR Millions)",
                    "Sales volume across 36 stores mapped to geographic territories")

    sub_ax3 = fig.add_axes([0.160, 0.075, 0.310, 0.230])
    style_axes(sub_ax3)
    regions = ["West (Mumbai/Pune)", "South (Bengaluru/Hyd)", "North (Delhi/Jaipur)", "East (Kolkata)", "Central (Nagpur)"]
    reg_sales = [52.4, 46.1, 28.5, 11.2, 4.6]
    reg_colors = [ORANGE_BRIGHT, ORANGE, GRAY_LIGHT, GRAY_MUTED, GRAY_MID]
    sub_ax3.barh(range(len(regions)), reg_sales, color=reg_colors, height=0.55)
    sub_ax3.set_yticks(range(len(regions)))
    sub_ax3.set_yticklabels(regions, color=TEXT_WHITE, fontsize=7.5)
    sub_ax3.invert_yaxis()
    sub_ax3.set_xlim(0, 62)
    sub_ax3.set_xlabel("Revenue (₹M)", color=TEXT_MUTED, fontsize=7)

    # Bottom Right: Stockout Risk Level Distribution (Donut with side legend)
    draw_card_frame(ax, 0.510, 0.035, 0.470, 0.340,
                    "Inventory Stockout Risk Level Distribution",
                    "42,640 active stock snapshots classified by replenishment risk")

    sub_ax4 = fig.add_axes([0.525, 0.055, 0.240, 0.250])
    sub_ax4.set_facecolor(CARD_BG)
    sub_ax4.axis("off")
    risk_labels = ["Low Risk (>14d)", "Medium (8-14d)", "High Risk (4-7d)", "Critical (<=3d)"]
    risk_counts = [28450, 9420, 3120, 1650]
    risk_colors = [GRAY_DARK, GRAY_MID, COLOR_WARN, ORANGE]
    sub_ax4.pie(risk_counts, colors=risk_colors, autopct="%1.1f%%", pctdistance=0.70,
                textprops={"color": TEXT_WHITE, "fontsize": 7.5, "fontweight": "bold"}, startangle=140,
                wedgeprops={"width": 0.45, "edgecolor": CARD_BORDER, "linewidth": 1})

    leg_x = 0.775
    leg_y = 0.250
    for l_idx, (l_name, l_col, l_cnt) in enumerate(zip(risk_labels, risk_colors, risk_counts)):
        sq = patches.Rectangle((leg_x, leg_y - l_idx * 0.048), 0.012, 0.018, transform=ax.transAxes, facecolor=l_col, edgecolor=CARD_BORDER)
        ax.add_patch(sq)
        ax.text(leg_x + 0.018, leg_y - l_idx * 0.048 + 0.009, l_name, transform=ax.transAxes, color=TEXT_WHITE, fontsize=7.5, va="center")
        ax.text(leg_x + 0.175, leg_y - l_idx * 0.048 + 0.009, f"{l_cnt:,}", transform=ax.transAxes, color=TEXT_MUTED, fontsize=7, ha="right", va="center")

    plt.savefig(os.path.join(OUTPUT_DIR, "01_executive_overview.png"), dpi=200, facecolor=BG_COLOR, edgecolor="none")
    plt.close()
    print("  -> Saved 01_executive_overview.png")

def create_page_2():
    print("Generating Page 2: Clarivens Inventory Intelligence...")
    fig, ax = init_canvas()

    draw_header(ax, "Clarivens Inventory Intelligence", "Stockout Risk, Replenishment Velocity & Reorder Alerts")
    draw_slicer_bar(ax, [("Risk Tier", "All Tiers", False), ("Category", "Electronics & FMCG", True), ("Store Format", "Flagship & Hyper", True), ("Replenishment", "Alerts Active", True)])

    kpis = [
        ("Current On-Hand", "412,800 Units", "Across 36 Active Stores", TEXT_WHITE),
        ("Inventory Valuation", "₹64.25M", "Valued at UnitCost", ORANGE_BRIGHT),
        ("Days of Inventory", "18.4 Days", "Demand Coverage Ratio", ORANGE),
        ("Critical Stock (<=3d)", "42 Items", "Immediate Stockout Risk", COLOR_FAIL),
        ("High Risk (4-7d)", "106 Items", "Expedite Reorder Workflow", COLOR_WARN),
        ("Reorder Required", "248 Alerts", "Stock <= Safety Threshold", ORANGE_SOFT)
    ]
    for i, (lbl, val, sub, col) in enumerate(kpis):
        draw_kpi_card(ax, 0.020 + i * 0.162, 0.755, 0.148, 0.115, lbl, val, sub, col)

    # Main Grid: Inventory Risk Action Table (Left side)
    draw_card_frame(ax, 0.020, 0.035, 0.655, 0.700,
                    "Critical & High Stockout Risk Action Matrix",
                    "Active product/store combinations requiring immediate procurement intervention")

    headers = ["Product Name", "Store Location", "Stock", "ADS", "Days Left", "Risk Tier", "Reorder Qty"]
    col_x = [0.036, 0.285, 0.415, 0.465, 0.515, 0.565, 0.620]
    for h_name, hx in zip(headers, col_x):
        ax.text(hx, 0.655, h_name.upper(), transform=ax.transAxes, color=ORANGE, fontsize=7.5, fontweight="bold")

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

    y_start = 0.615
    for r in table_rows:
        prod, store, stock, ads, days, tier, reorder, color = r
        ax.text(col_x[0], y_start, prod[:30], transform=ax.transAxes, color=TEXT_WHITE, fontsize=7.5)
        ax.text(col_x[1], y_start, store[:16], transform=ax.transAxes, color=GRAY_LIGHT, fontsize=7.5)
        ax.text(col_x[2], y_start, stock, transform=ax.transAxes, color=TEXT_WHITE, fontsize=7.5)
        ax.text(col_x[3], y_start, ads, transform=ax.transAxes, color=GRAY_LIGHT, fontsize=7.5)
        ax.text(col_x[4], y_start, days, transform=ax.transAxes, color=color, fontsize=7.5, fontweight="bold")
        ax.text(col_x[5], y_start, tier, transform=ax.transAxes, color=color, fontsize=7.5, fontweight="bold")
        ax.text(col_x[6], y_start, reorder, transform=ax.transAxes, color=ORANGE_BRIGHT, fontsize=7.5)
        y_start -= 0.053

    # Right side Top: Days of Inventory by Category
    draw_card_frame(ax, 0.695, 0.395, 0.285, 0.340,
                    "Avg Days of Inventory by Category",
                    "Low DOI indicates high velocity stock depletion")

    sub_ax_doi = fig.add_axes([0.780, 0.435, 0.185, 0.230])
    style_axes(sub_ax_doi)
    c_names = ["Beverages", "Grocery", "Electronics", "Personal Care", "Stationery", "Home Appl."]
    c_doi = [9.4, 12.8, 16.5, 21.2, 24.8, 28.1]
    c_colors = [COLOR_FAIL, COLOR_WARN, ORANGE_BRIGHT, ORANGE, GRAY_MUTED, GRAY_DARK]
    sub_ax_doi.barh(range(len(c_names)), c_doi, color=c_colors, height=0.55)
    sub_ax_doi.set_yticks(range(len(c_names)))
    sub_ax_doi.set_yticklabels(c_names, color=TEXT_WHITE, fontsize=7.5)
    sub_ax_doi.invert_yaxis()
    sub_ax_doi.set_xlim(0, 35)
    sub_ax_doi.set_xlabel("Days", color=TEXT_MUTED, fontsize=7)

    # Right side Bottom: Turnover by Store Format
    draw_card_frame(ax, 0.695, 0.035, 0.285, 0.340,
                    "Inventory Turnover by Format",
                    "Annualized inventory turn rates across store types")

    sub_ax_turn = fig.add_axes([0.745, 0.075, 0.215, 0.230])
    style_axes(sub_ax_turn)
    stypes = ["Flagship", "Hyper", "Super", "Express"]
    turns = [6.8, 5.9, 4.4, 3.2]
    sub_ax_turn.bar(stypes, turns, color=ORANGE, width=0.45)
    sub_ax_turn.set_ylabel("Turns (x/yr)", color=TEXT_MUTED, fontsize=7)
    sub_ax_turn.set_ylim(0, 8)

    plt.savefig(os.path.join(OUTPUT_DIR, "02_inventory_intelligence.png"), dpi=200, facecolor=BG_COLOR, edgecolor="none")
    plt.close()
    print("  -> Saved 02_inventory_intelligence.png")

def create_page_3():
    print("Generating Page 3: Clarivens Sales Analytics...")
    fig, ax = init_canvas()

    draw_header(ax, "Clarivens Sales Analytics", "Customer Segments, Tender Types & Product Velocity")
    draw_slicer_bar(ax, [("Tender Type", "All Modes", False), ("Customer Segment", "All Segments", False), ("Promotion", "Active Campaigns", True), ("Sales Channel", "Store POS", True)])

    kpis = [
        ("Total Sales Volume", "120,462 Orders", "+14.2% MoM Surge", ORANGE_BRIGHT),
        ("Average Order Value", "₹1,185.80", "+4.8% vs Prior Year", TEXT_WHITE),
        ("Top Category", "Electronics", "26.9% Total Share", ORANGE),
        ("UPI Penetration", "45.2%", "Leading Digital Payment", ORANGE_SOFT),
        ("Promotional Sales", "24.8%", "Campaign Surge", GRAY_LIGHT),
        ("Gross Margin", "34.02%", "34.0% Target Achieved", TEXT_WHITE)
    ]
    for i, (lbl, val, sub, col) in enumerate(kpis):
        draw_kpi_card(ax, 0.020 + i * 0.162, 0.755, 0.148, 0.115, lbl, val, sub, col)

    # Middle Row: 3 Cards
    # Card 1: Tender Types
    draw_card_frame(ax, 0.020, 0.395, 0.305, 0.340, "Sales by Payment Method", "Distribution across checkout payment modes")
    sub_ax1 = fig.add_axes([0.050, 0.420, 0.245, 0.245])
    sub_ax1.set_facecolor(CARD_BG)
    sub_ax1.axis("off")
    tenders = ["UPI", "Credit", "Debit", "Cash", "NetBank"]
    t_counts = [45, 25, 15, 10, 5]
    t_colors = [ORANGE_BRIGHT, ORANGE, GRAY_LIGHT, GRAY_MUTED, GRAY_DARK]
    sub_ax1.pie(t_counts, labels=tenders, colors=t_colors, autopct="%1.0f%%", pctdistance=0.70,
                textprops={"color": TEXT_WHITE, "fontsize": 7.5}, startangle=140,
                wedgeprops={"width": 0.45, "edgecolor": CARD_BORDER, "linewidth": 1})

    # Card 2: Customer Segments
    draw_card_frame(ax, 0.345, 0.395, 0.305, 0.340, "Revenue by Customer Segment", "Contribution by customer loyalty tier")
    sub_ax2 = fig.add_axes([0.395, 0.435, 0.235, 0.230])
    style_axes(sub_ax2)
    segs = ["Regular", "Walk-in", "Premium", "Corporate"]
    seg_rev = [64.2, 49.8, 21.4, 7.4]
    sub_ax2.bar(segs, seg_rev, color=[ORANGE_BRIGHT, ORANGE, GRAY_LIGHT, GRAY_DARK], width=0.45)
    sub_ax2.set_ylabel("Revenue (₹M)", color=TEXT_MUTED, fontsize=7)
    sub_ax2.set_ylim(0, 75)

    # Card 3: Regional Contribution
    draw_card_frame(ax, 0.670, 0.395, 0.310, 0.340, "Regional Revenue Contribution", "Share by operational sales territory")
    sub_ax3 = fig.add_axes([0.700, 0.420, 0.250, 0.245])
    sub_ax3.set_facecolor(CARD_BG)
    sub_ax3.axis("off")
    regs = ["West", "South", "North", "East", "Central"]
    r_rev = [36.7, 32.3, 20.0, 7.8, 3.2]
    r_cols = [ORANGE_BRIGHT, ORANGE, ORANGE_HIGHLIGHT, GRAY_MUTED, GRAY_DARK]
    sub_ax3.pie(r_rev, labels=regs, colors=r_cols, autopct="%1.1f%%", pctdistance=0.72,
                textprops={"color": TEXT_WHITE, "fontsize": 7.5},
                wedgeprops={"width": 0.45, "edgecolor": CARD_BORDER, "linewidth": 1})

    # Bottom Row: Top 10 Best Selling Products
    draw_card_frame(ax, 0.020, 0.035, 0.960, 0.340,
                    "Top 10 Best Selling Products by Annual Gross Revenue (INR Millions)",
                    "High-velocity retail merchandise SKUs driving omni-channel sales")

    sub_ax4 = fig.add_axes([0.065, 0.075, 0.895, 0.230])
    style_axes(sub_ax4)
    prods = [
        "Sony UltraHD TV", "Samsung Air Fryer", "OnePlus Earbuds", "Philips Microwave",
        "Prestige Cooker", "Mamaearth Cream", "Tata Tea Gold", "Decathlon Mat", "Titan Watch", "Classmate A5"
    ]
    p_rev = [8.4, 6.2, 5.8, 4.9, 4.2, 3.8, 3.4, 2.9, 2.7, 2.1]
    p_cols = [ORANGE_BRIGHT, ORANGE, ORANGE, ORANGE_SOFT, GRAY_LIGHT, GRAY_LIGHT, GRAY_MUTED, GRAY_MUTED, GRAY_MID, GRAY_MID]
    sub_ax4.bar(prods, p_rev, color=p_cols, width=0.45)
    sub_ax4.set_ylabel("Revenue (₹M)", color=TEXT_MUTED, fontsize=7)
    sub_ax4.set_ylim(0, 10)

    plt.savefig(os.path.join(OUTPUT_DIR, "03_sales_analytics.png"), dpi=200, facecolor=BG_COLOR, edgecolor="none")
    plt.close()
    print("  -> Saved 03_sales_analytics.png")

def create_page_4():
    print("Generating Page 4: Clarivens Store Performance...")
    fig, ax = init_canvas()

    draw_header(ax, "Clarivens Store Performance", "Benchmarking 36 Retail Stores Across 9 Indian States")
    draw_slicer_bar(ax, [("Store Cluster", "All 36 Stores", False), ("Tier City", "Tier 1 & Metro", True), ("Format", "All Formats", False), ("Metric Focus", "Revenue & Margin", True)])

    kpis = [
        ("Total Operating Stores", "36 Locations", "4 Operating Formats", TEXT_WHITE),
        ("Average Revenue / Store", "₹3.97M", "Annual Sales Velocity", ORANGE_BRIGHT),
        ("Average Rev / Sq Ft", "₹182.40", "Retail Floor Density", ORANGE),
        ("Top City by Sales", "Mumbai", "6 Stores / ₹28.4M Total", ORANGE_SOFT),
        ("Fastest Growing", "Bengaluru", "+24.2% YoY Growth", COLOR_PASS),
        ("Avg Return Rate", "1.84%", "Under 3.0% Limit", COLOR_WARN)
    ]
    for i, (lbl, val, sub, col) in enumerate(kpis):
        draw_kpi_card(ax, 0.020 + i * 0.162, 0.755, 0.148, 0.115, lbl, val, sub, col)

    # Left: Store Ranking Bar Chart (Full height)
    draw_card_frame(ax, 0.020, 0.035, 0.485, 0.700,
                    "Top 12 Stores by Revenue & Margin Efficiency",
                    "Store-level revenue ranking across multi-format retail footprint")

    sub_ax1 = fig.add_axes([0.160, 0.075, 0.325, 0.585])
    style_axes(sub_ax1)
    top_stores = [
        "Mumbai Flagship #1", "Bengaluru Flagship #1", "Delhi Hypermarket #1", "Pune Flagship #1",
        "Hyderabad Flagship #1", "Ahmedabad Hyper #1", "Mumbai Hypermarket #2", "Chennai Hyper #1",
        "Kolkata Flagship #1", "Jaipur Supermarket #1", "Lucknow Super #1", "Nagpur Express #1"
    ]
    store_sales = [7.8, 7.4, 6.9, 6.2, 5.8, 5.1, 4.9, 4.4, 3.8, 3.2, 2.8, 1.9]
    store_cols = [ORANGE_BRIGHT, ORANGE, ORANGE, ORANGE_SOFT, GRAY_LIGHT, GRAY_LIGHT, GRAY_MUTED, GRAY_MUTED, GRAY_MID, GRAY_MID, GRAY_DARK, GRAY_DARK]
    y_pos = np.arange(len(top_stores))
    sub_ax1.barh(y_pos, store_sales, color=store_cols, height=0.6)
    sub_ax1.set_yticks(y_pos)
    sub_ax1.set_yticklabels(top_stores, color=TEXT_WHITE, fontsize=7.5)
    sub_ax1.invert_yaxis()
    sub_ax1.set_xlim(0, 9)
    sub_ax1.set_xlabel("Revenue (INR Millions)", color=TEXT_MUTED, fontsize=7)

    # Right Top: Revenue & Margin by Store Format
    draw_card_frame(ax, 0.525, 0.395, 0.455, 0.340,
                    "Revenue & Margin by Store Format",
                    "Comparison of revenue volume vs gross margin percentage")

    sub_ax2 = fig.add_axes([0.575, 0.435, 0.355, 0.230])
    style_axes(sub_ax2)
    formats = ["Flagship", "Hypermarket", "Supermarket", "Express"]
    f_rev = [44.2, 51.6, 34.8, 12.2]
    f_margin = [36.2, 34.8, 33.1, 31.4]
    sub_ax2.bar(np.arange(4) - 0.15, f_rev, width=0.3, color=ORANGE, label="Revenue (₹M)")
    ax2_twin = sub_ax2.twinx()
    ax2_twin.plot(np.arange(4) + 0.15, f_margin, color=ORANGE_HIGHLIGHT, marker="o", linewidth=2, label="Gross Margin %")
    ax2_twin.tick_params(colors=TEXT_MUTED, labelsize=7.5)
    ax2_twin.spines["top"].set_visible(False)
    ax2_twin.spines["left"].set_visible(False)
    ax2_twin.spines["right"].set_color(CARD_BORDER)
    ax2_twin.set_ylim(20, 45)
    sub_ax2.set_xticks(range(4))
    sub_ax2.set_xticklabels(formats, color=TEXT_WHITE, fontsize=7.5)
    sub_ax2.set_ylim(0, 65)
    sub_ax2.set_ylabel("Revenue (₹M)", color=TEXT_MUTED, fontsize=7)
    ax2_twin.set_ylabel("Margin %", color=TEXT_MUTED, fontsize=7)

    # Right Bottom: Store Footprint Density Matrix (Scatter)
    draw_card_frame(ax, 0.525, 0.035, 0.455, 0.340,
                    "Store Footprint & Density Matrix (Sq Ft vs Sales)",
                    "Capital efficiency: Store retail floor area vs generated revenue")

    sub_ax3 = fig.add_axes([0.575, 0.075, 0.355, 0.230])
    style_axes(sub_ax3)
    sqft_vals = [45000, 52000, 38000, 41000, 32000, 28000, 18000, 15000, 8000, 6000]
    rev_vals = [7.8, 7.4, 6.9, 6.2, 5.8, 5.1, 3.8, 3.2, 1.9, 1.4]
    sub_ax3.scatter(sqft_vals, rev_vals, color=ORANGE, s=90, edgecolors=TEXT_WHITE, linewidth=1, alpha=0.9)
    sub_ax3.set_xlabel("Store Floor Area (Sq Ft)", color=TEXT_MUTED, fontsize=7)
    sub_ax3.set_ylabel("Revenue (₹M)", color=TEXT_MUTED, fontsize=7)
    sub_ax3.set_xlim(0, 60000)
    sub_ax3.set_ylim(0, 9)

    plt.savefig(os.path.join(OUTPUT_DIR, "04_store_performance.png"), dpi=200, facecolor=BG_COLOR, edgecolor="none")
    plt.close()
    print("  -> Saved 04_store_performance.png")

def create_page_5():
    print("Generating Page 5: Clarivens Product & Supplier Intelligence...")
    fig, ax = init_canvas()

    draw_header(ax, "Clarivens Product & Supplier Intelligence", "Procurement Fulfillment, Vendor SLAs & Product Defect Rates")
    draw_slicer_bar(ax, [("Vendor Rating", "All Ratings", False), ("SLA Tier", "Standard & Fast-Track", True), ("PO Status", "All Purchase Orders", False), ("Lead Time", "Pan-India", False)])

    kpis = [
        ("Cataloged SKUs", "1,200 Products", "9 Core Categories", TEXT_WHITE),
        ("Active Suppliers", "60 Vendors", "Pan-India Network", ORANGE_SOFT),
        ("Purchase Orders", "10,500 POs", "Total Spend: ₹38.2M", ORANGE_BRIGHT),
        ("On-Time Delivery", "88.4%", "Within Contract SLA", COLOR_PASS),
        ("Delayed PO Rate", "7.6%", "Avg Delay: 4.8 Days", COLOR_WARN),
        ("Return Rate", "1.84%", "5,249 Defect Records", COLOR_FAIL)
    ]
    for i, (lbl, val, sub, col) in enumerate(kpis):
        draw_kpi_card(ax, 0.020 + i * 0.162, 0.755, 0.148, 0.115, lbl, val, sub, col)

    # Left: Supplier Lead Time vs Delivery Performance
    draw_card_frame(ax, 0.020, 0.035, 0.485, 0.700,
                    "Top 10 Suppliers by Purchase Order Volume & SLA Score",
                    "Vendor spend analysis and contractual procurement fulfillment")

    sub_ax1 = fig.add_axes([0.165, 0.075, 0.320, 0.585])
    style_axes(sub_ax1)
    sups = [
        "Aura Consumer Brands", "Apex Electronics Ltd", "Vanguard Appliances", "Lotus Personal Care",
        "Himalayan Spring", "Sovereign Kitchenwares", "Velocity Sports", "Indus Valley Staples",
        "Zenith Audio & Tech", "BlueStar Home Comfort"
    ]
    po_vol = [4.8, 4.2, 3.9, 3.5, 3.1, 2.9, 2.6, 2.4, 2.1, 1.9]
    sup_cols = [ORANGE_BRIGHT, ORANGE, ORANGE, ORANGE_SOFT, GRAY_LIGHT, GRAY_LIGHT, GRAY_MUTED, GRAY_MUTED, GRAY_MID, GRAY_DARK]
    y_pos = np.arange(len(sups))
    sub_ax1.barh(y_pos, po_vol, color=sup_cols, height=0.6)
    sub_ax1.set_yticks(y_pos)
    sub_ax1.set_yticklabels(sups, color=TEXT_WHITE, fontsize=7.5)
    sub_ax1.invert_yaxis()
    sub_ax1.set_xlim(0, 6)
    sub_ax1.set_xlabel("Purchase Order Spend (₹M)", color=TEXT_MUTED, fontsize=7)

    # Right Top: PO Status Breakdown
    draw_card_frame(ax, 0.525, 0.395, 0.455, 0.340,
                    "Purchase Order Fulfillment Status",
                    "10,500 PO tracking events across procurement lifecycle")

    sub_ax2 = fig.add_axes([0.550, 0.420, 0.250, 0.245])
    sub_ax2.set_facecolor(CARD_BG)
    sub_ax2.axis("off")
    po_labels = ["Completed", "Delayed", "In-Transit", "Cancelled"]
    po_counts = [8840, 760, 520, 380]
    po_colors = [COLOR_PASS, COLOR_WARN, ORANGE, COLOR_FAIL]
    sub_ax2.pie(po_counts, colors=po_colors, autopct="%1.1f%%", pctdistance=0.70,
                textprops={"color": TEXT_WHITE, "fontsize": 7.5, "fontweight": "bold"},
                wedgeprops={"width": 0.45, "edgecolor": CARD_BORDER, "linewidth": 1})

    leg_x = 0.815
    leg_y = 0.620
    for l_idx, (l_name, l_col, l_cnt) in enumerate(zip(po_labels, po_colors, po_counts)):
        sq = patches.Rectangle((leg_x, leg_y - l_idx * 0.048), 0.012, 0.018, transform=ax.transAxes, facecolor=l_col, edgecolor=CARD_BORDER)
        ax.add_patch(sq)
        ax.text(leg_x + 0.018, leg_y - l_idx * 0.048 + 0.009, l_name, transform=ax.transAxes, color=TEXT_WHITE, fontsize=7.5, va="center")
        ax.text(leg_x + 0.145, leg_y - l_idx * 0.048 + 0.009, f"{l_cnt:,}", transform=ax.transAxes, color=TEXT_MUTED, fontsize=7, ha="right", va="center")

    # Right Bottom: Customer Return Reasons
    draw_card_frame(ax, 0.525, 0.035, 0.455, 0.340,
                    "Customer Return Root Cause Classification",
                    "Analysis of 5,249 product defect and merchandise return events")

    sub_ax3 = fig.add_axes([0.575, 0.075, 0.355, 0.230])
    style_axes(sub_ax3)
    reasons = ["Defect Item", "Wrong Item", "Size Issue", "Mind Chg", "Transit Dam"]
    pcts = [35.2, 20.4, 19.8, 14.5, 10.1]
    sub_ax3.bar(reasons, pcts, color=[COLOR_FAIL, COLOR_WARN, ORANGE, GRAY_MUTED, GRAY_DARK], width=0.45)
    sub_ax3.set_ylabel("% Returns", color=TEXT_MUTED, fontsize=7)
    sub_ax3.set_ylim(0, 45)

    plt.savefig(os.path.join(OUTPUT_DIR, "05_product_supplier_analysis.png"), dpi=200, facecolor=BG_COLOR, edgecolor="none")
    plt.close()
    print("  -> Saved 05_product_supplier_analysis.png")

def create_page_6():
    print("Generating Page 6: Clarivens Data Pipeline Observability...")
    fig, ax = init_canvas()

    draw_header(ax, "Clarivens Data Pipeline Observability", "ADF Telemetry, Data Quality Gates & Audit Logging")
    draw_slicer_bar(ax, [("Pipeline Scope", "All 11 Pipelines", False), ("Run Environment", "Production", True), ("Quality Tier", "Tiers 1 to 4", True), ("Status Filter", "Success & Warnings", True)])

    kpis = [
        ("ADF Master Pipeline", "SUCCESS", "All 11 Pipelines Active", COLOR_PASS),
        ("SQL Warehouse Load", "SUCCESS", "Incremental Load 100%", COLOR_PASS),
        ("Python Validation", "SUCCESS", "59 Passed / 16 Warnings", COLOR_PASS),
        ("Data Quality Score", "99.93%", "Enterprise Gate >= 98.0%", ORANGE_BRIGHT),
        ("Records Ingested", "178,851 Rows", "Sales, Inventory & POs", TEXT_WHITE),
        ("Controlled Anomalies", "1,112 Rows", "Caught & Cleansed", COLOR_WARN)
    ]
    for i, (lbl, val, sub, col) in enumerate(kpis):
        draw_kpi_card(ax, 0.020 + i * 0.162, 0.755, 0.148, 0.115, lbl, val, sub, col)

    # Activity Execution Grid (left side)
    draw_card_frame(ax, 0.020, 0.035, 0.545, 0.700,
                    "Azure Data Factory Pipeline Execution Telemetry",
                    "Activity telemetry captured live from audit.PipelineExecutionLog")

    headers = ["Pipeline Name", "Activity Name", "Duration", "Rows Ingested", "Status"]
    col_x = [0.036, 0.205, 0.340, 0.410, 0.495]
    for h_name, hx in zip(headers, col_x):
        ax.text(hx, 0.655, h_name.upper(), transform=ax.transAxes, color=ORANGE, fontsize=7.5, fontweight="bold")

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

    y_pos = 0.615
    for row in adf_logs:
        pname, act, dur, rows, status, col = row
        ax.text(col_x[0], y_pos, pname[:20], transform=ax.transAxes, color=TEXT_WHITE, fontsize=7.5)
        ax.text(col_x[1], y_pos, act[:18], transform=ax.transAxes, color=GRAY_LIGHT, fontsize=7.5)
        ax.text(col_x[2], y_pos, dur, transform=ax.transAxes, color=GRAY_MUTED, fontsize=7.5)
        ax.text(col_x[3], y_pos, rows, transform=ax.transAxes, color=TEXT_WHITE, fontsize=7.5)
        ax.text(col_x[4], y_pos, f"● {status}", transform=ax.transAxes, color=col, fontsize=7.5, fontweight="bold")
        y_pos -= 0.053

    # Right Top: Python Data Quality Rule Compliance
    draw_card_frame(ax, 0.585, 0.395, 0.395, 0.340,
                    "Data Quality Check Tier Compliance",
                    "Validation pass rate across 75 automated quality rules")

    sub_ax2 = fig.add_axes([0.720, 0.435, 0.240, 0.230])
    style_axes(sub_ax2)
    tiers = ["Tier 1: Schema", "Tier 2: Nulls", "Tier 3: Uniqueness", "Tier 4: Business"]
    scores = [100.0, 99.85, 99.85, 99.62]
    sub_ax2.barh(tiers, scores, color=[COLOR_PASS, ORANGE_BRIGHT, ORANGE, ORANGE_SOFT], height=0.55)
    sub_ax2.set_xlim(95, 101)
    sub_ax2.set_xlabel("Compliance %", color=TEXT_MUTED, fontsize=7)

    # Right Bottom: Cleansed Record Breakdown
    draw_card_frame(ax, 0.585, 0.035, 0.395, 0.340,
                    "Controlled Defects Reconciled (Rows)",
                    "Pre-warehouse data cleansing & automated outlier isolation")

    sub_ax3 = fig.add_axes([0.635, 0.075, 0.325, 0.230])
    style_axes(sub_ax3)
    anom_types = ["Null FK", "Dupl", "Neg Qty", "Bad Date", "Math Fix"]
    anom_counts = [300, 180, 96, 72, 180]
    sub_ax3.bar(anom_types, anom_counts, color=ORANGE, width=0.45)
    sub_ax3.set_ylabel("Cleansed Rows", color=TEXT_MUTED, fontsize=7)
    sub_ax3.set_ylim(0, 350)

    plt.savefig(os.path.join(OUTPUT_DIR, "06_data_pipeline_health.png"), dpi=200, facecolor=BG_COLOR, edgecolor="none")
    plt.close()
    print("  -> Saved 06_data_pipeline_health.png")

def main():
    print("==========================================================================")
    print(" CLARIVENS POWER BI MOCKUP GENERATOR — ZERO-COLLISION ENGINE")
    print(" Rendering Perfectly Aligned 16:9 Screenshots for All 6 Analytics Pages")
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
