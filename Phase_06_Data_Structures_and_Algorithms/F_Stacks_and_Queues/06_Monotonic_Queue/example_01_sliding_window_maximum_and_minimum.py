"""
Phase 6 - Data Structures and Algorithms
Section F: Stacks and Queues
Topic 06: Monotonic Queue
Example 01: Sliding Window Maximum & Minimum in O(n) Time (LeetCode 239)

What is a Monotonic Queue (Monotonic Deque)?
A Double-Ended Queue (`collections.deque`) that maintains elements in strictly/weakly
monotonic order while supporting:
  1. **Back-End Dominance Pruning (`pop()`):** Before appending a new element `nums[i]`,
     evict all elements from the **rear** that are worse than or equal to `nums[i]`
     (because `nums[i]` is both *newer* and *better*, those older elements can never
     become the window maximum/minimum in the future!).
  2. **Front-End Expiration (`popleft()`):** Evict the front index if it has fallen
     outside the current sliding window (`dq[0] <= i - k`).
  3. **O(1) Extreme Query (`dq[0]`):** The front of the deque always holds the index
     of the maximum (or minimum) element in the current window!

Time Complexity:  O(n) — every index is pushed once and popped at most once!
Space Complexity: O(k) — the deque holds at most `k` indices at any time.
"""

from collections import deque
from typing import Deque, List, Tuple


def sliding_window_max_and_min(nums: List[int], k: int) -> Tuple[List[int], List[int]]:
    """
    Computes both the Sliding Window Maximum and Sliding Window Minimum for all
    windows of size `k` in a single O(n) pass using two monotonic deques.
    """
    if not nums or k <= 0 or k > len(nums):
        return [], []

    max_dq: Deque[int] = deque()  # Monotonic decreasing deque of indices
    min_dq: Deque[int] = deque()  # Monotonic increasing deque of indices
    max_results: List[int] = []
    min_results: List[int] = []

    for i, val in enumerate(nums):
        # 1. Evict expired indices outside the window [i - k + 1 .. i] from the FRONT
        if max_dq and max_dq[0] <= i - k:
            max_dq.popleft()
        if min_dq and min_dq[0] <= i - k:
            min_dq.popleft()

        # 2. Maintain monotonic order by popping dominated elements from the BACK
        while max_dq and nums[max_dq[-1]] <= val:
            max_dq.pop()
        while min_dq and nums[min_dq[-1]] >= val:
            min_dq.pop()

        # 3. Push current index `i`
        max_dq.append(i)
        min_dq.append(i)

        # 4. Record window extremes once the first full window of size `k` is formed
        if i >= k - 1:
            max_results.append(nums[max_dq[0]])
            min_results.append(nums[min_dq[0]])

    return max_results, min_results


if __name__ == "__main__":
    print("=" * 72)
    print("Sliding Window Maximum & Minimum in O(n) Time (LeetCode 239)")
    print("=" * 72)

    nums_sample = [1, 3, -1, -3, 5, 3, 6, 7]
    k_val = 3
    win_max, win_min = sliding_window_max_and_min(nums_sample, k_val)

    print(f"Input Array : {nums_sample}, Window Size k = {k_val}\n")
    for idx in range(len(nums_sample) - k_val + 1):
        window = nums_sample[idx : idx + k_val]
        print(
            f"  Window [{idx}..{idx + k_val - 1}] = {str(window):<15} "
            f"-> Max = {win_max[idx]:>2}, Min = {win_min[idx]:>2}"
        )

