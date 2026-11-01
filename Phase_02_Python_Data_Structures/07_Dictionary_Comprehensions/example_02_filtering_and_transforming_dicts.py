"""
Topic 07: Dictionary Comprehensions
Example 02: Filtering, Discount Transformation, and Key Normalization

Demonstrates how to filter a dictionary by value/key criteria and transform
all values or keys in a single readable dictionary comprehension.
"""


def main() -> None:
    product_prices = {
        "Mechanical Keyboard": 3500.0,
        "USB-C Cable": 299.0,
        "27-Inch Monitor": 18500.0,
        "Mouse Pad": 199.0,
        "Laptop Stand": 1200.0,
    }

    # 1. Filtering: keep only premium items (>= Rs. 1000)
    premium_items = {
        item: price
        for item, price in product_prices.items()
        if price >= 1000.0
    }
    print("=== 1. Filtered Premium Products (>= Rs. 1000) ===")
    print(f"Premium Items : {premium_items}")

    # 2. Conditional Value Transformation: 15% discount on items >= 1000, else 5%
    discounted_catalog = {
        item: round(price * 0.85, 2) if price >= 1000.0 else round(price * 0.95, 2)
        for item, price in product_prices.items()
    }
    print("\n=== 2. Tiered Discount Catalog ===")
    for name, new_price in discounted_catalog.items():
        print(f"  {name:<21} : Rs.{new_price:>8.2f}")

    # 3. Normalizing messy HTTP Header keys to lowercase
    raw_headers = {"  Content-Type ": "application/json", "X-Request-ID": "req-99"}
    normalized_headers = {k.strip().lower(): v for k, v in raw_headers.items()}
    print("\n=== 3. Normalized HTTP Headers ===")
    print(f"Normalized : {normalized_headers}")


if __name__ == "__main__":
    main()
