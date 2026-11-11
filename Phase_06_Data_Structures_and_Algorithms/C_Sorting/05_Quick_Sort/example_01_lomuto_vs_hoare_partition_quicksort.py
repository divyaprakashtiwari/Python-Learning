"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 05: Quick Sort
Example 01: Lomuto vs Hoare Partition Schemes & In-Place Quick Sort

Demonstrates:
1. Lomuto Partition Scheme: single directional pointer scan using `arr[high]` as pivot.
   Easy to understand and places pivot at its exact final index `p`.
2. Hoare Partition Scheme (Tony Hoare's original 1959 design): two pointers (`i` moving right,
   `j` moving left) that performs ~3x FEWER swaps on average than Lomuto!
"""


def lomuto_partition(arr: list[int], low: int, high: int) -> tuple[int, int]:
    """
    Lomuto Partition using `pivot = arr[high]`.
    Rearranges `arr[low .. high]` so elements `<= pivot` are in `arr[low .. i]`
    and elements `> pivot` are in `arr[i + 1 .. high]`.
    Returns (final_pivot_index, swaps_performed).
    """
    pivot = arr[high]
    i = low - 1  # Boundary of elements <= pivot
    swaps = 0

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            if i != j:
                arr[i], arr[j] = arr[j], arr[i]
                swaps += 1

    if (i + 1) != high:
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        swaps += 1

    return i + 1, swaps


def quicksort_lomuto(arr: list[int], low: int, high: int) -> int:
    """In-place Quick Sort using Lomuto partition. Returns total swaps."""
    if low >= high:
        return 0
    pivot_idx, swaps = lomuto_partition(arr, low, high)
    swaps += quicksort_lomuto(arr, low, pivot_idx - 1)
    swaps += quicksort_lomuto(arr, pivot_idx + 1, high)
    return swaps


def hoare_partition(arr: list[int], low: int, high: int) -> tuple[int, int]:
    """
    Hoare Partition using `pivot = arr[low + (high - low) // 2]`.
    Two pointers converge from both ends, swapping inversions across the pivot.
    Returns (split_index_j, swaps_performed).
    """
    pivot = arr[low + (high - low) // 2]
    i = low - 1
    j = high + 1
    swaps = 0

    while True:
        i += 1
        while arr[i] < pivot:
            i += 1

        j -= 1
        while arr[j] > pivot:
            j -= 1

        if i >= j:
            return j, swaps

        arr[i], arr[j] = arr[j], arr[i]
        swaps += 1


def quicksort_hoare(arr: list[int], low: int, high: int) -> int:
    """In-place Quick Sort using Hoare partition. Returns total swaps."""
    if low >= high:
        return 0
    split_idx, swaps = hoare_partition(arr, low, high)
    # Note: In Hoare partition, split_idx is included in the left recursive call!
    swaps += quicksort_hoare(arr, low, split_idx)
    swaps += quicksort_hoare(arr, split_idx + 1, high)
    return swaps


if __name__ == "__main__":
    print("=" * 72)
    print("1. LOMUTO PARTITION vs HOARE PARTITION QUICK SORT (SWAP BENCHMARK)")
    print("=" * 72)

    sample = [42, 15, 88, 7, 63, 29, 95, 11, 54, 36, 71, 20, 81, 49, 18, 60]
    a_lomuto = sample.copy()
    a_hoare = sample.copy()

    lomuto_swaps = quicksort_lomuto(a_lomuto, 0, len(a_lomuto) - 1)
    hoare_swaps = quicksort_hoare(a_hoare, 0, len(a_hoare) - 1)
    assert a_lomuto == a_hoare == sorted(sample)

    print(f"Input Array (N={len(sample)}) : {sample}")
    print(f"Sorted Result      : {a_hoare}")
    print(f"Lomuto Total Swaps : {lomuto_swaps}")
    print(f"Hoare Total Swaps  : {hoare_swaps} (Hoare performs significantly fewer swaps!)")
