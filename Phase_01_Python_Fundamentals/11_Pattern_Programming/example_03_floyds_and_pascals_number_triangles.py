"""
Topic 11: Pattern Programming
Example 03: Number Patterns — Floyd's Triangle, Palindromic Pyramid & Pascal's Triangle

Demonstrates classic placement-interview number patterns using nested loops
and binomial recurrence.
"""


def print_floyds_triangle(rows: int) -> None:
    print(f"=== 1. Floyd's Triangle (rows={rows}) ===")
    counter = 1
    for r in range(1, rows + 1):
        row_nums = []
        for _ in range(r):
            row_nums.append(f"{counter:>2}")
            counter += 1
        print(" ".join(row_nums))


def print_palindromic_number_pyramid(n: int) -> None:
    print(f"\n=== 2. Palindromic Number Pyramid (n={n}) ===")
    for r in range(1, n + 1):
        leading_spaces = "  " * (n - r)
        ascending = [str(k) for k in range(1, r + 1)]
        descending = [str(k) for k in range(r - 1, 0, -1)]
        line = " ".join(ascending + descending)
        print(f"{leading_spaces}{line}")


def print_pascals_triangle(rows: int) -> None:
    print(f"\n=== 3. Pascal's Triangle (rows={rows}) ===")
    for r in range(rows):
        spaces = "  " * (rows - r - 1)
        val = 1
        row_values = []
        for c in range(r + 1):
            row_values.append(f"{val:>3}")
            val = val * (r - c) // (c + 1)
        print(f"{spaces}{' '.join(row_values)}")


def main() -> None:
    print_floyds_triangle(4)
    print_palindromic_number_pyramid(5)
    print_pascals_triangle(5)


if __name__ == "__main__":
    main()
