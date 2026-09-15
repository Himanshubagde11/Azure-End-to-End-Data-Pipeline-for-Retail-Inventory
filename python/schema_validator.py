"""
CLARIVENS INVENTORY INTELLIGENCE
Module: schema_validator.py
Description: Validates column existence, missing columns, and data type conformity
Author: Senior Data Engineer / Azure Data Architect
Organization: CLARIVENS RETAIL GROUP
"""

import pandas as pd
from typing import Dict, Any

class SchemaValidator:
    def __init__(self, table_name: str, expected_schema: Dict[str, Any]):
        self.table_name = table_name
        self.expected_schema = expected_schema

    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validates column completeness and schema structure.
        """
        total_records = len(df)
        expected_cols = set(self.expected_schema.get("columns", []))
        actual_cols = set(df.columns)

        missing_cols = list(expected_cols - actual_cols)
        unexpected_cols = list(actual_cols - expected_cols)

        # Check for column presence
        failed_records = 0
        status = "PASS"
        error_msgs = []

        if missing_cols:
            status = "FAIL"
            failed_records = total_records # Entire table compromised if required columns missing
            error_msgs.append(f"Missing required columns: {missing_cols}")

        if unexpected_cols:
            error_msgs.append(f"Found unexpected extra columns: {unexpected_cols}")

        pass_pct = 100.0 if failed_records == 0 else 0.0

        return {
            "table": self.table_name,
            "check_type": "SCHEMA",
            "rule_name": "Required_Columns_Check",
            "total_records": total_records,
            "failed_records": failed_records,
            "pass_percentage": round(pass_pct, 2),
            "status": status,
            "error_message": "; ".join(error_msgs) if error_msgs else "All required columns present and conform to schema contract"
        }
