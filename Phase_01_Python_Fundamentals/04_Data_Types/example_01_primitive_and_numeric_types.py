"""
Topic 04: Data Types
Example 01: Primitive and Numeric Data Types in Python

Demonstrates `int` (including arbitrary-precision large integers and binary/hex literals),
`float`, `complex`, `bool`, `str`, and `NoneType`.
"""


def main() -> None:
    # 1. Integer (int) - arbitrary precision (never overflows!)
    regular_int = 42
    binary_literal = 0b101010       # 42 in binary
    hex_literal = 0x2A              # 42 in hexadecimal
    huge_int = 10 ** 30             # 1 followed by 30 zeros

    # 2. Floating-point (float) and Scientific Notation
    pi_approx = 3.14159
    avogadro = 6.022e23

    # 3. Complex numbers (complex)
    impedance = 3 + 4j

    # 4. Boolean (bool), String (str), and NoneType (None)
    is_verified = True
    greeting = "Namaste Python"
    missing_value = None

    print("=== Python Primitive & Numeric Data Types ===")
    print(f"regular_int    : {regular_int} (bin={binary_literal}, hex={hex_literal}) -> {type(regular_int).__name__}")
    print(f"huge_int       : {huge_int} -> {type(huge_int).__name__}")
    print(f"pi_approx      : {pi_approx}, avogadro={avogadro:.3e} -> {type(pi_approx).__name__}")
    print(f"impedance      : {impedance} (real={impedance.real}, imag={impedance.imag}, abs={abs(impedance)}) -> {type(impedance).__name__}")
    print(f"is_verified    : {is_verified} (isinstance of int: {isinstance(is_verified, int)}) -> {type(is_verified).__name__}")
    print(f"greeting       : {greeting!r} (length={len(greeting)}) -> {type(greeting).__name__}")
    print(f"missing_value  : {missing_value} -> {type(missing_value).__name__}")


if __name__ == "__main__":
    main()
