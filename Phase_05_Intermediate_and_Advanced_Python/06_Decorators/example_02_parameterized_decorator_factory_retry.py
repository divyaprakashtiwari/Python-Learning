"""
Phase 5 - Topic 06: Decorators
Example 02: Parameterized Decorator Factories (`@retry(max_attempts=3)`)

Demonstrates:
  - Building a 3-layer decorator factory that accepts configuration arguments
  - Automatically retrying transient failures before succeeding or re-raising
"""

import functools
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def retry(
    max_attempts: int = 3,
    catch_exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator factory that retries `func` up to `max_attempts` times on matching exceptions."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except catch_exceptions as err:
                    print(f"  [retry] Attempt {attempt}/{max_attempts} failed: {err}")
                    if attempt == max_attempts:
                        raise
            raise RuntimeError("Unreachable")

        return wrapper

    return decorator


def main() -> None:
    attempts_made = 0

    @retry(max_attempts=3, catch_exceptions=(ConnectionError,))
    def fetch_remote_profile(user_id: int) -> dict[str, object]:
        nonlocal attempts_made
        attempts_made += 1
        if attempts_made < 3:
            raise ConnectionError(f"Transient socket timeout on try #{attempts_made}")
        return {"user_id": user_id, "status": "ok", "attempts": attempts_made}

    print("=== Testing Parameterized `@retry(max_attempts=3)` Decorator ===")
    profile = fetch_remote_profile(42)
    print(f"  Success on attempt #{attempts_made}: {profile}")


if __name__ == "__main__":
    main()
