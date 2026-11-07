"""
Phase 6 - Section A (Complexity Analysis) - Topic 01: Time Complexity
Example 01: Counting Exact Primitive Operations — O(1) Formula vs O(n) Loop vs O(n^2) Nested Loop

Demonstrates:
  - Why operation counts (not raw wall-clock seconds alone) measure algorithmic time complexity
  - Comparing Gauss's O(1) closed-form sum against an O(n) single loop and O(n^2) nested unit-addition loop
"""


def sum_o1_formula(n: int) -> tuple[int, int]:
    """Return `(total, step_count)` using Gauss's O(1) formula `n * (n + 1) // 2`."""
    steps = 1
    return (n * (n + 1)) // 2, steps


def sum_on_loop(n: int) -> tuple[int, int]:
    """Return `(total, step_count)` using a single O(n) loop."""
    total = 0
    steps = 0
    for i in range(1, n + 1):
        total += i
        steps += 1
    return total, steps


def sum_on2_nested(n: int) -> tuple[int, int]:
    """Return `(total, step_count)` using a naive O(n^2) nested loop."""
    total = 0
    steps = 0
    for i in range(1, n + 1):
        for _ in range(i):
            total += 1
            steps += 1
    return total, steps


def main() -> None:
    print("=== Operation Count Scaling Across Input Sizes N ===")
    print(f"  {'N':>5} | {'O(1) Steps':>12} | {'O(n) Steps':>12} | {'O(n^2) Steps':>14} | {'All Sums Equal?':>15}")
    print("  " + "-" * 68)
    for n in [10, 50, 200]:
        s1, c1 = sum_o1_formula(n)
        s2, c2 = sum_on_loop(n)
        s3, c3 = sum_on2_nested(n)
        equal = s1 == s2 == s3
        print(f"  {n:>5} | {c1:>12,} | {c2:>12,} | {c3:>14,} | {str(equal):>15}")


if __name__ == "__main__":
    main()
