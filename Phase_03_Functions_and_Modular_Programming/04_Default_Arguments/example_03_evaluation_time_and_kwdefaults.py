"""
Phase 3 - Topic 04: Default Arguments
Example 03: Dynamic Default Evaluation Time (`datetime` / Memoization Cache)

Demonstrates:
  - Why `def log(msg, ts=datetime.now())` freezes the timestamp at definition time
  - How to generate a fresh timestamp on every call using `None`
  - One legitimate advanced use case of a mutable default: a local memoization cache
"""

import time


def log_with_frozen_default(
    message: str,
    timestamp: float = time.monotonic(),
) -> str:
    """PITFALL: `time.monotonic()` runs ONCE when `def` is executed!"""
    return f"[t={timestamp:.4f}] {message}"


def log_with_dynamic_default(
    message: str,
    timestamp: float | None = None,
) -> str:
    """CORRECT: Evaluates `time.monotonic()` fresh when `timestamp` is omitted."""
    if timestamp is None:
        timestamp = time.monotonic()
    return f"[t={timestamp:.4f}] {message}"


def fibonacci_cached(n: int, _cache: dict[int, int] = {0: 0, 1: 1}) -> int:
    """Intentional mutable default `_cache` for $O(n)$ memoization."""
    if n not in _cache:
        _cache[n] = fibonacci_cached(n - 1) + fibonacci_cached(n - 2)
    return _cache[n]


def main() -> None:
    print("=== 1. Frozen Timestamp Default Pitfall ===")
    first_frozen = log_with_frozen_default("Server starting")
    time.sleep(0.02)
    second_frozen = log_with_frozen_default("Server ready (20ms later)")
    print(f"  {first_frozen}")
    print(f"  {second_frozen}  <-- IDENTICAL timestamp!")

    print("\n=== 2. Dynamic Timestamp Default (`None` Sentinel) ===")
    first_dyn = log_with_dynamic_default("Server starting")
    time.sleep(0.02)
    second_dyn = log_with_dynamic_default("Server ready (20ms later)")
    print(f"  {first_dyn}")
    print(f"  {second_dyn}  <-- Updated timestamp!")

    print("\n=== 3. Intentional Mutable Default for Memoization ===")
    print(f"  fibonacci_cached(10) = {fibonacci_cached(10)}")
    print(f"  fibonacci_cached(20) = {fibonacci_cached(20)}")
    print(f"  Cached keys count    = {len(fibonacci_cached.__defaults__[0])}")  # type: ignore[index]


if __name__ == "__main__":
    main()
