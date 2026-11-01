"""
Topic 08: Nested Data Structures
Example 01: 2D Matrices — Row/Column Sums, Diagonals, and 4-Directional Neighbors

Demonstrates fundamental 2D grid operations used in Matrix DSA problems:
primary/secondary diagonal extraction and valid neighbor coordinate generation.
"""


def get_valid_neighbors(grid: list[list[int]], r: int, c: int) -> list[tuple[int, int, int]]:
    """Return (row, col, value) for Up, Down, Left, Right neighbors within bounds."""
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    neighbors = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc, grid[nr][nc]))
    return neighbors


def main() -> None:
    matrix = [
        [10, 20, 30],
        [40, 50, 60],
        [70, 80, 90],
    ]
    n = len(matrix)

    # 1. Primary (r == c) and Secondary (r + c == n - 1) Diagonals
    primary_diag = [matrix[i][i] for i in range(n)]
    secondary_diag = [matrix[i][n - 1 - i] for i in range(n)]

    print("=== 1. 2D Matrix Diagonals & Row/Column Sums ===")
    print(f"Primary Diagonal   : {primary_diag} (Sum={sum(primary_diag)})")
    print(f"Secondary Diagonal : {secondary_diag} (Sum={sum(secondary_diag)})")
    print(f"Row Sums           : {[sum(row) for row in matrix]}")
    print(f"Column Sums        : {[sum(matrix[r][c] for r in range(n)) for c in range(n)]}")

    print("\n=== 2. 4-Directional Neighbors of Center Cell (1, 1) and Corner (0, 0) ===")
    print(f"Neighbors of (1, 1): {get_valid_neighbors(matrix, 1, 1)}")
    print(f"Neighbors of (0, 0): {get_valid_neighbors(matrix, 0, 0)}")


if __name__ == "__main__":
    main()
