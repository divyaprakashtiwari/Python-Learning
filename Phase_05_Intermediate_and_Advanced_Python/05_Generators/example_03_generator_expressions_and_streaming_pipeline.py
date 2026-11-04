"""
Phase 5 - Topic 05: Generators
Example 03: Generator Expressions, Lazy Streaming Pipelines, & `sys.getsizeof()` Memory Comparison

Demonstrates:
  - Comparing memory usage of a 1,000,000-element list comprehension vs a generator expression
  - Building a multi-stage lazy log processing pipeline where zero intermediate lists are allocated
"""

import sys
from typing import Iterable, Iterator


def parse_status_codes(raw_logs: Iterable[str]) -> Iterator[tuple[str, int]]:
    """Stage 1: Parse `'ENDPOINT STATUS_CODE'` lines lazily."""
    for line in raw_logs:
        endpoint, code_str = line.strip().split()
        yield endpoint, int(code_str)


def filter_server_errors(parsed: Iterable[tuple[str, int]]) -> Iterator[str]:
    """Stage 2: Yield only endpoints with 5xx HTTP status codes."""
    return (f"{ep} (HTTP {code})" for ep, code in parsed if 500 <= code < 600)


def main() -> None:
    print("=== 1. Memory Footprint: List Comprehension vs Generator Expression ===")
    list_comp = [x * x for x in range(100_000)]
    gen_expr = (x * x for x in range(100_000))
    print(f"  List comprehension (100k ints) : {sys.getsizeof(list_comp):>9,} bytes")
    print(f"  Generator expression (100k)    : {sys.getsizeof(gen_expr):>9,} bytes (constant O(1)!)")

    print("\n=== 2. Multi-Stage Lazy Streaming Pipeline ===")
    raw_log_stream = [
        "/api/users 200",
        "/api/orders 502",
        "/api/health 200",
        "/api/payments 504",
        "/api/cart 404",
    ]
    pipeline = filter_server_errors(parse_status_codes(raw_log_stream))
    print(f"  Pipeline object: {type(pipeline).__name__}")
    print(f"  5xx Alerts     : {list(pipeline)}")


if __name__ == "__main__":
    main()
