"""
Topic 08 - Modules and Packages: Question 2
Problem: Custom Statistics Module demonstrating __all__ export control and wildcard import simulation.
"""

from types import ModuleType
from typing import Any, List


def create_custom_stats_module() -> ModuleType:
    """Dynamically synthesizes custom_stats module with strict __all__ export controls."""
    mod = ModuleType("custom_stats")

    # Module Constants
    mod.VERSION = "2.1.0"
    mod.INTERNAL_PRECISION = 6
    mod._CALCULATION_CACHE = {}

    # Private Helpers (Leading underscore)
    def _validate_numeric_series(dataset: list) -> List[float]:
        if not dataset:
            raise ValueError("Dataset must be non-empty")
        return [float(x) for x in dataset]

    def _sum_of_squared_deviations(dataset: List[float], mean_val: float) -> float:
        return sum((x - mean_val) ** 2 for x in dataset)

    # Public Exported Functions
    def calculate_mean(dataset: list) -> float:
        data = _validate_numeric_series(dataset)
        return round(sum(data) / len(data), mod.INTERNAL_PRECISION)

    def calculate_median(dataset: list) -> float:
        data = sorted(_validate_numeric_series(dataset))
        n = len(data)
        mid = n // 2
        if n % 2 == 1:
            med = data[mid]
        else:
            med = (data[mid - 1] + data[mid]) / 2.0
        return round(med, mod.INTERNAL_PRECISION)

    def calculate_variance(dataset: list) -> float:
        data = _validate_numeric_series(dataset)
        if len(data) < 2:
            return 0.0
        mean_val = sum(data) / len(data)
        sq_dev = _sum_of_squared_deviations(data, mean_val)
        return round(sq_dev / (len(data) - 1), mod.INTERNAL_PRECISION)

    mod._validate_numeric_series = _validate_numeric_series
    mod._sum_of_squared_deviations = _sum_of_squared_deviations
    mod.calculate_mean = calculate_mean
    mod.calculate_median = calculate_median
    mod.calculate_variance = calculate_variance

    # Strict export whitelisting via __all__
    mod.__all__ = ["calculate_mean", "calculate_median", "calculate_variance", "VERSION"]

    return mod


def simulate_wildcard_import(mod: ModuleType) -> List[str]:
    """Simulates 'from module import *' honoring __all__ whitelisting."""
    if hasattr(mod, "__all__"):
        return list(mod.__all__)
    return [attr for attr in dir(mod) if not attr.startswith("_")]


# Verification & Execution
mod = create_custom_stats_module()

mean_val = mod.calculate_mean([10.0, 20.0, 30.0, 40.0, 50.0])
print(f"Mean Calculation: {mean_val}")

exported_symbols = simulate_wildcard_import(mod)
print("Exported Symbols via `from custom_stats import *`:")
print(exported_symbols)

direct_access_precision = mod.INTERNAL_PRECISION
print("\nEncapsulation Verification:")
print(f"- Is 'INTERNAL_PRECISION' in `__all__`? {'INTERNAL_PRECISION' in exported_symbols}")
print(f"- Can 'INTERNAL_PRECISION' be accessed directly via module attribute? True (Value: {direct_access_precision})")
print(f"- Are private functions ('_validate_numeric_series') in `__all__`? {'_validate_numeric_series' in exported_symbols}")
