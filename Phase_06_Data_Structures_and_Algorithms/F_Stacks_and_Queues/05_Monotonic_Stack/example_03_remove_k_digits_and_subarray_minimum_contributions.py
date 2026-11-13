"""
Phase 6 - Data Structures and Algorithms
Section F: Stacks and Queues
Topic 05: Monotonic Stack
Example 03: Remove K Digits for Smallest Number (LeetCode 402), Online Stock Span
            (LeetCode 901) & Sum of Subarray Minimums (LeetCode 907)

Three classic interview variations of the Monotonic Stack pattern:
  1. Remove K Digits to Form the Smallest Possible Integer (LeetCode 402):
     Maintain a monotonic increasing stack of digits. Whenever a smaller digit `d`
     arrives and we still have `k > 0` deletions available, greedily pop the larger
     preceding digit `stack[-1] > d`!
  2. Online Stock Span (LeetCode 901):
     Streams daily stock prices and returns the consecutive number of days (ending
     today) for which the price was `<=` today's price, using a monotonic decreasing
     stack of `(price, span)` pairs in amortized O(1) time per day.
  3. Sum of Subarray Minimums (LeetCode 907 — Contribution Technique):
     Counts how many contiguous subarrays have `arr[i]` as their minimum by finding
     the distance to the Previous Less Element (`left_count`) and Next Less-or-Equal
     Element (`right_count`), contributing `arr[i] * left_count * right_count`!
"""

from typing import List, Tuple


def remove_k_digits(num: str, k: int) -> str:
    """
    Removes `k` digits from `num` so that the new number is the smallest possible
    non-negative integer (LeetCode 402) in O(n) time.
    """
    stack: List[str] = []
    for digit in num:
        while k > 0 and stack and stack[-1] > digit:
            stack.pop()
            k -= 1
        stack.append(digit)

    # If `k > 0` remains (e.g., already non-decreasing like "12345"), trim from the right
    if k > 0:
        stack = stack[:-k]

    result = "".join(stack).lstrip("0")
    return result if result else "0"


class StockSpanner:
    """Computes online stock price spans in amortized O(1) time (LeetCode 901)."""

    def __init__(self) -> None:
        self._stack: List[Tuple[int, int]] = []  # (price, accumulated_span)

    def next(self, price: int) -> int:
        span = 1
        while self._stack and self._stack[-1][0] <= price:
            span += self._stack.pop()[1]
        self._stack.append((price, span))
        return span


def sum_of_subarray_minimums(arr: List[int]) -> int:
    """
    Computes the sum of `min(subarray)` over all contiguous subarrays in O(n) time
    (LeetCode 907). Uses strict `<` on the left and `<=` on the right to avoid
    double-counting subarrays when duplicate minimums exist!
    """
    MOD = 10**9 + 7
    n = len(arr)
    left_dist = [0] * n
    right_dist = [0] * n

    # Previous Strictly Less Element (<)
    stack: List[int] = []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        left_dist[i] = i - stack[-1] if stack else i + 1
        stack.append(i)

    # Next Less-or-Equal Element (<=) — note `>` in while loop
    stack.clear()
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        right_dist[i] = stack[-1] - i if stack else n - i
        stack.append(i)

    total = 0
    for i in range(n):
        total = (total + arr[i] * left_dist[i] * right_dist[i]) % MOD
    return total


if __name__ == "__main__":
    print("=" * 72)
    print("1. Remove K Digits for Smallest Number (LeetCode 402)")
    print("=" * 72)
    for s, k_rem in [("1432219", 3), ("10200", 1), ("10", 2), ("12345", 2)]:
        print(f"  num = '{s}', k = {k_rem} -> smallest = '{remove_k_digits(s, k_rem)}'")

    print("\n" + "=" * 72)
    print("2. Online Stock Span (LeetCode 901)")
    print("=" * 72)
    spanner = StockSpanner()
    prices = [100, 80, 60, 70, 60, 75, 85]
    spans = [spanner.next(p) for p in prices]
    print(f"  Daily Prices : {prices}")
    print(f"  Stock Spans  : {spans}")

    print("\n" + "=" * 72)
    print("3. Sum of Subarray Minimums via Monotonic Contribution (LeetCode 907)")
    print("=" * 72)
    for sample in [[3, 1, 2, 4], [11, 81, 94, 43, 3]]:
        print(f"  Array: {str(sample):<22} -> Sum of Subarray Mins = {sum_of_subarray_minimums(sample)}")

