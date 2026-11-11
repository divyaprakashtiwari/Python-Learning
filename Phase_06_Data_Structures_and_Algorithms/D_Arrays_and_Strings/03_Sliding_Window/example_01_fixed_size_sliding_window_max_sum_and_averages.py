"""
Phase 6 - Data Structures and Algorithms
Section D: Arrays and Strings - Topic 03: Sliding Window
Example 01: Fixed-Size Sliding Window (Max Subarray Sum of Size K & Rolling Averages)

Demonstrates:
1. Why Naive Fixed-Size Window recalculates the sum of `k` elements from scratch on every
   step (`O(N * k)` time), whereas a Sliding Window updates the sum in `O(1)` per step:
   `window_sum += arr[right] - arr[right - k]` -> `O(N)` total time and `O(1)` space!
2. Maximum Sum Subarray of Fixed Size `k` and 1-Pass Rolling Window Averages.
"""


def max_sum_subarray_fixed_k(
    arr: list[int], k: int
) -> tuple[int, int, list[int]]:
    """
    Find the contiguous subarray of exact length `k` with the maximum sum in O(N) time.
    Returns (max_sum, start_index, best_subarray).
    """
    n = len(arr)
    if k <= 0 or k > n:
        raise ValueError(f"Window size k={k} must be in [1 .. {n}]")

    # 1. Compute sum of the initial window [0 .. k - 1]
    window_sum = sum(arr[:k])
    max_sum = window_sum
    best_start = 0

    # 2. Slide window 1 step right at a time: add entering `arr[right]`, subtract leaving `arr[right - k]`
    for right in range(k, n):
        window_sum += arr[right] - arr[right - k]
        if window_sum > max_sum:
            max_sum = window_sum
            best_start = right - k + 1

    return max_sum, best_start, arr[best_start : best_start + k]


def rolling_window_averages(arr: list[int], k: int) -> list[float]:
    """Compute moving average of every contiguous window of size `k` in O(N) time."""
    n = len(arr)
    if k <= 0 or k > n:
        return []

    window_sum = sum(arr[:k])
    averages = [round(window_sum / k, 2)]

    for right in range(k, n):
        window_sum += arr[right] - arr[right - k]
        averages.append(round(window_sum / k, 2))

    return averages


if __name__ == "__main__":
    print("=" * 72)
    print("1. FIXED-SIZE SLIDING WINDOW: MAX SUBARRAY SUM OF SIZE K = 3")
    print("=" * 72)

    hourly_requests = [120, 340, 210, 580, 490, 150, 620, 310, 280]
    best_sum, start_i, sub = max_sum_subarray_fixed_k(hourly_requests, k=3)
    print(f"Hourly Traffic (N={len(hourly_requests)}): {hourly_requests}")
    print(f"Peak 3-Hour Window    : Start Index {start_i} -> {sub} (Sum = {best_sum})")

    print("\n" + "=" * 72)
    print("2. 4-DAY ROLLING MOVING AVERAGES IN O(N) TIME")
    print("=" * 72)
    prices = [100, 104, 108, 102, 110, 116, 112, 120]
    print(f"Daily Closing Prices  : {prices}")
    print(f"4-Day Moving Averages : {rolling_window_averages(prices, k=4)}")
