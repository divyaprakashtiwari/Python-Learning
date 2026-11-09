"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 03: Insertion Sort
Example 01: Standard Shift-Based Insertion Sort & Adaptive Performance

Demonstrates:
1. Why Insertion Sort uses SHIFTING (`a[j + 1] = a[j]`) instead of repeated 3-write swaps:
   Saves `key = a[i]`, shifts larger elements in `[0 .. i - 1]` right by 1 slot, and drops
   `key` into `a[j + 1]` in a single final write!
2. Why Insertion Sort is O(N + I) where `I` is the number of inversions:
   - Best Case (Already Sorted, I = 0): O(N) time (N - 1 comparisons, 0 shifts).
   - Nearly Sorted (k-sorted): O(k * N) linear time!
   - Worst Case (Reverse Sorted): O(N^2) time.
"""


def insertion_sort(arr: list[int]) -> tuple[list[int], int, int]:
    """
    Standard Shift-Based Insertion Sort (operates on a copy).
    Returns (sorted_list, comparisons, element_shifts).
    Time Complexity : O(N) Best Case, O(N^2) Average/Worst Case
    Space Complexity: O(1) auxiliary space
    Stable          : Yes (stops shifting when `a[j] <= key`)
    """
    a = arr.copy()
    n = len(a)
    comparisons = 0
    shifts = 0

    for i in range(1, n):
        key = a[i]
        j = i - 1

        # Shift elements of the sorted prefix a[0 .. i-1] that are strictly > key
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                shifts += 1
                j -= 1
            else:
                break

        # Place key into its sorted slot
        a[j + 1] = key

    return a, comparisons, shifts


if __name__ == "__main__":
    print("=" * 72)
    print("1. SHIFT-BASED INSERTION SORT ACROSS INPUT DISTRIBUTIONS")
    print("=" * 72)

    distributions = [
        ("Already Sorted (Best Case)", [10, 20, 30, 40, 50, 60, 70, 80]),
        ("Nearly Sorted (2 Inversions)", [10, 30, 20, 40, 50, 70, 60, 80]),
        ("Random Order (Average Case)", [64, 34, 25, 12, 22, 11, 90, 45]),
        ("Reverse Sorted (Worst Case)", [80, 70, 60, 50, 40, 30, 20, 10]),
    ]

    for label, sample in distributions:
        sorted_out, comps, shifts = insertion_sort(sample)
        assert sorted_out == sorted(sample)
        print(f"\n[{label}] Input: {sample}")
        print(
            f"  Sorted -> {sorted_out} | "
            f"Comparisons: {comps:>2} | Element Shifts (= Inversions): {shifts:>2}"
        )

