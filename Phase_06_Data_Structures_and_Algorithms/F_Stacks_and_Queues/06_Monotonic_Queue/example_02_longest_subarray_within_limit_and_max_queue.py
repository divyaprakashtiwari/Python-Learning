"""
Phase 6 - Data Structures and Algorithms
Section F: Stacks and Queues
Topic 06: Monotonic Queue
Example 02: Longest Subarray With Absolute Diff <= Limit (LeetCode 1438) &
            MaxQueue with O(1) `get_max()`

Two powerful designs built on Monotonic Queues:
  1. Longest Continuous Subarray With Absolute Diff <= Limit (LeetCode 1438):
     A variable-size sliding window `[left .. right]` is valid if and only if
     `max(window) - min(window) <= limit`. By maintaining a Monotonic Decreasing
     Deque (`max_dq`) and a Monotonic Increasing Deque (`min_dq`), we check
     `nums[max_dq[0]] - nums[min_dq[0]] > limit` and shrink `left` in O(n) total time!
  2. `MaxQueue` (FIFO Queue supporting O(1) `enqueue`, `dequeue`, and `get_max`):
     Combines a standard FIFO `deque` of items with a shadow monotonic decreasing
     deque of candidate maximums.
"""

from collections import deque
from typing import Deque, List, Tuple


def longest_subarray_abs_diff_limit(nums: List[int], limit: int) -> Tuple[int, List[int]]:
    """
    Finds the longest contiguous subarray where the absolute difference between any
    two elements is `<= limit` in O(n) time (LeetCode 1438).
    """
    max_dq: Deque[int] = deque()
    min_dq: Deque[int] = deque()
    left = 0
    best_len = 0
    best_start = 0

    for right, val in enumerate(nums):
        while max_dq and nums[max_dq[-1]] < val:
            max_dq.pop()
        while min_dq and nums[min_dq[-1]] > val:
            min_dq.pop()
        max_dq.append(right)
        min_dq.append(right)

        # Shrink window from the left while max - min exceeds `limit`
        while nums[max_dq[0]] - nums[min_dq[0]] > limit:
            if max_dq[0] == left:
                max_dq.popleft()
            if min_dq[0] == left:
                min_dq.popleft()
            left += 1

        curr_len = right - left + 1
        if curr_len > best_len:
            best_len = curr_len
            best_start = left

    return best_len, nums[best_start : best_start + best_len]


class MaxQueue:
    """
    FIFO Queue supporting worst-case O(1) `dequeue()` and `get_max()`, and
    amortized O(1) `enqueue(x)` using a companion monotonic decreasing deque.
    """

    def __init__(self) -> None:
        self._items: Deque[int] = deque()
        self._max_candidates: Deque[int] = deque()

    def enqueue(self, val: int) -> None:
        self._items.append(val)
        # Note strict `<` so duplicate maximums are preserved individually!
        while self._max_candidates and self._max_candidates[-1] < val:
            self._max_candidates.pop()
        self._max_candidates.append(val)

    def dequeue(self) -> int:
        if not self._items:
            raise IndexError("dequeue from empty MaxQueue")
        front = self._items.popleft()
        if front == self._max_candidates[0]:
            self._max_candidates.popleft()
        return front

    def get_max(self) -> int:
        if not self._max_candidates:
            raise IndexError("get_max from empty MaxQueue")
        return self._max_candidates[0]


if __name__ == "__main__":
    print("=" * 72)
    print("1. Longest Subarray With Absolute Diff <= Limit in O(n) (LeetCode 1438)")
    print("=" * 72)
    samples = [
        ([8, 2, 4, 7], 4),
        ([10, 1, 2, 4, 7, 2], 5),
        ([4, 2, 2, 2, 4, 4, 2, 2], 0),
    ]
    for arr, lim in samples:
        length, sub = longest_subarray_abs_diff_limit(arr, lim)
        print(f"  nums={str(arr):<28}, limit={lim} -> max_len={length}, subarray={sub}")

    print("\n" + "=" * 72)
    print("2. MaxQueue — Amortized O(1) Enqueue, Dequeue, and GetMax")
    print("=" * 72)
    mq = MaxQueue()
    for x in [4, 7, 2, 7, 5]:
        mq.enqueue(x)
        print(f"  enqueue({x}) -> items={list(mq._items)}, get_max()={mq.get_max()}")

    for _ in range(4):
        popped = mq.dequeue()
        print(f"  dequeue() -> {popped} | items={list(mq._items)}, get_max()={mq.get_max()}")

