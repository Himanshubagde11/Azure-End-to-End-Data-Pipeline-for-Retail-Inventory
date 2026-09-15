"""
CLARIVENS INVENTORY INTELLIGENCE
Module: null_validator.py
Description: Validates completeness and absence of null/empty values on mandatory fields
Author: Senior Data Engineer / Azure Data Architect
Organization: CLARIVENS RETAIL GROUP
"""

import pandas as pd
from typing import Dict, Any, List

class NullValidator:
    def __init__(self, table_name: str, not_null_columns: List[str]):
        self.table_name = table_name
        self.not_null_columns = not_null_columns

    def validate(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Validates mandatory not-null fields and returns evaluation per column.
        """
        results = []
        total_records = len(df)

        for col in self.not_null_columns:
            if col not in df.columns:
                continue

            # Identify NaN, None, or empty whitespace strings
            is_null = df[col].isna() | (df[col].astype(str).str.strip().isin(["", "nan", "None", "NULL"]))
            failed_count = int(is_null.sum())
            pass_pct = round(((total_records - failed_count) / total_records) * 100.0, 2) if total_records > 0 else 100.0

            if failed_count == 0:
                status = "PASS"
                err_msg = f"Zero nulls in mandatory column '{col}'"
            elif pass_pct >= 98.0:
                status = "WARNING"
                err_msg = f"Column '{col}' contains {failed_count} nulls ({100.0 - pass_pct:.2f}% defect rate)"
            else:
                status = "FAIL"
                err_msg = f"Critical null volume in '{col}': {failed_count} null records ({100.0 - pass_pct:.2f}% defect rate)"

            results.append({
                "table": self.table_name,
                "check_type": "NULL",
                "rule_name": f"NotNull_{col}",
                "total_records": total_records,
                "failed_records": failed_count,
                "pass_percentage": pass_pct,
                "status": status,
                "error_message": err_msg
            })

        return results
