"""
Phase 5 - Topic 10: Python Collections Module
Example 01: `Counter` (Multiset Frequency Analysis) & `defaultdict` (Automatic Grouping)

Demonstrates:
  - Counting frequencies, finding `.most_common(k)`, and multiset arithmetic (`+`, `-`, `&`) with `Counter`
  - Grouping items without `KeyError` boilerplate using `defaultdict(list)` and `defaultdict(int)`
"""

from collections import Counter, defaultdict


def main() -> None:
    print("=== 1. `Counter` Frequency Counting & `.most_common()` ===")
    words = ["python", "rust", "python", "go", "python", "rust", "c++"]
    counts = Counter(words)
    print(f"  Counter        : {counts}")
    print(f"  Top 2 languages: {counts.most_common(2)}")
    print(f"  Missing key lookup (`counts['java']`): {counts['java']} (returns 0, never KeyError!)")

    print("\n=== 2. `Counter` Multiset Arithmetic (`+` and `-`) ===")
    warehouse_a = Counter(keyboard=5, mouse=10)
    warehouse_b = Counter(keyboard=3, monitor=4)
    combined = warehouse_a + warehouse_b
    print(f"  Combined inventory : {dict(combined)}")

    print("\n=== 3. Grouping Records with `defaultdict(list)` ===")
    employees = [
        ("Engineering", "Aarav"),
        ("Design", "Diya"),
        ("Engineering", "Rohan"),
        ("Design", "Meera"),
    ]
    by_dept: defaultdict[str, list[str]] = defaultdict(list)
    for dept, name in employees:
        by_dept[dept].append(name)
    print(f"  Grouped by department: {dict(by_dept)}")


if __name__ == "__main__":
    main()
