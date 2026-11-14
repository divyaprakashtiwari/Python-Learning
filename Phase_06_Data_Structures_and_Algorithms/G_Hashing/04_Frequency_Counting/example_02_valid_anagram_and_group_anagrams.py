"""
Phase 6 - Section G.04: Frequency Counting
Example 02: Valid Anagram and Group Anagrams

Demonstrating:
1. Valid Anagram verification using character frequency array in O(n) time.
2. Group Anagrams using 26-tuple character frequency signatures as dictionary keys.
3. Sorting baseline comparison for Group Anagrams.
"""

from collections import defaultdict


def is_anagram_frequency(s, t):
    """
    Check if s and t are anagrams using a fixed 26-element integer frequency array.
    Time Complexity: O(len(s) + len(t))
    Space Complexity: O(1) (fixed 26 lowercase English letters)
    """
    if len(s) != len(t):
        return False

    counts = [0] * 26
    for c1, c2 in zip(s, t):
        counts[ord(c1) - ord('a')] += 1
        counts[ord(c2) - ord('a')] -= 1

    return all(c == 0 for c in counts)


def group_anagrams_count_signature(strs):
    """
    Group anagrams by 26-element character count tuple signature.
    Time Complexity: O(n * k) where n = len(strs), k = max word length.
    Space Complexity: O(n * k)
    """
    groups = defaultdict(list)

    for word in strs:
        count = [0] * 26
        for char in word:
            count[ord(char) - ord('a')] += 1
        groups[tuple(count)].append(word)

    return list(groups.values())


def group_anagrams_sorted(strs):
    """
    Group anagrams by sorted string key.
    Time Complexity: O(n * k log k)
    """
    groups = defaultdict(list)
    for word in strs:
        key = "".join(sorted(word))
        groups[key].append(word)
    return list(groups.values())


def main():
    print("=" * 60)
    print("1. Valid Anagram Verification")
    print("=" * 60)
    pairs = [
        ("anagram", "nagaram"),
        ("rat", "car"),
        ("listen", "silent"),
        ("aacc", "ccac"),
    ]
    for s, t in pairs:
        valid = is_anagram_frequency(s, t)
        print(f"s = '{s}', t = '{t}' -> Anagram: {valid}")

    print("\n" + "=" * 60)
    print("2. Group Anagrams via 26-Tuple Frequency Signature O(N * K)")
    print("=" * 60)
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    grouped = group_anagrams_count_signature(words)
    print("Input Words:", words)
    print("Grouped Anagrams:")
    for g in grouped:
        print(" ", sorted(g))

    print("\n" + "=" * 60)
    print("3. Group Anagrams via Sorted Key Baseline")
    print("=" * 60)
    grouped_sorted = group_anagrams_sorted(words)
    print("Sorted Key Result Count:", len(grouped_sorted))


if __name__ == "__main__":
    main()
