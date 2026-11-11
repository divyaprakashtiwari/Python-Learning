"""
Phase 6 - Data Structures and Algorithms
Section D: Arrays and Strings - Topic 05: Kadane's Algorithm
Example 02: Maximum Sum Circular Subarray (Total Sum - Minimum Subarray Trick)

Demonstrates:
1. Maximum Sum Circular Subarray (LeetCode 918):
   In a circular array, the maximum subarray either:
   - Case 1 (Non-Wrapping): lives entirely inside the normal array `[0 .. n - 1]` -> `max_kadane`.
   - Case 2 (Wrapping Around Both Ends): takes a prefix AND a suffix of the array, leaving
     a contiguous **Minimum Subarray** in the middle!
     Therefore, `max_wrap_sum = total_sum - min_kadane`!
2. Critical Edge Case: when ALL elements are negative, `total_sum == min_kadane`, which would
   yield `total_sum - min_kadane = 0` (an invalid empty subarray!). We check `if max_kadane < 0: return max_kadane`.
"""


def max_subarray_sum_circular(nums: list[int]) -> tuple[int, int, int]:
    """
    Return `(circular_max_sum, normal_max_kadane, normal_min_kadane)` in a single O(N) pass!
    Time Complexity : O(N)
    Space Complexity: O(1)
    """
    total_sum = 0
    curr_max = 0
    max_so_far = nums[0]
    curr_min = 0
    min_so_far = nums[0]

    for x in nums:
        total_sum += x

        curr_max = max(x, curr_max + x)
        max_so_far = max(max_so_far, curr_max)

        curr_min = min(x, curr_min + x)
        min_so_far = min(min_so_far, curr_min)

    # Edge case: if all numbers are negative, `total_sum == min_so_far`, so wrapping gives 0 (empty!)
    if max_so_far < 0:
        return max_so_far, max_so_far, min_so_far

    circular_best = max(max_so_far, total_sum - min_so_far)
    return circular_best, max_so_far, min_so_far


if __name__ == "__main__":
    print("=" * 72)
    print("1. MAXIMUM SUM CIRCULAR SUBARRAY (LEETCODE 918) IN 1 PASS")
    print("=" * 72)

    circular_cases = [
        ("Wrapping Wins [5, -3, 5]", [5, -3, 5]),
        ("Non-Wrapping Wins [1, -2, 3, -2]", [1, -2, 3, -2]),
        ("Heavy Wrap [8, -1, -3, 8]", [8, -1, -3, 8]),
        ("All Negative Edge Case [-3, -2, -5]", [-3, -2, -5]),
    ]

    for label, arr in circular_cases:
        ans, max_k, min_k = max_subarray_sum_circular(arr)
        print(
            f"  {label:<36} | Total={sum(arr):>3}, MaxKadane={max_k:>2}, "
            f"MinKadane={min_k:>3} -> Circular Max: {ans}"
        )
