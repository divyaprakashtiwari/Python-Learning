"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 02: Selection Sort
Example 01: Standard Selection Sort & Minimal Memory-Write Guarantee (At Most N - 1 Swaps)

Demonstrates:
1. How Selection Sort partitions the array into `[Sorted Prefix | Unsorted Suffix]` and
   repeatedly selects the minimum element from the unsorted suffix to swap into place.
2. Why Selection Sort always performs `N * (N - 1) // 2` comparisons regardless of input order
   (O(N^2) in Best, Average, and Worst cases), yet performs AT MOST `N - 1` swaps (O(N) writes!).
3. Side-by-side swap-count comparison against Bubble Sort when flash/EEPROM writes are expensive.
"""


def selection_sort(arr: list[int]) -> tuple[list[int], int, int]:
    """
    In-place Selection Sort (operates on a copy to preserve caller's list).
    Returns (sorted_list, comparisons, swaps).
    Time Complexity : O(N^2) in Best, Average, and Worst cases
    Space Complexity: O(1) auxiliary space
    Memory Writes   : At most N - 1 swaps (O(N))
    """
    a = arr.copy()
    n = len(a)
    comparisons = 0
    swaps = 0

    for i in range(n - 1):
        min_idx = i
        # Scan the unsorted suffix [i + 1 .. n - 1] for the smallest element
        for j in range(i + 1, n):
            comparisons += 1
            if a[j] < a[min_idx]:
                min_idx = j

        # Swap ONLY if a strictly smaller element was found at a different index
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1

    return a, comparisons, swaps


if __name__ == "__main__":
    print("=" * 72)
    print("1. SELECTION SORT: O(N^2) COMPARISONS BUT AT MOST N - 1 SWAPS!")
    print("=" * 72)

    test_distributions = [
        ("Already Sorted (Best Case)", [10, 20, 30, 40, 50, 60, 70, 80]),
        ("Random Order (Average Case)", [64, 25, 12, 22, 11, 90, 45, 33]),
        ("Reverse Sorted (Worst Case)", [80, 70, 60, 50, 40, 30, 20, 10]),
    ]

    for label, data in test_distributions:
        sorted_out, comps, swaps = selection_sort(data)
        assert sorted_out == sorted(data)
        print(f"\n[{label}] (N = {len(data)})")
        print(f"  Input       : {data}")
        print(f"  Sorted      : {sorted_out}")
        print(
            f"  Comparisons : {comps:>2} (Always N*(N-1)//2 = 28) | "
            f"Swaps (Memory Writes): {swaps} (<= N - 1 = 7)"
        )

