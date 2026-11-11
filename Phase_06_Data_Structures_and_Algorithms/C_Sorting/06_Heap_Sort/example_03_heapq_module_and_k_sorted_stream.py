"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 06: Heap Sort
Example 03: Python's `heapq` Module, Streaming Top-K, and Introsort Fallback

Demonstrates:
1. Using Python's C-optimized `heapq` standard library module (`heapify`, `heappush`,
   `heappop`, `nlargest`, `nsmallest`).
2. Sorting a K-Sorted (Nearly Sorted) Stream in O(N log K) time and O(K) space using a
   Min-Heap window of size K + 1.
"""

import heapq


def heapsort_with_heapq(iterable: list[int]) -> list[int]:
    """
    Sort an iterable using Python's built-in `heapq` (Min-Heap).
    `heapq.heapify` runs Floyd's bottom-up algorithm in O(N) C-speed time!
    """
    h = list(iterable)
    heapq.heapify(h)
    return [heapq.heappop(h) for _ in range(len(h))]


def sort_k_sorted_array(arr: list[int], k: int) -> list[int]:
    """
    Sort an array where every element is at most `k` indices away from its target
    sorted position in O(N log k) time and O(k) auxiliary space using a Min-Heap!
    """
    if not arr or k <= 0:
        return arr.copy()

    n = len(arr)
    # 1. Push the first k + 1 elements into the min-heap
    window_size = min(k + 1, n)
    min_heap = arr[:window_size]
    heapq.heapify(min_heap)

    result: list[int] = []

    # 2. For each remaining element, pop the smallest from the heap and push the new element
    for idx in range(window_size, n):
        smallest = heapq.heappushpop(min_heap, arr[idx])
        result.append(smallest)

    # 3. Drain remaining elements from the min-heap
    while min_heap:
        result.append(heapq.heappop(min_heap))

    return result


if __name__ == "__main__":
    print("=" * 72)
    print("1. PYTHON `heapq` MODULE HEAPSORT & TOP-K EXTRACTION")
    print("=" * 72)

    scores = [72, 15, 98, 44, 63, 89, 21, 95, 53, 38]
    print(f"Original Scores : {scores}")
    print(f"heapsort_heapq  : {heapsort_with_heapq(scores)}")
    print(f"3 Largest (O(N)): {heapq.nlargest(3, scores)}")
    print(f"3 Smallest(O(N)): {heapq.nsmallest(3, scores)}")

    print("\n" + "=" * 72)
    print("2. SORTING A K-SORTED (NEARLY SORTED) ARRAY IN O(N log K) TIME")
    print("=" * 72)

    # Every element is displaced by at most k = 2 positions from its sorted index
    k_sorted = [3, 2, 1, 6, 4, 5, 9, 7, 8]
    sorted_k = sort_k_sorted_array(k_sorted, k=2)
    assert sorted_k == sorted(k_sorted)
    print(f"2-Sorted Input  : {k_sorted}")
    print(f"Sorted in O(N log 2) via size-3 Min-Heap: {sorted_k}")
