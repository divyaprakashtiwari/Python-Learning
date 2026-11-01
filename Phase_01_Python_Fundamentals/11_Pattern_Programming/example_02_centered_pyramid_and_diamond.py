"""
Topic 11: Pattern Programming
Example 02: Centered Pyramid and Symmetric Diamond Pattern

Demonstrates the mathematical relationship between leading spaces (`n - r`)
and odd star counts (`2 * r - 1`) in centered pyramids and diamonds.
"""


def print_centered_pyramid(n: int) -> None:
    print(f"=== 1. Centered Pyramid (n={n}) ===")
    for r in range(1, n + 1):
        spaces = " " * (n - r)
        stars = "*" * (2 * r - 1)
        print(f"{spaces}{stars}")


def print_symmetric_diamond(n: int) -> None:
    print(f"\n=== 2. Symmetric Diamond (half-height n={n}) ===")
    # Upper half (1 to n) + Lower half (n-1 down to 1)
    row_sequence = list(range(1, n + 1)) + list(range(n - 1, 0, -1))
    for r in row_sequence:
        spaces = " " * (n - r)
        stars = "*" * (2 * r - 1)
        print(f"{spaces}{stars}")


def main() -> None:
    print_centered_pyramid(5)
    print_symmetric_diamond(4)


if __name__ == "__main__":
    main()
