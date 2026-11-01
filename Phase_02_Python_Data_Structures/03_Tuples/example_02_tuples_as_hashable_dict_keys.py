"""
Topic 03: Tuples
Example 02: Tuples as Hashable Dictionary Keys (2D Grid Coordinate Map)

Demonstrates why immutable tuples can serve as dictionary keys or set elements
(unlike lists) and explains what happens when a tuple contains a mutable list.
"""


def main() -> None:
    # 1. Sparse 2D Chessboard / Grid using (row, col) tuple keys
    grid_obstacles: dict[tuple[int, int], str] = {
        (0, 0): "Start Tower",
        (2, 4): "Laser Wall",
        (5, 7): "Goal Portal",
    }

    print("=== 1. Tuples as (row, col) Dictionary Keys ===")
    for coord in [(0, 0), (2, 4), (3, 3)]:
        feature = grid_obstacles.get(coord, "Empty Tile")
        print(f"  Coordinate {coord} -> {feature}")

    # 2. Tuple Methods: .count() and .index()
    grades = ("A", "B", "A", "C", "A", "B")
    print("\n=== 2. Tuple Built-in Methods (.count & .index) ===")
    print(f"Grades Tuple      : {grades}")
    print(f"Count of 'A'      : {grades.count('A')}")
    print(f"First index of 'B': {grades.index('B')}")

    # 3. Mutable Object Inside an Immutable Tuple
    print("\n=== 3. Mutable List Inside a Tuple ===")
    student_record = ("STU-101", ["Math", "Physics"])
    student_record[1].append("Computer Science")
    print(f"Updated inner list inside tuple: {student_record}")


if __name__ == "__main__":
    main()
