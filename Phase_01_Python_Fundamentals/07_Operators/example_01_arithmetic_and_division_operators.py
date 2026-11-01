"""
Topic 07: Operators
Example 01: Arithmetic Operators (`/`, `//`, `%`, `**`) and Time Conversion

Demonstrates the difference between true division (`/`) and floor division (`//`),
modulo (`%`), exponentiation (`**`), and a practical seconds-to-HH:MM:SS converter.
"""


def format_duration(total_seconds: int) -> str:
    """Convert total seconds into HH:MM:SS using floor division (//) and modulo (%)."""
    hours = total_seconds // 3600
    remaining_after_hours = total_seconds % 3600
    minutes = remaining_after_hours // 60
    seconds = remaining_after_hours % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def main() -> None:
    a, b = 17, 5
    print("=== 1. Core Arithmetic Operators ===")
    print(f"{a} + {b}  = {a + b}   (Addition)")
    print(f"{a} - {b}  = {a - b}   (Subtraction)")
    print(f"{a} * {b}  = {a * b}   (Multiplication)")
    print(f"{a} / {b}  = {a / b}  (True Division -> always float)")
    print(f"{a} // {b} = {a // b}    (Floor Division -> quotient)")
    print(f"{a} % {b}  = {a % b}    (Modulo -> remainder)")
    print(f"2 ** 10 = {2 ** 10} (Exponentiation)")

    # Negative floor division & modulo invariant: a == (a // b) * b + (a % b)
    print("\n=== 2. Negative Floor Division & Modulo Invariant ===")
    neg_a = -17
    print(f"{neg_a} // {b} = {neg_a // b} (rounds down toward -infinity)")
    print(f"{neg_a} % {b}  = {neg_a % b}  (because (-4 * 5) + 3 == -17)")

    print("\n=== 3. Real-World Seconds to HH:MM:SS Converter ===")
    for sec in [3661, 7384, 86399]:
        print(f"  {sec:>5} seconds -> {format_duration(sec)}")


if __name__ == "__main__":
    main()
