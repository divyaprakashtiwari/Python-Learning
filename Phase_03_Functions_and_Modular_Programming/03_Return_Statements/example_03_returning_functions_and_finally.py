"""
Phase 3 - Topic 03: Return Statements
Example 03: Returning Functions (Factory Pattern) & Returning Inside `try/finally`

Demonstrates:
  - Higher-order functions that create and return customized inner functions
  - How `return` interacts with `try ... finally` blocks (why `finally` ALWAYS runs
    before the return value is handed back to the caller)
"""

from typing import Callable


def make_multiplier(factor: int) -> Callable[[int], int]:
    """Return a newly created function that multiplies its input by `factor`."""

    def multiply(number: int) -> int:
        return number * factor

    return multiply


def query_with_cleanup(query: str) -> str:
    """Demonstrate that `finally` executes even when `try` hits a `return` statement."""
    execution_steps: list[str] = []
    try:
        execution_steps.append(f"1. Executing query: {query}")
        return " | ".join(execution_steps) + " -> [Returned from try]"
    finally:
        # Runs right before the function actually exits to the caller
        print("  [finally block] Closing database cursor cleanly before returning!")


def main() -> None:
    print("=== 1. Returning a Function (Function Factory) ===")
    double = make_multiplier(2)
    triple = make_multiplier(3)
    print(f"  `double` object : {double.__name__} | double(14) = {double(14)}")
    print(f"  `triple` object : {triple.__name__} | triple(14) = {triple(14)}")

    print("\n=== 2. `return` Inside `try ... finally` ===")
    result = query_with_cleanup("SELECT id FROM orders")
    print(f"  Caller received : {result}")


if __name__ == "__main__":
    main()
