"""
Question 1: Custom Cyclical Stream Iterator & Sentinel iter() Protocol
Topic: Advanced Python

Key Concepts Tested:
- Python Iterator Protocol (__iter__, __next__, StopIteration)
- Cyclical indexing with state tracking (cursor, cycle counts)
- Two-argument sentinel invocation: iter(callable, sentinel)
- Proper exhaustibility and edge condition handling (empty items, non-positive cycles)
"""

from typing import Any, Callable, List


class RingBufferIterator:
    """
    A cyclical iterator that repeatedly cycles through a sequence of items
    up to a specified maximum number of cycles before raising StopIteration.
    """

    def __init__(self, items: List[Any], max_cycles: int = 1) -> None:
        if not items:
            raise ValueError("Ring buffer items cannot be empty")
        self._items = list(items)
        self._max_cycles = max_cycles
        self._index = 0
        self._completed_cycles = 0

    def __iter__(self) -> "RingBufferIterator":
        """An iterator must return itself from __iter__."""
        return self

    def __next__(self) -> Any:
        """
        Fetches the next item in the cyclical sequence.
        Raises StopIteration when completed_cycles reaches max_cycles.
        """
        if self._max_cycles <= 0 or self._completed_cycles >= self._max_cycles:
            raise StopIteration

        item = self._items[self._index]
        self._index += 1

        if self._index >= len(self._items):
            self._index = 0
            self._completed_cycles += 1

        return item


def read_stream_until_sentinel(source_callable: Callable[[], Any], sentinel_value: Any) -> List[Any]:
    """
    Consumes items from source_callable using the two-argument iter(callable, sentinel)
    protocol until sentinel_value is encountered.
    """
    sentinel_iterator = iter(source_callable, sentinel_value)
    return list(sentinel_iterator)


if __name__ == "__main__":
    print("=== Test A: Custom Ring Buffer Iterator (2 Cycles) ===")
    tasks = ["TASK_A", "TASK_B", "TASK_C"]
    buffer = RingBufferIterator(tasks, max_cycles=2)
    collected = list(buffer)
    print(f"Ring Buffer Iteration (2 complete cycles):\n{collected}")

    print("\n=== Post-Exhaustion Check ===")
    try:
        next(buffer)
        print("Error: Expected StopIteration!")
    except StopIteration:
        print("Invoking next(buffer) after completion correctly raises StopIteration.")

    print("\n=== Test B: Sentinel Iteration ===")
    numbers = [10, 20, 30, -1, 40, 50]
    iterator_src = iter(numbers)

    def read_next() -> int:
        return next(iterator_src, -1)

    stream_result = read_stream_until_sentinel(read_next, sentinel_value=-1)
    print(f"Sentinel Stream Output (stopped at sentinel -1):\n{stream_result}")

    print("\n=== Test C: Edge Cases ===")
    # 1. Empty items
    try:
        RingBufferIterator([])
    except ValueError as e:
        print(f"Empty collection correctly rejected: {e}")

    # 2. Non-positive cycles
    zero_cycle_iter = RingBufferIterator(["X", "Y"], max_cycles=0)
    print(f"Zero cycles produced: {list(zero_cycle_iter)}")
