"""
Phase 6 - Data Structures and Algorithms
Section F: Stacks and Queues
Topic 02: Queue Implementation
Example 03: Binary Number Generator (1..N) & Sliding Time-Window Rate Limiter

Two practical algorithmic applications of a FIFO Queue:
  1. Generate Binary Representations from 1 to N in O(N) Time Using a Queue:
     Instead of converting each integer via bit division, start with `"1"` in a
     queue. Each dequeued binary string `s` is printed, and its two children
     `s + "0"` (which is 2*x) and `s + "1"` (which is 2*x + 1) are enqueued!
     This is a Breadth-First traversal of the implicit binary number tree.
  2. Sliding Time-Window Request Rate Limiter / Hit Counter (LeetCode 362 / 933):
     Processes a stream of chronologically arriving request timestamps and evicts
     expired timestamps older than `t - window_sec` from the front of the queue in
     amortized O(1) time per request.
"""

from collections import deque
from typing import Deque, List, Tuple


def generate_binary_1_to_n(n: int) -> List[str]:
    """Generates binary strings for 1..n in O(n) time using a FIFO queue."""
    if n <= 0:
        return []
    result: List[str] = []
    q: Deque[str] = deque(["1"])

    for _ in range(n):
        curr = q.popleft()
        result.append(curr)
        # Only enqueue children if we still need more binary strings
        if len(result) + len(q) < n:
            q.append(curr + "0")
        if len(result) + len(q) < n:
            q.append(curr + "1")

    return result


class SlidingWindowRateLimiter:
    """
    Allows at most `max_requests` within any rolling `window_sec` time window
    using a FIFO queue of accepted request timestamps.
    """

    def __init__(self, max_requests: int, window_sec: int) -> None:
        self.max_requests = max_requests
        self.window_sec = window_sec
        self._timestamps: Deque[int] = deque()

    def allow_request(self, timestamp_sec: int) -> Tuple[bool, int]:
        """
        Evicts timestamps strictly older than `timestamp_sec - window_sec + 1`,
        and accepts the request if active count < `max_requests`.
        Returns `(allowed, active_requests_in_window)`.
        """
        cutoff = timestamp_sec - self.window_sec
        while self._timestamps and self._timestamps[0] <= cutoff:
            self._timestamps.popleft()

        if len(self._timestamps) < self.max_requests:
            self._timestamps.append(timestamp_sec)
            return True, len(self._timestamps)
        return False, len(self._timestamps)


if __name__ == "__main__":
    print("=" * 72)
    print("1. Generate Binary Numbers 1..12 via FIFO Queue BFS")
    print("=" * 72)
    binaries = generate_binary_1_to_n(12)
    for idx, b_str in enumerate(binaries, start=1):
        print(f"  Decimal {idx:>2} -> Binary {b_str:>4}")

    print("\n" + "=" * 72)
    print("2. Sliding Time-Window API Rate Limiter (Max 3 reqs / 10 seconds)")
    print("=" * 72)
    limiter = SlidingWindowRateLimiter(max_requests=3, window_sec=10)
    request_times = [1, 2, 4, 8, 11, 12, 13]
    for t in request_times:
        allowed, active = limiter.allow_request(t)
        status = "ALLOWED" if allowed else "BLOCKED (429 Too Many Requests)"
        print(
            f"  t = {t:>2}s -> {status:<33} | Active window timestamps: {list(limiter._timestamps)}"
        )

