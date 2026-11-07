"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 01: Bubble Sort
Example 01: Standard Bubble Sort vs Early-Exit (Swapped-Flag) Bubble Sort

Demonstrates:
1. Standard Unoptimized Bubble Sort: always runs N*(N-1)//2 comparisons even if the array
   is already sorted (O(N^2) in Best, Average, and Worst cases).
2. Optimized Bubble Sort (`swapped` boolean flag + shrinking right boundary):
   - Achieves O(N) Best-Case time on already-sorted input (0 swaps -> stops after Pass 1).
   - Tracks the exact index of the `last_swap` so multiple already-sorted elements at the
     tail are skipped in a single jump!
"""


def bubble_sort_standard(arr: list[int]) -> tuple[list[int], int, int]:
    """
    Unoptimized Bubble Sort (copies input to preserve caller's list).
    Returns (sorted_list, comparisons, swaps).
    """
    a = arr.copy()
    n = len(a)
    comparisons = 0
    swaps = 0

    for pass_num in range(n - 1):
        # After `pass_num` passes, the last `pass_num` elements are in final position
        for j in range(n - 1 - pass_num):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1

    return a, comparisons, swaps


def bubble_sort_optimized(arr: list[int]) -> tuple[list[int], int, int, int]:
    """
    Optimized Bubble Sort with:
    1. `swapped` early-exit flag (stops immediately if a pass makes 0 swaps).
    2. `last_swap_idx` boundary tightening (all elements after the last swap in a pass
       are already in their final sorted positions!).
    Returns (sorted_list, passes_taken, comparisons, swaps).
    """
    a = arr.copy()
    unsorted_end = len(a) - 1
    comparisons = 0
    swaps = 0
    passes = 0

    while unsorted_end > 0:
        passes += 1
        last_swap_idx = 0

        for j in range(unsorted_end):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                last_swap_idx = j

        # Tighten right boundary to the exact position of the last swap (0 if no swaps!)
        unsorted_end = last_swap_idx

    return a, passes, comparisons, swaps


if __name__ == "__main__":
    print("=" * 72)
    print("1. STANDARD vs OPTIMIZED BUBBLE SORT ACROSS INPUT DISTRIBUTIONS")
    print("=" * 72)

    test_cases = [
        ("Already Sorted (Best Case)", [10, 20, 30, 40, 50, 60, 70, 80]),
        ("Nearly Sorted (Tail Sorted)", [20, 10, 30, 40, 50, 60, 70, 80]),
        ("Random Order (Average Case)", [64, 34, 25, 12, 22, 11, 90, 45]),
        ("Reverse Sorted (Worst Case)", [80, 70, 60, 50, 40, 30, 20, 10]),
    ]

    for label, sample in test_cases:
        res_std, comps_std, swaps_std = bubble_sort_standard(sample)
        res_opt, passes_opt, comps_opt, swaps_opt = bubble_sort_optimized(sample)
        assert res_std == res_opt == sorted(sample)
        print(f"\n[{label}] Input: {sample}")
        print(
            f"  Standard Bubble Sort  -> Comps: {comps_std:>2} | Swaps: {swaps_std:>2}"
        )
        print(
            f"  Optimized Bubble Sort -> Comps: {comps_opt:>2} | Swaps: {swaps_opt:>2} "
            f"| Passes: {passes_opt}"
        )
