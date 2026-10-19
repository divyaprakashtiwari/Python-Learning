"""
Topic: Data Structures and Algorithms (DSA) - Arrays and Two-Pointer Technique
-----------------------------------------------------------------------------
Questions Covered:
1. In-Place Array Reversal: Two converging pointers swapping opposite elements (O(n) time, O(1) space).
2. Two Sum in Sorted Array: Converging pointers locating target pair without auxiliary hash storage.
3. Remove Duplicates from Sorted Array: Fast-and-slow pointers deduplicating in-place.
4. Move Zeroes to End: Stable in-place compaction preserving relative order of non-zero elements.
5. Container With Most Water: Greedy two-pointer area maximization based on bottleneck height.
6. Valid Palindrome with Filtering: Two-pointer alphanumeric scanning with case-insensitivity.
7. Dutch National Flag (3-Way Partitioning): Three-pointer partitioning of 0s, 1s, and 2s in single pass.
8. Trapping Rain Water: Optimal two-pointer elevation scanning with left_max and right_max bounds.
9. 3Sum (Triplets Summing to Zero): Sorting combined with two-pointer search avoiding duplicate triplets.
10. Architectural System: Real-Time Interval Merging and Volatility Scanner Buffer using two-pointer mechanics.
"""

from typing import List, Tuple, Optional, Dict, Any


# ==============================================================================
# Question 1: In-Place Array Reversal
# ==============================================================================
def reverse_array_inplace(arr: List[Any]) -> None:
    """
    Reverses arr in-place using two converging pointers.
    Time Complexity: O(n), Space Complexity: O(1).
    """
    left = 0
    right = len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1


def test_q1_reverse_array_inplace():
    a1 = [1, 2, 3, 4, 5]
    reverse_array_inplace(a1)
    assert a1 == [5, 4, 3, 2, 1]

    a2 = ["a", "b", "c", "d"]
    reverse_array_inplace(a2)
    assert a2 == ["d", "c", "b", "a"]

    empty: List[int] = []
    reverse_array_inplace(empty)
    assert empty == []
    print("=== Q1: In-Place Array Reversal Verified ===")


# ==============================================================================
# Question 2: Two Sum in Sorted Array
# ==============================================================================
def two_sum_sorted(numbers: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
    Finds 0-indexed indices (i, j) such that numbers[i] + numbers[j] == target.
    Assumes array is sorted in non-decreasing order.
    Returns (i, j) if found, else None.
    """
    left = 0
    right = len(numbers) - 1

    while left < right:
        current_sum = numbers[left] + numbers[right]
        if current_sum == target:
            return (left, right)
        elif current_sum < target:
            left += 1
        else:
            right -= 1

    return None


def test_q2_two_sum_sorted():
    nums = [2, 7, 11, 15]
    assert two_sum_sorted(nums, 9) == (0, 1)
    assert two_sum_sorted(nums, 18) == (1, 2)
    assert two_sum_sorted(nums, 26) == (2, 3)
    assert two_sum_sorted(nums, 100) is None
    print("=== Q2: Two Sum in Sorted Array Verified ===")


# ==============================================================================
# Question 3: Remove Duplicates from Sorted Array In-Place
# ==============================================================================
def remove_duplicates_sorted(nums: List[int]) -> int:
    """
    Removes duplicates in-place such that each unique element appears once.
    Returns the count of unique elements (k).
    The first k elements of nums will contain unique elements in sorted order.
    """
    if not nums:
        return 0

    slow = 0  # Points to last unique element written
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]

    return slow + 1


def test_q3_remove_duplicates():
    arr = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    k = remove_duplicates_sorted(arr)
    assert k == 5
    assert arr[:k] == [0, 1, 2, 3, 4]

    single = [42]
    assert remove_duplicates_sorted(single) == 1
    assert single == [42]
    print("=== Q3: Remove Duplicates from Sorted Array Verified ===")


# ==============================================================================
# Question 4: Move Zeroes to End In-Place
# ==============================================================================
def move_zeroes_inplace(nums: List[int]) -> None:
    """
    Moves all 0's to the end of nums while maintaining relative order of non-zero elements.
    Operates strictly in-place with O(1) extra space.
    """
    write_idx = 0
    for read_idx in range(len(nums)):
        if nums[read_idx] != 0:
            if write_idx != read_idx:
                nums[write_idx], nums[read_idx] = nums[read_idx], nums[write_idx]
            write_idx += 1


def test_q4_move_zeroes():
    arr1 = [0, 1, 0, 3, 12]
    move_zeroes_inplace(arr1)
    assert arr1 == [1, 3, 12, 0, 0]

    arr2 = [0, 0, 0]
    move_zeroes_inplace(arr2)
    assert arr2 == [0, 0, 0]

    arr3 = [1, 2, 3]
    move_zeroes_inplace(arr3)
    assert arr3 == [1, 2, 3]
    print("=== Q4: Move Zeroes to End In-Place Verified ===")


# ==============================================================================
# Question 5: Container With Most Water
# ==============================================================================
def max_water_area(heights: List[int]) -> int:
    """
    Finds two lines that together with x-axis forms a container that stores the most water.
    Area = min(height[l], height[r]) * (r - l).
    Time Complexity: O(n), Space Complexity: O(1).
    """
    left = 0
    right = len(heights) - 1
    max_area = 0

    while left < right:
        width = right - left
        h = min(heights[left], heights[right])
        current_area = width * h
        if current_area > max_area:
            max_area = current_area

        # Move the pointer pointing to shorter vertical line inward
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1

    return max_area


def test_q5_max_water_area():
    heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    # Optimal between index 1 (height 8) and index 8 (height 7): min(8, 7) * (8 - 1) = 7 * 7 = 49
    assert max_water_area(heights) == 49

    assert max_water_area([1, 1]) == 1
    assert max_water_area([4, 3, 2, 1, 4]) == 16
    print("=== Q5: Container With Most Water Verified ===")


# ==============================================================================
# Question 6: Valid Palindrome with Alphanumeric Filtering
# ==============================================================================
def is_valid_palindrome(s: str) -> bool:
    """
    Checks if string is palindrome considering only alphanumeric characters and ignoring cases.
    Evaluated with two converging pointers in O(1) auxiliary space.
    """
    left = 0
    right = len(s) - 1

    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True


def test_q6_valid_palindrome():
    assert is_valid_palindrome("A man, a plan, a canal: Panama") is True
    assert is_valid_palindrome("race a car") is False
    assert is_valid_palindrome("Was it a car or a cat I saw?") is True
    assert is_valid_palindrome(" ") is True
    assert is_valid_palindrome("0P") is False
    print("=== Q6: Valid Palindrome with Alphanumeric Filtering Verified ===")


# ==============================================================================
# Question 7: Dutch National Flag Problem (Sort Colors 0, 1, 2)
# ==============================================================================
def sort_colors_inplace(nums: List[int]) -> None:
    """
    Sorts array containing only 0s, 1s, and 2s in-place in a single pass O(n)
    using 3 pointers (low, mid, high).
    """
    low = 0
    mid = 0
    high = len(nums) - 1

    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1


def test_q7_dutch_national_flag():
    colors = [2, 0, 2, 1, 1, 0]
    sort_colors_inplace(colors)
    assert colors == [0, 0, 1, 1, 2, 2]

    c2 = [2, 0, 1]
    sort_colors_inplace(c2)
    assert c2 == [0, 1, 2]

    c3 = [0]
    sort_colors_inplace(c3)
    assert c3 == [0]
    print("=== Q7: Dutch National Flag 3-Way Partitioning Verified ===")


# ==============================================================================
# Question 8: Trapping Rain Water
# ==============================================================================
def trap_rain_water(heights: List[int]) -> int:
    """
    Computes total units of rainwater trapped between elevation bars.
    Uses two pointers with running left_max and right_max bounds in O(n) time, O(1) space.
    """
    if not heights:
        return 0

    left = 0
    right = len(heights) - 1
    left_max = 0
    right_max = 0
    total_water = 0

    while left < right:
        if heights[left] < heights[right]:
            if heights[left] >= left_max:
                left_max = heights[left]
            else:
                total_water += left_max - heights[left]
            left += 1
        else:
            if heights[right] >= right_max:
                right_max = heights[right]
            else:
                total_water += right_max - heights[right]
            right -= 1

    return total_water


def test_q8_trap_rain_water():
    elevation = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    # Total trapped water = 6
    assert trap_rain_water(elevation) == 6

    elevation2 = [4, 2, 0, 3, 2, 5]
    # Total trapped water = 9
    assert trap_rain_water(elevation2) == 9

    assert trap_rain_water([1, 2, 3, 4]) == 0
    print("=== Q8: Trapping Rain Water (Two-Pointer Elevation) Verified ===")


# ==============================================================================
# Question 9: 3Sum (Unique Triplets Summing to Zero)
# ==============================================================================
def three_sum(nums: List[int]) -> List[Tuple[int, int, int]]:
    """
    Finds all unique triplets [nums[i], nums[j], nums[k]] such that
    i != j != k and nums[i] + nums[j] + nums[k] == 0.
    Avoids duplicate triplets by skipping duplicate values.
    Time Complexity: O(n^2), Space Complexity: O(1) auxiliary (excluding output).
    """
    nums.sort()
    triplets: List[Tuple[int, int, int]] = []
    n = len(nums)

    for i in range(n - 2):
        # Skip identical consecutive elements for the first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        target = -nums[i]
        left = i + 1
        right = n - 1

        while left < right:
            current_sum = nums[left] + nums[right]
            if current_sum == target:
                triplets.append((nums[i], nums[left], nums[right]))
                # Skip duplicates for left and right
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1

    return triplets


def test_q9_three_sum():
    nums = [-1, 0, 1, 2, -1, -4]
    res = three_sum(nums)
    # Expected triplets: (-1, -1, 2) and (-1, 0, 1)
    assert len(res) == 2
    assert (-1, -1, 2) in res
    assert (-1, 0, 1) in res

    assert three_sum([0, 1, 1]) == []
    assert three_sum([0, 0, 0]) == [(0, 0, 0)]
    print("=== Q9: 3Sum (Unique Triplets) Verified ===")


# ==============================================================================
# Question 10: Architectural System: Two-Pointer Interval Merger & Volatility Buffer
# ==============================================================================
class TwoPointerIntervalBuffer:
    """
    Production-grade temporal interval merger and price-pair volatility scanner.
    Implements two-pointer interval consolidation and sliding volatility spread detection.
    """
    @staticmethod
    def merge_overlapping_intervals(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Merges overlapping intervals in-place/sorted order using two-pointer consolidation.
        e.g. [(1, 3), (2, 6), (8, 10), (15, 18)] -> [(1, 6), (8, 10), (15, 18)].
        """
        if not intervals:
            return []

        sorted_intervals = sorted(intervals, key=lambda x: x[0])
        merged = [sorted_intervals[0]]

        for i in range(1, len(sorted_intervals)):
            current_start, current_end = sorted_intervals[i]
            last_start, last_end = merged[-1]

            if current_start <= last_end:
                # Overlap: extend previous interval end if needed
                merged[-1] = (last_start, max(last_end, current_end))
            else:
                merged.append((current_start, current_end))

        return merged

    @staticmethod
    def find_target_spread_pair(sorted_prices: List[float], target_spread: float, tolerance: float = 0.01) -> Optional[Tuple[float, float]]:
        """
        Two-pointer scanner on sorted prices to find two prices (p1, p2)
        such that p2 - p1 ~= target_spread within tolerance.
        """
        left = 0
        right = 1
        n = len(sorted_prices)

        while left < n and right < n:
            if left == right:
                right += 1
                continue

            diff = sorted_prices[right] - sorted_prices[left]
            if abs(diff - target_spread) <= tolerance:
                return (sorted_prices[left], sorted_prices[right])
            elif diff < target_spread:
                right += 1
            else:
                left += 1

        return None


def test_q10_interval_buffer_and_volatility():
    # 1. Interval consolidation
    raw_intervals = [(1, 3), (2, 6), (8, 10), (15, 18), (9, 12)]
    merged = TwoPointerIntervalBuffer.merge_overlapping_intervals(raw_intervals)
    assert merged == [(1, 6), (8, 12), (15, 18)]

    # 2. Volatility spread detection
    prices = [100.0, 102.5, 105.0, 112.5, 125.0]
    pair = TwoPointerIntervalBuffer.find_target_spread_pair(prices, target_spread=10.0, tolerance=0.1)
    assert pair == (102.5, 112.5)

    no_pair = TwoPointerIntervalBuffer.find_target_spread_pair(prices, target_spread=50.0)
    assert no_pair is None
    print("=== Q10: Architectural Two-Pointer Interval Merger & Volatility Buffer Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_reverse_array_inplace()
    test_q2_two_sum_sorted()
    test_q3_remove_duplicates()
    test_q4_move_zeroes()
    test_q5_max_water_area()
    test_q6_valid_palindrome()
    test_q7_dutch_national_flag()
    test_q8_trap_rain_water()
    test_q9_three_sum()
    test_q10_interval_buffer_and_volatility()
    print("\nAll 10 arrays and two-pointer DSA questions passed successfully!")
