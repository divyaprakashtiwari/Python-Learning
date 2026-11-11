"""
Phase 6 - Data Structures and Algorithms
Section D: Arrays and Strings - Topic 04: Prefix Sum
Example 03: 2D Matrix Prefix Sum (Inclusion-Exclusion) & Difference Array for O(1) Range Updates

Demonstrates:
1. 2D Prefix Sum Matrix (Range Sum Query 2D Immutable, LeetCode 304):
   Precomputes `P[r + 1][c + 1]` in O(R * C) time so any rectangular sub-grid sum
   `(r1, c1) .. (r2, c2)` is answered in O(1) time via Inclusion-Exclusion:
   `rect_sum = P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]`.
2. 1D Difference Array (Dual of Prefix Sum):
   Applies `M` range-addition updates `add(L, R, delta)` in O(1) time per update
   (`diff[L] += delta; diff[R + 1] -= delta`), then reconstructs the final array in a
   single O(N) prefix-sum pass!
"""


class NumMatrix2DPrefixSum:
    """O(R * C) precomputation for O(1) 2D rectangular subgrid sum queries."""

    def __init__(self, matrix: list[list[int]]) -> None:
        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0
        self.pref = [[0] * (cols + 1) for _ in range(rows + 1)]

        for r in range(rows):
            for c in range(cols):
                self.pref[r + 1][c + 1] = (
                    matrix[r][c]
                    + self.pref[r][c + 1]
                    + self.pref[r + 1][c]
                    - self.pref[r][c]
                )

    def sum_region(self, r1: int, c1: int, r2: int, c2: int) -> int:
        """Return sum of rectangle `(r1, c1)` to `(r2, c2)` inclusive in O(1) time."""
        return (
            self.pref[r2 + 1][c2 + 1]
            - self.pref[r1][c2 + 1]
            - self.pref[r2 + 1][c1]
            + self.pref[r1][c1]
        )


def apply_range_updates_difference_array(
    n: int, updates: list[tuple[int, int, int]]
) -> list[int]:
    """
    Given an array of `n` zeros and a list of `(left, right, delta)` inclusive range
    additions, apply all updates in O(1) per update + O(n) final reconstruction!
    """
    diff = [0] * (n + 1)

    for left, right, delta in updates:
        diff[left] += delta
        diff[right + 1] -= delta

    # Reconstruct final array via prefix sum of `diff`
    result = [0] * n
    running = 0
    for i in range(n):
        running += diff[i]
        result[i] = running

    return result


if __name__ == "__main__":
    print("=" * 72)
    print("1. 2D MATRIX PREFIX SUM (O(1) RECTANGULAR SUBGRID QUERIES)")
    print("=" * 72)
    grid = [
        [3, 0, 1, 4, 2],
        [5, 6, 3, 2, 1],
        [1, 2, 0, 1, 5],
        [4, 1, 0, 1, 7],
    ]
    mat = NumMatrix2DPrefixSum(grid)
    print(f"Subgrid (1, 1) to (2, 2) [6+3+2+0]       -> Sum: {mat.sum_region(1, 1, 2, 2)}")
    print(f"Subgrid (1, 2) to (3, 4) [3+2+1+0+1+5+0+1+7] -> Sum: {mat.sum_region(1, 2, 3, 4)}")

    print("\n" + "=" * 72)
    print("2. DIFFERENCE ARRAY: O(1) BATCH RANGE ADDITION UPDATES")
    print("=" * 72)
    # LeetCode 370 Range Addition: n = 5, updates = [(1, 3, 2), (2, 4, 3), (0, 2, -2)]
    batch_updates = [(1, 3, 2), (2, 4, 3), (0, 2, -2)]
    final_arr = apply_range_updates_difference_array(5, batch_updates)
    print(f"Updates on N=5 zeros: {batch_updates}")
    print(f"Final Reconstructed : {final_arr}")
