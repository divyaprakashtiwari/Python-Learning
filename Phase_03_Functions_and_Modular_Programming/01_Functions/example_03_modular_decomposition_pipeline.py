"""
Topic 01: Functions
Example 03: Single-Responsibility Decomposition (Order Processing Pipeline)

Demonstrates breaking a complex task into small, testable, single-responsibility
functions that compose cleanly inside a coordinator function.
"""


def validate_items(items: list[tuple[str, int, float]]) -> bool:
    """Return True if the order is non-empty and all quantities/prices are positive."""
    if not items:
        return False
    return all(qty > 0 and price >= 0.0 for _, qty, price in items)


def compute_subtotal(items: list[tuple[str, int, float]]) -> float:
    """Sum (quantity * unit_price) across all line items."""
    return sum(qty * price for _, qty, price in items)


def apply_coupon_discount(subtotal: float, coupon_code: str) -> float:
    """Apply flat percentage discount based on coupon code."""
    discounts = {"SAVE10": 0.10, "FESTIVE20": 0.20}
    rate = discounts.get(coupon_code.upper(), 0.0)
    return round(subtotal * (1.0 - rate), 2)


def generate_order_summary(items: list[tuple[str, int, float]], coupon: str = "") -> str:
    """Coordinator function composing validation, subtotal, and discount helpers."""
    if not validate_items(items):
        return "ERROR: Invalid order items."
    raw_subtotal = compute_subtotal(items)
    discounted = apply_coupon_discount(raw_subtotal, coupon)
    gst_total = round(discounted * 1.18, 2)
    return (
        f"Subtotal: Rs.{raw_subtotal:.2f} | "
        f"After Coupon ({coupon or 'NONE'}): Rs.{discounted:.2f} | "
        f"Final (incl. 18% GST): Rs.{gst_total:.2f}"
    )


def main() -> None:
    cart = [
        ("DSA Course", 1, 1500.0),
        ("Mock Interviews", 2, 500.0),
    ]
    print("=== Single-Responsibility Order Pipeline ===")
    print(generate_order_summary(cart, coupon="FESTIVE20"))
    print(generate_order_summary(cart, coupon=""))
    print(generate_order_summary([], coupon="SAVE10"))


if __name__ == "__main__":
    main()
