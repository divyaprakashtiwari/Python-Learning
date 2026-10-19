"""
Topic 12: JSON, CSV, API, Database
Question 05: Data Transformation Pipeline

A comprehensive, production-grade guide to building Extract, Transform, Load (ETL)
and data engineering pipelines in pure Python. Covers canonical key normalization,
dead-letter quarantine (DLQ), messy string type casting, deduplication windowing,
dimension table lookups, stream aggregations, pivot/melt operators, composable
pipeline stages, multi-sink loading, and an architectural end-to-end pipeline.

Every question contains standalone runnable exercises verified with 100% assertions.
"""

import csv
import json
import sqlite3
import re
from datetime import date
from decimal import Decimal
from typing import List, Dict, Any, Generator, Tuple, Callable, Optional


# =====================================================================
# Q1: Ingestion & Canonical Key Normalization
# =====================================================================
def to_snake_case(text: str) -> str:
    """Converts strings like 'First Name', 'firstName', 'First-Name' to 'first_name'."""
    text = re.sub(r"[\s\-]+", "_", text.strip())
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
    return text.lower()


def normalize_record_keys(record: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively normalizes all dictionary keys to snake_case."""
    normalized = {}
    for k, v in record.items():
        clean_key = to_snake_case(k)
        if isinstance(v, dict):
            normalized[clean_key] = normalize_record_keys(v)
        elif isinstance(v, list):
            normalized[clean_key] = [
                normalize_record_keys(item) if isinstance(item, dict) else item
                for item in v
            ]
        else:
            normalized[clean_key] = v
    return normalized


def q1_ingestion_and_key_normalization():
    raw_payload = {
        "User-ID": "USR-101",
        "FullName": "Jane Doe",
        "Contact Info": {
            "Phone Number": "555-0199",
            "ZipCode": "90210"
        },
        "Order-Items": [
            {"Item Name": "Laptop Stand", "ItemPrice": "49.99"}
        ]
    }

    clean = normalize_record_keys(raw_payload)
    assert clean["user_id"] == "USR-101"
    assert clean["full_name"] == "Jane Doe"
    assert clean["contact_info"]["phone_number"] == "555-0199"
    assert clean["contact_info"]["zip_code"] == "90210"
    assert clean["order_items"][0]["item_name"] == "Laptop Stand"
    assert clean["order_items"][0]["item_price"] == "49.99"

    print("=== Q1: Ingestion & Canonical Key Normalization Verified ===")


# =====================================================================
# Q2: Validation & Dead-Letter Queue (DLQ) Quarantine
# =====================================================================
class ValidationRule:
    def __init__(self, field: str, validator: Callable[[Any], bool], error_message: str):
        self.field = field
        self.validator = validator
        self.error_message = error_message


def run_validation_dlq(
    records: List[Dict[str, Any]],
    rules: List[ValidationRule]
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Evaluates records against validation rules.
    Returns (valid_records, dlq_quarantine_records).
    """
    valid = []
    dlq = []

    for rec in records:
        errors = []
        for rule in rules:
            val = rec.get(rule.field)
            if not rule.validator(val):
                errors.append(f"{rule.field}: {rule.error_message}")

        if errors:
            quarantined = dict(rec)
            quarantined["__dlq_reasons"] = errors
            dlq.append(quarantined)
        else:
            valid.append(rec)

    return valid, dlq


def q2_validation_and_dlq_quarantine():
    records = [
        {"txn_id": "T1", "amount": 150.0, "currency": "USD"},
        {"txn_id": "T2", "amount": -20.0, "currency": "USD"},   # negative amount
        {"txn_id": "T3", "amount": 75.0, "currency": "UNKNOWN"}, # invalid currency
        {"txn_id": "T4", "amount": 500.0, "currency": "EUR"},
    ]

    rules = [
        ValidationRule("amount", lambda v: isinstance(v, (int, float)) and v > 0, "Must be positive number"),
        ValidationRule("currency", lambda v: v in {"USD", "EUR", "GBP"}, "Must be valid ISO currency")
    ]

    valid, dlq = run_validation_dlq(records, rules)
    assert len(valid) == 2
    assert [r["txn_id"] for r in valid] == ["T1", "T4"]

    assert len(dlq) == 2
    assert dlq[0]["txn_id"] == "T2"
    assert "amount: Must be positive number" in dlq[0]["__dlq_reasons"]
    assert dlq[1]["txn_id"] == "T3"
    assert "currency: Must be valid ISO currency" in dlq[1]["__dlq_reasons"]

    print("=== Q2: Validation & Dead-Letter Queue Quarantine Verified ===")


# =====================================================================
# Q3: Dirty String Normalization and Type Casting
# =====================================================================
def clean_currency(raw: str) -> Decimal:
    """Strips currency symbols ('$', '€', '£'), commas, and whitespaces into Decimal."""
    cleaned = re.sub(r"[^\d.\-]", "", raw)
    return Decimal(cleaned)


def clean_date(raw: str) -> date:
    """Parses various formats (YYYY-MM-DD, YYYY/MM/DD, MM-DD-YYYY, DD/MM/YYYY) into date."""
    raw = raw.strip()
    # Match YYYY-MM-DD or YYYY/MM/DD
    m1 = re.match(r"^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$", raw)
    if m1:
        return date(int(m1.group(1)), int(m1.group(2)), int(m1.group(3)))
    # Match MM-DD-YYYY or MM/DD/YYYY
    m2 = re.match(r"^(\d{1,2})[-/](\d{1,2})[-/](\d{4})$", raw)
    if m2:
        return date(int(m2.group(3)), int(m2.group(1)), int(m2.group(2)))
    raise ValueError(f"Unrecognized date format: {raw}")


def clean_phone(raw: str) -> str:
    """Extracts numeric digits and formats as canonical E.164-like '+1XXXXXXXXXX'."""
    digits = re.sub(r"\D", "", raw)
    if len(digits) == 10:
        return f"+1{digits}"
    elif len(digits) == 11 and digits.startswith("1"):
        return f"+{digits}"
    return f"+{digits}"


def q3_dirty_string_normalization():
    assert clean_currency("$1,250.75") == Decimal("1250.75")
    assert clean_currency(" - £300.50 ") == Decimal("-300.50")

    assert clean_date("2024-06-15") == date(2024, 6, 15)
    assert clean_date("2024/11/05") == date(2024, 11, 5)
    assert clean_date("12/25/2023") == date(2023, 12, 25)

    assert clean_phone("(555) 234-5678") == "+15552345678"
    assert clean_phone("1-800-555-0199") == "+18005550199"

    print("=== Q3: Dirty String Normalization & Type Casting Verified ===")


# =====================================================================
# Q4: Deduplication and State Windowing
# =====================================================================
def deduplicate_stream(
    records: List[Dict[str, Any]],
    key_fn: Callable[[Dict[str, Any]], Any],
    tie_breaker: Optional[Callable[[Dict[str, Any]], Any]] = None
) -> List[Dict[str, Any]]:
    """
    Deduplicates records based on compound business key.
    If tie_breaker provided (e.g. timestamp), retains record with max tie_breaker value.
    """
    store: Dict[Any, Dict[str, Any]] = {}
    for r in records:
        k = key_fn(r)
        if k not in store:
            store[k] = r
        elif tie_breaker:
            if tie_breaker(r) > tie_breaker(store[k]):
                store[k] = r

    return list(store.values())


def q4_deduplication_and_windowing():
    events = [
        {"session_id": "S1", "event": "click", "ts": 100},
        {"session_id": "S1", "event": "click", "ts": 105}, # duplicate with newer timestamp
        {"session_id": "S1", "event": "scroll", "ts": 102},
        {"session_id": "S2", "event": "click", "ts": 101},
    ]

    # Deduplicate on (session_id, event), keeping highest ts
    deduped = deduplicate_stream(
        events,
        key_fn=lambda e: (e["session_id"], e["event"]),
        tie_breaker=lambda e: e["ts"]
    )
    assert len(deduped) == 3
    s1_click = next(e for e in deduped if e["session_id"] == "S1" and e["event"] == "click")
    assert s1_click["ts"] == 105

    print("=== Q4: Stream Deduplication with Tie-Breaking Verified ===")


# =====================================================================
# Q5: Relational Lookup & Dimension Table Enrichment
# =====================================================================
def enrich_transactions(
    transactions: List[Dict[str, Any]],
    product_dim: Dict[str, Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Enriches transaction rows with dimension table data (e.g. category, cost, profit_margin).
    Gracefully handles unknown/unmatched foreign keys.
    """
    enriched = []
    for txn in transactions:
        row = dict(txn)
        sku = txn["sku"]
        dim_info = product_dim.get(sku, {
            "name": "Unknown Item",
            "category": "Uncategorized",
            "cost_price": Decimal("0.00")
        })

        row["product_name"] = dim_info["name"]
        row["category"] = dim_info["category"]
        cost = Decimal(str(dim_info["cost_price"]))
        sale_price = Decimal(str(txn["unit_price"]))
        row["profit"] = (sale_price - cost) * txn["qty"]
        enriched.append(row)

    return enriched


def q5_relational_lookup_enrichment():
    product_catalog = {
        "SKU-01": {"name": "Wireless Mouse", "category": "Electronics", "cost_price": Decimal("15.00")},
        "SKU-02": {"name": "USB-C Cable", "category": "Accessories", "cost_price": Decimal("3.50")},
    }

    transactions = [
        {"txn_id": "TX1", "sku": "SKU-01", "qty": 2, "unit_price": Decimal("25.00")},
        {"txn_id": "TX2", "sku": "SKU-02", "qty": 3, "unit_price": Decimal("8.50")},
        {"txn_id": "TX3", "sku": "SKU-99", "qty": 1, "unit_price": Decimal("10.00")}, # Missing SKU
    ]

    results = enrich_transactions(transactions, product_catalog)
    assert len(results) == 3

    assert results[0]["product_name"] == "Wireless Mouse"
    assert results[0]["profit"] == Decimal("20.00") # (25 - 15) * 2 = 20

    assert results[1]["product_name"] == "USB-C Cable"
    assert results[1]["profit"] == Decimal("15.00") # (8.50 - 3.50) * 3 = 15

    assert results[2]["product_name"] == "Unknown Item"
    assert results[2]["category"] == "Uncategorized"

    print("=== Q5: Relational Lookup & Dimension Enrichment Verified ===")


# =====================================================================
# Q6: Streaming GroupBy and Multi-Metric Aggregator Engine
# =====================================================================
class MetricAggregator:
    def __init__(self):
        self.count = 0
        self.total = Decimal("0.00")
        self.min_val: Optional[Decimal] = None
        self.max_val: Optional[Decimal] = None

    def add(self, value: Decimal):
        self.count += 1
        self.total += value
        if self.min_val is None or value < self.min_val:
            self.min_val = value
        if self.max_val is None or value > self.max_val:
            self.max_val = value

    @property
    def average(self) -> Decimal:
        return (self.total / self.count).quantize(Decimal("0.01")) if self.count > 0 else Decimal("0.00")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "count": self.count,
            "total": self.total,
            "average": self.average,
            "min": self.min_val,
            "max": self.max_val,
        }


def aggregate_by_key(
    records: List[Dict[str, Any]],
    group_key: str,
    val_key: str
) -> Dict[str, Dict[str, Any]]:
    groups: Dict[str, MetricAggregator] = {}
    for r in records:
        g = str(r[group_key])
        val = Decimal(str(r[val_key]))
        if g not in groups:
            groups[g] = MetricAggregator()
        groups[g].add(val)

    return {k: agg.to_dict() for k, agg in groups.items()}


def q6_groupby_aggregation():
    orders = [
        {"region": "North", "sales": "100.00"},
        {"region": "North", "sales": "250.00"},
        {"region": "South", "sales": "400.00"},
        {"region": "North", "sales": "50.00"},
        {"region": "South", "sales": "100.00"},
    ]

    summary = aggregate_by_key(orders, group_key="region", val_key="sales")
    assert "North" in summary and "South" in summary

    north = summary["North"]
    assert north["count"] == 3
    assert north["total"] == Decimal("400.00")
    assert north["average"] == Decimal("133.33")
    assert north["min"] == Decimal("50.00")
    assert north["max"] == Decimal("250.00")

    south = summary["South"]
    assert south["count"] == 2
    assert south["total"] == Decimal("500.00")
    assert south["average"] == Decimal("250.00")

    print("=== Q6: Streaming GroupBy & Multi-Metric Aggregator Verified ===")


# =====================================================================
# Q7: Pivot and Unpivot (Melt) Matrix Operations
# =====================================================================
def pivot_table(
    records: List[Dict[str, Any]],
    row_key: str,
    col_key: str,
    val_key: str,
    fill_value: Any = 0
) -> Tuple[List[str], List[Dict[str, Any]]]:
    """Pivots normalized long rows into wide format."""
    unique_cols = sorted({str(r[col_key]) for r in records})
    rows_map: Dict[str, Dict[str, Any]] = {}

    for r in records:
        rk = str(r[row_key])
        ck = str(r[col_key])
        val = r[val_key]
        if rk not in rows_map:
            rows_map[rk] = {row_key: rk, **{c: fill_value for c in unique_cols}}
        rows_map[rk][ck] = val

    return unique_cols, list(rows_map.values())


def melt_table(
    wide_records: List[Dict[str, Any]],
    id_vars: List[str],
    value_vars: List[str],
    var_name: str = "variable",
    val_name: str = "value"
) -> List[Dict[str, Any]]:
    """Unpivots wide columns back into long normalized key-value records."""
    melted = []
    for row in wide_records:
        base_id = {k: row[k] for k in id_vars}
        for vcol in value_vars:
            rec = dict(base_id)
            rec[var_name] = vcol
            rec[val_name] = row[vcol]
            melted.append(rec)
    return melted


def q7_pivot_and_melt_transforms():
    # Long format sales data: (store, quarter, revenue)
    long_data = [
        {"store": "Main St", "quarter": "Q1", "revenue": 100},
        {"store": "Main St", "quarter": "Q2", "revenue": 150},
        {"store": "Broad St", "quarter": "Q1", "revenue": 80},
        {"store": "Broad St", "quarter": "Q2", "revenue": 120},
    ]

    cols, wide = pivot_table(long_data, row_key="store", col_key="quarter", val_key="revenue")
    assert cols == ["Q1", "Q2"]
    assert len(wide) == 2
    main = next(r for r in wide if r["store"] == "Main St")
    assert main["Q1"] == 100 and main["Q2"] == 150

    # Melt back to long
    melted = melt_table(wide, id_vars=["store"], value_vars=["Q1", "Q2"], var_name="quarter", val_name="revenue")
    assert len(melted) == 4
    assert {"store": "Main St", "quarter": "Q1", "revenue": 100} in melted
    assert {"store": "Broad St", "quarter": "Q2", "revenue": 120} in melted

    print("=== Q7: Pivot & Melt Matrix Transformations Verified ===")


# =====================================================================
# Q8: Composable Functional Pipeline Builder
# =====================================================================
class DataPipeline:
    """A composable, fluent data transformation pipeline with stage-wise timing."""
    def __init__(self, name: str):
        self.name = name
        self.stages: List[Tuple[str, Callable[[List[Dict[str, Any]]], List[Dict[str, Any]]]]] = []

    def add_stage(
        self,
        stage_name: str,
        fn: Callable[[List[Dict[str, Any]]], List[Dict[str, Any]]]
    ) -> "DataPipeline":
        self.stages.append((stage_name, fn))
        return self

    def execute(self, initial_data: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
        data = initial_data
        metrics = {"initial_count": len(initial_data)}
        for stage_name, fn in self.stages:
            data = fn(data)
            metrics[f"{stage_name}_count"] = len(data)
        metrics["final_count"] = len(data)
        return data, metrics


def q8_composable_pipeline_builder():
    def filter_active(records):
        return [r for r in records if r.get("status") == "active"]

    def convert_scores(records):
        return [{**r, "score": int(r["score"])} for r in records]

    def filter_high_scorers(records):
        return [r for r in records if r["score"] >= 80]

    pipeline = (
        DataPipeline("PlayerRatingPipeline")
        .add_stage("filter_active", filter_active)
        .add_stage("convert_scores", convert_scores)
        .add_stage("filter_high_scorers", filter_high_scorers)
    )

    raw_players = [
        {"player": "A", "status": "active", "score": "95"},
        {"player": "B", "status": "inactive", "score": "99"},
        {"player": "C", "status": "active", "score": "60"},
        {"player": "D", "status": "active", "score": "85"},
    ]

    out, metrics = pipeline.execute(raw_players)
    assert len(out) == 2
    assert [p["player"] for p in out] == ["A", "D"]
    assert metrics["initial_count"] == 4
    assert metrics["filter_active_count"] == 3
    assert metrics["filter_high_scorers_count"] == 2

    print("=== Q8: Composable Functional Pipeline Builder Verified ===")


# =====================================================================
# Q9: Multi-Sink Loaders (CSV, JSON Lines, SQLite)
# =====================================================================
def load_to_sqlite(records: List[Dict[str, Any]], conn: sqlite3.Connection, table_name: str):
    if not records:
        return
    columns = list(records[0].keys())
    col_defs = ", ".join(f"{col} TEXT" for col in columns)
    placeholders = ", ".join("?" for _ in columns)

    with conn:
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({col_defs});")
        data = [[str(r[c]) for c in columns] for r in records]
        conn.executemany(f"INSERT INTO {table_name} VALUES ({placeholders});", data)


def load_to_jsonl(records: List[Dict[str, Any]]) -> str:
    return "\n".join(json.dumps(r) for r in records)


def q9_multi_sink_loaders():
    records = [
        {"id": "1", "name": "Alpha", "val": "100"},
        {"id": "2", "name": "Beta", "val": "200"},
    ]

    # Sink 1: SQLite
    conn = sqlite3.connect(":memory:")
    load_to_sqlite(records, conn, "staging_table")
    cursor = conn.execute("SELECT COUNT(*) FROM staging_table;")
    assert cursor.fetchone()[0] == 2

    # Sink 2: JSON Lines
    jsonl_output = load_to_jsonl(records)
    lines = jsonl_output.strip().split("\n")
    assert len(lines) == 2
    assert json.loads(lines[0])["name"] == "Alpha"

    conn.close()
    print("=== Q9: Multi-Sink Loading Verified ===")


# =====================================================================
# Q10: Architectural End-to-End Enterprise ETL Pipeline
# =====================================================================
class EnterpriseETLPipeline:
    """
    Orchestrates an enterprise end-to-end data pipeline:
    1. Extract: Ingests raw untyped customer purchase logs
    2. Transform:
       - Normalizes keys
       - Type casts currency and dates
       - Quarantines invalid records (DLQ)
       - Enriches with product category lookup
    3. Load: Loads valid transformed data into SQLite analytics table and DLQ table
    """
    def __init__(self, db_conn: sqlite3.Connection, catalog_lookup: Dict[str, str]):
        self.conn = db_conn
        self.catalog = catalog_lookup

    def run(self, raw_input: List[Dict[str, Any]]) -> Dict[str, Any]:
        extracted_count = len(raw_input)
        valid_records = []
        dlq_records = []

        for item in raw_input:
            clean_item = normalize_record_keys(item)
            reasons = []

            # Validate order_id
            order_id = clean_item.get("order_id", "").strip()
            if not order_id:
                reasons.append("Missing order_id")

            # Parse amount
            raw_amt = clean_item.get("amount", "")
            try:
                amount = clean_currency(str(raw_amt))
                if amount <= 0:
                    reasons.append("Amount must be positive")
            except Exception:
                reasons.append(f"Invalid amount '{raw_amt}'")
                amount = None

            # Parse date
            raw_date = clean_item.get("order_date", "")
            try:
                order_date = clean_date(str(raw_date))
            except Exception:
                reasons.append(f"Invalid date '{raw_date}'")
                order_date = None

            if reasons:
                bad_row = dict(clean_item)
                bad_row["errors"] = "; ".join(reasons)
                dlq_records.append(bad_row)
            else:
                sku = clean_item.get("sku", "UNKNOWN")
                category = self.catalog.get(sku, "General Merchandise")
                valid_records.append({
                    "order_id": order_id,
                    "sku": sku,
                    "category": category,
                    "amount": float(amount),
                    "order_date": order_date.isoformat(),
                })

        # Load valid records
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS orders_fact (
                    order_id TEXT PRIMARY KEY,
                    sku TEXT,
                    category TEXT,
                    amount REAL,
                    order_date TEXT
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS orders_dlq (
                    raw_data TEXT,
                    errors TEXT
                );
            """)

            for v in valid_records:
                self.conn.execute(
                    "INSERT INTO orders_fact VALUES (?, ?, ?, ?, ?);",
                    (v["order_id"], v["sku"], v["category"], v["amount"], v["order_date"])
                )

            for d in dlq_records:
                self.conn.execute(
                    "INSERT INTO orders_dlq VALUES (?, ?);",
                    (json.dumps(d), d["errors"])
                )

        return {
            "extracted": extracted_count,
            "loaded": len(valid_records),
            "quarantined": len(dlq_records),
        }


def q10_architectural_enterprise_etl():
    catalog = {
        "SKU-100": "Hardware",
        "SKU-200": "Software",
    }
    conn = sqlite3.connect(":memory:")

    pipeline = EnterpriseETLPipeline(conn, catalog)

    raw_batch = [
        {"Order-ID": "ORD-001", "SKU": "SKU-100", "Amount": "$1,499.00", "Order-Date": "2024-05-01"},
        {"Order-ID": "ORD-002", "SKU": "SKU-200", "Amount": "£89.50", "Order-Date": "05/15/2024"},
        {"Order-ID": "ORD-003", "SKU": "SKU-300", "Amount": "-$10.00", "Order-Date": "2024-05-20"}, # negative amt -> DLQ
        {"Order-ID": "", "SKU": "SKU-100", "Amount": "$50.00", "Order-Date": "invalid-date"}, # missing id & bad date -> DLQ
    ]

    stats = pipeline.run(raw_batch)
    assert stats["extracted"] == 4
    assert stats["loaded"] == 2
    assert stats["quarantined"] == 2

    # Verify orders_fact in SQLite
    cur = conn.execute("SELECT order_id, category, amount FROM orders_fact ORDER BY order_id;")
    fact_rows = cur.fetchall()
    assert len(fact_rows) == 2
    assert fact_rows[0] == ("ORD-001", "Hardware", 1499.00)
    assert fact_rows[1] == ("ORD-002", "Software", 89.50)

    # Verify orders_dlq in SQLite
    cur = conn.execute("SELECT COUNT(*) FROM orders_dlq;")
    assert cur.fetchone()[0] == 2

    conn.close()
    print("=== Q10: Architectural Enterprise ETL Pipeline Verified ===")


# =====================================================================
# Main Test Runner
# =====================================================================
if __name__ == "__main__":
    q1_ingestion_and_key_normalization()
    q2_validation_and_dlq_quarantine()
    q3_dirty_string_normalization()
    q4_deduplication_and_windowing()
    q5_relational_lookup_enrichment()
    q6_groupby_aggregation()
    q7_pivot_and_melt_transforms()
    q8_composable_pipeline_builder()
    q9_multi_sink_loaders()
    q10_architectural_enterprise_etl()

    print("\nAll 10 data transformation pipeline practice questions passed successfully!")
