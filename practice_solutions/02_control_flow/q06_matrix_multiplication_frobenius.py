"""
Topic 02 - Control Flow
Practice Question 6 Solution: Matrix Multiplication & Frobenius Norm via Nested Loops

Problem Statement:
1. Matrix Dimension Validation: A (m x k) and B (k x n). Raise ValueError if cols(A) != rows(B).
2. Matrix Multiplication via 3-level nested loops: C[i][j] = sum(A[i][k] * B[k][j]).
3. Frobenius Norm Calculation: square root of the sum of squared elements in C.
"""

import math


def multiply_matrices(a: list[list[float]], b: list[list[float]]) -> tuple[list[list[float]], float]:
    """Multiplies two matrices using 3 nested loops and calculates the Frobenius norm."""
    if not a or not a[0] or not b or not b[0]:
        raise ValueError("Matrices cannot be empty.")

    m = len(a)
    k_a = len(a[0])
    k_b = len(b)
    n = len(b[0])

    if k_a != k_b:
        raise ValueError("Incompatible matrix dimensions for multiplication")

    # Initialize m x n result matrix with zeros
    c: list[list[float]] = [[0.0 for _ in range(n)] for _ in range(m)]

    # 3-level nested loops for matrix multiplication
    for i in range(m):
        for j in range(n):
            cell_sum = 0.0
            for k in range(k_a):
                cell_sum += a[i][k] * b[k][j]
            c[i][j] = cell_sum

    # 2-level nested loops for Frobenius norm
    sum_squares = 0.0
    for i in range(m):
        for j in range(n):
            sum_squares += c[i][j] ** 2

    frobenius_norm = math.sqrt(sum_squares)

    return c, frobenius_norm


def main() -> None:
    matrix_a = [
        [1, 2, 3],
        [4, 5, 6],
    ]
    matrix_b = [
        [7, 8],
        [9, 1],
        [2, 3],
    ]

    c, norm = multiply_matrices(matrix_a, matrix_b)

    print(f"Matrix A Dimensions: {len(matrix_a)}x{len(matrix_a[0])}")
    print(f"Matrix B Dimensions: {len(matrix_b)}x{len(matrix_b[0])}")
    print(f"Result Matrix C ({len(c)}x{len(c[0])}):")
    for row in c:
        int_row = [int(x) if x.is_integer() else x for x in row]
        print(int_row)
    print(f"Frobenius Norm: {norm:.2f}")


if __name__ == "__main__":
    main()
