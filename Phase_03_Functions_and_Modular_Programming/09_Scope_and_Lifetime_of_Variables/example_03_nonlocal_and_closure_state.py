"""
Phase 3 - Topic 09: Scope and Lifetime of Variables
Example 03: The `nonlocal` Keyword & Stateful Closures (Extended Variable Lifetime)

Demonstrates:
  - How an inner function (closure) extends the lifetime of an enclosing variable
    even after the outer function has finished executing!
  - Using `nonlocal` to rebind enclosing variables inside a stateful closure
  - Why `for`/`while` loops and `if/else` blocks do NOT create a new scope in Python
"""

from typing import Callable


def make_rate_limiter(max_calls: int) -> Callable[[str], str]:
    """
    Return a closure that tracks `remaining_calls` in its enclosing scope.
    Even after `make_rate_limiter` returns, `remaining_calls` stays alive in a cell!
    """
    remaining_calls = max_calls

    def call_api(endpoint: str) -> str:
        nonlocal remaining_calls
        if remaining_calls <= 0:
            return f"429 Too Many Requests: {endpoint} blocked (0 remaining)"
        remaining_calls -= 1
        return f"200 OK: {endpoint} (remaining quota: {remaining_calls})"

    return call_api


def demonstrate_block_scope_leak() -> None:
    """Show that `if` and `for` blocks share the function's local scope."""
    if True:
        leaked_from_if = "I was defined inside an `if` block"
    for loop_item in ("alpha", "beta", "gamma"):
        pass

    print(f"  Accessible after `if`  : {leaked_from_if!r}")
    print(f"  Accessible after `for` : loop_item = {loop_item!r}")


def main() -> None:
    print("=== 1. Stateful Closure with `nonlocal` (Extended Lifetime) ===")
    limiter = make_rate_limiter(2)
    print(f"  Call 1 : {limiter('/v1/pay')}")
    print(f"  Call 2 : {limiter('/v1/pay')}")
    print(f"  Call 3 : {limiter('/v1/pay')}")
    # Inspect the closure cell that keeps `remaining_calls` alive:
    cell_val = limiter.__closure__[0].cell_contents  # type: ignore[index]
    print(f"  Closure cell contents  : remaining_calls = {cell_val}")

    print("\n=== 2. Loops and `if` Blocks Do NOT Create a Separate Scope ===")
    demonstrate_block_scope_leak()


if __name__ == "__main__":
    main()
