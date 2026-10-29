"""
Question 3: Binary Search Algorithmic Toolkit
Topic: Data Structures & Algorithms (DSA)

Key Concepts Tested:
- Standard iterative binary search in O(log N) time and O(1) auxiliary space
- Bisect search insert position (lower bound)
- First and last occurrence range search with boundary bias
- Rotated sorted array search identifying monotonic halves
- Comprehensive edge cases (empty lists, missing elements, duplicates)
"""

from typing import List, Tuple


class BinarySearchSuite:
    """
    Algorithmic toolkit implementing essential logarithmic search patterns.
    """

    @staticmethod
    def search_exact(nums: List[int], target: int) -> int:
        """
        Classic iterative binary search.
        Returns 0-indexed position if found, or -1 if absent.
        """
        low = 0
        high = len(nums) - 1

        while low <= high:
            mid = low + (high - low) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                low = mid + 1
            else:
                high = mid - 1

        return -1

    @staticmethod
    def search_insert_position(nums: List[int], target: int) -> int:
        """
        Finds target index or the insertion index preserving sorted order.
        Equivalent to bisect_left.
        """
        low = 0
        high = len(nums) - 1

        while low <= high:
            mid = low + (high - low) // 2
            if nums[mid] >= target:
                high = mid - 1
            else:
                low = mid + 1

        return low

    @staticmethod
    def find_occurrence_range(nums: List[int], target: int) -> Tuple[int, int]:
        """
        Finds the first and last occurrence indices of target in a sorted list with duplicates.
        Returns (first_idx, last_idx) or (-1, -1) if target is absent.
        """
        if not nums:
            return (-1, -1)

        # 1. Leftmost occurrence search
        first_idx = -1
        low, high = 0, len(nums) - 1
        while low <= high:
            mid = low + (high - low) // 2
            if nums[mid] == target:
                first_idx = mid
                high = mid - 1  # Bias search to the left
            elif nums[mid] < target:
                low = mid + 1
            else:
                high = mid - 1

        if first_idx == -1:
            return (-1, -1)

        # 2. Rightmost occurrence search
        last_idx = -1
        low, high = 0, len(nums) - 1
        while low <= high:
            mid = low + (high - low) // 2
            if nums[mid] == target:
                last_idx = mid
                low = mid + 1  # Bias search to the right
            elif nums[mid] < target:
                low = mid + 1
            else:
                high = mid - 1

        return (first_idx, last_idx)

    @staticmethod
    def search_rotated(nums: List[int], target: int) -> int:
        """
        Searches for target in an array rotated at an unknown pivot.
        Operates in strict O(log N) time.
        """
        low = 0
        high = len(nums) - 1

        while low <= high:
            mid = low + (high - low) // 2

            if nums[mid] == target:
                return mid

            # Determine which half is monotonically sorted
            if nums[low] <= nums[mid]:
                # Left half [low..mid] is sorted
                if nums[low] <= target < nums[mid]:
                    high = mid - 1
                else:
                    low = mid + 1
            else:
                # Right half [mid..high] is sorted
                if nums[mid] < target <= nums[high]:
                    low = mid + 1
                else:
                    high = mid - 1

        return -1


if __name__ == "__main__":
    suite = BinarySearchSuite()

    print("=== 1. Exact Match Search ===")
    arr1 = [10, 20, 30, 40, 50]
    idx1 = suite.search_exact(arr1, target=30)
    idx_missing = suite.search_exact(arr1, target=25)
    print(f"Exact Match Index (30): {idx1}")
    print(f"Exact Match Missing (25): {idx_missing}")

    print("\n=== 2. Search Insert Position ===")
    arr2 = [1, 3, 5, 6]
    insert_pos = suite.search_insert_position(arr2, target=4)
    print(f"Insert Position for 4 in {arr2}: {insert_pos} (Inserts between 3 and 5)")

    print("\n=== 3. First and Last Occurrence Range ===")
    arr3 = [5, 7, 7, 8, 8, 8, 10]
    range_res = suite.find_occurrence_range(arr3, target=8)
    print(f"Occurrence Range for 8 in {arr3}: {range_res}")

    print("\n=== 4. Rotated Sorted Array Search ===")
    rotated_arr = [4, 5, 6, 7, 0, 1, 2]
    rotated_idx = suite.search_rotated(rotated_arr, target=0)
    print(f"Rotated Search for 0 in {rotated_arr}: {rotated_idx}")

    print("\n=== 5. Empty List & Edge Cases ===")
    print(f"Empty list exact search: {suite.search_exact([], target=10)}")
    print(f"Empty list insert position: {suite.search_insert_position([], target=10)}")
    print(f"Empty list occurrence range: {suite.find_occurrence_range([], target=10)}")
    print(f"Empty list rotated search: {suite.search_rotated([], target=10)}")
