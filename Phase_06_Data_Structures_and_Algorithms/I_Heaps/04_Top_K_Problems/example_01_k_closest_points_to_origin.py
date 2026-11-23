"""
Phase 6 - Section I.04: Top K Problems
Example 01: K Closest Points to Origin

Demonstrating:
1. Finding K closest points to (0, 0) using a Max-Heap of size K in O(N log K) time.
2. Comparing with Python's heapq.nsmallest and sorting baseline.
3. Euclidean squared distance comparison avoiding floating-point sqrt.
"""

import heapq


def k_closest_max_heap(points, k):
    """
    Find k points closest to origin (0, 0) using a max-heap of size k.
    Heap stores (-dist_sq, x, y) so furthest point in top k is at the root.
    Time Complexity: O(N log k)
    Space Complexity: O(k)
    """
    heap = []
    for x, y in points:
        dist_sq = x * x + y * y
        if len(heap) < k:
            heapq.heappush(heap, (-dist_sq, x, y))
        elif dist_sq < -heap[0][0]:
            heapq.heapreplace(heap, (-dist_sq, x, y))

    return [[x, y] for _, x, y in heap]


def k_closest_nsmallest(points, k):
    """Pythonic baseline using heapq.nsmallest."""
    return heapq.nsmallest(k, points, key=lambda p: p[0] * p[0] + p[1] * p[1])


def main():
    print("=" * 60)
    print("K Closest Points to Origin")
    print("=" * 60)
    points1 = [[1, 3], [-2, 2], [5, 8], [0, 1]]
    k1 = 2
    res_heap1 = k_closest_max_heap(points1, k1)
    res_nsmall1 = k_closest_nsmallest(points1, k1)

    print(f"Points: {points1}, k = {k1}")
    print("Max-Heap Result (O(N log K)) :", sorted(res_heap1))
    print("heapq.nsmallest Result       :", sorted(res_nsmall1))

    points2 = [[3, 3], [5, -1], [-2, 4]]
    k2 = 2
    res_heap2 = k_closest_max_heap(points2, k2)
    print(f"\nPoints: {points2}, k = {k2}")
    print("Max-Heap Result (O(N log K)) :", sorted(res_heap2))


if __name__ == "__main__":
    main()
