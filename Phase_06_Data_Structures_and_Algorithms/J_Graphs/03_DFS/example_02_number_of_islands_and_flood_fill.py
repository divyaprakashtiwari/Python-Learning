"""
Example 02: 2D Grid DFS - Number of Islands, Max Area, and Flood Fill

Demonstrates:
1. Number of Islands (LeetCode 200): Counting connected components in a 2D binary grid.
2. Max Area of Island (LeetCode 695): Finding the size of the largest component.
3. Flood Fill (LeetCode 733): In-place color replacement using depth-first search.

Time Complexity: O(R * C) where R is rows and C is columns.
Space Complexity: O(R * C) worst case for recursion call stack in a dense grid.
"""

from typing import List


class GridGraphDFS:
    @staticmethod
    def num_islands(grid: List[List[str]]) -> int:
        """Counts the number of distinct islands ('1' surrounded by '0')."""
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        island_count = 0

        # We copy the grid to avoid mutating the original input
        g = [row[:] for row in grid]

        def _dfs(r: int, c: int) -> None:
            # Boundary checks and water check
            if r < 0 or r >= rows or c < 0 or c >= cols or g[r][c] != "1":
                return
            # Sink the island cell to mark as visited
            g[r][c] = "0"
            # 4-directional traversal
            _dfs(r + 1, c)
            _dfs(r - 1, c)
            _dfs(r, c + 1)
            _dfs(r, c - 1)

        for r in range(rows):
            for c in range(cols):
                if g[r][c] == "1":
                    island_count += 1
                    _dfs(r, c)

        return island_count

    @staticmethod
    def max_area_of_island(grid: List[List[int]]) -> int:
        """Calculates the maximum area (number of connected 1s) of an island."""
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        visited = set()

        def _dfs(r: int, c: int) -> int:
            if (
                r < 0
                or r >= rows
                or c < 0
                or c >= cols
                or grid[r][c] == 0
                or (r, c) in visited
            ):
                return 0

            visited.add((r, c))
            area = 1
            area += _dfs(r + 1, c)
            area += _dfs(r - 1, c)
            area += _dfs(r, c + 1)
            area += _dfs(r, c - 1)
            return area

        max_area = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1 and (r, c) not in visited:
                    max_area = max(max_area, _dfs(r, c))

        return max_area

    @staticmethod
    def flood_fill(
        image: List[List[int]], sr: int, sc: int, color: int
    ) -> List[List[int]]:
        """Fills matching adjacent cells with a replacement color."""
        rows, cols = len(image), len(image[0])
        initial_color = image[sr][sc]

        if initial_color == color:
            return image

        res = [row[:] for row in image]

        def _dfs(r: int, c: int) -> None:
            if (
                r < 0
                or r >= rows
                or c < 0
                or c >= cols
                or res[r][c] != initial_color
            ):
                return
            res[r][c] = color
            _dfs(r + 1, c)
            _dfs(r - 1, c)
            _dfs(r, c + 1)
            _dfs(r, c - 1)

        _dfs(sr, sc)
        return res


def main() -> None:
    print("=" * 60)
    print("1. Number of Islands (LeetCode 200)")
    print("=" * 60)

    sea_grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]

    print("Input Grid:")
    for row in sea_grid:
        print(" ", " ".join(row))

    islands = GridGraphDFS.num_islands(sea_grid)
    print(f"Total Islands Count: {islands}")

    print("\n" + "=" * 60)
    print("2. Max Area of Island (LeetCode 695)")
    print("=" * 60)

    area_grid = [
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    ]

    max_area = GridGraphDFS.max_area_of_island(area_grid)
    print(f"Maximum Connected Island Area: {max_area}")

    print("\n" + "=" * 60)
    print("3. Flood Fill Algorithm (LeetCode 733)")
    print("=" * 60)

    canvas = [
        [1, 1, 1],
        [1, 1, 0],
        [1, 0, 1],
    ]
    print("Initial Canvas (Color 1 at (1, 1)):")
    for row in canvas:
        print(" ", row)

    filled = GridGraphDFS.flood_fill(canvas, sr=1, sc=1, color=2)
    print("After Flood Fill with color 2:")
    for row in filled:
        print(" ", row)


if __name__ == "__main__":
    main()
