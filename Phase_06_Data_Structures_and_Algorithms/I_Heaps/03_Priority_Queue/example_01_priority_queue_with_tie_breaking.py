"""
Phase 6 - Section I.03: Priority Queue
Example 01: Priority Queue with FIFO Tie-Breaking

Demonstrating:
1. Stable Priority Queue using (priority, count, task) entries.
2. Preventing comparison crashes on unorderable task payloads.
3. Thread-safe queue.PriorityQueue comparison with lightweight heapq wrapper.
"""

import heapq
import itertools
from queue import PriorityQueue as ThreadSafePriorityQueue


class UnorderableTask:
    """A task object without __lt__ defined."""
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Task({self.name})"


class StablePriorityQueue:
    """
    Priority Queue that breaks priority ties using strict FIFO order.
    Uses entry format: [priority, count, task]
    """
    def __init__(self):
        self.pq = []
        self.counter = itertools.count()  # unique sequence count

    def push(self, task, priority=0):
        """Add a new task or update priority."""
        count = next(self.counter)
        entry = [priority, count, task]
        heapq.heappush(self.pq, entry)

    def pop(self):
        """Remove and return the lowest priority task."""
        if not self.pq:
            raise KeyError("pop from an empty priority queue")
        priority, count, task = heapq.heappop(self.pq)
        return task, priority

    def peek(self):
        """Return the lowest priority task without removing."""
        if not self.pq:
            raise KeyError("peek from an empty priority queue")
        return self.pq[0][2], self.pq[0][0]

    def __len__(self):
        return len(self.pq)


def main():
    print("=" * 60)
    print("1. Stable Priority Queue (FIFO Tie-Breaking)")
    print("=" * 60)
    spq = StablePriorityQueue()

    # Enqueue tasks with identical priorities but distinct unorderable objects
    t1 = UnorderableTask("Email Digest", "Send weekly digest")
    t2 = UnorderableTask("DB Backup", "Perform nightly DB backup")
    t3 = UnorderableTask("Health Check", "Ping health endpoint")
    t4 = UnorderableTask("Urgent Alert", "PagerDuty high severity")

    spq.push(t1, priority=2)
    spq.push(t2, priority=2)  # Same priority as t1; FIFO order must hold
    spq.push(t3, priority=3)
    spq.push(t4, priority=1)  # Higher urgency (smaller number)

    print("Initial task count:", len(spq))
    print("Popping all tasks in priority order:")
    while len(spq) > 0:
        task, prio = spq.pop()
        print(f"  Priority {prio}: {task}")

    print("\n" + "=" * 60)
    print("2. Thread-Safe queue.PriorityQueue Verification")
    print("=" * 60)
    tspq = ThreadSafePriorityQueue()
    counter = itertools.count()

    tspq.put((1, next(counter), "Critical System Patch"))
    tspq.put((2, next(counter), "Cache Invalidation"))
    tspq.put((2, next(counter), "Log Rotation"))

    while not tspq.empty():
        prio, count, name = tspq.get()
        print(f"  [Thread-Safe] Priority {prio}: {name}")


if __name__ == "__main__":
    main()
