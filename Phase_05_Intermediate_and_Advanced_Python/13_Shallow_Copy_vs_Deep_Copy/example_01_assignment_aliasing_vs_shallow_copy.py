"""
Phase 5 - Topic 13: Shallow Copy vs Deep Copy
Example 01: Assignment Aliasing (`=`) vs Shallow Copy (`copy.copy()`, `.copy()`, `[:]`)

Demonstrates:
  - Why `b = a` does NOT copy a list (both names point to the exact same object in memory)
  - How a shallow copy creates a new outer container (`a is not b`) whose top-level
    elements are independent when rebound
"""

import copy


def main() -> None:
    print("=== 1. Assignment Aliasing (`alias = original`) ===")
    original = [10, 20, 30]
    alias = original
    alias.append(40)
    print(f"  original is alias : {original is alias}")
    print(f"  original after alias.append(40): {original}")

    print("\n=== 2. Shallow Copy (`copy.copy`, `.copy()`, `[:]`) on Flat List ===")
    shallow_1 = copy.copy(original)
    shallow_2 = original.copy()
    shallow_3 = original[:]
    shallow_1.append(999)
    print(f"  original is shallow_1 : {original is shallow_1}")
    print(f"  original              : {original} (unaffected by shallow_1.append)")
    print(f"  shallow_1             : {shallow_1}")
    print(f"  All 3 shallow copy techniques equal? {shallow_1[:-1] == shallow_2 == shallow_3}")


if __name__ == "__main__":
    main()
