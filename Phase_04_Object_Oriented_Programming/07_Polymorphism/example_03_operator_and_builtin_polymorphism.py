"""
Phase 4 - Topic 07: Polymorphism
Example 03: Ad-Hoc Polymorphism (Operator Overloading & `@functools.singledispatch`)

Demonstrates:
  - Built-in operator polymorphism (`+` and `*` behaving differently on `int`, `str`, `list`)
  - Custom operator polymorphism (`__add__` on a `Money` class)
  - Function overloading by argument type in Python using `@functools.singledispatch`
"""

from functools import singledispatch


class Money:
    """Supports polymorphic `+` operator via `__add__`."""

    def __init__(self, amount: float, currency: str = "INR") -> None:
        self.amount = round(amount, 2)
        self.currency = currency

    def __add__(self, other: "Money") -> "Money":
        if not isinstance(other, Money) or self.currency != other.currency:
            raise TypeError("Can only add Money instances of the same currency")
        return Money(self.amount + other.amount, self.currency)

    def __repr__(self) -> str:
        return f"Money({self.amount:.2f}, {self.currency!r})"


@singledispatch
def format_for_audit(value: object) -> str:
    """Default fallback implementation for arbitrary objects."""
    return f"OBJECT({value!r})"


@format_for_audit.register
def _(value: int) -> str:
    return f"INT({value:,})"


@format_for_audit.register
def _(value: list) -> str:
    return f"LIST(len={len(value)}, items={value})"


def main() -> None:
    print("=== 1. Operator Polymorphism (`+` on `int`, `str`, `list`, and `Money`) ===")
    print(f"  10 + 25                      = {10 + 25}")
    print(f"  'Py' + 'thon'                = {'Py' + 'thon'!r}")
    print(f"  Money(450) + Money(550)      = {Money(450) + Money(550)}")

    print("\n=== 2. Type-Based Function Dispatch (`@functools.singledispatch`) ===")
    for sample in (1250000, ["read", "write"], Money(99.50)):
        print(f"  {format_for_audit(sample)}")


if __name__ == "__main__":
    main()
