"""
Submodule inside `ecommerce_pkg`: `discounts.py`
"""


def seasonal_discount(price: float, percent: float) -> float:
    """Apply a percentage discount to `price`."""
    return round(price * (1.0 - percent / 100.0), 2)


def _internal_rounding_helper(val: float) -> float:
    """Private helper (leading underscore convention)."""
    return round(val, 2)
