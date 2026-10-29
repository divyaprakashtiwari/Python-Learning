"""
Question 5: Anagram Engine (Detection, Clustering & Deletion Distance)
Topic: Problem Solving & Competitive Programming Patterns

Key Concepts Tested:
- Linear-time O(N) anagram verification using frequency mapping
- Phrase anagram normalization across spaces and punctuation
- Optimal O(N * K) anagram grouping using 26-element character-count tuples
- Character deletion distance calculation for anagram transformation
"""

from collections import Counter, defaultdict
from typing import List, Dict, Tuple


class AnagramEngine:
    """
    Algorithmic engine for anagram analysis, grouping, and edit distance.
    """

    @staticmethod
    def _normalize(text: str) -> str:
        """Strips non-alphabetic characters and converts to lowercase."""
        return "".join(ch.lower() for ch in text if ch.isalpha())

    def is_anagram(self, s1: str, s2: str) -> bool:
        """
        Validates if s1 and s2 are exact anagrams in O(N) time and O(1) auxiliary space (26 chars).
        """
        clean1 = self._normalize(s1)
        clean2 = self._normalize(s2)

        if len(clean1) != len(clean2):
            return False

        return Counter(clean1) == Counter(clean2)

    def is_phrase_anagram(self, phrase1: str, phrase2: str) -> bool:
        """Validates if two multi-word phrases are anagrams."""
        return self.is_anagram(phrase1, phrase2)

    @staticmethod
    def group_anagrams(words: List[str]) -> List[List[str]]:
        """
        Groups words by anagram identity in O(N * K) time.
        Uses 26-tuple character frequency signatures as hashable dictionary keys.
        Returns groups sorted internally and ordered by group size descending.
        """
        groups: Dict[Tuple[int, ...], List[str]] = defaultdict(list)

        for word in words:
            # 26-element array for 'a' through 'z'
            counts = [0] * 26
            for ch in word.lower():
                if "a" <= ch <= "z":
                    counts[ord(ch) - ord("a")] += 1
            groups[tuple(counts)].append(word)

        # Sort each group internally and sort all groups by size descending
        sorted_groups = [sorted(group) for group in groups.values()]
        sorted_groups.sort(key=lambda g: len(g), reverse=True)
        return sorted_groups

    @staticmethod
    def min_deletions_to_make_anagram(s1: str, s2: str) -> int:
        """
        Computes the minimum number of character deletions across both strings
        so that the remaining characters form an anagram.
        """
        c1 = Counter(s1.lower())
        c2 = Counter(s2.lower())

        all_chars = set(c1.keys()).union(set(c2.keys()))
        deletions = 0

        for ch in all_chars:
            deletions += abs(c1.get(ch, 0) - c2.get(ch, 0))

        return deletions


if __name__ == "__main__":
    engine = AnagramEngine()

    print("=== 1. Simple and Phrase Anagrams ===")
    test1 = engine.is_anagram("silent", "listen")
    test2 = engine.is_phrase_anagram("Debit Card", "Bad Credit")
    test3 = engine.is_anagram("hello", "world")

    print(f"is_anagram('silent', 'listen'): {test1}")
    print(f"is_phrase_anagram('Debit Card', 'Bad Credit'): {test2}")
    print(f"is_anagram('hello', 'world'): {test3}")

    print("\n=== 2. Group Anagrams ===")
    words_to_group = ["eat", "tea", "tan", "ate", "nat", "bat"]
    grouped = engine.group_anagrams(words_to_group)
    print(f"Grouped Anagrams:\n{grouped}")

    print("\n=== 3. Minimum Deletions for Anagram ===")
    deletions = engine.min_deletions_to_make_anagram("cde", "abc")
    print(f"Min Deletions for 'cde' and 'abc': {deletions}")

    print("\n=== 4. Edge Cases ===")
    print(f"Empty strings are anagrams: {engine.is_anagram('', '')}")
    print(f"Unequal lengths fast return: {engine.is_anagram('a', 'ab')}")
    print(f"Identical words min deletions: {engine.min_deletions_to_make_anagram('python', 'python')}")
