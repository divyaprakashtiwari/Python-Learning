"""
Phase 4 - Topic 01: Classes and Objects
Example 03: Collaborating Objects (E-Commerce Order & Product Domain Model)

Demonstrates:
  - Designing multiple classes (`Product` and `Order`) whose instances interact
  - Bundling data (state) and business rules (behavior) inside cohesive classes
"""


class Product:
    """Represents a catalog item with SKU, name, unit price, and available stock."""

    def __init__(self, sku: str, name: str, price: float, stock: int) -> None:
        self.sku = sku
        self.name = name
        self.price = price
        self.stock = stock

    def reserve_stock(self, quantity: int) -> bool:
        """Deduct `quantity` from `self.stock` if available; return True on success."""
        if quantity <= 0 or quantity > self.stock:
            return False
        self.stock -= quantity
        return True


class Order:
    """Represents a customer order containing line items of `Product` objects."""

    def __init__(self, order_id: str, customer_name: str) -> None:
        self.order_id = order_id
        self.customer_name = customer_name
        self.line_items: list[tuple[Product, int]] = []

    def add_product(self, product: Product, quantity: int) -> str:
        """Attempt to reserve stock and add `(product, quantity)` to the order."""
        if not product.reserve_stock(quantity):
            return (
                f"FAILED: Cannot add {quantity}x '{product.name}' "
                f"(only {product.stock} in stock)"
            )
        self.line_items.append((product, quantity))
        return f"ADDED : {quantity}x '{product.name}' @ INR {product.price:,.2f}"

    def total_amount(self) -> float:
        """Calculate the grand total across all reserved line items."""
        return round(sum(prod.price * qty for prod, qty in self.line_items), 2)

    def print_invoice(self) -> None:
        """Print a formatted invoice summary."""
        print(f"  Invoice {self.order_id} | Customer: {self.customer_name}")
        for prod, qty in self.line_items:
            line_total = prod.price * qty
            print(f"    - {prod.sku} | {prod.name:<18} x{qty} = INR {line_total:,.2f}")
        print(f"    Total Payable: INR {self.total_amount():,.2f}")


def main() -> None:
    print("=== 1. Creating Catalog Product Objects ===")
    laptop = Product("SKU-101", "ThinkPad Laptop", 85000.0, stock=3)
    mouse = Product("SKU-202", "Wireless Mouse", 1500.0, stock=10)

    print("=== 2. Collaborating Objects: Building an Order ===")
    order = Order("ORD-9001", "Divya Prakash")
    print(f"  {order.add_product(laptop, 1)}")
    print(f"  {order.add_product(mouse, 2)}")
    print(f"  {order.add_product(laptop, 5)}")  # Exceeds remaining stock (2)

    print("\n=== 3. Final Invoice & Updated Product Stock ===")
    order.print_invoice()
    print(f"  Remaining stock -> {laptop.name}: {laptop.stock}, {mouse.name}: {mouse.stock}")


if __name__ == "__main__":
    main()
