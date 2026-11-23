"""
Phase 6 - Section I.02: Max Heap
Example 01: Complete Max Heap Implementation from Scratch

Demonstrating:
1. Max-Heap invariant: A[parent(i)] >= A[i] for every node i.
2. Complete Binary Tree array mapping formulas.
3. Sift-Up for O(log n) push and Sift-Down for O(log n) pop_max.
4. Linear time O(n) Floyd's bottom-up max-heapify.
"""


class MaxHeap:
    """Array-backed Binary Max Heap."""

    def __init__(self, items=None):
        self.heap = []
        if items:
            self.heap = list(items)
            self._heapify()

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def _sift_up(self, i):
        """Restore max-heap invariant upwards from index i."""
        while i > 0 and self.heap[i] > self.heap[self._parent(i)]:
            p = self._parent(i)
            self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
            i = p

    def _sift_down(self, i):
        """Restore max-heap invariant downwards from index i."""
        size = len(self.heap)
        largest = i

        while True:
            left = self._left(i)
            right = self._right(i)

            if left < size and self.heap[left] > self.heap[largest]:
                largest = left
            if right < size and self.heap[right] > self.heap[largest]:
                largest = right

            if largest != i:
                self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
                i = largest
            else:
                break

    def _heapify(self):
        """Floyd's bottom-up heapify in O(n) time."""
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._sift_down(i)

    def push(self, val):
        """Insert value into max-heap in O(log n) time."""
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    def pop_max(self):
        """Remove and return maximum element in O(log n) time."""
        if not self.heap:
            raise IndexError("pop from empty heap")

        max_val = self.heap[0]
        last_val = self.heap.pop()

        if self.heap:
            self.heap[0] = last_val
            self._sift_down(0)

        return max_val

    def peek(self):
        """Return maximum element in O(1) time."""
        if not self.heap:
            raise IndexError("peek from empty heap")
        return self.heap[0]

    def __len__(self):
        return len(self.heap)


def main():
    print("=" * 60)
    print("Max Heap Implementation from Scratch")
    print("=" * 60)
    h = MaxHeap()
    elements = [10, 30, 20, 5, 1, 40, 15]
    print("Inserting elements:", elements)
    for x in elements:
        h.push(x)

    print("Internal Heap Array Representation:", h.heap)
    print("Current Maximum (peek)             :", h.peek())

    print("\nExtracting all elements in descending order:")
    extracted = []
    while len(h) > 0:
        extracted.append(h.pop_max())
    print("Extracted (Heap Sort descending)   :", extracted)

    print("\n" + "=" * 60)
    print("Floyd's Bottom-Up Max-Heapify")
    print("=" * 60)
    raw = [4, 10, 3, 5, 1]
    fast_heap = MaxHeap(raw)
    print("Built from raw list:", raw)
    print("Max-Heapified Array :", fast_heap.heap)
    print("Root (Maximum)      :", fast_heap.peek())


if __name__ == "__main__":
    main()
