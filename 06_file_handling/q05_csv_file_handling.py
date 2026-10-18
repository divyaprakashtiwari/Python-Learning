"""
Topic 06: File Handling - Question 05: CSV File Handling

A comprehensive collection of 10 standalone, runnable exercises exploring
CSV (Comma-Separated Values) processing using Python's built-in `csv` module.

Questions Covered:
 1. csv.reader Basics: Parsing rows, row iteration, skipping headers, and type casting.
 2. csv.writer Mechanics: Writing rows (writerow vs writerows) and the Windows newline='' rule.
 3. csv.DictReader: Mapping rows to dictionaries, custom fieldnames, restkey, and restval.
 4. csv.DictWriter: Structuring dictionary exports, writeheader(), and extrasaction handling.
 5. Custom Delimiters & Separators: TSV (tabs), semicolons, and pipe-delimited formats.
 6. Quoting Modes: QUOTE_MINIMAL, QUOTE_ALL, QUOTE_NONNUMERIC, and quotechar/escapechar.
 7. Dialects & csv.Sniffer: Registering custom dialects and sniffing unknown CSV formats.
 8. Complex Fields: Multiline cells, embedded commas, quotes, and Excel UTF-8-SIG BOM.
 9. Memory-Efficient Streaming & Filtering: Generator-based row-by-row data transformation.
10. Advanced Project: CSV ETL & Schema Validation Pipeline with cleansing and aggregated metrics.
"""

import csv
import io
import os
import shutil
import tempfile
from typing import Any, Generator


# ==============================================================================
# Question 1: csv.reader Basics
# ==============================================================================
def exercise_q1_csv_reader_basics() -> None:
    """
    Demonstrate reading basic CSV data using csv.reader, skipping headers with
    next(), and parsing string rows into strongly typed data records.
    """
    print("=== Q1: csv.reader Basics ===")

    csv_data = """id,product,price,quantity
1,Keyboard,49.99,10
2,Mouse,24.50,25
3,Monitor,199.00,5
"""
    stream = io.StringIO(csv_data.strip())
    reader = csv.reader(stream)

    header = next(reader)
    assert header == ["id", "product", "price", "quantity"]

    records = []
    for row in reader:
        item = {
            "id": int(row[0]),
            "product": row[1],
            "price": float(row[2]),
            "quantity": int(row[3]),
        }
        records.append(item)

    assert len(records) == 3
    assert records[0]["product"] == "Keyboard"
    assert records[1]["price"] == 24.50
    assert records[2]["quantity"] == 5

    total_inventory_value = sum(r["price"] * r["quantity"] for r in records)
    assert round(total_inventory_value, 2) == 2107.40

    print(f"  Header parsed: {header}")
    print(f"  Total records parsed: {len(records)}")
    print(f"  Calculated total inventory value: ${total_inventory_value:.2f}")


# ==============================================================================
# Question 2: csv.writer Mechanics & Windows newline='' Rule
# ==============================================================================
def exercise_q2_csv_writer_mechanics() -> None:
    """
    Demonstrate csv.writer with writerow and writerows. Explain the critical
    requirement of passing newline='' when opening files to prevent double-spaced
    CRCRLF line breaks on Windows.
    """
    print("\n=== Q2: csv.writer Mechanics & Windows newline='' Rule ===")

    temp_dir = tempfile.mkdtemp(prefix="csv_writer_")
    file_path = os.path.join(temp_dir, "employees.csv")

    try:
        # Note: newline='' is mandatory per Python csv documentation
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Write single header row
            writer.writerow(["emp_id", "name", "department", "active"])
            # Write multiple rows at once
            rows = [
                [101, "Alice Walker", "Engineering", True],
                [102, "Bob Martin", "Marketing", False],
                [103, "Charlie Davis", "Sales", True],
            ]
            writer.writerows(rows)

        # Verify read back
        with open(file_path, mode="r", newline="", encoding="utf-8") as f:
            lines = f.readlines()

        assert len(lines) == 4
        assert lines[0].strip() == "emp_id,name,department,active"
        assert lines[1].strip() == "101,Alice Walker,Engineering,True"

        print(f"  Successfully wrote {len(lines)} lines to {file_path}")
        print(f"  First line: {lines[0].strip()}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 3: csv.DictReader Mapping & Handling Missing/Extra Columns
# ==============================================================================
def exercise_q3_dict_reader() -> None:
    """
    Demonstrate csv.DictReader to automatically map rows into dictionaries.
    Handle missing columns using `restval` and extraneous columns using `restkey`.
    """
    print("\n=== Q3: csv.DictReader Mapping ===")

    # Row 2 has only 2 columns (missing role)
    # Row 3 has 4 columns (extra salary)
    ragged_csv = """name,dept,role
Alice,Engineering,Lead
Bob,Support
Charlie,Sales,Associate,95000
"""
    stream = io.StringIO(ragged_csv.strip())
    reader = csv.DictReader(stream, restval="<N/A>", restkey="extra_fields")

    rows = list(reader)
    assert len(rows) == 3

    # Row 1: complete
    assert rows[0] == {"name": "Alice", "dept": "Engineering", "role": "Lead"}
    # Row 2: missing role filled by restval
    assert rows[1]["role"] == "<N/A>"
    # Row 3: extra column captured in restkey list
    assert rows[2]["extra_fields"] == ["95000"]

    print(f"  Fieldnames deduced: {reader.fieldnames}")
    print(f"  Row 1: {rows[0]}")
    print(f"  Row 2 (missing role): {rows[1]}")
    print(f"  Row 3 (extra fields): {rows[2]}")


# ==============================================================================
# Question 4: csv.DictWriter & Extras Handling
# ==============================================================================
def exercise_q4_dict_writer() -> None:
    """
    Demonstrate csv.DictWriter, writeheader(), and handling unexpected keys
    with extrasaction='ignore' vs extrasaction='raise'.
    """
    print("\n=== Q4: csv.DictWriter & Extras Handling ===")

    stream = io.StringIO()
    fields = ["id", "username", "email"]

    # Use extrasaction='ignore' so unexpected dictionary keys are safely omitted
    writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()

    users = [
        {"id": 1, "username": "alice", "email": "alice@corp.internal", "temp_token": "secret1"},
        {"id": 2, "username": "bob", "email": "bob@corp.internal", "temp_token": "secret2"},
    ]
    for user in users:
        writer.writerow(user)

    output = stream.getvalue()
    lines = output.strip().splitlines()

    assert lines[0] == "id,username,email"
    assert lines[1] == "1,alice,alice@corp.internal"
    assert "secret1" not in output

    # Demonstrate extrasaction='raise'
    strict_stream = io.StringIO()
    strict_writer = csv.DictWriter(strict_stream, fieldnames=fields, extrasaction="raise")
    try:
        strict_writer.writerow({"id": 3, "username": "claire", "email": "c@c.com", "role": "admin"})
        assert False, "Should have raised ValueError for extra keys"
    except ValueError as err:
        assert "role" in str(err)

    print(f"  DictWriter generated rows safely ignoring extra keys:\n{output.strip()}")


# ==============================================================================
# Question 5: Custom Delimiters (TSV, Pipe, Semicolon)
# ==============================================================================
def exercise_q5_custom_delimiters() -> None:
    """
    Process non-comma separated delimited formats: Tab-Separated Values (TSV)
    and Pipe-Delimited (|) files.
    """
    print("\n=== Q5: Custom Delimiters ===")

    tsv_data = "sku\tdescription\tstock\nSKU-01\tWidget Alpha\t140\nSKU-02\tGadget Beta\t92"
    pipe_data = "user_id|session_id|duration\nu1|sess_99|12.5\nu2|sess_42|8.0"

    # TSV parsing
    tsv_stream = io.StringIO(tsv_data)
    tsv_reader = csv.reader(tsv_stream, delimiter="\t")
    tsv_rows = list(tsv_reader)
    assert tsv_rows[0] == ["sku", "description", "stock"]
    assert tsv_rows[1] == ["SKU-01", "Widget Alpha", "140"]

    # Pipe-delimited parsing
    pipe_stream = io.StringIO(pipe_data)
    pipe_reader = csv.DictReader(pipe_stream, delimiter="|")
    pipe_rows = list(pipe_reader)
    assert len(pipe_rows) == 2
    assert pipe_rows[0]["user_id"] == "u1"
    assert pipe_rows[1]["duration"] == "8.0"

    print(f"  TSV row count: {len(tsv_rows)}")
    print(f"  Pipe DictReader row 0: {pipe_rows[0]}")


# ==============================================================================
# Question 6: Quoting Modes & Escape Characters
# ==============================================================================
def exercise_q6_quoting_modes() -> None:
    """
    Explore different csv quoting strategies:
    QUOTE_MINIMAL (default), QUOTE_ALL, QUOTE_NONNUMERIC, and QUOTE_NONE.
    """
    print("\n=== Q6: Quoting Modes & Escape Characters ===")

    data = [
        ["product", "code", "price"],
        ["Coffee Mug", "MUG,RED", 12.50],
        ["Notebook", "NB-01", 5.00],
    ]

    # 1. QUOTE_MINIMAL: quotes only fields containing delimiter or quotechar
    s_min = io.StringIO()
    w_min = csv.writer(s_min, quoting=csv.QUOTE_MINIMAL)
    w_min.writerows(data)
    min_res = s_min.getvalue()
    # "MUG,RED" has a comma, so it must be quoted
    assert '"MUG,RED"' in min_res
    assert '"Coffee Mug"' not in min_res

    # 2. QUOTE_ALL: quotes every single field regardless of content
    s_all = io.StringIO()
    w_all = csv.writer(s_all, quoting=csv.QUOTE_ALL)
    w_all.writerows(data)
    all_res = s_all.getvalue()
    assert '"Coffee Mug"' in all_res
    assert '"12.5"' in all_res

    # 3. QUOTE_NONNUMERIC: quotes strings and casts non-quoted numbers automatically
    s_non = io.StringIO()
    w_non = csv.writer(s_non, quoting=csv.QUOTE_NONNUMERIC)
    w_non.writerows(data)
    non_res = s_non.getvalue()
    # Headers are strings -> quoted; numbers (12.5) are unquoted
    assert '"Coffee Mug"' in non_res
    assert ',12.5' in non_res

    # Reader with QUOTE_NONNUMERIC converts unquoted fields directly to float!
    read_non = io.StringIO(non_res)
    parsed = list(csv.reader(read_non, quoting=csv.QUOTE_NONNUMERIC))
    assert isinstance(parsed[1][2], float)
    assert parsed[1][2] == 12.50

    print("  QUOTE_MINIMAL output snippet:\n    " + min_res.splitlines()[1])
    print("  QUOTE_ALL output snippet:\n    " + all_res.splitlines()[1])
    print("  QUOTE_NONNUMERIC parsed numeric float directly:", parsed[1][2])


# ==============================================================================
# Question 7: Dialects & csv.Sniffer
# ==============================================================================
def exercise_q7_dialects_and_sniffer() -> None:
    """
    Demonstrate registering a reusable custom dialect and using csv.Sniffer to
    automatically detect delimiters and the presence of a header row.
    """
    print("\n=== Q7: Dialects & csv.Sniffer ===")

    # Register custom dialect
    dialect_name = "semicolon_custom"
    if dialect_name in csv.list_dialects():
        csv.unregister_dialect(dialect_name)

    csv.register_dialect(
        dialect_name,
        delimiter=";",
        quoting=csv.QUOTE_MINIMAL,
        lineterminator="\n",
    )

    sample_output = io.StringIO()
    writer = csv.writer(sample_output, dialect=dialect_name)
    writer.writerow(["host", "port", "env"])
    writer.writerow(["127.0.0.1", 5432, "dev"])

    assert "host;port;env" in sample_output.getvalue()

    # csv.Sniffer auto-detection
    raw_sample = "name|age|city\nAlice|30|Seattle\nBob|25|Austin\n"
    sniffer = csv.Sniffer()

    has_header = sniffer.has_header(raw_sample)
    detected_dialect = sniffer.sniff(raw_sample)

    assert has_header is True
    assert detected_dialect.delimiter == "|"

    # Read using detected dialect
    sniffer_stream = io.StringIO(raw_sample)
    reader = csv.reader(sniffer_stream, dialect=detected_dialect)
    header = next(reader)
    assert header == ["name", "age", "city"]

    print(f"  Registered and tested dialect: {dialect_name}")
    print(f"  Sniffer detected delimiter: '{detected_dialect.delimiter}'")
    print(f"  Sniffer detected header: {has_header}")


# ==============================================================================
# Question 8: Multiline Cells, Quotes & Excel UTF-8-SIG BOM
# ==============================================================================
def exercise_q8_complex_multiline_and_bom() -> None:
    """
    Process CSV files containing complex nested features: multiline text cells,
    escaped double quotes (""), and Excel UTF-8-SIG Byte Order Mark (BOM).
    """
    print("\n=== Q8: Multiline Cells, Quotes & Excel UTF-8-SIG BOM ===")

    # Embedded newline inside quotes and escaped quote ("" inside quotes)
    complex_data = (
        'id,description,status\n'
        '1,"Line 1 of description\nLine 2 of description with ""quoted"" word",OK\n'
        '2,"Simple text",OK\n'
    )
    stream = io.StringIO(complex_data)
    reader = csv.reader(stream)
    rows = list(reader)

    assert len(rows) == 3
    # Check that multiline cell was properly preserved as a single string
    multiline_cell = rows[1][1]
    assert "\n" in multiline_cell
    assert 'with "quoted" word' in multiline_cell

    # UTF-8 with BOM (utf-8-sig) - standard for opening CSVs cleanly in Microsoft Excel
    temp_dir = tempfile.mkdtemp(prefix="csv_bom_")
    bom_file = os.path.join(temp_dir, "excel_export.csv")

    try:
        # Writing with utf-8-sig automatically prefixes file with bytes \xef\xbb\xbf
        with open(bom_file, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["item", "price"])
            w.writerow(["Cafe Latte", "4.50"])

        # Reading with standard 'utf-8' exposes the raw BOM char '\ufeff'
        with open(bom_file, "r", encoding="utf-8") as f:
            raw_text = f.read()
            assert raw_text.startswith("\ufeff")

        # Reading with 'utf-8-sig' strips the BOM cleanly!
        with open(bom_file, "r", newline="", encoding="utf-8-sig") as f:
            clean_reader = csv.reader(f)
            first_header = next(clean_reader)[0]
            assert first_header == "item"
            assert not first_header.startswith("\ufeff")

        print("  Multiline field parsed successfully:")
        print(f"    Lines in cell: {len(multiline_cell.splitlines())}")
        print("  Excel UTF-8-SIG BOM handled cleanly without polluting fieldnames.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 9: Memory-Efficient Streaming & Filtering
# ==============================================================================
def csv_stream_filter(
    source_stream: io.StringIO,
    min_score: float,
) -> Generator[dict[str, Any], None, None]:
    """
    Generator that processes CSV rows lazily one-by-one, filtering rows
    without buffering the dataset in memory.
    """
    reader = csv.DictReader(source_stream)
    for row in reader:
        score = float(row["score"])
        if score >= min_score:
            yield {
                "id": int(row["id"]),
                "candidate": row["candidate"],
                "score": score,
            }


def exercise_q9_streaming_and_filtering() -> None:
    """
    Demonstrate generator-based row-by-row streaming to filter records efficiently.
    """
    print("\n=== Q9: Memory-Efficient Streaming & Filtering ===")

    raw_candidates = """id,candidate,score
1,Alice,88.5
2,Bob,62.0
3,Charlie,95.0
4,Dave,71.5
5,Eva,91.0
"""
    stream = io.StringIO(raw_candidates.strip())
    qualifying_gen = csv_stream_filter(stream, min_score=85.0)

    # Lazily extract candidates
    qualified = list(qualifying_gen)
    assert len(qualified) == 3
    assert [q["candidate"] for q in qualified] == ["Alice", "Charlie", "Eva"]

    print(f"  Filtered {len(qualified)} qualifying candidates via generator streaming:")
    for item in qualified:
        print(f"    - {item['candidate']} (Score: {item['score']})")


# ==============================================================================
# Question 10: Advanced Project - CSV ETL & Schema Validation Pipeline
# ==============================================================================
class CSVETLPipeline:
    """
    Robust CSV ETL pipeline that enforces schema validation, coerces types,
    accumulates errors without crashing, and generates clean output summaries.
    """

    def __init__(self, schema: dict[str, type]) -> None:
        self.schema = schema
        self.errors: list[dict[str, Any]] = []

    def process(self, stream: io.StringIO) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        reader = csv.DictReader(stream)
        valid_records: list[dict[str, Any]] = []

        # Validate headers
        missing_fields = [f for f in self.schema if f not in (reader.fieldnames or [])]
        if missing_fields:
            raise ValueError(f"CSV missing mandatory schema columns: {missing_fields}")

        for row_idx, row in enumerate(reader, start=2):  # row 1 is header
            record: dict[str, Any] = {}
            row_has_error = False

            for field_name, target_type in self.schema.items():
                val_str = row.get(field_name, "").strip()
                if not val_str:
                    self.errors.append({
                        "row": row_idx,
                        "field": field_name,
                        "error": "Empty value",
                    })
                    row_has_error = True
                    break

                try:
                    record[field_name] = target_type(val_str)
                except (ValueError, TypeError) as exc:
                    self.errors.append({
                        "row": row_idx,
                        "field": field_name,
                        "val": val_str,
                        "error": f"Type cast error: {exc}",
                    })
                    row_has_error = True
                    break

            if not row_has_error:
                valid_records.append(record)

        summary = {
            "total_processed": len(valid_records) + len(self.errors),
            "valid_count": len(valid_records),
            "error_count": len(self.errors),
        }
        return valid_records, summary


def exercise_q10_etl_pipeline() -> None:
    """
    Test CSVETLPipeline against mixed clean and corrupted data.
    """
    print("\n=== Q10: CSV ETL & Schema Validation Pipeline ===")

    mixed_csv = """trans_id,amount,approved
TX-101,45.50,1
TX-102,invalid_amount,1
TX-103,120.00,0
TX-104,,1
TX-105,99.90,1
"""
    schema = {
        "trans_id": str,
        "amount": float,
        "approved": lambda v: bool(int(v)),
    }

    pipeline = CSVETLPipeline(schema)
    records, summary = pipeline.process(io.StringIO(mixed_csv.strip()))

    assert summary["valid_count"] == 3
    assert summary["error_count"] == 2
    assert records[0]["amount"] == 45.50
    assert records[0]["approved"] is True
    assert records[1]["trans_id"] == "TX-103"
    assert records[1]["approved"] is False

    print(f"  ETL Summary: {summary}")
    print(f"  Errors Recorded: {pipeline.errors}")
    print(f"  Cleaned Records: {records}")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_csv_reader_basics()
    exercise_q2_csv_writer_mechanics()
    exercise_q3_dict_reader()
    exercise_q4_dict_writer()
    exercise_q5_custom_delimiters()
    exercise_q6_quoting_modes()
    exercise_q7_dialects_and_sniffer()
    exercise_q8_complex_multiline_and_bom()
    exercise_q9_streaming_and_filtering()
    exercise_q10_etl_pipeline()

    print("\nAll 10 CSV file handling questions executed and asserted successfully!")
