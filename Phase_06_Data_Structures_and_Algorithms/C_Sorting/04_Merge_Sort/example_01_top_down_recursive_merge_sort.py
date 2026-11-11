"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 04: Merge Sort
Example 01: Top-Down Recursive Merge Sort & Guaranteed O(N log N) Two-Pointer Merge

Demonstrates:
1. Divide-and-Conquer Top-Down Merge Sort:
   - Divide  : Split `arr` at `mid = len(arr) // 2` into `left_half` and `right_half`.
   - Conquer : Recursively sort `left_half` and `right_half`.
   - Combine : Merge two sorted halves in O(N) linear time using two pointers (`i` and `j`).
2. Why Merge Sort guarantees O(N log N) comparisons in Best, Average, AND Worst cases!
"""


def merge_two_sorted_lists(
    left: list[int], right: list[int]
) -> tuple[list[int], int]:
    """
    Merge two sorted lists `left` and `right` into a single sorted list in O(L + R) time.
    Uses `left[i] <= right[j]` (with `<=`) so elements from the LEFT half win ties,
    guaranteeing that Merge Sort is STABLE!
    Returns (merged_list, comparisons).
    """
    merged: list[int] = []
    i = 0
    j = 0
    comparisons = 0

    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Append any remaining elements (at most one of `left[i:]` or `right[j:]` is non-empty)
    if i < len(left):
        merged.extend(left[i:])
    if j < len(right):
        merged.extend(right[j:])

    return merged, comparisons


def merge_sort_top_down(arr: list[int]) -> tuple[list[int], int]:
    """
    Top-Down Recursive Merge Sort.
    Returns (sorted_list, total_comparisons).
    Time Complexity : O(N log N) in Best, Average, and Worst cases
    Space Complexity: O(N) auxiliary array + O(log N) recursion stack = O(N)
    """
    if len(arr) <= 1:
        return arr.copy(), 0

    mid = len(arr) // 2
    left_sorted, left_comps = merge_sort_top_down(arr[:mid])
    right_sorted, right_comps = merge_sort_top_down(arr[mid:])
    merged, merge_comps = merge_two_sorted_lists(left_sorted, right_sorted)

    return merged, (left_comps + right_comps + merge_comps)


if __name__ == "__main__":
    print("=" * 72)
    print("1. TOP-DOWN RECURSIVE MERGE SORT ACROSS INPUT DISTRIBUTIONS (N = 16)")
    print("=" * 72)

    cases = [
        ("Already Sorted (Best Case)", list(range(10, 170, 10))),
        (
            "Random Order (Average Case)",
            [90, 20, 150, 40, 110, 70, 10, 160, 50, 130, 80, 30, 140, 60, 120, 100],
        ),
        ("Reverse Sorted (Worst Case)", list(range(160, 0, -10))),
    ]

    for label, data in cases:
        sorted_res, comps = merge_sort_top_down(data)
        assert sorted_res == sorted(data)
        print(f"\n[{label}] (N = {len(data)}, N*log2(N) = 64)")
        print(f"  Comparisons : {comps} (Guaranteed <= N*log2(N) = 64 in ALL cases!)")
        print(f"  Sorted Head : {sorted_res[:8]} ...")

