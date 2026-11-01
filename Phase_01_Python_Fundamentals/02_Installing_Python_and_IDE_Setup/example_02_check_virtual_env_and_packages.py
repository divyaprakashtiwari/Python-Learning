"""
Topic 02: Installing Python and IDE Setup
Example 02: Checking Virtual Environment Status and Standard Library Availability

Demonstrates how a developer script checks if it is running inside an isolated
virtual environment (`venv`) and verifies core built-in tools (`pip`, `venv`, `unittest`).
"""

import importlib.util
import sys


def check_environment_readiness() -> None:
    # A virtual environment changes sys.prefix compared to sys.base_prefix
    in_virtualenv = sys.prefix != sys.base_prefix

    print("=== Environment & Tooling Readiness ===")
    print(f"Running inside VirtualEnv (venv) : {in_virtualenv}")

    essential_modules = ["venv", "pip", "unittest", "sqlite3", "json"]
    print("\nStandard Tooling Verification:")
    for mod_name in essential_modules:
        spec = importlib.util.find_spec(mod_name)
        status = "INSTALLED" if spec is not None else "MISSING"
        print(f"  - {mod_name:<10} : {status}")


if __name__ == "__main__":
    check_environment_readiness()
