"""
Phase 6 - Section I.04: Top K Problems
Example 02: Reorganize String and Rearrange K Distance Apart

Demonstrating:
1. Reorganize String so no adjacent characters are identical using Max-Heap of character frequencies.
2. Rearrange String K Distance Apart using Max-Heap + Cooldown Queue.
"""

import heapq
from collections import Counter, deque


def reorganize_string(s):
    """
    Rearrange characters so no two adjacent characters are identical.
    Returns empty string if impossible (max_freq > (len(s) + 1) // 2).
    Time Complexity: O(n log A) where A is alphabet size (<= 26) -> O(n)
    Space Complexity: O(A)
    """
    counts = Counter(s)
    max_freq = max(counts.values())
    if max_freq > (len(s) + 1) // 2:
        return ""

    # Max-heap: (-freq, char)
    max_heap = [(-freq, char) for char, freq in counts.items()]
    heapq.heapify(max_heap)

    prev_freq, prev_char = 0, ""
    result = []

    while max_heap:
        freq, char = heapq.heappop(max_heap)
        result.append(char)

        # Re-add previous character if it still had remaining frequency
        if prev_freq < 0:
            heapq.heappush(max_heap, (prev_freq, prev_char))

        # Decrement frequency (remember freq is negative)
        prev_freq = freq + 1
        prev_char = char

    return "".join(result)


def rearrange_k_distance_apart(s, k):
    """
    Rearrange characters such that identical characters are at least distance k apart.
    Time Complexity: O(n log A)
    Space Complexity: O(n)
    """
    if k <= 1:
        return s

    counts = Counter(s)
    max_heap = [(-freq, char) for char, freq in counts.items()]
    heapq.heapify(max_heap)

    cooldown = deque()
    result = []

    while max_heap:
        freq, char = heapq.heappop(max_heap)
        result.append(char)

        # Append to cooldown queue with remaining frequency
        cooldown.append((freq + 1, char))

        # Once cooldown reaches size k, release the oldest element back to heap
        if len(cooldown) >= k:
            c_freq, c_char = cooldown.popleft()
            if c_freq < 0:
                heapq.heappush(max_heap, (c_freq, c_char))

    # Drain remaining cooldown items that still have frequency
    while cooldown:
        c_freq, _ = cooldown.popleft()
        if c_freq < 0:
            return ""  # Impossible to satisfy distance constraint

    return "".join(result) if len(result) == len(s) else ""


def main():
    print("=" * 60)
    print("1. Reorganize String (No Adjacent Duplicates)")
    print("=" * 60)
    for test in ["aab", "aaab", "vvvlo", "baaba"]:
        res = reorganize_string(test)
        print(f"s = '{test:5s}' -> Reorganized: '{res}'")

    print("\n" + "=" * 60)
    print("2. Rearrange String K Distance Apart")
    print("=" * 60)
    test_cases = [("aabbcc", 3), ("aaabc", 3), ("aaadbbcc", 2)]
    for text, k in test_cases:
        res = rearrange_k_distance_apart(text, k)
        print(f"s = '{text}', k = {k} -> Result: '{res}'")


if __name__ == "__main__":
    main()
