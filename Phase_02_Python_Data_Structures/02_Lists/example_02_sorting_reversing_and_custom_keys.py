"""
Topic 02: Lists
Example 02: Sorting Lists (`sort()` vs `sorted()`) and Custom `key` Functions

Demonstrates Timsort (`O(n log n)`), preserving the original list with `sorted()`,
in-place sorting with `.sort()`, and sorting complex records using `key=`.
"""


def main() -> None:
    latencies_ms = [48, 12, 105, 19, 32]

    print("=== 1. sorted(list) vs list.sort() ===")
    ascending_copy = sorted(latencies_ms)
    print(f"Original (unchanged) : {latencies_ms}")
    print(f"sorted() new list    : {ascending_copy}")

    latencies_ms.sort(reverse=True)
    print(f"In-place .sort(desc) : {latencies_ms}")

    print("\n=== 2. Custom Key Sorting (Case-Insensitive & By Length) ===")
    words = ["banana", "Apple", "fig", "Cherry", "date"]
    print(f"Case-Insensitive     : {sorted(words, key=str.lower)}")
    print(f"By Word Length       : {sorted(words, key=len)}")

    print("\n=== 3. Multi-Criteria Sorting (Highest Score, then Alphabetical Name) ===")
    candidates = [
        ("Rohan", 88),
        ("Aarav", 95),
        ("Divya", 95),
        ("Sneha", 88),
    ]
    # Sort by (-score, name) so higher scores come first and ties break alphabetically
    ranked = sorted(candidates, key=lambda item: (-item[1], item[0]))
    for rank, (name, score) in enumerate(ranked, start=1):
        print(f"  Rank #{rank}: {name:<6} (Score: {score})")


if __name__ == "__main__":
    main()
