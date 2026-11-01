"""
Topic 06: List Comprehensions
Example 01: Mapping, Filtering (`if` at End), and Conditional Transformation (`if-else` at Front)

Demonstrates the exact syntax difference between filtering items out of a list
and transforming every item with a ternary expression inside a list comprehension.
"""


def main() -> None:
    numbers = list(range(1, 11))

    # 1. Pure Mapping: [expr for item in iterable]
    squares = [n * n for n in numbers]

    # 2. Filtering (if at the END): [expr for item in iterable if condition]
    even_squares = [n * n for n in numbers if n % 2 == 0]

    # 3. Conditional Transformation (if-else at the FRONT): [a if cond else b for item in iterable]
    parity_labels = [f"{n}:Even" if n % 2 == 0 else f"{n}:Odd" for n in numbers[:6]]

    print("=== 1. Mapping & Filtering List Comprehensions ===")
    print(f"Input Numbers (1..10) : {numbers}")
    print(f"All Squares           : {squares}")
    print(f"Even Squares (Filter) : {even_squares}")
    print(f"Parity Labels (if/else): {parity_labels}")

    # 4. Real-world string cleaning pipeline
    raw_emails = ["  DIVYA@example.com ", "invalid_email", " aarav@startup.io  ", ""]
    clean_valid_emails = [
        email.strip().lower()
        for email in raw_emails
        if "@" in email
    ]
    print("\n=== 2. Cleaned & Validated Emails ===")
    print(f"Cleaned Emails        : {clean_valid_emails}")


if __name__ == "__main__":
    main()
