"""
Topic 06 - File Handling: Question 5
Problem: Enterprise Payroll CSV Transformation using csv.DictReader and csv.DictWriter.
"""

import csv
import os
from typing import Any, Dict


def process_payroll_csv(input_csv_path: str, output_csv_path: str) -> Dict[str, Any]:
    """Processes raw timesheet CSV, computes overtime & net wages, and writes structured output."""
    if not os.path.exists(input_csv_path):
        raise FileNotFoundError(f"Input file not found: {input_csv_path}")

    required_cols = ["emp_id", "full_name", "department", "hours_worked", "hourly_rate"]
    output_headers = ["emp_id", "full_name", "department", "gross_pay", "tax_withheld", "net_pay"]

    total_gross = 0.0
    total_net = 0.0
    records_count = 0
    transformed_records = []

    with open(input_csv_path, mode="r", newline="", encoding="utf-8") as in_f:
        raw_reader = csv.DictReader(in_f)
        if not raw_reader.fieldnames:
            raise ValueError("CSV file is empty or missing header row")

        # Strip whitespace from header names
        cleaned_fieldnames = [f.strip() for f in raw_reader.fieldnames]
        for col in required_cols:
            if col not in cleaned_fieldnames:
                raise KeyError(f"Missing required column in CSV: '{col}'")

        for raw_row in raw_reader:
            row = {k.strip(): v.strip() for k, v in raw_row.items() if k is not None}
            if not row or not any(row.values()):
                continue

            hours = float(row["hours_worked"])
            rate = float(row["hourly_rate"])

            if hours < 0.0 or rate < 0.0:
                raise ValueError("Hours and rates must be non-negative")

            # Overtime calculation: regular <= 40, overtime > 40 at 1.5x
            if hours <= 40.0:
                gross = hours * rate
            else:
                regular_pay = 40.0 * rate
                overtime_pay = (hours - 40.0) * rate * 1.5
                gross = regular_pay + overtime_pay

            tax = gross * 0.20
            net = gross - tax

            total_gross += gross
            total_net += net
            records_count += 1

            transformed_records.append({
                "emp_id": row["emp_id"],
                "full_name": row["full_name"],
                "department": row["department"],
                "gross_pay": f"{gross:.2f}",
                "tax_withheld": f"{tax:.2f}",
                "net_pay": f"{net:.2f}"
            })

    # Write processed records
    parent_dir = os.path.dirname(output_csv_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as out_f:
        writer = csv.DictWriter(out_f, fieldnames=output_headers)
        writer.writeheader()
        writer.writerows(transformed_records)

    return {
        "records_processed": records_count,
        "total_gross": round(total_gross, 2),
        "total_net": round(total_net, 2)
    }


# Verification & Execution
in_file = "raw_timesheets.csv"
out_file = "processed_payroll.csv"

raw_csv_content = (
    "emp_id, full_name, department, hours_worked, hourly_rate\n"
    "E101, Alice Smith , Engineering , 40.0 , 50.00\n"
    "E102, Bob Jones   , Support     , 45.0 , 30.00\n"
    "E103, Charlie Ray , Marketing   , 35.0 , 40.00\n"
)

try:
    with open(in_file, "w", newline="", encoding="utf-8") as f:
        f.write(raw_csv_content)

    summary = process_payroll_csv(in_file, out_file)
    print(f"Processed {summary['records_processed']} payroll records.")
    print("Summary:")
    print(f"- Total Gross Payout: ${summary['total_gross']:.2f}")
    print(f"- Total Net Payout:   ${summary['total_net']:.2f}")

    print(f'\n# Generated CSV File ("{out_file}"):')
    with open(out_file, "r", newline="", encoding="utf-8") as f:
        print(f.read().strip())

    # Validation Tests
    print("\nValidation Tests:")
    # 1. Negative hours test
    neg_file = "neg_test.csv"
    with open(neg_file, "w", newline="", encoding="utf-8") as f:
        f.write("emp_id, full_name, department, hours_worked, hourly_rate\nE999, Bad Guy, QA, -5.0, 20.0\n")
    try:
        process_payroll_csv(neg_file, "neg_out.csv")
    except ValueError as err:
        print(f'- Negative hours input: ValueError("{err}")')
    finally:
        if os.path.exists(neg_file):
            os.remove(neg_file)

    # 2. Missing column test
    bad_col_file = "bad_col.csv"
    with open(bad_col_file, "w", newline="", encoding="utf-8") as f:
        f.write("emp_id, full_name, department, hours_worked\nE999, Incomplete, QA, 40.0\n")
    try:
        process_payroll_csv(bad_col_file, "bad_out.csv")
    except KeyError as err:
        print(f'- Missing required column: KeyError({err})')
    finally:
        if os.path.exists(bad_col_file):
            os.remove(bad_col_file)

finally:
    for path in (in_file, out_file):
        if os.path.exists(path):
            os.remove(path)
