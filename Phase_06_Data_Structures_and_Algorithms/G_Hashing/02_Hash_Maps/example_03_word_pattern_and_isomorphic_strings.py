"""
Phase 6 - Section G.02: Hash Maps
Example 03: Word Pattern, Isomorphic Strings, and Group Shifted Strings

Demonstrating bijective mapping and canonical representation with hash maps:
1. Word Pattern verification (1-to-1 bijection).
2. Isomorphic Strings test.
3. Group Shifted Strings (canonical key transformation).
"""


def word_pattern(pattern, s):
    """
    Check if s follows pattern via strict bijection.
    Example: pattern = 'abba', s = 'dog cat cat dog' -> True
    """
    words = s.split()
    if len(pattern) != len(words):
        return False

    char_to_word = {}
    word_to_char = {}

    for ch, word in zip(pattern, words):
        if ch in char_to_word and char_to_word[ch] != word:
            return False
        if word in word_to_char and word_to_char[word] != ch:
            return False
        char_to_word[ch] = word
        word_to_char[word] = ch

    return True


def is_isomorphic(s, t):
    """
    Check if two strings s and t are isomorphic.
    All occurrences of a character in s map to one in t and vice-versa.
    """
    if len(s) != len(t):
        return False

    s_to_t = {}
    t_to_s = {}

    for c1, c2 in zip(s, t):
        if (c1 in s_to_t and s_to_t[c1] != c2) or (c2 in t_to_s and t_to_s[c2] != c1):
            return False
        s_to_t[c1] = c2
        t_to_s[c2] = c1

    return True


def group_shifted_strings(strings):
    """
    Group strings that belong to the same shifting sequence.
    Example: 'abc' and 'bcd' and 'xyz' have shift differences (1, 1).
    """
    groups = {}

    for s in strings:
        # Canonical diff tuple
        if len(s) == 1:
            key = ()
        else:
            key = tuple((ord(s[i]) - ord(s[i - 1])) % 26 for i in range(1, len(s)))

        if key not in groups:
            groups[key] = []
        groups[key].append(s)

    return list(groups.values())


def main():
    print("=" * 60)
    print("1. Word Pattern Validation")
    print("=" * 60)
    patterns = [
        ("abba", "dog cat cat dog"),
        ("abba", "dog cat cat fish"),
        ("aaaa", "dog cat cat dog"),
        ("abba", "dog dog dog dog"),
    ]
    for p, s in patterns:
        match = word_pattern(p, s)
        print(f"pattern='{p}', s='{s}' -> Match: {match}")

    print("\n" + "=" * 60)
    print("2. Isomorphic Strings Validation")
    print("=" * 60)
    pairs = [
        ("egg", "add"),
        ("foo", "bar"),
        ("paper", "title"),
        ("ab", "aa"),
    ]
    for s1, s2 in pairs:
        res = is_isomorphic(s1, s2)
        print(f"s='{s1}', t='{s2}' -> Isomorphic: {res}")

    print("\n" + "=" * 60)
    print("3. Group Shifted Strings")
    print("=" * 60)
    word_list = ["abc", "bcd", "acef", "xyz", "az", "ba", "a", "z"]
    grouped = group_shifted_strings(word_list)
    print("Input:", word_list)
    print("Grouped by shift pattern:")
    for group in grouped:
        print(" ", group)


if __name__ == "__main__":
    main()
