"""
Topic: Problem Solving - Palindrome Checker
-------------------------------------------
Questions Covered:
1. Core String Palindrome: Two-pointer comparison vs slicing with case sensitivity options.
2. Sentence-Level Alphanumeric Palindrome: Sanitizing whitespace and non-alphanumeric punctuation.
3. Integer Palindrome (Zero String Conversion): Mathematical digit extraction using modulo and division.
4. Almost-Palindrome (Single Character Deletion): Verifying if palindrome can be formed deleting <= 1 character.
5. Longest Palindromic Substring: Expand-around-center algorithm in O(n^2) time and O(1) space.
6. Longest Palindromic Subsequence: 2D dynamic programming grid evaluating non-contiguous subsequences.
7. Palindrome Partitioning: Backtracking search generating all valid palindromic segmentations.
8. Shortest Palindrome via Prepending: KMP prefix / rolling symmetry prepending minimum characters.
9. Palindrome Permutation Check: Bitmask / odd-frequency validation for anagram palindromes.
10. Architectural System: Genomic Reverse-Complement Palindrome & Hairpin Loop Scanner.
"""

from typing import List, Tuple, Optional, Any, Dict, Set


# ==============================================================================
# Question 1: Core String Palindrome (Two-Pointer vs Slicing)
# ==============================================================================
def is_plain_palindrome(s: str, case_sensitive: bool = False) -> bool:
    """Checks if exact string is a palindrome using two pointers in O(1) space."""
    target = s if case_sensitive else s.lower()
    left = 0
    right = len(target) - 1
    while left < right:
        if target[left] != target[right]:
            return False
        left += 1
        right -= 1
    return True


def test_q1_plain_palindrome():
    assert is_plain_palindrome("racecar") is True
    assert is_plain_palindrome("Racecar", case_sensitive=False) is True
    assert is_plain_palindrome("Racecar", case_sensitive=True) is False
    assert is_plain_palindrome("hello") is False
    assert is_plain_palindrome("") is True
    print("=== Q1: Core String Palindrome Verified ===")


# ==============================================================================
# Question 2: Sentence-Level Alphanumeric Palindrome
# ==============================================================================
def is_sentence_palindrome(sentence: str) -> bool:
    """
    Checks if sentence is palindrome considering only alphanumeric characters and ignoring case.
    Time Complexity: O(n), Space Complexity: O(1).
    """
    left = 0
    right = len(sentence) - 1

    while left < right:
        while left < right and not sentence[left].isalnum():
            left += 1
        while left < right and not sentence[right].isalnum():
            right -= 1

        if sentence[left].lower() != sentence[right].lower():
            return False

        left += 1
        right -= 1

    return True


def test_q2_sentence_palindrome():
    assert is_sentence_palindrome("A man, a plan, a canal: Panama!") is True
    assert is_sentence_palindrome("Was it a car or a cat I saw?") is True
    assert is_sentence_palindrome("No 'x' in Nixon") is True
    assert is_sentence_palindrome("Not a palindrome") is False
    print("=== Q2: Sentence-Level Alphanumeric Palindrome Verified ===")


# ==============================================================================
# Question 3: Integer Palindrome (Zero String Conversion)
# ==============================================================================
def is_integer_palindrome(x: int) -> bool:
    """
    Checks if integer is a palindrome without converting to string.
    Negative numbers are not palindromes.
    Reverses second half of number to prevent integer overflow.
    """
    # Negative numbers or numbers ending in 0 (except 0 itself) cannot be palindromes
    if x < 0 or (x % 10 == 0 and x != 0):
        return False

    reverted_half = 0
    while x > reverted_half:
        reverted_half = reverted_half * 10 + (x % 10)
        x //= 10

    # For even digits: x == reverted_half
    # For odd digits: x == reverted_half // 10 (discard middle digit)
    return x == reverted_half or x == (reverted_half // 10)


def test_q3_integer_palindrome():
    assert is_integer_palindrome(121) is True
    assert is_integer_palindrome(1221) is True
    assert is_integer_palindrome(0) is True
    assert is_integer_palindrome(-121) is False
    assert is_integer_palindrome(10) is False
    assert is_integer_palindrome(123454321) is True
    print("=== Q3: Integer Palindrome (Zero String Conversion) Verified ===")


# ==============================================================================
# Question 4: Almost-Palindrome (At Most One Deletion)
# ==============================================================================
def is_almost_palindrome(s: str) -> bool:
    """
    Returns True if s can be a palindrome after deleting at most one character.
    """
    def check_sub_palindrome(left: int, right: int) -> bool:
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    left = 0
    right = len(s) - 1

    while left < right:
        if s[left] != s[right]:
            # Try deleting s[left] or deleting s[right]
            return check_sub_palindrome(left + 1, right) or check_sub_palindrome(left, right - 1)
        left += 1
        right -= 1

    return True


def test_q4_almost_palindrome():
    assert is_almost_palindrome("aba") is True
    assert is_almost_palindrome("abca") is True  # delete 'b' or 'c'
    assert is_almost_palindrome("abc") is False
    assert is_almost_palindrome("deeee") is True
    print("=== Q4: Almost-Palindrome (Single Character Deletion) Verified ===")


# ==============================================================================
# Question 5: Longest Palindromic Substring
# ==============================================================================
def longest_palindromic_substring(s: str) -> str:
    """
    Finds the longest contiguous palindromic substring using expand-around-center.
    Time Complexity: O(n^2), Space Complexity: O(1).
    """
    if not s:
        return ""

    start = 0
    end = 0

    def expand_around_center(left: int, right: int) -> int:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1

    for i in range(len(s)):
        len1 = expand_around_center(i, i)      # Odd length
        len2 = expand_around_center(i, i + 1)  # Even length
        max_len = max(len1, len2)
        if max_len > end - start + 1:
            start = i - (max_len - 1) // 2
            end = i + max_len // 2

    return s[start : end + 1]


def test_q5_longest_palindromic_substring():
    res1 = longest_palindromic_substring("babad")
    assert res1 in ("bab", "aba")

    res2 = longest_palindromic_substring("cbbd")
    assert res2 == "bb"

    assert longest_palindromic_substring("a") == "a"
    assert longest_palindromic_substring("racecar") == "racecar"
    print("=== Q5: Longest Palindromic Substring Verified ===")


# ==============================================================================
# Question 6: Longest Palindromic Subsequence (LPS) via 2D DP
# ==============================================================================
def longest_palindromic_subsequence(s: str) -> int:
    """
    Calculates the length of the longest palindromic subsequence (non-contiguous allowed).
    Uses 2D dynamic programming grid.
    Time: O(n^2), Space: O(n^2).
    """
    n = len(s)
    if n == 0:
        return 0

    # dp[i][j]: length of LPS in s[i..j]
    dp = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = 1

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2 if length > 2 else 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    return dp[0][n - 1]


def test_q6_longest_palindromic_subsequence():
    # "bbbab" -> LPS is "bbbb" (length 4)
    assert longest_palindromic_subsequence("bbbab") == 4
    # "cbbd" -> LPS is "bb" (length 2)
    assert longest_palindromic_subsequence("cbbd") == 2
    assert longest_palindromic_subsequence("a") == 1
    print("=== Q6: Longest Palindromic Subsequence Verified ===")


# ==============================================================================
# Question 7: Palindrome Partitioning (Backtracking)
# ==============================================================================
def partition_palindromes(s: str) -> List[List[str]]:
    """
    Finds all possible partitions of s such that every substring of the partition is a palindrome.
    Uses backtracking with palindrome pre-validation.
    """
    result: List[List[str]] = []

    def is_pal(sub: str) -> bool:
        return sub == sub[::-1]

    def backtrack(start: int, current_path: List[str]):
        if start == len(s):
            result.append(list(current_path))
            return

        for end in range(start + 1, len(s) + 1):
            sub = s[start:end]
            if is_pal(sub):
                current_path.append(sub)
                backtrack(end, current_path)
                current_path.pop()

    backtrack(0, [])
    return result


def test_q7_palindrome_partitioning():
    parts = partition_palindromes("aab")
    expected = [["a", "a", "b"], ["aa", "b"]]
    assert parts == expected

    single = partition_palindromes("a")
    assert single == [["a"]]
    print("=== Q7: Palindrome Partitioning (Backtracking) Verified ===")


# ==============================================================================
# Question 8: Shortest Palindrome via Prepending Characters
# ==============================================================================
def shortest_palindrome_prepend(s: str) -> str:
    """
    Finds the shortest palindrome by prepending characters in front of s.
    Finds longest palindromic prefix of s, and prepends the reverse of the remaining suffix.
    """
    if not s:
        return ""

    # KMP-based pattern: s + '#' + reverse(s)
    rev_s = s[::-1]
    combined = s + "#" + rev_s
    n = len(combined)
    lps = [0] * n

    for i in range(1, n):
        j = lps[i - 1]
        while j > 0 and combined[i] != combined[j]:
            j = lps[j - 1]
        if combined[i] == combined[j]:
            j += 1
        lps[i] = j

    longest_prefix_pal_len = lps[-1]
    suffix_to_prepend = s[longest_prefix_pal_len:][::-1]
    return suffix_to_prepend + s


def test_q8_shortest_palindrome_prepend():
    # "aacecaaa" -> already has palindromic prefix "aacecaa" (len 7) -> prepend "a" -> "aaacecaaa"
    assert shortest_palindrome_prepend("aacecaaa") == "aaacecaaa"
    # "abcd" -> longest prefix pal "a" -> prepend "dcb" -> "dcbabcd"
    assert shortest_palindrome_prepend("abcd") == "dcbabcd"
    assert shortest_palindrome_prepend("") == ""
    print("=== Q8: Shortest Palindrome via Prepending Verified ===")


# ==============================================================================
# Question 9: Palindrome Permutation Check (Bit Manipulation)
# ==============================================================================
def can_permute_palindrome(s: str) -> bool:
    """
    Checks if any permutation of string s can form a palindrome.
    A string can form a palindrome if and only if at most one character has an odd frequency.
    Uses bitmask XOR toggling to achieve O(n) time and O(1) space.
    """
    bitmask = 0
    for ch in s:
        bit = 1 << (ord(ch) % 64)
        bitmask ^= bit  # Toggle bit

    # If at most one bit is set, bitmask & (bitmask - 1) == 0
    return (bitmask & (bitmask - 1)) == 0


def test_q9_can_permute_palindrome():
    assert can_permute_palindrome("code") is False
    assert can_permute_palindrome("aab") is True       # "aba"
    assert can_permute_palindrome("carerac") is True   # "racecar"
    assert can_permute_palindrome("tactcoa") is True   # "taco cat"
    print("=== Q9: Palindrome Permutation Check (Bit Manipulation) Verified ===")


# ==============================================================================
# Question 10: Architectural Genomic Reverse-Complement Palindrome Scanner
# ==============================================================================
class GenomicPalindromeScanner:
    """
    Bioinformatics tool for scanning DNA sequences for biological reverse-complement palindromes:
    In DNA, A complements T, and C complements G.
    A sequence like "GAATTC" is a reverse-complement palindrome because its complement
    read backwards ("CTTAAG"[::-1] = "GAATTC") equals itself (restriction enzyme EcoRI site).
    """
    COMPLEMENT = {"A": "T", "T": "A", "C": "G", "G": "C"}

    @classmethod
    def reverse_complement(cls, dna: str) -> str:
        return "".join(cls.COMPLEMENT.get(ch, "N") for ch in reversed(dna.upper()))

    @classmethod
    def is_reverse_complement_palindrome(cls, dna: str) -> bool:
        if len(dna) % 2 != 0:
            return False  # DNA palindromes must be even length
        return dna.upper() == cls.reverse_complement(dna)

    @classmethod
    def find_restriction_sites(cls, dna_sequence: str, min_len: int = 4, max_len: int = 8) -> List[Dict[str, Any]]:
        """
        Scans a chromosome sequence for all restriction enzyme cleavage sites.
        Returns list of matches with start index, length, and motif.
        """
        matches = []
        seq = dna_sequence.upper()
        n = len(seq)

        for length in range(min_len, max_len + 1, 2):  # Even lengths only
            for i in range(n - length + 1):
                sub = seq[i : i + length]
                if cls.is_reverse_complement_palindrome(sub):
                    matches.append({"start": i, "length": length, "motif": sub})

        # Sort by start coordinate
        return sorted(matches, key=lambda m: (m["start"], m["length"]))


def test_q10_genomic_palindrome_scanner():
    # EcoRI site: GAATTC (complement CTTAAG -> reversed GAATTC)
    assert GenomicPalindromeScanner.is_reverse_complement_palindrome("GAATTC") is True
    # HindIII site: AAGCTT (complement TTCGAA -> reversed AAGCTT)
    assert GenomicPalindromeScanner.is_reverse_complement_palindrome("AAGCTT") is True
    # Non-palindrome
    assert GenomicPalindromeScanner.is_reverse_complement_palindrome("GAAATC") is False

    # Scan DNA stream
    dna = "CCGAATTCGGGAAGCTTAA"
    sites = GenomicPalindromeScanner.find_restriction_sites(dna, min_len=6, max_len=6)
    # GAATTC at index 2, AAGCTT at index 11
    assert len(sites) == 2
    assert sites[0] == {"start": 2, "length": 6, "motif": "GAATTC"}
    assert sites[1] == {"start": 11, "length": 6, "motif": "AAGCTT"}
    print("=== Q10: Architectural Genomic Reverse-Complement Palindrome Scanner Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_plain_palindrome()
    test_q2_sentence_palindrome()
    test_q3_integer_palindrome()
    test_q4_almost_palindrome()
    test_q5_longest_palindromic_substring()
    test_q6_longest_palindromic_subsequence()
    test_q7_palindrome_partitioning()
    test_q8_shortest_palindrome_prepend()
    test_q9_can_permute_palindrome()
    test_q10_genomic_palindrome_scanner()
    print("\nAll 10 palindrome checker problem-solving questions passed successfully!")
