"""
Phase 3 - Topic 06: *args and **kwargs
Example 01: Variable Positional Arguments (`*args` Tuple Packing & `*` Unpacking)

Demonstrates:
  - How `*args` collects any number of positional arguments into a `tuple`
  - Combining required positional parameters with `*args`
  - Unpacking an existing `list` or `tuple` into a `*args` function using `*seq`
"""


def calculate_invoice_total(
    tax_rate: float,
    *item_prices: float,
) -> tuple[float, float, float]:
    """
    Calculate (subtotal, tax_amount, grand_total) for 0 or more item prices.
    `tax_rate` is a required first parameter; `*item_prices` packs the rest into a tuple.
    """
    print(f"    [Inside] item_prices={item_prices} (type: {type(item_prices).__name__})")
    subtotal = sum(item_prices)
    tax_amount = round(subtotal * tax_rate, 2)
    grand_total = round(subtotal + tax_amount, 2)
    return subtotal, tax_amount, grand_total


def main() -> None:
    print("=== 1. Calling `*item_prices` with Varying Counts of Arguments ===")
    sub_1, tax_1, total_1 = calculate_invoice_total(0.18, 499.0, 1299.0, 200.0)
    print(f"  3 items -> subtotal={sub_1:.2f}, tax={tax_1:.2f}, total={total_1:.2f}")

    sub_0, tax_0, total_0 = calculate_invoice_total(0.18)
    print(f"  0 items -> subtotal={sub_0:.2f}, tax={tax_0:.2f}, total={total_0:.2f}")

    print("\n=== 2. Unpacking a List into `*item_prices` Using `*cart_prices` ===")
    cart_prices = [150.0, 350.0, 500.0, 250.0]
    sub_2, tax_2, total_2 = calculate_invoice_total(0.12, *cart_prices)
    print(f"  Unpacked list -> subtotal={sub_2:.2f}, tax={tax_2:.2f}, total={total_2:.2f}")


if __name__ == "__main__":
    main()
