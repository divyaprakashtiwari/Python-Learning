"""
Topic 04 - Functions: Question 1
Problem: Cone Properties Calculator (Pure functions, return values, and input validation).
"""

import math
from typing import Dict


def calculate_cone_properties(radius: float, height: float) -> Dict[str, float]:
    """Calculates geometric properties of a right circular cone without side effects."""
    if radius <= 0 or height <= 0:
        raise ValueError("Dimensions must be strictly positive numbers")

    slant_height = math.sqrt(radius ** 2 + height ** 2)
    lateral_area = math.pi * radius * slant_height
    total_area = math.pi * radius * (radius + slant_height)
    volume = (1 / 3) * math.pi * (radius ** 2) * height

    return {
        "slant_height": round(slant_height, 2),
        "lateral_area": round(lateral_area, 2),
        "total_area": round(total_area, 2),
        "volume": round(volume, 2)
    }


# Caller execution & presentation
r = 3.0
h = 4.0
metrics = calculate_cone_properties(r, h)

print(f"Cone Properties for r={r:.2f}, h={h:.2f}:")
print(f"- Slant Height: {metrics['slant_height']:.2f}")
print(f"- Lateral Surface Area: {metrics['lateral_area']:.2f}")
print(f"- Total Surface Area: {metrics['total_area']:.2f}")
print(f"- Volume: {metrics['volume']:.2f}")

# Input validation test
try:
    calculate_cone_properties(-2.0, 5.0)
except ValueError as err:
    print(f"\nValidation Guard Verified: Caught expected ValueError: {err}")
