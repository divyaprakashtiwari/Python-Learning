"""
Phase 6 - Section I.02: Max Heap
Example 02: Pythonic Max Heap Patterns with heapq

Demonstrating:
1. Emulating Max Heap by negating values with heapq.
2. Custom MaxHeapWrapper class using inverted comparison operator (__lt__).
3. Using Python's internal _heapify_max and _heappop_max functions.
"""

import heapq


def max_heap_with_negation(nums):
    """
    Standard Python pattern for max heap:
    Negate elements so the largest positive value becomes the smallest negative value.
    """
    # Push negated values
    heap = [-x for x in nums]
    heapq.heapify(heap)

    result = []
    while heap:
        # Pop and negate back to original positive value
        result.append(-heapq.heappop(heap))
    return result


class MaxHeapItem:
    """Wrapper to invert comparisons for complex objects or custom types."""
    def __init__(self, val, data=None):
        self.val = val
        self.data = data

    def __lt__(self, other):
        # Inverted comparison: greater val has higher priority
        return self.val > other.val

    def __repr__(self):
        return f"Item(val={self.val}, data='{self.data}')"


def max_heap_with_wrapper(tasks):
    """Priority queue where higher priority value is popped first."""
    heap = [MaxHeapItem(priority, name) for priority, name in tasks]
    heapq.heapify(heap)

    processed = []
    while heap:
        item = heapq.heappop(heap)
        processed.append((item.val, item.data))
    return processed


def max_heap_internal_methods(nums):
    """Using CPython internal _heapify_max and _heappop_max."""
    h = list(nums)
    heapq._heapify_max(h)

    popped = []
    while h:
        popped.append(heapq._heappop_max(h))
    return popped


def main():
    print("=" * 60)
    print("1. Max Heap via Value Negation")
    print("=" * 60)
    raw_nums = [20, 5, 100, 45, 12, 88]
    descending = max_heap_with_negation(raw_nums)
    print("Original Numbers:", raw_nums)
    print("Popped via Negation Max-Heap:", descending)

    print("\n" + "=" * 60)
    print("2. Max Heap via Inverted __lt__ Wrapper")
    print("=" * 60)
    tasks = [(1, "Low Priority Task"), (10, "Critical Hotfix"), (5, "Feature Update")]
    print("Input Tasks:", tasks)
    ordered_tasks = max_heap_with_wrapper(tasks)
    print("Tasks Processed by Priority Descending:")
    for prio, name in ordered_tasks:
        print(f"  Priority {prio:2d}: {name}")

    print("\n" + "=" * 60)
    print("3. Max Heap via heapq Internal Functions")
    print("=" * 60)
    internal_res = max_heap_internal_methods(raw_nums)
    print("Popped via _heappop_max:", internal_res)


if __name__ == "__main__":
    main()
