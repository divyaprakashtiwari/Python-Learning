"""
Topic 10: String Manipulation
Example 03: String Interview Classics — O(n) Anagram Check & Longest Unique Substring

Demonstrates:
1. Checking if two strings are anagrams in `O(n)` time using a 26-letter frequency array.
2. Finding the length and value of the longest substring without repeating characters
   using a variable-size Sliding Window (`O(n)` time).
"""


def are_anagrams_ascii(s: str, t: str) -> bool:
    """Check if two lowercase English strings are anagrams in O(n) time and O(1) space."""
    if len(s) != len(t):
        return False
    counts = [0] * 26
    base = ord("a")
    for ch_s, ch_t in zip(s, t):
        counts[ord(ch_s) - base] += 1
        counts[ord(ch_t) - base] -= 1
    return all(c == 0 for c in counts)


def longest_unique_substring(s: str) -> tuple[int, str]:
    """Return (max_length, substring) of the longest substring with all unique chars."""
    last_seen: dict[str, int] = {}
    left = 0
    best_len = 0
    best_start = 0

    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        window_len = right - left + 1
        if window_len > best_len:
            best_len = window_len
            best_start = left

    return (best_len, s[best_start : best_start + best_len])


def main() -> None:
    print("=== 1. O(n) Anagram Check (26-Bucket Frequency Array) ===")
    for s1, s2 in [("listen", "silent"), ("rat", "car"), ("anagram", "nagaram")]:
        print(f"  are_anagrams({s1!r}, {s2!r}) -> {are_anagrams_ascii(s1, s2)}")

    print("\n=== 2. Longest Substring Without Repeating Characters ===")
    for sample in ["abcabcbb", "pwwkew", "dvdf"]:
        length, sub = longest_unique_substring(sample)
        print(f"  Input: {sample!r:<10} -> Max Length: {length} (Substring: {sub!r})")


if __name__ == "__main__":
    main()
