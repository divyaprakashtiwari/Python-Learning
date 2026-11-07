"""
Phase 6 - Data Structures and Algorithms
Section B: Searching - Topic 02: Binary Search
Example 02: Order-Agnostic Binary Search & Python's `bisect` Module

Demonstrates:
1. Order-Agnostic Binary Search: works automatically whether the input array is sorted
   in ascending order OR descending order.
2. Python's standard library `bisect` module (`bisect_left`, `bisect_right`, `insort`)
   for ultra-fast C-level binary search and grade/tier lookup tables.
"""

import bisect


def order_agnostic_binary_search(arr: list[int], target: int) -> int:
    """
    Binary Search that automatically detects whether `arr` is sorted
    in ascending or descending order by comparing `arr[0]` and `arr[-1]`.
    """
    if not arr:
        return -1

    low = 0
    high = len(arr) - 1
    is_ascending = arr[low] <= arr[high]

    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            return mid

        if is_ascending:
            if arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        else:
            # Descending order: larger values are on the left!
            if arr[mid] < target:
                high = mid - 1
            else:
                low = mid + 1

    return -1


def assign_credit_tier(credit_score: int) -> str:
    """
    Use `bisect.bisect_right` (alias `bisect.bisect`) to map a numeric score
    to a rating tier in O(log K) time without a long chain of if/elif statements.
    Breakpoints: <580 Poor, 580-669 Fair, 670-739 Good, 740-799 Very Good, >=800 Exceptional
    """
    breakpoints = [580, 670, 740, 800]
    tiers = ["Poor", "Fair", "Good", "Very Good", "Exceptional"]
    bucket_idx = bisect.bisect_right(breakpoints, credit_score)
    return tiers[bucket_idx]


if __name__ == "__main__":
    print("=" * 72)
    print("1. ORDER-AGNOSTIC BINARY SEARCH (ASCENDING & DESCENDING)")
    print("=" * 72)

    asc_prices = [10, 25, 40, 55, 70, 85, 100]
    desc_leaderboard = [980, 850, 720, 610, 500, 390, 210]

    print(f"Ascending Array  : {asc_prices}")
    print(f"  Search 70      -> Index: {order_agnostic_binary_search(asc_prices, 70)}")
    print(f"Descending Array : {desc_leaderboard}")
    print(f"  Search 720     -> Index: {order_agnostic_binary_search(desc_leaderboard, 720)}")
    print(f"  Search 390     -> Index: {order_agnostic_binary_search(desc_leaderboard, 390)}")

    print("\n" + "=" * 72)
    print("2. PYTHON'S BUILT-IN `bisect` MODULE (`bisect_left` vs `bisect_right`)")
    print("=" * 72)

    scores = [60, 70, 70, 70, 80, 90]
    left_pos = bisect.bisect_left(scores, 70)
    right_pos = bisect.bisect_right(scores, 70)
    print(f"Sorted Scores          : {scores}")
    print(f"bisect_left(scores, 70): {left_pos} (First index >= 70)")
    print(f"bisect_right(scores,70): {right_pos} (First index >  70)")
    print(f"Count of 70s in O(logN): right_pos - left_pos = {right_pos - left_pos}")

    print("\n" + "=" * 72)
    print("3. TABLE LOOKUP WITH `bisect_right` (CREDIT SCORE TIERS)")
    print("=" * 72)
    for sample_score in [520, 580, 669, 705, 740, 815]:
        print(f"  Credit Score {sample_score} -> Tier: {assign_credit_tier(sample_score)}")
