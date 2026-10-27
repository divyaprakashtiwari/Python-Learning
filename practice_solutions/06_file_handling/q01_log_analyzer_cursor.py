"""
Topic 06 - File Handling: Question 1
Problem: Text Log Inspection Utility using File Context Management, tell(), and seek().
"""

import os
import re
from typing import Any, Dict, List


def analyze_server_log(filepath: str) -> Dict[str, Any]:
    """Analyzes a server log file using seek(), tell(), and line streaming."""
    if not os.path.exists(filepath):
        raise FileNotFoundError("Log file not found")

    counts = {"INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}
    unique_ips = set()
    total_lines = 0

    ipv4_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

    with open(filepath, mode="r", encoding="utf-8") as f:
        # 1. Cursor Inspection & Navigation
        pos_start = f.tell()
        print(f"Cursor at start: {pos_start}")

        header_preview = f.readline()
        print(f"Header preview: {repr(header_preview)}")

        f.seek(0)
        pos_reset = f.tell()
        print(f"Cursor reset: {pos_reset}")

        # 2. Line streaming and metric extraction
        for line in f:
            stripped = line.strip()
            if not stripped:
                continue

            total_lines += 1

            for level in counts.keys():
                if f" {level} " in stripped or stripped.startswith(level):
                    counts[level] += 1
                    break

            ip_match = ipv4_pattern.search(stripped)
            if ip_match:
                unique_ips.add(ip_match.group(0))

    return {
        "total_lines": total_lines,
        "counts": counts,
        "unique_ips": sorted(list(unique_ips))
    }


# Verification & Demonstration
sample_log_path = "sample_server.log"
sample_log_data = (
    "2026-10-24 10:00:01 INFO 192.168.1.10 System started\n"
    "2026-10-24 10:00:15 WARNING 10.0.0.5 High memory usage\n"
    "2026-10-24 10:01:22 ERROR 192.168.1.10 Database connection failed\n"
    "2026-10-24 10:02:05 INFO 172.16.0.2 User login success\n"
)

try:
    with open(sample_log_path, "w", encoding="utf-8") as temp_file:
        temp_file.write(sample_log_data)

    result = analyze_server_log(sample_log_path)

    print("Log Analysis Summary:")
    print(f"- Total Lines: {result['total_lines']}")
    for level, count in result["counts"].items():
        print(f"- {level} Count: {count}")
    print(f"- Unique Client IPs: {result['unique_ips']}")

    # Missing file guard verification
    try:
        analyze_server_log("non_existent_file.log")
    except FileNotFoundError as err:
        print(f"\nMissing File Guard Verified: Caught FileNotFoundError: {err}")

finally:
    if os.path.exists(sample_log_path):
        os.remove(sample_log_path)
