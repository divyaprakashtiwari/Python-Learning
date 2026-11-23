"""
Phase 6 - Section I.03: Priority Queue
Example 02: Indexed Priority Queue and Decrease-Key Operation

Demonstrating:
1. Indexed Priority Queue (IPQ) mapping element keys to heap array positions.
2. O(log n) decrease_key operation (essential for Dijkstra's algorithm).
3. O(log n) arbitrary element deletion.
"""


class IndexedPriorityQueue:
    """
    Min-Indexed Priority Queue.
    Maintains:
    - heap: list of [key, priority]
    - pos: dict mapping key -> index in heap list
    """

    def __init__(self):
        self.heap = []
        self.pos = {}  # key -> index

    def _swap(self, i, j):
        self.pos[self.heap[i][0]] = j
        self.pos[self.heap[j][0]] = i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.heap[i][1] < self.heap[parent][1]:
                self._swap(i, parent)
                i = parent
            else:
                break

    def _sift_down(self, i):
        size = len(self.heap)
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = i

            if left < size and self.heap[left][1] < self.heap[smallest][1]:
                smallest = left
            if right < size and self.heap[right][1] < self.heap[smallest][1]:
                smallest = right

            if smallest != i:
                self._swap(i, smallest)
                i = smallest
            else:
                break

    def push(self, key, priority):
        """Insert a key with priority in O(log n) time."""
        if key in self.pos:
            raise KeyError(f"Key '{key}' already exists in priority queue")

        idx = len(self.heap)
        self.heap.append([key, priority])
        self.pos[key] = idx
        self._sift_up(idx)

    def pop_min(self):
        """Extract key and priority with minimum priority in O(log n) time."""
        if not self.heap:
            raise IndexError("pop from empty priority queue")

        min_key, min_prio = self.heap[0]
        last_key, last_prio = self.heap.pop()
        del self.pos[min_key]

        if self.heap:
            self.heap[0] = [last_key, last_prio]
            self.pos[last_key] = 0
            self._sift_down(0)

        return min_key, min_prio

    def decrease_key(self, key, new_priority):
        """
        Decrease priority of an existing key in O(log n) time.
        Raises ValueError if new_priority is greater than current priority.
        """
        if key not in self.pos:
            raise KeyError(f"Key '{key}' not found in priority queue")

        idx = self.pos[key]
        if new_priority > self.heap[idx][1]:
            raise ValueError("new priority cannot be greater than current priority")

        self.heap[idx][1] = new_priority
        self._sift_up(idx)

    def delete(self, key):
        """Delete an arbitrary key from the queue in O(log n) time."""
        if key not in self.pos:
            raise KeyError(f"Key '{key}' not found in priority queue")

        idx = self.pos[key]
        last_idx = len(self.heap) - 1

        if idx == last_idx:
            del self.pos[key]
            self.heap.pop()
            return

        self._swap(idx, last_idx)
        del self.pos[key]
        self.heap.pop()

        # May need sift-down or sift-up depending on replacement key value
        self._sift_down(idx)
        self._sift_up(idx)

    def contains(self, key):
        return key in self.pos

    def __len__(self):
        return len(self.heap)


def main():
    print("=" * 60)
    print("Indexed Priority Queue with O(log n) Decrease-Key")
    print("=" * 60)
    ipq = IndexedPriorityQueue()

    # Initial graph vertices with tentative distances
    ipq.push("A", 10)
    ipq.push("B", 25)
    ipq.push("C", 15)
    ipq.push("D", 30)

    print("Initial IPQ (key -> pos):", ipq.pos)
    print("Initial Heap Array       :", ipq.heap)

    # Decrease distance to B from 25 down to 5 (shorter path found)
    print("\nExecuting decrease_key('B', 5)...")
    ipq.decrease_key("B", 5)
    print("Updated IPQ (key -> pos) :", ipq.pos)
    print("Updated Heap Array       :", ipq.heap)

    # Delete C
    print("\nExecuting delete('C')...")
    ipq.delete("C")
    print("After deleting 'C'       :", ipq.heap)

    print("\nExtracting all remaining in priority order:")
    while len(ipq) > 0:
        k, prio = ipq.pop_min()
        print(f"  Popped: {k} (distance: {prio})")


if __name__ == "__main__":
    main()
