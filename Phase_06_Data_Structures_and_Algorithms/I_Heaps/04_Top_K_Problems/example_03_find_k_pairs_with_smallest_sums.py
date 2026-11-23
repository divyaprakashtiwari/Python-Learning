"""
Phase 6 - Section I.04: Top K Problems
Example 03: Find K Pairs with Smallest Sums

Demonstrating:
1. Finding K pairs with smallest sums from two sorted arrays in O(K log K) time.
2. Multi-way merge pattern avoiding full Cartesian product O(N * M).
"""

import heapq


def k_smallest_pairs(nums1, nums2, k):
    """
    Find k pairs (u, v) with smallest sum u + v.
    Both nums1 and nums2 are sorted in non-decreasing order.
    Time Complexity: O(min(k, n1 * n2) * log(min(k, n1)))
    Space Complexity: O(min(k, n1))
    """
    if not nums1 or not nums2 or k == 0:
        return []

    # Min-heap stores: (sum, i, j) where i is index in nums1, j is index in nums2
    min_heap = []

    # Initialize heap with pairs (nums1[i], nums2[0]) for the first min(k, len(nums1)) elements
    for i in range(min(k, len(nums1))):
        heapq.heappush(min_heap, (nums1[i] + nums2[0], i, 0))

    result = []
    while min_heap and len(result) < k:
        curr_sum, i, j = heapq.heappop(min_heap)
        result.append([nums1[i], nums2[j]])

        # If there is a next element in nums2 for the current nums1[i], push it
        if j + 1 < len(nums2):
            heapq.heappush(min_heap, (nums1[i] + nums2[j + 1], i, j + 1))

    return result


def main():
    print("=" * 60)
    print("Find K Pairs with Smallest Sums (Multi-Way Heap Merge)")
    print("=" * 60)
    n1 = [1, 7, 11]
    n2 = [2, 4, 6]
    k = 3
    pairs1 = k_smallest_pairs(n1, n2, k)
    print(f"nums1 = {n1}, nums2 = {n2}, k = {k}")
    print("Smallest Pairs:", pairs1)

    n3 = [1, 1, 2]
    n4 = [1, 2, 3]
    k2 = 2
    pairs2 = k_smallest_pairs(n3, n4, k2)
    print(f"\nnums1 = {n3}, nums2 = {n4}, k = {k2}")
    print("Smallest Pairs:", pairs2)

    n5 = [1, 2]
    n6 = [3]
    k3 = 3
    pairs3 = k_smallest_pairs(n5, n6, k3)
    print(f"\nnums1 = {n5}, nums2 = {n6}, k = {k3}")
    print("Smallest Pairs:", pairs3)


if __name__ == "__main__":
    main()
