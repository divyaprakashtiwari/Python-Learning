"""
Phase 5 - Topic 15: Type Hints
Example 02: Generic Functions & Classes (Python 3.12+ `[T]` Syntax) and `TypedDict`

Demonstrates:
  - Python 3.12+ PEP 695 generic type parameter syntax `def first[T](items: list[T]) -> T:`
    and `class Box[T]:`
  - Typing structured JSON-like dictionaries with `typing.TypedDict` and `NotRequired`
"""

from typing import NotRequired, TypedDict


class UserPayload(TypedDict):
    """Typed dictionary schema for a JSON API user object."""

    id: int
    username: str
    email: NotRequired[str]


class Stack[T]:
    """Generic LIFO Stack using Python 3.12+ `class Stack[T]:` syntax."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()


def head_or_default[T](items: list[T], default: T) -> T:
    """Generic function returning the first element or `default`."""
    return items[0] if items else default


def main() -> None:
    print("=== 1. Python 3.12+ Generic Function & Class (`[T]`) ===")
    int_stack = Stack[int]()
    int_stack.push(10)
    int_stack.push(20)
    print(f"  Popped from Stack[int]: {int_stack.pop()}")
    print(f"  head_or_default([], 'fallback'): {head_or_default([], 'fallback')!r}")

    print("\n=== 2. Structured Dictionary Schema with `TypedDict` ===")
    user: UserPayload = {"id": 101, "username": "aarav"}
    print(f"  TypedDict instance (runtime dict): {user} | type={type(user).__name__}")


if __name__ == "__main__":
    main()
