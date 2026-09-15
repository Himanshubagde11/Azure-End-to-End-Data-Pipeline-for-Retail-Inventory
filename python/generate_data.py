"""
CLARIVENS INVENTORY INTELLIGENCE
Data Generation Engine
Author: Himanshu Bagde (Azure Data Engineer & Cloud Analytics Architect)
Organization: CLARIVENS RETAIL GROUP

Generates realistic enterprise retail data for 2025 covering:
- 9 Categories, 1,200 Products
- 36 Stores across 9 Indian states and 12 key cities
- 60 Suppliers with realistic ratings and lead times
- 100,000+ Sales records across 12 monthly partitions with seasonal variation
- 36,000+ Weekly Inventory snapshots with realistic stock balance equations
- 10,000+ Purchase orders with fulfillment status
- 5,000+ Return records linked to sales
- Controlled 1.5% - 2.5% data quality defects for the validation framework
"""

import os
import random
import datetime
import json
import pandas as pd
import numpy as np

# Set random seed for deterministic generation
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
ANOMALY_LOG = []

def log_anomaly(table_name, record_id, column_name, original_value, injected_value, defect_type, description):
    ANOMALY_LOG.append({
        "table": table_name,
        "record_id": str(record_id),
        "column": column_name,
        "original_value": str(original_value),
        "injected_value": str(injected_value),
        "defect_type": defect_type,
        "description": description
    })

def generate_categories():
    print("[1/7] Generating Categories...")
    categories = [
        {"CategoryID": "CAT001", "CategoryName": "Electronics", "Department": "Technology"},
        {"CategoryID": "CAT002", "CategoryName": "Home Appliances", "Department": "Home"},
        {"CategoryID": "CAT003", "CategoryName": "Personal Care", "Department": "Health & Beauty"},
        {"CategoryID": "CAT004", "CategoryName": "Grocery", "Department": "Food & Essentials"},
        {"CategoryID": "CAT005", "CategoryName": "Beverages", "Department": "Food & Essentials"},
        {"CategoryID": "CAT006", "CategoryName": "Home & Kitchen", "Department": "Home"},
        {"CategoryID": "CAT007", "CategoryName": "Sports & Fitness", "Department": "Leisure"},
        {"CategoryID": "CAT008", "CategoryName": "Stationery", "Department": "Office & Education"},
        {"CategoryID": "CAT009", "CategoryName": "Fashion Accessories", "Department": "Apparel & Lifestyle"}
    ]
    df = pd.DataFrame(categories)
    path = os.path.join(DATA_DIR, "categories.csv")
    df.to_csv(path, index=False)
    print(f"  -> Created {path} ({len(df)} rows)")
    return df

def generate_stores():
    print("[2/7] Generating Stores...")
    # 36 stores across 9 states, 12 major cities
    locations = [
        # Maharashtra (West)
        {"City": "Mumbai", "State": "Maharashtra", "Region": "West", "Count": 6},
        {"City": "Pune", "State": "Maharashtra", "Region": "West", "Count": 4},
        {"City": "Nagpur", "State": "Maharashtra", "Region": "West", "Count": 2},
        {"City": "Nashik", "State": "Maharashtra", "Region": "West", "Count": 2},
        # Karnataka (South)
        {"City": "Bengaluru", "State": "Karnataka", "Region": "South", "Count": 6},
        # Gujarat (West)
        {"City": "Ahmedabad", "State": "Gujarat", "Region": "West", "Count": 3},
        # Telangana (South)
        {"City": "Hyderabad", "State": "Telangana", "Region": "South", "Count": 4},
        # Delhi (North)
        {"City": "Delhi", "State": "Delhi", "Region": "North", "Count": 4},
        # Tamil Nadu (South)
        {"City": "Chennai", "State": "Tamil Nadu", "Region": "South", "Count": 3},
        # West Bengal (East)
        {"City": "Kolkata", "State": "West Bengal", "Region": "East", "Count": 3},
        # Rajasthan (North)
        {"City": "Jaipur", "State": "Rajasthan", "Region": "North", "Count": 2},
        # Uttar Pradesh (North)
        {"City": "Lucknow", "State": "Uttar Pradesh", "Region": "North", "Count": 2},
    ]

    first_names = ["Aarav", "Rohan", "Vikram", "Neha", "Pooja", "Ananya", "Rahul", "Siddharth", "Priya", "Sunita", "Rajesh", "Karan", "Meera", "Amit", "Divya"]
    last_names = ["Sharma", "Verma", "Patel", "Mehta", "Iyer", "Nair", "Deshmukh", "Kulkarni", "Reddy", "Banerjee", "Gupta", "Singh", "Choudhury", "Joshi"]
    store_types = ["Flagship", "Hypermarket", "Supermarket", "Express"]
    type_weights = [0.15, 0.35, 0.35, 0.15]

    stores = []
    store_counter = 1
    for loc in locations:
        for i in range(loc["Count"]):
            store_id = f"STR{store_counter:03d}"
            stype = random.choices(store_types, weights=type_weights)[0]
            sqft = {
                "Flagship": random.randint(35000, 65000),
                "Hypermarket": random.randint(25000, 45000),
                "Supermarket": random.randint(12000, 24000),
                "Express": random.randint(4000, 9000)
            }[stype]
            
            mgr = f"{random.choice(first_names)} {random.choice(last_names)}"
            open_year = random.randint(2018, 2024)
            open_month = random.randint(1, 12)
            open_day = random.randint(1, 28)
            opening_date = f"{open_year}-{open_month:02d}-{open_day:02d}"

            stores.append({
                "StoreID": store_id,
                "StoreName": f"Clarivens {loc['City']} {stype} #{i+1}",
                "City": loc["City"],
                "State": loc["State"],
                "Region": loc["Region"],
                "StoreType": stype,
                "OpeningDate": opening_date,
                "Manager": mgr,
                "SquareFeet": sqft,
                "IsActive": 1
            })
            store_counter += 1

    df = pd.DataFrame(stores)
    path = os.path.join(DATA_DIR, "stores.csv")
    df.to_csv(path, index=False)
    print(f"  -> Created {path} ({len(df)} rows)")
    return df

def generate_suppliers():
    print("[3/7] Generating Suppliers...")
    supplier_names = [
        "Aura Consumer Brands", "Bharat Agri Produce", "Apex Electronics Ltd", "Vanguard Appliances",
        "Lotus Personal Care", "GreenLeaf Organics", "Himalayan Spring Beverages", "Sovereign Kitchenwares",
        "Velocity Sports Equipment", "Pronto Stationery Supplies", "Crown Fashion Goods", "Indus Valley Staples",
        "Zenith Audio & Tech", "BlueStar Home Comfort", "PureNature Botanicals", "SpiceRoute Trading Co",
        "Deccan Beverages Pvt Ltd", "Heritage Tableware", "Pulse Fitness Essentials", "Camlin Craft Works",
        "UrbanStyle Leather & Accessories", "Orient Digital Innovations", "Ganges Millers & Grains", "Sunlight Dairy & Foods",
        "Titan Consumer Electronics", "Prestige Household Appliances", "Hindustan Health & Beauty", "National Agro Consortium",
        "Pacific Refreshments Ltd", "Crest Homeware Industries", "Kavach Safety & Sports", "Navneet Educational Paper",
        "Elegance Lifestyle Goods", "Royal Spices & Condiments", "Cosmic Gadgets India", "Vedic Herbals & Care",
        "EverFresh Beverages", "Classic Cookware India", "Matrix Fitness Systems", "Saraswati Office Supplies",
        "Trendz Global Accessories", "Pinnacle Home Essentials", "Gourmet Foods Direct", "Quantum Microelectronics",
        "ThermaFlow Home Heating", "Aromas of India", "Nectar Juice & Beverage", "Sterling Kitchen Solutions",
        "IronGrip Gym Wear", "Pioneer Paper Co", "Glamour Touch Lifestyle", "AgroHarvest Staples",
        "SparkTech Mobiles", "CleanPro Appliances", "NaturalGlow Cosmetics", "TasteCraft Foods",
        "BrewMaster Coffee & Tea", "ChefCraft Cutlery", "Dynamic Athletics", "Signature Leather Craft"
    ]

    terms_options = ["Net 30", "Net 45", "Net 60", "2/10 Net 30"]
    cities = ["Mumbai", "Bengaluru", "Delhi", "Ahmedabad", "Chennai", "Pune", "Hyderabad", "Kolkata", "Jaipur", "Surat"]

    suppliers = []
    for idx, name in enumerate(supplier_names, start=1):
        sup_id = f"SUP{idx:03d}"
        city = random.choice(cities)
        lead_time = random.randint(3, 21)
        rating = round(random.uniform(3.2, 4.9), 2)
        payment_term = random.choice(terms_options)
        
        suppliers.append({
            "SupplierID": sup_id,
            "SupplierName": name,
            "ContactName": f"Contact for {name}",
            "Email": f"procurement@{name.lower().replace(' ', '').replace('&', 'and')[:14]}.in",
            "Phone": f"+91 {random.randint(70000, 99999)} {random.randint(10000, 99999)}",
            "City": city,
            "State": "Maharashtra" if city in ["Mumbai", "Pune"] else "Karnataka" if city == "Bengaluru" else "Delhi" if city == "Delhi" else "Gujarat" if city in ["Ahmedabad", "Surat"] else "Tamil Nadu" if city == "Chennai" else "Telangana" if city == "Hyderabad" else "West Bengal" if city == "Kolkata" else "Rajasthan",
            "Rating": rating,
            "PaymentTerms": payment_term,
            "LeadTimeDays": lead_time,
            "IsActive": 1
        })

    df = pd.DataFrame(suppliers)
    path = os.path.join(DATA_DIR, "suppliers.csv")
    df.to_csv(path, index=False)
    print(f"  -> Created {path} ({len(df)} rows)")
    return df

def generate_products(categories_df, suppliers_df):
    print("[4/7] Generating Products (1,200 rows)...")
    
    product_templates = {
        "Electronics": {
            "prefixes": ["UltraHD Smart LED TV", "Wireless Noise-Canceling Headphones", "Bluetooth Soundbar", "Portable Power Bank 20000mAh", "Gaming Mechanical Keyboard", "Ergonomic Wireless Mouse", "Smartwatch Fitness Tracker", "Fast USB-C Charging Hub", "4K Action Camera", "True Wireless Earbuds", "Wi-Fi 6 Dual-Band Router", "Tablet Stylus Pen", "Compact Bluetooth Speaker", "Noise Isolating Gaming Headset"],
            "brands": ["Sony", "Samsung", "boAt", "Noise", "Logitech", "Zebronics", "OnePlus", "Mi", "Boult", "JBL"],
            "cost_range": (350.0, 18500.0),
            "margin_range": (0.18, 0.35)
        },
        "Home Appliances": {
            "prefixes": ["Convection Microwave Oven", "Air Fryer Digital 4.5L", "Electric Kettle 1.8L", "Induction Cooktop 2000W", "Heavy Weight Dry Iron", "Hand Blender & Chopper", "Tower Air Cooler", "Steam Iron 1800W", "Pop-up 4-Slice Toaster", "Multi-Cooker Electric Pan", "Ionic Hair Dryer 2000W", "Garment Steamer Portable", "Vacuum Cleaner Handheld"],
            "brands": ["Philips", "Bajaj", "Prestige", "Havells", "Morphy Richards", "Usha", "Kent", "Crompton"],
            "cost_range": (450.0, 8200.0),
            "margin_range": (0.22, 0.40)
        },
        "Personal Care": {
            "prefixes": ["Hydrating Face Moisturizer 100ml", "Anti-Dandruff Shampoo 400ml", "Natural Brightening Serum 30ml", "Charcoal Face Wash 150ml", "Herbal Hair Growth Oil 200ml", "Broad Spectrum Sunscreen SPF50", "Gentle Body Wash 500ml", "Electric Shaver & Trimmer", "Bamboo Toothbrush Pack of 4", "Deep Cleansing Clay Mask", "Aloe Vera Calming Gel 250ml"],
            "brands": ["Mamaearth", "Nivea", "Himalaya", "The Derma Co", "Biotique", "Garnier", "Dove", "L'Oreal", "Beardo"],
            "cost_range": (80.0, 850.0),
            "margin_range": (0.30, 0.55)
        },
        "Grocery": {
            "prefixes": ["Organic Basmati Rice 5kg", "Pure Cold Pressed Mustard Oil 1L", "Whole Wheat Flour 10kg", "Kashmiri Red Chilli Powder 500g", "Roasted Almonds California 500g", "Organic Turmeric Powder 500g", "Raw Cashew Nuts Whole 500g", "Toor Dal Premium Unpolished 1kg", "Himalayan Pink Rock Salt 1kg", "Natural Honey Pure 500g", "Desi Cow Ghee Bilona 1L", "Oats Rolled Breakfast 1kg"],
            "brands": ["Tata Sampann", "Fortune", "Aashirvaad", "Daawat", "Catch", "Organic Tattva", "Saffola", "Patanjali"],
            "cost_range": (45.0, 950.0),
            "margin_range": (0.12, 0.25)
        },
        "Beverages": {
            "prefixes": ["Sparkling Natural Mineral Water 750ml", "Cold Pressed Mixed Fruit Juice 1L", "Green Tea Lemon Honey 100 Bags", "Premium Roasted Filter Coffee 500g", "Classic Indian Masala Chai 500g", "Isotonic Electrolyte Drink 500ml", "Alphonso Mango Pulp 850g", "Cold Brew Coffee Concentrate 300ml", "Herbal Infusion Chamomile Tea", "Energy Drink Sugar Free 250ml"],
            "brands": ["Tata Tea", "Bru", "Real", "Raw Pressery", "Red Bull", "Paper Boat", "Tetley", "Davidoff", "B-Fizz"],
            "cost_range": (25.0, 480.0),
            "margin_range": (0.25, 0.45)
        },
        "Home & Kitchen": {
            "prefixes": ["Hard Anodized Pressure Cooker 3L", "Triply Stainless Steel Kadhai 24cm", "Non-Stick Granite Frying Pan 26cm", "Airtight Glass Container Set of 4", "Stainless Steel Insulated Water Bottle 1L", "Rotating Spice Rack 16 Jars", "Bamboo Cutting Board Set", "Fine Bone China Dinner Set 24 Pcs", "Double Wall Coffee Mug Set of 2"],
            "brands": ["Prestige", "Hawkins", "Milton", "Borosil", "Cello", "Vinod", "Signoraware", "Wonderchef"],
            "cost_range": (150.0, 3200.0),
            "margin_range": (0.25, 0.45)
        },
        "Sports & Fitness": {
            "prefixes": ["Anti-Slip High Density Yoga Mat 8mm", "Hexagonal Rubber Dumbbells Pair 5kg", "Adjustable Hand Grip Strengthener", "Speed Jump Rope Aluminum Handle", "Resistance Loop Bands Set of 5", "Protein Shaker Bottle 700ml", "Gym Bag with Shoe Compartment", "Badminton Racket Carbon Fiber", "Cricket Bat English Willow Grade 2"],
            "brands": ["Decathlon", "Nivia", "Cosco", "Yonex", "Kobo", "Boldfit", "Strauss", "Vector X"],
            "cost_range": (120.0, 2400.0),
            "margin_range": (0.25, 0.45)
        },
        "Stationery": {
            "prefixes": ["Hardbound Ruled Executive Notebook A5", "Fine Tip Gel Pen Set Pack of 10", "Highlighter Pastel Colors Set of 6", "Scientific Calculator 417 Functions", "Heavy Duty Desktop Stapler", "Mechanical Pencil 0.7mm Set", "Sticky Notes Neon Pack of 5", "Expanding File Folder 12 Pockets"],
            "brands": ["Classmate", "Camlin", "Parker", "Casio", "Kangaro", "Luxor", "Doms", "Pilot"],
            "cost_range": (20.0, 650.0),
            "margin_range": (0.28, 0.50)
        },
        "Fashion Accessories": {
            "prefixes": ["Genuine Leather Bifold Wallet", "Classic Analog Stainless Steel Watch", "Polarized Aviator Sunglasses", "Reversible Formal Leather Belt", "Canvas Laptop Backpack 15.6 Inch", "Silk Touch Printed Neck Scarf", "RFID Blocking Travel Card Case", "Minimalist Chronograph Wristwatch"],
            "brands": ["Titan", "Fastrack", "Wildhorn", "Fastrack", "Fossil", "Lavie", "Baggit", "Lenskart", "Tommy Hilfiger"],
            "cost_range": (180.0, 4500.0),
            "margin_range": (0.35, 0.60)
        }
    }

    supplier_ids = suppliers_df["SupplierID"].tolist()
    products = []
    prod_id = 1
    
    # Generate ~133 products per category to reach 1,200 total
    for cat_idx, cat_row in categories_df.iterrows():
        cat_id = cat_row["CategoryID"]
        cat_name = cat_row["CategoryName"]
        config = product_templates[cat_name]
        
        for _ in range(134 if cat_name in ["Electronics", "Grocery", "Home & Kitchen"] else 133):
            prefix = random.choice(config["prefixes"])
            brand = random.choice(config["brands"])
            model_suffix = f"{random.choice(['Pro', 'Max', 'Plus', 'Elite', 'Prime', 'Select', 'Classic', 'Eco'])} {random.randint(100, 999)}"
            product_name = f"{brand} {prefix} {model_suffix}"
            
            unit_cost = round(random.uniform(config["cost_range"][0], config["cost_range"][1]), 2)
            margin = random.uniform(config["margin_range"][0], config["margin_range"][1])
            unit_price = round(unit_cost / (1.0 - margin), 2)
            
            # Reorder levels based on cost
            if unit_cost > 3000:
                reorder_level = random.randint(10, 30)
                reorder_qty = random.randint(25, 75)
            elif unit_cost > 500:
                reorder_level = random.randint(25, 60)
                reorder_qty = random.randint(75, 180)
            else:
                reorder_level = random.randint(60, 150)
                reorder_qty = random.randint(150, 400)

            launch_year = random.randint(2021, 2024)
            launch_month = random.randint(1, 12)
            launch_day = random.randint(1, 28)
            launch_date = f"{launch_year}-{launch_month:02d}-{launch_day:02d}"

            supplier_id = random.choice(supplier_ids)

            products.append({
                "ProductID": f"PRD{prod_id:05d}",
                "ProductName": product_name,
                "CategoryID": cat_id,
                "CategoryName": cat_name,
                "SupplierID": supplier_id,
                "Brand": brand,
                "UnitCost": unit_cost,
                "UnitPrice": unit_price,
                "ReorderLevel": reorder_level,
                "ReorderQuantity": reorder_qty,
                "LaunchDate": launch_date,
                "IsActive": 1
            })
            prod_id += 1

    df = pd.DataFrame(products)

    # Incur controlled 1.5% defects in products
    # 1. Inconsistent CategoryName (e.g., 'electronic', 'ELECTR', 'Beverage' instead of Beverages)
    for idx in random.sample(range(len(df)), 12):
        orig = df.at[idx, "CategoryName"]
        corrupted = orig.lower() if random.random() > 0.5 else orig.upper()[:6]
        df.at[idx, "CategoryName"] = corrupted
        log_anomaly("products", df.at[idx, "ProductID"], "CategoryName", orig, corrupted, "INCONSISTENT_CATEGORY", "Inconsistent category casing/abbreviation")

    # 2. Missing/Null UnitPrice
    for idx in random.sample(range(len(df)), 8):
        orig = df.at[idx, "UnitPrice"]
        df.at[idx, "UnitPrice"] = np.nan
        log_anomaly("products", df.at[idx, "ProductID"], "UnitPrice", orig, "NULL", "NULL_PRICE", "Null unit price on active product")

    # 3. Invalid SupplierID (referential integrity defect)
    for idx in random.sample(range(len(df)), 6):
        orig = df.at[idx, "SupplierID"]
        df.at[idx, "SupplierID"] = "SUP999"
        log_anomaly("products", df.at[idx, "ProductID"], "SupplierID", orig, "SUP999", "INVALID_SUPPLIER_FK", "Referenced non-existent supplier key")

    path = os.path.join(DATA_DIR, "products.csv")
    df.to_csv(path, index=False)
    print(f"  -> Created {path} ({len(df)} rows)")
    return df

def generate_sales(stores_df, products_df):
    print("[5/7] Generating Sales (100,000+ rows across 12 months)...")
    
    # Pre-index valid product info
    valid_products = products_df.dropna(subset=["UnitPrice"]).copy()
    product_pool = valid_products.to_dict(orient="records")
    store_pool = stores_df.to_dict(orient="records")

    store_type_multiplier = {
        "Flagship": 1.6,
        "Hypermarket": 1.3,
        "Supermarket": 0.9,
        "Express": 0.5
    }

    category_seasonality = {
        # Month: {Category: Multiplier}
        # Summer (Apr-Jun): Beverages & Cooling Appliances spike
        4: {"Beverages": 1.65, "Home Appliances": 1.35},
        5: {"Beverages": 1.85, "Home Appliances": 1.45},
        6: {"Beverages": 1.60, "Home Appliances": 1.25},
        # Festival Season (Oct-Nov): Electronics, Grocery, Home & Kitchen, Fashion Accessories spike
        10: {"Electronics": 1.60, "Grocery": 1.55, "Home & Kitchen": 1.50, "Fashion Accessories": 1.45},
        11: {"Electronics": 1.75, "Grocery": 1.65, "Home & Kitchen": 1.55, "Fashion Accessories": 1.60},
        # Year-end (Dec): Electronics, Fitness, Grocery
        12: {"Electronics": 1.50, "Sports & Fitness": 1.40, "Grocery": 1.35}
    }

    customer_segments = ["Regular", "Walk-in", "Premium", "Corporate"]
    segment_weights = [0.45, 0.35, 0.15, 0.05]
    payment_methods = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]
    payment_weights = [0.45, 0.25, 0.15, 0.10, 0.05]

    total_sales_generated = 0
    sale_global_counter = 1
    
    # Store sales in monthly chunks
    for month in range(1, 13):
        month_str = f"{month:02d}"
        days_in_month = 28 if month == 2 else 30 if month in [4, 6, 9, 11] else 31
        # Target ~8,500 - 11,000 sales per month to reach 115,000 total
        month_target = random.randint(8600, 11500)
        
        records = []
        for _ in range(month_target):
            day = random.randint(1, days_in_month)
            sale_date = f"2025-{month_str}-{day:02d}"
            
            store = random.choice(store_pool)
            product = random.choice(product_pool)
            cat_name = product["CategoryName"]
            
            # Apply seasonality & store type weighting
            season_mult = category_seasonality.get(month, {}).get(cat_name, 1.0)
            store_mult = store_type_multiplier.get(store["StoreType"], 1.0)
            
            # Quantity purchased
            if cat_name in ["Grocery", "Beverages", "Stationery"]:
                qty = random.choices([1, 2, 3, 4, 5, 6, 10], weights=[0.40, 0.25, 0.15, 0.10, 0.05, 0.03, 0.02])[0]
            elif cat_name in ["Electronics", "Home Appliances"]:
                qty = random.choices([1, 2, 3], weights=[0.85, 0.12, 0.03])[0]
            else:
                qty = random.choices([1, 2, 3, 4], weights=[0.60, 0.25, 0.10, 0.05])[0]

            unit_price = float(product["UnitPrice"])
            unit_cost = float(product["UnitCost"])
            
            # Discount (higher during festivals)
            if month in [10, 11, 12] and random.random() < 0.40:
                discount = round(random.choice([0.05, 0.10, 0.15, 0.20]), 2)
            elif random.random() < 0.20:
                discount = round(random.choice([0.05, 0.10]), 2)
            else:
                discount = 0.0
                
            revenue = round(qty * unit_price * (1.0 - discount), 2)
            cost = round(qty * unit_cost, 2)
            
            sale_id = f"SAL2025{sale_global_counter:07d}"
            sale_global_counter += 1

            records.append({
                "SaleID": sale_id,
                "SaleDate": sale_date,
                "StoreID": store["StoreID"],
                "ProductID": product["ProductID"],
                "Quantity": qty,
                "UnitPrice": unit_price,
                "Discount": discount,
                "Revenue": revenue,
                "Cost": cost,
                "PaymentMethod": random.choices(payment_methods, weights=payment_weights)[0],
                "CustomerSegment": random.choices(customer_segments, weights=segment_weights)[0]
            })

        month_df = pd.DataFrame(records)

        # Inject controlled 1.5% defects per monthly file
        # A. Null ProductID (e.g. 15 per month = 180 total)
        for idx in random.sample(range(len(month_df)), 15):
            orig = month_df.at[idx, "ProductID"]
            month_df.at[idx, "ProductID"] = np.nan
            log_anomaly("sales", month_df.at[idx, "SaleID"], "ProductID", orig, "NULL", "NULL_PRODUCT_FK", "Missing ProductID in sale record")

        # B. Null StoreID (e.g. 10 per month = 120 total)
        for idx in random.sample(range(len(month_df)), 10):
            orig = month_df.at[idx, "StoreID"]
            month_df.at[idx, "StoreID"] = np.nan
            log_anomaly("sales", month_df.at[idx, "SaleID"], "StoreID", orig, "NULL", "NULL_STORE_FK", "Missing StoreID in sale record")

        # C. Negative Quantity (e.g. 8 per month = 96 total)
        for idx in random.sample(range(len(month_df)), 8):
            orig = month_df.at[idx, "Quantity"]
            corrupted = -abs(orig)
            month_df.at[idx, "Quantity"] = corrupted
            month_df.at[idx, "Revenue"] = round(corrupted * month_df.at[idx, "UnitPrice"] * (1 - month_df.at[idx, "Discount"]), 2)
            log_anomaly("sales", month_df.at[idx, "SaleID"], "Quantity", orig, corrupted, "NEGATIVE_QUANTITY", "Negative sales quantity transaction")

        # D. Invalid / Future Dates (e.g. 6 per month = 72 total)
        for idx in random.sample(range(len(month_df)), 6):
            orig = month_df.at[idx, "SaleDate"]
            corrupted = "2026-05-15" if random.random() > 0.5 else "2025-02-30"  # Impossible date
            month_df.at[idx, "SaleDate"] = corrupted
            log_anomaly("sales", month_df.at[idx, "SaleID"], "SaleDate", orig, corrupted, "INVALID_SALE_DATE", "Future or impossible calendar sale date")

        # E. Duplicate SaleID (e.g. 15 per month = 180 total)
        dup_indices = random.sample(range(len(month_df)), 15)
        target_indices = random.sample(range(len(month_df)), 15)
        for d_idx, t_idx in zip(dup_indices, target_indices):
            if d_idx != t_idx:
                orig = month_df.at[d_idx, "SaleID"]
                dup_val = month_df.at[t_idx, "SaleID"]
                month_df.at[d_idx, "SaleID"] = dup_val
                log_anomaly("sales", dup_val, "SaleID", orig, dup_val, "DUPLICATE_SALE_KEY", "Duplicate transaction primary key")

        file_path = os.path.join(DATA_DIR, "sales", f"sales_2025_{month_str}.csv")
        month_df.to_csv(file_path, index=False)
        total_sales_generated += len(month_df)
        print(f"  -> Created {file_path} ({len(month_df)} rows)")

    print(f"  -> Total Sales generated: {total_sales_generated:,} rows")
    return total_sales_generated

def generate_inventory(stores_df, products_df):
    print("[6/7] Generating Weekly Inventory Snapshots (36,000+ rows)...")
    # 52 weekly snapshot dates throughout 2025
    start_date = datetime.date(2025, 1, 5) # First Sunday of 2025
    snapshot_dates = [start_date + datetime.timedelta(weeks=w) for w in range(52)]
    
    store_ids = stores_df["StoreID"].tolist()
    # Sample 750 high-velocity products per store for inventory snapshots
    active_products = products_df.to_dict(orient="records")

    inv_id_counter = 1
    total_inventory_rows = 0

    # Group snapshots by month
    snapshots_by_month = {}
    for d in snapshot_dates:
        m = d.month
        snapshots_by_month.setdefault(m, []).append(d)

    for month, dates in snapshots_by_month.items():
        month_records = []
        month_str = f"{month:02d}"

        for s_date in dates:
            s_date_str = s_date.strftime("%Y-%m-%d")
            # Select stores and products
            for store_id in store_ids:
                # Sample 20 products per store per week to yield ~36 stores * 20 products * 52 weeks = 37,440 rows
                selected_prods = random.sample(active_products, 20)
                for prod in selected_prods:
                    reorder_lvl = prod["ReorderLevel"]
                    reorder_qty = prod["ReorderQuantity"]
                    unit_cost = float(prod["UnitCost"]) if not pd.isna(prod["UnitCost"]) else 250.0

                    # Simulate realistic weekly flow
                    opening = random.randint(int(reorder_lvl * 0.5), int(reorder_lvl * 3.5))
                    sold = random.randint(5, max(8, int(opening * 0.6)))
                    
                    # Replenishment if opening was low
                    received = reorder_qty if opening < reorder_lvl else (reorder_qty if random.random() < 0.25 else 0)
                    returns = random.choices([0, 1, 2, 3], weights=[0.82, 0.12, 0.04, 0.02])[0]
                    damaged = random.choices([0, 1, 2], weights=[0.90, 0.08, 0.02])[0]
                    
                    # Mathematical balance equation
                    closing = opening + received - sold + returns - damaged
                    if closing < 0:
                        closing = 0
                    
                    inv_value = round(closing * unit_cost, 2)
                    inv_id = f"INV{inv_id_counter:08d}"
                    inv_id_counter += 1

                    month_records.append({
                        "InventoryID": inv_id,
                        "SnapshotDate": s_date_str,
                        "StoreID": store_id,
                        "ProductID": prod["ProductID"],
                        "OpeningStock": opening,
                        "ReceivedQuantity": received,
                        "SoldQuantity": sold,
                        "ReturnQuantity": returns,
                        "ClosingStock": closing,
                        "DamagedQuantity": damaged,
                        "InventoryValue": inv_value
                    })

        df_month = pd.DataFrame(month_records)

        # Inject controlled defects in inventory (1.5%)
        # 1. Broken mathematical balance equation: closing != opening + received - sold + returns - damaged
        for idx in random.sample(range(len(df_month)), 15):
            orig = df_month.at[idx, "ClosingStock"]
            corrupted = orig + random.choice([50, 100, -30])
            df_month.at[idx, "ClosingStock"] = corrupted
            log_anomaly("inventory", df_month.at[idx, "InventoryID"], "ClosingStock", orig, corrupted, "BROKEN_INVENTORY_EQUATION", "ClosingStock violates stock balance equation")

        # 2. Negative Closing Stock
        for idx in random.sample(range(len(df_month)), 8):
            orig = df_month.at[idx, "ClosingStock"]
            corrupted = -abs(random.randint(5, 25))
            df_month.at[idx, "ClosingStock"] = corrupted
            log_anomaly("inventory", df_month.at[idx, "InventoryID"], "ClosingStock", orig, corrupted, "NEGATIVE_CLOSING_STOCK", "Negative inventory closing quantity")

        # 3. Impossible Inventory Value
        for idx in random.sample(range(len(df_month)), 6):
            orig = df_month.at[idx, "InventoryValue"]
            corrupted = -9999.0
            df_month.at[idx, "InventoryValue"] = corrupted
            log_anomaly("inventory", df_month.at[idx, "InventoryID"], "InventoryValue", orig, corrupted, "NEGATIVE_INVENTORY_VALUE", "Impossible negative monetary inventory valuation")

        file_path = os.path.join(DATA_DIR, "inventory", f"inventory_2025_{month_str}.csv")
        df_month.to_csv(file_path, index=False)
        total_inventory_rows += len(df_month)
        print(f"  -> Created {file_path} ({len(df_month)} rows)")

    print(f"  -> Total Inventory Snapshots generated: {total_inventory_rows:,} rows")
    return total_inventory_rows

def generate_purchases_and_returns(stores_df, products_df, suppliers_df):
    print("[7/7] Generating Purchase Orders (10,000+ rows) & Returns (5,000+ rows)...")
    
    # 1. Purchase Orders
    supplier_pool = suppliers_df.to_dict(orient="records")
    store_ids = stores_df["StoreID"].tolist()
    product_pool = products_df.dropna(subset=["UnitCost"]).to_dict(orient="records")

    purchases = []
    po_counter = 1
    start_date = datetime.date(2025, 1, 1)

    for i in range(10500):
        order_day_offset = random.randint(0, 360)
        order_date = start_date + datetime.timedelta(days=order_day_offset)
        
        supplier = random.choice(supplier_pool)
        store_id = random.choice(store_ids)
        product = random.choice(product_pool)
        
        ordered_qty = product["ReorderQuantity"]
        lead_time = supplier["LeadTimeDays"]
        expected_delivery = order_date + datetime.timedelta(days=lead_time)
        
        # Delivery status
        status_roll = random.random()
        if order_day_offset > 345:
            status = "In-Transit"
            received_qty = 0
            actual_delivery = None
        elif status_roll < 0.04:
            status = "Cancelled"
            received_qty = 0
            actual_delivery = None
        elif status_roll < 0.20:
            status = "Delayed"
            delay_days = random.randint(3, 14)
            actual_delivery = expected_delivery + datetime.timedelta(days=delay_days)
            received_qty = ordered_qty if random.random() > 0.1 else ordered_qty - random.randint(2, 10)
        else:
            status = "Completed"
            actual_delivery = expected_delivery + datetime.timedelta(days=random.choice([-2, -1, 0, 1]))
            received_qty = ordered_qty

        unit_cost = float(product["UnitCost"])
        po_id = f"PO2025{po_counter:06d}"
        po_counter += 1

        purchases.append({
            "PurchaseOrderID": po_id,
            "OrderDate": order_date.strftime("%Y-%m-%d"),
            "SupplierID": supplier["SupplierID"],
            "StoreID": store_id,
            "ProductID": product["ProductID"],
            "OrderedQuantity": ordered_qty,
            "ReceivedQuantity": received_qty,
            "UnitCost": unit_cost,
            "ExpectedDeliveryDate": expected_delivery.strftime("%Y-%m-%d"),
            "ActualDeliveryDate": actual_delivery.strftime("%Y-%m-%d") if actual_delivery else "",
            "Status": status
        })

    po_df = pd.DataFrame(purchases)

    # Inject controlled defects in purchases (1.5%)
    # 1. ReceivedQuantity > OrderedQuantity by unreasonable factor
    for idx in random.sample(range(len(po_df)), 35):
        orig = po_df.at[idx, "ReceivedQuantity"]
        corrupted = po_df.at[idx, "OrderedQuantity"] * 5
        po_df.at[idx, "ReceivedQuantity"] = corrupted
        log_anomaly("purchases", po_df.at[idx, "PurchaseOrderID"], "ReceivedQuantity", orig, corrupted, "EXCESSIVE_RECEIVED_QTY", "Received quantity exceeded ordered by 5x")

    # 2. ActualDeliveryDate earlier than OrderDate
    for idx in random.sample(range(len(po_df)), 25):
        orig = po_df.at[idx, "ActualDeliveryDate"]
        o_date = datetime.datetime.strptime(po_df.at[idx, "OrderDate"], "%Y-%m-%d")
        corrupted = (o_date - datetime.timedelta(days=15)).strftime("%Y-%m-%d")
        po_df.at[idx, "ActualDeliveryDate"] = corrupted
        log_anomaly("purchases", po_df.at[idx, "PurchaseOrderID"], "ActualDeliveryDate", orig, corrupted, "DELIVERY_BEFORE_ORDER", "Delivery date precedes order placement date")

    po_path = os.path.join(DATA_DIR, "purchases", "purchase_orders.csv")
    po_df.to_csv(po_path, index=False)
    print(f"  -> Created {po_path} ({len(po_df)} rows)")

    # 2. Returns (5,200 rows)
    return_reasons = [
        "Defective Item",
        "Wrong Item Delivered",
        "Size/Fit Issue",
        "Customer Changed Mind",
        "Damaged in Transit"
    ]
    reason_weights = [0.35, 0.20, 0.20, 0.15, 0.10]

    returns = []
    for ret_idx in range(1, 5250):
        ret_day_offset = random.randint(5, 364)
        ret_date = start_date + datetime.timedelta(days=ret_day_offset)
        store_id = random.choice(store_ids)
        product = random.choice(product_pool)
        
        # Link to a realistic sale ID
        sale_sample_id = f"SAL2025{random.randint(1, 100000):07d}"
        qty = random.choices([1, 2, 3], weights=[0.85, 0.12, 0.03])[0]
        unit_price = float(product["UnitPrice"]) if not pd.isna(product["UnitPrice"]) else 500.0
        refund_amount = round(qty * unit_price, 2)

        returns.append({
            "ReturnID": f"RET2025{ret_idx:06d}",
            "ReturnDate": ret_date.strftime("%Y-%m-%d"),
            "SaleID": sale_sample_id,
            "StoreID": store_id,
            "ProductID": product["ProductID"],
            "Quantity": qty,
            "ReturnReason": random.choices(return_reasons, weights=reason_weights)[0],
            "RefundAmount": refund_amount
        })

    ret_df = pd.DataFrame(returns)

    # Inject controlled defects in returns (1.5%)
    # Negative RefundAmount
    for idx in random.sample(range(len(ret_df)), 30):
        orig = ret_df.at[idx, "RefundAmount"]
        corrupted = -abs(orig)
        ret_df.at[idx, "RefundAmount"] = corrupted
        log_anomaly("returns", ret_df.at[idx, "ReturnID"], "RefundAmount", orig, corrupted, "NEGATIVE_REFUND_AMOUNT", "Negative customer refund amount")

    ret_path = os.path.join(DATA_DIR, "returns", "returns.csv")
    ret_df.to_csv(ret_path, index=False)
    print(f"  -> Created {ret_path} ({len(ret_df)} rows)")

    # Save complete anomaly tracking manifest
    anomaly_path = os.path.join(DATA_DIR, "injected_anomalies_log.json")
    with open(anomaly_path, "w") as f:
        json.dump(ANOMALY_LOG, f, indent=2)
    print(f"  -> Injected Anomalies Log saved to {anomaly_path} ({len(ANOMALY_LOG)} total anomalies documented)")

def main():
    print("=================================================================")
    print(" CLARIVENS INVENTORY INTELLIGENCE — DATA GENERATION ENGINE")
    print(" CLARIVENS RETAIL GROUP — Enterprise Retail Data Platform")
    print("=================================================================")
    cats_df = generate_categories()
    stores_df = generate_stores()
    suppliers_df = generate_suppliers()
    prods_df = generate_products(cats_df, suppliers_df)
    generate_sales(stores_df, prods_df)
    generate_inventory(stores_df, prods_df)
    generate_purchases_and_returns(stores_df, prods_df, suppliers_df)
    print("=================================================================")
    print(" Data Generation Complete! All CSV files created successfully.")
    print("=================================================================")

if __name__ == "__main__":
    main()
