"""
Phase 6 - Data Structures and Algorithms
Section F: Stacks and Queues
Topic 06: Monotonic Queue
Example 03: Shortest Subarray With Sum >= K with Negative Numbers (LeetCode 862 Hard)
            & Jump Game VI Monotonic Queue DP Optimization (LeetCode 1696)

Two advanced O(n) algorithms unlocked by Monotonic Queues:

1. Shortest Subarray with Sum at Least K with Negative Numbers (LeetCode 862 Hard):
   - When an array contains negative numbers, the prefix sum `P` is NOT monotonic,
     so a standard two-pointer sliding window fails!
   - We want the smallest `j - i` such that `P[j] - P[i] >= k`.
   - Maintain a **Monotonic Increasing Deque of prefix indices**:
     a) **Front Pop (`P[j] - P[dq[0]] >= k`):** `dq[0]` forms a valid subarray ending
        at `j`. Once recorded, `dq[0]` never needs to be tested with any future `j' > j`
        because `j' - dq[0] > j - dq[0]`, so pop `dq.popleft()`!
     b) **Back Pop (`P[j] <= P[dq[-1]]`):** If a later index `j` has a smaller or equal
        prefix sum than an earlier index `dq[-1]`, `j` is both *further right* (shorter
        subarray) and *smaller* (larger difference `P[future] - P[j]`), so `dq[-1]` is
        completely dominated and popped!

2. Jump Game VI / Constrained Subsequence DP Optimization (LeetCode 1696):
   - Optimizes `dp[i] = nums[i] + max(dp[i - k .. i - 1])` from O(n * k) to O(n)
     using a Monotonic Decreasing Deque over `dp` values!
"""

from collections import deque
from typing import Deque, List


def shortest_subarray_at_least_k(nums: List[int], k: int) -> int:
    """
    Finds the length of the shortest non-empty contiguous subarray of `nums`
    (which may contain negative numbers) with sum >= `k` in O(n) time (LeetCode 862).
    Returns -1 if no such subarray exists.
    """
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    best_len = n + 1
    dq: Deque[int] = deque()  # Monotonic increasing deque of indices into `prefix`

    for j in range(n + 1):
        # a) Pop valid starting indices from the front to minimize `j - dq[0]`
        while dq and prefix[j] - prefix[dq[0]] >= k:
            best_len = min(best_len, j - dq.popleft())

        # b) Maintain monotonic increasing order of `prefix[idx]` from the back
        while dq and prefix[j] <= prefix[dq[-1]]:
            dq.pop()

        dq.append(j)

    return best_len if best_len <= n else -1


def max_result_jump_game_vi(nums: List[int], k: int) -> int:
    """
    Computes the maximum score to reach index `n - 1` from index `0` where each jump
    can advance at most `k` steps (`dp[i] = nums[i] + max(dp[i-k .. i-1])`) in O(n)
    time using a monotonic decreasing deque (LeetCode 1696).
    """
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    dq: Deque[int] = deque([0])  # Stores indices `idx` with decreasing `dp[idx]`

    for i in range(1, n):
        # Evict indices that are more than `k` steps behind `i`
        while dq and dq[0] < i - k:
            dq.popleft()

        dp[i] = nums[i] + dp[dq[0]]

        # Maintain decreasing order of `dp` in the deque
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        dq.append(i)

    return dp[-1]


if __name__ == "__main__":
    print("=" * 72)
    print("1. Shortest Subarray With Sum >= K (with Negatives — LeetCode 862 Hard)")
    print("=" * 72)
    test_cases = [
        ([2, -1, 2], 3),
        ([84, -37, 32, 40, 95], 167),
        ([1, 2], 4),
    ]
    for arr, target_k in test_cases:
        ans = shortest_subarray_at_least_k(arr, target_k)
        print(f"  nums={str(arr):<26}, k={target_k:<3} -> Shortest Length = {ans}")

    print("\n" + "=" * 72)
    print("2. Jump Game VI — Monotonic Queue DP Optimization in O(n) (LeetCode 1696)")
    print("=" * 72)
    for arr, max_jump in [([1, -1, -2, 4, -7, 3], 2), ([10, -5, -2, 4, 0, 3], 3)]:
        score = max_result_jump_game_vi(arr, max_jump)
        print(f"  nums={str(arr):<26}, k={max_jump} -> Max DP Score = {score}")

