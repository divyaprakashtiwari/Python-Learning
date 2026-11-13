"""
Phase 6 - Data Structures and Algorithms
Section F: Stacks and Queues
Topic 03: Circular Queue
Example 01: Fixed-Capacity Array-Backed Circular Queue (Ring Buffer — LeetCode 622)

Why do we need a Circular Queue (Ring Buffer) when we have a dynamic array?
- In an ordinary array queue, advancing `front` on every `dequeue()` leaves dead,
  unusable slots at the left end of the array (`[None, None, None, 40, 50]`), even
  when the array has plenty of free slots!
- A Circular Queue wraps indices around the fixed capacity `k` using modulo arithmetic:
    `rear_index = (self.front + self.size - 1) % self.capacity`
    `next_write = (self.front + self.size) % self.capacity`
    `self.front = (self.front + 1) % self.capacity`
- All operations (`enQueue`, `deQueue`, `Front`, `Rear`, `isEmpty`, `isFull`) run in
  strict worst-case O(1) time and zero dynamic memory allocations after initialization!
"""

from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class MyCircularQueue(Generic[T]):
    """
    Fixed-capacity Ring Buffer implementation (LeetCode 622) using `front` index
    and explicit `size` counter to distinguish full (`size == k`) from empty (`size == 0`).
    """

    def __init__(self, k: int) -> None:
        if k <= 0:
            raise ValueError("Capacity k must be positive")
        self._capacity: int = k
        self._buffer: List[Optional[T]] = [None] * k
        self._front: int = 0
        self._size: int = 0

    def enQueue(self, value: T) -> bool:
        """Inserts an element into the circular queue. Returns True if successful."""
        if self.isFull():
            return False
        write_idx = (self._front + self._size) % self._capacity
        self._buffer[write_idx] = value
        self._size += 1
        return True

    def deQueue(self) -> bool:
        """Deletes an element from the front of the circular queue. Returns True if successful."""
        if self.isEmpty():
            return False
        self._buffer[self._front] = None  # Clear reference for GC
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return True

    def Front(self) -> Optional[T]:
        """Gets the front item from the queue, or None if empty."""
        if self.isEmpty():
            return None
        return self._buffer[self._front]

    def Rear(self) -> Optional[T]:
        """Gets the last item from the queue, or None if empty."""
        if self.isEmpty():
            return None
        rear_idx = (self._front + self._size - 1) % self._capacity
        return self._buffer[rear_idx]

    def isEmpty(self) -> bool:
        return self._size == 0

    def isFull(self) -> bool:
        return self._size == self._capacity

    def debug_state(self) -> str:
        return (
            f"buffer={self._buffer}, front={self._front}, "
            f"size={self._size}/{self._capacity}, Front()={self.Front()}, Rear()={self.Rear()}"
        )


if __name__ == "__main__":
    print("=" * 72)
    print("Fixed-Capacity Circular Queue / Ring Buffer (Capacity k = 4)")
    print("=" * 72)

    cq: MyCircularQueue[int] = MyCircularQueue(4)
    for x in [10, 20, 30, 40]:
        ok = cq.enQueue(x)
        print(f"enQueue({x}) -> {ok:<5} | {cq.debug_state()}")

    print(f"enQueue(50) on full queue -> {cq.enQueue(50)}")

    print("\nDequeueing 2 items to free slots 0 and 1:")
    cq.deQueue()
    cq.deQueue()
    print(f"After 2 deQueues  | {cq.debug_state()}")

    print("\nWrapping around the end of the array (enQueue 50 and 60 into slots 0 & 1):")
    cq.enQueue(50)
    print(f"After enQueue(50) | {cq.debug_state()}")
    cq.enQueue(60)
    print(f"After enQueue(60) | {cq.debug_state()}")

