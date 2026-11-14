"""
Phase 6 - Section G.05: Hashing Problems
Example 01: 4Sum II and Minimum Window Substring

Demonstrating:
1. 4Sum II (Meet in the Middle) reducing O(n^4) brute force to O(n^2) using a Hash Map.
2. Minimum Window Substring using frequency hash maps with sliding window.
"""

from collections import Counter, defaultdict


def four_sum_count(nums1, nums2, nums3, nums4):
    """
    Count tuples (i, j, k, l) such that nums1[i] + nums2[j] + nums3[k] + nums4[l] == 0.
    Time Complexity: O(n^2)
    Space Complexity: O(n^2)
    """
    sum_ab = defaultdict(int)
    for a in nums1:
        for b in nums2:
            sum_ab[a + b] += 1

    count = 0
    for c in nums3:
        for d in nums4:
            target = -(c + d)
            if target in sum_ab:
                count += sum_ab[target]

    return count


def min_window_substring(s, t):
    """
    Find smallest window in s containing all characters of t (including multiplicity).
    Time Complexity: O(|s| + |t|)
    Space Complexity: O(|s| + |t|)
    """
    if not s or not t or len(s) < len(t):
        return ""

    target_counts = Counter(t)
    required = len(target_counts)

    window_counts = defaultdict(int)
    formed = 0
    left = 0

    best_len = float("inf")
    best_window = (0, 0)

    for right, char in enumerate(s):
        window_counts[char] += 1
        if char in target_counts and window_counts[char] == target_counts[char]:
            formed += 1

        while left <= right and formed == required:
            curr_len = right - left + 1
            if curr_len < best_len:
                best_len = curr_len
                best_window = (left, right)

            left_char = s[left]
            window_counts[left_char] -= 1
            if left_char in target_counts and window_counts[left_char] < target_counts[left_char]:
                formed -= 1
            left += 1

    start, end = best_window
    return s[start : end + 1] if best_len != float("inf") else ""


def main():
    print("=" * 60)
    print("1. 4Sum II (Meet in the Middle via Hash Map)")
    print("=" * 60)
    n1 = [1, 2]
    n2 = [-2, -1]
    n3 = [-1, 2]
    n4 = [0, 2]
    ans1 = four_sum_count(n1, n2, n3, n4)
    print("Arrays:")
    print("  nums1:", n1)
    print("  nums2:", n2)
    print("  nums3:", n3)
    print("  nums4:", n4)
    print("Number of 4-tuples summing to 0:", ans1)

    print("\n" + "=" * 60)
    print("2. Minimum Window Substring")
    print("=" * 60)
    s1, t1 = "ADOBECODEBANC", "ABC"
    win1 = min_window_substring(s1, t1)
    print(f"s = '{s1}', t = '{t1}' -> Min Window: '{win1}'")

    s2, t2 = "a", "aa"
    win2 = min_window_substring(s2, t2)
    print(f"s = '{s2}', t = '{t2}' -> Min Window: '{win2}'")


if __name__ == "__main__":
    main()
