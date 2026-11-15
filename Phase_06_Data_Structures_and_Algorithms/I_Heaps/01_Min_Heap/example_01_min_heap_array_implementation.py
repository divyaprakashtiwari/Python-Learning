"""
Phase 6 - Section I.01: Min Heap
Example 01: Complete Array-Based Min Heap Implementation from Scratch

Demonstrating:
1. Complete Binary Tree representation in a flat 1D array:
   - parent(i) = (i - 1) // 2
   - left(i)   = 2 * i + 1
   - right(i)  = 2 * i + 2
2. Sift-Up (Bubble-Up) for push in O(log n).
3. Sift-Down (Bubble-Down) for pop_min in O(log n).
4. peek() in O(1).
"""


class MinHeap:
    """Array-backed Binary Min Heap."""

    def __init__(self):
        self.heap = []

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def _sift_up(self, i):
        """Restore min-heap invariant upwards from index i."""
        while i > 0 and self.heap[i] < self.heap[self._parent(i)]:
            p = self._parent(i)
            self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
            i = p

    def _sift_down(self, i):
        """Restore min-heap invariant downwards from index i."""
        size = len(self.heap)
        smallest = i

        while True:
            left = self._left(i)
            right = self._right(i)

            if left < size and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < size and self.heap[right] < self.heap[smallest]:
                smallest = right

            if smallest != i:
                self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
                i = smallest
            else:
                break

    def push(self, val):
        """Insert value into heap in O(log n) time."""
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    def pop_min(self):
        """Remove and return minimum element in O(log n) time."""
        if not self.heap:
            raise IndexError("pop from empty heap")

        min_val = self.heap[0]
        last_val = self.heap.pop()

        if self.heap:
            self.heap[0] = last_val
            self._sift_down(0)

        return min_val

    def peek(self):
        """Return minimum element without removing in O(1) time."""
        if not self.heap:
            raise IndexError("peek from empty heap")
        return self.heap[0]

    def __len__(self):
        return len(self.heap)


def main():
    print("=" * 60)
    print("Min Heap Operations from Scratch")
    print("=" * 60)
    h = MinHeap()
    elements = [15, 10, 20, 17, 8, 25, 5]
    print("Inserting elements:", elements)
    for x in elements:
        h.push(x)

    print("Internal Heap Array Representation:", h.heap)
    print("Current Minimum (peek)             :", h.peek())

    print("\nExtracting all elements in sorted order:")
    extracted = []
    while len(h) > 0:
        extracted.append(h.pop_min())
    print("Extracted (Heap Sort)              :", extracted)


if __name__ == "__main__":
    main()
