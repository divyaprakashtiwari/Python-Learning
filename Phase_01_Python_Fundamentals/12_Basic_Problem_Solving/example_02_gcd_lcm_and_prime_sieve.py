"""
Topic 12: Basic Problem Solving
Example 02: Euclidean GCD & LCM and Sieve of Eratosthenes for Primes

Demonstrates:
1. Finding Greatest Common Divisor (GCD) in `O(log(min(a, b)))` using Euclid's algorithm.
2. Computing Least Common Multiple (LCM) safely via `(a // gcd(a, b)) * b`.
3. Generating all prime numbers up to `N` using the Sieve of Eratosthenes.
"""


def euclidean_gcd(a: int, b: int) -> int:
    """Compute GCD(a, b) using Euclid's iterative remainder algorithm."""
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def compute_lcm(a: int, b: int) -> int:
    """Compute LCM(a, b) using the identity a * b = GCD(a, b) * LCM(a, b)."""
    if a == 0 or b == 0:
        return 0
    return abs(a // euclidean_gcd(a, b) * b)


def sieve_of_eratosthenes(limit: int) -> list[int]:
    """Return all prime numbers <= limit in O(N log log N) time."""
    if limit < 2:
        return []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    p = 2
    while p * p <= limit:
        if is_prime[p]:
            # Mark multiples of p starting from p*p as composite
            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False
        p += 1

    return [num for num, prime_flag in enumerate(is_prime) if prime_flag]


def main() -> None:
    print("=== 1. Euclidean GCD & LCM ===")
    pairs = [(48, 18), (105, 35), (17, 23)]
    for x, y in pairs:
        print(f"  Pair ({x:>3}, {y:>2}) -> GCD: {euclidean_gcd(x, y):>2} | LCM: {compute_lcm(x, y):>3}")

    print("\n=== 2. Sieve of Eratosthenes (Primes <= 50) ===")
    primes_up_to_50 = sieve_of_eratosthenes(50)
    print(f"  Count: {len(primes_up_to_50)} primes")
    print(f"  Primes: {primes_up_to_50}")


if __name__ == "__main__":
    main()
