"""
Phase 6 - Data Structures and Algorithms
Section D: Arrays and Strings - Topic 03: Sliding Window
Example 03: Frequency-Map Sliding Window (Find All Anagrams & Minimum Window Substring)

Demonstrates:
1. Finding All Start Indices of Anagrams of Pattern `p` in String `s` (LeetCode 438)
   in O(|s| + |p|) linear time using a fixed-size sliding frequency window.
2. Minimum Window Substring (LeetCode 76 Hard): finding the shortest substring of `s`
   that contains every character of `t` (including multiplicity) in O(|s| + |t|) time!
"""

from collections import Counter


def find_all_anagram_indices(s: str, p: str) -> list[int]:
    """
    Return all start indices of `p`'s anagrams in `s` in O(len(s)) time.
    """
    n, k = len(s), len(p)
    if k > n:
        return []

    p_count = Counter(p)
    window_count = Counter(s[:k])
    indices: list[int] = []

    if window_count == p_count:
        indices.append(0)

    for right in range(k, n):
        enter_ch = s[right]
        leave_ch = s[right - k]

        window_count[enter_ch] += 1
        window_count[leave_ch] -= 1
        if window_count[leave_ch] == 0:
            del window_count[leave_ch]

        if window_count == p_count:
            indices.append(right - k + 1)

    return indices


def min_window_substring(s: str, t: str) -> str:
    """
    Return the minimum window substring of `s` such that every character in `t`
    (including duplicates) is included in the window (LeetCode 76).
    Time Complexity: O(|s| + |t|)
    """
    if not s or not t or len(t) > len(s):
        return ""

    need = Counter(t)
    required_unique = len(need)
    window: dict[str, int] = {}
    formed_unique = 0

    left = 0
    best_len = len(s) + 1
    best_slice = (0, 0)

    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if ch in need and window[ch] == need[ch]:
            formed_unique += 1

        # Contract from the left while all required characters are satisfied
        while formed_unique == required_unique:
            curr_len = right - left + 1
            if curr_len < best_len:
                best_len = curr_len
                best_slice = (left, right + 1)

            leave_ch = s[left]
            window[leave_ch] -= 1
            if leave_ch in need and window[leave_ch] < need[leave_ch]:
                formed_unique -= 1
            left += 1

    return "" if best_len > len(s) else s[best_slice[0] : best_slice[1]]


if __name__ == "__main__":
    print("=" * 72)
    print("1. FIND ALL ANAGRAMS IN A STRING (FIXED FREQUENCY WINDOW)")
    print("=" * 72)
    text, pattern = "cbaebabacd", "abc"
    starts = find_all_anagram_indices(text, pattern)
    print(f"String: '{text}', Pattern: '{pattern}'")
    print(f"Anagram Start Indices: {starts} -> {[text[i:i+len(pattern)] for i in starts]}")

    print("\n" + "=" * 72)
    print("2. MINIMUM WINDOW SUBSTRING (LEETCODE 76 HARD)")
    print("=" * 72)
    s_in, t_in = "ADOBECODEBANC", "ABC"
    print(f"Source s = '{s_in}', Target t = '{t_in}'")
    print(f"Minimum Window Substring: '{min_window_substring(s_in, t_in)}'")
