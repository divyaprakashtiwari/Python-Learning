"""
Phase 6 - Section A (Complexity Analysis) - Topic 01: Time Complexity
Example 02: Logarithmic O(log n) Halving & Linearithmic O(n log n) Divide-and-Conquer

Demonstrates:
  - How repeatedly halving a search space (`n //= 2`) finishes in at most `floor(log2(n)) + 1` steps
  - How running an O(log n) halving loop for each of `n` elements produces O(n log n) total steps
"""

import math


def count_halving_steps(n: int) -> int:
    """Count how many times `n` can be halved before reaching 0 -> O(log n)."""
    steps = 0
    current = n
    while current > 0:
        current //= 2
        steps += 1
    return steps


def count_n_log_n_steps(n: int) -> int:
    """Perform an O(log n) halving trace for each of `n` items -> O(n log n)."""
    total_steps = 0
    for _ in range(n):
        total_steps += count_halving_steps(n)
    return total_steps


def main() -> None:
    print("=== O(log n) and O(n log n) Step Counts vs Theoretical `floor(log2(n)) + 1` ===")
    for n in [8, 64, 1024, 1_048_576]:
        log_steps = count_halving_steps(n)
        expected = math.floor(math.log2(n)) + 1
        print(f"  N = {n:>9,} -> O(log n) steps = {log_steps:>2} (expected={expected:>2})")

    print("\n=== O(n log n) Total Steps on Moderate Input Sizes ===")
    for n in [16, 128, 1024]:
        print(f"  N = {n:>5,} -> O(n log n) steps = {count_n_log_n_steps(n):>8,}")


if __name__ == "__main__":
    main()
