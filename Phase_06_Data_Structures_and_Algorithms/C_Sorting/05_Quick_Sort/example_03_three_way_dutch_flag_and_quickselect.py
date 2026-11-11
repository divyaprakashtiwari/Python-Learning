"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 05: Quick Sort
Example 03: 3-Way Dutch National Flag Partition (Handling Duplicates) & Quickselect

Demonstrates:
1. Edsger Dijkstra's 3-Way Partition (Dutch National Flag):
   Splits array into THREE zones: `[ < pivot | == pivot | > pivot ]`.
   When an array has many duplicate keys, 3-Way Quick Sort runs in O(N) linear time instead
   of degrading to O(N^2) like standard 2-way Lomuto partition!
2. Quickselect (Hoare's Selection Algorithm): finds the k-th smallest element in O(N)
   average time by recursing into ONLY the partition that contains index `k`!
"""


def three_way_quicksort(arr: list[int], low: int, high: int) -> int:
    """
    3-Way Quick Sort (Dutch National Flag Partition):
    Partitions `arr[low .. high]` into:
    - `arr[low .. lt - 1]`   : strictly < pivot
    - `arr[lt .. gt]`        : equal to pivot (ALL locked in final position at once!)
    - `arr[gt + 1 .. high]`  : strictly > pivot
    Returns number of recursive calls made.
    """
    if low >= high:
        return 1

    pivot = arr[low + (high - low) // 2]
    lt = low       # Next slot for element < pivot
    i = low        # Current scanner
    gt = high      # Next slot for element > pivot

    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1

    # All elements in [lt .. gt] equal `pivot` and NEVER need to be touched again!
    calls_left = three_way_quicksort(arr, low, lt - 1)
    calls_right = three_way_quicksort(arr, gt + 1, high)
    return 1 + calls_left + calls_right


def quickselect_kth_smallest(arr: list[int], k_zero_based: int) -> int:
    """
    Find the k-th smallest element (0-based index) in O(N) average time and O(1) space
    by partitioning only the side that contains index `k_zero_based`.
    """
    a = arr.copy()
    low = 0
    high = len(a) - 1

    while low <= high:
        pivot = a[low + (high - low) // 2]
        lt, i, gt = low, low, high
        while i <= gt:
            if a[i] < pivot:
                a[lt], a[i] = a[i], a[lt]
                lt += 1
                i += 1
            elif a[i] > pivot:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:
                i += 1

        if k_zero_based < lt:
            high = lt - 1
        elif k_zero_based > gt:
            low = gt + 1
        else:
            # k_zero_based falls right inside the [lt .. gt] equal-to-pivot zone!
            return a[k_zero_based]

    raise ValueError("k out of bounds")


if __name__ == "__main__":
    print("=" * 72)
    print("1. 3-WAY DUTCH NATIONAL FLAG QUICK SORT ON HEAVY DUPLICATES")
    print("=" * 72)

    heavy_dups = [2, 1, 3, 2, 1, 2, 3, 1, 2, 3, 2, 1, 3, 2, 1, 2]
    print(f"Input with 3 Distinct Keys (N={len(heavy_dups)}): {heavy_dups}")
    calls = three_way_quicksort(heavy_dups, 0, len(heavy_dups) - 1)
    print(f"Sorted Result                        : {heavy_dups}")
    print(f"Total Recursive Calls                : {calls} (Finished in just 2 levels!)")

    print("\n" + "=" * 72)
    print("2. QUICKSELECT: O(N) AVERAGE K-TH SMALLEST ELEMENT & MEDIAN")
    print("=" * 72)
    latencies = [85, 12, 49, 93, 27, 64, 38, 71, 19]
    median_idx = len(latencies) // 2
    median_val = quickselect_kth_smallest(latencies, median_idx)
    print(f"Unsorted Latencies : {latencies}")
    print(f"Sorted Reference   : {sorted(latencies)}")
    print(f"Median (k={median_idx})       : {median_val}")
