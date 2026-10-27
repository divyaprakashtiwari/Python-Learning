"""
Topic 03 - Data Structures: Question 9
Problem: Bounded Stack (LIFO via list) and Bounded Queue (FIFO via collections.deque).
"""

from collections import deque
from typing import Any, List


class BoundedStack:
    """Bounded LIFO Stack backed by a contiguous Python list."""

    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("Capacity must be >= 1")
        self.capacity = capacity
        self._items: List[Any] = []

    def push(self, item: Any) -> None:
        if self.is_full:
            raise OverflowError("Stack is full")
        self._items.append(item)

    def pop(self) -> Any:
        if self.is_empty:
            raise IndexError("Stack is empty")
        return self._items.pop()

    def peek(self) -> Any:
        if self.is_empty:
            raise IndexError("Stack is empty")
        return self._items[-1]

    @property
    def is_empty(self) -> bool:
        return len(self._items) == 0

    @property
    def is_full(self) -> bool:
        return len(self._items) >= self.capacity

    def __len__(self) -> int:
        return len(self._items)


class BoundedQueue:
    """Bounded FIFO Queue backed by collections.deque for O(1) pops and appends."""

    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("Capacity must be >= 1")
        self.capacity = capacity
        self._items: deque = deque()

    def enqueue(self, item: Any) -> None:
        if self.is_full:
            raise OverflowError("Queue is full")
        self._items.append(item)

    def dequeue(self) -> Any:
        if self.is_empty:
            raise IndexError("Queue is empty")
        return self._items.popleft()

    def peek(self) -> Any:
        if self.is_empty:
            raise IndexError("Queue is empty")
        return self._items[0]

    @property
    def is_empty(self) -> bool:
        return len(self._items) == 0

    @property
    def is_full(self) -> bool:
        return len(self._items) >= self.capacity

    def __len__(self) -> int:
        return len(self._items)


# --- Bounded Stack Simulation (Browser History) ---
print("--- Bounded Stack Simulation ---")
history = BoundedStack(capacity=3)
history.push("Page1")
history.push("Page2")
history.push("Page3")
print(f"Pushed: 'Page1', 'Page2', 'Page3' (Current Size: {len(history)}/{history.capacity})")

popped = history.pop()
print(f"Popped Top Page: '{popped}'")
print(f"Current Active Page (Peek): '{history.peek()}'")

try:
    history.push("Page4")
    history.push("Page5")  # Exceeds capacity of 3
except OverflowError as err:
    print(f"Attempted Overflow: Caught OverflowError on capacity breach: {err}")


# --- Bounded Queue Simulation (Print Spooler) ---
print("\n--- Bounded Queue Simulation ---")
spooler = BoundedQueue(capacity=4)
spooler.enqueue("JobA")
spooler.enqueue("JobB")
print(f"Enqueued: 'JobA', 'JobB' (Current Size: {len(spooler)}/{spooler.capacity})")

processed = spooler.dequeue()
print(f"Processed Job (Dequeued): '{processed}'")

spooler.enqueue("JobC")
print("Enqueued: 'JobC'")
print(f"Next Up in Spooler (Peek): '{spooler.peek()}'")

remaining = []
while not spooler.is_empty:
    remaining.append(spooler.dequeue())
print(f"Dequeued Remaining: {remaining}")

# Algorithmic complexity note
print("\nComplexity Analysis:")
print("- deque.popleft() is O(1) amortized via doubly-linked memory blocks.")
print("- list.pop(0) is O(N) because every remaining element must shift left in contiguous RAM.")
