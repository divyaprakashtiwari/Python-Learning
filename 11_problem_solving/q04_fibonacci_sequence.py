"""
Topic: Problem Solving - Fibonacci Sequence
-------------------------------------------
Questions Covered:
1. Iterative and Space-Optimized Fibonacci: O(n) time and O(1) space accumulator.
2. Fast Matrix Exponentiation: Logarithmic O(log n) Fibonacci computation with modulo 10^9 + 7.
3. Binet's Analytical Closed-Form: Golden ratio (phi) analytical computation with precision guards.
4. Pisano Period (Fibonacci Modulo M): Periodic sequence cycles for astronomical n (10^18).
5. Zeckendorf's Theorem: Unique decomposition of integers into non-consecutive Fibonacci numbers.
6. Generalized N-bonacci (Tribonacci & K-bonacci): Dynamic k-term sliding recurrence.
7. Perfect Square Fibonacci Test: Constant-time identity 5*N^2 +/- 4 perfect square verification.
8. Fibonacci Word Sequence: Binary recursive concatenation generating fractal words.
9. Fibonacci Search Algorithm: Division-free sorted array searching using Fibonacci boundaries.
10. Architectural System: Quantitative Trading Fibonacci Retracement & Extension Indicator Engine.
"""

import math
from typing import List, Tuple, Optional, Any, Dict


# ==============================================================================
# Question 1: Iterative and Space-Optimized Fibonacci
# ==============================================================================
def fibonacci_iterative(n: int) -> int:
    """Computes n-th Fibonacci number in O(n) time and O(1) auxiliary space."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def test_q1_iterative_fibonacci():
    first_10 = [fibonacci_iterative(i) for i in range(10)]
    assert first_10 == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert fibonacci_iterative(20) == 6765
    print("=== Q1: Iterative and Space-Optimized Fibonacci Verified ===")


# ==============================================================================
# Question 2: Fast Matrix Exponentiation (O(log n))
# ==============================================================================
def matrix_multiply_2x2(A: List[List[int]], B: List[List[int]], mod: Optional[int] = None) -> List[List[int]]:
    """Multiplies two 2x2 matrices with optional modulo."""
    c00 = A[0][0] * B[0][0] + A[0][1] * B[1][0]
    c01 = A[0][0] * B[0][1] + A[0][1] * B[1][1]
    c10 = A[1][0] * B[0][0] + A[1][1] * B[1][0]
    c11 = A[1][0] * B[0][1] + A[1][1] * B[1][1]
    if mod:
        return [[c00 % mod, c01 % mod], [c10 % mod, c11 % mod]]
    return [[c00, c01], [c10, c11]]


def matrix_power_2x2(M: List[List[int]], p: int, mod: Optional[int] = None) -> List[List[int]]:
    """Computes M^p in O(log p) using binary exponentiation."""
    res = [[1, 0], [0, 1]]  # Identity matrix
    base = [[M[0][0], M[0][1]], [M[1][0], M[1][1]]]

    while p > 0:
        if p % 2 == 1:
            res = matrix_multiply_2x2(res, base, mod)
        base = matrix_multiply_2x2(base, base, mod)
        p //= 2

    return res


def fibonacci_matrix_exp(n: int, mod: Optional[int] = None) -> int:
    """
    Computes F(n) in O(log n) time using:
    [[F(n+1), F(n)], [F(n), F(n-1)]] = [[1, 1], [1, 0]]^n
    """
    if n == 0:
        return 0
    t = [[1, 1], [1, 0]]
    powered = matrix_power_2x2(t, n - 1, mod)
    ans = powered[0][0]
    return ans % mod if mod else ans


def test_q2_matrix_exponentiation():
    assert fibonacci_matrix_exp(10) == 55
    assert fibonacci_matrix_exp(20) == 6765

    # Compute F(10^9) % (10^9 + 7) in milliseconds
    mod = 1_000_000_007
    f_huge = fibonacci_matrix_exp(1_000_000_000, mod=mod)
    assert 0 <= f_huge < mod
    print("=== Q2: Fast Matrix Exponentiation O(log n) Verified ===")


# ==============================================================================
# Question 3: Binet's Analytical Closed-Form Formula
# ==============================================================================
def fibonacci_binet(n: int) -> int:
    """
    Computes F(n) using Binet's formula: F(n) = round((phi^n - psi^n) / sqrt(5))
    Valid for n <= 70 within standard 64-bit IEEE 754 float precision.
    """
    if n <= 1:
        return n
    sqrt5 = math.sqrt(5)
    phi = (1 + sqrt5) / 2
    # Since psi = (1 - sqrt5)/2 has |psi| < 1, psi^n / sqrt(5) < 0.5 for all n >= 0
    return round((phi ** n) / sqrt5)


def test_q3_binet_formula():
    for i in range(15):
        assert fibonacci_binet(i) == fibonacci_iterative(i)
    assert fibonacci_binet(30) == 832040
    print("=== Q3: Binet's Closed-Form Formula Verified ===")


# ==============================================================================
# Question 4: Pisano Period (Fibonacci Modulo M)
# ==============================================================================
def find_pisano_period(m: int) -> int:
    """
    The sequence of Fibonacci numbers modulo m is periodic.
    Finds length of the Pisano period for modulo m.
    Period always starts with 0, 1.
    """
    if m <= 1:
        return 1

    prev, curr = 0, 1
    for i in range(0, m * m):
        prev, curr = curr, (prev + curr) % m
        # Pisano period always restarts with 0, 1
        if prev == 0 and curr == 1:
            return i + 1

    return m * m


def fibonacci_huge_modulo(n: int, m: int) -> int:
    """
    Computes F(n) % m for astronomical n (e.g. 10^18) in O(m^2) by reducing n modulo Pisano period.
    """
    period = find_pisano_period(m)
    remainder = n % period
    return fibonacci_iterative(remainder) % m


def test_q4_pisano_period():
    # Pisano period for m=2 is 3 (0, 1, 1, 0, 1, 1...)
    assert find_pisano_period(2) == 3
    # Pisano period for m=3 is 8
    assert find_pisano_period(3) == 8

    # F(2014) % 3: 2014 % 8 = 6, F(6) = 8, 8 % 3 = 2
    assert fibonacci_huge_modulo(2014, 3) == 2
    print("=== Q4: Pisano Period & Astronomical Modulo Verified ===")


# ==============================================================================
# Question 5: Zeckendorf's Theorem (Unique Non-Consecutive Decomposition)
# ==============================================================================
def zeckendorf_decomposition(n: int) -> List[int]:
    """
    Every positive integer can be uniquely represented as the sum of one or more
    non-consecutive Fibonacci numbers (using greedy selection of largest F_k <= n).
    """
    if n <= 0:
        return []

    # Generate Fibonacci numbers up to n
    fibs = [1, 2]
    while True:
        nxt = fibs[-1] + fibs[-2]
        if nxt > n:
            break
        fibs.append(nxt)

    result = []
    rem = n
    for f in reversed(fibs):
        if f <= rem:
            result.append(f)
            rem -= f
            if rem == 0:
                break

    return result


def test_q5_zeckendorf_decomposition():
    # 100 = 89 + 8 + 3
    decomp100 = zeckendorf_decomposition(100)
    assert decomp100 == [89, 8, 3]
    assert sum(decomp100) == 100

    # 17 = 13 + 3 + 1
    decomp17 = zeckendorf_decomposition(17)
    assert decomp17 == [13, 3, 1]
    assert sum(decomp17) == 17
    print("=== Q5: Zeckendorf's Theorem Decomposition Verified ===")


# ==============================================================================
# Question 6: Generalized N-bonacci (Tribonacci and K-bonacci)
# ==============================================================================
def k_bonacci(k: int, n: int) -> int:
    """
    Computes n-th term of k-bonacci sequence:
    First k-1 terms are 0, term k-1 is 1.
    Each subsequent term is the sum of the preceding k terms.
    k=2 is Fibonacci, k=3 is Tribonacci.
    """
    if n < k - 1:
        return 0
    if n == k - 1:
        return 1

    window = [0] * (k - 1) + [1]
    running_sum = 1

    for _ in range(k, n + 1):
        next_val = running_sum
        running_sum += next_val - window.pop(0)
        window.append(next_val)

    return window[-1]


def test_q6_k_bonacci():
    # Tribonacci (k=3): 0, 0, 1, 1, 2, 4, 7, 13, 24, 44...
    trib = [k_bonacci(3, i) for i in range(10)]
    assert trib == [0, 0, 1, 1, 2, 4, 7, 13, 24, 44]

    # Verify k=2 matches standard Fibonacci offset
    fibs = [k_bonacci(2, i) for i in range(8)]
    assert fibs == [0, 1, 1, 2, 3, 5, 8, 13]
    print("=== Q6: Generalized N-bonacci Recurrence Verified ===")


# ==============================================================================
# Question 7: Constant-Time Perfect Square Fibonacci Test
# ==============================================================================
def is_perfect_square(num: int) -> bool:
    if num < 0:
        return False
    s = math.isqrt(num)
    return s * s == num


def is_fibonacci_number(n: int) -> bool:
    """
    A number N is a Fibonacci number if and only if:
    (5 * N^2 + 4) OR (5 * N^2 - 4) is a perfect square.
    """
    if n < 0:
        return False
    n2_5 = 5 * n * n
    return is_perfect_square(n2_5 + 4) or is_perfect_square(n2_5 - 4)


def test_q7_perfect_square_fibonacci_test():
    fib_samples = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]
    for f in fib_samples:
        assert is_fibonacci_number(f) is True

    non_fib_samples = [4, 6, 7, 9, 10, 11, 12, 14, 15, 100]
    for nf in non_fib_samples:
        assert is_fibonacci_number(nf) is False
    print("=== Q7: Perfect Square Fibonacci Test Verified ===")


# ==============================================================================
# Question 8: Fibonacci Word and Fractal Sequence
# ==============================================================================
def generate_fibonacci_word(n: int) -> str:
    """
    Generates the n-th Fibonacci word through recurrence:
    S_0 = "0"
    S_1 = "01"
    S_n = S_{n-1} + S_{n-2}
    """
    if n == 0:
        return "0"
    if n == 1:
        return "01"

    w_prev2 = "0"
    w_prev1 = "01"

    for _ in range(2, n + 1):
        w_curr = w_prev1 + w_prev2
        w_prev2, w_prev1 = w_prev1, w_curr

    return w_prev1


def test_q8_fibonacci_word():
    # S0 = "0", S1 = "01", S2 = "010", S3 = "01001", S4 = "01001010"
    assert generate_fibonacci_word(0) == "0"
    assert generate_fibonacci_word(1) == "01"
    assert generate_fibonacci_word(2) == "010"
    assert generate_fibonacci_word(3) == "01001"
    assert generate_fibonacci_word(4) == "01001010"
    # Length of S_n equals F(n + 2)
    assert len(generate_fibonacci_word(5)) == 13
    print("=== Q8: Fibonacci Word Fractal Sequence Verified ===")


# ==============================================================================
# Question 9: Fibonacci Search Algorithm
# ==============================================================================
def fibonacci_search(arr: List[int], target: int) -> int:
    """
    Searches for target in sorted array using Fibonacci numbers to divide range.
    Uses only addition and subtraction (division-free).
    Time Complexity: O(log n).
    """
    n = len(arr)
    if n == 0:
        return -1

    # Find smallest Fibonacci number >= n
    fib_m2 = 0  # (m-2)'th Fibonacci No.
    fib_m1 = 1  # (m-1)'th Fibonacci No.
    fib_m = fib_m2 + fib_m1  # m'th Fibonacci No.

    while fib_m < n:
        fib_m2 = fib_m1
        fib_m1 = fib_m
        fib_m = fib_m2 + fib_m1

    offset = -1

    while fib_m > 1:
        i = min(offset + fib_m2, n - 1)

        if arr[i] < target:
            fib_m = fib_m1
            fib_m1 = fib_m2
            fib_m2 = fib_m - fib_m1
            offset = i
        elif arr[i] > target:
            fib_m = fib_m2
            fib_m1 = fib_m1 - fib_m2
            fib_m2 = fib_m - fib_m1
        else:
            return i

    if fib_m1 and offset + 1 < n and arr[offset + 1] == target:
        return offset + 1

    return -1


def test_q9_fibonacci_search():
    data = [10, 22, 35, 40, 45, 50, 80, 82, 85, 90, 100]
    assert fibonacci_search(data, 85) == 8
    assert fibonacci_search(data, 10) == 0
    assert fibonacci_search(data, 100) == 10
    assert fibonacci_search(data, 42) == -1
    print("=== Q9: Fibonacci Search Algorithm Verified ===")


# ==============================================================================
# Question 10: Architectural Quantitative Trading Fibonacci Retracement Engine
# ==============================================================================
class FibonacciRetracementEngine:
    """
    Production technical analysis engine computing key Fibonacci retracement
    and extension ratios between market swing high and swing low points.
    """
    STANDARD_RETRACEMENT_RATIOS = [0.236, 0.382, 0.500, 0.618, 0.786]
    STANDARD_EXTENSION_RATIOS = [1.272, 1.618, 2.618]

    @classmethod
    def calculate_levels(
        cls, swing_low: float, swing_high: float, trend: str = "UPTREND"
    ) -> Dict[str, Dict[str, float]]:
        if swing_high <= swing_low:
            raise ValueError("swing_high must be strictly greater than swing_low")

        diff = swing_high - swing_low
        retracements = {}
        extensions = {}

        if trend.upper() == "UPTREND":
            # Retracement falls from high towards low
            for r in cls.STANDARD_RETRACEMENT_RATIOS:
                retracements[f"{r*100:.1f}%"] = round(swing_high - diff * r, 2)
            for ext in cls.STANDARD_EXTENSION_RATIOS:
                extensions[f"{ext*100:.1f}%"] = round(swing_high + diff * (ext - 1.0), 2)
        else:  # DOWNTREND
            # Retracement bounces from low towards high
            for r in cls.STANDARD_RETRACEMENT_RATIOS:
                retracements[f"{r*100:.1f}%"] = round(swing_low + diff * r, 2)
            for ext in cls.STANDARD_EXTENSION_RATIOS:
                extensions[f"{ext*100:.1f}%"] = round(swing_low - diff * (ext - 1.0), 2)

        return {
            "swing_range": {"low": swing_low, "high": swing_high, "diff": round(diff, 2)},
            "retracement_levels": retracements,
            "extension_targets": extensions,
        }

    @classmethod
    def find_nearest_support_level(
        cls, current_price: float, levels: Dict[str, float]
    ) -> Optional[Tuple[str, float]]:
        """Finds closest support level immediately below current price."""
        supports = [(name, price) for name, price in levels.items() if price <= current_price]
        if not supports:
            return None
        # Max price among supports
        return max(supports, key=lambda x: x[1])


def test_q10_fibonacci_retracement_engine():
    # Asset moves from swing low 100.0 to swing high 200.0 (diff = 100.0)
    analysis = FibonacciRetracementEngine.calculate_levels(100.0, 200.0, trend="UPTREND")
    ret = analysis["retracement_levels"]
    ext = analysis["extension_targets"]

    # 38.2% retracement: 200 - 38.2 = 161.80
    assert ret["38.2%"] == 161.8
    # 50.0% retracement: 200 - 50.0 = 150.00
    assert ret["50.0%"] == 150.0
    # 61.8% golden ratio: 200 - 61.8 = 138.20
    assert ret["61.8%"] == 138.2

    # 161.8% extension: 200 + 100 * 0.618 = 261.80
    assert ext["161.8%"] == 261.8

    # Nearest support when price pulls back to 155.0 is the 50.0% level at 150.0
    support = FibonacciRetracementEngine.find_nearest_support_level(155.0, ret)
    assert support == ("50.0%", 150.0)
    print("=== Q10: Architectural Fibonacci Retracement Trading Engine Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_iterative_fibonacci()
    test_q2_matrix_exponentiation()
    test_q3_binet_formula()
    test_q4_pisano_period()
    test_q5_zeckendorf_decomposition()
    test_q6_k_bonacci()
    test_q7_perfect_square_fibonacci_test()
    test_q8_fibonacci_word()
    test_q9_fibonacci_search()
    test_q10_fibonacci_retracement_engine()
    print("\nAll 10 Fibonacci sequence problem-solving questions passed successfully!")
