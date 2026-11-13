"""
Phase 6 - Data Structures and Algorithms
Section F: Stacks and Queues
Topic 05: Monotonic Stack
Example 01: Next Greater Element I, Circular Next Greater Element II & Daily Temperatures

What is a Monotonic Stack?
A stack whose elements (or the array values at the indices stored in the stack)
are maintained in strictly/weakly **monotonic order** (either decreasing from
bottom to top, or increasing from bottom to top).

1. Monotonic Decreasing Stack (finds the **Next Greater Element** to the right):
   - As we scan `nums[i]` left-to-right, while `stack` is non-empty and
     `nums[i] > nums[stack[-1]]`, `nums[i]` is the **first greater element to the
     right** of `stack.pop()`!
   - Why is this O(n) total time despite the nested `while` loop?
     Each index `0 .. n - 1` is pushed onto the stack **once** and popped at most
     **once** -> at most 2n stack operations total!

2. Applications demonstrated here:
   - Next Greater Element (right and left) in a single O(n) pass.
   - Daily Temperatures (LeetCode 739): days until a warmer temperature.
   - Next Greater Element II on a Circular Array (LeetCode 503): scanning `0 .. 2*n - 1`
     using `i % n`.
"""

from typing import List, Tuple


def next_and_prev_greater_elements(nums: List[int]) -> Tuple[List[int], List[int]]:
    """
    Computes in a SINGLE O(n) pass using a monotonic decreasing stack of indices:
      - `next_greater[i]`: first value strictly greater than `nums[i]` to its RIGHT (or -1)
      - `prev_greater[i]`: first value strictly greater than `nums[i]` to its LEFT (or -1)
    """
    n = len(nums)
    next_greater = [-1] * n
    prev_greater = [-1] * n
    stack: List[int] = []  # Stores indices whose values are monotonically decreasing

    for i, val in enumerate(nums):
        # Pop any indices whose value is strictly smaller than `val`:
        # `val` is their Next Greater Element!
        while stack and nums[stack[-1]] < val:
            smaller_idx = stack.pop()
            next_greater[smaller_idx] = val

        # After popping smaller or equal elements, if we also want strict prev_greater,
        # note that if duplicates exist, stack[-1] could equal `val`. To handle duplicates
        # cleanly for prev_greater, we can peek past equals or pop `<=` if needed.
        if stack:
            prev_greater[i] = nums[stack[-1]]

        stack.append(i)

    return next_greater, prev_greater


def daily_temperatures(temperatures: List[int]) -> List[int]:
    """
    For each day `i`, returns the number of days you have to wait until a warmer
    temperature (LeetCode 739), or 0 if no warmer day exists.
    Time Complexity: O(n), Space Complexity: O(n).
    """
    n = len(temperatures)
    wait_days = [0] * n
    stack: List[int] = []  # Monotonic decreasing stack of day indices

    for curr_day, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            prev_day = stack.pop()
            wait_days[prev_day] = curr_day - prev_day
        stack.append(curr_day)

    return wait_days


def next_greater_elements_circular(nums: List[int]) -> List[int]:
    """
    Finds the Next Greater Element in a circular array (LeetCode 503) by iterating
    `2 * n` times with modulo indexing `i % n`.
    """
    n = len(nums)
    res = [-1] * n
    stack: List[int] = []

    for step in range(2 * n):
        idx = step % n
        while stack and nums[stack[-1]] < nums[idx]:
            res[stack.pop()] = nums[idx]
        if step < n:
            stack.append(idx)

    return res


if __name__ == "__main__":
    print("=" * 72)
    print("1. Next Greater & Previous Greater Elements in One O(n) Pass")
    print("=" * 72)
    arr = [2, 7, 4, 3, 5, 1, 9]
    nge, pge = next_and_prev_greater_elements(arr)
    print(f"Input Array      : {arr}")
    print(f"Next Greater     : {nge}")
    print(f"Previous Greater : {pge}")

    print("\n" + "=" * 72)
    print("2. Daily Temperatures — Days Until Warmer Weather (LeetCode 739)")
    print("=" * 72)
    temps = [73, 74, 75, 71, 69, 72, 76, 73]
    print(f"Temperatures : {temps}")
    print(f"Wait Days    : {daily_temperatures(temps)}")

    print("\n" + "=" * 72)
    print("3. Circular Array Next Greater Element II (LeetCode 503)")
    print("=" * 72)
    circ = [1, 2, 1, 4, 3]
    print(f"Circular Array : {circ}")
    print(f"Next Greater   : {next_greater_elements_circular(circ)}")

