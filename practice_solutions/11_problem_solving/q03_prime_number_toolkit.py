"""
Question 3: Prime Number Toolkit & Number-Theoretic Algorithms
Topic: Problem Solving & Competitive Programming Patterns

Key Concepts Tested:
- Fast 6k +/- 1 primality testing in O(sqrt(N)) time
- Sieve of Eratosthenes with bytearray cross-off in O(N log log N) time
- Prime factorization returning factor multiplicities
- Goldbach's conjecture decomposition for even integers
"""

import math
from typing import List, Dict, Tuple


class PrimeToolkit:
    """
    Comprehensive toolkit for prime number generation, testing,
    factorization, and conjecture decomposition.
    """

    @staticmethod
    def is_prime(n: int) -> bool:
        """
        Fast primality test using 6k +/- 1 wheel factorization.
        Runs in O(sqrt(N)) time and O(1) space.
        """
        if n < 2:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False

        # Check factors of form 6k - 1 and 6k + 1 up to sqrt(n)
        limit = math.isqrt(n)
        factor = 5
        while factor <= limit:
            if n % factor == 0 or n % (factor + 2) == 0:
                return False
            factor += 6

        return True

    @staticmethod
    def sieve_primes(limit: int) -> List[int]:
        """
        Generates all prime numbers up to limit using the Sieve of Eratosthenes.
        Returns primes in ascending order.
        """
        if limit < 2:
            return []

        # Use memory-efficient bytearray
        is_prime_mask = bytearray([1]) * (limit + 1)
        is_prime_mask[0] = is_prime_mask[1] = 0

        p = 2
        while p * p <= limit:
            if is_prime_mask[p]:
                # Cross off multiples starting from p * p
                is_prime_mask[p * p : limit + 1 : p] = bytearray(
                    len(range(p * p, limit + 1, p))
                )
            p += 1

        return [i for i, prime in enumerate(is_prime_mask) if prime]

    @staticmethod
    def prime_factorization(n: int) -> Dict[int, int]:
        """
        Decomposes integer n >= 2 into prime factors with their multiplicities.
        Returns mapping {prime_factor: exponent}.
        """
        if n <= 1:
            raise ValueError(f"Prime factorization requires integer >= 2, got: {n}")

        factors: Dict[int, int] = {}
        temp = n

        # Factor out 2s
        while temp % 2 == 0:
            factors[2] = factors.get(2, 0) + 1
            temp //= 2

        # Factor out 3s
        while temp % 3 == 0:
            factors[3] = factors.get(3, 0) + 1
            temp //= 3

        # Factor out 6k +/- 1
        d = 5
        while d * d <= temp:
            while temp % d == 0:
                factors[d] = factors.get(d, 0) + 1
                temp //= d
            while temp % (d + 2) == 0:
                factors[d + 2] = factors.get(d + 2, 0) + 1
                temp //= (d + 2)
            d += 6

        if temp > 1:
            factors[temp] = factors.get(temp, 0) + 1

        return factors

    def goldbach_pair(self, even_num: int) -> Tuple[int, int]:
        """
        Finds the Goldbach pair (p1, p2) such that p1 + p2 == even_num
        with smallest prime p1 <= p2.
        """
        if even_num <= 2 or even_num % 2 != 0:
            raise ValueError(f"Goldbach conjecture requires an even integer > 2, got: {even_num}")

        for p1 in range(2, (even_num // 2) + 1):
            p2 = even_num - p1
            if self.is_prime(p1) and self.is_prime(p2):
                return (p1, p2)

        raise ValueError(f"No Goldbach pair found for {even_num}")


if __name__ == "__main__":
    toolkit = PrimeToolkit()

    print("=== 1. Primality Testing ===")
    p1 = toolkit.is_prime(29)
    p2 = toolkit.is_prime(1)
    p3 = toolkit.is_prime(49)
    print(f"is_prime(29): {p1}")
    print(f"is_prime(1): {p2}")
    print(f"is_prime(49): {p3}")

    print("\n=== 2. Sieve of Eratosthenes ===")
    primes_up_to_30 = toolkit.sieve_primes(30)
    print(f"Sieve Primes up to 30: {primes_up_to_30}")

    print("\n=== 3. Prime Factorization ===")
    factors_360 = toolkit.prime_factorization(360)
    print(f"Prime Factorization of 360: {factors_360}")

    print("\n=== 4. Goldbach Conjecture Pair ===")
    goldbach_28 = toolkit.goldbach_pair(28)
    print(f"Goldbach Pair for 28: {goldbach_28}  # {goldbach_28[0]} + {goldbach_28[1]} = 28")

    print("\n=== 5. Edge Cases & Constraints ===")
    print(f"Sieve limit < 2: {toolkit.sieve_primes(1)}")
    try:
        toolkit.prime_factorization(1)
    except ValueError as err:
        print(f"Caught factorize <= 1: {err}")

    try:
        toolkit.goldbach_pair(27)  # Odd number
    except ValueError as err:
        print(f"Caught odd number Goldbach: {err}")
