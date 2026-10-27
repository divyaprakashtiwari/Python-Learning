"""
Topic 07 - Exception Handling: Question 1
Problem: Robust Mathematical Input Evaluator with Specific ValueError & ZeroDivisionError Trapping.
"""

from typing import Any, Dict


def safe_compute_ratio(numerator_str: str, denominator_str: str) -> Dict[str, Any]:
    """Computes division ratio with targeted exception handling for conversion and math errors."""
    try:
        numerator = float(numerator_str)
        denominator = float(denominator_str)
        ratio = numerator / denominator
        return {
            "status": "SUCCESS",
            "ratio": round(ratio, 4)
        }
    except ValueError as err:
        return {
            "status": "ERROR",
            "error_type": "ValueError",
            "message": str(err)
        }
    except ZeroDivisionError:
        return {
            "status": "ERROR",
            "error_type": "ZeroDivisionError",
            "message": "Denominator cannot be zero"
        }


# Verification & Execution
test1 = safe_compute_ratio("100", "4")
test2 = safe_compute_ratio("75.5", "0")
test3 = safe_compute_ratio("abc", "10")
test4 = safe_compute_ratio("22", "7")

print("Test 1 (100 / 4):")
print(test1)

print("\nTest 2 (75.5 / 0):")
print(test2)

print("\nTest 3 ('abc' / 10):")
print(test3)

print("\nTest 4 (22 / 7):")
print(test4)
