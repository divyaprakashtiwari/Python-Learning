"""
Phase 5 - Topic 11: Map, Filter and Reduce
Example 03: `functools.reduce()` — Accumulators, Initializers, & `operator` Module Helpers

Demonstrates:
  - Folding a sequence into a single value using `functools.reduce(func, iterable, initializer)`
  - Combining `reduce` with `operator.mul` and dictionary merging (`operator.or_`)
  - Running prefix accumulations with `itertools.accumulate()`
"""

import functools
from itertools import accumulate
import operator


def main() -> None:
    numbers = [2, 3, 4, 5]

    print("=== 1. Product Calculation via `reduce(operator.mul, numbers, 1)` ===")
    product = functools.reduce(operator.mul, numbers, 1)
    running_products = list(accumulate(numbers, operator.mul))
    print(f"  Final product (`reduce`)          : {product}")
    print(f"  Running products (`accumulate`)   : {running_products}")

    print("\n=== 2. Why Always Supply an `initializer` for Empty Sequences ===")
    empty_list: list[int] = []
    safe_product = functools.reduce(operator.mul, empty_list, 1)
    print(f"  reduce(operator.mul, [], 1)       : {safe_product} (no TypeError on empty input!)")

    print("\n=== 3. Merging a List of Dictionaries with `reduce(operator.or_, ...)` ===")
    patches = [{"a": 1, "b": 2}, {"b": 20, "c": 30}, {"d": 40}]
    merged = functools.reduce(operator.or_, patches, {})
    print(f"  Merged dictionary                 : {merged}")


if __name__ == "__main__":
    main()
