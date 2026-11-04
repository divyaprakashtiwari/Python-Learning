"""
Topic 01: Functions
Example 01: Defining and Calling Functions (The DRY Principle & Docstrings)

Demonstrates how `def` encapsulates reusable logic, separates pure calculation
from console output, and attaches documentation via docstrings (`__doc__`).
"""


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Compute Body Mass Index (BMI) given weight in kg and height in meters."""
    if height_m <= 0:
        raise ValueError("Height must be strictly positive.")
    return round(weight_kg / (height_m ** 2), 2)


def classify_bmi(bmi: float) -> str:
    """Return the WHO health category corresponding to a BMI value."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25.0:
        return "Normal Weight"
    elif bmi < 30.0:
        return "Overweight"
    return "Obese"


def main() -> None:
    profiles = [
        ("Divya", 68.0, 1.75),
        ("Aarav", 82.0, 1.72),
        ("Sneha", 50.0, 1.68),
    ]

    print("=== 1. Reusable Function Calls (DRY Principle) ===")
    for name, weight, height in profiles:
        bmi_val = calculate_bmi(weight, height)
        category = classify_bmi(bmi_val)
        print(f"  {name:<6} | Weight: {weight:>4.1f}kg, Height: {height:.2f}m -> BMI: {bmi_val:>5.2f} ({category})")

    print("\n=== 2. Inspecting Function Docstrings (__doc__) ===")
    print(f"calculate_bmi.__doc__ : {calculate_bmi.__doc__!r}")


if __name__ == "__main__":
    main()
