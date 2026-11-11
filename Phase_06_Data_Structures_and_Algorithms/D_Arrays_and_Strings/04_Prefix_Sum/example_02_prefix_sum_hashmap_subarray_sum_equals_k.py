"""
Phase 6 - Data Structures and Algorithms
Section D: Arrays and Strings - Topic 04: Prefix Sum
Example 02: Prefix Sum + Hash Map Pattern (Subarray Sum Equals K & Divisible by K)

Demonstrates:
1. Why Sliding Window FAILS on subarray sum problems when the array contains NEGATIVE numbers
   (expanding `right` can decrease the sum, and shrinking `left` can increase the sum!).
2. How `Prefix Sum + Hash Map` solves Subarray Sum Equals K (LeetCode 560) in O(N) time
   even with negative integers:
   `sum(arr[i .. j]) == k  <==>  prefix_sum[j] - prefix_sum[i - 1] == k  <==>  prefix_sum[i - 1] == current_sum - k`.
3. Longest Subarray with Sum == K using a `{first_seen_prefix_sum: index}` map.
"""


def count_subarrays_with_sum_k(nums: list[int], k: int) -> int:
    """
    Count total contiguous subarrays whose elements sum to `k` (LeetCode 560).
    Works with positive, zero, AND negative integers in O(N) time and O(N) space!
    """
    # Seed with {0: 1} to handle subarrays starting at index 0 whose prefix sum equals k!
    prefix_counts: dict[int, int] = {0: 1}
    current_sum = 0
    total_subarrays = 0

    for num in nums:
        current_sum += num
        needed_prior_prefix = current_sum - k
        if needed_prior_prefix in prefix_counts:
            total_subarrays += prefix_counts[needed_prior_prefix]

        prefix_counts[current_sum] = prefix_counts.get(current_sum, 0) + 1

    return total_subarrays


def longest_subarray_with_sum_k(
    nums: list[int], k: int
) -> tuple[int, list[int]]:
    """
    Find the longest contiguous subarray summing to `k` (with negative numbers allowed).
    Stores only the EARLIEST index where each prefix sum occurred to maximize `j - i`!
    """
    first_seen_idx: dict[int, int] = {0: -1}
    current_sum = 0
    max_len = 0
    best_slice = (0, 0)

    for idx, num in enumerate(nums):
        current_sum += num
        needed = current_sum - k
        if needed in first_seen_idx:
            length = idx - first_seen_idx[needed]
            if length > max_len:
                max_len = length
                best_slice = (first_seen_idx[needed] + 1, idx + 1)

        # Only record the FIRST time we see `current_sum` so `(idx - first_seen)` is maximized!
        if current_sum not in first_seen_idx:
            first_seen_idx[current_sum] = idx

    return max_len, nums[best_slice[0] : best_slice[1]]


if __name__ == "__main__":
    print("=" * 72)
    print("1. SUBARRAY SUM EQUALS K WITH NEGATIVE NUMBERS (LEETCODE 560)")
    print("=" * 72)
    arr_neg = [3, 4, -7, 1, 3, 3, 1, -4]
    count_7 = count_subarrays_with_sum_k(arr_neg, k=7)
    print(f"Input Array (with negatives): {arr_neg}")
    print(f"Total Subarrays Summing to 7: {count_7}")
    print("  Matching Subarrays: [3, 4], [3, 4, -7, 1, 3, 3], [1, 3, 3], [3, 3, 1]")

    print("\n" + "=" * 72)
    print("2. LONGEST SUBARRAY WITH SUM == K (FIRST-SEEN PREFIX INDEX MAP)")
    print("=" * 72)
    length, sub = longest_subarray_with_sum_k(arr_neg, k=7)
    print(f"Longest Subarray Summing to 7: {sub} (Length = {length})")
