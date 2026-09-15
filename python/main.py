"""
CLARIVENS INVENTORY INTELLIGENCE
CLI Entrypoint for Data Validation & Quality Framework
Author: Senior Data Engineer / Azure Data Architect
Organization: CLARIVENS RETAIL GROUP
"""

import sys
import argparse
import os
import glob
import pandas as pd

from config import DATA_DIR, SALES_DIR, INVENTORY_DIR, PURCHASES_DIR, RETURNS_DIR
from data_quality import DataQualityEngine
from pipeline_validator import run_pipeline_validation
from mock_api import export_enrichment_snapshot

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Clarivens Inventory Intelligence — Data Quality & Pipeline Validation Framework"
    )
    parser.add_argument(
        "--check-all",
        action="store_true",
        help="Run comprehensive validation suite across all staging files and entities"
    )
    parser.add_argument(
        "--table",
        type=str,
        choices=["categories", "stores", "suppliers", "products", "sales", "inventory", "purchases", "returns"],
        help="Validate a single target table"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Custom CSV file path to validate against target table schema"
    )
    parser.add_argument(
        "--export-api",
        action="store_true",
        help="Export mock REST API catalog & replenishment enrichment feed"
    )
    return parser.parse_args()

def main():
    args = parse_arguments()

    print("==========================================================================")
    print(" CLARIVENS INVENTORY INTELLIGENCE — DATA QUALITY ENGINE")
    print(" CLARIVENS RETAIL GROUP — Enterprise Retail Data Platform")
    print("==========================================================================")

    if args.export_api:
        print("[ACTION] Exporting REST API Enrichment Snapshot...")
        export_enrichment_snapshot()
        return

    if args.table:
        print(f"[ACTION] Running validation on target table: {args.table}")
        engine = DataQualityEngine()
        
        # Load reference lookups
        ref_lookups = {}
        for ref_name, filename in [("products", "products.csv"), ("stores", "stores.csv"), ("suppliers", "suppliers.csv"), ("categories", "categories.csv")]:
            p = os.path.join(DATA_DIR, filename)
            if os.path.exists(p):
                ref_lookups[ref_name] = pd.read_csv(p)

        target_file = args.file
        if not target_file:
            if args.table in ["categories", "stores", "suppliers", "products"]:
                target_file = os.path.join(DATA_DIR, f"{args.table}.csv")
            elif args.table == "sales":
                # Take first month or combined
                files = sorted(glob.glob(os.path.join(SALES_DIR, "*.csv")))
                target_file = files[0] if files else None
            elif args.table == "inventory":
                files = sorted(glob.glob(os.path.join(INVENTORY_DIR, "*.csv")))
                target_file = files[0] if files else None
            elif args.table == "purchases":
                target_file = os.path.join(PURCHASES_DIR, "purchase_orders.csv")
            elif args.table == "returns":
                target_file = os.path.join(RETURNS_DIR, "returns.csv")

        if not target_file or not os.path.exists(target_file):
            print(f"[ERROR] Target file not found for table '{args.table}'. Please check data directory.")
            sys.exit(1)

        print(f"[INFO] Reading dataset from: {target_file}")
        df = pd.read_csv(target_file)
        engine.evaluate_dataset(args.table, df, ref_lookups)
        engine.print_report()
        export_path = engine.export_report()
        print(f"[SUCCESS] Audit report saved: {export_path}")
        return

    # Default to running comprehensive validation
    print("[ACTION] Running comprehensive pipeline validation across all staging entities...")
    summary = run_pipeline_validation()
    print(f"[COMPLETED] Validation finished with Data Quality Score: {summary['data_quality_score']}%")

if __name__ == "__main__":
    main()
