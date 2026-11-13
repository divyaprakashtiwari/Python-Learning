"""
Phase 6 - Data Structures and Algorithms
Section F: Stacks and Queues
Topic 04: Deque (Double-Ended Queue)
Example 01: Circular Array Deque Implementation (LeetCode 641) vs Sentinel Doubly Linked List

A Deque (Double-Ended Queue, pronounced "deck") generalizes both a Stack and a Queue
by supporting O(1) insertion and deletion at BOTH the FRONT and the REAR:
  - `insertFront(x)` / `appendleft(x)` : O(1)
  - `insertLast(x)`  / `append(x)`     : O(1)
  - `deleteFront()`  / `popleft()`     : O(1)
  - `deleteLast()`   / `pop()`         : O(1)
  - `getFront()` / `getRear()`         : O(1)

Notice the crucial backward-wrap formula for `insertFront(x)` in a circular array:
  `self._front = (self._front - 1) % self._capacity`
In Python, `-1 % k` automatically evaluates to `k - 1`!
"""

from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class MyCircularDeque(Generic[T]):
    """Fixed-capacity Circular Array Deque (LeetCode 641) with O(1) operations at both ends."""

    def __init__(self, k: int) -> None:
        if k <= 0:
            raise ValueError("Capacity k must be positive")
        self._capacity: int = k
        self._buffer: List[Optional[T]] = [None] * k
        self._front: int = 0
        self._size: int = 0

    def insertFront(self, value: T) -> bool:
        """Inserts an item at the front of Deque by stepping `_front` backward modulo k."""
        if self.isFull():
            return False
        self._front = (self._front - 1) % self._capacity
        self._buffer[self._front] = value
        self._size += 1
        return True

    def insertLast(self, value: T) -> bool:
        """Inserts an item at the rear of Deque."""
        if self.isFull():
            return False
        rear_write = (self._front + self._size) % self._capacity
        self._buffer[rear_write] = value
        self._size += 1
        return True

    def deleteFront(self) -> bool:
        """Deletes an item from the front of Deque."""
        if self.isEmpty():
            return False
        self._buffer[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return True

    def deleteLast(self) -> bool:
        """Deletes an item from the rear of Deque."""
        if self.isEmpty():
            return False
        rear_idx = (self._front + self._size - 1) % self._capacity
        self._buffer[rear_idx] = None
        self._size -= 1
        return True

    def getFront(self) -> Optional[T]:
        return None if self.isEmpty() else self._buffer[self._front]

    def getRear(self) -> Optional[T]:
        if self.isEmpty():
            return None
        return self._buffer[(self._front + self._size - 1) % self._capacity]

    def isEmpty(self) -> bool:
        return self._size == 0

    def isFull(self) -> bool:
        return self._size == self._capacity

    def to_list(self) -> List[T]:
        return [
            self._buffer[(self._front + i) % self._capacity]  # type: ignore[misc]
            for i in range(self._size)
        ]


if __name__ == "__main__":
    print("=" * 72)
    print("Circular Array Deque (LeetCode 641) — O(1) Front and Rear Operations")
    print("=" * 72)

    cd: MyCircularDeque[int] = MyCircularDeque(4)
    cd.insertLast(20)
    cd.insertLast(30)
    cd.insertFront(10)
    cd.insertFront(5)
    print(f"After insertLast(20, 30) & insertFront(10, 5):")
    print(f"  Logical Deque : {cd.to_list()} (Front={cd.getFront()}, Rear={cd.getRear()})")
    print(f"  Raw Buffer    : {cd._buffer} (_front={cd._front}, isFull={cd.isFull()})")

    cd.deleteFront()
    cd.deleteLast()
    print(f"\nAfter deleteFront() & deleteLast():")
    print(f"  Logical Deque : {cd.to_list()} (Front={cd.getFront()}, Rear={cd.getRear()})")
    print(f"  Raw Buffer    : {cd._buffer} (_front={cd._front})")

