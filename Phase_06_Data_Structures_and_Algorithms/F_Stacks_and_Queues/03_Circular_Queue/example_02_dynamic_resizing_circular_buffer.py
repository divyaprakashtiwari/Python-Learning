"""
Phase 6 - Data Structures and Algorithms
Section F: Stacks and Queues
Topic 03: Circular Queue
Example 02: Dynamically Resizing Circular Array Queue (Doubling & Halving with Unwrap)

How are industrial dynamic queues/deques implemented when maximum capacity is not
known upfront?
- Maintain a circular buffer of initial capacity `cap = 4`.
- When `size == cap` on `enqueue`, allocate a new buffer of size `2 * cap` and
  **unwrap** the circular elements sequentially into indices `0 .. size - 1` of
  the new array, resetting `front = 0`!
- When `size > 0 and size == cap // 4` on `dequeue`, shrink the buffer to `cap // 2`
  so memory usage stays proportional to active elements without thrashing.
- Both `enqueue` and `dequeue` achieve amortized O(1) time!
"""

from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class DynamicCircularQueue(Generic[T]):
    """Amortized O(1) dynamically resizing circular array queue."""

    MIN_CAPACITY = 4

    def __init__(self, initial_capacity: int = 4) -> None:
        cap = max(self.MIN_CAPACITY, initial_capacity)
        self._buffer: List[Optional[T]] = [None] * cap
        self._front: int = 0
        self._size: int = 0

    @property
    def capacity(self) -> int:
        return len(self._buffer)

    def __len__(self) -> int:
        return self._size

    def _resize(self, new_capacity: int) -> None:
        """Unwraps the circular queue into a fresh contiguous buffer of `new_capacity`."""
        new_buf: List[Optional[T]] = [None] * new_capacity
        old_cap = len(self._buffer)
        for i in range(self._size):
            new_buf[i] = self._buffer[(self._front + i) % old_cap]
        self._buffer = new_buf
        self._front = 0

    def enqueue(self, item: T) -> None:
        if self._size == len(self._buffer):
            self._resize(len(self._buffer) * 2)
        write_idx = (self._front + self._size) % len(self._buffer)
        self._buffer[write_idx] = item
        self._size += 1

    def dequeue(self) -> T:
        if self._size == 0:
            raise IndexError("dequeue from empty DynamicCircularQueue")
        val = self._buffer[self._front]
        assert val is not None
        self._buffer[self._front] = None
        self._front = (self._front + 1) % len(self._buffer)
        self._size -= 1

        # Shrink by half when 1/4 full (prevents oscillation thrashing at 1/2 boundary)
        if self._size > 0 and self._size == len(self._buffer) // 4:
            new_cap = max(self.MIN_CAPACITY, len(self._buffer) // 2)
            if new_cap < len(self._buffer):
                self._resize(new_cap)

        return val

    def to_logical_list(self) -> List[T]:
        cap = len(self._buffer)
        return [self._buffer[(self._front + i) % cap] for i in range(self._size)]  # type: ignore[misc]


if __name__ == "__main__":
    print("=" * 72)
    print("Dynamically Resizing Circular Buffer (Wrap + Unwrap on Double/Shrink)")
    print("=" * 72)

    dq: DynamicCircularQueue[int] = DynamicCircularQueue(4)
    for x in [10, 20, 30]:
        dq.enqueue(x)
    # Pop 2 items so front moves to index 2, then push 40, 50 so buffer wraps around!
    dq.dequeue()
    dq.dequeue()
    dq.enqueue(40)
    dq.enqueue(50)
    dq.enqueue(60)
    print(f"Wrapped Full State (size={len(dq)}/{dq.capacity}):")
    print(f"  Raw Buffer  : {dq._buffer} (front={dq._front})")
    print(f"  Logical FIFO: {dq.to_logical_list()}")

    print("\nTriggering 2x Capacity Doubling via enqueue(70) & enqueue(80):")
    dq.enqueue(70)
    dq.enqueue(80)
    print(f"  Raw Buffer  : {dq._buffer} (front={dq._front}, size={len(dq)}/{dq.capacity})")
    print(f"  Logical FIFO: {dq.to_logical_list()}")

    print("\nDraining 4 items to trigger quarter-full capacity halving:")
    for _ in range(4):
        dq.dequeue()
    print(f"  Raw Buffer  : {dq._buffer} (front={dq._front}, size={len(dq)}/{dq.capacity})")
    print(f"  Logical FIFO: {dq.to_logical_list()}")

