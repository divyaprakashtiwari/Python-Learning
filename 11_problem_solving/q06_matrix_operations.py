"""
Topic: Problem Solving - Matrix Operations
------------------------------------------
Questions Covered:
1. Element-Wise Matrix Algebra: Addition, subtraction, and scalar multiplication with dimension checks.
2. Standard Matrix Multiplication: Dot product multiplication with inner dimension validation.
3. In-Place Square Matrix Transposition: Swapping elements across the main diagonal in O(1) space.
4. Rotate Matrix 90 Degrees Clockwise In-Place: Composition of transpose and row reflection.
5. Spiral Matrix Order Traversal: Four-boundary inward winding traversal into flat list.
6. Set Matrix Zeroes In-Place: O(1) auxiliary space zero-propagation using first row/col markers.
7. Matrix Determinant via Laplace Expansion: Recursive cofactor expansion for arbitrary square matrices.
8. Gaussian Elimination with Back-Substitution: Linear equation solver (Ax = b) with partial pivoting.
9. Matrix Chain Multiplication: Dynamic programming minimizing scalar multiplication count.
10. Architectural System: 2D Computer Graphics Affine Transformation Pipeline (Translation, Rotation, Scaling).
"""

import math
from typing import List, Tuple, Optional, Any, Dict


# ==============================================================================
# Question 1: Element-Wise Matrix Algebra
# ==============================================================================
def matrix_add(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """Adds two matrices of identical dimensions."""
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Matrix dimensions must match for addition")
    return [[A[r][c] + B[r][c] for c in range(len(A[0]))] for r in range(len(A))]


def matrix_scalar_multiply(A: List[List[float]], scalar: float) -> List[List[float]]:
    """Multiplies every element in matrix by a scalar."""
    return [[elem * scalar for elem in row] for row in A]


def test_q1_elementwise_algebra():
    m1 = [[1.0, 2.0], [3.0, 4.0]]
    m2 = [[5.0, 6.0], [7.0, 8.0]]
    assert matrix_add(m1, m2) == [[6.0, 8.0], [10.0, 12.0]]
    assert matrix_scalar_multiply(m1, 2.5) == [[2.5, 5.0], [7.5, 10.0]]
    print("=== Q1: Element-Wise Matrix Algebra Verified ===")


# ==============================================================================
# Question 2: Standard Matrix Multiplication (Dot Product)
# ==============================================================================
def matrix_multiply(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """
    Multiplies matrix A (m x k) with matrix B (k x n) to produce an m x n matrix.
    Raises ValueError if cols(A) != rows(B).
    """
    m = len(A)
    k_a = len(A[0])
    k_b = len(B)
    n = len(B[0])

    if k_a != k_b:
        raise ValueError(f"Cannot multiply dimensions ({m}x{k_a}) with ({k_b}x{n})")

    result = [[0.0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            result[i][j] = sum(A[i][k] * B[k][j] for k in range(k_a))

    return result


def test_q2_matrix_multiply():
    a = [
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
    ]  # 2 x 3
    b = [
        [7.0, 8.0],
        [9.0, 1.0],
        [2.0, 3.0],
    ]  # 3 x 2
    # Result (2 x 2):
    # [1*7 + 2*9 + 3*2, 1*8 + 2*1 + 3*3] = [7 + 18 + 6, 8 + 2 + 9] = [31, 19]
    # [4*7 + 5*9 + 6*2, 4*8 + 5*1 + 6*3] = [28 + 45 + 12, 32 + 5 + 18] = [85, 55]
    prod = matrix_multiply(a, b)
    assert prod == [[31.0, 19.0], [85.0, 55.0]]
    print("=== Q2: Standard Matrix Multiplication Verified ===")


# ==============================================================================
# Question 3: In-Place Square Matrix Transposition
# ==============================================================================
def transpose_square_inplace(matrix: List[List[Any]]) -> None:
    """Transposes an N x N square matrix in-place in O(1) auxiliary space."""
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]


def test_q3_inplace_transpose():
    sq = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    transpose_square_inplace(sq)
    assert sq == [
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],
    ]
    print("=== Q3: In-Place Square Matrix Transposition Verified ===")


# ==============================================================================
# Question 4: Rotate Matrix 90 Degrees Clockwise In-Place
# ==============================================================================
def rotate_matrix_90_clockwise(matrix: List[List[Any]]) -> None:
    """
    Rotates an N x N matrix by 90 degrees clockwise in-place:
    1. Transpose the matrix
    2. Reverse each row
    """
    n = len(matrix)
    # 1. Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # 2. Reverse each row
    for row in matrix:
        row.reverse()


def test_q4_rotate_matrix_90():
    img = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    rotate_matrix_90_clockwise(img)
    # 90 degrees clockwise:
    # 7 4 1
    # 8 5 2
    # 9 6 3
    assert img == [
        [7, 4, 1],
        [8, 5, 2],
        [9, 6, 3],
    ]
    print("=== Q4: Rotate Matrix 90 Degrees Clockwise In-Place Verified ===")


# ==============================================================================
# Question 5: Spiral Matrix Traversal
# ==============================================================================
def spiral_order_traversal(matrix: List[List[Any]]) -> List[Any]:
    """
    Traverses an M x N matrix in spiral clockwise order, returning elements in a 1D list.
    """
    if not matrix or not matrix[0]:
        return []

    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        # Traverse right across top boundary
        for c in range(left, right + 1):
            result.append(matrix[top][c])
        top += 1

        # Traverse down right boundary
        for r in range(top, bottom + 1):
            result.append(matrix[r][right])
        right -= 1

        # Traverse left across bottom boundary
        if top <= bottom:
            for c in range(right, left - 1, -1):
                result.append(matrix[bottom][c])
            bottom -= 1

        # Traverse up left boundary
        if left <= right:
            for r in range(bottom, top - 1, -1):
                result.append(matrix[r][left])
            left += 1

    return result


def test_q5_spiral_order():
    m = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
    ]
    res = spiral_order_traversal(m)
    assert res == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    print("=== Q5: Spiral Matrix Traversal Verified ===")


# ==============================================================================
# Question 6: Set Matrix Zeroes In-Place (O(1) Space)
# ==============================================================================
def set_matrix_zeroes(matrix: List[List[int]]) -> None:
    """
    If an element is 0, sets its entire row and column to 0 in-place.
    Uses first row and first column as state markers to achieve O(1) auxiliary space.
    """
    rows = len(matrix)
    cols = len(matrix[0])
    first_col_zero = False

    for r in range(rows):
        if matrix[r][0] == 0:
            first_col_zero = True
        for c in range(1, cols):
            if matrix[r][c] == 0:
                matrix[r][0] = 0
                matrix[0][c] = 0

    # Fill inner elements
    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0

    # Fill first row if needed
    if matrix[0][0] == 0:
        for c in range(cols):
            matrix[0][c] = 0

    # Fill first column if needed
    if first_col_zero:
        for r in range(rows):
            matrix[r][0] = 0


def test_q6_set_matrix_zeroes():
    m = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]
    set_matrix_zeroes(m)
    assert m == [
        [1, 0, 1],
        [0, 0, 0],
        [1, 0, 1],
    ]
    print("=== Q6: Set Matrix Zeroes In-Place Verified ===")


# ==============================================================================
# Question 7: Matrix Determinant via Laplace Expansion
# ==============================================================================
def matrix_determinant(matrix: List[List[float]]) -> float:
    """
    Computes determinant of square matrix recursively using cofactor Laplace expansion.
    """
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0.0
    for col in range(n):
        # Submatrix excluding row 0 and column col
        sub = [row[:col] + row[col + 1 :] for row in matrix[1:]]
        sign = 1.0 if col % 2 == 0 else -1.0
        det += sign * matrix[0][col] * matrix_determinant(sub)

    return det


def test_q7_matrix_determinant():
    m2 = [[4.0, 6.0], [3.0, 8.0]]
    # 4*8 - 6*3 = 32 - 18 = 14
    assert matrix_determinant(m2) == 14.0

    m3 = [
        [6.0, 1.0, 1.0],
        [4.0, -2.0, 5.0],
        [2.0, 8.0, 7.0],
    ]
    # det(m3) = -306.0
    assert abs(matrix_determinant(m3) - (-306.0)) < 1e-6
    print("=== Q7: Matrix Determinant via Laplace Expansion Verified ===")


# ==============================================================================
# Question 8: Gaussian Elimination Linear System Solver (Ax = b)
# ==============================================================================
def solve_linear_system(A: List[List[float]], b: List[float]) -> List[float]:
    """
    Solves linear equation system A * x = b using Gaussian elimination with partial pivoting.
    Returns vector x.
    """
    n = len(A)
    # Augment matrix [A | b]
    aug = [A[i][:] + [b[i]] for i in range(n)]

    # Forward elimination with partial pivoting
    for col in range(n):
        # Find pivot row with largest absolute value in current column
        pivot_row = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot_row][col]) < 1e-12:
            raise ValueError("Matrix is singular or nearly singular")

        aug[col], aug[pivot_row] = aug[pivot_row], aug[col]

        # Eliminate rows below
        for row in range(col + 1, n):
            factor = aug[row][col] / aug[col][col]
            for c in range(col, n + 1):
                aug[row][c] -= factor * aug[col][c]

    # Back substitution
    x = [0.0] * n
    for row in range(n - 1, -1, -1):
        total = aug[row][n]
        for c in range(row + 1, n):
            total -= aug[row][c] * x[c]
        x[row] = total / aug[row][row]

    return x


def test_q8_gaussian_elimination():
    # 2x + y - z = 8
    # -3x - y + 2z = -11
    # -2x + y + 2z = -3
    # Solution: x = 2, y = 3, z = -1
    A = [
        [2.0, 1.0, -1.0],
        [-3.0, -1.0, 2.0],
        [-2.0, 1.0, 2.0],
    ]
    b = [8.0, -11.0, -3.0]
    sol = solve_linear_system(A, b)
    assert [round(val, 2) for val in sol] == [2.0, 3.0, -1.0]
    print("=== Q8: Gaussian Elimination Linear Solver Verified ===")


# ==============================================================================
# Question 9: Matrix Chain Multiplication (Dynamic Programming)
# ==============================================================================
def matrix_chain_multiplication(dims: List[int]) -> int:
    """
    Computes minimum number of scalar multiplications needed to multiply a chain of matrices.
    Matrix A_i has dimension dims[i-1] x dims[i].
    dims of length n represents n-1 matrices.
    """
    n = len(dims) - 1  # Number of matrices
    # dp[i][j]: minimum cost to multiply A_i .. A_j
    dp = [[0] * (n + 1) for _ in range(n + 1)]

    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                if cost < dp[i][j]:
                    dp[i][j] = cost

    return int(dp[1][n])


def test_q9_matrix_chain_multiplication():
    # Dimensions: 10x30, 30x5, 5x60 -> dims = [10, 30, 5, 60]
    # Optimal: (A1 * A2) * A3 -> (10*30*5) + (10*5*60) = 1500 + 3000 = 4500
    assert matrix_chain_multiplication([10, 30, 5, 60]) == 4500
    assert matrix_chain_multiplication([40, 20, 30, 10, 30]) == 26000
    print("=== Q9: Matrix Chain Multiplication Verified ===")


# ==============================================================================
# Question 10: Architectural 2D Computer Graphics Affine Transform Pipeline
# ==============================================================================
class MatrixTransform2D:
    """
    Production 2D affine graphics transformation pipeline using 3x3 homogeneous coordinates:
    Point (x, y) is represented as [x, y, 1]^T.
    Transformations are composed via matrix multiplication.
    """
    @staticmethod
    def identity() -> List[List[float]]:
        return [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]

    @staticmethod
    def translation(tx: float, ty: float) -> List[List[float]]:
        return [
            [1.0, 0.0, tx],
            [0.0, 1.0, ty],
            [0.0, 0.0, 1.0],
        ]

    @staticmethod
    def scale(sx: float, sy: float) -> List[List[float]]:
        return [
            [sx, 0.0, 0.0],
            [0.0, sy, 0.0],
            [0.0, 0.0, 1.0],
        ]

    @staticmethod
    def rotation(theta_degrees: float) -> List[List[float]]:
        rad = math.radians(theta_degrees)
        c = math.cos(rad)
        s = math.sin(rad)
        return [
            [c, -s, 0.0],
            [s, c, 0.0],
            [0.0, 0.0, 1.0],
        ]

    @classmethod
    def apply_transform(cls, transform_matrix: List[List[float]], point: Tuple[float, float]) -> Tuple[float, float]:
        x, y = point
        # [M] * [x, y, 1]^T
        res_x = transform_matrix[0][0] * x + transform_matrix[0][1] * y + transform_matrix[0][2] * 1.0
        res_y = transform_matrix[1][0] * x + transform_matrix[1][1] * y + transform_matrix[1][2] * 1.0
        return (round(res_x, 2), round(res_y, 2))


def test_q10_graphics_transform_pipeline():
    # 1. Translate point (5, 5) by (10, -2) -> (15, 3)
    t_mat = MatrixTransform2D.translation(10.0, -2.0)
    p_trans = MatrixTransform2D.apply_transform(t_mat, (5.0, 5.0))
    assert p_trans == (15.0, 3.0)

    # 2. Scale point (2, 3) by (3, 4) -> (6, 12)
    s_mat = MatrixTransform2D.scale(3.0, 4.0)
    p_scale = MatrixTransform2D.apply_transform(s_mat, (2.0, 3.0))
    assert p_scale == (6.0, 12.0)

    # 3. Rotate (1, 0) by 90 degrees -> (0, 1)
    r_mat = MatrixTransform2D.rotation(90.0)
    p_rot = MatrixTransform2D.apply_transform(r_mat, (1.0, 0.0))
    assert p_rot == (0.0, 1.0)

    # 4. Composite transform: Scale then Translate -> T * S
    composite = matrix_multiply(t_mat, s_mat)
    # Point (2, 3) scaled by (3, 4) gives (6, 12), then translated by (10, -2) gives (16, 10)
    p_comp = MatrixTransform2D.apply_transform(composite, (2.0, 3.0))
    assert p_comp == (16.0, 10.0)
    print("=== Q10: Architectural 2D Graphics Affine Transform Pipeline Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_elementwise_algebra()
    test_q2_matrix_multiply()
    test_q3_inplace_transpose()
    test_q4_rotate_matrix_90()
    test_q5_spiral_order()
    test_q6_set_matrix_zeroes()
    test_q7_matrix_determinant()
    test_q8_gaussian_elimination()
    test_q9_matrix_chain_multiplication()
    test_q10_graphics_transform_pipeline()
    print("\nAll 10 matrix operations problem-solving questions passed successfully!")
