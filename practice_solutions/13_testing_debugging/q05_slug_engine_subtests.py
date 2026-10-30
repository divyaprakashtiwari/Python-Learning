"""
Topic 13: Testing & Debugging - Question 5: Slug Engine SubTests
Demonstrating parameterized unit testing with unittest.TestCase.subTest to evaluate
a matrix of inputs without stopping execution on first failure.
"""

import re
import unicodedata
import unittest
from typing import Dict, Any, List, Tuple


# ==========================================
# System Under Test (SUT)
# ==========================================
class SlugEngine:
    """Utility engine for converting strings into clean, SEO-friendly URL slugs."""

    @staticmethod
    def slugify(
        text: str,
        max_length: int = 50,
        separator: str = "-",
        allow_unicode: bool = False
    ) -> str:
        """
        Converts text to URL-safe slug.
        - Strips whitespace and non-alphanumeric characters.
        - De-accents unicode characters when allow_unicode=False.
        - Truncates at word boundaries to preserve integrity under max_length.
        - Collapses duplicate separators.
        """
        if text is None or not str(text).strip():
            raise ValueError("Input text cannot be empty or solely whitespace.")
        if max_length <= 0:
            raise ValueError("max_length must be a positive integer.")

        # Normalize unicode accents if unicode is disallowed
        if not allow_unicode:
            text = unicodedata.normalize("NFKD", text)
            text = "".join(c for c in text if not unicodedata.combining(c))

        text = text.lower()

        # Strip non-alphanumeric characters while preserving whitespace and chosen separator
        escaped_sep = re.escape(separator)
        pattern = rf"[^a-z0-9\s{escaped_sep}]"
        text = re.sub(pattern, "", text)

        # Split into words by collapsing whitespace and separator sequences
        split_pattern = rf"[\s{escaped_sep}]+"
        words = [w for w in re.split(split_pattern, text.strip()) if w]
        if not words:
            raise ValueError("Input contains no alphanumeric characters after sanitization.")

        # Assemble words respecting max_length at word boundaries
        result_words: List[str] = []
        current_len = 0
        for word in words:
            sep_len = len(separator) if result_words else 0
            if current_len + sep_len + len(word) <= max_length:
                result_words.append(word)
                current_len += sep_len + len(word)
            else:
                break

        # If even the first word exceeds max_length, slice that single word
        if not result_words and words:
            result_words = [words[0][:max_length]]

        slug = separator.join(result_words)
        return slug.strip(separator)


# ==========================================
# Parameterized Test Suite with subTest
# ==========================================
class TestSlugEngineParameterized(unittest.TestCase):
    """Evaluates SlugEngine against comprehensive test matrices using subTest."""

    def test_valid_slug_matrix(self) -> None:
        """Evaluates 10 matrix permutations of valid inputs, separators, and length boundaries."""
        valid_matrix: List[Tuple[str, str, Dict[str, Any]]] = [
            ("Hello World!", "hello-world", {}),
            ("Crème Brûlée & Café", "creme-brulee-cafe", {}),
            ("Python 3.12: The Next Gen", "python-312-the", {"max_length": 15}),
            ("Custom___Under__Score", "custom_under_score", {"separator": "_"}),
            ("   Trim Leading and Trailing   ", "trim-leading-and-trailing", {}),
            ("Multiple   Spaces & Special #$@! Chars", "multiple-spaces-special-chars", {}),
            ("Supercalifragilisticexpialidocious", "supercalifragilistic", {"max_length": 20}),
            ("Café 123", "cafe-123", {}),
            ("Alpha Beta Gamma", "alpha/beta/gamma", {"separator": "/"}),
            ("JustOneWord", "justoneword", {}),
        ]

        for raw_input, expected_slug, options in valid_matrix:
            with self.subTest(raw_input=raw_input, expected=expected_slug, options=options):
                actual = SlugEngine.slugify(raw_input, **options)
                self.assertEqual(actual, expected_slug)

    def test_invalid_input_matrix(self) -> None:
        """Evaluates 4 matrix permutations of invalid edge cases raising ValueError."""
        invalid_matrix: List[Tuple[str, Dict[str, Any]]] = [
            ("", {}),                                    # Empty string
            ("     \t\n   ", {}),                        # Whitespace only
            ("Valid Text", {"max_length": 0}),           # Zero max_length
            ("Valid Text", {"max_length": -10}),         # Negative max_length
        ]

        for raw_input, options in invalid_matrix:
            with self.subTest(invalid_input=raw_input, options=options):
                with self.assertRaises(ValueError):
                    SlugEngine.slugify(raw_input, **options)


# ==========================================
# Driver Execution
# ==========================================
if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSlugEngineParameterized)
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)

    print("Parameterized Test Method Run: 2 (1 for valid matrix with 10 subtests, 1 for invalid matrix with 4 subtests)")
    print("Total SubTests Evaluated: 14")
    print("SubTest Valid Examples:")
    print('- "Hello World!" -> "hello-world"')
    print('- "Crème Brûlée & Café" -> "creme-brulee-cafe"')
    print('- "Python 3.12: The Next Gen" (max_len=15) -> "python-312-the"')
    print('- "Custom___Under__Score" (separator="_") -> "custom_under_score"')
    print(f"All 14 SubTests Passed: {result.wasSuccessful()}")
