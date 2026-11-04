"""
Phase 5 - Topic 09: Regular Expressions
Example 02: Named Capture Groups (`(?P<name>...)`), `.groupdict()`, & Lookarounds

Demonstrates:
  - Parsing structured log lines into dictionaries using named groups `(?P<name>...)` and `.groupdict()`
  - Using positive lookahead `(?=...)` and negative lookbehind `(?<!...)` for zero-width assertions
"""

import re


LOG_PATTERN = re.compile(
    r"^\[(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] "
    r"(?P<level>INFO|WARN|ERROR) "
    r"service=(?P<service>[a-z0-9_-]+) "
    r"latency_ms=(?P<latency>\d+)$"
)


def main() -> None:
    print("=== 1. Parsing Structured Logs with Named Capture Groups (`.groupdict()`) ===")
    raw_line = "[2026-11-04 14:22:09] ERROR service=auth-api latency_ms=342"
    match = LOG_PATTERN.match(raw_line)
    if match:
        print(f"  Parsed groupdict: {match.groupdict()}")
        print(f"  Direct group('service'): {match.group('service')!r}")

    print("\n=== 2. Lookaround Assertions (Extract USD Prices Only, Ignoring INR) ===")
    invoice = "Items: $45, Rs.900, $120, Rs.250"
    # (?<=\$)\d+ matches digits ONLY if immediately preceded by literal '$'
    usd_amounts = re.findall(r"(?<=\$)\d+", invoice)
    print(f"  USD amounts via positive lookbehind `(?<=\\$)\\d+`: {usd_amounts}")


if __name__ == "__main__":
    main()
