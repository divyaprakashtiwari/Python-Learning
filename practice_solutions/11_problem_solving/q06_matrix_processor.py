"""
Question 6: 2D Matrix Computing Engine (Multiplication, Transposition, Rotation & Spiral)
Topic: Problem Solving & Competitive Programming Patterns

Key Concepts Tested:
- Matrix multiplication validation and dot-product computation
- Rectangular matrix transposition
- In-place 90-degree clockwise rotation (transpose + row reversal) in O(1) space
- Clockwise spiral order traversal using 4 dynamic boundary pointers
- Boundary condition handling (empty matrices, ragged inputs, dimension mismatches)
"""

from typing import List


class MatrixProcessor:
    """
    Multidimensional 2D matrix transformation engine.
    """

    @staticmethod
    def multiply(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
        """
        Computes the matrix product A x B.
        Validates column count of A matches row count of B.
        """
        if not A or not A[0] or not B or not B[0]:
            return []

        m, k = len(A), len(A[0])
        kb, n = len(B), len(B[0])

        if k != kb:
            raise ValueError(f"Incompatible dimensions for multiplication: {m}x{k} and {kb}x{n}")

        result = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                result[i][j] = sum(A[i][p] * B[p][j] for p in range(k))

        return result

    @staticmethod
    def transpose(M: List[List[int]]) -> List[List[int]]:
        """Flips an M x N matrix across its main diagonal into an N x M matrix."""
        if not M or not M[0]:
            return []

        rows, cols = len(M), len(M[0])
        return [[M[r][c] for r in range(rows)] for c in range(cols)]

    @staticmethod
    def rotate_clockwise_inplace(M: List[List[int]]) -> None:
        """
        Rotates an N x N square matrix 90 degrees clockwise in-place with O(1) extra memory.
        Step 1: Transpose across primary diagonal.
        Step 2: Reverse every row horizontally.
        """
        if not M or not M[0]:
            return

        n = len(M)
        if any(len(row) != n for row in M):
            raise ValueError("Matrix must be square (N x N) for in-place rotation")

        # Step 1: Transpose in-place
        for i in range(n):
            for j in range(i + 1, n):
                M[i][j], M[j][i] = M[j][i], M[i][j]

        # Step 2: Reverse each row in-place
        for row in M:
            row.reverse()

    @staticmethod
    def spiral_order(M: List[List[int]]) -> List[int]:
        """Traverses an M x N matrix in clockwise spiral order."""
        if not M or not M[0]:
            return []

        result: List[int] = []
        top, bottom = 0, len(M) - 1
        left, right = 0, len(M[0]) - 1

        while top <= bottom and left <= right:
            # 1. Traverse left to right along top boundary
            for c in range(left, right + 1):
                result.append(M[top][c])
            top += 1

            # 2. Traverse top to bottom along right boundary
            for r in range(top, bottom + 1):
                result.append(M[r][right])
            right -= 1

            # 3. Traverse right to left along bottom boundary (if valid)
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    result.append(M[bottom][c])
                bottom -= 1

            # 4. Traverse bottom to top along left boundary (if valid)
            if left <= right:
                for r in range(bottom, top - 1, -1):
                    result.append(M[r][left])
                left += 1

        return result


if __name__ == "__main__":
    processor = MatrixProcessor()

    print("=== 1. Matrix Multiplication ===")
    A = [[1, 2], [3, 4]]
    B = [[2, 0], [1, 2]]
    prod = processor.multiply(A, B)
    print(f"Matrix Product A x B: {prod}")

    print("\n=== 2. Matrix Transposition ===")
    rect_mat = [[1, 2, 3], [4, 5, 6]]
    transposed = processor.transpose(rect_mat)
    print(f"Transposed Rectangular Matrix: {transposed}")

    print("\n=== 3. In-Place 90-Degree Clockwise Rotation ===")
    sq_mat = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    processor.rotate_clockwise_inplace(sq_mat)
    print("90-Degree Clockwise Rotated Matrix:")
    for row in sq_mat:
        print(f"  {row}")

    print("\n=== 4. Clockwise Spiral Order Traversal ===")
    spiral_mat = [
        [1,  2,  3,  4],
        [5,  6,  7,  8],
        [9, 10, 11, 12],
    ]
    spiral_res = processor.spiral_order(spiral_mat)
    print(f"Spiral Order Traversal: {spiral_res}")

    print("\n=== 5. Edge Cases & Validation ===")
    print(f"Empty matrix multiplication: {processor.multiply([], [])}")
    print(f"Empty spiral order: {processor.spiral_order([])}")
    try:
        processor.multiply([[1, 2]], [[1, 2], [3, 4], [5, 6]])
    except ValueError as err:
        print(f"Caught incompatible dimensions: {err}")

    try:
        processor.rotate_clockwise_inplace([[1, 2, 3], [4, 5, 6]])
    except ValueError as err:
        print(f"Caught non-square rotation: {err}")
