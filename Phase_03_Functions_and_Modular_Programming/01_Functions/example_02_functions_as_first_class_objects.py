"""
Topic 01: Functions
Example 02: Functions as First-Class Objects (Dispatch Tables & Higher-Order Calls)

Demonstrates that functions in Python are first-class objects: they can be assigned
to variables, stored in dictionaries, and passed as arguments to other functions.
"""

from typing import Callable


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def apply_operation(func: Callable[[float, float], float], x: float, y: float) -> float:
    """Higher-order function that accepts another function `func` and invokes it."""
    return func(x, y)


def main() -> None:
    # 1. Assigning a function to a variable (no parentheses!)
    compute = multiply
    print("=== 1. Assigning a Function to a Variable ===")
    print(f"compute(6, 7) via alias : {compute(6, 7)}")

    # 2. Storing functions in a Dictionary Dispatch Table (O(1) routing)
    operations: dict[str, Callable[[float, float], float]] = {
        "ADD": add,
        "SUB": subtract,
        "MUL": multiply,
    }
    print("\n=== 2. Dictionary Dispatch Table ===")
    commands = [("ADD", 15, 5), ("SUB", 15, 5), ("MUL", 15, 5)]
    for op_name, x, y in commands:
        handler = operations[op_name]
        result = apply_operation(handler, x, y)
        print(f"  Command {op_name}({x}, {y}) -> {result}")


if __name__ == "__main__":
    main()
