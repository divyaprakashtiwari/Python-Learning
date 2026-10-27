"""
Topic 01 - Python Basics & Variables
Practice Question 2 Solution: Safe Type Converter & Aggregator

Problem Statement:
Takes a list of heterogeneous raw string inputs and performs safe type conversion:
- Integer conversion if represents integer.
- Float conversion if represents valid decimal number.
- Boolean conversion if case-insensitively "true" or "false".
- Retain as string otherwise.
Counts elements of each type and computes sum of all numeric values.
"""

from typing import Any


def parse_raw_value(val: str) -> Any:
    """Safely converts a raw string value into int, float, bool, or str."""
    val_stripped = val.strip()

    # 1. Check for boolean
    if val_stripped.lower() == "true":
        return True
    if val_stripped.lower() == "false":
        return False

    # 2. Check for integer
    try:
        # Handles positive and negative integers
        return int(val_stripped)
    except ValueError:
        pass

    # 3. Check for float
    try:
        return float(val_stripped)
    except ValueError:
        pass

    # 4. Fallback to raw string
    return val


def process_raw_dataset(raw_items: list[str]) -> dict[str, Any]:
    """Processes a list of raw strings, groups by inferred type, and aggregates numerics."""
    buckets: dict[str, list[Any]] = {
        "int": [],
        "float": [],
        "bool": [],
        "str": [],
    }

    numeric_sum = 0.0

    for item in raw_items:
        parsed = parse_raw_value(item)
        if isinstance(parsed, bool):
            buckets["bool"].append(parsed)
        elif isinstance(parsed, int):
            buckets["int"].append(parsed)
            numeric_sum += parsed
        elif isinstance(parsed, float):
            buckets["float"].append(parsed)
            numeric_sum += parsed
        else:
            buckets["str"].append(parsed)

    return {
        "buckets": buckets,
        "counts": {k: len(v) for k, v in buckets.items()},
        "numeric_sum": numeric_sum,
    }


def main() -> None:
    raw_data = ["42", "3.14159", "True", "hello", "-18", "FALSE", "100.5", "Python3"]

    results = process_raw_dataset(raw_data)
    buckets = results["buckets"]
    counts = results["counts"]

    print("Parsed types count:")
    print(f"- int: {counts['int']} (values: {', '.join(str(x) for x in buckets['int'])})")
    print(f"- float: {counts['float']} (values: {', '.join(str(x) for x in buckets['float'])})")
    print(f"- bool: {counts['bool']} (values: {', '.join(str(x) for x in buckets['bool'])})")
    print(f"- str: {counts['str']} (values: {', '.join(repr(x) for x in buckets['str'])})")
    print(f"Total numeric sum: {results['numeric_sum']:.5f}")


if __name__ == "__main__":
    main()
