"""
CLARIVENS INVENTORY INTELLIGENCE
Module: business_rule_validator.py
Description: Validates mathematical integrity, range checks, referential integrity, and domain rules
Author: Senior Data Engineer / Azure Data Architect
Organization: CLARIVENS RETAIL GROUP
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List

class BusinessRuleValidator:
    def __init__(self, table_name: str, reference_lookups: Dict[str, pd.DataFrame] = None):
        self.table_name = table_name
        self.reference_lookups = reference_lookups or {}

    def validate(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Executes domain business rules specific to each entity table.
        """
        results = []
        total_records = len(df)

        if self.table_name == "sales":
            # 1. Rule: Quantity must be strictly positive (> 0)
            if "Quantity" in df.columns:
                failed = df["Quantity"].isna() | (df["Quantity"] <= 0)
                results.append(self._format_rule_result(
                    "Rule_Positive_Sales_Quantity", total_records, int(failed.sum()),
                    "Quantity must be strictly greater than 0"
                ))

            # 2. Rule: UnitPrice must be non-negative
            if "UnitPrice" in df.columns:
                failed = df["UnitPrice"].isna() | (df["UnitPrice"] < 0)
                results.append(self._format_rule_result(
                    "Rule_Non_Negative_UnitPrice", total_records, int(failed.sum()),
                    "Unit selling price cannot be negative or null"
                ))

            # 3. Rule: Revenue calculation formula consistency (Qty * Price * (1 - Disc))
            if all(c in df.columns for c in ["Quantity", "UnitPrice", "Discount", "Revenue"]):
                expected_rev = df["Quantity"] * df["UnitPrice"] * (1.0 - df["Discount"].fillna(0.0))
                # Tolerant to rounding within 1.0 currency unit
                failed = (df["Revenue"] - expected_rev).abs() > 1.5
                results.append(self._format_rule_result(
                    "Rule_Revenue_Equation_Integrity", total_records, int(failed.sum()),
                    "Revenue must equal Quantity * UnitPrice * (1 - Discount)"
                ))

            # 4. Rule: Valid historical SaleDate (not in future / calendar valid)
            if "SaleDate" in df.columns:
                parsed_dates = pd.to_datetime(df["SaleDate"], errors="coerce")
                failed = parsed_dates.isna() | (parsed_dates > pd.Timestamp("2025-12-31"))
                results.append(self._format_rule_result(
                    "Rule_Valid_Calendar_SaleDate", total_records, int(failed.sum()),
                    "Sale date must be a valid calendar date on or before 2025-12-31"
                ))

            # 5. Rule: Referential integrity for ProductID & StoreID
            if "products" in self.reference_lookups and "ProductID" in df.columns:
                valid_prods = set(self.reference_lookups["products"]["ProductID"].dropna().astype(str))
                failed = ~df["ProductID"].astype(str).isin(valid_prods)
                results.append(self._format_rule_result(
                    "Rule_Referential_Integrity_ProductID", total_records, int(failed.sum()),
                    "ProductID must exist in master Products catalog"
                ))

            if "stores" in self.reference_lookups and "StoreID" in df.columns:
                valid_stores = set(self.reference_lookups["stores"]["StoreID"].dropna().astype(str))
                failed = ~df["StoreID"].astype(str).isin(valid_stores)
                results.append(self._format_rule_result(
                    "Rule_Referential_Integrity_StoreID", total_records, int(failed.sum()),
                    "StoreID must exist in master Stores catalog"
                ))

        elif self.table_name == "inventory":
            # 1. Rule: Non-negative Closing Stock
            if "ClosingStock" in df.columns:
                failed = df["ClosingStock"].isna() | (df["ClosingStock"] < 0)
                results.append(self._format_rule_result(
                    "Rule_Non_Negative_ClosingStock", total_records, int(failed.sum()),
                    "Closing stock count cannot be negative"
                ))

            # 2. Rule: Stock Balance Equation: Closing = Opening + Received - Sold + Returns - Damaged
            eq_cols = ["OpeningStock", "ReceivedQuantity", "SoldQuantity", "ReturnQuantity", "DamagedQuantity", "ClosingStock"]
            if all(c in df.columns for c in eq_cols):
                expected_close = (
                    df["OpeningStock"].fillna(0) +
                    df["ReceivedQuantity"].fillna(0) -
                    df["SoldQuantity"].fillna(0) +
                    df["ReturnQuantity"].fillna(0) -
                    df["DamagedQuantity"].fillna(0)
                )
                failed = (df["ClosingStock"] != expected_close)
                results.append(self._format_rule_result(
                    "Rule_Inventory_Balance_Equation", total_records, int(failed.sum()),
                    "Closing stock must balance with Opening + Received - Sold + Returns - Damaged"
                ))

            # 3. Rule: Non-negative Inventory Value
            if "InventoryValue" in df.columns:
                failed = df["InventoryValue"].isna() | (df["InventoryValue"] < 0)
                results.append(self._format_rule_result(
                    "Rule_Non_Negative_InventoryValue", total_records, int(failed.sum()),
                    "Total monetary inventory value cannot be negative"
                ))

        elif self.table_name == "products":
            # 1. Rule: Standard Category Naming
            if "CategoryName" in df.columns and "categories" in self.reference_lookups:
                valid_cats = set(self.reference_lookups["categories"]["CategoryName"].dropna().astype(str))
                failed = ~df["CategoryName"].astype(str).isin(valid_cats)
                results.append(self._format_rule_result(
                    "Rule_Standard_Category_Naming", total_records, int(failed.sum()),
                    "CategoryName must conform to standardized casing and titles"
                ))

            # 2. Rule: UnitPrice >= UnitCost (Positive Margin)
            if "UnitPrice" in df.columns and "UnitCost" in df.columns:
                failed = (df["UnitPrice"].notna()) & (df["UnitCost"].notna()) & (df["UnitPrice"] < df["UnitCost"])
                results.append(self._format_rule_result(
                    "Rule_Positive_Gross_Margin", total_records, int(failed.sum()),
                    "Selling price must exceed purchase cost"
                ))

            # 3. Rule: Referential integrity for SupplierID
            if "SupplierID" in df.columns and "suppliers" in self.reference_lookups:
                valid_sups = set(self.reference_lookups["suppliers"]["SupplierID"].dropna().astype(str))
                failed = ~df["SupplierID"].astype(str).isin(valid_sups)
                results.append(self._format_rule_result(
                    "Rule_Referential_Integrity_SupplierID", total_records, int(failed.sum()),
                    "SupplierID must exist in master Suppliers directory"
                ))

        elif self.table_name == "purchases":
            # 1. Rule: Plausible Received Quantity (not > 2x ordered)
            if "OrderedQuantity" in df.columns and "ReceivedQuantity" in df.columns:
                failed = (df["ReceivedQuantity"] > (df["OrderedQuantity"] * 2))
                results.append(self._format_rule_result(
                    "Rule_Plausible_Received_Quantity", total_records, int(failed.sum()),
                    "Received quantity cannot exceed twice the ordered quantity"
                ))

            # 2. Rule: Chronological delivery dates
            if "OrderDate" in df.columns and "ActualDeliveryDate" in df.columns:
                has_dates = df["ActualDeliveryDate"].notna() & (df["ActualDeliveryDate"].astype(str).str.strip() != "")
                o_dates = pd.to_datetime(df.loc[has_dates, "OrderDate"], errors="coerce")
                d_dates = pd.to_datetime(df.loc[has_dates, "ActualDeliveryDate"], errors="coerce")
                invalid_dates = (d_dates < o_dates)
                failed_count = int(invalid_dates.sum())
                results.append(self._format_rule_result(
                    "Rule_Chronological_Delivery_Dates", total_records, failed_count,
                    "Actual delivery date must occur on or after the order date"
                ))

        elif self.table_name == "returns":
            # 1. Rule: Positive Refund Amount
            if "RefundAmount" in df.columns:
                failed = df["RefundAmount"].isna() | (df["RefundAmount"] <= 0)
                results.append(self._format_rule_result(
                    "Rule_Positive_Refund_Amount", total_records, int(failed.sum()),
                    "Customer refund amount must be strictly greater than 0"
                ))

        return results

    def _format_rule_result(self, rule_name: str, total: int, failed: int, desc: str) -> Dict[str, Any]:
        pass_pct = round(((total - failed) / total) * 100.0, 2) if total > 0 else 100.0
        if failed == 0:
            status = "PASS"
            err_msg = f"{desc} (100% compliant)"
        elif pass_pct >= 98.0:
            status = "WARNING"
            err_msg = f"{desc}: {failed:,} violations detected ({100.0 - pass_pct:.2f}% defect rate)"
        else:
            status = "FAIL"
            err_msg = f"CRITICAL: {desc}: {failed:,} violations detected ({100.0 - pass_pct:.2f}% defect rate)"

        return {
            "table": self.table_name,
            "check_type": "BUSINESS_RULE",
            "rule_name": rule_name,
            "total_records": total,
            "failed_records": failed,
            "pass_percentage": pass_pct,
            "status": status,
            "error_message": err_msg
        }
