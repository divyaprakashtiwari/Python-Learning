"""
Topic 06 - File Handling: Question 2
Problem: Safe, Atomic Audit Report Writer with Overwrite Protection and os.replace().
"""

import os
from typing import Any, Dict, List


def generate_audit_report(target_filepath: str, records: List[Dict[str, Any]], overwrite: bool = False) -> int:
    """Writes audit reports atomically using a staging temporary file and os.replace()."""
    # 1. Directory creation & Overwrite Protection
    parent_dir = os.path.dirname(target_filepath)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    if os.path.exists(target_filepath) and not overwrite:
        raise FileExistsError(f"Target '{target_filepath}' already exists and overwrite is False")

    # 2. Atomic Temporary Staging Pattern
    tmp_filepath = f"{target_filepath}.tmp"

    try:
        with open(tmp_filepath, mode="w", encoding="utf-8") as f:
            f.write("=== SYSTEM AUDIT REPORT ===\n")
            f.write("TIMESTAMP           | EVENT_ID | SEVERITY | DESCRIPTION\n")

            lines = []
            for r in records:
                formatted_line = f"{r['timestamp']} | {r['id']:<8} | {r['severity']:<8} | {r['desc']}\n"
                lines.append(formatted_line)

            f.writelines(lines)
            f.write("=== END OF REPORT ===\n")

            # Flush and force sync to disk storage
            f.flush()
            os.fsync(f.fileno())

        print(f"Staging written to: {tmp_filepath.replace(os.sep, '/')}")

        # 4. Atomic Promotion
        os.replace(tmp_filepath, target_filepath)
        print(f"Atomic commit completed: {target_filepath.replace(os.sep, '/')}")
        return len(records)

    finally:
        # Guarantee tmp file cleanup on failure
        if os.path.exists(tmp_filepath):
            os.remove(tmp_filepath)


# Verification & Execution
audit_data = [
    {"timestamp": "2026-10-24 10:15:00", "id": "EVT-101", "severity": "LOW", "desc": "Config reloaded"},
    {"timestamp": "2026-10-24 10:17:30", "id": "EVT-102", "severity": "HIGH", "desc": "TLS cert expired"},
    {"timestamp": "2026-10-24 10:20:10", "id": "EVT-103", "severity": "CRITICAL", "desc": "Kernel panic avoided"}
]

test_report_path = "reports/audit_2026.log"

try:
    count = generate_audit_report(test_report_path, audit_data, overwrite=True)
    print(f"Total Audit Records Written: {count}")

    print("\n# Generated File Content:")
    with open(test_report_path, "r", encoding="utf-8") as f:
        print(f.read().strip())

    # Overwrite Conflict Test
    print("\nOverwrite Conflict Test:")
    try:
        generate_audit_report(test_report_path, audit_data, overwrite=False)
    except FileExistsError as err:
        print(f'Caught Expected: FileExistsError("{err}")')

finally:
    # Cleanup generated files after test
    if os.path.exists(test_report_path):
        os.remove(test_report_path)
    if os.path.exists("reports"):
        try:
            os.rmdir("reports")
        except OSError:
            pass
