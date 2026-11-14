"""
Phase 6 - Section G.04: Frequency Counting
Example 03: First Unique Character and Majority Element

Demonstrating:
1. First Unique Character in a String using two-pass frequency count.
2. Majority Element (> n // 2) using Hash Map frequency table.
3. Majority Element using Boyer-Moore Voting Algorithm O(1) space optimization.
"""

from collections import Counter


def first_unique_char(s):
    """
    Find index of first non-repeating character in s.
    Returns -1 if all characters repeat.
    Time Complexity: O(n)
    Space Complexity: O(1) (at most 26 lowercase characters)
    """
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1


def majority_element_hashmap(nums):
    """
    Find element that appears more than floor(n / 2) times.
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    threshold = len(nums) // 2
    counts = Counter(nums)
    for num, count in counts.items():
        if count > threshold:
            return num
    return None


def majority_element_boyer_moore(nums):
    """
    Boyer-Moore Voting Algorithm.
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    candidate = None
    count = 0

    for num in nums:
        if count == 0:
            candidate = num
        count += (1 if num == candidate else -1)

    return candidate


def main():
    print("=" * 60)
    print("1. First Unique Character in String")
    print("=" * 60)
    strings = ["leetcode", "loveleetcode", "aabb"]
    for s in strings:
        idx = first_unique_char(s)
        char = s[idx] if idx != -1 else "None"
        print(f"s = '{s}' -> First Unique Index: {idx} (Character: '{char}')")

    print("\n" + "=" * 60)
    print("2. Majority Element: Hash Map vs Boyer-Moore")
    print("=" * 60)
    test_arrays = [
        [3, 2, 3],
        [2, 2, 1, 1, 1, 2, 2],
        [1, 1, 1, 3, 3, 2, 2, 2, 2, 2],
    ]
    for arr in test_arrays:
        maj_hash = majority_element_hashmap(arr)
        maj_bm = majority_element_boyer_moore(arr)
        print(f"nums = {arr}")
        print(f"  Hash Map Result     : {maj_hash}")
        print(f"  Boyer-Moore Result  : {maj_bm}")


if __name__ == "__main__":
    main()
