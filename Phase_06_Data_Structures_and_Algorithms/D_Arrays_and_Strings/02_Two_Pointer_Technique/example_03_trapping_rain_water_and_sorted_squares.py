"""
Phase 6 - Data Structures and Algorithms
Section D: Arrays and Strings - Topic 02: Two Pointer Technique
Example 03: Trapping Rain Water (O(N) Time, O(1) Space Two-Pointer Solution) & Squares of Sorted Array

Demonstrates:
1. Trapping Rain Water (LeetCode 42):
   Instead of allocating O(N) `prefix_max` and `suffix_max` arrays, maintain `left_max` and
   `right_max` with two converging pointers (`left`, `right`) in O(N) time and strictly O(1) space!
2. Squares of a Sorted Array with Negatives (LeetCode 977) in O(N) time (instead of O(N log N)
   sorting after squaring) by comparing absolute values at `left` and `right` and filling backward!
"""


def trap_rain_water_two_pointers(heights: list[int]) -> int:
    """
    Compute total units of rain water trapped between bars in `heights` in O(N) time
    and strictly O(1) auxiliary space using two converging pointers.
    """
    if not heights:
        return 0

    left = 0
    right = len(heights) - 1
    left_max = heights[left]
    right_max = heights[right]
    total_water = 0

    while left < right:
        # The water level at the smaller boundary is bottlenecked ONLY by its own side's max!
        if left_max <= right_max:
            left += 1
            left_max = max(left_max, heights[left])
            total_water += left_max - heights[left]
        else:
            right -= 1
            right_max = max(right_max, heights[right])
            total_water += right_max - heights[right]

    return total_water


def sorted_squares_two_pointers(nums: list[int]) -> list[int]:
    """
    Given an integer array `nums` sorted in non-decreasing order (which may contain negatives),
    return an array of the squares of each number sorted in non-decreasing order in O(N) time!
    """
    n = len(nums)
    result = [0] * n
    left = 0
    right = n - 1

    # Fill `result` from the largest square (index n - 1) down to 0
    for write_idx in range(n - 1, -1, -1):
        if abs(nums[left]) >= abs(nums[right]):
            result[write_idx] = nums[left] * nums[left]
            left += 1
        else:
            result[write_idx] = nums[right] * nums[right]
            right -= 1

    return result


if __name__ == "__main__":
    print("=" * 72)
    print("1. TRAPPING RAIN WATER IN O(N) TIME AND O(1) AUXILIARY SPACE")
    print("=" * 72)
    elevation = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    print(f"Elevation Map : {elevation}")
    print(f"Trapped Water : {trap_rain_water_two_pointers(elevation)} units")

    print("\n" + "=" * 72)
    print("2. SQUARES OF A SORTED ARRAY WITH NEGATIVES IN O(N) TIME")
    print("=" * 72)
    signed_nums = [-7, -3, -1, 2, 4, 5, 11]
    print(f"Sorted Input  : {signed_nums}")
    print(f"Sorted Squares: {sorted_squares_two_pointers(signed_nums)}")
