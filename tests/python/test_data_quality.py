"""
NEXORA INVENTORY INTELLIGENCE
Test Suite: test_data_quality.py
Description: Pytest and unittest test cases for modular Python Data Quality Framework
Author: Senior Data Engineer / Azure Data Architect
Organization: NEXORA RETAIL GROUP
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add root and python directories to path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
python_dir = os.path.join(BASE_DIR, "python")
if python_dir not in sys.path:
    sys.path.insert(0, python_dir)

from python.schema_validator import SchemaValidator
from python.null_validator import NullValidator
from python.duplicate_validator import DuplicateValidator
from python.business_rule_validator import BusinessRuleValidator
from python.data_quality import DataQualityEngine

class TestDataQualityFramework(unittest.TestCase):

    def setUp(self):
        # Clean sample dataframe
        self.clean_sales = pd.DataFrame([
            {"SaleID": "SAL001", "SaleDate": "2025-05-10", "StoreID": "STR001", "ProductID": "PRD00001", "Quantity": 2, "UnitPrice": 100.0, "Discount": 0.0, "Revenue": 200.0, "Cost": 150.0, "PaymentMethod": "UPI", "CustomerSegment": "Regular"},
            {"SaleID": "SAL002", "SaleDate": "2025-05-11", "StoreID": "STR001", "ProductID": "PRD00002", "Quantity": 1, "UnitPrice": 500.0, "Discount": 0.1, "Revenue": 450.0, "Cost": 350.0, "PaymentMethod": "Credit Card", "CustomerSegment": "Premium"}
        ])

        # Corrupted sample dataframe
        self.dirty_sales = pd.DataFrame([
            {"SaleID": "SAL001", "SaleDate": "2025-05-10", "StoreID": "STR001", "ProductID": "PRD00001", "Quantity": 2, "UnitPrice": 100.0, "Discount": 0.0, "Revenue": 200.0, "Cost": 150.0, "PaymentMethod": "UPI", "CustomerSegment": "Regular"},
            {"SaleID": "SAL001", "SaleDate": "2026-05-11", "StoreID": None, "ProductID": None, "Quantity": -5, "UnitPrice": -50.0, "Discount": 0.0, "Revenue": 9999.0, "Cost": 100.0, "PaymentMethod": "Cash", "CustomerSegment": "Walk-in"}
        ])

        self.ref_lookups = {
            "products": pd.DataFrame([{"ProductID": "PRD00001"}, {"ProductID": "PRD00002"}]),
            "stores": pd.DataFrame([{"StoreID": "STR001"}])
        }

    def test_schema_validator_clean(self):
        schema_cfg = {"columns": ["SaleID", "SaleDate", "StoreID", "ProductID", "Quantity", "UnitPrice", "Discount", "Revenue", "Cost", "PaymentMethod", "CustomerSegment"]}
        val = SchemaValidator("sales", schema_cfg)
        res = val.validate(self.clean_sales)
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["failed_records"], 0)
        self.assertEqual(res["pass_percentage"], 100.0)

    def test_schema_validator_missing_column(self):
        schema_cfg = {"columns": ["SaleID", "NonExistentColumn"]}
        val = SchemaValidator("sales", schema_cfg)
        res = val.validate(self.clean_sales)
        self.assertEqual(res["status"], "FAIL")
        self.assertIn("Missing required columns", res["error_message"])

    def test_null_validator_clean_and_dirty(self):
        val = NullValidator("sales", ["ProductID", "StoreID"])
        clean_res = val.validate(self.clean_sales)
        for r in clean_res:
            self.assertEqual(r["status"], "PASS")
            self.assertEqual(r["failed_records"], 0)

        dirty_res = val.validate(self.dirty_sales)
        failed_rules = [r for r in dirty_res if r["failed_records"] > 0]
        self.assertEqual(len(failed_rules), 2)
        self.assertEqual(failed_rules[0]["failed_records"], 1)

    def test_duplicate_validator(self):
        dup_val = DuplicateValidator("sales", ["SaleID"])
        clean_res = dup_val.validate(self.clean_sales)
        self.assertEqual(clean_res["failed_records"], 0)
        self.assertEqual(clean_res["status"], "PASS")

        dirty_res = dup_val.validate(self.dirty_sales)
        self.assertEqual(dirty_res["failed_records"], 1)

    def test_business_rules_sales_math_and_dates(self):
        biz_val = BusinessRuleValidator("sales", self.ref_lookups)
        results = biz_val.validate(self.dirty_sales)
        results_by_rule = {r["rule_name"]: r for r in results}

        # Quantity > 0 rule caught negative qty
        self.assertEqual(results_by_rule["Rule_Positive_Sales_Quantity"]["failed_records"], 1)
        # UnitPrice >= 0 rule caught negative price
        self.assertEqual(results_by_rule["Rule_Non_Negative_UnitPrice"]["failed_records"], 1)
        # Revenue equation integrity caught mathematical mismatch
        self.assertEqual(results_by_rule["Rule_Revenue_Equation_Integrity"]["failed_records"], 1)
        # Calendar date validation caught future date 2026-05-11
        self.assertEqual(results_by_rule["Rule_Valid_Calendar_SaleDate"]["failed_records"], 1)
        # Referential integrity caught null ProductID
        self.assertEqual(results_by_rule["Rule_Referential_Integrity_ProductID"]["failed_records"], 1)

    def test_inventory_balance_equation(self):
        inv_data = pd.DataFrame([
            {"InventoryID": "INV001", "OpeningStock": 100, "ReceivedQuantity": 50, "SoldQuantity": 30, "ReturnQuantity": 2, "DamagedQuantity": 1, "ClosingStock": 121, "InventoryValue": 5000.0}, # Correct: 100+50-30+2-1 = 121
            {"InventoryID": "INV002", "OpeningStock": 100, "ReceivedQuantity": 50, "SoldQuantity": 30, "ReturnQuantity": 2, "DamagedQuantity": 1, "ClosingStock": 999, "InventoryValue": -100.0} # Incorrect ClosingStock and Negative Value
        ])
        biz_val = BusinessRuleValidator("inventory")
        results = biz_val.validate(inv_data)
        results_by_rule = {r["rule_name"]: r for r in results}

        self.assertEqual(results_by_rule["Rule_Inventory_Balance_Equation"]["failed_records"], 1)
        self.assertEqual(results_by_rule["Rule_Non_Negative_InventoryValue"]["failed_records"], 1)

    def test_data_quality_engine_score_aggregation(self):
        engine = DataQualityEngine(run_id="TEST_RUN_001")
        engine.evaluate_dataset("sales", self.clean_sales, self.ref_lookups)
        summary = engine.compute_summary()
        self.assertEqual(summary["overall_status"], "PASS")
        self.assertEqual(summary["data_quality_score"], 100.0)

if __name__ == "__main__":
    unittest.main()
