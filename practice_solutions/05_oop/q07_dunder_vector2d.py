"""
Topic 05 - Object-Oriented Programming (OOP): Question 7
Problem: 2D Vector Geometry Class Overloading Python Dunder (Magic) Methods.
"""

import math
from typing import Union


class Vector2D:
    """Euclidean 2D Vector overloading arithmetic, comparison, and container dunders."""

    def __init__(self, x: float, y: float):
        self.x: float = float(x)
        self.y: float = float(y)

    def __repr__(self) -> str:
        return f"Vector2D(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other: object) -> "Vector2D":
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: object) -> "Vector2D":
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: Union[int, float]) -> "Vector2D":
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: Union[int, float]) -> "Vector2D":
        return self.__mul__(scalar)

    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2D):
            return False
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Vector2D):
            return NotImplemented
        return abs(self) < abs(other)

    def __bool__(self) -> bool:
        return not (math.isclose(self.x, 0.0) and math.isclose(self.y, 0.0))

    def __getitem__(self, index: int) -> float:
        if index in (0, -2):
            return self.x
        elif index in (1, -1):
            return self.y
        else:
            raise IndexError("Vector index out of range (0 or 1 only)")


# Verification & Execution
v1 = Vector2D(3.0, 4.0)
v2 = Vector2D(1.0, 2.0)
v_origin = Vector2D(0.0, 0.0)

print(f"repr(v1): {repr(v1)}")
print(f"str(v1): {str(v1)}")
print(f"v1 + v2: {repr(v1 + v2)}")
print(f"v1 - v2: {repr(v1 - v2)}")
print(f"v1 * 2.5: {repr(v1 * 2.5)}")
print(f"3 * v2: {repr(3 * v2)}")
print(f"abs(v1): {abs(v1)}")
print(f"bool(v1): {bool(v1)}")
print(f"bool(v_origin): {bool(v_origin)}")
print(f"Index Access: v1[0] = {v1[0]}, v1[1] = {v1[1]}")

vector_list = [Vector2D(10.0, 10.0), Vector2D(1.0, 1.0), Vector2D(3.0, 4.0)]
sorted_vectors = sorted(vector_list)
print("Sorted Vectors by Magnitude:")
print(sorted_vectors)
