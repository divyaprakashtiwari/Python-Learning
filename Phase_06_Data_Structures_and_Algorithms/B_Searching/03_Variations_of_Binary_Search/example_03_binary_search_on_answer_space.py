"""
Phase 6 - Data Structures and Algorithms
Section B: Searching - Topic 03: Variations of Binary Search
Example 03: Binary Search on the Answer Space (Monotonic Predicate Optimization)

Demonstrates:
1. Binary Search on Answer (Minimum Ship Capacity to Ship Packages Within D Days):
   When a feasibility predicate `can_ship(capacity)` is monotonic
   (`False, False, ..., False, True, True, ...`), we can binary-search the answer space
   `[max(weights) .. sum(weights)]` in O(N * log(sum(weights))) time!
2. Exponential / Unbounded Binary Search for searching an unbounded or massive sorted stream.
"""


def can_ship_within_days(
    weights: list[int], max_days: int, capacity: int
) -> tuple[bool, int]:
    """
    Greedy feasibility check: Given a ship of `capacity`, how many days are needed
    to ship all `weights` in order? Returns (days_needed <= max_days, days_needed).
    Time Complexity: O(N)
    """
    days_used = 1
    current_load = 0

    for w in weights:
        if current_load + w > capacity:
            days_used += 1
            current_load = w
        else:
            current_load += w

    return days_used <= max_days, days_used


def min_ship_capacity(weights: list[int], max_days: int) -> int:
    """
    Binary Search on Answer Space:
    - Minimum possible capacity `low = max(weights)` (must carry the heaviest single package).
    - Maximum needed capacity `high = sum(weights)` (carry everything in 1 day).
    Finds the smallest `capacity` for which `can_ship_within_days` is True.
    """
    low = max(weights)
    high = sum(weights)
    best_capacity = high

    while low <= high:
        mid_cap = low + (high - low) // 2
        feasible, _ = can_ship_within_days(weights, max_days, mid_cap)

        if feasible:
            best_capacity = mid_cap
            high = mid_cap - 1  # Try an even smaller capacity!
        else:
            low = mid_cap + 1   # Capacity too small; must increase!

    return best_capacity


def exponential_search(arr: list[int], target: int) -> int:
    """
    Exponential Search (Galloping Search):
    Finds the range `[bound // 2 .. min(bound, n - 1)]` containing `target` by doubling
    `bound = 1, 2, 4, 8, ...`, then runs standard binary search in O(log(target_index)) time!
    """
    n = len(arr)
    if n == 0:
        return -1
    if arr[0] == target:
        return 0

    bound = 1
    while bound < n and arr[bound] <= target:
        bound *= 2

    # Binary search within [bound // 2 .. min(bound, n - 1)]
    low = bound // 2
    high = min(bound, n - 1)
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


if __name__ == "__main__":
    print("=" * 72)
    print("1. BINARY SEARCH ON THE ANSWER SPACE (MINIMUM SHIP CAPACITY IN D DAYS)")
    print("=" * 72)

    packages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    deadline_days = 5
    print(f"Package Weights : {packages} (Total = {sum(packages)}, Max = {max(packages)})")
    print(f"Deadline        : {deadline_days} days\n")

    print("Monotonic Feasibility Table across candidate capacities [10 .. 20]:")
    for cap in range(10, 21, 2):
        ok, days = can_ship_within_days(packages, deadline_days, cap)
        print(f"  Capacity = {cap:>2} -> Days Required = {days} -> Feasible (<=5 days)? {ok}")

    optimal = min_ship_capacity(packages, deadline_days)
    print(f"\n-> Optimal Minimum Capacity via Binary Search on Answer: {optimal}")

    print("\n" + "=" * 72)
    print("2. EXPONENTIAL (GALLOPING) SEARCH O(log i)")
    print("=" * 72)
    stream = [i * 10 for i in range(1, 101)]  # [10, 20, ..., 1000]
    for q in [10, 70, 640, 995]:
        print(f"  Exponential Search for {q:>3} -> Index: {exponential_search(stream, q)}")
