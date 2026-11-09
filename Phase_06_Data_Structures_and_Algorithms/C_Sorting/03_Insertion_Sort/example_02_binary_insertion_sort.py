"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 03: Insertion Sort
Example 02: Binary Insertion Sort (Reducing Comparisons to O(N log N))

Demonstrates:
1. Binary Insertion Sort: Since the prefix `a[0 .. i - 1]` is ALWAYS sorted, we can use
   Binary Search (`bisect_right` logic) to find the exact insertion index in O(log i)
   comparisons instead of O(i) linear comparisons!
2. Why Binary Insertion Sort is critical when **comparisons are expensive** (e.g., comparing
   long strings, cryptographic hashes, or custom objects), even though shifting still takes
   O(N^2) memory moves.
"""


def binary_search_upper_bound(
    arr: list[int], key: int, low: int, high: int
) -> tuple[int, int]:
    """
    Find the first index in `arr[low .. high]` that is strictly greater than `key`
    (preserves stability by placing `key` AFTER equal elements!).
    Returns (insertion_index, comparisons).
    """
    comps = 0
    while low <= high:
        mid = low + (high - low) // 2
        comps += 1
        if arr[mid] <= key:
            low = mid + 1
        else:
            high = mid - 1
    return low, comps


def binary_insertion_sort(arr: list[int]) -> tuple[list[int], int, int]:
    """
    Binary Insertion Sort:
    - Comparisons : O(N log N) in ALL cases (Best, Average, Worst)!
    - Shifts      : O(N^2) in Average/Worst case, O(1) in Best case.
    Returns (sorted_list, comparisons, shifts).
    """
    a = arr.copy()
    n = len(a)
    total_comps = 0
    total_shifts = 0

    for i in range(1, n):
        key = a[i]
        # Find insertion position in sorted prefix a[0 .. i - 1]
        ins_idx, comps = binary_search_upper_bound(a, key, 0, i - 1)
        total_comps += comps

        # Shift elements [ins_idx .. i - 1] one position right
        for j in range(i - 1, ins_idx - 1, -1):
            a[j + 1] = a[j]
            total_shifts += 1

        a[ins_idx] = key

    return a, total_comps, total_shifts


if __name__ == "__main__":
    from example_01_shift_based_insertion_sort_and_adaptivity import insertion_sort

    print("=" * 72)
    print("1. STANDARD INSERTION SORT vs BINARY INSERTION SORT (COMPARISONS)")
    print("=" * 72)

    reverse_16 = list(range(160, 0, -10))  # 16 elements in reverse order
    s_out, s_comps, s_shifts = insertion_sort(reverse_16)
    b_out, b_comps, b_shifts = binary_insertion_sort(reverse_16)
    assert s_out == b_out

    print(f"Reverse-Sorted Input (N={len(reverse_16)}): {reverse_16}")
    print(
        f"  Standard Insertion Sort -> Comparisons: {s_comps:>3} (O(N^2))     | Shifts: {s_shifts}"
    )
    print(
        f"  Binary Insertion Sort   -> Comparisons: {b_comps:>3} (O(N log N)) | Shifts: {b_shifts}"
    )

