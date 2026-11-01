"""
Topic 09: Common Built-in Methods
Example 03: Numeric Built-ins (`divmod`, 3-Arg `pow`, `round`) and Object Inspection

Demonstrates:
1. `divmod(a, b)` returning `(a // b, a % b)` in a single operation.
2. Fast modular exponentiation `pow(base, exp, mod)` running in `O(log exp)` time.
3. Banker's round-half-to-even behavior in `round()`.
"""


def main() -> None:
    # 1. divmod(dividend, divisor) -> (quotient, remainder)
    total_minutes = 135
    hours, mins = divmod(total_minutes, 60)
    print("=== 1. Simultaneous Quotient & Remainder with divmod() ===")
    print(f"divmod(135, 60) -> {hours} hours, {mins} minutes")

    # 2. Fast Modular Exponentiation: pow(base, exp, mod)
    # Computes (2 ** 1000) % 1_000_000_007 in O(log(exp)) without huge intermediate ints!
    MOD = 1_000_000_007
    fast_mod_pow = pow(2, 1000, MOD)
    print("\n=== 2. Fast Modular Exponentiation: pow(base, exp, mod) ===")
    print(f"pow(2, 1000, 10^9 + 7) = {fast_mod_pow}")

    # 3. Banker's Rounding (Round Half to Even) in Python 3
    print("\n=== 3. Banker's Rounding (round half to nearest even integer) ===")
    print(f"round(2.5) -> {round(2.5)}  (rounds to even 2)")
    print(f"round(3.5) -> {round(3.5)}  (rounds to even 4)")

    # 4. Object Inspection: isinstance() and callable()
    print("\n=== 4. Object Inspection Built-ins ===")
    print(f"isinstance(42, (int, float)) : {isinstance(42, (int, float))}")
    print(f"callable(len)                : {callable(len)}")


if __name__ == "__main__":
    main()
