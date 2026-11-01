"""
Topic 02: Lists
Example 03: List Aliasing vs Copying and the 2D Grid Multiplication Trap

Demonstrates:
1. Why `b = a` creates an alias (both names point to the same list).
2. Why `[[0] * cols] * rows` creates shared row references and how to initialize
   a 2D matrix safely with a list comprehension.
"""


def main() -> None:
    print("=== 1. Reference Aliasing (`b = a`) vs Shallow Copy (`a.copy()`) ===")
    original = [10, 20, 30]
    alias = original
    safe_copy = original.copy()

    alias.append(40)
    print(f"Original after alias.append(40) : {original}")
    print(f"Safe Copy (unaffected)          : {safe_copy}")

    print("\n=== 2. The Classic 2D Grid Trap: [[0] * 3] * 3 ===")
    buggy_grid = [[0] * 3] * 3
    buggy_grid[0][0] = 99
    print(f"Buggy Grid after setting [0][0]=99 (ALL rows mutated!):")
    for row in buggy_grid:
        print(f"  {row}")

    print("\n=== 3. Safe 2D Grid Initialization: [[0] * 3 for _ in range(3)] ===")
    safe_grid = [[0] * 3 for _ in range(3)]
    safe_grid[0][0] = 99
    print(f"Safe Grid after setting [0][0]=99 (Only row 0 mutated):")
    for row in safe_grid:
        print(f"  {row}")


if __name__ == "__main__":
    main()
