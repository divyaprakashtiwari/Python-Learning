"""
Phase 3 - Topic 07: Lambda Functions
Example 03: Functional Pipelines (`map`, `filter`) & The Late-Binding Loop Trap

Demonstrates:
  - Using `lambda` with `map()` and `filter()` vs list comprehensions
  - The classic interview trap: creating `lambda` functions inside a `for` loop
    (late-binding closure) and fixing it with a default parameter `lambda x, i=i: ...`
"""


def main() -> None:
    print("=== 1. `map()` and `filter()` with `lambda` ===")
    raw_prices = [120, 450, 80, 999, 310, 45]
    # Keep prices >= 100 and apply 18% GST
    premium_prices = list(filter(lambda p: p >= 100, raw_prices))
    prices_with_gst = list(map(lambda p: round(p * 1.18, 2), premium_prices))
    print(f"  Raw prices          : {raw_prices}")
    print(f"  Filtered (>= 100)   : {premium_prices}")
    print(f"  Mapped (+18% GST)   : {prices_with_gst}")

    print("\n=== 2. The Late-Binding Loop Closure Trap ===")
    # BUGGY: All 4 lambdas look up loop variable `i` AFTER the loop ends (`i == 3`)
    buggy_multipliers = [lambda x: x * i for i in range(4)]
    buggy_outputs = [fn(10) for fn in buggy_multipliers]
    print(f"  Buggy `[lambda x: x * i]` for x=10       -> {buggy_outputs} (all use i=3!)")

    # FIXED: Capture current `i` at each iteration as a default parameter `i=i`
    fixed_multipliers = [lambda x, i=i: x * i for i in range(4)]
    fixed_outputs = [fn(10) for fn in fixed_multipliers]
    print(f"  Fixed `[lambda x, i=i: x * i]` for x=10  -> {fixed_outputs} (0, 10, 20, 30!)")


if __name__ == "__main__":
    main()
