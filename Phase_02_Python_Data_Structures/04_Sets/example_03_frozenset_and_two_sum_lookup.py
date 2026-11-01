"""
Topic 04: Sets
Example 03: `frozenset` as Dict Keys & O(n) Pair-Sum Detection with a Hash Set

Demonstrates:
1. `frozenset` (immutable, hashable set) used as a dictionary key for undirected routes.
2. Using a set for O(n) Two-Sum pair existence detection instead of O(n^2) nested loops.
"""


def has_pair_with_sum(nums: list[int], target: int) -> tuple[bool, tuple[int, int] | None]:
    """Return True and the pair if any two numbers in `nums` sum to `target` in O(n) time."""
    seen: set[int] = set()
    for num in nums:
        complement = target - num
        if complement in seen:
            return (True, (complement, num))
        seen.add(num)
    return (False, None)


def main() -> None:
    print("=== 1. Undirected Flight Routes using frozenset Keys ===")
    flight_fares: dict[frozenset[str], int] = {
        frozenset({"DEL", "BLR"}): 5400,
        frozenset({"BOM", "HYD"}): 3800,
    }
    # Order does not matter when querying with frozenset!
    route_query = frozenset({"BLR", "DEL"})
    print(f"Fare for BLR <-> DEL : Rs.{flight_fares[route_query]}")

    print("\n=== 2. O(n) Pair-Sum Existence Check Using a Set ===")
    prices = [120, 450, 300, 80, 620]
    for target_sum in [530, 999]:
        found, pair = has_pair_with_sum(prices, target_sum)
        print(f"  Target={target_sum} -> Found: {found}, Pair: {pair}")


if __name__ == "__main__":
    main()
