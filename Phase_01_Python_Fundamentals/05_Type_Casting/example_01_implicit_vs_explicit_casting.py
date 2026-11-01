"""
Topic 05: Type Casting
Example 01: Implicit Coercion vs Explicit Type Casting

Demonstrates how Python automatically widens `int` to `float` in mixed arithmetic
(implicit casting) and how developers explicitly convert between `int`, `float`,
and `str` (including binary and hexadecimal string parsing).
"""


def main() -> None:
    # 1. Implicit Type Casting (Coercion)
    items_count = 4          # int
    unit_weight_kg = 1.75    # float
    total_weight = items_count + unit_weight_kg  # int is widened to float
    print("=== 1. Implicit Type Casting ===")
    print(f"{items_count} (int) + {unit_weight_kg} (float) = {total_weight} ({type(total_weight).__name__})")

    # 2. Explicit Type Casting (int, float, str)
    raw_price_str = "1299.95"
    price_float = float(raw_price_str)
    truncated_int = int(price_float)   # Truncates toward zero (does NOT round)
    rounded_int = round(price_float)

    print("\n=== 2. Explicit Numeric & String Casting ===")
    print(f"String {raw_price_str!r} -> float : {price_float}")
    print(f"float {price_float} -> int()  : {truncated_int} (truncated toward zero)")
    print(f"float {price_float} -> round(): {rounded_int} (rounded to nearest integer)")

    # 3. Parsing integers from different number bases using int(string, base)
    binary_str = "11010"
    hex_str = "FF"
    print("\n=== 3. Base Conversion with int(str, base) ===")
    print(f"Binary {binary_str!r} (base 2)  -> int: {int(binary_str, 2)}")
    print(f"Hex    {hex_str!r} (base 16) -> int: {int(hex_str, 16)}")


if __name__ == "__main__":
    main()
