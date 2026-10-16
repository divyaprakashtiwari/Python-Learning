"""
Topic 02: Control Flow
Question 06: Nested Loops

Master multi-dimensional iteration: matrix multiplication, Cartesian products,
sorting algorithms (Bubble Sort), Pascal's Triangle, 2D convolution filters,
matrix transpositions, co-occurrence heatmaps, and cellular automata.
"""

# ============================================================
# Q1: Formatted Multiplication Table Grid
# ============================================================
# Question: Generate a formatted, cleanly aligned N x M multiplication table
# using nested loops with headers and separators.

print("=== Q1: Multiplication Table Grid ===")

def print_multiplication_table(rows: int, cols: int):
    """Prints aligned multiplication table."""
    # Header row
    header = "     |" + "".join(f"{c:>5}" for c in range(1, cols + 1))
    print(header)
    print("-----+" + "-----" * cols)
    
    # Outer loop: rows
    for r in range(1, rows + 1):
        row_str = f"{r:>4} |"
        # Inner loop: columns
        for c in range(1, cols + 1):
            row_str += f"{r * c:>5}"
        print(row_str)

print_multiplication_table(5, 6)

# Explanation: The outer loop controls row advancement, while the inner loop
# computes and concatenates cell values across that specific row.


# ============================================================
# Q2: Matrix Multiplication Algorithm
# ============================================================
# Question: Implement matrix multiplication A (M x K) and B (K x N) from scratch
# using 3 nested loops: validate dimensions and compute dot products.

print("\n=== Q2: Matrix Multiplication ===")

def multiply_matrices(matrix_a: list[list[float]], matrix_b: list[list[float]]) -> list[list[float]]:
    """Multiplies two matrices using standard O(N^3) triple nested loops."""
    rows_a = len(matrix_a)
    cols_a = len(matrix_a[0])
    rows_b = len(matrix_b)
    cols_b = len(matrix_b[0])
    
    if cols_a != rows_b:
        raise ValueError(f"Incompatible dimensions: ({rows_a}x{cols_a}) and ({rows_b}x{cols_b})")
        
    # Initialize product matrix with zeros of size rows_a x cols_b
    result = [[0.0 for _ in range(cols_b)] for _ in range(rows_a)]
    
    # Triple nested loops
    for i in range(rows_a):            # Row of A
        for j in range(cols_b):        # Column of B
            dot_product = 0.0
            for k in range(cols_a):    # Element index across row A and column B
                dot_product += matrix_a[i][k] * matrix_b[k][j]
            result[i][j] = dot_product
            
    return result

mat1 = [
    [1, 2, 3],
    [4, 5, 6]
]  # 2 x 3

mat2 = [
    [7, 8],
    [9, 1],
    [2, 3]
]  # 3 x 2

product = multiply_matrices(mat1, mat2)
print("  Product Matrix (2x2):")
for r in product:
    print(f"    [ {r[0]:>5.1f}, {r[1]:>5.1f} ]")

# Explanation: Dimension rule: `Cols(A) == Rows(B)`. The output has shape `Rows(A) x Cols(B)`.
# Time complexity is $O(M \times K \times N)$.


# ============================================================
# Q3: Cartesian Product Combinations Generator
# ============================================================
# Question: Given multiple attribute lists (colors, sizes, fabrics), generate all
# possible product SKU combinations using nested loops without external libraries.

print("\n=== Q3: Cartesian Product Generator ===")

colors = ["Red", "Navy", "Emerald"]
sizes = ["S", "M", "L"]
fabrics = ["Cotton", "Silk"]

catalog = []
for color in colors:
    for size in sizes:
        for fabric in fabrics:
            sku = f"{color[:2].upper()}-{size}-{fabric[:3].upper()}"
            catalog.append({"color": color, "size": size, "fabric": fabric, "sku": sku})

print(f"  Generated {len(catalog)} combinations (3 colors * 3 sizes * 2 fabrics):")
for item in catalog[:6]:  # Display first 6
    print(f"    SKU: {item['sku']:<10} -> {item['color']:<7} | Size: {item['size']:<2} | {item['fabric']}")
print("    ...")

# Explanation: Nested loops compute the Cartesian product $S_1 \times S_2 \times \dots \times S_k$,
# yielding $|S_1| \times |S_2| \times \dots \times |S_k|$ total combinations.


# ============================================================
# Q4: Optimized Bubble Sort Algorithm
# ============================================================
# Question: Implement Bubble Sort using nested loops. Optimize by tracking whether
# any swaps occurred during a pass, terminating early if the list is already sorted.

print("\n=== Q4: Optimized Bubble Sort ===")

def bubble_sort(arr: list[int]) -> tuple[list[int], int, int]:
    """Sorts array using optimized bubble sort. Returns (sorted_arr, comparisons, swaps)."""
    items = list(arr)
    n = len(items)
    comparisons = 0
    swaps = 0
    
    # Outer loop: passes
    for i in range(n):
        swapped = False
        # Inner loop: adjacent comparisons up to unsorted boundary
        for j in range(0, n - 1 - i):
            comparisons += 1
            if items[j] > items[j + 1]:
                # Swap elements
                items[j], items[j + 1] = items[j + 1], items[j]
                swaps += 1
                swapped = True
                
        # If no swaps occurred during the entire pass, array is already sorted!
        if not swapped:
            break
            
    return items, comparisons, swaps

sample_arr = [64, 34, 25, 12, 22, 11, 90]
sorted_res, comps, swps = bubble_sort(sample_arr)
print(f"  Original:    {sample_arr}")
print(f"  Sorted:      {sorted_res}")
print(f"  Comparisons: {comps} | Swaps: {swps}")

# Pre-sorted array shows early termination
presorted = [1, 2, 3, 4, 5, 6]
_, comps_early, _ = bubble_sort(presorted)
print(f"  Pre-sorted early termination comparisons: {comps_early} (O(N) best case)")

# Explanation: Tracking the `swapped` flag turns $O(N^2)$ worst-case Bubble Sort
# into an $O(N)$ adaptive sort on already sorted data.


# ============================================================
# Q5: Pair Sum Finding Without Duplicate Pairs
# ============================================================
# Question: Given an array of integers and a target sum, use nested loops to find all
# unique index pairs (i, j) where i < j such that arr[i] + arr[j] == target.

print("\n=== Q5: Unique Pair Sum Finder ===")

def find_target_pairs(arr: list[int], target: int) -> list[tuple[int, int, int, int]]:
    """Finds all pairs summing to target with i < j."""
    n = len(arr)
    pairs = []
    
    for i in range(n):
        for j in range(i + 1, n):  # Start at i + 1 to avoid self-pairs and duplicates
            if arr[i] + arr[j] == target:
                pairs.append((i, j, arr[i], arr[j]))
                
    return pairs

numbers = [2, 7, 11, 15, 3, 6, 8, 1, 9]
target_sum = 10
found_pairs = find_target_pairs(numbers, target_sum)

print(f"  Array: {numbers} | Target: {target_sum}")
for i, j, v1, v2 in found_pairs:
    print(f"    Indices ({i}, {j}): {v1} + {v2} = {target_sum}")

# Explanation: Starting the inner loop at `i + 1` ensures:
# 1. An element is never paired with itself ($i \neq j$).
# 2. Every pair is evaluated exactly once in canonical order ($i < j$).


# ============================================================
# Q6: Pascal's Triangle Generator
# ============================================================
# Question: Generate the first N rows of Pascal's Triangle using nested loops.
# Each entry is the sum of the two values directly above it.

print("\n=== Q6: Pascal's Triangle Generator ===")

def generate_pascals_triangle(num_rows: int) -> list[list[int]]:
    """Generates Pascal's triangle rows iteratively."""
    if num_rows <= 0:
        return []
        
    triangle = []
    
    for r in range(num_rows):
        row = [1] * (r + 1)  # First and last elements are always 1
        
        # Calculate inner values
        for c in range(1, r):
            row[c] = triangle[r - 1][c - 1] + triangle[r - 1][c]
            
        triangle.append(row)
        
    return triangle

triangle_rows = generate_pascals_triangle(6)
for row in triangle_rows:
    row_text = " ".join(f"{num:^3}" for num in row)
    print(f"    {row_text:^30}")

# Explanation: Row $r$ has $r + 1$ elements. The inner loop fills interior cells
# using recurrence $T(r, c) = T(r-1, c-1) + T(r-1, c)$.


# ============================================================
# Q7: 2D Spatial Convolution / Smoothing Filter
# ============================================================
# Question: Apply a 3x3 average blur kernel to a 2D intensity grid using 4 nested loops:
# outer 2 loops iterate image pixels, inner 2 loops iterate the kernel window.

print("\n=== Q7: 2D Image Smoothing Convolution ===")

def apply_box_blur_3x3(image: list[list[float]]) -> list[list[float]]:
    """Applies a 3x3 uniform box blur filter across a 2D image matrix."""
    height = len(image)
    width = len(image[0])
    blurred = [[0.0 for _ in range(width)] for _ in range(height)]
    
    # Outer loops: image pixel coordinates (r, c)
    for r in range(height):
        for c in range(width):
            pixel_sum = 0.0
            sample_count = 0
            
            # Inner loops: 3x3 kernel offsets [-1, 0, 1]
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr = r + dr
                    nc = c + dc
                    # Boundary clamping: only sample within image bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        pixel_sum += image[nr][nc]
                        sample_count += 1
                        
            blurred[r][c] = round(pixel_sum / sample_count, 1)
            
    return blurred

test_image = [
    [10.0, 10.0, 10.0, 10.0],
    [10.0, 90.0, 90.0, 10.0],  # Bright central square
    [10.0, 90.0, 90.0, 10.0],
    [10.0, 10.0, 10.0, 10.0]
]

smoothed = apply_box_blur_3x3(test_image)
print("  Original Sharp Image:")
for row in test_image:
    print("   ", [f"{x:>4.1f}" for x in row])
print("  Smoothed / Blurred Image:")
for row in smoothed:
    print("   ", [f"{x:>4.1f}" for x in row])

# Explanation: 2D spatial filtering uses 4 nested loops (2 for image dimensions,
# 2 for kernel dimensions), fundamental to computer vision and signal processing.


# ============================================================
# Q8: Matrix Transposition
# ============================================================
# Question: Transpose an M x N matrix into an N x M matrix from scratch
# using nested loops (without zip(*matrix)).

print("\n=== Q8: Matrix Transposition ===")

def transpose_matrix(matrix: list[list]) -> list[list]:
    """Transposes matrix from M x N to N x M."""
    m_rows = len(matrix)
    n_cols = len(matrix[0])
    
    # Create empty target matrix of dimension N x M
    transposed = [[None for _ in range(m_rows)] for _ in range(n_cols)]
    
    for r in range(m_rows):
        for c in range(n_cols):
            transposed[c][r] = matrix[r][c]
            
    return transposed

orig_mat = [
    ["A1", "A2", "A3", "A4"],
    ["B1", "B2", "B3", "B4"],
    ["C1", "C2", "C3", "C4"]
]  # 3 rows, 4 columns

trans = transpose_matrix(orig_mat)
print(f"  Original Dimension:   {len(orig_mat)}x{len(orig_mat[0])}")
print(f"  Transposed Dimension: {len(trans)}x{len(trans[0])}")
print("  Transposed Matrix:")
for row in trans:
    print(f"    {row}")

# Explanation: Transposition swaps row and column indices: $T[j][i] = M[i][j]$.


# ============================================================
# Q9: Co-occurrence Matrix / Basket Analysis
# ============================================================
# Question: Build an item co-occurrence matrix from shopping baskets using nested loops:
# Count how frequently pairs of items are purchased together.

print("\n=== Q9: Item Co-occurrence Matrix ===")

baskets = [
    ["milk", "bread", "butter"],
    ["bread", "eggs"],
    ["milk", "bread", "eggs", "butter"],
    ["milk", "cookies"],
    ["bread", "butter"]
]

# Collect all unique items
all_items = sorted(list({item for b in baskets for item in b}))
co_matrix = {item: {other: 0 for other in all_items} for item in all_items}

for basket in baskets:
    n = len(basket)
    # Nested loops across pairs within each basket
    for i in range(n):
        for j in range(n):
            if i != j:
                item_a = basket[i]
                item_b = basket[j]
                co_matrix[item_a][item_b] += 1

print(f"  Co-occurrence Matrix (Header = {all_items}):")
for item in all_items:
    row_counts = [str(co_matrix[item][other]) for other in all_items]
    print(f"    {item:<8}: {' '.join(f'{c:>6}' for c in row_counts)}")

# Explanation: Co-occurrence matrices are the foundation of collaborative filtering
# recommendation engines and association rule mining (e.g. Apriori algorithm).


# ============================================================
# Q10: Conway's Game of Life Cellular Automaton Tick
# ============================================================
# Question: Implement one generation update of Conway's Game of Life on a 2D grid:
# Live cell survives if it has 2 or 3 neighbors, dead cell becomes alive if exactly 3 neighbors.
# Use nested loops to evaluate the 8-connected neighborhood for each cell.

print("\n=== Q10: Conway's Game of Life Simulation ===")

def step_game_of_life(grid: list[list[int]]) -> list[list[int]]:
    """Calculates next generation grid based on Conway's 4 rules."""
    rows = len(grid)
    cols = len(grid[0])
    next_gen = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # 8 neighbor relative offsets
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]
    
    for r in range(rows):
        for c in range(cols):
            # Count live neighbors
            live_neighbors = 0
            for dr, dc in neighbors:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    live_neighbors += grid[nr][nc]
                    
            # Apply Conway's rules
            current_state = grid[r][c]
            if current_state == 1:
                # Rule 1 & 2: Under/overpopulation -> dies; Rule 3: 2 or 3 neighbors -> lives
                if live_neighbors in (2, 3):
                    next_gen[r][c] = 1
                else:
                    next_gen[r][c] = 0
            else:
                # Rule 4: Reproduction -> exactly 3 neighbors
                if live_neighbors == 3:
                    next_gen[r][c] = 1
                else:
                    next_gen[r][c] = 0
                    
    return next_gen

def render_grid(grid: list[list[int]]):
    for row in grid:
        print("    " + "".join("# " if cell == 1 else ". " for cell in row))

# Blinker oscillator pattern (period 2)
blinker_gen0 = [
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0]
]

print("  Generation 0 (Vertical Blinker):")
render_grid(blinker_gen0)

blinker_gen1 = step_game_of_life(blinker_gen0)
print("\n  Generation 1 (Horizontal Blinker):")
render_grid(blinker_gen1)

blinker_gen2 = step_game_of_life(blinker_gen1)
print("\n  Generation 2 (Oscillates back to Vertical):")
render_grid(blinker_gen2)

# Summary Output
print("\n" + "=" * 55)
print("  All 10 Questions for Topic 02 - Q06 executed successfully!")
print("=" * 55)
