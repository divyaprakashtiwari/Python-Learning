"""
Phase 3 - Topic 09: Scope and Lifetime of Variables
Example 02: The `UnboundLocalError` Trap & The `global` Keyword

Demonstrates:
  - Why Python determines whether a variable is local at COMPILE TIME (not line-by-line)
  - How assigning to a name anywhere in a function makes it local across the ENTIRE function,
    causing `UnboundLocalError` if read before the assignment
  - Using `global` to rebind a module-level variable (and why returning values is cleaner)
"""

request_counter = 100


def buggy_increment() -> None:
    """
    Raises `UnboundLocalError`!
    Because `request_counter += 1` assigns to `request_counter`, Python marks
    `request_counter` as a LOCAL variable for the entire function at compile time.
    """
    print(request_counter)  # Tries to read uninitialized local `request_counter`!
    request_counter += 1  # type: ignore[misc]


def increment_with_global() -> int:
    """Explicitly tells Python that `request_counter` refers to the module global."""
    global request_counter
    request_counter += 1
    return request_counter


def increment_pure(current_count: int) -> int:
    """Preferred production pattern: pass state in and return new state (no `global`)."""
    return current_count + 1


def main() -> None:
    print("=== 1. Catching the Compile-Time `UnboundLocalError` Trap ===")
    try:
        buggy_increment()
    except UnboundLocalError as err:
        print(f"  Caught expected UnboundLocalError: {err}")

    print("\n=== 2. Rebinding Module State with `global` ===")
    print(f"  Before `increment_with_global()` : request_counter = {request_counter}")
    increment_with_global()
    increment_with_global()
    print(f"  After 2 calls                    : request_counter = {request_counter}")

    print("\n=== 3. Pure Function Alternative (No Global Mutation) ===")
    clean_count = increment_pure(request_counter)
    print(f"  Pure return value                : {clean_count} (global still {request_counter})")


if __name__ == "__main__":
    main()
