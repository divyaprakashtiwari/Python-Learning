"""
Question 2: Bubble Sort & Selection Sort Empirical Comparator
Topic: Data Structures & Algorithms (DSA)

Key Concepts Tested:
- Optimized Bubble Sort with early-exit flag (O(N) best case)
- Selection Sort with minimum-swap property (at most N-1 swaps)
- Empirical metrics tracking: comparison count, swap count, passes completed
- Sorting stability analysis (stable Bubble Sort vs unstable Selection Sort)
- Non-mutating behavior on caller input
"""

from typing import List, Dict, Any, Callable, Optional


class SortingComparator:
    """
    Benchmark engine for comparing elementary quadratic sorting algorithms:
    Optimized Bubble Sort and Selection Sort.
    """

    @staticmethod
    def bubble_sort(arr: List[Any], key: Optional[Callable[[Any], Any]] = None) -> Dict[str, Any]:
        """
        In-place Bubble Sort on a shallow copy with early-exit flag optimization.
        Tracks comparisons, swaps, and passes.
        """
        a = list(arr)
        n = len(a)
        comparisons = 0
        swaps = 0
        passes = 0

        if n <= 1:
            return {
                "sorted_array": a,
                "comparison_count": 0,
                "swap_count": 0,
                "passes_completed": 0,
            }

        get_val = key if key else lambda x: x

        for i in range(n - 1):
            passes += 1
            swapped = False
            for j in range(n - 1 - i):
                comparisons += 1
                if get_val(a[j]) > get_val(a[j + 1]):
                    a[j], a[j + 1] = a[j + 1], a[j]
                    swaps += 1
                    swapped = True
            if not swapped:
                break

        return {
            "sorted_array": a,
            "comparison_count": comparisons,
            "swap_count": swaps,
            "passes_completed": passes,
        }

    @staticmethod
    def selection_sort(arr: List[Any], key: Optional[Callable[[Any], Any]] = None) -> Dict[str, Any]:
        """
        In-place Selection Sort on a shallow copy.
        Performs N*(N-1)//2 comparisons and at most N-1 swaps.
        """
        a = list(arr)
        n = len(a)
        comparisons = 0
        swaps = 0

        if n <= 1:
            return {
                "sorted_array": a,
                "comparison_count": 0,
                "swap_count": 0,
            }

        get_val = key if key else lambda x: x

        for i in range(n - 1):
            min_idx = i
            for j in range(i + 1, n):
                comparisons += 1
                if get_val(a[j]) < get_val(a[min_idx]):
                    min_idx = j

            if min_idx != i:
                a[i], a[min_idx] = a[min_idx], a[i]
                swaps += 1

        return {
            "sorted_array": a,
            "comparison_count": comparisons,
            "swap_count": swaps,
        }


if __name__ == "__main__":
    comparator = SortingComparator()

    print("=== 1. Sorting Empirical Comparison on Unsorted Array ===")
    test_arr = [64, 25, 12, 22, 11]
    bubble_res = comparator.bubble_sort(test_arr)
    selection_res = comparator.selection_sort(test_arr)

    print(f"Original Array preserved: {test_arr == [64, 25, 12, 22, 11]}")
    print(f"Bubble Sort on {test_arr}:")
    print(f"- Sorted: {bubble_res['sorted_array']}")
    print(f"- Comparisons: {bubble_res['comparison_count']}")
    print(f"- Swaps: {bubble_res['swap_count']}")
    print(f"- Passes: {bubble_res['passes_completed']}")

    print(f"\nSelection Sort on {test_arr}:")
    print(f"- Sorted: {selection_res['sorted_array']}")
    print(f"- Comparisons: {selection_res['comparison_count']}")
    print(f"- Swaps: {selection_res['swap_count']}")

    print("\n=== 2. Early-Exit Optimization on Sorted Array ===")
    sorted_arr = [1, 2, 3, 4, 5]
    bubble_best = comparator.bubble_sort(sorted_arr)
    print(f"Bubble Sort Early-Exit on Already Sorted Array {sorted_arr}:")
    print(f"- Comparisons: {bubble_best['comparison_count']}")
    print(f"- Swaps: {bubble_best['swap_count']}")
    print(f"- Passes Completed: {bubble_best['passes_completed']} (Terminated after 1st pass via early-exit flag)")

    print("\n=== 3. Stability Demonstration ===")
    # Array designed to expose instability in Selection Sort:
    # ("ItemA", 2) precedes ("ItemB", 2). Selection Sort swaps ("ItemA", 2) with ("ItemC", 1),
    # putting ItemA AFTER ItemB!
    keyed_data = [("ItemA", 2), ("ItemB", 2), ("ItemC", 1)]

    bubble_stable = comparator.bubble_sort(keyed_data, key=lambda x: x[1])
    selection_unstable = comparator.selection_sort(keyed_data, key=lambda x: x[1])

    print("Original items:", keyed_data)
    print("Bubble Sort (Stable - ItemA precedes ItemB):")
    print(bubble_stable["sorted_array"])
    print("Selection Sort (Unstable - ItemB precedes ItemA):")
    print(selection_unstable["sorted_array"])
