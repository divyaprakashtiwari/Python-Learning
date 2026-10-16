"""
Topic 02: Control Flow
Question 08: Pattern Printing and Geometric Loops

Master loops for spatial logic and geometric pattern generation: triangles,
pyramids, hollow diamonds, Floyd's triangle, alternating binary grids,
hourglasses, spiral matrices, alphabet rangoli, and checkerboards.
"""

# ============================================================
# Q1: Right-Angled and Inverted Triangles
# ============================================================
# Question: Print left-aligned upright and inverted star triangles of height N
# using loop index calculations.

print("=== Q1: Right-Angled and Inverted Triangles ===")

def print_triangles(n: int):
    print(f"  Upright Triangle (N={n}):")
    for i in range(1, n + 1):
        print("    " + "* " * i)
        
    print(f"\n  Inverted Triangle (N={n}):")
    for i in range(n, 0, -1):
        print("    " + "* " * i)

print_triangles(4)

# Explanation: Upright triangle prints $i$ stars on row $i$ where $1 \le i \le n$.
# Inverted triangle counts backwards from $n$ down to 1.


# ============================================================
# Q2: Centered Symmetrical Pyramid
# ============================================================
# Question: Print a centered symmetrical pyramid of height N.
# Each row $i$ contains $(N - i - 1)$ leading spaces and $(2i + 1)$ stars.

print("\n=== Q2: Centered Symmetrical Pyramid ===")

def print_pyramid(n: int):
    print(f"  Centered Pyramid (N={n}):")
    for i in range(n):
        spaces = "  " * (n - i - 1)
        stars = "* " * (2 * i + 1)
        print("    " + spaces + stars)

print_pyramid(5)

# Explanation: Symmetrical centered alignment requires coordinating leading whitespace
# with odd-numbered star counts ($2i + 1 = 1, 3, 5, 7, 9$).


# ============================================================
# Q3: Solid and Hollow Diamonds
# ============================================================
# Question: Print a solid diamond and a hollow diamond (stars only on the border)
# of radius N.

print("\n=== Q3: Solid and Hollow Diamonds ===")

def print_hollow_diamond(n: int):
    """Prints hollow diamond of radius n (2n - 1 total rows)."""
    print(f"  Hollow Diamond (N={n}):")
    
    # Upper half (including center row)
    for i in range(n):
        outer_spaces = " " * (n - i - 1)
        if i == 0:
            print("    " + outer_spaces + "*")
        else:
            inner_spaces = " " * (2 * i - 1)
            print("    " + outer_spaces + "*" + inner_spaces + "*")
            
    # Lower half
    for i in range(n - 2, -1, -1):
        outer_spaces = " " * (n - i - 1)
        if i == 0:
            print("    " + outer_spaces + "*")
        else:
            inner_spaces = " " * (2 * i - 1)
            print("    " + outer_spaces + "*" + inner_spaces + "*")

print_hollow_diamond(5)

# Explanation: Hollow patterns compute both outer padding and interior cavity spacing.
# Edge rows ($i = 0$) emit a single vertex star; internal rows emit two boundary stars.


# ============================================================
# Q4: Floyd's Consecutive Number Triangle
# ============================================================
# Question: Print Floyd's Triangle where integers from 1 upwards are laid out
# sequentially in rows of increasing width.

print("\n=== Q4: Floyd's Number Triangle ===")

def print_floyds_triangle(rows: int):
    """Prints Floyd's number triangle."""
    print(f"  Floyd's Triangle ({rows} rows):")
    current_num = 1
    
    for r in range(1, rows + 1):
        row_values = []
        for _ in range(r):
            row_values.append(f"{current_num:>3}")
            current_num += 1
        print("    " + " ".join(row_values))

print_floyds_triangle(5)

# Explanation: Floyd's triangle maintains a persistent global counter that increments
# continuously across both inner and outer loops.


# ============================================================
# Q5: Alternating Binary Triangle (0 and 1 Grid)
# ============================================================
# Question: Print a triangle where cells alternate between 1 and 0
# based on row and column parity: cell(r, c) = (r + c) % 2.

print("\n=== Q5: Alternating Binary Triangle ===")

def print_binary_triangle(rows: int):
    print(f"  Binary Triangle ({rows} rows):")
    for r in range(1, rows + 1):
        row_str = []
        for c in range(1, r + 1):
            val = (r + c) % 2  # Parity sum
            row_str.append(str(val))
        print("    " + " ".join(row_str))

print_binary_triangle(6)

# Explanation: When $(r + c)$ is even, $(r + c) \% 2 = 0$; when odd, it equals 1.
# This produces an alternating checkerboard pattern across triangular bounds.


# ============================================================
# Q6: Hourglass / Sandglass Pattern
# ============================================================
# Question: Print an Hourglass pattern: an inverted pyramid joined at its vertex
# to an upright pyramid.

print("\n=== Q6: Hourglass Pattern ===")

def print_hourglass(n: int):
    print(f"  Hourglass Pattern (N={n}):")
    # Top inverted half
    for i in range(n, 0, -1):
        spaces = " " * (n - i)
        stars = "* " * i
        print("    " + spaces + stars)
    # Bottom upright half (start from 2 to avoid duplicate center vertex)
    for i in range(2, n + 1):
        spaces = " " * (n - i)
        stars = "* " * i
        print("    " + spaces + stars)

print_hourglass(4)

# Explanation: An hourglass joins two mirrored triangles. Starting the lower loop
# at $i=2$ prevents duplicating the single vertex point at the waist.


# ============================================================
# Q7: Palindromic Number Pyramid
# ============================================================
# Question: Print a pyramid of palindromic numbers:
# row 1: 1; row 2: 1 2 1; row 3: 1 2 3 2 1; row 4: 1 2 3 4 3 2 1.

print("\n=== Q7: Palindromic Number Pyramid ===")

def print_palindrome_pyramid(n: int):
    print(f"  Palindromic Number Pyramid (N={n}):")
    for i in range(1, n + 1):
        spaces = "  " * (n - i)
        # Ascending: 1 to i
        asc = [str(x) for x in range(1, i + 1)]
        # Descending: i-1 down to 1
        desc = [str(x) for x in range(i - 1, 0, -1)]
        print("    " + spaces + " ".join(asc + desc))

print_palindrome_pyramid(5)

# Explanation: Palindromic rows concatenate an ascending integer range $[1 \dots i]$
# with a descending range $[i-1 \dots 1]$.


# ============================================================
# Q8: Clockwise Spiral Matrix Generator
# ============================================================
# Question: Fill an N x N matrix with integers 1 to N^2 in a clockwise spiral
# using four-boundary while/for loop coordinates and format the resulting grid.

print("\n=== Q8: Clockwise Spiral Matrix ===")

def generate_spiral_matrix(n: int) -> list[list[int]]:
    """Fills an N x N matrix with 1..N^2 in spiral order."""
    matrix = [[0] * n for _ in range(n)]
    top, bottom = 0, n - 1
    left, right = 0, n - 1
    num = 1
    
    while top <= bottom and left <= right:
        # Traverse Left to Right along Top row
        for c in range(left, right + 1):
            matrix[top][c] = num
            num += 1
        top += 1
        
        # Traverse Top to Bottom along Right column
        for r in range(top, bottom + 1):
            matrix[r][right] = num
            num += 1
        right -= 1
        
        # Traverse Right to Left along Bottom row
        if top <= bottom:
            for c in range(right, left - 1, -1):
                matrix[bottom][c] = num
                num += 1
            bottom -= 1
            
        # Traverse Bottom to Top along Left column
        if left <= right:
            for r in range(bottom, top - 1, -1):
                matrix[r][left] = num
                num += 1
            left += 1
            
    return matrix

spiral = generate_spiral_matrix(5)
print("  5x5 Spiral Grid:")
for row in spiral:
    print("    [ " + " ".join(f"{x:>3}" for x in row) + " ]")

# Explanation: Four boundary pointers (top, bottom, left, right) contract inward
# after each directional sweep until all $N^2$ cells are populated.


# ============================================================
# Q9: Alphabet Rangoli / Diamond Pattern
# ============================================================
# Question: Print an alphabet rangoli pattern of size N where characters
# expand outward and contract back to 'a' joined by hyphens.

print("\n=== Q9: Alphabet Rangoli ===")

def print_alphabet_rangoli(size: int):
    """Generates an alphabet rangoli of given size."""
    import string
    alphabet = string.ascii_lowercase
    lines = []
    
    for i in range(size):
        # Letters from size-1 down to size-1-i, then back up
        left_side = [alphabet[size - 1 - j] for j in range(i + 1)]
        full_row = left_side + left_side[:-1][::-1]
        lines.append("-".join(full_row))
        
    width = len(lines[-1])
    
    print(f"  Rangoli Pattern (Size {size}):")
    # Top half + center
    for line in lines:
        print("    " + line.center(width, "-"))
    # Bottom inverted half
    for line in reversed(lines[:-1]):
        print("    " + line.center(width, "-"))

print_alphabet_rangoli(4)

# Explanation: `str.center(width, '-')` pads symmetric character strings evenly,
# producing a diamond aesthetic across alphabet slices.


# ============================================================
# Q10: Scalable Checkerboard / Chessboard Grid
# ============================================================
# Question: Render an 8x8 chessboard pattern with cell blocks of size K x K
# using alternating characters ('#' and ' ').

print("\n=== Q10: Scalable Checkerboard Grid ===")

def render_checkerboard(grid_size: int = 8, cell_width: int = 2):
    """Renders checkerboard grid with custom square block dimensions."""
    print(f"  Chessboard Grid ({grid_size}x{grid_size}, cell scale {cell_width}x{cell_width}):")
    
    # Border
    border = "  +" + "---" * grid_size + "+"
    print("  " + border)
    
    for r in range(grid_size):
        row_str = "  |"
        for c in range(grid_size):
            # If (r + c) is even -> dark square, odd -> light square
            tile = "## " if (r + c) % 2 == 0 else "   "
            row_str += tile
        row_str += "|"
        print(row_str)
        
    print("  " + border)

render_checkerboard(8)

# Summary Output
print("\n" + "=" * 55)
print("  All 10 Questions for Topic 02 - Q08 executed successfully!")
print("=" * 55)
