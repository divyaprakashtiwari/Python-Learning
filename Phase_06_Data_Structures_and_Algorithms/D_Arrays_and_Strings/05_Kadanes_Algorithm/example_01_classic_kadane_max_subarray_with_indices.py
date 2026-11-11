"""
Phase 6 - Data Structures and Algorithms
Section D: Arrays and Strings - Topic 05: Kadane's Algorithm
Example 01: Classic Kadane's Algorithm (Maximum Subarray Sum & Exact Index Reconstruction)

Demonstrates:
1. Why Brute-Force Maximum Subarray Sum takes O(N^2) time, whereas Jay Kadane's 1984
   algorithm solves it in a single O(N) pass and O(1) auxiliary space!
2. Core DP transition at index `i`:
   Should we EXTEND the best subarray ending at `i - 1` (`curr_sum + nums[i]`), or
   START FRESH at index `i` (`nums[i]`) because `curr_sum < 0` was dragging us down?
   `curr_sum = max(nums[i], curr_sum + nums[i])`.
3. Reconstructing the exact `[best_start .. best_end]` subarray indices AND handling
   arrays where ALL numbers are negative!
"""


def kadane_max_subarray_with_indices(
    nums: list[int],
) -> tuple[int, int, int, list[int]]:
    """
    Find the contiguous non-empty subarray with the maximum sum in O(N) time and O(1) space.
    Returns (max_sum, best_start_idx, best_end_idx, subarray).
    Correctly handles all-negative arrays (returns the least-negative single element).
    """
    if not nums:
        raise ValueError("Input array must be non-empty")

    curr_sum = nums[0]
    max_sum = nums[0]
    curr_start = 0
    best_start = 0
    best_end = 0

    for i in range(1, len(nums)):
        val = nums[i]
        # If previous running sum is negative, discard it and start fresh at `i`!
        if curr_sum < 0:
            curr_sum = val
            curr_start = i
        else:
            curr_sum += val

        if curr_sum > max_sum:
            max_sum = curr_sum
            best_start = curr_start
            best_end = i

    return max_sum, best_start, best_end, nums[best_start : best_end + 1]


if __name__ == "__main__":
    print("=" * 72)
    print("1. KADANE'S ALGORITHM: MAXIMUM SUBARRAY SUM & EXACT INDICES")
    print("=" * 72)

    test_cases = [
        ("Classic LeetCode 53", [-2, 1, -3, 4, -1, 2, 1, -5, 4]),
        ("All Negative Numbers", [-8, -3, -6, -2, -5, -4]),
        ("Profit/Loss Swing", [15, -20, 12, 18, -5, 25, -40, 10]),
    ]

    for label, sample in test_cases:
        best_sum, s_idx, e_idx, sub = kadane_max_subarray_with_indices(sample)
        print(f"\n[{label}] Input: {sample}")
        print(
            f"  Max Sum = {best_sum:>3} | Range: [{s_idx} .. {e_idx}] -> Subarray: {sub}"
        )
