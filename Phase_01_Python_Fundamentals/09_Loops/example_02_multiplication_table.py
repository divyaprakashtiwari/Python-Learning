"""
Topic 09: Loops (for, while)
Example 02: Multiplication Table Generator (Single Loop & Nested 2D Grid)

Demonstrates a standard multiplication table using a `for` loop and a 5x5
multiplication matrix using nested `for` loops.
"""


def print_single_table(number: int, limit: int = 10) -> None:
    print(f"=== Multiplication Table of {number} ===")
    for multiplier in range(1, limit + 1):
        product = number * multiplier
        print(f"  {number:>2} x {multiplier:>2} = {product:>3}")


def print_multiplication_grid(size: int = 5) -> None:
    print(f"\n=== {size}x{size} Nested Loop Multiplication Grid ===")
    header = "    | " + " ".join(f"{col:>3}" for col in range(1, size + 1))
    print(header)
    print("-" * len(header))
    for row in range(1, size + 1):
        row_cells = " ".join(f"{row * col:>3}" for col in range(1, size + 1))
        print(f" {row:>2} | {row_cells}")


def main() -> None:
    print_single_table(7, limit=10)
    print_multiplication_grid(size=5)


if __name__ == "__main__":
    main()
