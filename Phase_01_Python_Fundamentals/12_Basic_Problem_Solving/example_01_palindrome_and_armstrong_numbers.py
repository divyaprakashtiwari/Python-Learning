"""
Topic 12: Basic Problem Solving
Example 01: Mathematical Integer Reversal, Palindrome Check, and Armstrong Numbers

Demonstrates solving classic placement numeric problems in `O(d)` time (where `d`
is the number of digits) without converting integers to strings.
"""


def reverse_integer(n: int) -> int:
    """Reverse the digits of an integer mathematically (preserving sign)."""
    sign = -1 if n < 0 else 1
    remaining = abs(n)
    reversed_num = 0
    while remaining > 0:
        reversed_num = (reversed_num * 10) + (remaining % 10)
        remaining //= 10
    return sign * reversed_num


def is_palindrome_number(n: int) -> bool:
    """Negative numbers are not palindromes; non-negative numbers match their reverse."""
    if n < 0:
        return False
    return n == reverse_integer(n)


def is_armstrong_number(n: int) -> bool:
    """
    Check if a positive integer equals the sum of its digits each raised to
    the power of the number of digits (e.g., 153 = 1^3 + 5^3 + 3^3).
    """
    if n < 0:
        return False
    # Count digits
    temp = n
    num_digits = 1 if n == 0 else 0
    while temp > 0:
        num_digits += 1
        temp //= 10

    # Sum d ** num_digits
    temp = n
    powered_sum = 0
    while temp > 0:
        digit = temp % 10
        powered_sum += digit ** num_digits
        temp //= 10
    return powered_sum == n


def main() -> None:
    print("=== 1. Integer Reversal & Palindrome Check ===")
    for num in [12321, 4500, -121, 9009]:
        print(f"  n={num:>6} | reversed={reverse_integer(num):>6} | palindrome={is_palindrome_number(num)}")

    print("\n=== 2. Armstrong Numbers up to 10,000 ===")
    armstrong_list = [x for x in range(1, 10000) if is_armstrong_number(x)]
    print(f"  Found: {armstrong_list}")


if __name__ == "__main__":
    main()
