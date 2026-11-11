"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 06: Heap Sort
Example 01: In-Place Max-Heap Sort (`sift_down`, `build_max_heap` in O(N), and Extraction)

Demonstrates:
1. Representing a Complete Binary Tree inside a 0-indexed contiguous array with ZERO pointers:
   - Parent of node `i`      : `(i - 1) // 2`
   - Left child of node `i`  : `2 * i + 1`
   - Right child of node `i` : `2 * i + 2`
2. Robert Floyd's Bottom-Up `build_max_heap` algorithm: converts an arbitrary unsorted array
   into a valid Max-Heap in O(N) linear time (not O(N log N)!) by sifting down only the
   non-leaf nodes from `(n // 2) - 1` down to `0`.
3. In-Place Heap Sort: guarantees O(N log N) time in Best, Average, AND Worst cases using
    strictly O(1) auxiliary memory!
"""


def sift_down_max(arr: list[int], start: int, end_exclusive: int) -> int:
    """
    Iterative Max-Heap `sift_down` (also called `max_heapify`).
    Sinks `arr[start]` down the heap `arr[0 .. end_exclusive - 1]` until the Max-Heap
    property (`parent >= both children`) is restored.
    Returns number of comparisons performed.
    Time Complexity : O(log N)
    Space Complexity: O(1) (iterative, no recursion stack!)
    """
    root = start
    comparisons = 0

    while True:
        left_child = 2 * root + 1
        if left_child >= end_exclusive:
            break  # `root` is a leaf node

        right_child = left_child + 1
        largest = root

        comparisons += 1
        if arr[left_child] > arr[largest]:
            largest = left_child

        if right_child < end_exclusive:
            comparisons += 1
            if arr[right_child] > arr[largest]:
                largest = right_child

        if largest == root:
            break  # Max-heap invariant satisfied!

        arr[root], arr[largest] = arr[largest], arr[root]
        root = largest

    return comparisons


def heap_sort_in_place(arr: list[int]) -> tuple[list[int], int, int]:
    """
    In-Place Ascending Heap Sort using a Max-Heap.
    Phase 1: Build Max-Heap bottom-up in O(N) time.
    Phase 2: Repeatedly swap root (`arr[0]`, the maximum) with the end of the active heap
             (`arr[end]`) and sift down the new root in O(log N) time.
    Returns (sorted_list, build_heap_comparisons, extraction_comparisons).
    """
    a = arr.copy()
    n = len(a)
    build_comps = 0
    extract_comps = 0

    # Phase 1: Bottom-up Build-Max-Heap from last internal node (n // 2 - 1) down to 0
    for i in range(n // 2 - 1, -1, -1):
        build_comps += sift_down_max(a, i, n)

    # Phase 2: Extract maximum N - 1 times from the root to the shrinking suffix
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        extract_comps += sift_down_max(a, 0, end)

    return a, build_comps, extract_comps


if __name__ == "__main__":
    print("=" * 72)
    print("1. IN-PLACE MAX-HEAP SORT (O(N log N) TIME, O(1) AUXILIARY SPACE)")
    print("=" * 72)

    test_cases = [
        ("Already Sorted", list(range(10, 170, 10))),
        (
            "Random Order",
            [45, 12, 89, 33, 71, 24, 96, 18, 60, 5, 82, 39, 51, 27, 68, 14],
        ),
        ("Reverse Sorted", list(range(160, 0, -10))),
    ]

    for label, data in test_cases:
        sorted_out, b_comps, e_comps = heap_sort_in_place(data)
        assert sorted_out == sorted(data)
        print(
            f"  {label:<16} (N={len(data)}) -> Build-Heap Comps: {b_comps:>2} (O(N)) | "
            f"Extract Comps: {e_comps:>2} (O(N log N)) | Total: {b_comps + e_comps}"
        )
