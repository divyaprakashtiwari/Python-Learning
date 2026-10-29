"""
Question 4: Fibonacci Algorithms Suite (Iterative, Memoized, Logarithmic Matrix & Stream)
Topic: Problem Solving & Competitive Programming Patterns

Key Concepts Tested:
- Space-optimized iterative Fibonacci computation in O(N) time and O(1) space
- Top-down memoized recursion eliminating exponential subtrees
- Logarithmic O(log N) matrix exponentiation (repeated squaring) for huge N
- Infinite generator yielding Fibonacci numbers on demand
- Value-to-index search in Fibonacci sequence
"""

from typing import Generator, Dict, List, Optional


class FibonacciSuite:
    """
    Toolkit implementing multiple algorithmic paradigms for calculating Fibonacci numbers.
    """

    @staticmethod
    def fib_iterative(n: int) -> int:
        """Computes F(n) in O(N) time and strict O(1) space."""
        if n < 0:
            raise ValueError(f"Fibonacci index cannot be negative, got: {n}")
        if n <= 1:
            return n

        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    def fib_memoized(self, n: int, memo: Optional[Dict[int, int]] = None) -> int:
        """Computes F(n) using top-down recursion with memoization."""
        if n < 0:
            raise ValueError(f"Fibonacci index cannot be negative, got: {n}")
        if memo is None:
            memo = {0: 0, 1: 1}

        if n in memo:
            return memo[n]

        memo[n] = self.fib_memoized(n - 1, memo) + self.fib_memoized(n - 2, memo)
        return memo[n]

    @staticmethod
    def fib_matrix(n: int) -> int:
        """
        Computes F(n) in strict O(log N) time using 2x2 matrix binary exponentiation.
        [[1, 1], [1, 0]]^n = [[F(n+1), F(n)], [F(n), F(n-1)]]
        """
        if n < 0:
            raise ValueError(f"Fibonacci index cannot be negative, got: {n}")
        if n == 0:
            return 0

        def multiply_2x2(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
            return [
                [
                    a[0][0] * b[0][0] + a[0][1] * b[1][0],
                    a[0][0] * b[0][1] + a[0][1] * b[1][1],
                ],
                [
                    a[1][0] * b[0][0] + a[1][1] * b[1][0],
                    a[1][0] * b[0][1] + a[1][1] * b[1][1],
                ],
            ]

        # Identity matrix
        result = [[1, 0], [0, 1]]
        # Base transition matrix M
        base = [[1, 1], [1, 0]]
        power = n

        while power > 0:
            if power % 2 == 1:
                result = multiply_2x2(result, base)
            base = multiply_2x2(base, base)
            power //= 2

        # F(n) is stored at result[0][1]
        return result[0][1]

    @staticmethod
    def fib_stream() -> Generator[int, None, None]:
        """Infinite generator yielding Fibonacci numbers on demand."""
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    @staticmethod
    def find_index_of_fib(target: int) -> int:
        """
        Determines the 0-indexed Fibonacci position n for target,
        or -1 if target is not a Fibonacci number.
        """
        if target < 0:
            return -1
        if target == 0:
            return 0
        if target == 1:
            return 1  # F(1) == 1

        a, b = 1, 1
        idx = 2
        while b < target:
            a, b = b, a + b
            idx += 1

        return idx if b == target else -1


if __name__ == "__main__":
    suite = FibonacciSuite()

    print("=== 1. Paradigm Comparison for N = 10 ===")
    res_iter = suite.fib_iterative(10)
    res_memo = suite.fib_memoized(10)
    res_matrix = suite.fib_matrix(10)

    print(f"F(10) Iterative: {res_iter}")
    print(f"F(10) Memoized: {res_memo}")
    print(f"F(10) Matrix (Log N): {res_matrix}")

    print("\n=== 2. Large N via Matrix Exponentiation ===")
    res_matrix_large = suite.fib_matrix(50)
    print(f"F(50) Matrix Exponentiation: {res_matrix_large}")

    print("\n=== 3. Infinite Stream Inspection ===")
    stream = suite.fib_stream()
    first_7 = [next(stream) for _ in range(7)]
    print(f"First 7 Fibonacci Numbers: {first_7}")

    print("\n=== 4. Index Search ===")
    idx_55 = suite.find_index_of_fib(55)
    idx_50 = suite.find_index_of_fib(50)
    print(f"Index of 55 in Fibonacci: {idx_55}")
    print(f"Index of 50 in Fibonacci: {idx_50}")

    print("\n=== 5. Edge Cases ===")
    print(f"F(0) Matrix: {suite.fib_matrix(0)}")
    print(f"F(1) Matrix: {suite.fib_matrix(1)}")
    try:
        suite.fib_iterative(-5)
    except ValueError as err:
        print(f"Caught negative input: {err}")
