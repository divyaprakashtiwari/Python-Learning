"""
Topic 04 - Functions: Question 4
Problem: Multiple Return Values, Guard Clauses, and Callable Factory Functions.
"""

from typing import Callable, List, Tuple


# 1. Multi-Value Statistical Analyzer with Early Return Guard Clause
def compute_descriptive_stats(dataset: List[float]) -> Tuple[int, float, float, float, float]:
    """Computes count, mean, median, sample variance, and range without external libraries."""
    if not dataset:
        return (0, 0.0, 0.0, 0.0, 0.0)

    n = len(dataset)
    mean_val = sum(dataset) / n

    # Median calculation on sorted copy
    sorted_data = sorted(dataset)
    mid = n // 2
    if n % 2 == 1:
        median_val = sorted_data[mid]
    else:
        median_val = (sorted_data[mid - 1] + sorted_data[mid]) / 2.0

    # Sample variance: sum((x - mean)^2) / (n - 1)
    if n > 1:
        variance_val = sum((x - mean_val) ** 2 for x in dataset) / (n - 1)
    else:
        variance_val = 0.0

    range_val = max(dataset) - min(dataset)

    return (
        n,
        round(mean_val, 2),
        round(median_val, 2),
        round(variance_val, 2),
        round(range_val, 2),
    )


# 2. Function Factory (Returning Callables)
def make_unit_converter(from_unit: str, to_unit: str) -> Callable[[float], float]:
    """Factory creating specialized unit conversion functions."""
    pair = (from_unit.upper(), to_unit.upper())
    converters = {
        ("C", "F"): lambda c: c * 9.0 / 5.0 + 32.0,
        ("F", "C"): lambda f: (f - 32.0) * 5.0 / 9.0,
        ("C", "K"): lambda c: c + 273.15,
        ("K", "C"): lambda k: k - 273.15,
        ("KM", "MILES"): lambda km: km * 0.621371,
        ("MILES", "KM"): lambda mi: mi / 0.621371,
    }

    if pair not in converters:
        raise ValueError(f"Unsupported unit conversion: {from_unit} -> {to_unit}")

    return converters[pair]


# Execution and Verification
data = [12.5, 14.0, 15.5, 18.0, 20.0, 22.5, 24.0]
cnt, mean, median, variance, range_val = compute_descriptive_stats(data)

print("Dataset Statistics:")
print(f"- Count: {cnt}")
print(f"- Mean: {mean:.2f}")
print(f"- Median: {median:.2f}")
print(f"- Variance: {variance:.2f}")
print(f"- Range: {range_val:.2f}")

c_to_f = make_unit_converter("C", "F")
c_to_k = make_unit_converter("C", "K")

print("\nFactory Conversion:")
print(f"- 100.0 C -> F: {c_to_f(100.0):.1f} F")
print(f"- 0.0 C -> K: {c_to_k(0.0):.2f} K")

empty_res = compute_descriptive_stats([])
print(f"Empty Dataset Guard: {empty_res}")
