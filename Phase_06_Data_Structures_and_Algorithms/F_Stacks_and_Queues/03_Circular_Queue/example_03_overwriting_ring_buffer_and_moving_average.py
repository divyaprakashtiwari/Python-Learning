"""
Phase 6 - Data Structures and Algorithms
Section F: Stacks and Queues
Topic 03: Circular Queue
Example 03: Overwriting Ring Buffer for Telemetry Logs & Moving Average from Data Stream

In real-time telemetry, audio DSP, flight black-box recorders, and IoT sensors,
when a circular buffer reaches capacity, a new sample does NOT block or fail —
instead, it **overwrites the oldest sample** in O(1) time!

We demonstrate:
  1. `OverwritingRingBuffer` (Telemetry / Flight Recorder Log):
     Automatically advances both `write_idx` and `front` when full so the buffer
     always holds the most recent `k` samples in O(1) time.
  2. `MovingAverageFromDataStream` (LeetCode 346):
     Maintains a circular array of size `k` and a running `window_sum`. When a new
     value `val` overwrites `buffer[idx]`, updates `window_sum += val - evicted` in
     strict O(1) time and O(k) fixed space!
"""

from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class OverwritingRingBuffer(Generic[T]):
    """Fixed-capacity ring buffer that overwrites the oldest element when full."""

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._buffer: List[Optional[T]] = [None] * capacity
        self._front: int = 0
        self._size: int = 0

    def push_sample(self, sample: T) -> Optional[T]:
        """
        Writes `sample` into the ring buffer in O(1) time.
        If the buffer was already full, overwrites and returns the evicted oldest item.
        """
        if self._size < self._capacity:
            write_idx = (self._front + self._size) % self._capacity
            self._buffer[write_idx] = sample
            self._size += 1
            return None
        else:
            # Buffer is full: overwrite `_buffer[_front]` and advance `_front`!
            evicted = self._buffer[self._front]
            self._buffer[self._front] = sample
            self._front = (self._front + 1) % self._capacity
            return evicted

    def snapshot_chronological(self) -> List[T]:
        """Returns the buffered samples from oldest to newest."""
        return [
            self._buffer[(self._front + i) % self._capacity]  # type: ignore[misc]
            for i in range(self._size)
        ]


class MovingAverageStream:
    """
    Computes the moving average of the last `window_size` numbers in strict O(1) time
    per `.next(val)` call using a circular array of length `window_size` (LeetCode 346).
    """

    def __init__(self, window_size: int) -> None:
        self._window_size = window_size
        self._ring: List[float] = [0.0] * window_size
        self._head_idx: int = 0
        self._count: int = 0
        self._window_sum: float = 0.0

    def next(self, val: float) -> float:
        evicted = self._ring[self._head_idx] if self._count == self._window_size else 0.0
        self._ring[self._head_idx] = val
        self._head_idx = (self._head_idx + 1) % self._window_size
        if self._count < self._window_size:
            self._count += 1
        self._window_sum += val - evicted
        return self._window_sum / self._count


if __name__ == "__main__":
    print("=" * 72)
    print("1. Overwriting Telemetry Ring Buffer (Capacity k = 4)")
    print("=" * 72)

    ring: OverwritingRingBuffer[str] = OverwritingRingBuffer(4)
    events = ["E1_Boot", "E2_Auth", "E3_Query", "E4_Cache", "E5_Alert", "E6_Recover"]
    for ev in events:
        dropped = ring.push_sample(ev)
        print(
            f"  push({ev:<10}) -> Evicted: {str(dropped):<8} | "
            f"Chronological Ring: {ring.snapshot_chronological()}"
        )

    print("\n" + "=" * 72)
    print("2. O(1) Moving Average from Data Stream via Circular Array (Window = 3)")
    print("=" * 72)
    ma = MovingAverageStream(window_size=3)
    for x in [1, 10, 3, 5, 8, 12]:
        avg = ma.next(x)
        print(f"  next({x:>2}) -> window_sum = {ma._window_sum:>4.1f}, moving_avg = {avg:.2f}")

