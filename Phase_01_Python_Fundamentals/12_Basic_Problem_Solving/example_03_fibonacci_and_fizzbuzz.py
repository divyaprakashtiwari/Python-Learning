"""
Topic 12: Basic Problem Solving
Example 03: O(1)-Space Iterative Fibonacci and Extensible FizzBuzz

Demonstrates:
1. Computing the first N Fibonacci numbers using two rolling variables (`a, b = b, a + b`).
2. Writing a clean, extensible FizzBuzz engine without messy duplicate conditions.
"""


def generate_fibonacci(count: int) -> list[int]:
    """Return the first `count` Fibonacci numbers starting with 0, 1."""
    result: list[int] = []
    a, b = 0, 1
    for _ in range(count):
        result.append(a)
        a, b = b, a + b
    return result


def extensible_fizzbuzz(limit: int) -> list[str]:
    """Generate FizzBuzz output up to `limit` using extensible divisor rules."""
    rules = [(3, "Fizz"), (5, "Buzz")]
    output: list[str] = []

    for num in range(1, limit + 1):
        word = "".join(label for divisor, label in rules if num % divisor == 0)
        output.append(word if word else str(num))
    return output


def main() -> None:
    print("=== 1. First 12 Fibonacci Numbers ===")
    fib_12 = generate_fibonacci(12)
    print(f"  {fib_12}")

    print("\n=== 2. Extensible FizzBuzz (1 to 20) ===")
    fb_20 = extensible_fizzbuzz(20)
    print("  " + ", ".join(fb_20))


if __name__ == "__main__":
    main()
