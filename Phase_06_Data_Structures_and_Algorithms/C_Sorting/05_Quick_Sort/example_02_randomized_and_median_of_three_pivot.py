"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 05: Quick Sort
Example 02: Avoiding O(N^2) Worst Case via Randomized Pivot & Median-of-Three

Demonstrates:
1. Why Naive Quick Sort (`pivot = arr[high]`) degrades to O(N^2) comparisons and O(N) stack
   depth on an ALREADY SORTED array (every partition splits into `N - 1` and `0` elements!).
2. How Median-of-Three Pivot Selection (`median(arr[low], arr[mid], arr[high])`) and
   Randomized Pivot Selection turn sorted/reverse-sorted arrays into the O(N log N) Best Case!
"""

import random


def naive_last_element_quicksort(
    arr: list[int], low: int, high: int
) -> tuple[int, int]:
    """
    Naive Lomuto Quick Sort always choosing `arr[high]` as pivot.
    Returns (comparisons, max_recursion_depth).
    """
    if low >= high:
        return 0, 1

    pivot = arr[high]
    i = low - 1
    comps = 0
    for j in range(low, high):
        comps += 1
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    p = i + 1

    c_left, d_left = naive_last_element_quicksort(arr, low, p - 1)
    c_right, d_right = naive_last_element_quicksort(arr, p + 1, high)
    return comps + c_left + c_right, 1 + max(d_left, d_right)


def choose_median_of_three_index(arr: list[int], low: int, high: int) -> int:
    """Return the index among (low, mid, high) whose value is the median of the three."""
    mid = low + (high - low) // 2
    a, b, c = arr[low], arr[mid], arr[high]
    if (a <= b <= c) or (c <= b <= a):
        return mid
    if (b <= a <= c) or (c <= a <= b):
        return low
    return high


def median_of_three_quicksort(
    arr: list[int], low: int, high: int
) -> tuple[int, int]:
    """
    Quick Sort using Median-of-Three pivot selection.
    Swaps the median of `(arr[low], arr[mid], arr[high])` into `arr[high]` before partitioning.
    Returns (comparisons, max_recursion_depth).
    """
    if low >= high:
        return 0, 1

    med_idx = choose_median_of_three_index(arr, low, high)
    arr[med_idx], arr[high] = arr[high], arr[med_idx]

    pivot = arr[high]
    i = low - 1
    comps = 0
    for j in range(low, high):
        comps += 1
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    p = i + 1

    c_left, d_left = median_of_three_quicksort(arr, low, p - 1)
    c_right, d_right = median_of_three_quicksort(arr, p + 1, high)
    return comps + c_left + c_right, 1 + max(d_left, d_right)


if __name__ == "__main__":
    random.seed(42)
    print("=" * 72)
    print("1. NAIVE LAST-ELEMENT PIVOT vs MEDIAN-OF-THREE ON SORTED INPUT (N=31)")
    print("=" * 72)

    already_sorted = list(range(1, 32))  # N = 31 sorted integers
    a1 = already_sorted.copy()
    a2 = already_sorted.copy()

    naive_comps, naive_depth = naive_last_element_quicksort(a1, 0, len(a1) - 1)
    med3_comps, med3_depth = median_of_three_quicksort(a2, 0, len(a2) - 1)
    assert a1 == a2 == already_sorted

    print(f"Input: Already Sorted Array [1 .. 31] (N = 31)")
    print(
        f"  Naive Pivot (arr[high]) -> Comparisons: {naive_comps:>3} (O(N^2) = 465) | "
        f"Stack Depth: {naive_depth:>2} (O(N))"
    )
    print(
        f"  Median-of-Three Pivot   -> Comparisons: {med3_comps:>3} (O(N log N))   | "
        f"Stack Depth: {med3_depth:>2} (O(log N))"
    )
