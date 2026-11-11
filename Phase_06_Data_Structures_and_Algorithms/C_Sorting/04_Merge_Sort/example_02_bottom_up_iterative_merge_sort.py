"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 04: Merge Sort
Example 02: Bottom-Up Iterative Merge Sort & Single Shared Auxiliary Buffer

Demonstrates:
1. Bottom-Up Iterative Merge Sort: eliminates recursion overhead (`O(1)` call stack space)
   by merging adjacent subarrays of size `width = 1, 2, 4, 8, 16, ...`.
2. Pre-allocating a SINGLE `aux` buffer of size `N` upfront instead of slicing/allocating
   new lists at every recursive node (reducing garbage-collection pressure!).
"""


def merge_into_buffer(
    a: list[int], aux: list[int], left: int, mid: int, right: int
) -> None:
    """
    Merge sorted `a[left .. mid - 1]` and `a[mid .. right - 1]` using the pre-allocated
    `aux` buffer, then copy the merged segment back into `a[left .. right - 1]`.
    """
    # Early-skip optimization: if greatest element of left half <= smallest of right half,
    # the combined segment [left .. right - 1] is ALREADY sorted!
    if a[mid - 1] <= a[mid]:
        return

    i = left
    j = mid
    k = left

    while i < mid and j < right:
        if a[i] <= a[j]:
            aux[k] = a[i]
            i += 1
        else:
            aux[k] = a[j]
            j += 1
        k += 1

    while i < mid:
        aux[k] = a[i]
        i += 1
        k += 1

    while j < right:
        aux[k] = a[j]
        j += 1
        k += 1

    for idx in range(left, right):
        a[idx] = aux[idx]


def bottom_up_merge_sort(arr: list[int], trace: bool = False) -> list[int]:
    """
    Iterative Bottom-Up Merge Sort using a single pre-allocated auxiliary buffer.
    Time Complexity : O(N log N)
    Space Complexity: O(N) single buffer, O(1) stack space (zero recursion!)
    """
    a = arr.copy()
    n = len(a)
    if n <= 1:
        return a

    aux = [0] * n
    width = 1
    pass_num = 0

    while width < n:
        pass_num += 1
        for left in range(0, n, 2 * width):
            mid = min(left + width, n)
            right = min(left + 2 * width, n)
            if mid < right:
                merge_into_buffer(a, aux, left, mid, right)

        if trace:
            print(f"  After Pass {pass_num} (merging width={width:>2} -> {2*width:>2}): {a}")
        width *= 2

    return a


if __name__ == "__main__":
    print("=" * 72)
    print("1. BOTTOM-UP ITERATIVE MERGE SORT TRACE (ZERO RECURSION)")
    print("=" * 72)

    sample = [38, 27, 43, 3, 9, 82, 10, 19, 55, 12]
    print(f"Initial Array (N={len(sample)}): {sample}\n")
    sorted_out = bottom_up_merge_sort(sample, trace=True)
    assert sorted_out == sorted(sample)
    print(f"\nFinal Sorted Array     : {sorted_out}")

