"""
Question 1: Two-Pointer Array Manipulation Algorithms
Topic: Data Structures & Algorithms (DSA)

Key Concepts Tested:
- Converging two-pointer technique for sorted search in O(N) time and O(1) space
- Fast/slow two-pointer pattern for in-place deduplication
- Bidirectional swapping for in-place subarray reversal
- Boundary and edge case handling (empty lists, single elements)
"""

from typing import List, Tuple, Optional


class TwoPointerAlgorithms:
    """
    Classical two-pointer algorithms operating in optimal O(N) time and O(1) auxiliary space.
    """

    @staticmethod
    def two_sum_sorted(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
        """
        Finds two indices in a pre-sorted list whose values sum to target.
        Runs in O(N) time and strictly O(1) auxiliary space.
        """
        left = 0
        right = len(nums) - 1

        while left < right:
            current_sum = nums[left] + nums[right]
            if current_sum == target:
                return (left, right)
            elif current_sum < target:
                left += 1
            else:
                right -= 1

        return None

    @staticmethod
    def remove_duplicates_sorted(nums: List[int]) -> int:
        """
        Removes duplicates from a sorted list in-place using fast/slow pointers.
        Returns k, the count of unique elements, such that nums[:k] contains the result.
        """
        if len(nums) <= 1:
            return len(nums)

        write_idx = 1
        for read_idx in range(1, len(nums)):
            if nums[read_idx] != nums[read_idx - 1]:
                nums[write_idx] = nums[read_idx]
                write_idx += 1

        return write_idx

    @staticmethod
    def reverse_subarray(nums: List[int], start_idx: int, end_idx: int) -> None:
        """
        Reverses the slice nums[start_idx : end_idx + 1] in-place.
        """
        if not (0 <= start_idx <= end_idx < len(nums)):
            raise ValueError(f"Invalid subarray indices: [{start_idx}, {end_idx}] for length {len(nums)}")

        left = start_idx
        right = end_idx
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1


if __name__ == "__main__":
    algo = TwoPointerAlgorithms()

    print("=== 1. Two-Sum Sorted Search ===")
    sorted_arr = [2, 7, 11, 15, 18, 22]
    pair = algo.two_sum_sorted(sorted_arr, target=26)
    if pair:
        i, j = pair
        print(f"Two-Sum Target 26 Found: indices ({i}, {j}) -> values ({sorted_arr[i]} + {sorted_arr[j]} = {sorted_arr[i] + sorted_arr[j]})")
    else:
        print("No matching pair found.")

    print("\n=== 2. In-Place Deduplication ===")
    dups_arr = [1, 1, 2, 2, 3, 4, 4, 4, 5]
    k = algo.remove_duplicates_sorted(dups_arr)
    print("Deduplication Result:")
    print(f"- Unique Count k = {k}")
    print(f"- Deduplicated Prefix: {dups_arr[:k]}")

    print("\n=== 3. Subarray In-Place Reversal ===")
    arr_to_rev = [10, 20, 30, 40, 50, 60]
    algo.reverse_subarray(arr_to_rev, 1, 4)
    print(f"Subarray Reversed (indices 1 to 4):\n{arr_to_rev}")

    print("\n=== 4. Edge Cases ===")
    empty_list: List[int] = []
    print(f"Empty list deduplication k: {algo.remove_duplicates_sorted(empty_list)}")
    single_list = [42]
    print(f"Single element deduplication k: {algo.remove_duplicates_sorted(single_list)}")
    print(f"No match two-sum: {algo.two_sum_sorted([1, 2, 3], target=100)}")
