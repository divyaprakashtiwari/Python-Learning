"""
Phase 6 - Data Structures and Algorithms
Section B: Searching - Topic 01: Linear Search
Example 01: Standard Linear Search & Sentinel Linear Search Optimization

Demonstrates:
1. Standard Linear Search: checks both loop boundary (i < n) and match (arr[i] == target)
   on every iteration (2 comparisons per step).
2. Sentinel Linear Search: places target at the end of the array so the loop boundary check
   is eliminated inside the loop (1 comparison per step), reducing constant-factor overhead.
3. Exact comparison counts across hit and miss scenarios.
"""


def standard_linear_search(arr: list[int], target: int) -> tuple[int, int]:
    """
    Search for target sequentially from index 0 to n - 1.
    Returns (found_index, total_comparisons).
    Each iteration performs 1 index-bound check + 1 equality check, plus 1 final bound check on miss.
    """
    comparisons = 0
    n = len(arr)
    i = 0

    while True:
        comparisons += 1  # Check: i < n
        if i >= n:
            return -1, comparisons

        comparisons += 1  # Check: arr[i] == target
        if arr[i] == target:
            return i, comparisons

        i += 1


def sentinel_linear_search(arr: list[int], target: int) -> tuple[int, int]:
    """
    Sentinel Linear Search:
    Temporarily places `target` at the last index (arr[n - 1]) as a 'sentinel' guard
    so the while loop is guaranteed to terminate without checking `i < n` on every step!
    """
    n = len(arr)
    if n == 0:
        return -1, 1

    comparisons = 0
    # Save the original last element and replace it with the sentinel (target)
    last_element = arr[n - 1]
    arr[n - 1] = target

    i = 0
    while True:
        comparisons += 1  # Only 1 check per iteration: arr[i] == target
        if arr[i] == target:
            break
        i += 1

    # Restore the original last element
    arr[n - 1] = last_element

    # Final check: did we stop before n - 1, or was the original last element equal to target?
    comparisons += 1
    if i < n - 1 or last_element == target:
        return i, comparisons

    return -1, comparisons


if __name__ == "__main__":
    print("=" * 72)
    print("1. STANDARD vs SENTINEL LINEAR SEARCH (COMPARISON COUNT BENCHMARK)")
    print("=" * 72)

    inventory_skus = [402, 119, 875, 330, 912, 654, 208, 741, 559, 183]
    print(f"Array (n={len(inventory_skus)}): {inventory_skus}\n")

    test_targets = [
        (402, "First element (Best Case)"),
        (912, "Middle element (Index 4)"),
        (183, "Last element (Index 9)"),
        (999, "Missing element (Worst Case)"),
    ]

    print(
        f"{'Scenario':<30} | {'Target':>6} | {'Idx':>4} | "
        f"{'Standard Comps':>14} | {'Sentinel Comps':>14}"
    )
    print("-" * 78)

    for target, label in test_targets:
        idx_std, comps_std = standard_linear_search(inventory_skus, target)
        idx_sen, comps_sen = sentinel_linear_search(inventory_skus, target)
        assert idx_std == idx_sen, "Mismatch between standard and sentinel search!"
        print(
            f"{label:<30} | {target:>6} | {idx_std:>4} | "
            f"{comps_std:>14} | {comps_sen:>14}"
        )

    print("\nKey Insight:")
    print("  Standard Linear Search executes ~2N comparisons in the worst case (bound + equality).")
    print("  Sentinel Linear Search executes ~N + 2 comparisons by eliminating the loop-bound check!")
