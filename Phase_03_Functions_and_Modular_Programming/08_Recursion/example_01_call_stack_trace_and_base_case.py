"""
Phase 3 - Topic 08: Recursion
Example 01: Anatomy of Recursion (Base Case, Recursive Step & Call Stack Trace)

Demonstrates:
  - How every recursive function requires a Base Case and a Recursive Step
  - Visualizing the Call Stack: Winding phase (pushing frames) vs Unwinding phase (returning)
  - Fast exponentiation (`power_fast`) in O(log n) recursive steps
"""


def factorial_traced(n: int, depth: int = 0) -> int:
    """Compute n! while printing the winding and unwinding call stack frames."""
    indent = "  " * (depth + 1)
    print(f"{indent}-> Enter factorial_traced(n={n})")

    # 1. Base Case: stops the recursion
    if n <= 1:
        print(f"{indent}<- Base case reached! Returning 1")
        return 1

    # 2. Recursive Step: problem reduced from `n` to `n - 1`
    sub_result = factorial_traced(n - 1, depth + 1)
    total = n * sub_result
    print(f"{indent}<- Unwinding n={n}: {n} * {sub_result} = {total}")
    return total


def power_fast(base: int, exp: int) -> int:
    """Compute `base ** exp` in O(log exp) time using binary exponentiation."""
    if exp == 0:
        return 1
    half = power_fast(base, exp // 2)
    if exp % 2 == 0:
        return half * half
    return base * half * half


def main() -> None:
    print("=== 1. Call Stack Trace for `factorial_traced(4)` ===")
    ans = factorial_traced(4)
    print(f"  Final Result: 4! = {ans}")

    print("\n=== 2. O(log n) Recursive Binary Exponentiation ===")
    print(f"  power_fast(2, 10) = {power_fast(2, 10)}")
    print(f"  power_fast(3, 7)  = {power_fast(3, 7)}")


if __name__ == "__main__":
    main()
