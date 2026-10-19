"""
Topic: Problem Solving - Prime Numbers
--------------------------------------
Questions Covered:
1. Fast Primality Test (6k +/- 1 Optimization): Trial division testing up to sqrt(n).
2. Sieve of Eratosthenes: Classical prime sieve generating all primes <= N in O(n log log n).
3. Segmented Sieve: Memory-bounded prime generation across arbitrary range [L, R].
4. Prime Factorization with Exponent Powers: Decomposing integers into unique prime powers.
5. Miller-Rabin Primality Test: Deterministic 64-bit probabilistic primality verification.
6. Euler's Totient Function (Phi): Counting coprime residues using prime factor decomposition.
7. Goldbach's Conjecture Verification: Decomposing even integers > 2 into pairs of primes.
8. Prime Constellations (Twin and Cousin Primes): Sieve-backed gap pattern search.
9. Pollard's Rho Integer Factorization: Cycle-finding integer factorization for composite numbers.
10. Architectural System: Cryptographic RSA Key Pair Generation Pipeline with Extended Euclidean GCD.
"""

import math
import random
from typing import List, Tuple, Optional, Any, Dict, Set


# ==============================================================================
# Question 1: Fast Primality Test (6k +/- 1 Optimization)
# ==============================================================================
def is_prime(n: int) -> bool:
    """
    Checks if n is prime in O(sqrt(n)) time using 6k +/- 1 wheel optimization.
    All primes > 3 can be expressed in form 6k - 1 or 6k + 1.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True


def test_q1_fast_primality():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 97, 101, 1009]
    for p in primes:
        assert is_prime(p) is True

    non_primes = [0, 1, 4, 6, 8, 9, 15, 25, 27, 49, 100, 1007]
    for np in non_primes:
        assert is_prime(np) is False
    print("=== Q1: Fast Primality Test (6k +/- 1) Verified ===")


# ==============================================================================
# Question 2: Sieve of Eratosthenes
# ==============================================================================
def sieve_of_eratosthenes(limit: int) -> List[int]:
    """
    Computes all prime numbers up to limit in O(n log log n) time.
    """
    if limit < 2:
        return []

    is_prime_arr = [True] * (limit + 1)
    is_prime_arr[0] = is_prime_arr[1] = False

    p = 2
    while p * p <= limit:
        if is_prime_arr[p]:
            for multiple in range(p * p, limit + 1, p):
                is_prime_arr[multiple] = False
        p += 1

    return [i for i, prime in enumerate(is_prime_arr) if prime]


def test_q2_sieve():
    primes_up_to_30 = sieve_of_eratosthenes(30)
    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert primes_up_to_30 == expected
    assert len(sieve_of_eratosthenes(100)) == 25
    print("=== Q2: Sieve of Eratosthenes Verified ===")


# ==============================================================================
# Question 3: Segmented Sieve for Range [L, R]
# ==============================================================================
def segmented_sieve(low: int, high: int) -> List[int]:
    """
    Finds all primes in the range [low, high] with O(sqrt(high) + (high - low + 1)) memory.
    """
    if high < 2 or low > high:
        return []

    # 1. Generate base primes up to sqrt(high)
    limit = int(math.isqrt(high))
    base_primes = sieve_of_eratosthenes(limit)

    # 2. Boolean array for range [low, high]
    range_len = high - low + 1
    is_prime_range = [True] * range_len

    for p in base_primes:
        # Find smallest multiple of p >= low
        start = max(p * p, ((low + p - 1) // p) * p)
        for multiple in range(start, high + 1, p):
            is_prime_range[multiple - low] = False

    result = []
    for i in range(range_len):
        num = low + i
        if is_prime_range[i] and num >= 2:
            result.append(num)

    return result


def test_q3_segmented_sieve():
    # Primes between 50 and 80: 53, 59, 61, 67, 71, 73, 79
    res = segmented_sieve(50, 80)
    expected = [53, 59, 61, 67, 71, 73, 79]
    assert res == expected
    print("=== Q3: Segmented Sieve Range [L, R] Verified ===")


# ==============================================================================
# Question 4: Prime Factorization with Exponent Powers
# ==============================================================================
def prime_factors_decomposition(n: int) -> List[Tuple[int, int]]:
    """
    Returns prime factorization of n as list of (prime, exponent) pairs.
    e.g. 360 = 2^3 * 3^2 * 5^1 -> [(2, 3), (3, 2), (5, 1)].
    """
    if n <= 1:
        return []

    factors: List[Tuple[int, int]] = []
    d = 2

    while d * d <= n:
        if n % d == 0:
            count = 0
            while n % d == 0:
                count += 1
                n //= d
            factors.append((d, count))
        d += 1 if d == 2 else 2

    if n > 1:
        factors.append((n, 1))

    return factors


def test_q4_prime_factorization():
    f360 = prime_factors_decomposition(360)
    assert f360 == [(2, 3), (3, 2), (5, 1)]

    f13 = prime_factors_decomposition(13)
    assert f13 == [(13, 1)]
    print("=== Q4: Prime Factorization with Powers Verified ===")


# ==============================================================================
# Question 5: Miller-Rabin Deterministic Primality Test
# ==============================================================================
def miller_rabin_test(n: int) -> bool:
    """
    Deterministic Miller-Rabin primality test for 64-bit integers.
    Uses known deterministic base set: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37].
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Write n - 1 as 2^r * d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for a in bases:
        if n <= a:
            break
        # Compute x = a^d % n
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def test_q5_miller_rabin():
    # Large 64-bit prime: 1000000007, 2147483647 (Mersenne prime 2^31 - 1)
    assert miller_rabin_test(1_000_000_007) is True
    assert miller_rabin_test(2_147_483_647) is True
    # Carmichael numbers (pseudo-primes that fool Fermat test, e.g. 561 = 3 * 11 * 17)
    assert miller_rabin_test(561) is False
    assert miller_rabin_test(1105) is False
    print("=== Q5: Miller-Rabin Deterministic Primality Test Verified ===")


# ==============================================================================
# Question 6: Euler's Totient Function Phi(n)
# ==============================================================================
def euler_totient(n: int) -> int:
    """
    Computes count of numbers k (1 <= k <= n) coprime to n: gcd(k, n) == 1.
    Formula: phi(n) = n * prod((1 - 1/p)) for all distinct prime factors p of n.
    """
    if n <= 0:
        return 0

    result = n
    p = 2
    temp = n

    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1

    if temp > 1:
        result -= result // temp

    return result


def test_q6_euler_totient():
    # phi(9) = 6 (coprimes: 1, 2, 4, 5, 7, 8)
    assert euler_totient(9) == 6
    # For prime p, phi(p) = p - 1
    assert euler_totient(13) == 12
    # phi(36) = 12
    assert euler_totient(36) == 12
    print("=== Q6: Euler's Totient Function Verified ===")


# ==============================================================================
# Question 7: Goldbach's Conjecture Verification
# ==============================================================================
def goldbach_pair(even_num: int) -> Optional[Tuple[int, int]]:
    """
    Every even integer > 2 can be expressed as sum of two primes.
    Finds pair of primes (p1, p2) such that p1 + p2 == even_num and p1 <= p2.
    """
    if even_num <= 2 or even_num % 2 != 0:
        return None

    for p in range(2, even_num // 2 + 1):
        if is_prime(p) and is_prime(even_num - p):
            return (p, even_num - p)

    return None


def test_q7_goldbach():
    assert goldbach_pair(4) == (2, 2)
    assert goldbach_pair(10) == (3, 7)
    assert goldbach_pair(28) == (5, 23)
    assert goldbach_pair(100) == (3, 97)
    assert goldbach_pair(9) is None  # Odd
    print("=== Q7: Goldbach's Conjecture Verification Verified ===")


# ==============================================================================
# Question 8: Twin and Cousin Primes Generator
# ==============================================================================
def find_prime_pairs_with_gap(limit: int, gap: int) -> List[Tuple[int, int]]:
    """
    Finds all prime pairs (p1, p2) <= limit such that p2 - p1 == gap.
    gap=2 -> Twin Primes
    gap=4 -> Cousin Primes
    """
    primes = sieve_of_eratosthenes(limit)
    prime_set = set(primes)
    pairs = []

    for p in primes:
        if (p + gap) in prime_set and (p + gap) <= limit:
            pairs.append((p, p + gap))

    return pairs


def test_q8_prime_pairs():
    # Twin primes <= 30 (gap 2): (3, 5), (5, 7), (11, 13), (17, 19)
    twins = find_prime_pairs_with_gap(30, gap=2)
    assert twins == [(3, 5), (5, 7), (11, 13), (17, 19)]

    # Cousin primes <= 30 (gap 4): (3, 7), (7, 11), (13, 17), (19, 23)
    cousins = find_prime_pairs_with_gap(30, gap=4)
    assert cousins == [(3, 7), (7, 11), (13, 17), (19, 23)]
    print("=== Q8: Twin and Cousin Prime Pairs Verified ===")


# ==============================================================================
# Question 9: Pollard's Rho Integer Factorization
# ==============================================================================
def pollards_rho_factor(n: int) -> int:
    """
    Finds a non-trivial factor of composite n using Pollard's Rho algorithm with polynomial
    f(x) = (x^2 + 1) % n and Floyd's cycle-finding tortoise and hare.
    """
    if n % 2 == 0:
        return 2

    x = 2
    y = 2
    c = 1
    d = 1

    f = lambda val: (val * val + c) % n

    while d == 1:
        x = f(x)
        y = f(f(y))
        d = math.gcd(abs(x - y), n)
        if d == n:
            # Retry with different starting polynomial offset
            c += 1
            x = 2
            y = 2
            d = 1

    return d


def test_q9_pollards_rho():
    comp1 = 8051  # 83 * 97
    factor1 = pollards_rho_factor(comp1)
    assert factor1 in (83, 97)
    assert comp1 % factor1 == 0

    comp2 = 10403  # 101 * 103
    factor2 = pollards_rho_factor(comp2)
    assert factor2 in (101, 103)
    print("=== Q9: Pollard's Rho Integer Factorization Verified ===")


# ==============================================================================
# Question 10: Architectural Cryptographic RSA Primality Pipeline
# ==============================================================================
def extended_euclidean_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Returns (gcd, x, y) such that a*x + b*y == gcd."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_euclidean_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def modular_inverse(e: int, phi: int) -> int:
    """Computes d such that (d * e) % phi == 1."""
    gcd, x, _ = extended_euclidean_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % phi + phi) % phi


class CryptoPrimeEngine:
    """
    Production cryptographic pipeline for RSA key generation:
    1. Selects primes p and q
    2. Computes modulus n = p * q and totient phi = (p - 1) * (q - 1)
    3. Selects public exponent e coprime to phi
    4. Computes private exponent d = e^-1 mod phi
    5. Performs integer block encryption and decryption
    """
    @classmethod
    def generate_key_pair(cls, p: int, q: int, e: int = 65537) -> Dict[str, Any]:
        if not miller_rabin_test(p) or not miller_rabin_test(q):
            raise ValueError("p and q must be prime numbers")
        if p == q:
            raise ValueError("p and q must be distinct primes")

        n = p * q
        phi = (p - 1) * (q - 1)

        if math.gcd(e, phi) != 1:
            # Fallback to smaller public exponent if gcd != 1
            for candidate_e in [3, 5, 17, 257]:
                if math.gcd(candidate_e, phi) == 1:
                    e = candidate_e
                    break

        d = modular_inverse(e, phi)
        return {
            "public_key": {"e": e, "n": n},
            "private_key": {"d": d, "n": n},
            "modulus": n,
            "phi": phi,
        }

    @classmethod
    def encrypt(cls, plaintext_int: int, public_key: Dict[str, int]) -> int:
        e = public_key["e"]
        n = public_key["n"]
        if plaintext_int >= n:
            raise ValueError("Message integer must be less than modulus n")
        return pow(plaintext_int, e, n)

    @classmethod
    def decrypt(cls, ciphertext_int: int, private_key: Dict[str, int]) -> int:
        d = private_key["d"]
        n = private_key["n"]
        return pow(ciphertext_int, d, n)


def test_q10_crypto_prime_rsa_pipeline():
    # Use distinct primes
    p = 61
    q = 53
    keys = CryptoPrimeEngine.generate_key_pair(p, q, e=17)

    assert keys["modulus"] == 61 * 53  # 3233
    assert keys["phi"] == 60 * 52      # 3120

    pub = keys["public_key"]
    priv = keys["private_key"]

    # Encrypt integer secret
    secret_msg = 65
    ciphertext = CryptoPrimeEngine.encrypt(secret_msg, pub)
    decrypted = CryptoPrimeEngine.decrypt(ciphertext, priv)

    assert decrypted == secret_msg
    print("=== Q10: Architectural Cryptographic RSA Primality Pipeline Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_fast_primality()
    test_q2_sieve()
    test_q3_segmented_sieve()
    test_q4_prime_factorization()
    test_q5_miller_rabin()
    test_q6_euler_totient()
    test_q7_goldbach()
    test_q8_prime_pairs()
    test_q9_pollards_rho()
    test_q10_crypto_prime_rsa_pipeline()
    print("\nAll 10 prime number problem-solving questions passed successfully!")
