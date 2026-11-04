"""
Package initializer: `ecommerce_pkg/__init__.py`
Exposes public package API via relative imports and `__all__`.
"""

from .discounts import seasonal_discount

PACKAGE_VERSION = "1.2.0"

# Controls what `from ecommerce_pkg import *` exports and documents public API
__all__ = ["PACKAGE_VERSION", "seasonal_discount"]
