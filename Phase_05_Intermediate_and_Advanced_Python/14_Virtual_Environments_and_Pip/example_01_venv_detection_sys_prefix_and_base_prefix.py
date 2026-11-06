"""
Phase 5 - Topic 14: Virtual Environments and pip
Example 01: Detecting Active Virtual Environments via `sys.prefix` vs `sys.base_prefix`

Demonstrates:
  - How Python tracks the base installation (`sys.base_prefix`) vs active environment (`sys.prefix`)
  - Inspecting `sys.path` module search order and `site.getsitepackages()`
"""

from pathlib import Path
import site
import sys


def get_environment_report() -> dict[str, object]:
    """Return diagnostic details about the current Python interpreter and venv status."""
    in_venv = sys.prefix != sys.base_prefix
    return {
        "python_version": sys.version.split()[0],
        "in_virtualenv": in_venv,
        "executable_name": Path(sys.executable).name,
        "has_site_packages": len(site.getsitepackages()) > 0,
    }


def main() -> None:
    print("=== 1. Virtual Environment Detection (`sys.prefix != sys.base_prefix`) ===")
    report = get_environment_report()
    print(f"  In Virtual Environment? : {report['in_virtualenv']} (sys.prefix != sys.base_prefix)")
    print(f"  Executable Name         : {report['executable_name']!r}")
    print(f"  Site-packages configured: {report['has_site_packages']}")

    print("\n=== 2. Standard CLI Commands for `venv` Lifecycle ===")
    commands = [
        ("Create venv", "python -m venv .venv"),
        ("Activate (Windows PowerShell)", ".venv\\Scripts\\Activate.ps1"),
        ("Activate (Linux/macOS)", "source .venv/bin/activate"),
        ("Deactivate", "deactivate"),
    ]
    for step, cmd in commands:
        print(f"  {step:<30} -> `{cmd}`")


if __name__ == "__main__":
    main()
