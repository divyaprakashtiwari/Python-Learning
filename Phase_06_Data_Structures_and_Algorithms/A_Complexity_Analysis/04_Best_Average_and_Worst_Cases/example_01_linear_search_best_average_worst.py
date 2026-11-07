"""
Phase 6 - Section A (Complexity Analysis) - Topic 04: Best, Average and Worst Cases
Example 01: Best, Average, and Worst Case Comparisons in Linear Search & Early-Exit Bubble Check

Demonstrates:
  - Best Case Omega(1): target found at index 0 on the very first comparison
  - Average Case Theta(n): target equally likely at any index (`~(n + 1) / 2` comparisons)
  - Worst Case O(n): target at last index `n - 1` or absent (`n` comparisons)
"""


def linear_search_with_count(arr: list[int], target: int) -> tuple[int, int]:
    """Return `(found_index_or_neg1, comparisons_made)`."""
    comparisons = 0
    for idx, val in enumerate(arr):
        comparisons += 1
        if val == target:
            return idx, comparisons
    return -1, comparisons


def main() -> None:
    data = list(range(10, 110, 10))  # [10, 20, ..., 100] (N = 10)

    print("=== Best, Average, and Worst Case of Linear Search (N = 10) ===")
    _, best_comps = linear_search_search_best = linear_search_with_count(data, 10)
    _, worst_comps = linear_search_with_count(data, 999)
    avg_comps = sum(linear_search_with_count(data, x)[1] for x in data) / len(data)

    print(f"  Best Case  (target=10 at idx 0)  : {best_comps} comparison   -> Omega(1)")
    print(f"  Average    (across all 10 hits)  : {avg_comps:.1f} comparisons -> Theta(n)")
    print(f"  Worst Case (target=999 absent)   : {worst_comps} comparisons  -> O(n)")


if __name__ == "__main__":
    main()
