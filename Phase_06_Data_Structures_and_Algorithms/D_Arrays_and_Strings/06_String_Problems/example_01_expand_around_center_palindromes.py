"""
Phase 6 - Data Structures and Algorithms
Section D: Arrays and Strings - Topic 06: String Problems
Example 01: Expand-Around-Center Palindromes (Longest Palindromic Substring & Count of Palindromes)

Demonstrates:
1. Why Brute-Force Longest Palindromic Substring takes O(N^3) time (O(N^2) substrings * O(N) check),
   whereas Expand-Around-Center solves it in O(N^2) time and strictly O(1) auxiliary space!
2. Handling both ODD-length palindromes (centered at `(i, i)`, e.g., `"racecar"`) and
   EVEN-length palindromes (centered between `(i, i + 1)`, e.g., `"abba"`): `2N - 1` centers total!
3. Counting ALL Palindromic Substrings (LeetCode 647) in O(N^2) time and O(1) space.
"""


def expand_around_center(s: str, left: int, right: int) -> tuple[int, int, int]:
    """
    Expand outward from `(left, right)` as long as `s[left] == s[right]`.
    Returns `(start_idx, end_idx_exclusive, palindromes_counted_on_this_center)`.
    """
    n = len(s)
    count = 0
    while left >= 0 and right < n and s[left] == s[right]:
        count += 1
        left -= 1
        right += 1

    # After the loop breaks, the valid palindrome was [left + 1 .. right - 1]
    return left + 1, right, count


def longest_palindromic_substring_and_total_count(s: str) -> tuple[str, int]:
    """
    Return `(longest_palindromic_substring, total_palindromic_substrings)` in O(N^2) time
    and O(1) auxiliary space by expanding around all `2N - 1` centers.
    """
    if not s:
        return "", 0

    best_start = 0
    best_end = 1
    total_palindromes = 0

    for i in range(len(s)):
        # 1. Odd-length palindromes centered at character `i`
        s1, e1, c1 = expand_around_center(s, i, i)
        total_palindromes += c1
        if (e1 - s1) > (best_end - best_start):
            best_start, best_end = s1, e1

        # 2. Even-length palindromes centered between `i` and `i + 1`
        s2, e2, c2 = expand_around_center(s, i, i + 1)
        total_palindromes += c2
        if (e2 - s2) > (best_end - best_start):
            best_start, best_end = s2, e2

    return s[best_start:best_end], total_palindromes


if __name__ == "__main__":
    print("=" * 72)
    print("1. EXPAND-AROUND-CENTER: LONGEST PALINDROME & TOTAL COUNT")
    print("=" * 72)

    for sample in ["babad", "cbbd", "racecar", "aaa", "abacdfgdcaba"]:
        longest_pal, total_cnt = longest_palindromic_substring_and_total_count(sample)
        print(
            f"  String: '{sample:<14}' -> Longest Palindrome: '{longest_pal:<7}' | "
            f"Total Palindromic Substrings: {total_cnt}"
        )
