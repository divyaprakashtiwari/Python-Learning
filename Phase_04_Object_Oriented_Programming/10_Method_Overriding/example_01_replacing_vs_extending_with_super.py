"""
Phase 4 - Topic 10: Method Overriding
Example 01: Replacing vs Extending Parent Methods (`super().method()`)

Demonstrates:
  - Complete Replacement Override: child method replaces parent behavior entirely
  - Cooperative Extension Override: child method calls `super().calculate_price()`
    and adds/discounts on top of the parent's calculation
"""


class StandardShippingOrder:
    """Base order with standard shipping calculation."""

    def __init__(self, order_id: str, subtotal: float, weight_kg: float) -> None:
        self.order_id = order_id
        self.subtotal = subtotal
        self.weight_kg = weight_kg

    def shipping_label(self) -> str:
        return f"[STANDARD-SURFACE] Order {self.order_id}"

    def calculate_total(self) -> float:
        """Base total = subtotal + INR 50 per kg shipping."""
        shipping_cost = self.weight_kg * 50.0
        return round(self.subtotal + shipping_cost, 2)


class ExpressAirOrder(StandardShippingOrder):
    """
    1. Replaces `shipping_label()` completely.
    2. Extends `calculate_total()` by calling `super().calculate_total()` + air surcharge.
    """

    def __init__(
        self,
        order_id: str,
        subtotal: float,
        weight_kg: float,
        priority_surcharge: float = 350.0,
    ) -> None:
        super().__init__(order_id, subtotal, weight_kg)
        self.priority_surcharge = priority_surcharge

    # 1. Complete Replacement Override
    def shipping_label(self) -> str:
        return f"[EXPRESS-AIR-PRIORITY] Order {self.order_id}"

    # 2. Cooperative Extension Override via `super()`
    def calculate_total(self) -> float:
        base_total = super().calculate_total()
        return round(base_total + self.priority_surcharge, 2)


def main() -> None:
    std_order = StandardShippingOrder("ORD-101", subtotal=2000.0, weight_kg=3.0)
    air_order = ExpressAirOrder("ORD-202", subtotal=2000.0, weight_kg=3.0)

    print("=== 1. Base Class Behavior (`StandardShippingOrder`) ===")
    print(f"  {std_order.shipping_label():<35} -> Total: INR {std_order.calculate_total():,.2f}")

    print("\n=== 2. Overridden Subclass Behavior (`ExpressAirOrder`) ===")
    print(f"  {air_order.shipping_label():<35} -> Total: INR {air_order.calculate_total():,.2f}")


if __name__ == "__main__":
    main()
