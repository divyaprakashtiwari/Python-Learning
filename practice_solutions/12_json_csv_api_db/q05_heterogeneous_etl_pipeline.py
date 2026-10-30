"""
Question 5: Heterogeneous ETL Pipeline with Schema Normalization & DLQ
Topic: JSON, CSV, Web APIs, and Databases

Key Concepts Tested:
- Extraction and canonical key mapping across CSV and JSON inputs
- Date parsing across multiple date formats (YYYY-MM-DD, YYYY/MM/DD, MM-DD-YYYY)
- Validation, cleansing, and Dead-Letter Queue (DLQ) isolation
- Business enrichment (tax calculation, gross revenue, spending tiers)
- Relational loading into SQLite and execution manifest generation
"""

import csv
import io
import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Tuple


class ETLPipeline:
    """
    Data transformation pipeline supporting extraction from heterogeneous sources,
    deduplication, date normalization, DLQ validation, and loading into SQLite.
    """

    def __init__(self) -> None:
        self.raw_extracted_count = 0
        self.duplicates_dropped_count = 0
        self.dlq_records: List[Dict[str, Any]] = []
        self.loaded_records: List[Dict[str, Any]] = []

    @staticmethod
    def _parse_flexible_date(date_str: str) -> str:
        """Parses various date formats into ISO YYYY-MM-DD."""
        clean_str = date_str.strip()
        formats = ["%Y-%m-%d", "%Y/%m/%d", "%m-%d-%Y", "%d-%m-%Y"]
        for fmt in formats:
            try:
                dt = datetime.strptime(clean_str, fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
        raise ValueError(f"Unrecognized date format: '{clean_str}'")

    def extract(self, raw_csv: str, raw_json: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ingests and canonicalizes records from CSV string and JSON list."""
        records: List[Dict[str, Any]] = []

        # 1. Ingest CSV
        if raw_csv.strip():
            reader = csv.DictReader(io.StringIO(raw_csv.strip()))
            for row in reader:
                norm_row: Dict[str, Any] = {}
                for k, v in row.items():
                    if k is None:
                        continue
                    clean_k = k.strip()
                    val = v.strip() if v is not None else ""
                    # Canonical key mapping
                    if clean_k in ("cust_id", "customer_id", "UserID"):
                        norm_row["customer_id"] = val
                    else:
                        norm_row[clean_k] = val
                records.append(norm_row)

        # 2. Ingest JSON
        for item in raw_json:
            norm_item: Dict[str, Any] = {}
            for k, v in item.items():
                if k in ("cust_id", "customer_id", "UserID"):
                    norm_item["customer_id"] = str(v).strip()
                else:
                    norm_item[k] = v
            records.append(norm_item)

        self.raw_extracted_count = len(records)
        return records

    def transform(self, raw_records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Deduplicates, validates, cleanses, and enriches raw records.
        Returns (valid_records, dlq_records).
        """
        valid_records: List[Dict[str, Any]] = []
        seen_txn_ids: Dict[str, Dict[str, Any]] = {}

        for rec in raw_records:
            txn_id = rec.get("transaction_id", "").strip() if isinstance(rec.get("transaction_id"), str) else str(rec.get("transaction_id", "")).strip()
            cust_id = rec.get("customer_id", "").strip() if isinstance(rec.get("customer_id"), str) else str(rec.get("customer_id", "")).strip()

            # Required field validation
            if not txn_id or not cust_id:
                self.dlq_records.append({"record": rec, "reason": "Missing required fields (transaction_id or customer_id)"})
                continue

            # Amount validation
            try:
                raw_amt = rec.get("amount")
                amount = round(float(raw_amt), 2)
                if amount <= 0:
                    self.dlq_records.append({"record": rec, "reason": f"Negative or zero amount: {amount}"})
                    continue
            except (ValueError, TypeError):
                self.dlq_records.append({"record": rec, "reason": f"Invalid numeric amount: {rec.get('amount')}"})
                continue

            # Date normalization
            try:
                date_str = self._parse_flexible_date(str(rec.get("date", "")))
            except ValueError as err:
                self.dlq_records.append({"record": rec, "reason": str(err)})
                continue

            # Deduplication check
            if txn_id in seen_txn_ids:
                self.duplicates_dropped_count += 1
                continue

            # Enrichment
            tax_amount = round(amount * 0.08, 2)
            total_amount = round(amount + tax_amount, 2)
            if amount < 50.0:
                tier = "Bronze"
            elif amount <= 200.0:
                tier = "Silver"
            else:
                tier = "Gold"

            enriched_rec = {
                "transaction_id": txn_id,
                "customer_id": cust_id,
                "date": date_str,
                "amount": amount,
                "tax_amount": tax_amount,
                "total_amount": total_amount,
                "tier": tier,
            }
            seen_txn_ids[txn_id] = enriched_rec
            valid_records.append(enriched_rec)

        return valid_records, self.dlq_records

    def load_to_sqlite(self, clean_records: List[Dict[str, Any]], db_path: str = ":memory:") -> int:
        """Loads clean records into SQLite database."""
        conn = sqlite3.connect(db_path)
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id TEXT PRIMARY KEY,
                    customer_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    amount REAL NOT NULL,
                    tax_amount REAL NOT NULL,
                    total_amount REAL NOT NULL,
                    tier TEXT NOT NULL
                );
            """)
            conn.executemany("""
                INSERT OR REPLACE INTO transactions (
                    transaction_id, customer_id, date, amount, tax_amount, total_amount, tier
                ) VALUES (
                    :transaction_id, :customer_id, :date, :amount, :tax_amount, :total_amount, :tier
                );
            """, clean_records)

        self.loaded_records = clean_records
        conn.close()
        return len(clean_records)

    def run_pipeline(
        self,
        raw_csv: str,
        raw_json: List[Dict[str, Any]],
        db_path: str = ":memory:",
    ) -> Dict[str, Any]:
        """Runs full ETL cycle and outputs summary manifest."""
        raw = self.extract(raw_csv, raw_json)
        valid, dlq = self.transform(raw)
        self.load_to_sqlite(valid, db_path)

        total_revenue = sum(r["amount"] for r in valid)
        tier_dist: Dict[str, int] = {}
        for r in valid:
            tier_dist[r["tier"]] = tier_dist.get(r["tier"], 0) + 1

        return {
            "total_extracted": self.raw_extracted_count,
            "duplicates_dropped": self.duplicates_dropped_count,
            "validation_failures": len(dlq),
            "successfully_loaded": len(valid),
            "total_revenue": round(total_revenue, 2),
            "tier_distribution": tier_dist,
            "sample_enriched": valid[:2],
        }


if __name__ == "__main__":
    pipeline = ETLPipeline()

    raw_csv_data = """transaction_id, cust_id, date, amount
TXN-101, CUST-01, 2026/10/20, 150.00
TXN-102, CUST-02, 2026-10-21, -25.00
TXN-103, CUST-01, 10-22-2026, 45.00
"""
    raw_json_data = [
        {"transaction_id": "TXN-104", "customer_id": "CUST-03", "date": "2026-10-23", "amount": 320.00},
        {"transaction_id": "TXN-101", "customer_id": "CUST-01", "date": "2026-10-20", "amount": 150.00},  # duplicate
    ]

    manifest = pipeline.run_pipeline(raw_csv_data, raw_json_data, db_path=":memory:")

    print("=== Pipeline Execution Summary ===")
    print(f"- Total Raw Extracted: {manifest['total_extracted']}")
    print(f"- Duplicates Dropped: {manifest['duplicates_dropped']}")
    print(f"- Validation Failures (DLQ): {manifest['validation_failures']}")
    print(f"- Successfully Loaded into SQLite: {manifest['successfully_loaded']}")

    for rec in manifest["sample_enriched"]:
        print(f"Enriched {rec['transaction_id']}:")
        print(f"  Amount: {rec['amount']:.2f}, Tax (8%): {rec['tax_amount']:.2f}, Total: {rec['total_amount']:.2f}, Tier: '{rec['tier']}'")

    print(f"Total Revenue Processed: ${manifest['total_revenue']:.2f}")
    print(f"Tier Distribution: {manifest['tier_distribution']}")
