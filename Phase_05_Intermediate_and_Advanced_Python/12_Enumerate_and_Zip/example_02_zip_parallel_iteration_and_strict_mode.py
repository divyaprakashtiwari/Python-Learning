"""
Phase 5 - Topic 12: Enumerate and Zip
Example 02: `zip()` — Parallel Iteration, Dictionary Construction, & `strict=True` (Python 3.10+)

Demonstrates:
  - Iterating over multiple sequences in lockstep with `zip()`
  - Constructing dictionaries cleanly with `dict(zip(keys, values))`
  - Catching silent length-mismatch bugs immediately with `zip(..., strict=True)` (Python 3.10+)
"""


def main() -> None:
    headers = ["id", "username", "role"]
    row = [101, "aarav_dev", "admin"]

    print("=== 1. Building a Dictionary from Parallel Lists (`dict(zip(keys, values))`) ===")
    record = dict(zip(headers, row, strict=True))
    print(f"  Constructed dict: {record}")

    print("\n=== 2. Default Shortest-Truncation vs `strict=True` Guard ===")
    names = ["Alice", "Bob", "Charlie"]
    scores = [95, 88]  # Oops: missing Charlie's score!

    print(f"  Default `list(zip(names, scores))` : {list(zip(names, scores))} (silently dropped 'Charlie'!)")
    try:
        list(zip(names, scores, strict=True))
    except ValueError as err:
        print(f"  `zip(..., strict=True)` caught bug  : ValueError -> {err}")


if __name__ == "__main__":
    main()
