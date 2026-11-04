"""
Phase 3 - Topic 10: Modules and Packages
Example 01: Importing Custom Modules (`import`, `from ... import`, `as`, `sys.modules`)

Demonstrates:
  - Importing a sibling module (`billing_utils`) in 3 standard ways
  - How Python caches imported modules in `sys.modules` so repeated imports are O(1)
  - Inspecting module metadata (`__name__`, `__doc__`, `dir()`)
"""

import os
import sys

# Ensure the current topic directory is on `sys.path` regardless of working directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import billing_utils  # 1. Full module import
import billing_utils as bu  # 2. Aliased module import
from billing_utils import apply_gst, format_currency  # 3. Selective symbol import


def main() -> None:
    print("=== 1. Three Ways to Use an Imported Module ===")
    raw_price = 2500.0
    print(f"  Via `billing_utils.apply_gst` : {billing_utils.apply_gst(raw_price)}")
    print(f"  Via alias `bu.DEFAULT_CURRENCY`: {bu.DEFAULT_CURRENCY}")
    print(f"  Via `from ... import`         : {format_currency(apply_gst(raw_price))}")

    print("\n=== 2. Module Caching in `sys.modules` ===")
    print(f"  'billing_utils' in sys.modules: {'billing_utils' in sys.modules}")
    print(f"  `billing_utils is bu`         : {billing_utils is bu} (exact same module object!)")

    print("\n=== 3. Inspecting Public Attributes via `dir()` ===")
    public_attrs = [name for name in dir(billing_utils) if not name.startswith("_")]
    print(f"  Public API of billing_utils   : {public_attrs}")


if __name__ == "__main__":
    main()
