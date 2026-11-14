"""
Phase 6 - Section G.03: Hash Sets
Example 02: Longest Substring Without Repeating Characters

Demonstrating:
1. Sliding window with HashSet tracking active unique characters.
2. Substring with at most K distinct characters.
"""


def length_of_longest_substring(s):
    """
    Find length of longest contiguous substring without repeating characters.
    Uses two pointers with a dynamic hash set.
    Time Complexity: O(n)
    Space Complexity: O(min(n, alphabet_size))
    """
    seen = set()
    left = 0
    max_len = 0
    best_start = 0

    for right in range(len(s)):
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
        seen.add(s[right])

        if right - left + 1 > max_len:
            max_len = right - left + 1
            best_start = left

    longest_sub = s[best_start : best_start + max_len] if max_len > 0 else ""
    return max_len, longest_sub


def longest_substring_k_distinct(s, k):
    """
    Length of longest substring with at most k distinct characters.
    Time Complexity: O(n)
    Space Complexity: O(k)
    """
    if k == 0 or not s:
        return 0, ""

    freq = {}
    left = 0
    max_len = 0
    best_start = 0

    for right in range(len(s)):
        ch = s[right]
        freq[ch] = freq.get(ch, 0) + 1

        while len(freq) > k:
            left_ch = s[left]
            freq[left_ch] -= 1
            if freq[left_ch] == 0:
                del freq[left_ch]
            left += 1

        if right - left + 1 > max_len:
            max_len = right - left + 1
            best_start = left

    return max_len, s[best_start : best_start + max_len]


def main():
    print("=" * 60)
    print("1. Longest Substring Without Repeating Characters")
    print("=" * 60)
    test_cases = ["abcabcbb", "bbbbb", "pwwkew", "", "dvdf"]
    for s in test_cases:
        length, substr = length_of_longest_substring(s)
        print(f"s = '{s}' -> Max Length: {length}, Substring: '{substr}'")

    print("\n" + "=" * 60)
    print("2. Longest Substring with At Most K Distinct Characters")
    print("=" * 60)
    k_tests = [("eceba", 2), ("aa", 1), ("abaccc", 2)]
    for s, k in k_tests:
        length, substr = longest_substring_k_distinct(s, k)
        print(f"s = '{s}', k = {k} -> Max Length: {length}, Substring: '{substr}'")


if __name__ == "__main__":
    main()
