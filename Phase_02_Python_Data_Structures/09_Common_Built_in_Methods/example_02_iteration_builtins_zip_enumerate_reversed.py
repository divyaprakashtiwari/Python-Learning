"""
Topic 09: Common Built-in Methods
Example 02: Sequence Iteration Built-ins (`enumerate`, `zip`, `reversed`, `sorted`)

Demonstrates pairing sequences with `zip()`, unzipping a list of tuples with `zip(*pairs)`,
lazy reverse iteration with `reversed()`, and `enumerate()`.
"""


def main() -> None:
    names = ["Divya", "Aarav", "Sneha"]
    cities = ["New Delhi", "Mumbai", "Bengaluru"]
    ranks = [1, 2, 3]

    # 1. Zipping 3 sequences together
    zipped_profiles = list(zip(ranks, names, cities))
    print("=== 1. Pairing Multiple Iterables with zip() ===")
    print(f"Zipped Profiles : {zipped_profiles}")

    # 2. Unzipping a list of tuples using zip(*iterable)
    unzipped_ranks, unzipped_names, unzipped_cities = zip(*zipped_profiles)
    print("\n=== 2. Unzipping with zip(*zipped_profiles) ===")
    print(f"Unzipped Names  : {unzipped_names}")
    print(f"Unzipped Cities : {unzipped_cities}")

    # 3. Lazy reverse iteration with reversed()
    print("\n=== 3. Reverse Iteration with reversed() ===")
    rev_names = list(reversed(names))
    print(f"Reversed Names  : {rev_names} (Original unchanged: {names})")


if __name__ == "__main__":
    main()
