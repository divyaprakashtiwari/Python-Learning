"""
Phase 6 - Data Structures and Algorithms
Section F: Stacks and Queues
Topic 05: Monotonic Stack
Example 02: Largest Rectangle in Histogram (LeetCode 84) & Trapping Rain Water (LeetCode 42)

Two iconic Hard interview problems solved in a single O(n) pass via Monotonic Stack:

1. Largest Rectangle in Histogram (LeetCode 84 — Monotonic Increasing Stack):
   - Every bar `h = heights[mid]` can extend its rectangle leftward and rightward
     until it hits the **first bar strictly shorter than `h`** on the left (`left_bound`)
     and on the right (`right_bound`).
   - Using a **Monotonic Increasing Stack** with a trailing `0` sentinel bar:
     whenever `heights[i] < heights[stack[-1]]`, we pop `mid = stack.pop()`:
       - Its right boundary (first smaller to the right) is `i`.
       - Its left boundary (first smaller to the left) is `stack[-1]` (or `-1` if empty).
       - Its maximum width is `i - stack[-1] - 1`, giving area `heights[mid] * width`!

2. Trapping Rain Water (LeetCode 42 — Horizontal Layer-by-Layer Monotonic Decreasing Stack):
   - Whenever a bar `height[right]` is taller than `height[stack[-1]]`, the popped
     bar `bottom = stack.pop()` forms a valley floor bounded on the left by `left = stack[-1]`
     and on the right by `right`, trapping water of height
     `min(height[left], height[right]) - height[bottom]` and width `right - left - 1`!
"""

from typing import List, Tuple


def largest_rectangle_in_histogram(heights: List[int]) -> Tuple[int, Tuple[int, int, int]]:
    """
    Computes the area of the largest rectangle in `heights` in O(n) time using a
    monotonic increasing stack with a trailing 0-height sentinel.
    Returns `(max_area, (best_height, left_idx, right_idx_inclusive))`.
    """
    max_area = 0
    best_rect = (0, 0, -1)
    stack: List[int] = []  # Monotonic increasing stack of bar indices
    extended = heights + [0]  # Trailing 0 flushes all remaining bars at the end

    for right_bound, h in enumerate(extended):
        while stack and extended[stack[-1]] > h:
            mid = stack.pop()
            rect_height = extended[mid]
            left_bound = stack[-1] if stack else -1
            width = right_bound - left_bound - 1
            area = rect_height * width
            if area > max_area:
                max_area = area
                best_rect = (rect_height, left_bound + 1, right_bound - 1)
        stack.append(right_bound)

    return max_area, best_rect


def trap_rain_water_monotonic_stack(height: List[int]) -> int:
    """
    Computes total trapped rain water in O(n) time by accumulating horizontal
    water layers whenever a rising right wall closes a valley (LeetCode 42).
    """
    total_water = 0
    stack: List[int] = []  # Monotonic decreasing stack of indices

    for right, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = stack.pop()
            if not stack:
                break  # No left wall to hold water
            left = stack[-1]
            bounded_height = min(height[left], h) - height[bottom]
            width = right - left - 1
            total_water += bounded_height * width
        stack.append(right)

    return total_water


if __name__ == "__main__":
    print("=" * 72)
    print("1. Largest Rectangle in Histogram in O(n) Time (LeetCode 84 Hard)")
    print("=" * 72)
    histograms = [
        [2, 1, 5, 6, 2, 3],
        [2, 4],
        [6, 2, 5, 4, 5, 1, 6],
    ]
    for hist in histograms:
        area, (bh, l_idx, r_idx) = largest_rectangle_in_histogram(hist)
        print(
            f"  Heights: {str(hist):<24} -> Max Area = {area:>2} "
            f"(height={bh} across indices [{l_idx}..{r_idx}])"
        )

    print("\n" + "=" * 72)
    print("2. Trapping Rain Water via Horizontal Valley Layers (LeetCode 42 Hard)")
    print("=" * 72)
    elevations = [
        [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],
        [4, 2, 0, 3, 2, 5],
    ]
    for elev in elevations:
        print(f"  Elevation Map: {str(elev):<38} -> Trapped Water = {trap_rain_water_monotonic_stack(elev)}")

