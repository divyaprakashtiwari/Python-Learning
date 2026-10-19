"""
Topic: Problem Solving - Anagram Detector
-----------------------------------------
Questions Covered:
1. Core Anagram Validation: Sorted string vs frequency array comparison.
2. Wordlist Anagram Grouping: Canonical sorting key dictionary clustering.
3. Sliding Window Anagram Search: O(n) start-index detection of anagram occurrences.
4. Minimum Steps to Make Two Strings Anagram: Asymmetric difference replacement count.
5. Minimum Deletions for Mutual Anagrams: Symmetric frequency disparity count.
6. Permutation in Substring: Fixed-length sliding window permutation detection.
7. Palindrome Anagram Possibility: Bitmask and parity checks for palindromic permutations.
8. Array Anagram Index Mapping: Bijective index translation across duplicate-safe arrays.
9. Multi-Word Sentence Anagrams: Normalizing casing, punctuation, and multi-word whitespace.
10. Architectural System: Real-Time Plagiarism & Anagrammatic Document Similarity Auditor.
"""

import collections
import string
from typing import List, Tuple, Optional, Any, Dict, Set


# ==============================================================================
# Question 1: Core Anagram Validation (Sorting vs Frequency Map)
# ==============================================================================
def is_anagram_sorting(s1: str, s2: str) -> bool:
    """Checks if s1 and s2 are anagrams via sorted comparison in O(n log n)."""
    return len(s1) == len(s2) and sorted(s1) == sorted(s2)


def is_anagram_frequency(s1: str, s2: str) -> bool:
    """Checks if s1 and s2 are anagrams via frequency hash map in O(n) time and O(k) space."""
    if len(s1) != len(s2):
        return False

    counts: Dict[str, int] = {}
    for ch in s1:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in s2:
        if ch not in counts or counts[ch] == 0:
            return False
        counts[ch] -= 1

    return True


def test_q1_core_anagram():
    assert is_anagram_sorting("anagram", "nagaram") is True
    assert is_anagram_frequency("anagram", "nagaram") is True
    assert is_anagram_sorting("rat", "car") is False
    assert is_anagram_frequency("rat", "car") is False
    print("=== Q1: Core Anagram Validation Verified ===")


# ==============================================================================
# Question 2: Wordlist Anagram Grouping
# ==============================================================================
def group_anagram_wordlist(words: List[str]) -> List[List[str]]:
    """Groups words into anagram buckets using sorted character tuple keys."""
    groups: Dict[str, List[str]] = {}
    for w in words:
        canonical_key = "".join(sorted(w))
        if canonical_key not in groups:
            groups[canonical_key] = []
        groups[canonical_key].append(w)
    return list(groups.values())


def test_q2_group_anagrams():
    input_words = ["listen", "silent", "enlist", "google", "gogole", "cat", "act"]
    grouped = group_anagram_wordlist(input_words)

    # Sort groups by size and first element for deterministic check
    sorted_groups = sorted([sorted(g) for g in grouped], key=lambda g: (len(g), g[0]))
    assert ["act", "cat"] in sorted_groups
    assert ["gogole", "google"] in sorted_groups
    assert ["enlist", "listen", "silent"] in sorted_groups
    print("=== Q2: Wordlist Anagram Grouping Verified ===")


# ==============================================================================
# Question 3: Sliding Window Anagram Search (Find All Anagrams)
# ==============================================================================
def find_all_anagram_indices(s: str, p: str) -> List[int]:
    """
    Finds all start indices in s where a substring is an anagram of pattern p.
    Uses sliding window frequency comparison in O(len(s)) time and O(1) space.
    """
    if len(p) > len(s):
        return []

    p_count = [0] * 26
    s_count = [0] * 26
    for i in range(len(p)):
        p_count[ord(p[i]) - ord("a")] += 1
        s_count[ord(s[i]) - ord("a")] += 1

    result = []
    if s_count == p_count:
        result.append(0)

    for i in range(len(p), len(s)):
        # Slide window: add new char, evict oldest char
        s_count[ord(s[i]) - ord("a")] += 1
        s_count[ord(s[i - len(p)]) - ord("a")] -= 1

        if s_count == p_count:
            result.append(i - len(p) + 1)

    return result


def test_q3_find_all_anagrams():
    # s = "cbaebabacd", p = "abc" -> anagrams at index 0 ("cba") and index 6 ("bac")
    indices = find_all_anagram_indices("cbaebabacd", "abc")
    assert indices == [0, 6]

    indices2 = find_all_anagram_indices("abab", "ab")
    assert indices2 == [0, 1, 2]
    print("=== Q3: Sliding Window Anagram Search Verified ===")


# ==============================================================================
# Question 4: Minimum Steps to Make Two Strings Anagram (Replacements)
# ==============================================================================
def min_steps_to_make_anagram(s: str, t: str) -> int:
    """
    Given two equal-length strings s and t, returns the minimum number of character
    replacements in t to make t an anagram of s.
    """
    if len(s) != len(t):
        raise ValueError("Strings must have equal length")

    s_counts = collections.Counter(s)
    t_counts = collections.Counter(t)

    steps = 0
    for ch, count in s_counts.items():
        if count > t_counts.get(ch, 0):
            steps += count - t_counts.get(ch, 0)

    return steps


def test_q4_min_steps_to_make_anagram():
    # "bab" and "aba" -> change 1 'a' in t to 'b' -> 1 step
    assert min_steps_to_make_anagram("bab", "aba") == 1
    # "leetcode" and "practice" -> 5 steps
    assert min_steps_to_make_anagram("leetcode", "practice") == 5
    assert min_steps_to_make_anagram("anagram", "nagaram") == 0
    print("=== Q4: Minimum Steps to Make Anagram Verified ===")


# ==============================================================================
# Question 5: Minimum Deletions for Mutual Anagrams
# ==============================================================================
def min_deletions_to_make_anagram(s1: str, s2: str) -> int:
    """
    Finds the minimum number of character deletions from either s1 or s2
    so that the remaining strings are anagrams of each other.
    Calculates symmetric difference of character frequency counts.
    """
    c1 = collections.Counter(s1)
    c2 = collections.Counter(s2)

    all_chars = set(c1.keys()) | set(c2.keys())
    deletions = 0

    for ch in all_chars:
        deletions += abs(c1.get(ch, 0) - c2.get(ch, 0))

    return deletions


def test_q5_min_deletions():
    # "cde" and "abc" -> delete 'd', 'e' from s1 (2) and 'a', 'b' from s2 (2) -> total 4 deletions
    assert min_deletions_to_make_anagram("cde", "abc") == 4
    assert min_deletions_to_make_anagram("hello", "billion") == 6
    assert min_deletions_to_make_anagram("silent", "listen") == 0
    print("=== Q5: Minimum Deletions for Mutual Anagrams Verified ===")


# ==============================================================================
# Question 6: Permutation in Substring (Inclusion Check)
# ==============================================================================
def check_inclusion(s1: str, s2: str) -> bool:
    """
    Checks if s2 contains a permutation of s1 as a contiguous substring.
    """
    return len(find_all_anagram_indices(s2, s1)) > 0


def test_q6_permutation_in_substring():
    assert check_inclusion("ab", "eidbaooo") is True   # "ba" is in s2
    assert check_inclusion("ab", "eidboaoo") is False
    assert check_inclusion("hello", "ooolleeehelloth") is True
    print("=== Q6: Permutation in Substring Verified ===")


# ==============================================================================
# Question 7: Palindromic Anagram Possibility
# ==============================================================================
def can_form_palindromic_anagram(s: str) -> bool:
    """
    Checks if characters in s can be rearranged to form a valid palindrome.
    At most one character can have an odd frequency.
    """
    counts = collections.Counter(s)
    odd_count = sum(1 for c in counts.values() if c % 2 != 0)
    return odd_count <= 1


def test_q7_palindromic_anagram():
    assert can_form_palindromic_anagram("civic") is True
    assert can_form_palindromic_anagram("ivicc") is True  # anagram of civic
    assert can_form_palindromic_anagram("livic") is False
    assert can_form_palindromic_anagram("aabbcc") is True
    print("=== Q7: Palindromic Anagram Possibility Verified ===")


# ==============================================================================
# Question 8: Array Anagram Index Mapping
# ==============================================================================
def anagram_mappings(nums1: List[int], nums2: List[int]) -> List[int]:
    """
    Given nums1 and nums2 where nums2 is an anagram of nums1,
    returns an index mapping array P where P[i] = j means nums1[i] == nums2[j].
    Supports duplicate elements.
    """
    lookup: Dict[int, List[int]] = {}
    for idx, num in enumerate(nums2):
        if num not in lookup:
            lookup[num] = []
        lookup[num].append(idx)

    mapping = []
    for num in nums1:
        mapping.append(lookup[num].pop())

    return mapping


def test_q8_anagram_mappings():
    a = [12, 28, 46, 32, 50]
    b = [50, 12, 32, 46, 28]
    p = anagram_mappings(a, b)
    # Check that for all i, a[i] == b[p[i]]
    for i in range(len(a)):
        assert a[i] == b[p[i]]
    print("=== Q8: Array Anagram Index Mapping Verified ===")


# ==============================================================================
# Question 9: Multi-Word Sentence Anagrams (Sanitized)
# ==============================================================================
def is_sentence_anagram(phrase1: str, phrase2: str) -> bool:
    """
    Validates if two multi-word phrases are anagrams, ignoring casing,
    spaces, and punctuation.
    """
    clean1 = [ch.lower() for ch in phrase1 if ch.isalnum()]
    clean2 = [ch.lower() for ch in phrase2 if ch.isalnum()]
    return collections.Counter(clean1) == collections.Counter(clean2)


def test_q9_sentence_anagrams():
    assert is_sentence_anagram("Clint Eastwood", "Old West Action") is True
    assert is_sentence_anagram("Tom Marvolo Riddle", "I am Lord Voldemort") is True
    assert is_sentence_anagram("The Morse Code", "Here come dots!") is True
    assert is_sentence_anagram("Hello World", "World Goodbye") is False
    print("=== Q9: Multi-Word Sentence Anagrams Verified ===")


# ==============================================================================
# Question 10: Architectural Plagiarism & Anagrammatic Similarity Auditor
# ==============================================================================
class AnagramDocumentAuditor:
    """
    Enterprise plagiarism detection system scanning for anagrammatic text rearrangement:
    - Normalizes token stream removing stop words
    - Computes n-gram frequency signatures
    - Calculates Jaccard similarity and exact sentence anagram matches
    """
    STOP_WORDS = {"the", "is", "at", "which", "on", "a", "an", "and", "or", "in", "to"}

    @classmethod
    def tokenize(cls, text: str) -> List[str]:
        words = text.lower().split()
        return [w.strip(string.punctuation) for w in words if w.strip(string.punctuation) not in cls.STOP_WORDS]

    @classmethod
    def sentence_signature(cls, sentence: str) -> Tuple[Tuple[str, int], ...]:
        """Creates an immutable canonical frequency signature of a sentence."""
        tokens = cls.tokenize(sentence)
        freq = collections.Counter(tokens)
        return tuple(sorted(freq.items()))

    @classmethod
    def audit_documents(cls, doc_a: str, doc_b: str) -> Dict[str, Any]:
        """
        Audits two documents, detecting sentence-level anagrammatic matches
        and overall vocabulary rearrangement overlap.
        """
        sentences_a = [s.strip() for s in doc_a.split(".") if s.strip()]
        sentences_b = [s.strip() for s in doc_b.split(".") if s.strip()]

        sigs_a = {cls.sentence_signature(s): s for s in sentences_a}
        matched_pairs: List[Tuple[str, str]] = []

        for sb in sentences_b:
            sig_b = cls.sentence_signature(sb)
            if sig_b in sigs_a and sig_b:  # Non-empty match
                matched_pairs.append((sigs_a[sig_b], sb))

        # Jaccard bag-of-words similarity
        tokens_a = set(cls.tokenize(doc_a))
        tokens_b = set(cls.tokenize(doc_b))
        jaccard = len(tokens_a & tokens_b) / len(tokens_a | tokens_b) if (tokens_a | tokens_b) else 1.0

        return {
            "anagrammatic_sentence_matches": matched_pairs,
            "match_count": len(matched_pairs),
            "jaccard_vocabulary_similarity": round(jaccard, 3),
            "is_suspicious_plagiarism": len(matched_pairs) > 0 or jaccard > 0.8,
        }


def test_q10_anagram_document_auditor():
    doc1 = (
        "Alice created a secure database system. "
        "Bob verified the payment transaction gateway."
    )
    # Doc 2 has words rearranged in sentences with identical meaning words
    doc2 = (
        "A secure system database Alice created. "
        "The weather in California was sunny."
    )

    audit = AnagramDocumentAuditor.audit_documents(doc1, doc2)
    assert audit["match_count"] == 1
    # Matched pair: "Alice created a secure database system" <-> "A secure system database Alice created"
    assert audit["is_suspicious_plagiarism"] is True
    print("=== Q10: Architectural Anagrammatic Document Auditor Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_core_anagram()
    test_q2_group_anagrams()
    test_q3_find_all_anagrams()
    test_q4_min_steps_to_make_anagram()
    test_q5_min_deletions()
    test_q6_permutation_in_substring()
    test_q7_palindromic_anagram()
    test_q8_anagram_mappings()
    test_q9_sentence_anagrams()
    test_q10_anagram_document_auditor()
    print("\nAll 10 anagram detector problem-solving questions passed successfully!")
