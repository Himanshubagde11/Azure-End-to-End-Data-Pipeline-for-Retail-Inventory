"""
NEXORA INVENTORY INTELLIGENCE
Module: data_quality.py
Description: Master Data Quality Orchestration Engine calculating enterprise DQ scores
Author: Senior Data Engineer / Azure Data Architect
Organization: NEXORA RETAIL GROUP
"""

import os
import json
import datetime
import uuid
import pandas as pd
from typing import Dict, Any, List

from config import EXPECTED_SCHEMAS, DQ_THRESHOLDS, LOGS_DIR
from schema_validator import SchemaValidator
from null_validator import NullValidator
from duplicate_validator import DuplicateValidator
from business_rule_validator import BusinessRuleValidator

class DataQualityEngine:
    def __init__(self, run_id: str = None):
        self.run_id = run_id or f"RUN_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:6]}"
        self.results: List[Dict[str, Any]] = []

    def evaluate_dataset(self, table_name: str, df: pd.DataFrame, reference_lookups: Dict[str, pd.DataFrame] = None) -> List[Dict[str, Any]]:
        """
        Runs the full 4-tier validation suite on a target dataframe:
        1. Schema validation
        2. Null checks on mandatory columns
        3. Duplicate key checks
        4. Business rules & referential integrity
        """
        schema_cfg = EXPECTED_SCHEMAS.get(table_name, {})
        table_results = []

        # Tier 1: Schema Check
        schema_val = SchemaValidator(table_name, schema_cfg)
        table_results.append(schema_val.validate(df))

        # Tier 2: Null Check
        null_val = NullValidator(table_name, schema_cfg.get("not_null", []))
        table_results.extend(null_val.validate(df))

        # Tier 3: Duplicate Check
        dup_val = DuplicateValidator(table_name, schema_cfg.get("primary_key", []))
        table_results.append(dup_val.validate(df))

        # Tier 4: Business Rules
        biz_val = BusinessRuleValidator(table_name, reference_lookups)
        table_results.extend(biz_val.validate(df))

        # Attach run metadata
        for r in table_results:
            r["run_id"] = self.run_id
            r["execution_time"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

        self.results.extend(table_results)
        return table_results

    def compute_summary(self) -> Dict[str, Any]:
        """
        Computes overall pass rate and enterprise Data Quality Score.
        """
        if not self.results:
            return {"run_id": self.run_id, "data_quality_score": 100.0, "status": "NO_DATA"}

        total_checks = len(self.results)
        passed_checks = sum(1 for r in self.results if r["status"] == "PASS")
        warning_checks = sum(1 for r in self.results if r["status"] == "WARNING")
        failed_checks = sum(1 for r in self.results if r["status"] == "FAIL")

        total_evaluated_records = sum(r["total_records"] for r in self.results)
        total_failed_records = sum(r["failed_records"] for r in self.results)

        # Overall DQ Score as mean of check pass percentages
        avg_pass_pct = round(sum(r["pass_percentage"] for r in self.results) / total_checks, 2)

        overall_status = "PASS"
        if failed_checks > 0:
            overall_status = "FAIL"
        elif warning_checks > 0:
            overall_status = "WARNING"

        return {
            "run_id": self.run_id,
            "data_quality_score": avg_pass_pct,
            "overall_status": overall_status,
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "warning_checks": warning_checks,
            "failed_checks": failed_checks,
            "total_evaluated_records": total_evaluated_records,
            "total_defective_records": total_failed_records,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

    def print_report(self):
        """
        Prints a high-contrast enterprise console report.
        """
        summary = self.compute_summary()
        print("\n" + "=" * 90)
        print(" NEXORA INVENTORY INTELLIGENCE — DATA QUALITY & VALIDATION REPORT")
        print(f" Run ID: {self.run_id} | Timestamp: {summary['timestamp']}")
        print("=" * 90)
        print(f"{'Table':<12} | {'Check Type':<14} | {'Rule Name':<34} | {'Pass %':<8} | {'Status'}")
        print("-" * 90)

        for r in self.results:
            status_symbol = "[PASS]" if r['status'] == 'PASS' else "[WARN]" if r['status'] == 'WARNING' else "[FAIL]"
            print(f"{r['table']:<12} | {r['check_type']:<14} | {r['rule_name'][:34]:<34} | {r['pass_percentage']:>6.2f}% | {status_symbol}")

        print("=" * 90)
        print(f" Summary: {summary['passed_checks']} PASS | {summary['warning_checks']} WARNING | {summary['failed_checks']} FAIL")
        print(f" Enterprise Data Quality Score: {summary['data_quality_score']}% -> Status: {summary['overall_status']}")
        print("=" * 90 + "\n")

    def export_report(self, filepath: str = None) -> str:
        """
        Exports structured JSON audit logs for ingestion into audit.DataQualityLog.
        """
        if not filepath:
            filepath = os.path.join(LOGS_DIR, f"dq_audit_log_{self.run_id}.json")
        summary = self.compute_summary()
        payload = {
            "summary": summary,
            "details": self.results
        }
        with open(filepath, "w") as f:
            json.dump(payload, f, indent=2)
        return filepath
