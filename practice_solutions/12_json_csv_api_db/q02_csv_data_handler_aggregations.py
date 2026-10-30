"""
Question 2: Modular CSV Data Handler with Schema Casting & Aggregations
Topic: JSON, CSV, Web APIs, and Databases

Key Concepts Tested:
- csv.DictReader and csv.DictWriter with custom delimiters and quoting
- Dynamic schema casting and handling missing/empty cell values (None substitution)
- Cross-platform newline='' and UTF-8 encoding compliance
- Column statistics aggregation (count, sum, mean, min, max)
- Sniffing dialects using csv.Sniffer
"""

import csv
import io
import os
import tempfile
from typing import List, Dict, Any, Optional, Callable


class CSVDataHandler:
    """
    Modular CSV utility supporting schema casting, custom delimiters,
    statistical aggregations, and dialect sniffing.
    """

    @staticmethod
    def parse_csv_stream(
        stream: io.TextIOBase,
        delimiter: str = ",",
        schema: Optional[Dict[str, Callable[[str], Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """Parses a text stream into a list of dictionaries with optional schema casting."""
        reader = csv.DictReader(stream, delimiter=delimiter)
        records: List[Dict[str, Any]] = []

        for row in reader:
            clean_row: Dict[str, Any] = {}
            for col_name, raw_val in row.items():
                if col_name is None:
                    continue
                clean_key = col_name.strip()
                val = raw_val.strip() if raw_val is not None else ""

                if not val:
                    clean_row[clean_key] = None
                elif schema and clean_key in schema:
                    cast_fn = schema[clean_key]
                    try:
                        clean_row[clean_key] = cast_fn(val)
                    except (ValueError, TypeError):
                        clean_row[clean_key] = None
                else:
                    clean_row[clean_key] = val

            records.append(clean_row)

        return records

    @classmethod
    def parse_csv_string(
        cls,
        csv_text: str,
        delimiter: str = ",",
        schema: Optional[Dict[str, Callable[[str], Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """Parses in-memory CSV string."""
        f = io.StringIO(csv_text.strip())
        return cls.parse_csv_stream(f, delimiter=delimiter, schema=schema)

    @classmethod
    def read_csv(
        cls,
        filepath: str,
        delimiter: str = ",",
        schema: Optional[Dict[str, Callable[[str], Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """Reads CSV file from disk with UTF-8 encoding."""
        with open(filepath, "r", newline="", encoding="utf-8") as f:
            return cls.parse_csv_stream(f, delimiter=delimiter, schema=schema)

    @staticmethod
    def write_csv(
        filepath: str,
        data: List[Dict[str, Any]],
        fieldnames: List[str],
        delimiter: str = ",",
        quoting: int = csv.QUOTE_MINIMAL,
        restval: str = "N/A",
    ) -> None:
        """Writes records to CSV using DictWriter with specified formatting."""
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=fieldnames,
                delimiter=delimiter,
                quoting=quoting,
                restval=restval,
                extrasaction="ignore",
            )
            writer.writeheader()
            for row in data:
                writer.writerow(row)

    @staticmethod
    def aggregate_column(records: List[Dict[str, Any]], column_name: str) -> Dict[str, float]:
        """Calculates count, sum, mean, min, max for a numeric column, ignoring Nones."""
        values: List[float] = []
        for r in records:
            val = r.get(column_name)
            if val is not None and isinstance(val, (int, float)):
                values.append(float(val))

        if not values:
            return {"count": 0.0, "sum": 0.0, "mean": 0.0, "min": 0.0, "max": 0.0}

        total = sum(values)
        count = len(values)
        return {
            "count": float(count),
            "sum": round(total, 2),
            "mean": round(total / count, 2),
            "min": round(min(values), 2),
            "max": round(max(values), 2),
        }

    @staticmethod
    def sniff_dialect(filepath: str) -> Dict[str, Any]:
        """Sniffs delimiter and header status of an unknown CSV."""
        with open(filepath, "r", newline="", encoding="utf-8") as f:
            sample = f.read(1024)
            sniffer = csv.Sniffer()
            has_header = sniffer.has_header(sample)
            dialect = sniffer.sniff(sample)
            return {
                "delimiter": dialect.delimiter,
                "has_header": has_header,
                "quotechar": dialect.quotechar,
            }


if __name__ == "__main__":
    handler = CSVDataHandler()

    sample_csv_content = """emp_id, name, department, salary, active
101, Alice Smith, Engineering, 95000.50, True
102, Bob Jones, Marketing, 62000.00, False
103, Charlie Brown, Engineering, , True
104, Diana Prince, Leadership, 145000.00, True
"""
    schema = {
        "emp_id": int,
        "name": str,
        "department": str,
        "salary": float,
        "active": lambda v: v.strip().lower() == "true" if v else None,
    }

    print("=== 1. Flexible Reader with Schema Casting ===")
    records = handler.parse_csv_string(sample_csv_content, schema=schema)
    print(f"Parsed Record 0: {records[0]}")
    print(f"Parsed Record 2 (Missing Salary): {records[2]}")

    print("\n=== 2. Numeric Column Aggregation ===")
    salary_stats = handler.aggregate_column(records, "salary")
    print("Salary Aggregates:")
    for k, v in salary_stats.items():
        print(f"- {k.capitalize()}: {v:.2f}")

    print("\n=== 3. Custom Dialect Writing (Pipe-delimited, Quote All) ===")
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_file = os.path.join(tmp_dir, "filtered_employees.psv")
        handler.write_csv(
            out_file,
            records,
            fieldnames=["emp_id", "name", "salary"],
            delimiter="|",
            quoting=csv.QUOTE_ALL,
        )

        with open(out_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]
            print("Pipe-Delimited Header:")
            print(f"  {lines[0]}")
            print("Pipe-Delimited Sample Line:")
            print(f"  {lines[1]}")

        # Test sniffer
        dialect_info = handler.sniff_dialect(out_file)
        print(f"\nSniffed Dialect: {dialect_info}")
