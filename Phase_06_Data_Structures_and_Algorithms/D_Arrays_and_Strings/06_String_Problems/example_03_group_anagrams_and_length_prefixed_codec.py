"""
Phase 6 - Data Structures and Algorithms
Section D: Arrays and Strings - Topic 06: String Problems
Example 03: Group Anagrams via 26-Tuple Frequency Signature, Run-Length Encoding, & Reverse Words

Demonstrates:
1. Grouping Anagrams in O(N * L) time (instead of O(N * L log L) sorting each word)
   by using a 26-integer character-frequency tuple as the dictionary key!
2. Length-Prefixed Encode & Decode Strings (LeetCode 271) that safely handles ANY special
   characters (including `#`, `:`, and digits) inside the strings!
"""

from collections import defaultdict


def group_anagrams_linear(words: list[str]) -> list[list[str]]:
    """
    Group anagrams in O(N * L) time (where N = number of words, L = max word length)
    using a 26-slot lowercase letter count tuple as the hash map key.
    """
    groups: dict[tuple[int, ...], list[str]] = defaultdict(list)

    for word in words:
        counts = [0] * 26
        for ch in word:
            counts[ord(ch) - ord("a")] += 1
        groups[tuple(counts)].append(word)

    return list(groups.values())


def encode_strings_length_prefixed(strs: list[str]) -> str:
    """
    Serialize a list of arbitrary strings into a single string using `<len>#<payload>` framing.
    Works even if a string contains `#` or digits!
    """
    return "".join(f"{len(s)}#{s}" for s in strs)


def decode_strings_length_prefixed(encoded: str) -> list[str]:
    """Deserialize a `<len>#<payload>` framed string in O(N) time."""
    decoded: list[str] = []
    i = 0
    n = len(encoded)

    while i < n:
        # Find the '#' delimiter after the integer length prefix
        sep_idx = encoded.find("#", i)
        length = int(encoded[i:sep_idx])
        payload_start = sep_idx + 1
        payload_end = payload_start + length
        decoded.append(encoded[payload_start:payload_end])
        i = payload_end

    return decoded


if __name__ == "__main__":
    print("=" * 72)
    print("1. GROUP ANAGRAMS IN O(N * L) TIME VIA 26-TUPLE SIGNATURE")
    print("=" * 72)
    vocab = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print(f"Input Words    : {vocab}")
    print(f"Anagram Groups : {group_anagrams_linear(vocab)}")

    print("\n" + "=" * 72)
    print("2. LENGTH-PREFIXED STRING ENCODE & DECODE (LEETCODE 271)")
    print("=" * 72)
    tricky_messages = ["hello#world", "12#34", "", "antigravity:python"]
    wire_payload = encode_strings_length_prefixed(tricky_messages)
    restored = decode_strings_length_prefixed(wire_payload)
    assert restored == tricky_messages
    print(f"Original List  : {tricky_messages}")
    print(f"Wire Payload   : '{wire_payload}'")
    print(f"Decoded List   : {restored}")
