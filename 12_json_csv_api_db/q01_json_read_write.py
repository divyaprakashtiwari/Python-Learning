"""
Topic: Real-World Data Handling - JSON Read/Write
------------------------------------------------
Questions Covered:
1. Core JSON Serialization & Deserialization: dumps, loads, dump, load with indentation and sorting.
2. Custom JSONEncoder: Serializing non-standard types (datetime, Decimal, UUID, sets).
3. Custom Deserialization with object_hook: Reconstituting domain objects on parse.
4. JSON Lines (JSONL) Streaming Engine: High-throughput memory-bounded record processing.
5. Error Diagnostics & Malformed Recovery: Catching JSONDecodeError with line/column isolation and repair.
6. Circular Reference Detection: Identifying and safely rejecting cyclic graphs.
7. Deep Filtering & PII Masking: Redacting sensitive fields in deeply nested JSON structures.
8. Minification vs Pretty-Printing: Optimizing payload byte size using separators=(',', ':').
9. Exact High-Precision Numeric Parsing: Using parse_float=Decimal to prevent floating-point drift.
10. Architectural System: Crash-Resilient Atomic JSON Document Store with Indexing and Querying.
"""

import json
import os
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Tuple, Optional, Any, Dict, Set


# ==============================================================================
# Question 1: Core JSON Serialization and Deserialization
# ==============================================================================
def serialize_and_format_payload(data: Dict[str, Any], indent: int = 2) -> str:
    """Serializes dictionary to formatted, key-sorted JSON string."""
    return json.dumps(data, indent=indent, sort_keys=True)


def deserialize_payload(json_str: str) -> Dict[str, Any]:
    """Deserializes JSON string into dictionary."""
    return json.loads(json_str)


def test_q1_core_json():
    payload = {"service": "auth", "port": 8080, "active": True, "tags": ["prod", "security"]}
    json_str = serialize_and_format_payload(payload, indent=2)
    assert '"active": true' in json_str
    assert '"port": 8080' in json_str

    deserialized = deserialize_payload(json_str)
    assert deserialized == payload
    print("=== Q1: Core JSON Serialization and Deserialization Verified ===")


# ==============================================================================
# Question 2: Custom JSONEncoder for Non-Standard Types
# ==============================================================================
class ExtendedTypeEncoder(json.JSONEncoder):
    """
    Custom encoder handling:
    - datetime -> ISO 8601 string
    - Decimal -> float or str
    - UUID -> canonical hex string
    - set -> sorted list
    """
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, set):
            return sorted(list(obj))
        return super().default(obj)


def test_q2_custom_json_encoder():
    test_uuid = uuid.UUID("12345678-1234-5678-1234-567812345678")
    now_dt = datetime(2026, 10, 19, 12, 0, 0, tzinfo=timezone.utc)
    data = {
        "id": test_uuid,
        "timestamp": now_dt,
        "amount": Decimal("199.95"),
        "permissions": {"read", "write"},
    }

    encoded = json.dumps(data, cls=ExtendedTypeEncoder, sort_keys=True)
    assert '"id": "12345678-1234-5678-1234-567812345678"' in encoded
    assert '"amount": 199.95' in encoded
    assert '"permissions": ["read", "write"]' in encoded
    assert '"timestamp": "2026-10-19T12:00:00+00:00"' in encoded
    print("=== Q2: Custom JSONEncoder Verified ===")


# ==============================================================================
# Question 3: Custom Deserialization with object_hook
# ==============================================================================
class UserAccount:
    def __init__(self, username: str, user_id: int):
        self.username = username
        self.user_id = user_id

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, UserAccount) and self.username == other.username and self.user_id == other.user_id


def user_account_decoder(d: Dict[str, Any]) -> Any:
    """object_hook reconstructing UserAccount when __type__ is UserAccount."""
    if d.get("__type__") == "UserAccount":
        return UserAccount(username=d["username"], user_id=d["user_id"])
    return d


def test_q3_object_hook():
    raw_json = '{"user": {"__type__": "UserAccount", "username": "alice", "user_id": 101}, "status": "active"}'
    parsed = json.loads(raw_json, object_hook=user_account_decoder)

    assert isinstance(parsed["user"], UserAccount)
    assert parsed["user"].username == "alice"
    assert parsed["user"].user_id == 101
    assert parsed["status"] == "active"
    print("=== Q3: Custom Deserialization with object_hook Verified ===")


# ==============================================================================
# Question 4: JSON Lines (JSONL) Streaming Engine
# ==============================================================================
def write_json_lines(filepath: str, records: List[Dict[str, Any]]) -> None:
    """Writes list of records as newline-delimited JSON Lines (.jsonl)."""
    with open(filepath, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")


def stream_json_lines(filepath: str):
    """Generator streaming parsed records from .jsonl file line by line."""
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def test_q4_jsonl_streaming(tmp_path: str = "temp_records.jsonl"):
    records = [
        {"event": "login", "user": "alice", "ts": 100},
        {"event": "query", "user": "bob", "ts": 101},
        {"event": "logout", "user": "alice", "ts": 102},
    ]
    try:
        write_json_lines(tmp_path, records)
        streamed = list(stream_json_lines(tmp_path))
        assert streamed == records
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    print("=== Q4: JSON Lines (JSONL) Streaming Engine Verified ===")


# ==============================================================================
# Question 5: Error Diagnostics & Malformed Recovery
# ==============================================================================
def safe_parse_json(raw_json: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Parses JSON safely. If a syntax error occurs, captures exact line and col.
    Returns (data, error_diagnostic).
    """
    try:
        return json.loads(raw_json), None
    except json.JSONDecodeError as err:
        diag = f"JSONDecodeError at line {err.lineno}, col {err.colno}: {err.msg}"
        return None, diag


def repair_common_json_issues(malformed_json: str) -> str:
    """Repairs single quotes to double quotes and removes trailing commas before closing braces."""
    repaired = malformed_json.strip()
    # Replace single quotes with double quotes
    if "'" in repaired and '"' not in repaired:
        repaired = repaired.replace("'", '"')
    # Remove trailing commas like ', }' or ', ]'
    repaired = repaired.replace(",\n}", "\n}").replace(",\n]", "\n]").replace(", }", " }").replace(", ]", " ]")
    return repaired


def test_q5_error_diagnostics_and_repair():
    bad_json = '{\n  "key": "value",\n  "invalid": \n}'
    data, diag = safe_parse_json(bad_json)
    assert data is None
    assert "line 4" in diag

    single_quoted = "{'key': 'value'}"
    repaired_str = repair_common_json_issues(single_quoted)
    fixed_data = json.loads(repaired_str)
    assert fixed_data == {"key": "value"}
    print("=== Q5: Error Diagnostics & Malformed Recovery Verified ===")


# ==============================================================================
# Question 6: Circular Reference Detection
# ==============================================================================
def test_q6_circular_reference_detection():
    node_a = {"name": "NodeA"}
    node_b = {"name": "NodeB"}
    # Create circular reference
    node_a["link"] = node_b
    node_b["link"] = node_a

    try:
        json.dumps(node_a, check_circular=True)
        assert False, "Should raise ValueError on circular reference"
    except ValueError as err:
        assert "Circular reference detected" in str(err)
    print("=== Q6: Circular Reference Detection Verified ===")


# ==============================================================================
# Question 7: Deep Filtering and PII Masking
# ==============================================================================
def mask_pii_in_json(node: Any, pii_keys: Set[str], mask_value: str = "***REDACTED***") -> Any:
    """Recursively traverses nested dictionaries/lists and redacts keys in pii_keys."""
    if isinstance(node, dict):
        result = {}
        for k, v in node.items():
            if k.lower() in pii_keys:
                result[k] = mask_value
            else:
                result[k] = mask_pii_in_json(v, pii_keys, mask_value)
        return result
    elif isinstance(node, list):
        return [mask_pii_in_json(elem, pii_keys, mask_value) for elem in node]
    return node


def test_q7_pii_masking():
    payload = {
        "user": {"name": "Alice", "ssn": "123-45-6789", "email": "alice@example.com"},
        "accounts": [
            {"account_number": "ACC-999", "password_hash": "secret_hash"},
        ],
    }
    pii_fields = {"ssn", "password_hash"}
    masked = mask_pii_in_json(payload, pii_fields)

    assert masked["user"]["name"] == "Alice"
    assert masked["user"]["ssn"] == "***REDACTED***"
    assert masked["accounts"][0]["password_hash"] == "***REDACTED***"
    assert masked["accounts"][0]["account_number"] == "ACC-999"
    print("=== Q7: Deep Filtering and PII Masking Verified ===")


# ==============================================================================
# Question 8: Minification vs Pretty-Printing
# ==============================================================================
def minify_json(json_str: str) -> str:
    """Minifies JSON by stripping whitespace and using compact separators."""
    data = json.loads(json_str)
    return json.dumps(data, separators=(",", ":"))


def test_q8_minification():
    pretty_json = """
    {
      "title": "Document",
      "author": "Alice",
      "tags": [
        "python",
        "data"
      ]
    }
    """
    minified = minify_json(pretty_json)
    assert " " not in minified
    assert "\n" not in minified
    assert len(minified) < len(pretty_json) // 2
    assert json.loads(minified) == json.loads(pretty_json)
    print("=== Q8: Minification vs Pretty-Printing Verified ===")


# ==============================================================================
# Question 9: High-Precision Decimal Numeric Parsing
# ==============================================================================
def parse_financial_json_exact(json_str: str) -> Dict[str, Any]:
    """Parses JSON numbers into exact Python Decimals to avoid float precision loss."""
    return json.loads(json_str, parse_float=Decimal)


def test_q9_exact_decimal_parsing():
    # 0.1 + 0.2 in standard IEEE 754 float is 0.30000000000000004
    raw = '{"amount_a": 0.1, "amount_b": 0.2}'
    data = parse_financial_json_exact(raw)

    assert isinstance(data["amount_a"], Decimal)
    assert isinstance(data["amount_b"], Decimal)
    assert data["amount_a"] + data["amount_b"] == Decimal("0.3")
    print("=== Q9: High-Precision Decimal Numeric Parsing Verified ===")


# ==============================================================================
# Question 10: Architectural Crash-Resilient JSON Document Store
# ==============================================================================
class JsonDocumentStore:
    """
    Production crash-resilient file-backed JSON document store:
    - Maintains in-memory indexed collection
    - Writes atomically via temporary file and atomic os.replace to prevent corruption
    - Querying by field filter predicates
    """
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self._documents: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r", encoding="utf-8") as f:
                self._documents = json.load(f)

    def _persist_atomic(self):
        temp_path = f"{self.storage_path}.tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(self._documents, f, indent=2)
        # Atomic replace guarantees file is never half-written or corrupted
        os.replace(temp_path, self.storage_path)

    def insert(self, doc_id: str, document: Dict[str, Any]) -> None:
        self._documents[doc_id] = document
        self._persist_atomic()

    def get(self, doc_id: str) -> Optional[Dict[str, Any]]:
        return self._documents.get(doc_id)

    def query(self, predicate: Any) -> List[Dict[str, Any]]:
        return [doc for doc in self._documents.values() if predicate(doc)]

    def delete(self, doc_id: str) -> bool:
        if doc_id in self._documents:
            del self._documents[doc_id]
            self._persist_atomic()
            return True
        return False


def test_q10_json_document_store(store_path: str = "temp_store.json"):
    try:
        store = JsonDocumentStore(store_path)
        store.insert("doc_1", {"type": "invoice", "total": 500, "status": "PAID"})
        store.insert("doc_2", {"type": "invoice", "total": 1200, "status": "PENDING"})
        store.insert("doc_3", {"type": "receipt", "total": 50, "status": "PAID"})

        # Query
        pending_invoices = store.query(lambda d: d.get("status") == "PENDING")
        assert len(pending_invoices) == 1
        assert pending_invoices[0]["total"] == 1200

        # Reload from disk into new store instance
        store2 = JsonDocumentStore(store_path)
        assert store2.get("doc_1") == {"type": "invoice", "total": 500, "status": "PAID"}
        assert store2.delete("doc_1") is True
        assert store2.get("doc_1") is None
    finally:
        if os.path.exists(store_path):
            os.remove(store_path)
        if os.path.exists(f"{store_path}.tmp"):
            os.remove(f"{store_path}.tmp")
    print("=== Q10: Architectural Crash-Resilient JSON Document Store Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_core_json()
    test_q2_custom_json_encoder()
    test_q3_object_hook()
    test_q4_jsonl_streaming()
    test_q5_error_diagnostics_and_repair()
    test_q6_circular_reference_detection()
    test_q7_pii_masking()
    test_q8_minification()
    test_q9_exact_decimal_parsing()
    test_q10_json_document_store()
    print("\nAll 10 JSON read/write practice questions passed successfully!")
