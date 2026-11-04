"""
Phase 5 - Topic 06: Decorators
Example 01: Function Decorators & Preserving Metadata with `@functools.wraps`

Demonstrates:
  - How `@decorator` syntax is syntactic sugar for `func = decorator(func)`
  - Forwarding arbitrary arguments with `*args, **kwargs`
  - Why `@functools.wraps(func)` is critical to preserve `__name__`, `__doc__`, and `__wrapped__`
"""

import functools
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def audit_call(func: Callable[P, R]) -> Callable[P, R]:
    """Log function entry and exit while preserving original function metadata."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        arg_list = [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
        print(f"  [audit] Calling {func.__name__}({', '.join(arg_list)})")
        result = func(*args, **kwargs)
        print(f"  [audit] {func.__name__} returned {result!r}")
        return result

    return wrapper


@audit_call
def compute_emi(principal: float, annual_rate: float, months: int = 12) -> float:
    """Compute monthly EMI for a loan."""
    monthly_rate = annual_rate / (12 * 100)
    emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / (
        (1 + monthly_rate) ** months - 1
    )
    return round(emi, 2)


def main() -> None:
    print("=== 1. Invoking `@audit_call` Decorated Function ===")
    monthly = compute_emi(100_000, 12.0, months=12)
    print(f"  Result: Rs.{monthly}")

    print("\n=== 2. Inspecting Preserved Metadata (`@functools.wraps`) ===")
    print(f"  __name__ : {compute_emi.__name__!r}")
    print(f"  __doc__  : {compute_emi.__doc__!r}")
    print(f"  Has __wrapped__? {hasattr(compute_emi, '__wrapped__')}")


if __name__ == "__main__":
    main()
