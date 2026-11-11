"""
Phase 6 - Data Structures and Algorithms
Section D: Arrays and Strings - Topic 02: Two Pointer Technique
Example 02: Same-Direction (Reader / Writer) Two Pointers (In-Place Deduplication & Move Zeroes)

Demonstrates:
1. Removing Duplicates from a Sorted Array In-Place (LeetCode 26 / 80):
   - `writer` pointer marks the boundary of kept unique elements.
   - `reader` pointer scans ahead through the array in O(N) time and O(1) space.
2. Moving All Zeroes to the End While Preserving Relative Order of Non-Zeroes (LeetCode 283)
   in a single O(N) pass with minimal swaps.
"""


def remove_duplicates_sorted_in_place(arr: list[int], max_allowed_copies: int = 1) -> int:
    """
    In-place deduplication of a sorted array allowing at most `max_allowed_copies`
    of each distinct value (set `max_allowed_copies=1` for strict uniqueness, or `2` for LC 80).
    Returns the new valid prefix length `writer`.
    Time Complexity : O(N)
    Space Complexity: O(1)
    """
    n = len(arr)
    if n <= max_allowed_copies:
        return n

    writer = max_allowed_copies
    for reader in range(max_allowed_copies, n):
        # Compare current `arr[reader]` with the element `max_allowed_copies` slots back
        # in the ALREADY-WRITTEN valid prefix!
        if arr[reader] != arr[writer - max_allowed_copies]:
            arr[writer] = arr[reader]
            writer += 1

    return writer


def move_zeroes_in_place(arr: list[int]) -> list[int]:
    """
    Move all 0s to the end of `arr` in-place while maintaining the relative FIFO order
    of all non-zero elements in a single O(N) pass.
    """
    a = arr.copy()
    writer = 0

    for reader in range(len(a)):
        if a[reader] != 0:
            if writer != reader:
                a[writer], a[reader] = a[reader], a[writer]
            writer += 1

    return a


if __name__ == "__main__":
    print("=" * 72)
    print("1. READER/WRITER IN-PLACE DEDUPLICATION ON SORTED ARRAY")
    print("=" * 72)

    dup_data_1 = [10, 10, 20, 30, 30, 30, 40, 50, 50]
    k1 = remove_duplicates_sorted_in_place(dup_data_1, max_allowed_copies=1)
    print(f"Strict Unique (max 1 copy) -> Length={k1}, Prefix: {dup_data_1[:k1]}")

    dup_data_2 = [10, 10, 10, 20, 30, 30, 30, 40, 50, 50]
    k2 = remove_duplicates_sorted_in_place(dup_data_2, max_allowed_copies=2)
    print(f"At Most 2 Copies (LC 80)   -> Length={k2}, Prefix: {dup_data_2[:k2]}")

    print("\n" + "=" * 72)
    print("2. MOVE ZEROES TO END IN-PLACE (STABLE NON-ZERO ORDER)")
    print("=" * 72)
    sensor_packets = [0, 42, 0, 19, 88, 0, 0, 73, 15]
    print(f"Original Stream : {sensor_packets}")
    print(f"Compacted Stream: {move_zeroes_in_place(sensor_packets)}")
