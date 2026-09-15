"""
CLARIVENS INVENTORY INTELLIGENCE
Module: pipeline_validator.py
Description: Pipeline integration runner designed for Azure Data Factory Batch/Custom Activity or local orchestration
Author: Senior Data Engineer / Azure Data Architect
Organization: CLARIVENS RETAIL GROUP
"""

import os
import glob
import pandas as pd
from typing import Dict, Any

from config import DATA_DIR, SALES_DIR, INVENTORY_DIR, PURCHASES_DIR, RETURNS_DIR
from data_quality import DataQualityEngine

def run_pipeline_validation(run_id: str = None, fail_on_critical: bool = False) -> Dict[str, Any]:
    """
    Orchestrates validation across all ingested staging datasets.
    """
    engine = DataQualityEngine(run_id=run_id)

    # 1. Load reference datasets for referential integrity checks
    ref_lookups = {}
    cats_path = os.path.join(DATA_DIR, "categories.csv")
    stores_path = os.path.join(DATA_DIR, "stores.csv")
    sups_path = os.path.join(DATA_DIR, "suppliers.csv")
    prods_path = os.path.join(DATA_DIR, "products.csv")

    if os.path.exists(cats_path):
        ref_lookups["categories"] = pd.read_csv(cats_path)
    if os.path.exists(stores_path):
        ref_lookups["stores"] = pd.read_csv(stores_path)
    if os.path.exists(sups_path):
        ref_lookups["suppliers"] = pd.read_csv(sups_path)
    if os.path.exists(prods_path):
        ref_lookups["products"] = pd.read_csv(prods_path)

    # 2. Evaluate Reference Master Tables
    for name, path in [("categories", cats_path), ("stores", stores_path), ("suppliers", sups_path), ("products", prods_path)]:
        if os.path.exists(path):
            df = pd.read_csv(path)
            engine.evaluate_dataset(name, df, ref_lookups)

    # 3. Evaluate Sales (Combining sample or all monthly files)
    sales_files = sorted(glob.glob(os.path.join(SALES_DIR, "*.csv")))
    if sales_files:
        # Evaluate representative chunks across 2025
        sales_dfs = [pd.read_csv(f) for f in sales_files]
        combined_sales = pd.concat(sales_dfs, ignore_index=True)
        engine.evaluate_dataset("sales", combined_sales, ref_lookups)

    # 4. Evaluate Inventory Snapshots
    inv_files = sorted(glob.glob(os.path.join(INVENTORY_DIR, "*.csv")))
    if inv_files:
        inv_dfs = [pd.read_csv(f) for f in inv_files]
        combined_inv = pd.concat(inv_dfs, ignore_index=True)
        engine.evaluate_dataset("inventory", combined_inv, ref_lookups)

    # 5. Evaluate Purchases & Returns
    po_path = os.path.join(PURCHASES_DIR, "purchase_orders.csv")
    if os.path.exists(po_path):
        df_po = pd.read_csv(po_path)
        engine.evaluate_dataset("purchases", df_po, ref_lookups)

    ret_path = os.path.join(RETURNS_DIR, "returns.csv")
    if os.path.exists(ret_path):
        df_ret = pd.read_csv(ret_path)
        engine.evaluate_dataset("returns", df_ret, ref_lookups)

    # Print summary & export audit report
    engine.print_report()
    log_file = engine.export_report()
    print(f"[AUDIT] Detailed Data Quality JSON Log exported to: {log_file}")

    summary = engine.compute_summary()
    if fail_on_critical and summary["overall_status"] == "FAIL":
        raise ValueError(f"Pipeline Data Quality Gate Failed with score {summary['data_quality_score']}%")

    return summary

if __name__ == "__main__":
    run_pipeline_validation()
