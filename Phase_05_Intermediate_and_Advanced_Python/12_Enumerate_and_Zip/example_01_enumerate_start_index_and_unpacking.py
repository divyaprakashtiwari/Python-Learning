"""
Phase 5 - Topic 12: Enumerate and Zip
Example 01: `enumerate(iterable, start=...)` — Clean Index + Value Iteration

Demonstrates:
  - Replacing error-prone `for i in range(len(seq)):` loops with `enumerate()`
  - Setting a custom 1-based starting index (`start=1`) for human-readable rankings and line numbers
  - Building an O(1) value-to-index lookup dictionary via `{val: idx for idx, val in enumerate(seq)}`
"""


def main() -> None:
    runners = ["Aarav", "Diya", "Rohan", "Meera"]

    print("=== 1. 1-Based Leaderboard with `enumerate(runners, start=1)` ===")
    for rank, name in enumerate(runners, start=1):
        print(f"  Rank #{rank}: {name}")

    print("\n=== 2. Building an Value -> First-Index Map Using `enumerate` ===")
    index_map = {name: idx for idx, name in enumerate(runners)}
    print(f"  Index map: {index_map}")


if __name__ == "__main__":
    main()
