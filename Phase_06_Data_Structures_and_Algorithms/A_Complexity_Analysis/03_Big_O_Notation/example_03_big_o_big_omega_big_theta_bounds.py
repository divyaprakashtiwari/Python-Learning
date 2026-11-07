"""
Phase 6 - Section A (Complexity Analysis) - Topic 03: Big O Notation
Example 03: Big O (Upper Bound), Big Omega (Lower Bound), & Big Theta (Tight Bound)

Demonstrates:
  - Verifying formal inequality definitions `c1 * g(n) <= T(n) <= c2 * g(n)` for all `n >= n0`
  - Why `T(n) = 2n + 5` is Theta(n), O(n), O(n^2), and Omega(n), but NOT Theta(n^2)
"""


def t_linear(n: int) -> int:
    return 2 * n + 5


def verify_theta_linear(c1: int, c2: int, n0: int, max_n: int = 100) -> bool:
    """Verify `c1 * n <= 2n + 5 <= c2 * n` for all `n` in `n0..max_n`."""
    return all(c1 * n <= t_linear(n) <= c2 * n for n in range(n0, max_n + 1))


def main() -> None:
    print("=== Formal Verification of Theta(n) Bounds for `T(n) = 2n + 5` ===")
    # For n >= 5: 2n <= 2n + 5 <= 3n
    c1, c2, n0 = 2, 3, 5
    holds = verify_theta_linear(c1=c1, c2=c2, n0=n0)
    print(f"  Does {c1}*n <= 2n + 5 <= {c2}*n hold for all n >= {n0}? {holds}")
    for sample_n in [5, 10, 50]:
        print(f"    n={sample_n:>2}: lower={c1 * sample_n:>3} <= T(n)={t_linear(sample_n):>3} <= upper={c2 * sample_n:>3}")


if __name__ == "__main__":
    main()
