"""
Phase 6 - Data Structures and Algorithms
Section D: Arrays and Strings - Topic 04: Prefix Sum
Example 01: 1D Prefix Sum Array for O(1) Range Sum Queries & Equilibrium / Pivot Index

Demonstrates:
1. Precomputing a `(N + 1)`-length Prefix Sum array `P` where `P[i] = sum(arr[0 .. i - 1])`
   in O(N) time so ANY inclusive range sum query `sum(arr[L .. R])` is answered in O(1) time:
   `range_sum(L, R) = P[R + 1] - P[L]`.
2. Finding the Pivot / Equilibrium Index (LeetCode 724) where strictly left sum == strictly
   right sum in a single O(N) pass and O(1) auxiliary space!
"""


class RangeSumQueryImmutable:
    """
    Precomputes a 1-indexed padded prefix sum array `prefix` of length `N + 1`
    in O(N) time so `query(left, right)` executes in O(1) time without `if left == 0:` branches!
    """

    def __init__(self, nums: list[int]) -> None:
        self.prefix = [0] * (len(nums) + 1)
        for i, val in enumerate(nums):
            self.prefix[i + 1] = self.prefix[i] + val

    def query(self, left: int, right: int) -> int:
        """Return sum of `nums[left .. right]` inclusive in O(1) time."""
        return self.prefix[right + 1] - self.prefix[left]


def find_pivot_equilibrium_index(nums: list[int]) -> int:
    """
    Find the leftmost index `i` where `sum(nums[0 .. i - 1]) == sum(nums[i + 1 .. n - 1])`.
    Returns -1 if no equilibrium index exists.
    Time Complexity : O(N)
    Space Complexity: O(1)
    """
    total_sum = sum(nums)
    left_sum = 0

    for i, val in enumerate(nums):
        right_sum = total_sum - left_sum - val
        if left_sum == right_sum:
            return i
        left_sum += val

    return -1


if __name__ == "__main__":
    print("=" * 72)
    print("1. 1D PREFIX SUM ARRAY: O(N) BUILD, O(1) RANGE SUM QUERIES")
    print("=" * 72)
    daily_revenue = [120, 85, 200, 150, 95, 310, 140, 260]
    rsq = RangeSumQueryImmutable(daily_revenue)
    print(f"Daily Revenue (N={len(daily_revenue)}) : {daily_revenue}")
    print(f"Padded Prefix Array (N+1) : {rsq.prefix}\n")

    for L, R in [(0, 3), (2, 5), (0, 7), (4, 4)]:
        ans = rsq.query(L, R)
        assert ans == sum(daily_revenue[L : R + 1])
        print(f"  query({L}, {R}) = prefix[{R+1}] ({rsq.prefix[R+1]}) - prefix[{L}] ({rsq.prefix[L]}) = {ans}")

    print("\n" + "=" * 72)
    print("2. FIND PIVOT / EQUILIBRIUM INDEX IN O(N) TIME & O(1) SPACE")
    print("=" * 72)
    for sample in [[1, 7, 3, 6, 5, 6], [1, 2, 3], [2, 1, -1]]:
        p_idx = find_pivot_equilibrium_index(sample)
        print(f"  Array: {str(sample):<22} -> Pivot Index: {p_idx}")
