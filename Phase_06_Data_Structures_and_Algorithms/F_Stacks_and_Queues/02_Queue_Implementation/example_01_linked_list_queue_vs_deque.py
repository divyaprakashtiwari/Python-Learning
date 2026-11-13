"""
Phase 6 - Data Structures and Algorithms
Section F: Stacks and Queues
Topic 02: Queue Implementation
Example 01: Singly Linked List FIFO Queue vs `collections.deque` vs Why `list.pop(0)` is O(n)

A Queue is a First-In, First-Out (FIFO) linear data structure:
  - `enqueue(x)` : Insert element `x` at the BACK (rear / tail) in O(1) time.
  - `dequeue()`  : Remove and return the element from the FRONT (head) in O(1) time.
  - `peek()`     : Inspect the front element without removing it in O(1) time.

We demonstrate:
  1. Custom Pointer-Based `LinkedQueue` (maintaining both `head` and `tail` pointers
     for strict worst-case O(1) `enqueue` and `dequeue`).
  2. Python's standard library `collections.deque` (`append` + `popleft`).
  3. Empirical operation-count proof of why `list.pop(0)` is an O(n) anti-pattern.
"""

from collections import deque
from typing import Deque, Generic, List, Optional, TypeVar

T = TypeVar("T")


class _QNode(Generic[T]):
    __slots__ = ("val", "next")

    def __init__(self, val: T) -> None:
        self.val: T = val
        self.next: Optional["_QNode[T]"] = None


class LinkedQueue(Generic[T]):
    """
    FIFO Queue backed by a singly linked list with both `_head` (front) and
    `_tail` (rear) pointers for strict O(1) worst-case enqueue and dequeue.
    """

    def __init__(self) -> None:
        self._head: Optional[_QNode[T]] = None
        self._tail: Optional[_QNode[T]] = None
        self._size: int = 0

    def enqueue(self, item: T) -> None:
        """Appends `item` at the rear (`_tail`) in strict O(1) time."""
        new_node = _QNode(item)
        if self._tail is None:
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def dequeue(self) -> T:
        """Removes and returns the front (`_head`) item in strict O(1) time."""
        if self._head is None:
            raise IndexError("dequeue from an empty LinkedQueue")
        front_val = self._head.val
        self._head = self._head.next
        if self._head is None:
            # Queue just became empty -> must also clear `_tail`!
            self._tail = None
        self._size -= 1
        return front_val

    def peek(self) -> T:
        """Returns the front item without removing it in O(1) time."""
        if self._head is None:
            raise IndexError("peek from an empty LinkedQueue")
        return self._head.val

    def is_empty(self) -> bool:
        return self._head is None

    def __len__(self) -> int:
        return self._size

    def to_list(self) -> List[T]:
        out: List[T] = []
        curr = self._head
        while curr is not None:
            out.append(curr.val)
            curr = curr.next
        return out


if __name__ == "__main__":
    print("=" * 72)
    print("1. LinkedQueue (Head + Tail Pointers) vs `collections.deque` FIFO Check")
    print("=" * 72)

    lq: LinkedQueue[str] = LinkedQueue()
    dq: Deque[str] = deque()

    jobs = ["Job_A_Upload", "Job_B_Transcode", "Job_C_Thumbnail", "Job_D_Notify"]
    for job in jobs:
        lq.enqueue(job)
        dq.append(job)

    print(f"After enqueueing 4 jobs: {lq.to_list()}")
    print(f"Front of queue (`peek()`): {lq.peek()} == {dq[0]}")

    print("\nProcessing FIFO queue in arrival order:")
    while not lq.is_empty():
        j1 = lq.dequeue()
        j2 = dq.popleft()
        assert j1 == j2
        print(f"  Dequeued: {j1:<18} | Remaining in queue: {len(lq)}")

    print(f"After draining: is_empty={lq.is_empty()}, _head={lq._head}, _tail={lq._tail}")

    print("\n" + "=" * 72)
    print("2. Why `list.pop(0)` is O(n^2) for Draining n Elements vs O(n) Queue")
    print("=" * 72)
    for n in [1_000, 10_000]:
        list_shifts = n * (n - 1) // 2
        queue_pointer_updates = n
        print(
            f"  n = {n:>6} items -> list.pop(0) element shifts = {list_shifts:>10,} "
            f"| LinkedQueue/deque ops = {queue_pointer_updates:>6,}"
        )

