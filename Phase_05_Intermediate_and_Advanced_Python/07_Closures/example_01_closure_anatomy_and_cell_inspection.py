"""
Phase 5 - Topic 07: Closures
Example 01: Anatomy of a Closure — Free Variables & Inspecting `__closure__` Cells

Demonstrates:
  - How an inner function retains access to enclosing scope variables even after
    the outer function has finished executing and its stack frame is gone
  - Inspecting `__code__.co_freevars` and `[cell.cell_contents for cell in fn.__closure__]`
"""

from typing import Callable


def make_tax_calculator(region: str, tax_rate: float) -> Callable[[float], float]:
    """Return a closure that remembers `region` and `tax_rate` from the enclosing scope."""

    def calculate(amount: float) -> float:
        total = round(amount * (1.0 + tax_rate), 2)
        print(f"  [{region} @ {tax_rate * 100:.1f}%] Rs.{amount:,.2f} -> Rs.{total:,.2f}")
        return total

    return calculate


def main() -> None:
    print("=== 1. Creating Independent Closures from the Same Factory ===")
    gst_standard = make_tax_calculator("IN-GST-18", 0.18)
    gst_luxury = make_tax_calculator("IN-GST-28", 0.28)

    gst_standard(1000.0)
    gst_luxury(1000.0)

    print("\n=== 2. Introspecting Closure Free Variables & Cell Contents ===")
    free_vars = gst_standard.__code__.co_freevars
    cell_values = [cell.cell_contents for cell in (gst_standard.__closure__ or ())]
    print(f"  co_freevars   : {free_vars}")
    print(f"  cell_contents : {dict(zip(free_vars, cell_values))}")


if __name__ == "__main__":
    main()
