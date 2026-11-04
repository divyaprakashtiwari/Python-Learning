"""
Phase 5 - Topic 02: File Handling
Example 02: Structured CSV Processing & Atomic File Replacement Pattern

Demonstrates:
  - Reading and writing CSV data cleanly using `csv.DictReader` and `csv.DictWriter`
    with `newline=""` (preventing blank lines on Windows)
  - Atomic write pattern: writing to a `.tmp` file first and using `Path.replace()`
    so a crash mid-write never corrupts the target file
"""

import csv
from pathlib import Path
import tempfile


def write_inventory_atomically(target_path: Path, rows: list[dict[str, object]]) -> None:
    """Write CSV rows to a temporary sibling file, then atomically replace `target_path`."""
    temp_path = target_path.with_suffix(".csv.tmp")
    fieldnames = ["sku", "name", "qty", "price"]
    with open(temp_path, mode="w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    # Atomic OS-level rename/replace
    temp_path.replace(target_path)


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        csv_path = Path(tmp_dir) / "inventory.csv"
        initial_rows = [
            {"sku": "KB-101", "name": "Mechanical Keyboard", "qty": 15, "price": 3499.50},
            {"sku": "MS-202", "name": "Wireless Mouse", "qty": 4, "price": 1299.00},
            {"sku": "MN-303", "name": "27in 4K Monitor", "qty": 8, "price": 24999.00},
        ]

        print("=== 1. Atomic Write of `inventory.csv` ===")
        write_inventory_atomically(csv_path, initial_rows)
        print(f"  Exists: {csv_path.exists()} | Temp file cleaned up: {not csv_path.with_suffix('.csv.tmp').exists()}")

        print("\n=== 2. Reading with `csv.DictReader` & Computing Total Valuation ===")
        total_value = 0.0
        with open(csv_path, mode="r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                item_total = int(row["qty"]) * float(row["price"])
                total_value += item_total
                print(f"  {row['sku']} ({row['name']}): qty={row['qty']} -> Rs.{item_total:,.2f}")
        print(f"  Grand Total Valuation: Rs.{total_value:,.2f}")


if __name__ == "__main__":
    main()
