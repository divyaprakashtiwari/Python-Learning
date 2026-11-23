"""
Phase 6 - Section I.01: Min Heap
Example 03: Kth Largest Element in a Stream using Min Heap

Demonstrating:
1. Maintaining a Min Heap of fixed size K.
2. The root of the Min Heap always represents the Kth largest element overall.
3. Using Python's built-in `heapq` module for production performance.
"""

import heapq


class KthLargestStream:
    """
    Tracks the Kth largest element in a dynamic stream of numbers.
    Maintains a Min-Heap of size k.
    Space Complexity: O(k)
    Time Complexity: O(log k) per add operation
    """

    def __init__(self, k, nums):
        self.k = k
        self.heap = []
        for x in nums:
            self.add(x)

    def add(self, val):
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, val)
        elif val > self.heap[0]:
            heapq.heapreplace(self.heap, val)

        return self.heap[0]


def find_kth_largest_array(nums, k):
    """
    Find kth largest element in an array in O(n log k) time.
    """
    min_heap = []
    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            heapq.heappop(min_heap)
    return min_heap[0]


def main():
    print("=" * 60)
    print("1. Kth Largest Element in an Array")
    print("=" * 60)
    arr = [3, 2, 1, 5, 6, 4]
    k = 2
    ans = find_kth_largest_array(arr, k)
    print(f"Array: {arr}, k = {k}")
    print(f"{k}nd Largest Element:", ans)

    print("\n" + "=" * 60)
    print("2. Kth Largest in Dynamic Stream")
    print("=" * 60)
    # Stream tracking top 3 elements
    k_stream = 3
    initial_nums = [4, 5, 8, 2]
    tracker = KthLargestStream(k_stream, initial_nums)
    print(f"Initial stream: {initial_nums}, k = {k_stream}")
    print("Current 3rd largest:", tracker.heap[0])

    stream_additions = [3, 5, 10, 9, 4]
    for num in stream_additions:
        res = tracker.add(num)
        print(f"Added {num:2d} -> Heap: {sorted(tracker.heap)} -> Current 3rd Largest: {res}")


if __name__ == "__main__":
    main()
