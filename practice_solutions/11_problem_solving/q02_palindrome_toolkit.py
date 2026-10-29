"""
Question 2: Comprehensive Palindrome Validation & Detection Toolkit
Topic: Problem Solving & Competitive Programming Patterns

Key Concepts Tested:
- Two-pointer alphanumeric phrase palindrome validation
- Mathematical palindrome verification without string conversion (O(log10 N) time, O(1) space)
- Almost-palindrome validation with at most one character deletion (Valid Palindrome II)
- Longest palindromic substring via Expand Around Center technique
"""

from typing import Tuple, Optional


class PalindromeToolkit:
    """
    Comprehensive suite for string and numeric palindrome problems.
    """

    @staticmethod
    def is_phrase_palindrome(s: str) -> bool:
        """
        Validates whether s is a palindrome considering only alphanumeric characters
        and ignoring cases, using two converging pointers without string reversal.
        """
        left = 0
        right = len(s) - 1

        while left < right:
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1

            if s[left].lower() != s[right].lower():
                return False

            left += 1
            right -= 1

        return True

    @staticmethod
    def is_number_palindrome(num: int) -> bool:
        """
        Determines whether num is a palindrome purely mathematically
        without converting the number to a string.
        """
        # Negative numbers and non-zero numbers ending in 0 cannot be palindromes
        if num < 0 or (num != 0 and num % 10 == 0):
            return False

        # Revert the second half of the digits
        reversed_half = 0
        while num > reversed_half:
            reversed_half = (reversed_half * 10) + (num % 10)
            num //= 10

        # For even digit lengths: num == reversed_half
        # For odd digit lengths: num == reversed_half // 10 (middle digit discarded)
        return num == reversed_half or num == reversed_half // 10

    @staticmethod
    def can_be_palindrome_with_one_removal(s: str) -> Tuple[bool, Optional[int]]:
        """
        Checks if s can become a palindrome by removing at most one character.
        Returns (True, None) if already palindrome, (True, index) of character to drop,
        or (False, None) if impossible.
        """
        def is_sub_pal(sub: str) -> bool:
            return sub == sub[::-1]

        left = 0
        right = len(s) - 1

        while left < right:
            if s[left] != s[right]:
                # Test removing char at right
                if is_sub_pal(s[left:right]):
                    return (True, right)
                # Test removing char at left
                if is_sub_pal(s[left + 1 : right + 1]):
                    return (True, left)
                return (False, None)

            left += 1
            right -= 1

        return (True, None)

    @staticmethod
    def longest_palindromic_substring(s: str) -> str:
        """
        Finds the longest contiguous palindromic substring using
        Expand Around Center in O(N^2) time and O(1) auxiliary space.
        """
        if len(s) <= 1:
            return s

        start = 0
        max_len = 1

        def expand(left: int, right: int) -> Tuple[int, int]:
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            # Length is (right - 1) - (left + 1) + 1 = right - left - 1
            return (left + 1, right - left - 1)

        for i in range(len(s)):
            # Odd length palindromes (center at i)
            start_odd, len_odd = expand(i, i)
            if len_odd > max_len:
                max_len = len_odd
                start = start_odd

            # Even length palindromes (center between i and i + 1)
            start_even, len_even = expand(i, i + 1)
            if len_even > max_len:
                max_len = len_even
                start = start_even

        return s[start : start + max_len]


if __name__ == "__main__":
    toolkit = PalindromeToolkit()

    print("=== 1. Phrase Palindrome Validation ===")
    phrase_true = "A man, a plan, a canal: Panama!"
    phrase_false = "race a car"
    print(f'Phrase Palindrome "{phrase_true}": {toolkit.is_phrase_palindrome(phrase_true)}')
    print(f'Phrase Palindrome "{phrase_false}": {toolkit.is_phrase_palindrome(phrase_false)}')

    print("\n=== 2. Mathematical Number Palindrome (No String Conversion) ===")
    print(f"Number Palindrome 12321: {toolkit.is_number_palindrome(12321)}")
    print(f"Number Palindrome -121: {toolkit.is_number_palindrome(-121)}")
    print(f"Number Palindrome 10: {toolkit.is_number_palindrome(10)}")
    print(f"Number Palindrome 0: {toolkit.is_number_palindrome(0)}")

    print("\n=== 3. Almost Palindrome (Valid Palindrome II) ===")
    sample_str = "abca"
    almost_res = toolkit.can_be_palindrome_with_one_removal(sample_str)
    print(f'Almost Palindrome "{sample_str}": {almost_res}')

    print("\n=== 4. Longest Palindromic Substring ===")
    babad_res = toolkit.longest_palindromic_substring("babad")
    print(f'Longest Palindromic Substring of "babad": \'{babad_res}\'')
    cbbd_res = toolkit.longest_palindromic_substring("cbbd")
    print(f'Longest Palindromic Substring of "cbbd": \'{cbbd_res}\'')

    print("\n=== 5. Edge Cases ===")
    print(f"Empty string phrase palindrome: {toolkit.is_phrase_palindrome('')}")
    print(f"Single char phrase palindrome: {toolkit.is_phrase_palindrome('X')}")
    print(f"Empty string longest substring: '{toolkit.longest_palindromic_substring('')}'")
