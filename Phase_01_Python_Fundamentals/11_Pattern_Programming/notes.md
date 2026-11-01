# Topic 11: Pattern Programming

---

## 1. Introduction

**Pattern Programming** is the art of printing structured 2D shapes—such as triangles, pyramids, diamonds, hollow frames, and number matrices—using nested loops and mathematical coordinate formulas.

While you rarely print ASCII pyramids in production web apps, pattern programming is the #1 way to build **2D grid and matrix intuition** for Data Structures & Algorithms.

---

## 2. Why is it used?

1. **Mastering Nested Loop Control:** Teaches you how an outer loop (`row`) and an inner loop (`col`) interact—the exact same skill needed for Matrix Manipulation, Dynamic Programming tables, and Graph Grid BFS/DFS.
2. **Deriving Mathematical Formulas from Examples:** Trains you to express relationships like `spaces = n - r` and `stars = 2 * r - 1` instead of hardcoding lines.
3. **Campus Placement Rounds:** Service- and product-based campus placement assessments frequently test hollow diamonds, Pascal's triangle, or palindromic number pyramids in Round 1.

---

## 3. Syntax

### Universal 4-Step Framework for Any Pattern:
1. **Count total rows (`N`):** This defines the outer loop `for r in range(1, n + 1):`.
2. **For row `r`, count how many leading spaces and symbols are needed:**
   - Right-angled triangle: `r` stars
   - Inverted triangle: `n - r + 1` stars
   - Centered pyramid: `n - r` spaces followed by `2 * r - 1` stars
3. **Determine what to print at each column (`*`, `r`, `c`, or a running counter).**
4. **Move to a new line at the end of each row.**

```python
n = 5
for r in range(1, n + 1):
    spaces = " " * (n - r)
    stars = "*" * (2 * r - 1)
    print(f"{spaces}{stars}")
```

---

## 4. Explanation (Step-by-Step Formula Derivation)

Consider a **Centered Pyramid** of height `n = 5`:

| Row (`r`) | Leading Spaces (`n - r`) | Stars (`2 * r - 1`) | Output Line |
| :---: | :---: | :---: | :--- |
| `1` | `5 - 1 = 4` | `2(1) - 1 = 1` | `    *` |
| `2` | `5 - 2 = 3` | `2(2) - 1 = 3` | `   ***` |
| `3` | `5 - 3 = 2` | `2(3) - 1 = 5` | `  *****` |
| `4` | `5 - 4 = 1` | `2(4) - 1 = 7` | ` *******` |
| `5` | `5 - 5 = 0` | `2(5) - 1 = 9` | `*********` |

And for a **Hollow Square** of size `N x N`, a cell `(r, c)` is on the border if and only if:
`r == 1 or r == N or c == 1 or c == N`.

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_right_and_inverted_triangles.py`](example_01_right_and_inverted_triangles.py)
- [`example_02_centered_pyramid_and_diamond.py`](example_02_centered_pyramid_and_diamond.py)
- [`example_03_floyds_and_pascals_number_triangles.py`](example_03_floyds_and_pascals_number_triangles.py)

### Example 1: Right-Angled Triangle, Inverted Triangle, and Hollow Square (`example_01_right_and_inverted_triangles.py`)

```python
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
```

### Example 2: Centered Pyramid and Symmetric Diamond (`example_02_centered_pyramid_and_diamond.py`)

```python
def print_centered_pyramid(n: int) -> None:
    print(f"=== 1. Centered Pyramid (n={n}) ===")
    for r in range(1, n + 1):
        spaces = " " * (n - r)
        stars = "*" * (2 * r - 1)
        print(f"{spaces}{stars}")


def print_symmetric_diamond(n: int) -> None:
    print(f"\n=== 2. Symmetric Diamond (half-height n={n}) ===")
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
```

### Example 3: Floyd's Triangle, Palindromic Pyramid & Pascal's Triangle (`example_03_floyds_and_pascals_number_triangles.py`)

```python
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


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== 1. Right-Angled Star Triangle (n=5) ===
* 
* * 
* * * 
* * * * 
* * * * * 

=== 2. Inverted Star Triangle (n=5) ===
* * * * * 
* * * * 
* * * 
* * 
* 

=== 3. Hollow Square Frame (5x5) ===
* * * * *
*       *
*       *
*       *
* * * * *
```

### Output for Example 2:
```text
=== 1. Centered Pyramid (n=5) ===
    *
   ***
  *****
 *******
*********

=== 2. Symmetric Diamond (half-height n={4}) ===
   *
  ***
 *****
*******
 *****
  ***
   *
```

### Output for Example 3:
```text
=== 1. Floyd's Triangle (rows=4) ===
 1
 2  3
 4  5  6
 7  8  9 10

=== 2. Palindromic Number Pyramid (n=5) ===
        1
      1 2 1
    1 2 3 2 1
  1 2 3 4 3 2 1
1 2 3 4 5 4 3 2 1

=== 3. Pascal's Triangle (rows=5) ===
          1
        1   1
      1   2   1
    1   3   3   1
  1   4   6   4   1
```

---

## 7. Code Explanation

- **`val = val * (r - c) // (c + 1)`** — Computes the next binomial coefficient $\binom{r}{c+1}$ in Pascal's Triangle directly from $\binom{r}{c}$ in `O(1)` time without computing factorials!
- **`row_sequence = list(range(1, n + 1)) + list(range(n - 1, 0, -1))`** — For `n = 4`, this generates `[1, 2, 3, 4, 3, 2, 1]`, allowing a single loop to print both the upper and lower halves of a symmetric diamond without duplicating code.

---

## 8. Common Mistakes

1. **Resetting the Counter Inside the Outer Loop in Floyd's Triangle:**
   If you put `counter = 1` **inside** `for r in range(1, rows + 1):`, every row starts at `1` instead of continuing `1 / 2 3 / 4 5 6`. Initialize `counter = 1` **outside** the outer loop.
2. **Duplicating the Middle Row of a Diamond:**
   If the upper half runs `1..n` and the lower half runs `n..1`, the middle row of width `2n - 1` is printed twice! Always start the lower half at `n - 1`.
3. **Misaligned Multi-Digit Numbers:**
   When numbers grow from 1 digit (`9`) to 2 digits (`10`), the triangle skews unless you format numbers with fixed width (`f"{counter:>2}"`).

---

## 9. Practice Questions

1. **Easy:** Write a function `print_binary_triangle(n: int)` that prints `n` rows where cell `(r, c)` is `1` if `(r + c)` is even and `0` if `(r + c)` is odd (`1` / `0 1` / `1 0 1` / ...).
2. **Medium:** Write a function `print_hollow_pyramid(n: int)` that prints a centered pyramid of height `n` where only the outer left edge, outer right edge, and bottom base row contain `*`, and the interior is hollow spaces.
3. **Hard:** Write a function `print_butterfly(n: int)` that prints a symmetric `2n - 1` butterfly star pattern (left wing of `r` stars, middle gap of `2*(n - r)` spaces, right wing of `r` stars).

---

## 10. Interview Questions

### Q1: What is the time and space complexity of printing an `N`-row pyramid or Pascal's Triangle?
**Answer:** Row `r` contains `O(r)` characters. Across `N` rows, the total number of operations is $1 + 2 + \dots + N = \frac{N(N+1)}{2}$, so the **Time Complexity is `O(N^2)`** and auxiliary **Space Complexity is `O(N)`** (to hold a single row buffer before printing).

### Q2: How can you compute any row `r` of Pascal's Triangle in `O(r)` time and `O(1)` extra space without factorials?
**Answer:** Start with `val = 1` (since $\binom{r}{0} = 1$) and use the recurrence $\binom{r}{c+1} = \binom{r}{c} \times \frac{r - c}{c + 1}$ via integer division `val = val * (r - c) // (c + 1)` for `c` from `0` to `r - 1`.

### Q3: How do you print a concentric number square of size `(2n - 1) x (2n - 1)` where the outer border is `n` and the center is `1`?
**Answer:** For any cell `(r, c)` in `0 .. 2n - 2`, its distance from the nearest border is `min(r, c, 2*n - 2 - r, 2*n - 2 - c)`. Subtracting that distance from `n` (`n - min_dist`) gives the exact value at `(r, c)` in `O(1)` per cell!
