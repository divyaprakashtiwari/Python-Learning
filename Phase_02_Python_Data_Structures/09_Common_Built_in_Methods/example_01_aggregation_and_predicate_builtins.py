"""
Topic 09: Common Built-in Methods
Example 01: Aggregation (`sum`, `min`, `max` with `key`/`default`) and Logic (`any`, `all`)

Demonstrates Python's built-in aggregation functions and short-circuiting
boolean quantifiers `any()` and `all()`.
"""


def main() -> None:
    scores = [78, 92, 85, 64, 99]
    words = ["graph", "dp", "backtracking", "tree"]

    print("=== 1. Aggregation Built-ins: len(), sum(), min(), max() ===")
    print(f"Count (len)             : {len(scores)}")
    print(f"Total (sum)             : {sum(scores)}")
    print(f"Sum with base=100       : {sum(scores, start=100)}")
    print(f"Shortest Word (key=len) : {min(words, key=len)!r}")
    print(f"Longest Word (key=len)  : {max(words, key=len)!r}")
    print(f"Safe max on empty []    : {max([], default=-1)}")

    print("\n=== 2. Logical Quantifiers: any() and all() ===")
    all_passed = all(s >= 50 for s in scores)
    any_perfect = any(s == 100 for s in scores)
    any_distinction = any(s >= 95 for s in scores)
    print(f"Did ALL students score >= 50? : {all_passed}")
    print(f"Did ANY student score 100?    : {any_perfect}")
    print(f"Did ANY student score >= 95?  : {any_distinction}")


if __name__ == "__main__":
    main()
