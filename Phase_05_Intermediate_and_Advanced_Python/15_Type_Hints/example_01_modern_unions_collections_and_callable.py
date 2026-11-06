"""
Phase 5 - Topic 15: Type Hints
Example 01: Modern Built-in Generics (`list[int]`), Union Operator (`X | Y`), & `Callable`

Demonstrates:
  - Python 3.9+ built-in generic collection syntax (`list[str]`, `dict[str, int]`, `tuple[int, ...]`)
  - Python 3.10+ union operator `int | float | None` (replacing `Union` and `Optional`)
  - Annotating higher-order functions with `collections.abc.Callable[[ArgType], ReturnType]`
"""

from collections.abc import Callable


def apply_discount(
    prices: list[float],
    coupon_pct: float | None,
    rounding_fn: Callable[[float], float] = round,
) -> dict[str, float]:
    """Compute subtotal and final total with optional coupon discount."""
    subtotal = sum(prices)
    factor = 1.0 - (coupon_pct / 100.0) if coupon_pct is not None else 1.0
    final_total = rounding_fn(subtotal * factor)
    return {"subtotal": subtotal, "final_total": final_total}


def main() -> None:
    print("=== 1. Invoking Type-Annotated Function ===")
    cart = [499.0, 1200.0, 301.0]
    summary_with_coupon = apply_discount(cart, coupon_pct=15.0)
    summary_no_coupon = apply_discount(cart, coupon_pct=None)
    print(f"  With 15% coupon : {summary_with_coupon}")
    print(f"  With None coupon: {summary_no_coupon}")

    print("\n=== 2. Inspecting Function `__annotations__` Dict ===")
    for param, annotation in apply_discount.__annotations__.items():
        print(f"  {param:<13} -> {annotation}")


if __name__ == "__main__":
    main()
