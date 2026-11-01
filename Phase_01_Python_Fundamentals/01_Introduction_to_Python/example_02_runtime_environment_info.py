"""
Topic 01: Introduction to Python
Example 02: Inspecting the Python Runtime Environment

Uses Python's built-in `sys` and `platform` standard library modules to inspect
the Python version, implementation (CPython), and operating system platform.
"""

import platform
import sys


def inspect_python_runtime() -> None:
    print("=== Python Runtime Environment Summary ===")
    print(f"Python Implementation : {platform.python_implementation()}")
    print(f"Python Version        : {platform.python_version()}")
    print(f"Compiler Used         : {platform.python_compiler()}")
    print(f"Operating System      : {platform.system()} ({platform.release()})")
    print(f"Version Tuple         : major={sys.version_info.major}, "
          f"minor={sys.version_info.minor}, micro={sys.version_info.micro}")


if __name__ == "__main__":
    inspect_python_runtime()
