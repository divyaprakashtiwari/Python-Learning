"""
Phase 3 - Topic 09: Scope and Lifetime of Variables
Example 01: The LEGB Rule (Local -> Enclosing -> Global -> Built-in) & Variable Lifetime

Demonstrates:
  - How Python resolves variable names across the 4 LEGB scopes
  - How inner scopes can shadow outer scopes without overwriting them
  - Variable lifetime: local variables live only while the function's stack frame is active
"""

# [G] GLOBAL SCOPE: lives for the entire duration of the module
APP_THEME = "dark-global"


def outer_dashboard() -> None:
    # [E] ENCLOSING SCOPE: lives while `outer_dashboard` (or a closure) is active
    APP_THEME = "solarized-enclosing"

    def inner_widget() -> None:
        # [L] LOCAL SCOPE: created when `inner_widget()` is called, destroyed on return
        APP_THEME = "high-contrast-local"
        # [B] BUILT-IN SCOPE: `len` is resolved from Python's `builtins` module
        print(f"    [L - Local]     inner_widget sees APP_THEME = {APP_THEME!r} (len={len(APP_THEME)})")

    inner_widget()
    print(f"  [E - Enclosing] outer_dashboard sees APP_THEME = {APP_THEME!r}")


def read_global_without_shadowing() -> None:
    """When no Local or Enclosing `APP_THEME` exists, Python falls back to Global."""
    print(f"  [G - Global]    read_global sees APP_THEME     = {APP_THEME!r}")


def main() -> None:
    print("=== 1. Demonstrating the LEGB Name Resolution Hierarchy ===")
    outer_dashboard()
    read_global_without_shadowing()
    print(f"  [Module Root]   Global APP_THEME is still      = {APP_THEME!r}")

    print("\n=== 2. Inspecting Local vs Global Namespace Dictionaries ===")
    local_sample = 42
    print(f"  'local_sample' in locals()  : {'local_sample' in locals()}")
    print(f"  'local_sample' in globals() : {'local_sample' in globals()}")
    print(f"  'APP_THEME'    in globals() : {'APP_THEME' in globals()}")


if __name__ == "__main__":
    main()
