# Phase 3 — Topic 10: Modules and Packages

## 1. Introduction

As a Python project grows beyond a few hundred lines, keeping every function and class inside a single `.py` file becomes unmaintainable. Python organizes code into two hierarchical building blocks:

1. **Module:** Any single `.py` file containing Python definitions and statements (e.g., `billing_utils.py` is imported as the module `billing_utils`).
2. **Package:** A directory of modules (and subpackages) containing an **`__init__.py`** file (e.g., `ecommerce_pkg/__init__.py` and `ecommerce_pkg/discounts.py`).

---

## 2. Why is it used?

- **Separation of Concerns:** Authentication logic (`auth.py`), database models (`models.py`), and billing calculations (`billing_utils.py`) live in dedicated files that teams can work on independently without merge conflicts.
- **Namespace Protection:** Importing `billing_utils` keeps `billing_utils.GST_RATE` isolated from a `GST_RATE` defined in another module.
- **Reusability & Singleton Caching (`sys.modules`):** Even if 50 different files in your web app run `import billing_utils`, Python executes `billing_utils.py` **only once** and caches the module object in `sys.modules`.

---

## 3. Syntax

```python
# 1. Import the entire module object
import billing_utils
total = billing_utils.apply_gst(1000.0)

# 2. Import with an alias (`as`)
import billing_utils as bu
total = bu.apply_gst(1000.0)

# 3. Import specific symbols directly into current namespace
from billing_utils import apply_gst, format_currency
print(format_currency(apply_gst(1000.0)))

# 4. Relative import inside a package (`ecommerce_pkg/__init__.py`)
from .discounts import seasonal_discount

# 5. The `__main__` execution guard
if __name__ == "__main__":
    # Runs ONLY when this file is executed directly (`python my_script.py`),
    # NEVER when imported (`import my_script`).
    main()
```

---

## 4. Explanation (Step-by-Step)

### Step 1: What Happens During `import billing_utils`?
When Python executes `import billing_utils`:
1. **Cache Check (`sys.modules`):** Python checks if `"billing_utils"` is already in the `sys.modules` dictionary. If it is, Python immediately binds the cached module object ($O(1)$ lookup) without re-reading the file.
2. **Search Path (`sys.path`):** If not cached, Python searches the directories listed in `sys.path`:
   - First: The directory containing the entry-point script.
   - Second: `PYTHONPATH` environment variable directories.
   - Third: Standard library and virtual environment `site-packages` directories.
3. **Bytecode Compilation & Execution:** Python compiles `billing_utils.py` to bytecode (`.pyc` inside `__pycache__/`) and executes the module top-to-bottom to populate its namespace dictionary (`billing_utils.__dict__`).

### Step 2: Why `if __name__ == "__main__":` Is Essential
Every module has a built-in string variable `__name__`:
- When you run `python billing_utils.py` directly from the terminal, Python sets `__name__ = "__main__"`.
- When another file runs `import billing_utils`, Python sets `__name__ = "billing_utils"`.
Wrapping CLI/demo code inside `if __name__ == "__main__":` allows a file to be **both** an importable library module (with zero unwanted side effects on import) and a runnable script!

### Step 3: Packages, `__init__.py`, and `__all__`
```text
10_Modules_and_Packages/
├── billing_utils.py
└── ecommerce_pkg/
    ├── __init__.py
    └── discounts.py
```
- **`__init__.py`** runs automatically the first time `ecommerce_pkg` (or anything inside it) is imported. By placing `from .discounts import seasonal_discount` inside `__init__.py`, callers can write `from ecommerce_pkg import seasonal_discount` without needing to know the internal submodule structure.
- **`__all__ = ["PACKAGE_VERSION", "seasonal_discount"]`** explicitly declares the public API of a module or package and restricts what `from ecommerce_pkg import *` exports.

---

## 5. Minimum 3 Examples

### Supporting Module & Package Files
- `billing_utils.py` — Custom module defining `DEFAULT_CURRENCY`, `GST_RATE`, `apply_gst()`, and `format_currency()`.
- `ecommerce_pkg/__init__.py` & `ecommerce_pkg/discounts.py` — Sample package demonstrating relative imports and `__all__`.

---

### Example 1: Importing Custom Modules (`import`, `from ... import`, `as`, `sys.modules`)
File: `example_01_importing_custom_modules.py`

```python
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
```

---

### Example 2: The `if __name__ == "__main__":` Guard & `importlib.reload()`
File: `example_02_name_main_guard_and_reloading.py`

```python
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
```

---

### Example 3: Packages, `__init__.py`, Relative Imports, and `__all__`
File: `example_03_packages_init_and_all.py`

```python
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
```

---

## 6. Output

### Output — Example 1 (`example_01_importing_custom_modules.py`)
```text
=== 1. Three Ways to Use an Imported Module ===
  Via `billing_utils.apply_gst` : 2950.0
  Via alias `bu.DEFAULT_CURRENCY`: INR
  Via `from ... import`         : INR 2,950.00

=== 2. Module Caching in `sys.modules` ===
  'billing_utils' in sys.modules: True
  `billing_utils is bu`         : True (exact same module object!)

=== 3. Inspecting Public Attributes via `dir()` ===
  Public API of billing_utils   : ['DEFAULT_CURRENCY', 'GST_RATE', 'apply_gst', 'format_currency']
```

### Output — Example 2 (`example_02_name_main_guard_and_reloading.py`)
```text
=== 1. Inspecting `__name__` in Current Script vs Imported Module ===
  Current script `__name__`       : '__main__'
  Imported module `__name__`      : 'billing_utils'

=== 2. Running `billing_utils.py` Directly as `__main__` ===
  [billing_utils self-test] Running standalone diagnostics:
    __name__ = '__main__'
    Sample   = INR 1,180.00

=== 3. Reloading a Modified Module with `importlib.reload()` ===
  Mutated in-memory GST_RATE      : 0.28
  After `importlib.reload()`      : 0.18 (restored!)
```

### Output — Example 3 (`example_03_packages_init_and_all.py`)
```text
=== 1. Using Symbols Re-Exported by `ecommerce_pkg/__init__.py` ===
  Package version              : 1.2.0
  seasonal_discount(4000, 15%) : INR 3,400.00

=== 2. Accessing the Submodule Directly (`ecommerce_pkg.discounts`) ===
  Submodule `__name__`         : 'ecommerce_pkg.discounts'
  Package `__all__` export list: ['PACKAGE_VERSION', 'seasonal_discount']
```

---

## 7. Code Explanation

1. **Module Singleton Identity (`example_01`):** Even though we wrote `import billing_utils` and `import billing_utils as bu`, `billing_utils is bu` evaluates to `True`. Both names point to the exact same cached module object inside `sys.modules["billing_utils"]`.
2. **`__name__ == "__main__"` (`example_02`):** When `example_02` imports `billing_utils`, the `if __name__ == "__main__":` block inside `billing_utils.py` does **not** run because `billing_utils.__name__` is `'billing_utils'`. When `subprocess.run` invokes `python billing_utils.py` directly, `__name__` is `'__main__'` and the diagnostic prints.
3. **Package Facade Pattern (`example_03`):** `ecommerce_pkg/__init__.py` uses a relative import (`from .discounts import seasonal_discount`) to lift `seasonal_discount` to the top-level package namespace.

---

## 8. Common Mistakes

1. **Naming your script after a standard library module (`random.py`, `math.py`, `json.py`, `email.py`):**
   - Because the current script's directory is at index `0` of `sys.path`, naming your file `random.py` and writing `import random` imports **your own file instead of Python's standard library `random` module**, raising `AttributeError: partially initialized module 'random' has no attribute 'randint' (most likely due to a circular import)`!
2. **Circular Imports (`module_a` imports `from module_b import func_b` at top level while `module_b` imports `from module_a import func_a` at top level):**
   - Whoever is imported second sees the first module in a half-initialized state, raising `ImportError`. Fix circular dependencies by extracting shared helpers into a third module `common.py` (or importing the module itself `import module_b` and accessing `module_b.func_b` inside a function).
3. **Using wildcard imports (`from module import *`) in production code:**
   - Wildcard imports pollute the local namespace, silently shadow existing functions, and break IDE go-to-definition and static analysis.

---

## 9. Practice Questions

1. **Easy — Custom Geometry Module:**
   Create a module `geometry.py` with `circle_area(r)` and `rectangle_area(w, h)` plus an `if __name__ == "__main__":` self-test block. Import it from another script and verify that the self-test does not print on import.

2. **Medium — Inspecting `sys.path` and `sys.modules`:**
   Write a function `list_loaded_stdlib_modules() -> list[str]` that inspects `sys.modules` and returns a sorted list of currently loaded module names that do not contain a dot (`.`).

3. **Hard — Multi-Module Package with `__all__`:**
   Create a package `validators/` containing `email_validator.py`, `phone_validator.py`, and `__init__.py` that re-exports `is_valid_email` and `is_valid_phone` in `__all__`. Test importing the package.

---

## 10. Interview Questions

### Q1: What is the difference between a Regular Package and a Namespace Package (PEP 420) in Python 3.3+?
**Answer:**
- A **Regular Package** is a directory containing an explicit `__init__.py` file, which executes when the package is imported.
- A **Namespace Package** (introduced in Python 3.3 via PEP 420) omits `__init__.py`. This allows a single logical package name (such as `company.plugins.*`) to be split across multiple separate directories or pip wheels on `sys.path`. In standard single-repo projects, always include `__init__.py` to make packages explicit.

### Q2: If `config.py` defines `DEBUG = False`, and `module_a.py` runs `from config import DEBUG`, will `module_a` see the change if `module_b.py` later sets `config.DEBUG = True`?
**Answer:**
**No!** `from config import DEBUG` binds a local variable named `DEBUG` inside `module_a`'s namespace pointing to the boolean `False`. When `module_b` runs `config.DEBUG = True`, it rebinds the attribute on the `config` module object, leaving `module_a.DEBUG` pointing to `False`. To share mutable module-level flags across modules, always import the module itself (`import config`) and read `config.DEBUG`.

### Q3: What is the purpose of `__pycache__` and `.pyc` files?
**Answer:**
When Python imports a `.py` module, it compiles the source code into platform-independent **bytecode** and caches it in `__pycache__/<module>.cpython-313.pyc` along with the source file's modification timestamp. On subsequent runs, if the `.py` file has not been modified, Python skips parsing/compiling and loads the `.pyc` bytecode directly, speeding up startup time. (Note: `.pyc` files speed up **import/load time**, not execution speed.)
