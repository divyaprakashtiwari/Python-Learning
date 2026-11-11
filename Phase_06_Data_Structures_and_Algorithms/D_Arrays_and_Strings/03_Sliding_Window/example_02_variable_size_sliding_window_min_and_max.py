"""
Phase 6 - Data Structures and Algorithms
Section D: Arrays and Strings - Topic 03: Sliding Window
Example 02: Dynamic (Variable-Size) Sliding Window (Smallest Subarray >= Target & Longest Unique Substring)

Demonstrates:
1. Shrinking Window Pattern (Minimum Size Subarray Sum >= Target, LeetCode 209):
   Expand `right`, and `while window_sum >= target`, record minimum length and shrink `left += 1`.
2. Expanding Window Pattern (Longest Substring Without Repeating Characters, LeetCode 3):
   Maintain last-seen index of each character so `left` jumps directly past duplicates in O(N) time!
3. Why Variable Sliding Window is strictly O(N) time even though it has a `while` loop inside
   a `for` loop: `left` and `right` each move forward at most N times (`<= 2N` pointer steps total!).
"""


def min_subarray_len_at_least_target(
    nums: list[int], target: int
) -> tuple[int, list[int]]:
    """
    Find the minimal length of a contiguous subarray of positive integers whose sum >= target.
    Returns (min_length, subarray). Returns (0, []) if no such subarray exists.
    Time Complexity : O(N) (each element added once and subtracted at most once!)
    Space Complexity: O(1)
    """
    n = len(nums)
    left = 0
    window_sum = 0
    min_len = n + 1
    best_range = (0, 0)

    for right in range(n):
        window_sum += nums[right]

        # While window satisfies condition, record answer and shrink from left!
        while window_sum >= target:
            curr_len = right - left + 1
            if curr_len < min_len:
                min_len = curr_len
                best_range = (left, right + 1)
            window_sum -= nums[left]
            left += 1

    if min_len > n:
        return 0, []
    return min_len, nums[best_range[0] : best_range[1]]


def longest_unique_substring(s: str) -> tuple[int, str]:
    """
    Find the longest substring of `s` containing no duplicate characters (LeetCode 3)
    in O(N) time using a sliding window `[left .. right]` and `last_seen` index map.
    """
    last_seen: dict[str, int] = {}
    left = 0
    best_len = 0
    best_start = 0

    for right, ch in enumerate(s):
        # If `ch` was seen inside the current active window [left .. right - 1], jump `left`!
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1

        last_seen[ch] = right
        curr_len = right - left + 1
        if curr_len > best_len:
            best_len = curr_len
            best_start = left

    return best_len, s[best_start : best_start + best_len]


if __name__ == "__main__":
    print("=" * 72)
    print("1. MINIMUM SIZE SUBARRAY SUM >= TARGET (SHRINKING WINDOW)")
    print("=" * 72)
    arr = [2, 3, 1, 2, 4, 3]
    length, sub = min_subarray_len_at_least_target(arr, target=7)
    print(f"Input Array : {arr}, Target >= 7")
    print(f"Shortest Subarray : {sub} (Length = {length})")

    print("\n" + "=" * 72)
    print("2. LONGEST SUBSTRING WITHOUT REPEATING CHARACTERS (LC 3)")
    print("=" * 72)
    for sample_str in ["abcabcbb", "bbbbb", "pwwkew", "antigravity_python"]:
        L, substr = longest_unique_substring(sample_str)
        print(f"  '{sample_str:<18}' -> Max Length: {L:>2} | Substring: '{substr}'")
