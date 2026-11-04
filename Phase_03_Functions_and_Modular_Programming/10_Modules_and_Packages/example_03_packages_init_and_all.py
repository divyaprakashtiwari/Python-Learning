"""
Phase 3 - Topic 10: Modules and Packages
Example 03: Packages, `__init__.py`, Relative Imports, and `__all__`

Demonstrates:
  - Organizing modules into a package directory (`ecommerce_pkg/`) with `__init__.py`
  - Importing re-exported symbols directly from the top-level package
  - Importing a specific submodule (`from ecommerce_pkg import discounts`)
  - How `__all__` defines the public export list of a package
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ecommerce_pkg
from ecommerce_pkg import PACKAGE_VERSION, seasonal_discount
from ecommerce_pkg import discounts


def main() -> None:
    print("=== 1. Using Symbols Re-Exported by `ecommerce_pkg/__init__.py` ===")
    print(f"  Package version              : {PACKAGE_VERSION}")
    discounted = seasonal_discount(4000.0, 15.0)
    print(f"  seasonal_discount(4000, 15%) : INR {discounted:,.2f}")

    print("\n=== 2. Accessing the Submodule Directly (`ecommerce_pkg.discounts`) ===")
    print(f"  Submodule `__name__`         : {discounts.__name__!r}")
    print(f"  Package `__all__` export list: {ecommerce_pkg.__all__}")


if __name__ == "__main__":
    main()
