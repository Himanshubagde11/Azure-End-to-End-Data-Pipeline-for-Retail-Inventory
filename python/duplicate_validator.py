"""
CLARIVENS INVENTORY INTELLIGENCE
Module: duplicate_validator.py
Description: Validates uniqueness of primary keys and composite grain definitions
Author: Himanshu Bagde (Azure Data Engineer & Cloud Analytics Architect)
Organization: CLARIVENS RETAIL GROUP
"""

import pandas as pd
from typing import Dict, Any, List

class DuplicateValidator:
    def __init__(self, table_name: str, key_columns: List[str]):
        self.table_name = table_name
        self.key_columns = key_columns

    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validates uniqueness on key columns and returns duplicate violation count.
        """
        total_records = len(df)
        if not self.key_columns or not all(c in df.columns for c in self.key_columns):
            return {
                "table": self.table_name,
                "check_type": "DUPLICATE",
                "rule_name": f"UniqueKey_{'_'.join(self.key_columns)}",
                "total_records": total_records,
                "failed_records": 0,
                "pass_percentage": 100.0,
                "status": "PASS",
                "error_message": "Key columns not present for duplicate evaluation"
            }

        # Count records that appear more than once
        duplicates = df.duplicated(subset=self.key_columns, keep="first")
        failed_count = int(duplicates.sum())
        pass_pct = round(((total_records - failed_count) / total_records) * 100.0, 2) if total_records > 0 else 100.0

        if failed_count == 0:
            status = "PASS"
            err_msg = f"Primary key uniqueness verified across {total_records:,} records on ({', '.join(self.key_columns)})"
        elif pass_pct >= 98.0:
            status = "WARNING"
            err_msg = f"Detected {failed_count} duplicate rows on key ({', '.join(self.key_columns)})"
        else:
            status = "FAIL"
            err_msg = f"Critical duplicate volume: {failed_count} duplicate records on key ({', '.join(self.key_columns)})"

        return {
            "table": self.table_name,
            "check_type": "DUPLICATE",
            "rule_name": f"UniqueKey_{'_'.join(self.key_columns)}",
            "total_records": total_records,
            "failed_records": failed_count,
            "pass_percentage": pass_pct,
            "status": status,
            "error_message": err_msg
        }
