"""
Topic 12: JSON, CSV, API, Database
Question 02: CSV Processing

A comprehensive, production-grade guide to CSV and tabular delimiter processing in Python.
Covers csv.reader/csv.writer, csv.DictReader/csv.DictWriter, custom dialects, csv.Sniffer,
streaming chunk aggregations, schema validation, hierarchical grouping, formula injection
mitigation, and atomic sanitization pipelines.

Every question contains standalone runnable exercises verified with 100% assertions.
"""

import csv
import io
import os
import tempfile
import hashlib
from datetime import date
from typing import List, Dict, Any, Generator, Tuple, Optional


# =====================================================================
# Q1: Basic csv.reader, csv.writer, and Quoting Strategies
# =====================================================================
def q1_csv_reader_writer_quoting():
    """
    Demonstrates low-level row-based reading and writing using csv.reader and csv.writer,
    illustrating standard quoting mechanisms: QUOTE_MINIMAL, QUOTE_ALL, and QUOTE_NONNUMERIC.
    """
    headers = ["ID", "Name", "Score", "Notes"]
    rows = [
        [101, "Alice Smith", 95.5, "Passed, with honors"],
        [102, "Bob O'Reilly", 82.0, "Standard pass"],
        [103, "Charlie \"Chuck\"", 74.0, "Needs review\nretake possible"],
    ]

    # Write using QUOTE_MINIMAL
    buffer_minimal = io.StringIO()
    writer_min = csv.writer(buffer_minimal, quoting=csv.QUOTE_MINIMAL)
    writer_min.writerow(headers)
    writer_min.writerows(rows)
    content_min = buffer_minimal.getvalue()

    # The comma in Alice's note forces quotes; quotes in Charlie's name are escaped
    assert '"Passed, with honors"' in content_min
    assert 'Charlie ""Chuck""' in content_min

    # Read back and parse
    buffer_minimal.seek(0)
    reader = csv.reader(buffer_minimal)
    read_headers = next(reader)
    read_rows = list(reader)

    assert read_headers == headers
    assert len(read_rows) == 3
    assert read_rows[0][1] == "Alice Smith"
    assert read_rows[0][3] == "Passed, with honors"
    assert read_rows[2][1] == 'Charlie "Chuck"'

    # Write using QUOTE_NONNUMERIC (numbers unquoted, non-numbers quoted)
    buffer_nonnum = io.StringIO()
    writer_nonnum = csv.writer(buffer_nonnum, quoting=csv.QUOTE_NONNUMERIC)
    writer_nonnum.writerow(["Rank", "Score", "Active"])
    writer_nonnum.writerow([1, 98.75, "Yes"])
    content_nonnum = buffer_nonnum.getvalue()

    # In QUOTE_NONNUMERIC, "1" as int is rendered 1 without quotes; "Yes" has quotes
    lines = content_nonnum.strip().splitlines()
    assert lines[0] == '"Rank","Score","Active"'
    assert lines[1] == '1,98.75,"Yes"'

    print("=== Q1: Basic csv.reader & csv.writer with Quoting Verified ===")


# =====================================================================
# Q2: csv.DictReader and csv.DictWriter with Missing and Extra Fields
# =====================================================================
def q2_dict_reader_dict_writer():
    """
    Demonstrates dictionary-based CSV processing, handling missing values with restval
    and extra unexpected columns with restkey.
    """
    records = [
        {"sku": "A100", "product": "Mechanical Keyboard", "price": "129.99", "in_stock": "True"},
        {"sku": "B200", "product": "Ergonomic Mouse", "price": "59.50"}, # missing in_stock
    ]
    fieldnames = ["sku", "product", "price", "in_stock"]

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, restval="False")
    writer.writeheader()
    for rec in records:
        writer.writerow(rec)

    output = buffer.getvalue()
    lines = [line.strip() for line in output.strip().splitlines()]
    assert lines[0] == "sku,product,price,in_stock"
    assert lines[1] == "A100,Mechanical Keyboard,129.99,True"
    assert lines[2] == "B200,Ergonomic Mouse,59.50,False"

    # Reading a CSV containing extra undeclared columns using restkey
    csv_extra = "sku,product,price\nC300,Monitor,299.99,Warehouse_A,Shelving_4\n"
    reader_buf = io.StringIO(csv_extra)
    dict_reader = csv.DictReader(reader_buf, restkey="overflow_data")
    parsed = list(dict_reader)

    assert len(parsed) == 1
    row = parsed[0]
    assert row["sku"] == "C300"
    assert row["price"] == "299.99"
    assert row["overflow_data"] == ["Warehouse_A", "Shelving_4"]

    print("=== Q2: DictReader and DictWriter Verified ===")


# =====================================================================
# Q3: Custom Dialect Registration and Specification
# =====================================================================
def q3_custom_dialects():
    """
    Registers a custom CSV dialect with pipe delimiters, custom escape characters,
    and strict quote handling, verifying portability across readers and writers.
    """
    dialect_name = "pipe_custom_v1"
    if dialect_name in csv.list_dialects():
        csv.unregister_dialect(dialect_name)

    csv.register_dialect(
        dialect_name,
        delimiter="|",
        quotechar="'",
        escapechar="\\",
        doublequote=False,
        quoting=csv.QUOTE_MINIMAL,
        lineterminator="\n"
    )

    data = [
        ["user_id", "tag", "description"],
        [1, "dev", "Software 'Lead' | Architect"],
        [2, "ops", "Site Reliability Engineer"],
    ]

    buffer = io.StringIO()
    writer = csv.writer(buffer, dialect=dialect_name)
    writer.writerows(data)
    rendered = buffer.getvalue()

    # The pipe in "Lead' | Architect" must force quoting or escaping
    lines = rendered.strip().split("\n")
    assert lines[0] == "user_id|tag|description"
    assert "Software \\'Lead\\' | Architect" in lines[1] or "'Software \\'Lead\\' | Architect'" in lines[1]

    # Read back with same dialect
    buffer.seek(0)
    reader = csv.reader(buffer, dialect=dialect_name)
    parsed = list(reader)
    assert parsed[0] == ["user_id", "tag", "description"]
    assert parsed[1][2] == "Software 'Lead' | Architect"

    # Clean up dialect
    csv.unregister_dialect(dialect_name)
    assert dialect_name not in csv.list_dialects()

    print("=== Q3: Custom Dialect Registration Verified ===")


# =====================================================================
# Q4: Automatic Dialect and Header Sniffing with csv.Sniffer
# =====================================================================
def q4_csv_sniffer_inspection():
    """
    Demonstrates using csv.Sniffer to automatically deduce unknown delimiters
    (tab, semicolon, comma) and determine if the sample data includes a header row.
    """
    sample_tsv = (
        "employee_id\tfull_name\tdepartment\tsalary\n"
        "E001\tDavid Vance\tEngineering\t120000\n"
        "E002\tSarah Miller\tData Science\t135000\n"
        "E003\tKiran Rao\tProduct\t115000\n"
    )

    sniffer = csv.Sniffer()
    has_header = sniffer.has_header(sample_tsv)
    assert has_header is True

    dialect = sniffer.sniff(sample_tsv)
    assert dialect.delimiter == "\t"

    reader = csv.reader(io.StringIO(sample_tsv), dialect=dialect)
    rows = list(reader)
    assert len(rows) == 4
    assert rows[0] == ["employee_id", "full_name", "department", "salary"]
    assert rows[1][1] == "David Vance"

    # Semicolon-delimited sample without header
    sample_semicolon_no_header = (
        "100;apple;0.50\n"
        "200;banana;0.25\n"
        "300;cherry;1.50\n"
    )
    assert sniffer.has_header(sample_semicolon_no_header) is False
    dialect_sc = sniffer.sniff(sample_semicolon_no_header)
    assert dialect_sc.delimiter == ";"

    print("=== Q4: csv.Sniffer Dialect Deduction Verified ===")


# =====================================================================
# Q5: Robust Type-Casting and Schema Validation Pipeline
# =====================================================================
class CSVValidationError(Exception):
    def __init__(self, row_index: int, field: str, raw_value: str, reason: str):
        super().__init__(f"Row {row_index} invalid on '{field}'='{raw_value}': {reason}")
        self.row_index = row_index
        self.field = field
        self.raw_value = raw_value
        self.reason = reason


def parse_and_validate_csv(csv_content: str) -> Tuple[List[Dict[str, Any]], List[CSVValidationError]]:
    """
    Parses CSV data into typed Python primitives with schema validation and error reporting.
    Schema:
      - id: positive int
      - name: non-empty string
      - join_date: YYYY-MM-DD date
      - balance: float
      - active: boolean ('true'/'false' case-insensitive)
    """
    reader = csv.DictReader(io.StringIO(csv_content))
    valid_records = []
    errors = []

    for idx, row in enumerate(reader, start=1):
        err = None
        # Validate ID
        try:
            row_id = int(row["id"])
            if row_id <= 0:
                raise ValueError("Must be > 0")
        except Exception as e:
            errors.append(CSVValidationError(idx, "id", row.get("id", ""), str(e)))
            continue

        # Validate Name
        name = row.get("name", "").strip()
        if not name:
            errors.append(CSVValidationError(idx, "name", row.get("name", ""), "Cannot be blank"))
            continue

        # Validate Date
        try:
            join_date = date.fromisoformat(row["join_date"])
        except Exception as e:
            errors.append(CSVValidationError(idx, "join_date", row.get("join_date", ""), "Expected YYYY-MM-DD"))
            continue

        # Validate Balance
        try:
            balance = float(row["balance"])
        except Exception as e:
            errors.append(CSVValidationError(idx, "balance", row.get("balance", ""), "Invalid numeric float"))
            continue

        # Validate Active
        active_raw = row.get("active", "").strip().lower()
        if active_raw in ("true", "1", "yes"):
            active = True
        elif active_raw in ("false", "0", "no"):
            active = False
        else:
            errors.append(CSVValidationError(idx, "active", row.get("active", ""), "Expected boolean true/false"))
            continue

        valid_records.append({
            "id": row_id,
            "name": name,
            "join_date": join_date,
            "balance": balance,
            "active": active,
        })

    return valid_records, errors


def q5_type_casting_and_schema_validation():
    sample = (
        "id,name,join_date,balance,active\n"
        "1,Alice Smith,2023-01-15,1500.50,true\n"
        "-2,Invalid ID,2023-02-01,200.0,false\n"
        "3,,2023-03-10,340.0,yes\n"
        "4,Bob Jones,invalid-date,12.50,false\n"
        "5,Charlie Brown,2023-05-20,not-a-number,true\n"
        "6,Diana Prince,2023-06-30,4200.0,maybe\n"
        "7,Ethan Hunt,2023-07-07,9999.99,TRUE\n"
    )

    valid, errors = parse_and_validate_csv(sample)
    assert len(valid) == 2
    assert valid[0]["name"] == "Alice Smith"
    assert valid[0]["join_date"] == date(2023, 1, 15)
    assert valid[1]["name"] == "Ethan Hunt"
    assert valid[1]["active"] is True

    assert len(errors) == 5
    error_fields = [e.field for e in errors]
    assert error_fields == ["id", "name", "join_date", "balance", "active"]

    print("=== Q5: Type Casting & Schema Validation Pipeline Verified ===")


# =====================================================================
# Q6: Streaming Chunk Aggregation for Memory-Constrained Datasets
# =====================================================================
def stream_csv_chunks(stream: io.StringIO, chunk_size: int = 100) -> Generator[List[Dict[str, str]], None, None]:
    """Yields batches of rows as dictionaries without loading the entire CSV."""
    reader = csv.DictReader(stream)
    chunk = []
    for row in reader:
        chunk.append(row)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def compute_streaming_summary(stream: io.StringIO, value_col: str) -> Dict[str, float]:
    """Computes total, mean, min, and max using single-pass streaming in O(1) space."""
    count = 0
    total = 0.0
    val_min = float("inf")
    val_max = float("-inf")

    for chunk in stream_csv_chunks(stream, chunk_size=5):
        for record in chunk:
            val = float(record[value_col])
            count += 1
            total += val
            if val < val_min:
                val_min = val
            if val > val_max:
                val_max = val

    return {
        "count": count,
        "total": round(total, 2),
        "mean": round(total / count, 2) if count > 0 else 0.0,
        "min": val_min,
        "max": val_max,
    }


def q6_streaming_chunk_aggregations():
    # Build 25 synthetic rows
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=["txn_id", "amount"])
    writer.writeheader()
    for i in range(1, 26):
        writer.writerow({"txn_id": f"T{i}", "amount": str(i * 10)})

    buffer.seek(0)
    summary = compute_streaming_summary(buffer, "amount")

    assert summary["count"] == 25
    assert summary["total"] == 3250.0  # sum of 10*i for i=1..25 = 10 * 325 = 3250
    assert summary["mean"] == 130.0
    assert summary["min"] == 10.0
    assert summary["max"] == 250.0

    print("=== Q6: Streaming Chunk Aggregation in O(1) Memory Verified ===")


# =====================================================================
# Q7: Multi-CSV Merge and Primary-Key Conflict Resolution
# =====================================================================
def merge_csv_records(
    primary_key: str,
    sources: List[str],
    conflict_strategy: str = "latest_timestamp"
) -> List[Dict[str, str]]:
    """
    Merges multiple CSV source strings on a primary key.
    conflict_strategy:
      - 'latest_timestamp': takes record with higher 'updated_at' ISO timestamp.
      - 'first_wins': keeps the first encountered record.
      - 'last_wins': later records unconditionally overwrite earlier ones.
    """
    merged_store: Dict[str, Dict[str, str]] = {}

    for csv_text in sources:
        reader = csv.DictReader(io.StringIO(csv_text))
        for row in reader:
            key = row[primary_key]
            if key not in merged_store:
                merged_store[key] = row
            else:
                if conflict_strategy == "last_wins":
                    merged_store[key] = row
                elif conflict_strategy == "first_wins":
                    continue
                elif conflict_strategy == "latest_timestamp":
                    curr_ts = merged_store[key].get("updated_at", "")
                    new_ts = row.get("updated_at", "")
                    if new_ts >= curr_ts:
                        merged_store[key] = row
                else:
                    raise ValueError(f"Unknown strategy: {conflict_strategy}")

    return list(merged_store.values())


def q7_csv_merge_and_conflict_resolution():
    source_a = (
        "user_id,email,plan,updated_at\n"
        "U1,alice@example.com,free,2023-01-01T10:00:00\n"
        "U2,bob@example.com,pro,2023-01-01T12:00:00\n"
    )
    source_b = (
        "user_id,email,plan,updated_at\n"
        "U1,alice@work.org,enterprise,2023-02-15T09:30:00\n" # newer update
        "U3,charlie@sample.net,free,2023-01-05T08:00:00\n"
    )

    merged = merge_csv_records(
        primary_key="user_id",
        sources=[source_a, source_b],
        conflict_strategy="latest_timestamp"
    )
    merged_by_id = {r["user_id"]: r for r in merged}

    assert len(merged_by_id) == 3
    # U1 was upgraded to enterprise in source_b
    assert merged_by_id["U1"]["email"] == "alice@work.org"
    assert merged_by_id["U1"]["plan"] == "enterprise"
    assert merged_by_id["U2"]["plan"] == "pro"
    assert merged_by_id["U3"]["plan"] == "free"

    print("=== Q7: Multi-CSV Merge & Conflict Resolution Verified ===")


# =====================================================================
# Q8: CSV Flat Records to Hierarchical Master-Detail JSON Structure
# =====================================================================
def csv_to_hierarchical_structure(csv_content: str) -> Dict[str, Any]:
    """
    Transforms flat relational CSV rows containing (dept_id, dept_name, emp_id, emp_name, role)
    into a structured hierarchical tree representation.
    """
    reader = csv.DictReader(io.StringIO(csv_content))
    departments: Dict[str, Dict[str, Any]] = {}

    for row in reader:
        d_id = row["dept_id"]
        if d_id not in departments:
            departments[d_id] = {
                "dept_id": d_id,
                "name": row["dept_name"],
                "employees": [],
                "headcount": 0
            }

        # Add employee if present
        if row.get("emp_id"):
            departments[d_id]["employees"].append({
                "emp_id": row["emp_id"],
                "name": row["emp_name"],
                "role": row["role"],
            })
            departments[d_id]["headcount"] += 1

    return {"departments": list(departments.values())}


def q8_csv_to_hierarchical_json():
    flat_csv = (
        "dept_id,dept_name,emp_id,emp_name,role\n"
        "D10,Engineering,E01,Alice Wong,Staff Engineer\n"
        "D10,Engineering,E02,Bob Taylor,Frontend Dev\n"
        "D20,Marketing,E03,Chloe Davis,SEO Specialist\n"
        "D30,Research,,,\n"  # Empty department with no employees
    )

    hierarchy = csv_to_hierarchical_structure(flat_csv)
    depts = hierarchy["departments"]
    assert len(depts) == 3

    eng = next(d for d in depts if d["dept_id"] == "D10")
    assert eng["name"] == "Engineering"
    assert eng["headcount"] == 2
    assert eng["employees"][0]["name"] == "Alice Wong"

    res = next(d for d in depts if d["dept_id"] == "D30")
    assert res["name"] == "Research"
    assert res["headcount"] == 0
    assert res["employees"] == []

    print("=== Q8: CSV Flat to Hierarchical Structuring Verified ===")


# =====================================================================
# Q9: Delimiter Converter with Embedded Newlines & Escapes
# =====================================================================
def convert_delimiter(
    input_text: str,
    src_delimiter: str,
    tgt_delimiter: str,
    src_quotechar: str = '"',
    tgt_quotechar: str = '"'
) -> str:
    """
    Safely converts arbitrary delimited input (e.g. Tab, Pipe, Comma)
    to another target delimiter, respecting quotes and embedded newlines.
    """
    input_buf = io.StringIO(input_text)
    output_buf = io.StringIO()

    reader = csv.reader(input_buf, delimiter=src_delimiter, quotechar=src_quotechar)
    writer = csv.writer(output_buf, delimiter=tgt_delimiter, quotechar=tgt_quotechar, quoting=csv.QUOTE_MINIMAL)

    for row in reader:
        writer.writerow(row)

    return output_buf.getvalue()


def q9_delimiter_conversion_and_embedded_newlines():
    # Input has pipe delimiters with embedded commas and quotes
    src_pipe_data = (
        "id|name|address\n"
        "1|Apex Corp|\"Suite 500, Tower A\"\n"
        "2|Beta LLC|\"Line 1\nLine 2\"\n"
    )

    converted_csv = convert_delimiter(src_pipe_data, src_delimiter="|", tgt_delimiter=",")
    # Verify using standard csv reader
    reader = csv.reader(io.StringIO(converted_csv))
    rows = list(reader)

    assert len(rows) == 3
    assert rows[0] == ["id", "name", "address"]
    assert rows[1] == ["1", "Apex Corp", "Suite 500, Tower A"]
    assert rows[2] == ["2", "Beta LLC", "Line 1\nLine 2"]

    print("=== Q9: Delimiter Conversion with Multi-Line Quoting Verified ===")


# =====================================================================
# Q10: Enterprise CSV Sanitizer & Formula-Injection Mitigation Pipeline
# =====================================================================
class CSVDefensePipeline:
    """
    Hardens CSV data against Formula Injection (CSV injection / DDE attacks)
    where cells beginning with '=', '+', '-', '@', '\\t', or '\\r' can execute
    arbitrary formulas in spreadsheet tools (Excel, Calc, Sheets).
    Also performs column reordering, PII anonymization, and atomic writing.
    """
    INJECTION_TRIGGERS = ("=", "+", "-", "@", "\t", "\r")

    def __init__(self, target_columns: List[str], pii_columns: Optional[List[str]] = None):
        self.target_columns = target_columns
        self.pii_columns = set(pii_columns or [])

    @classmethod
    def sanitize_field(cls, value: str) -> str:
        """Prefaces dangerous formula prefix characters with a single quote."""
        if not isinstance(value, str):
            value = str(value)
        trimmed = value.lstrip()
        if trimmed and trimmed.startswith(cls.INJECTION_TRIGGERS):
            # Prepend single quote so spreadsheets treat formula as literal text
            return "'" + value
        return value

    def hash_pii(self, value: str) -> str:
        """Replaces sensitive PII values with deterministic SHA-256 digests."""
        if not value:
            return ""
        return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]

    def process_row(self, row: Dict[str, str]) -> Dict[str, str]:
        sanitized = {}
        for col in self.target_columns:
            raw_val = row.get(col, "")
            if col in self.pii_columns:
                processed_val = self.hash_pii(raw_val)
            else:
                processed_val = self.sanitize_field(raw_val)
            sanitized[col] = processed_val
        return sanitized

    def process_file_atomically(self, input_path: str, output_path: str) -> int:
        """Reads input_path, processes, and writes atomically to output_path."""
        rows_processed = 0
        output_dir = os.path.dirname(os.path.abspath(output_path))

        with open(input_path, mode="r", encoding="utf-8", newline="") as infile:
            reader = csv.DictReader(infile)
            temp_file = tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                newline="",
                dir=output_dir,
                delete=False
            )
            temp_name = temp_file.name
            try:
                writer = csv.DictWriter(temp_file, fieldnames=self.target_columns)
                writer.writeheader()
                for row in reader:
                    cleaned_row = self.process_row(row)
                    writer.writerow(cleaned_row)
                    rows_processed += 1
                temp_file.flush()
                os.fsync(temp_file.fileno())
                temp_file.close()

                # Atomic file replacement
                os.replace(temp_name, output_path)
            except Exception:
                temp_file.close()
                if os.path.exists(temp_name):
                    os.remove(temp_name)
                raise

        return rows_processed


def q10_enterprise_csv_sanitizer_and_formula_defense():
    temp_dir = tempfile.mkdtemp()
    in_file = os.path.join(temp_dir, "input_unsafe.csv")
    out_file = os.path.join(temp_dir, "output_sanitized.csv")

    try:
        # Create input containing malicious spreadsheet formula injections and PII
        raw_csv = (
            "id,user_ssn,customer_name,comment\n"
            "1,123-45-6789,Alice,=cmd|' /C calc'!A0\n"
            "2,987-65-4321,Bob,+1+2\n"
            "3,555-55-5555,Charlie,@SUM(1+1)\n"
            "4,333-33-3333,Diana,-10*5\n"
        )
        with open(in_file, "w", encoding="utf-8", newline="") as f:
            f.write(raw_csv)

        pipeline = CSVDefensePipeline(
            target_columns=["id", "customer_name", "user_ssn", "comment"],
            pii_columns=["user_ssn"]
        )
        processed_count = pipeline.process_file_atomically(in_file, out_file)
        assert processed_count == 4

        # Read back sanitized output
        with open(out_file, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # 1. Formula injection neutralization: prepended with "'"
        assert rows[0]["comment"] == "'=cmd|' /C calc'!A0"
        assert rows[1]["comment"] == "'+1+2"
        assert rows[2]["comment"] == "'@SUM(1+1)"
        assert rows[3]["comment"] == "'-10*5"

        # 2. PII hashed
        assert rows[0]["user_ssn"] != "123-45-6789"
        assert len(rows[0]["user_ssn"]) == 16
        assert rows[0]["user_ssn"] == hashlib.sha256("123-45-6789".encode("utf-8")).hexdigest()[:16]

        # 3. Clean columns maintained
        assert rows[0]["customer_name"] == "Alice"

    finally:
        for p in (in_file, out_file):
            if os.path.exists(p):
                os.remove(p)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)

    print("=== Q10: Enterprise CSV Sanitizer & Formula Injection Defense Verified ===")


# =====================================================================
# Main Test Runner
# =====================================================================
if __name__ == "__main__":
    q1_csv_reader_writer_quoting()
    q2_dict_reader_dict_writer()
    q3_custom_dialects()
    q4_csv_sniffer_inspection()
    q5_type_casting_and_schema_validation()
    q6_streaming_chunk_aggregations()
    q7_csv_merge_and_conflict_resolution()
    q8_csv_to_hierarchical_json()
    q9_delimiter_conversion_and_embedded_newlines()
    q10_enterprise_csv_sanitizer_and_formula_defense()

    print("\nAll 10 CSV processing practice questions passed successfully!")
