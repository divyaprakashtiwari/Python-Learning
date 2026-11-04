"""
Phase 5 - Topic 12: Enumerate and Zip
Example 03: Matrix Transposition (`zip(*matrix)`), Unzipping Pairs, & `itertools.zip_longest`

Demonstrates:
  - Transposing a 2D matrix (rows <-> columns) in one line using star-unpacking `zip(*matrix)`
  - Unzipping a list of `(x, y)` tuples back into separate `xs` and `ys` tuples
  - Padding uneven sequences instead of truncating using `itertools.zip_longest(..., fillvalue=...)`
"""

from itertools import zip_longest


def main() -> None:
    print("=== 1. 2D Matrix Transposition with `zip(*matrix)` ===")
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
    ]
    transposed = [list(col) for col in zip(*matrix, strict=True)]
    print(f"  Original (2x3)   : {matrix}")
    print(f"  Transposed (3x2) : {transposed}")

    print("\n=== 2. Unzipping `[(k, v), ...]` Pairs with `zip(*pairs)` ===")
    pairs = [("a", 10), ("b", 20), ("c", 30)]
    letters, numbers = zip(*pairs)
    print(f"  Letters : {letters} | Numbers : {numbers}")

    print("\n=== 3. Padding Uneven Iterables with `itertools.zip_longest` ===")
    q1_sales = [120, 150, 180]
    q2_sales = [140]
    padded = list(zip_longest(q1_sales, q2_sales, fillvalue=0))
    print(f"  zip_longest(..., fillvalue=0): {padded}")


if __name__ == "__main__":
    main()
