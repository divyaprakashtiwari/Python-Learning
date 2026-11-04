"""
Phase 3 - Topic 10: Modules and Packages
Example 02: The `if __name__ == "__main__":` Guard & `importlib.reload()`

Demonstrates:
  - Why `__name__` is `"__main__"` when a script is executed directly,
    but equals the module's filename (`"billing_utils"`) when imported
  - How `importlib.reload()` forces Python to re-execute a cached module
"""

import importlib
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import billing_utils


def main() -> None:
    print("=== 1. Inspecting `__name__` in Current Script vs Imported Module ===")
    print(f"  Current script `__name__`       : {__name__!r}")
    print(f"  Imported module `__name__`      : {billing_utils.__name__!r}")

    print("\n=== 2. Running `billing_utils.py` Directly as `__main__` ===")
    billing_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "billing_utils.py")
    proc = subprocess.run(
        [sys.executable, billing_script],
        capture_output=True,
        text=True,
        check=True,
    )
    for line in proc.stdout.strip().splitlines():
        print(f"  {line}")

    print("\n=== 3. Reloading a Modified Module with `importlib.reload()` ===")
    billing_utils.GST_RATE = 0.28  # Simulate in-memory mutation
    print(f"  Mutated in-memory GST_RATE      : {billing_utils.GST_RATE}")
    importlib.reload(billing_utils)
    print(f"  After `importlib.reload()`      : {billing_utils.GST_RATE} (restored!)")


if __name__ == "__main__":
    main()
