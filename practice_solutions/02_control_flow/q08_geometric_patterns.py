"""
Topic 02 - Control Flow
Practice Question 8 Solution: Geometric ASCII Pattern Generator

Problem Statement:
1. Symmetric Hollow Diamond:
   - Given odd integer width n >= 3, generates an n x n hollow diamond.
   - Peak and bottom tips have single asterisk centered at index n // 2.
2. Alternating Binary Floyd's Triangle:
   - Given height h >= 1, prints h rows where cell (r, c) is 1 if (r + c) is even, 0 otherwise.
"""


def generate_hollow_diamond(n: int) -> str:
    """Constructs a symmetric hollow diamond of width n using nested loop logic."""
    if not isinstance(n, int) or n < 3 or n % 2 == 0:
        raise ValueError("Diamond width must be an odd integer >= 3")

    mid = n // 2
    lines = []

    for r in range(n):
        dist = abs(mid - r)
        outer_spaces = " " * dist

        if dist == mid:
            # Top tip or bottom tip
            lines.append(f"{outer_spaces}*")
        else:
            inner_spaces = " " * (n - 2 * dist - 2)
            lines.append(f"{outer_spaces}*{inner_spaces}*")

    return "\n".join(lines)


def generate_binary_triangle(h: int) -> str:
    """Generates an alternating binary triangle of height h."""
    if not isinstance(h, int) or h < 1:
        raise ValueError("Height must be an integer >= 1")

    lines = []
    for r in range(1, h + 1):
        row_cells = []
        for c in range(1, r + 1):
            cell_val = 1 if (r + c) % 2 == 0 else 0
            row_cells.append(str(cell_val))
        lines.append(" ".join(row_cells))

    return "\n".join(lines)


def main() -> None:
    width = 7
    height = 5

    diamond_art = generate_hollow_diamond(width)
    triangle_art = generate_binary_triangle(height)

    print(f"--- Hollow Diamond (n={width}) ---")
    print(diamond_art)
    print(f"\n--- Alternating Binary Triangle (h={height}) ---")
    print(triangle_art)


if __name__ == "__main__":
    main()
