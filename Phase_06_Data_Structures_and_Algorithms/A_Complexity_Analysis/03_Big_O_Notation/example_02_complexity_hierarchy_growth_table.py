"""
Phase 6 - Section A (Complexity Analysis) - Topic 03: Big O Notation
Example 02: The Big O Growth Hierarchy — O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(2^n)

Demonstrates:
  - Tabulating the 6 major complexity classes side by side to see why O(2^n) and O(n^2)
    hit Time Limit Exceeded (TLE) at ~10^8 operations per second
"""

import math


def main() -> None:
    print("=== Complexity Class Growth Comparison Table ===")
    header = f"  {'N':>4} | {'O(1)':>4} | {'O(log2 n)':>9} | {'O(n)':>6} | {'O(n log2 n)':>11} | {'O(n^2)':>10} | {'O(2^n)':>12}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for n in [2, 8, 16, 32]:
        o_1 = 1
        o_log = int(math.log2(n))
        o_n = n
        o_nlogn = n * o_log
        o_n2 = n * n
        o_2n = 1 << n
        print(f"  {n:>4} | {o_1:>4} | {o_log:>9} | {o_n:>6} | {o_nlogn:>11} | {o_n2:>10,} | {o_2n:>12,}")


if __name__ == "__main__":
    main()
