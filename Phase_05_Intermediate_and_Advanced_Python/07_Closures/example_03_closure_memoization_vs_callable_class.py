"""
Phase 5 - Topic 07: Closures
Example 03: Closure-Based Memoization Cache & Comparing Closures vs Single-Method Classes

Demonstrates:
  - Building a custom memoization closure that caches expensive function results in a private dict
  - Exposing cache statistics (`cache_info`) as an attribute attached to the closure
"""

import functools
from typing import Callable


def memoize_unary(func: Callable[[int], int]) -> Callable[[int], int]:
    """Closure-based memoizer storing `(hits, misses)` and `cache` in enclosing scope."""
    cache: dict[int, int] = {}
    hits = 0
    misses = 0

    @functools.wraps(func)
    def wrapper(n: int) -> int:
        nonlocal hits, misses
        if n in cache:
            hits += 1
            return cache[n]
        misses += 1
        result = func(n)
        cache[n] = result
        return result

    def stats() -> dict[str, int]:
        return {"hits": hits, "misses": misses, "size": len(cache)}

    wrapper.stats = stats  # type: ignore[attr-defined]
    return wrapper


@memoize_unary
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def main() -> None:
    print("=== Closure-Based Memoization Cache on Recursive `fib(10)` ===")
    result = fib(10)
    print(f"  fib(10) = {result}")
    print(f"  Cache stats after fib(10): {fib.stats()}")  # type: ignore[attr-defined]

    print(f"  fib(8)  = {fib(8)} (instant cache hit!)")
    print(f"  Cache stats after fib(8) : {fib.stats()}")  # type: ignore[attr-defined]


if __name__ == "__main__":
    main()
