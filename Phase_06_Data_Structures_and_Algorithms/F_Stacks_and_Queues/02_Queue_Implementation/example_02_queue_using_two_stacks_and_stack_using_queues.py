"""
Phase 6 - Data Structures and Algorithms
Section F: Stacks and Queues
Topic 02: Queue Implementation
Example 02: Queue Using Two Stacks (Amortized O(1), LeetCode 232) &
            Stack Using One Queue (LeetCode 225)

Two classic data-structure duality problems asked in almost every interview loop:

1. Implement a FIFO Queue Using Two LIFO Stacks (`in_stack` & `out_stack`, LeetCode 232):
   - `enqueue(x)` : Push `x` onto `in_stack` in strict O(1) time.
   - `dequeue()` / `peek()`: If `out_stack` is non-empty, pop/peek from `out_stack` in O(1).
     Only when `out_stack` is EMPTY do we pour all elements from `in_stack` into
     `out_stack` (`out_stack.append(in_stack.pop())`), which reverses their LIFO order
     into FIFO order!
   - **Amortized Complexity Proof (Banker's Method):** Every element is pushed onto
     `in_stack` once, moved to `out_stack` once, and popped from `out_stack` once
     (at most 3 stack operations per element across its entire lifetime -> O(1) amortized!).

2. Implement a LIFO Stack Using a Single FIFO Queue (LeetCode 225):
   - Upon `push(x)`, enqueue `x` at the back and rotate the preceding `n - 1` items
     to the back so `x` sits at the front of the queue!
"""

from collections import deque
from typing import Deque, Generic, List, TypeVar

T = TypeVar("T")


class TwoStackQueue(Generic[T]):
    """FIFO Queue implemented using two LIFO stacks in amortized O(1) time."""

    def __init__(self) -> None:
        self._in_stack: List[T] = []
        self._out_stack: List[T] = []
        self.total_transfers: int = 0

    def _transfer_if_needed(self) -> None:
        """Pours `_in_stack` into `_out_stack` ONLY when `_out_stack` is empty."""
        if not self._out_stack:
            while self._in_stack:
                self._out_stack.append(self._in_stack.pop())
                self.total_transfers += 1

    def enqueue(self, item: T) -> None:
        """O(1) worst-case push onto `_in_stack`."""
        self._in_stack.append(item)

    def dequeue(self) -> T:
        """Amortized O(1) pop from `_out_stack`."""
        self._transfer_if_needed()
        if not self._out_stack:
            raise IndexError("dequeue from empty TwoStackQueue")
        return self._out_stack.pop()

    def peek(self) -> T:
        """Amortized O(1) peek at `_out_stack[-1]`."""
        self._transfer_if_needed()
        if not self._out_stack:
            raise IndexError("peek from empty TwoStackQueue")
        return self._out_stack[-1]

    def is_empty(self) -> bool:
        return not self._in_stack and not self._out_stack


class OneQueueStack(Generic[T]):
    """LIFO Stack implemented using a single FIFO Queue (LeetCode 225)."""

    def __init__(self) -> None:
        self._q: Deque[T] = deque()

    def push(self, item: T) -> None:
        """Enqueues `item` and rotates the old elements behind it in O(n) time."""
        prev_len = len(self._q)
        self._q.append(item)
        for _ in range(prev_len):
            self._q.append(self._q.popleft())

    def pop(self) -> T:
        """O(1) dequeue from the front."""
        if not self._q:
            raise IndexError("pop from empty OneQueueStack")
        return self._q.popleft()

    def top(self) -> T:
        if not self._q:
            raise IndexError("top from empty OneQueueStack")
        return self._q[0]

    def is_empty(self) -> bool:
        return len(self._q) == 0


if __name__ == "__main__":
    print("=" * 72)
    print("1. TwoStackQueue (LeetCode 232) — Amortized O(1) FIFO Verification")
    print("=" * 72)

    tsq: TwoStackQueue[int] = TwoStackQueue()
    for v in [10, 20, 30]:
        tsq.enqueue(v)
    print(f"After enqueue(10, 20, 30): in_stack={tsq._in_stack}, out_stack={tsq._out_stack}")
    print(f"First dequeue() -> {tsq.dequeue()} (triggered lazy transfer!)")
    print(f"State now        : in_stack={tsq._in_stack}, out_stack={tsq._out_stack}")

    tsq.enqueue(40)
    tsq.enqueue(50)
    print(f"After enqueue(40, 50): in_stack={tsq._in_stack}, out_stack={tsq._out_stack}")

    remaining: List[int] = []
    while not tsq.is_empty():
        remaining.append(tsq.dequeue())
    print(f"Drained remaining FIFO order: {remaining}")
    print(f"Total in->out transfers for 5 elements: {tsq.total_transfers} (exactly 1 per element!)")

    print("\n" + "=" * 72)
    print("2. OneQueueStack (LeetCode 225) — LIFO Behaviour from a Single Queue")
    print("=" * 72)
    oqs: OneQueueStack[str] = OneQueueStack()
    for ch in ["A", "B", "C", "D"]:
        oqs.push(ch)
    popped_order = [oqs.pop() for _ in range(4)]
    print(f"Pushed ['A', 'B', 'C', 'D'] -> Popped LIFO order: {popped_order}")

