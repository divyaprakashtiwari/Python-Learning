"""
Phase 6 - Data Structures and Algorithms
Section D: Arrays and Strings - Topic 06: String Problems
Example 02: KMP (Knuth-Morris-Pratt) Pattern Matching in O(N + M) Linear Time

Demonstrates:
1. Why Naive String Matching (`s.find(pattern)` brute force) degrades to O(N * M) worst-case
   time on repetitive strings like `text = "AAAAAAAAAB"`, `pattern = "AAAAB"`.
2. How the KMP Algorithm precomputes the **LPS (Longest Proper Prefix which is also a Suffix)**
   array in O(M) time so the text pointer `i` NEVER backs up (`O(N + M)` guaranteed linear time!).
"""


def build_kmp_lps_table(pattern: str) -> list[int]:
    """
    Build the KMP Longest Proper Prefix-Suffix (LPS / failure function) table in O(M) time.
    `lps[k]` = length of the longest proper prefix of `pattern[0..k]` that is also a suffix
    of `pattern[0..k]`.
    """
    m = len(pattern)
    lps = [0] * m
    length = 0  # Length of previous longest prefix-suffix
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                # Fall back to the shorter prefix-suffix without incrementing `i`!
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search_all(text: str, pattern: str) -> tuple[list[int], list[int]]:
    """
    Find all 0-based starting indices of `pattern` in `text` in O(N + M) worst-case time.
    Returns `(match_indices, lps_table)`.
    """
    if not pattern:
        return [0], []

    lps = build_kmp_lps_table(pattern)
    matches: list[int] = []
    i = 0  # Pointer in `text` (NEVER decrements!)
    j = 0  # Pointer in `pattern`
    n, m = len(text), len(pattern)

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                matches.append(i - m)
                j = lps[j - 1]  # Continue searching for overlapping matches!
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches, lps


if __name__ == "__main__":
    print("=" * 72)
    print("1. KNUTH-MORRIS-PRATT (KMP) O(N + M) STRING MATCHING & LPS TABLE")
    print("=" * 72)

    dna_text = "ABABDABACDABABCABABABABCABAB"
    dna_pat = "ABABCABAB"
    indices, lps_tbl = kmp_search_all(dna_text, dna_pat)

    print(f"Text    : '{dna_text}'")
    print(f"Pattern : '{dna_pat}'")
    print(f"LPS     : {lps_tbl}")
    print(f"Matches : {indices} (Overlapping matches found in a single pass!)")
