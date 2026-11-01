"""
Topic 11: Pattern Programming
Example 01: Right-Angled Triangle, Inverted Triangle, and Hollow Square

Demonstrates how outer loops control rows (`r`) and inner expressions/loops
control columns (`c`) to build foundational geometric star patterns.
"""


def print_right_triangle(rows: int) -> None:
    print(f"=== 1. Right-Angled Star Triangle (n={rows}) ===")
    for r in range(1, rows + 1):
        print("* " * r)


def print_inverted_triangle(rows: int) -> None:
    print(f"\n=== 2. Inverted Star Triangle (n={rows}) ===")
    for r in range(rows, 0, -1):
        print("* " * r)


def print_hollow_square(size: int) -> None:
    print(f"\n=== 3. Hollow Square Frame ({size}x{size}) ===")
    for r in range(1, size + 1):
        row_chars = []
        for c in range(1, size + 1):
            # Border condition: first/last row OR first/last column
            if r in (1, size) or c in (1, size):
                row_chars.append("*")
            else:
                row_chars.append(" ")
        print(" ".join(row_chars))


def main() -> None:
    print_right_triangle(5)
    print_inverted_triangle(5)
    print_hollow_square(5)


if __name__ == "__main__":
    main()
