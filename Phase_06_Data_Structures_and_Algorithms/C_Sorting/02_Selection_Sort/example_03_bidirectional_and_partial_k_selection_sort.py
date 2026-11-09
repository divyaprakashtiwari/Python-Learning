"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 02: Selection Sort
Example 03: Bidirectional (Double) Selection Sort & Partial Top-K Selection Sort

Demonstrates:
1. Bidirectional (Double) Selection Sort: finds BOTH the minimum AND maximum in each
   pass through `[left .. right]`, placing `min` at `left` and `max` at `right` (halving the
   number of outer passes!).
2. Partial Selection Sort (`select_smallest_k`): stops after `k` outer passes to retrieve the
   `k` smallest elements in O(N * k) time without sorting the remaining `N - k` elements!
"""


def bidirectional_selection_sort(arr: list[int]) -> tuple[list[int], int]:
    """
    Double Selection Sort: places both the minimum (at `left`) and maximum (at `right`)
    in every pass, shrinking the unsorted window from both ends simultaneously.
    Returns (sorted_list, outer_passes).
    """
    a = arr.copy()
    left = 0
    right = len(a) - 1
    passes = 0

    while left < right:
        passes += 1
        min_idx = left
        max_idx = left

        for i in range(left + 1, right + 1):
            if a[i] < a[min_idx]:
                min_idx = i
            if a[i] > a[max_idx]:
                max_idx = i

        # 1. Swap minimum element into `left`
        if min_idx != left:
            a[left], a[min_idx] = a[min_idx], a[left]
            # CRITICAL: If the maximum element was sitting at `left`, it just got moved to `min_idx`!
            if max_idx == left:
                max_idx = min_idx

        # 2. Swap maximum element into `right`
        if max_idx != right:
            a[right], a[max_idx] = a[max_idx], a[right]

        left += 1
        right -= 1

    return a, passes


def partial_selection_sort_top_k(arr: list[int], k: int) -> list[int]:
    """
    Run Selection Sort for only `k` passes to extract the `k` smallest elements
    in O(N * k) time (faster than full O(N log N) sort when k is tiny, e.g., k <= 3).
    """
    a = arr.copy()
    n = len(a)
    k = min(k, n)

    for i in range(k):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]

    return a[:k]


if __name__ == "__main__":
    print("=" * 72)
    print("1. BIDIRECTIONAL (DOUBLE) SELECTION SORT (MIN & MAX EACH PASS)")
    print("=" * 72)

    sample = [78, 12, 95, 34, 61, 8, 47, 89, 23, 50]
    sorted_bi, passes = bidirectional_selection_sort(sample)
    assert sorted_bi == sorted(sample)
    print(f"Input (N={len(sample)}) : {sample}")
    print(f"Sorted Output : {sorted_bi}")
    print(f"Outer Passes  : {passes} (Half of standard N - 1 = 9 passes!)")

    print("\n" + "=" * 72)
    print("2. PARTIAL SELECTION SORT: FIND 3 SMALLEST LATENCIES IN O(N * K)")
    print("=" * 72)
    latencies_ms = [142, 89, 210, 17, 64, 310, 24, 95, 11, 180]
    top_3_fastest = partial_selection_sort_top_k(latencies_ms, k=3)
    print(f"All Latencies (ms)   : {latencies_ms}")
    print(f"3 Lowest Latencies   : {top_3_fastest} (Computed in just 3 outer passes!)")

