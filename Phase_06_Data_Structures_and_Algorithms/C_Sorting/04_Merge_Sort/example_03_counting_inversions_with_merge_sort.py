"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 04: Merge Sort
Example 03: Counting Array Inversions in O(N log N) Using Merge Sort

Demonstrates:
1. Classic Interview Problem: Count the number of Inversions `(i, j)` in an array where
   `i < j` and `arr[i] > arr[j]`.
2. Naive nested loops take O(N^2) time; piggybacking on Merge Sort's merge step counts all
   inversions in O(N log N) time!
   Key insight: When merging sorted `left` and `right`, if `left[i] > right[j]`, then NOT ONLY
   does `left[i]` form an inversion with `right[j]`, EVERY remaining element in `left[i:]`
   (`len(left) - i` elements!) is also `> right[j]`!
"""


def sort_and_count_inversions(arr: list[int]) -> tuple[list[int], int]:
    """
    Return `(sorted_array, inversion_count)` in O(N log N) time using Merge Sort.
    """
    if len(arr) <= 1:
        return arr.copy(), 0

    mid = len(arr) // 2
    left_sorted, left_inv = sort_and_count_inversions(arr[:mid])
    right_sorted, right_inv = sort_and_count_inversions(arr[mid:])

    merged: list[int] = []
    i = 0
    j = 0
    split_inv = 0

    while i < len(left_sorted) and j < len(right_sorted):
        if left_sorted[i] <= right_sorted[j]:
            merged.append(left_sorted[i])
            i += 1
        else:
            # left_sorted[i] > right_sorted[j]!
            # Because left_sorted is sorted ascending, ALL remaining elements in
            # left_sorted[i .. end] are also strictly greater than right_sorted[j]!
            merged.append(right_sorted[j])
            split_inv += len(left_sorted) - i
            j += 1

    if i < len(left_sorted):
        merged.extend(left_sorted[i:])
    if j < len(right_sorted):
        merged.extend(right_sorted[j:])

    return merged, (left_inv + right_inv + split_inv)


def brute_force_inversions(arr: list[int]) -> int:
    """O(N^2) verification reference."""
    n = len(arr)
    return sum(1 for i in range(n) for j in range(i + 1, n) if arr[i] > arr[j])


if __name__ == "__main__":
    print("=" * 72)
    print("1. COUNTING INVERSIONS IN O(N log N) VIA MERGE SORT")
    print("=" * 72)

    test_arrays = [
        ("Sorted Array (0 Inversions)", [10, 20, 30, 40, 50]),
        ("Classic Example [2, 4, 1, 3, 5]", [2, 4, 1, 3, 5]),
        ("Reverse Array (Max N*(N-1)//2)", [50, 40, 30, 20, 10]),
        ("User Ranking Similarity Array", [8, 4, 2, 1, 7, 3, 6, 5]),
    ]

    for label, sample in test_arrays:
        sorted_out, inv_fast = sort_and_count_inversions(sample)
        inv_brute = brute_force_inversions(sample)
        assert inv_fast == inv_brute and sorted_out == sorted(sample)
        print(f"  {label:<32} | Input: {str(sample):<26} -> Inversions: {inv_fast}")

