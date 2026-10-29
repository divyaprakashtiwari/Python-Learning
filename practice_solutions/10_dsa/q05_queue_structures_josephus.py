"""
Question 5: Circular Queue, Two-Stack Queue & Josephus Ring Simulation
Topic: Data Structures & Algorithms (DSA)

Key Concepts Tested:
- Fixed-capacity circular buffer with head/tail modulo wrapping
- Two-stack queue achieving amortized O(1) FIFO operations
- Custom underflow and overflow error handling
- Hot potato / Josephus problem circular elimination simulation
"""

from collections import deque
from typing import TypeVar, Generic, List, Tuple, Optional

T = TypeVar("T")


class QueueOverflowError(Exception):
    """Raised when enqueuing into a full fixed-capacity queue."""
    pass


class QueueUnderflowError(Exception):
    """Raised when dequeuing or peeking into an empty queue."""
    pass


class CircularQueue(Generic[T]):
    """
    Fixed-capacity circular queue using a fixed-size list with modulo index pointer wrapping.
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._buffer: List[Optional[T]] = [None] * capacity
        self._head = 0
        self._tail = 0
        self._count = 0

    def enqueue(self, item: T) -> bool:
        """
        Inserts item at the tail if capacity permits.
        Returns True on success, or False if full.
        """
        if self.is_full():
            return False

        self._buffer[self._tail] = item
        self._tail = (self._tail + 1) % self._capacity
        self._count += 1
        return True

    def dequeue(self) -> T:
        """
        Removes and returns the front item.
        Raises QueueUnderflowError if empty.
        """
        if self.is_empty():
            raise QueueUnderflowError("Cannot dequeue from an empty CircularQueue")

        item = self._buffer[self._head]
        self._buffer[self._head] = None
        self._head = (self._head + 1) % self._capacity
        self._count -= 1
        return item  # type: ignore[return-value]

    def front(self) -> T:
        if self.is_empty():
            raise QueueUnderflowError("Cannot read front of an empty CircularQueue")
        return self._buffer[self._head]  # type: ignore[return-value]

    def rear(self) -> T:
        if self.is_empty():
            raise QueueUnderflowError("Cannot read rear of an empty CircularQueue")
        prev_tail = (self._tail - 1 + self._capacity) % self._capacity
        return self._buffer[prev_tail]  # type: ignore[return-value]

    def is_empty(self) -> bool:
        return self._count == 0

    def is_full(self) -> bool:
        return self._count == self._capacity

    def __len__(self) -> int:
        return self._count


class TwoStackQueue(Generic[T]):
    """
    FIFO queue implemented using two independent LIFO stacks.
    Yields O(1) amortized time for both enqueue and dequeue.
    """

    def __init__(self) -> None:
        self._in_stack: List[T] = []
        self._out_stack: List[T] = []

    def enqueue(self, item: T) -> None:
        self._in_stack.append(item)

    def _shift_stacks(self) -> None:
        if not self._out_stack:
            while self._in_stack:
                self._out_stack.append(self._in_stack.pop())

    def dequeue(self) -> T:
        if self.is_empty():
            raise QueueUnderflowError("Cannot dequeue from an empty TwoStackQueue")
        self._shift_stacks()
        return self._out_stack.pop()

    def peek(self) -> T:
        if self.is_empty():
            raise QueueUnderflowError("Cannot peek into an empty TwoStackQueue")
        self._shift_stacks()
        return self._out_stack[-1]

    def is_empty(self) -> bool:
        return len(self._in_stack) == 0 and len(self._out_stack) == 0

    def __len__(self) -> int:
        return len(self._in_stack) + len(self._out_stack)


def josephus_circle(names: List[str], elimination_step: int) -> Tuple[List[str], str]:
    """
    Simulates the Josephus elimination ring.
    Every elimination_step-th participant is removed until one survivor remains.
    """
    if not names:
        raise ValueError("Participant list cannot be empty")
    if elimination_step <= 0:
        raise ValueError("Elimination step must be a positive integer")

    ring: deque[str] = deque(names)
    elimination_order: List[str] = []

    while len(ring) > 1:
        # Pass (elimination_step - 1) times to front of potato
        for _ in range(elimination_step - 1):
            ring.append(ring.popleft())
        # Eliminate current holder
        eliminated_person = ring.popleft()
        elimination_order.append(eliminated_person)

    survivor = ring[0]
    return (elimination_order, survivor)


if __name__ == "__main__":
    print("=== 1. Fixed-Capacity Circular Queue ===")
    cq = CircularQueue[int](capacity=3)
    cq.enqueue(10)
    cq.enqueue(20)
    cq.enqueue(30)
    print(f"Circular Queue Full: {cq.is_full()}")

    d1 = cq.dequeue()
    print(f"Circular Queue Dequeued: {d1}")

    cq.enqueue(40)  # wraps around index 0
    print(f"Circular Queue Rear after 40: {cq.rear()}")

    print("\n=== 2. Two-Stack FIFO Queue ===")
    tsq = TwoStackQueue[str]()
    tsq.enqueue("A")
    tsq.enqueue("B")
    tsq.enqueue("C")
    q_pop1 = tsq.dequeue()
    tsq.enqueue("D")
    q_pop2 = tsq.dequeue()
    print(f"TwoStackQueue Dequeued First: '{q_pop1}'")
    print(f"TwoStackQueue Dequeued Second: '{q_pop2}'")

    print("\n=== 3. Josephus Ring Simulation ===")
    participants = ["Alice", "Bob", "Charlie", "David", "Emma"]
    eliminated, survivor = josephus_circle(participants, elimination_step=3)
    print(f"Josephus Elimination Order: {eliminated}")
    print(f"Josephus Survivor: '{survivor}'")

    print("\n=== 4. Edge Cases & Underflow Errors ===")
    empty_tsq = TwoStackQueue[int]()
    try:
        empty_tsq.dequeue()
    except QueueUnderflowError as err:
        print(f"Caught expected queue underflow: {err}")

    try:
        josephus_circle([], 2)
    except ValueError as err:
        print(f"Caught empty participant list: {err}")
