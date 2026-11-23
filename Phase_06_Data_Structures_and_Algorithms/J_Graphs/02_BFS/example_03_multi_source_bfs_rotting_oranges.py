"""
Phase 6 - Section J.02: BFS (Breadth-First Search)
Example 03: Multi-Source BFS (Rotting Oranges)

Demonstrating:
1. Multi-source BFS initializing the queue with multiple simultaneous roots.
2. Rotting Oranges (minimum minutes until all fresh oranges rot).
3. 2D grid matrix wavefront expansion.
"""

from collections import deque


def oranges_rotting(grid):
    """
    0 = Empty cell
    1 = Fresh orange
    2 = Rotten orange
    Every minute, any fresh orange 4-directionally adjacent to a rotten orange rots.
    Returns minimum minutes until no fresh orange remains, or -1 if impossible.
    Time Complexity: O(R * C)
    Space Complexity: O(R * C)
    """
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh_count = 0

    # Step 1: Enqueue all initially rotten oranges (multi-source roots)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))  # (row, col, minute)
            elif grid[r][c] == 1:
                fresh_count += 1

    if fresh_count == 0:
        return 0

    minutes_elapsed = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Step 2: Multi-source BFS wavefront expansion
    while queue:
        r, c, time = queue.popleft()
        minutes_elapsed = time

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2  # Orange rots
                fresh_count -= 1
                queue.append((nr, nc, time + 1))

    return minutes_elapsed if fresh_count == 0 else -1


def main():
    print("=" * 60)
    print("Multi-Source BFS: Rotting Oranges Simulation")
    print("=" * 60)

    # Grid 1: All fresh oranges can rot
    # [2, 1, 1]
    # [1, 1, 0]
    # [0, 1, 1]
    grid1 = [
        [2, 1, 1],
        [1, 1, 0],
        [0, 1, 1]
    ]
    print("Grid 1 Initial State:")
    for row in grid1:
        print(" ", row)

    ans1 = oranges_rotting(grid1)
    print("Minutes to rot all oranges:", ans1)

    # Grid 2: Impossible due to isolated fresh orange
    # [2, 1, 1]
    # [0, 1, 1]
    # [1, 0, 1]
    grid2 = [
        [2, 1, 1],
        [0, 1, 1],
        [1, 0, 1]
    ]
    print("\nGrid 2 Initial State (Impossible corner):")
    for row in grid2:
        print(" ", row)

    ans2 = oranges_rotting(grid2)
    print("Minutes to rot all oranges:", ans2)


if __name__ == "__main__":
    main()
