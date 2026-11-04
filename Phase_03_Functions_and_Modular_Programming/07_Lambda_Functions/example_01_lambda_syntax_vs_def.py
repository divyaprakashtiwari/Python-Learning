"""
Phase 3 - Topic 07: Lambda Functions
Example 01: Anonymous `lambda` Syntax vs `def` Statements & Dispatch Tables

Demonstrates:
  - Single-expression syntax of `lambda parameters: expression`
  - Comparing a `def` function and a `lambda` function (`type`, `__name__`, bytecode)
  - Using inline `lambda` expressions inside a dictionary dispatch table
"""

from typing import Callable


def add_with_def(a: float, b: float) -> float:
    """Standard named function defined with `def`."""
    return a + b


def main() -> None:
    print("=== 1. Comparing `def` vs `lambda` Function Objects ===")
    # Note: PEP 8 recommends `def` when binding a function to a variable name;
    # we bind `add_with_lambda` here purely to inspect its runtime attributes.
    add_with_lambda = lambda a, b: a + b  # noqa: E731

    print(f"  add_with_def(7, 5)    = {add_with_def(7, 5)} | __name__ = {add_with_def.__name__!r}")
    print(f"  add_with_lambda(7, 5) = {add_with_lambda(7, 5)} | __name__ = {add_with_lambda.__name__!r}")
    print(f"  Same runtime type?    : {type(add_with_def) is type(add_with_lambda)}")

    print("\n=== 2. Inline `lambda` Expressions in a Calculator Dispatch Table ===")
    operations: dict[str, Callable[[float, float], float]] = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: round(x / y, 4) if y != 0 else float("inf"),
        "**": lambda x, y: x**y,
    }
    for op_symbol in ("+", "-", "*", "/", "**"):
        result = operations[op_symbol](12.0, 3.0)
        print(f"  12.0 {op_symbol:<2} 3.0 = {result}")


if __name__ == "__main__":
    main()
