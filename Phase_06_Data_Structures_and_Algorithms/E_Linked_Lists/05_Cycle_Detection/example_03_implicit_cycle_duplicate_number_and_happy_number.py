"""
Phase 6 - Data Structures and Algorithms
Section E: Linked Lists
Topic 05: Cycle Detection
Example 03: Implicit Linked List Cycle Detection (Find Duplicate Number & Happy Number)

Floyd's Tortoise and Hare works on ANY deterministic state transition function
`f: S -> S` over a finite set `S`, even when no `ListNode` objects exist in memory!

1. Find the Duplicate Number in O(n) Time and O(1) Space without Modifying the Array
   (LeetCode 287):
   - Given an array `nums` of `n + 1` integers where each integer is in `[1, n]`.
   - Treat each index `i` as a node and `nums[i]` as its `.next` pointer (`i -> nums[i]`).
   - Since `0` never appears in `nums` (values are in `1..n`), index `0` has in-degree 0
     and serves as our `head` outside the cycle!
   - By the Pigeonhole Principle, at least two indices point to the duplicate value `d`,
     making `d` the exact **cycle entry node** (`mu`) of the implicit linked list!

2. Happy Number Detection in O(1) Space (LeetCode 202):
   - Repeatedly replace a number by the sum of the squares of its digits.
   - Either the sequence reaches `1` (which loops `1 -> 1`), or it enters a finite
     cycle not containing `1` (specifically the 8-node cycle containing `4`).
"""

from typing import List, Tuple


def find_duplicate_number_floyd(nums: List[int]) -> int:
    """
    Finds the duplicate number in `nums` (length n + 1, values in 1..n) in
    O(n) time and O(1) auxiliary space without modifying `nums`.
    """
    # Phase 1: Intersect inside the cycle
    slow = nums[0]
    fast = nums[nums[0]]
    while slow != fast:
        slow = nums[slow]
        fast = nums[nums[fast]]

    # Phase 2: Find the entrance to the cycle (the duplicate number)
    ptr1 = 0
    ptr2 = slow
    while ptr1 != ptr2:
        ptr1 = nums[ptr1]
        ptr2 = nums[ptr2]

    return ptr1


def sum_of_squared_digits(n: int) -> int:
    """Computes the sum of squares of base-10 digits of `n`."""
    total = 0
    while n > 0:
        n, digit = divmod(n, 10)
        total += digit * digit
    return total


def is_happy_number_floyd(n: int) -> Tuple[bool, List[int]]:
    """
    Determines whether `n` is a Happy Number in O(1) auxiliary memory using
    Tortoise & Hare, and also returns the trajectory prefix for illustration.
    """
    slow = n
    fast = sum_of_squared_digits(n)
    trajectory = [n]

    while fast != 1 and slow != fast:
        trajectory.append(fast)
        slow = sum_of_squared_digits(slow)
        fast = sum_of_squared_digits(sum_of_squared_digits(fast))

    if fast == 1:
        trajectory.append(1)
        return True, trajectory
    else:
        trajectory.append(fast)
        return False, trajectory


if __name__ == "__main__":
    print("=" * 72)
    print("1. Find the Duplicate Number via Implicit Linked List (LeetCode 287)")
    print("=" * 72)

    arrays = [
        [1, 3, 4, 2, 2],
        [3, 1, 3, 4, 2],
        [2, 5, 9, 6, 9, 3, 8, 9, 7, 1],
    ]
    for arr in arrays:
        dup = find_duplicate_number_floyd(arr)
        print(f"Array: {arr}")
        print(f"  Duplicate (Cycle Entry Node) = {dup}")

    print("\n" + "=" * 72)
    print("2. Happy Number Cycle Detection in O(1) Space (LeetCode 202)")
    print("=" * 72)

    for num in [19, 2, 7, 20]:
        happy, trace = is_happy_number_floyd(num)
        print(f"n = {num:<2} -> Happy: {str(happy):<5} | Fast-Pointer Sample: {trace}")

