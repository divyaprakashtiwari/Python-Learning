"""
Topic 03: Variables and Constants
Example 03: Constants (PEP 8 & typing.Final) and Object Identity

Demonstrates how to define constants in Python using UPPER_SNAKE_CASE and
`typing.Final`, and illustrates how variables point to objects in memory.
"""

from typing import Final

# Module-level constants (PEP 8 convention: UPPER_SNAKE_CASE)
SPEED_OF_LIGHT_M_S: Final[int] = 299_792_458
GST_RATE: Final[float] = 0.18
DEFAULT_CURRENCY: Final[str] = "INR"


def calculate_invoice_total(base_amount: float) -> float:
    """Calculate total invoice amount using the module-level GST_RATE constant."""
    tax_amount = base_amount * GST_RATE
    return round(base_amount + tax_amount, 2)


def main() -> None:
    course_price = 1500.00
    final_price = calculate_invoice_total(course_price)

    print("=== Constants in Action ===")
    print(f"Speed of Light : {SPEED_OF_LIGHT_M_S:,} m/s")
    print(f"Base Price     : {DEFAULT_CURRENCY} {course_price:.2f}")
    print(f"GST Rate       : {GST_RATE * 100:.0f}%")
    print(f"Final Invoice  : {DEFAULT_CURRENCY} {final_price:.2f}")

    # Object reference & identity demonstration
    a = 100
    b = a
    print("\n=== Object Reference Verification ===")
    print(f"a == b                 : {a == b}")
    print(f"a is b (same memory)   : {a is b}")
    b = 200
    print(f"After rebinding b=200  : a={a}, b={b}, (a is b)={a is b}")


if __name__ == "__main__":
    main()
