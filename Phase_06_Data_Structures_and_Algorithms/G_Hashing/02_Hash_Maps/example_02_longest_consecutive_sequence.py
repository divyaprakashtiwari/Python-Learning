"""
Phase 6 - Section G.02: Hash Maps
Example 02: Longest Consecutive Sequence

Demonstrating:
1. Longest Consecutive Sequence via HashSet O(n) checking sequence starts.
2. Boundary-Map approach storing contiguous interval lengths for dynamic stream.
"""


def longest_consecutive_set(nums):
    """
    Find length of the longest consecutive elements sequence in O(n) time.
    Only starts expanding if num - 1 is not in set (i.e., num is a sequence start).
    """
    if not nums:
        return 0

    num_set = set(nums)
    longest_streak = 0

    for num in num_set:
        if num - 1 not in num_set:
            current_num = num
            current_streak = 1

            while current_num + 1 in num_set:
                current_num += 1
                current_streak += 1

            longest_streak = max(longest_streak, current_streak)

    return longest_streak


class IntervalBoundaryMap:
    """
    Dynamic stream solver for longest consecutive sequence.
    Map stores length of continuous sequence an element belongs to.
    """
    def __init__(self):
        self.bounds = {}  # num -> interval length
        self.max_len = 0

    def add(self, num):
        if num in self.bounds:
            return self.max_len

        left = self.bounds.get(num - 1, 0)
        right = self.bounds.get(num + 1, 0)
        length = left + right + 1

        self.bounds[num] = length
        # Update boundaries of the merged sequence
        self.bounds[num - left] = length
        self.bounds[num + right] = length

        self.max_len = max(self.max_len, length)
        return self.max_len


def main():
    print("=" * 60)
    print("1. Longest Consecutive Sequence (Set-Based O(n))")
    print("=" * 60)
    test1 = [100, 4, 200, 1, 3, 2]
    ans1 = longest_consecutive_set(test1)
    print("Input:", test1)
    print("Longest Consecutive Length:", ans1)  # [1, 2, 3, 4] -> 4

    test2 = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
    ans2 = longest_consecutive_set(test2)
    print("\nInput:", test2)
    print("Longest Consecutive Length:", ans2)  # [0..8] -> 9

    print("\n" + "=" * 60)
    print("2. Dynamic Interval Boundary Map (Stream)")
    print("=" * 60)
    boundary_tracker = IntervalBoundaryMap()
    stream = [10, 1, 4, 2, 3]
    for x in stream:
        current_max = boundary_tracker.add(x)
        print("Inserted:", x, "-> Current Max Consecutive Length:", current_max)


if __name__ == "__main__":
    main()
