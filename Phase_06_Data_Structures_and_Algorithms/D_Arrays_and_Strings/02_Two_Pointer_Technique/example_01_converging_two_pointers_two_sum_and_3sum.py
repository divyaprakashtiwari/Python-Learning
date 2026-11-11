"""
Phase 6 - Data Structures and Algorithms
Section D: Arrays and Strings - Topic 02: Two Pointer Technique
Example 01: Opposite-Direction (Converging) Two Pointers (Two Sum II, Container With Most Water, 3Sum)

Demonstrates:
1. Two Sum II on a Sorted Array: `left = 0`, `right = n - 1` converging inward in O(N) time
   and O(1) auxiliary space (instead of O(N^2) nested loops or O(N) hash-map memory).
2. Container With Most Water (LeetCode 11): moving the pointer with the SHORTER wall inward
   in O(N) time.
3. 3Sum (Zero-Sum Triplets without Duplicates, LeetCode 15): sorting in O(N log N) and running
   converging two pointers for each anchor `i` in O(N^2) total time and O(1) auxiliary space.
"""


def two_sum_sorted(arr: list[int], target: int) -> tuple[int, int] | None:
    """
    Find 0-based indices `(left, right)` in sorted `arr` such that `arr[left] + arr[right] == target`.
    Time Complexity : O(N)
    Space Complexity: O(1)
    """
    left = 0
    right = len(arr) - 1

    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return left, right
        elif current_sum < target:
            left += 1   # Need a larger sum -> advance left pointer
        else:
            right -= 1  # Need a smaller sum -> retreat right pointer

    return None


def max_water_container(heights: list[int]) -> tuple[int, int, int]:
    """
    Find two vertical lines `(best_left, best_right)` that hold the maximum water area
    `(right - left) * min(heights[left], heights[right])` in O(N) time and O(1) space.
    """
    left = 0
    right = len(heights) - 1
    best_area = 0
    best_pair = (0, 0)

    while left < right:
        width = right - left
        h = min(heights[left], heights[right])
        area = width * h
        if area > best_area:
            best_area = area
            best_pair = (left, right)

        # Greedy invariant: moving the taller wall can NEVER increase `min(h_left, h_right)`,
        # so we MUST move the shorter wall inward!
        if heights[left] <= heights[right]:
            left += 1
        else:
            right -= 1

    return best_area, best_pair[0], best_pair[1]


def three_sum_zero(nums: list[int]) -> list[tuple[int, int, int]]:
    """
    Return all unique triplets `(a, b, c)` in `nums` such that `a + b + c == 0`.
    Time Complexity : O(N^2)
    Space Complexity: O(1) auxiliary (ignoring output list)
    """
    a = sorted(nums)
    n = len(a)
    triplets: list[tuple[int, int, int]] = []

    for i in range(n - 2):
        # Early stop: if smallest remaining number > 0, no three numbers can sum to 0!
        if a[i] > 0:
            break
        # Skip duplicate anchor values
        if i > 0 and a[i] == a[i - 1]:
            continue

        left = i + 1
        right = n - 1
        while left < right:
            total = a[i] + a[left] + a[right]
            if total == 0:
                triplets.append((a[i], a[left], a[right]))
                left += 1
                right -= 1
                # Skip duplicate left and right values
                while left < right and a[left] == a[left - 1]:
                    left += 1
                while left < right and a[right] == a[right + 1]:
                    right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1

    return triplets


if __name__ == "__main__":
    print("=" * 72)
    print("1. TWO SUM II ON SORTED ARRAY (O(N) TIME, O(1) SPACE)")
    print("=" * 72)
    sorted_prices = [12, 25, 34, 48, 60, 75, 90]
    print(f"Sorted Prices : {sorted_prices}")
    print(f"Target = 85   -> Indices: {two_sum_sorted(sorted_prices, 85)} (25 + 60 = 85)")

    print("\n" + "=" * 72)
    print("2. CONTAINER WITH MOST WATER (O(N) TWO POINTERS)")
    print("=" * 72)
    walls = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    area, l_idx, r_idx = max_water_container(walls)
    print(f"Wall Heights  : {walls}")
    print(f"Max Water Area: {area} between indices ({l_idx}, {r_idx}) [heights {walls[l_idx]} and {walls[r_idx]}]")

    print("\n" + "=" * 72)
    print("3. 3SUM UNIQUE ZERO-SUM TRIPLETS (O(N^2) TWO POINTERS)")
    print("=" * 72)
    sample_3sum = [-1, 0, 1, 2, -1, -4, -2, 3]
    print(f"Input Array   : {sample_3sum}")
    print(f"Zero Triplets : {three_sum_zero(sample_3sum)}")
