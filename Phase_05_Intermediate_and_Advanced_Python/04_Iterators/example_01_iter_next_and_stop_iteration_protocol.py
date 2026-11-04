"""
Phase 5 - Topic 04: Iterators
Example 01: The Iterator Protocol Under the Hood (`iter()`, `next()`, and `StopIteration`)

Demonstrates:
  - How Python's `for item in iterable:` loop actually desugars to `iter()` + `while True: next()`
  - Passing a default sentinel value to `next(iterator, default)` to avoid `StopIteration`
"""


def manual_for_loop(iterable: list[str]) -> None:
    """Manually emulate a Python `for` loop using `iter()` and `next()`."""
    iterator = iter(iterable)  # Calls iterable.__iter__()
    print(f"  Created iterator object: {type(iterator).__name__}")
    while True:
        try:
            item = next(iterator)  # Calls iterator.__next__()
        except StopIteration:
            print("  [StopIteration caught] Loop terminated cleanly.")
            break
        else:
            print(f"    -> Yielded item: {item!r}")


def main() -> None:
    print("=== 1. Emulating `for` Loop with `iter()`, `next()`, and `StopIteration` ===")
    manual_for_loop(["alpha", "beta", "gamma"])

    print("\n=== 2. Safe Pulling with Default Sentinel `next(it, default)` ===")
    tasks_iter = iter(["deploy-db", "run-migrations"])
    print(f"  Pull 1: {next(tasks_iter, '<queue-empty>')}")
    print(f"  Pull 2: {next(tasks_iter, '<queue-empty>')}")
    print(f"  Pull 3: {next(tasks_iter, '<queue-empty>')}")


if __name__ == "__main__":
    main()
