"""
Topic 05: Type Casting
Example 02: Boolean Casting (`bool()`) — Truthy vs Falsy Values

Demonstrates which Python values evaluate to `False` (falsy) and which evaluate
to `True` (truthy) when passed to `bool()` or used in an `if` condition.
"""


def main() -> None:
    falsy_values = [0, 0.0, 0j, "", [], (), {}, set(), None, False]
    truthy_values = [1, -5, 0.001, "False", "0", [0], (None,), {"k": 1}]

    print("=== 1. Falsy Values (bool(x) is Always False) ===")
    for val in falsy_values:
        print(f"  bool({val!r:<8}) -> {bool(val)}")

    print("\n=== 2. Truthy Values (bool(x) is Always True) ===")
    for val in truthy_values:
        print(f"  bool({val!r:<8}) -> {bool(val)}")


if __name__ == "__main__":
    main()
