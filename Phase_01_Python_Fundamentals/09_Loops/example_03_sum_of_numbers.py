"""
Topic 09: Loops (for, while)
Example 03: Summing Numbers (`for` Accumulator vs `while` Digit Extraction)

Demonstrates:
1. Summing 1..N using a `for` loop accumulator (and verifying with `N * (N + 1) // 2`).
2. Summing the individual digits of an integer using a `while` loop (`n % 10` and `n //= 10`).
"""


def sum_first_n_numbers(n: int) -> int:
    """Compute 1 + 2 + ... + n using an explicit for-loop accumulator."""
    total = 0
    for current in range(1, n + 1):
        total += current
    return total


def sum_of_digits(number: int) -> int:
    """Extract and sum all digits of a non-negative integer using a while loop."""
    remaining = abs(number)
    digit_sum = 0
    while remaining > 0:
        last_digit = remaining % 10
        digit_sum += last_digit
        remaining //= 10
    return digit_sum


def main() -> None:
    n = 100
    loop_sum = sum_first_n_numbers(n)
    formula_sum = n * (n + 1) // 2
    print("=== 1. Sum of First N Natural Numbers ===")
    print(f"Sum of 1..{n} (for loop)      : {loop_sum}")
    print(f"Sum of 1..{n} (Gauss formula) : {formula_sum}")

    print("\n=== 2. Sum of Digits using a while Loop ===")
    for sample in [9875, 2026, 100001]:
        print(f"  Number: {sample:>6} -> Sum of digits: {sum_of_digits(sample)}")


if __name__ == "__main__":
    main()
