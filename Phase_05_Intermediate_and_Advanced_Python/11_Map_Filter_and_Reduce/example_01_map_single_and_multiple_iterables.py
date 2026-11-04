"""
Phase 5 - Topic 11: Map, Filter and Reduce
Example 01: `map()` — Lazy Transformation on Single and Multiple Parallel Iterables

Demonstrates:
  - Transforming a sequence lazily with `map(func, iterable)`
  - Passing multiple iterables to `map(func, iter1, iter2)` (stops at the shortest iterable)
  - Side-by-side comparison with equivalent list/generator comprehensions
"""


def format_price(amount: float, tax_rate: float) -> str:
    return f"Rs.{amount * (1 + tax_rate):,.2f}"


def main() -> None:
    print("=== 1. Single-Iterable `map(str.strip, ...)` ===")
    raw_tags = ["  python ", "dsa\n", "\tbackend  "]
    cleaned_map = map(str.strip, raw_tags)
    print(f"  map object (lazy iterator): {type(cleaned_map).__name__}")
    print(f"  Materialized list         : {list(cleaned_map)}")

    print("\n=== 2. Multi-Iterable `map(func, prices, taxes)` ===")
    base_prices = [1000.0, 2500.0, 500.0]
    tax_rates = [0.18, 0.28, 0.05]
    formatted = list(map(format_price, base_prices, tax_rates))
    print(f"  Formatted with tax        : {formatted}")

    print("\n=== 3. Equivalent List Comprehension Comparison ===")
    comp_result = [format_price(p, t) for p, t in zip(base_prices, tax_rates)]
    print(f"  Matches comprehension?    : {formatted == comp_result}")


if __name__ == "__main__":
    main()
