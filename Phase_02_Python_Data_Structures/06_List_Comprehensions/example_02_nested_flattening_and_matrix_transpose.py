"""
Topic 06: List Comprehensions
Example 02: Flattening 2D Lists, Cartesian Products, and Matrix Transposition

Demonstrates multi-clause list comprehensions (`for row in matrix for val in row`)
and nested list comprehensions (`[[...] for c in range(cols)]`).
"""


def main() -> None:
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
    ]

    # 1. Flattening a 2D matrix into a 1D list (read left-to-right: outer loop first, inner loop second)
    flattened = [cell for row in matrix for cell in row]

    # 2. Transposing a 2x3 matrix into a 3x2 matrix (nested comprehension)
    num_cols = len(matrix[0])
    transposed = [[row[col_idx] for row in matrix] for col_idx in range(num_cols)]

    print("=== 1. 2D Matrix Flattening & Transposition ===")
    print(f"Original 2x3 Matrix   : {matrix}")
    print(f"Flattened 1D List     : {flattened}")
    print(f"Transposed 3x2 Matrix : {transposed}")

    # 3. Cartesian product with filter
    ranks = ["A", "K", "Q"]
    suits = ["Spades", "Hearts"]
    cards = [f"{r} of {s}" for r in ranks for s in suits]
    print("\n=== 2. Cartesian Product ===")
    print(f"Generated Cards ({len(cards)}) : {cards}")


if __name__ == "__main__":
    main()
