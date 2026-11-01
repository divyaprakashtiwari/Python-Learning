"""
Topic 04: Data Types
Example 03: Mutable vs Immutable Types & Floating-Point Precision

Demonstrates:
1. Why `int` and `str` are immutable while `list` is mutable.
2. Why `0.1 + 0.2 != 0.3` in binary floating-point and how to compare floats
   accurately using `math.isclose()` and `decimal.Decimal`.
"""

from decimal import Decimal
import math


def main() -> None:
    # 1. Immutable vs Mutable behavior
    print("=== 1. Immutable (int/str) vs Mutable (list) ===")
    word = "Py"
    initial_word_id = id(word)
    word += "thon"
    print(f"String after '+=' changed memory ID : {initial_word_id != id(word)} (Value: {word})")

    numbers = [10, 20]
    initial_list_id = id(numbers)
    numbers.append(30)
    print(f"List after '.append()' kept same ID : {initial_list_id == id(numbers)} (Value: {numbers})")

    # 2. IEEE-754 Floating-Point Precision
    print("\n=== 2. Floating-Point Precision (0.1 + 0.2) ===")
    float_sum = 0.1 + 0.2
    print(f"Raw float (0.1 + 0.2)            : {float_sum:.17f}")
    print(f"Direct equality (0.1 + 0.2 == 0.3): {float_sum == 0.3}")
    print(f"Safe check with math.isclose()   : {math.isclose(float_sum, 0.3)}")

    exact_sum = Decimal("0.1") + Decimal("0.2")
    print(f"Exact Decimal('0.1') + Decimal('0.2') == Decimal('0.3'): {exact_sum == Decimal('0.3')} (Value: {exact_sum})")


if __name__ == "__main__":
    main()
