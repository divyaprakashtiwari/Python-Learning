"""
Phase 6 - Section I.02: Max Heap
Example 03: Last Stone Weight and Find Median from Data Stream

Demonstrating:
1. Last Stone Weight simulation using Max Heap in O(n log n) time.
2. Continuous Data Stream Median using Dual Heaps:
   - Max-Heap for lower half of numbers (smaller values).
   - Min-Heap for upper half of numbers (larger values).
"""

import heapq


def last_stone_weight(stones):
    """
    Smash the two heaviest stones at each step.
    If x == y, both stones are destroyed.
    If x != y, the stone of weight x is destroyed, and the new stone has weight y - x.
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    # Max-heap via negation
    max_heap = [-s for s in stones]
    heapq.heapify(max_heap)

    while len(max_heap) > 1:
        stone1 = -heapq.heappop(max_heap)
        stone2 = -heapq.heappop(max_heap)

        if stone1 != stone2:
            heapq.heappush(max_heap, -(stone1 - stone2))

    return -max_heap[0] if max_heap else 0


class MedianFinder:
    """
    Finds median from dynamic continuous data stream in O(log n) add and O(1) find.
    Uses two balanced heaps:
    - small: Max-Heap (stores lower half; negated in Python)
    - large: Min-Heap (stores upper half)
    Invariant:
    - len(small) == len(large) OR len(small) == len(large) + 1
    - max(small) <= min(large)
    """

    def __init__(self):
        self.small = []  # Max-heap (negated)
        self.large = []  # Min-heap

    def add_num(self, num):
        # Step 1: Add to small (max-heap)
        heapq.heappush(self.small, -num)

        # Step 2: Ensure every element in small <= every element in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Step 3: Maintain size balance (small can have at most 1 more element than large)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def find_median(self):
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0


def main():
    print("=" * 60)
    print("1. Last Stone Weight Simulation")
    print("=" * 60)
    stones = [2, 7, 4, 1, 8, 1]
    res_stone = last_stone_weight(stones)
    print("Initial Stones:", stones)
    print("Remaining Stone Weight:", res_stone)

    print("\n" + "=" * 60)
    print("2. Find Median from Data Stream (Dual Heaps)")
    print("=" * 60)
    mf = MedianFinder()
    stream = [5, 15, 1, 3]
    for num in stream:
        mf.add_num(num)
        print(f"Added {num:2d} -> Current Median: {mf.find_median():.2f}")


if __name__ == "__main__":
    main()
