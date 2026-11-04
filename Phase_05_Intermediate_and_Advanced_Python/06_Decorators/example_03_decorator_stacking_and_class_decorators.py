"""
Phase 5 - Topic 06: Decorators
Example 03: Stacking Multiple Decorators & Class-Based Stateful Decorators

Demonstrates:
  - Stacking order of multiple decorators (`@outer` above `@inner` means `outer(inner(func))`)
  - Implementing a class-based decorator using `__call__` to track invocation counts
"""

import functools
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def html_tag(tag: str) -> Callable[[Callable[P, str]], Callable[P, str]]:
    """Wrap the string return value of a function in `<tag>...</tag>`."""

    def decorator(func: Callable[P, str]) -> Callable[P, str]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
            return f"<{tag}>{func(*args, **kwargs)}</{tag}>"

        return wrapper

    return decorator


class CallCounter:
    """Class-based decorator that counts how many times a function is invoked."""

    def __init__(self, func: Callable[P, R]) -> None:
        functools.update_wrapper(self, func)
        self.func = func
        self.call_count = 0

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        self.call_count += 1
        return self.func(*args, **kwargs)


@html_tag("div")
@html_tag("strong")
def render_headline(title: str) -> str:
    return title.strip()


@CallCounter
def add_numbers(a: int, b: int) -> int:
    return a + b


def main() -> None:
    print("=== 1. Stacking Decorators (`@html_tag('div')` over `@html_tag('strong')`) ===")
    print(f"  Output: {render_headline('Python 3.13 Released')}")

    print("\n=== 2. Class-Based Decorator Tracking Call Counts (`__call__`) ===")
    print(f"  Call 1: {add_numbers(10, 20)} | call_count={add_numbers.call_count}")
    print(f"  Call 2: {add_numbers(5, 7)}  | call_count={add_numbers.call_count}")


if __name__ == "__main__":
    main()
