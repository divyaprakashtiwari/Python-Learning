"""
Phase 6 - Section A (Complexity Analysis) - Topic 03: Big O Notation
Example 01: Asymptotic Dominance — Why Constants and Lower-Order Terms Drop Out as N Grows

Demonstrates:
  - Comparing `T(n) = 3n^2 + 50n + 1000` against `3n^2` as `n` grows from `10` to `10,000`
  - Showing quantitatively that the `3n^2` dominant term accounts for >99.8% of total operations at large N
"""


def exact_cost(n: int) -> tuple[int, int, float]:
    """Return `(total_ops, quadratic_term_ops, quadratic_share_pct)` for T(n) = 3n^2 + 50n + 1000."""
    quad = 3 * (n**2)
    linear = 50 * n
    constant = 1000
    total = quad + linear + constant
    share_pct = (quad / total) * 100.0
    return total, quad, share_pct


def main() -> None:
    print("=== Asymptotic Dominance of `3n^2` in `T(n) = 3n^2 + 50n + 1000` ===")
    print(f"  {'N':>7} | {'Total T(n)':>15} | {'3n^2 Term':>15} | {'3n^2 Share (%)':>14}")
    print("  " + "-" * 59)
    for n in [10, 100, 1_000, 10_000]:
        total, quad, pct = exact_cost(n)
        print(f"  {n:>7,} | {total:>15,} | {quad:>15,} | {pct:>13.2f}%")


if __name__ == "__main__":
    main()
