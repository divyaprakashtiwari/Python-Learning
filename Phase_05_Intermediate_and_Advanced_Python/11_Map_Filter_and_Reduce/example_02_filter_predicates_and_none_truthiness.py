"""
Phase 5 - Topic 11: Map, Filter and Reduce
Example 02: `filter()` — Predicate Filtering, `filter(None, ...)`, & `itertools.filterfalse`

Demonstrates:
  - Filtering elements lazily using a predicate function `filter(pred, iterable)`
  - Passing `None` as the predicate (`filter(None, iterable)`) to strip all falsy values
  - Inverting the predicate with `itertools.filterfalse()`
"""

from itertools import filterfalse


def is_valid_port(port: int) -> bool:
    return 1024 <= port <= 65535


def main() -> None:
    print("=== 1. Predicate Filtering with `filter(is_valid_port, ...)` ===")
    candidate_ports = [22, 80, 5432, 8080, 70000, -1, 3000]
    valid = list(filter(is_valid_port, candidate_ports))
    invalid = list(filterfalse(is_valid_port, candidate_ports))
    print(f"  Valid unprivileged ports (`filter`)      : {valid}")
    print(f"  Rejected ports (`itertools.filterfalse`) : {invalid}")

    print("\n=== 2. Truthiness Filtering with `filter(None, iterable)` ===")
    messy_inputs = ["aarav", "", None, "diya", "   ".strip(), "rohan", 0]
    truthy_only = list(filter(None, messy_inputs))
    print(f"  After `filter(None, messy_inputs)`       : {truthy_only}")


if __name__ == "__main__":
    main()
