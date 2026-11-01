"""
Topic 02: Installing Python and IDE Setup
Example 01: Verifying Python Installation and Module Search Paths

Demonstrates how to programmatically verify where the Python executable is
installed on your machine and where Python searches for imported modules.
"""

import os
import sys


def verify_python_installation() -> None:
    print("=== Python Installation Diagnostic ===")
    print(f"Executable Path exists : {os.path.exists(sys.executable)}")
    print(f"Python Version         : {sys.version.split()[0]}")
    print(f"Platform Identifier    : {sys.platform}")
    print(f"Default Encoding       : {sys.getdefaultencoding()}")

    print("\nTop 3 Module Search Entries (Relative/Standard):")
    for idx, entry in enumerate(sys.path[:3], start=1):
        display_entry = os.path.basename(entry) if entry else "<Current Working Directory>"
        print(f"  {idx}. {display_entry}")


if __name__ == "__main__":
    verify_python_installation()
