"""
Phase 4 - Topic 11: Magic/Dunder Methods
Example 02: Arithmetic Operators (`__add__`, `__mul__`, `__rmul__`) & Truthiness (`__bool__`)

Demonstrates:
  - Overloading `+` (`__add__`), scalar `*` (`__mul__` and reflected `__rmul__`),
    and equality on a 2D mathematical `Vector2D` class
  - Implementing `__abs__` (`abs(v)`) and `__bool__` (`bool(v)`)
"""

import math


class Vector2D:
    """2D Euclidean vector supporting `+`, scalar `*`, `abs()`, and `bool()`."""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector2D({self.x}, {self.y})"

    def __add__(self, other: "Vector2D") -> "Vector2D":
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> "Vector2D":
        """Handles `vec * 3.0`."""
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector2D":
        """Handles reflected `3.0 * vec` when left operand (`float`) returns NotImplemented."""
        return self.__mul__(scalar)

    def __abs__(self) -> float:
        """Handles `abs(vec)` -> Euclidean magnitude."""
        return math.hypot(self.x, self.y)

    def __bool__(self) -> bool:
        """Zero vector `Vector2D(0, 0)` is falsy; all other vectors are truthy."""
        return bool(self.x or self.y)


def main() -> None:
    v_a = Vector2D(3.0, 4.0)
    v_b = Vector2D(1.0, -2.0)
    v_zero = Vector2D(0.0, 0.0)

    print("=== 1. Arithmetic Dunder Methods (`+`, `*`, Reflected `__rmul__`) ===")
    print(f"  v_a + v_b   = {v_a + v_b}")
    print(f"  v_a * 2.5   = {v_a * 2.5}  (calls v_a.__mul__(2.5))")
    print(f"  2.5 * v_a   = {2.5 * v_a}  (calls v_a.__rmul__(2.5))")

    print("\n=== 2. Magnitude (`__abs__`) and Truthiness (`__bool__`) ===")
    print(f"  abs(v_a)    = {abs(v_a)} | bool(v_a)    = {bool(v_a)}")
    print(f"  abs(v_zero) = {abs(v_zero)} | bool(v_zero) = {bool(v_zero)}")


if __name__ == "__main__":
    main()
