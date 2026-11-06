# Phase 5 — Topic 14: Virtual Environments and pip

## 1. Introduction

A **Virtual Environment (`venv`)** is an isolated, self-contained directory tree that gives a Python project its own private `site-packages/` folder and interpreter links. Coupled with **`pip`** (the Python Package Installer), virtual environments solve "dependency hell"—allowing Project A to run `Django 4.2` and `pydantic 1.10` while Project B on the exact same machine runs `FastAPI` and `pydantic 2.9` without conflict.

---

## 2. Why is it used?

1. **Per-Project Dependency Isolation:** Installing packages globally into the OS/system Python can overwrite libraries required by OS utilities or break sibling projects.
2. **Reproducible Deployments (`requirements.txt` / Lockfiles):** Pinning exact package versions (`fastapi==0.115.0`) guarantees that CI/CD servers, Docker containers, and teammates run identical dependency versions.
3. **Runtime Metadata Introspection (`importlib.metadata`):** Allows applications and plugin frameworks to inspect installed package versions and entry points at runtime without invoking shell commands.

---

## 3. Syntax

```powershell
# 1. Create a virtual environment named `.venv`
python -m venv .venv

# 2. Activate the virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Windows (CMD):
.venv\Scripts\activate.bat
# macOS / Linux (bash/zsh):
source .venv/bin/activate

# 3. Install, freeze, and sync packages using `python -m pip`
python -m pip install --upgrade pip
python -m pip install "fastapi>=0.115.0" "uvicorn~=0.30.0"
python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt

# 4. Deactivate
deactivate
```

---

## 4. Explanation (Step-by-Step)

1. **How `venv` Works Under the Hood (`pyvenv.cfg`, `sys.prefix`, `sys.base_prefix`):**
   - Running `python -m venv .venv` does **not** copy the entire Python standard library. Instead, it creates a lightweight `.venv/` folder containing `pyvenv.cfg`, a `Scripts/` (Windows) or `bin/` (POSIX) directory, and an empty `Lib/site-packages/` directory.
   - When Python starts from `.venv`, it reads `pyvenv.cfg` and sets `sys.prefix` to the `.venv` path while keeping `sys.base_prefix` pointing to the base system Python installation. Therefore, `sys.prefix != sys.base_prefix` is the canonical programmatic check for whether a virtual environment is active!
2. **Why `python -m pip install ...` Is Safer Than Bare `pip install ...`:**
   - If your shell `PATH` is misconfigured, bare `pip` might point to a global Python 3.11 installation while `python` points to `.venv`'s Python 3.13. Running `python -m pip ...` guarantees that packages are installed into the exact interpreter you are running.
3. **Version Specifiers in `requirements.txt` (PEP 440):**
   - `== 2.4.1`: **Exact pin** (required for reproducible production lockfiles).
   - `~= 2.4.1`: **Compatible release** (`>= 2.4.1, == 2.4.*`, i.e., `< 2.5.0`—accepts patch bugfixes without minor breaking changes).
   - `>= 2.0, < 3.0`: **Range constraint** (common in library `pyproject.toml` files).

---

## 5. Minimum 3 Examples

### Example 01: Detecting Active Virtual Environments via `sys.prefix` vs `sys.base_prefix`
File: [`example_01_venv_detection_sys_prefix_and_base_prefix.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/14_Virtual_Environments_and_Pip/example_01_venv_detection_sys_prefix_and_base_prefix.py)

```python
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
```

### Example 02: Querying Installed Packages Programmatically with `importlib.metadata`
File: [`example_02_importlib_metadata_installed_packages.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/14_Virtual_Environments_and_Pip/example_02_importlib_metadata_installed_packages.py)

```python
"""
Phase 5 - Topic 14: Virtual Environments and pip
Example 02: Querying Installed Packages Programmatically with `importlib.metadata`

Demonstrates:
  - Inspecting installed distributions (`pip` itself) using Python's built-in `importlib.metadata`
  - Listing package metadata (`Name`, `Version`, `Summary`) without spawning a subprocess
"""

from importlib import metadata


def inspect_distribution(pkg_name: str) -> dict[str, str]:
    """Fetch standard metadata for an installed distribution (`pip`)."""
    meta = metadata.metadata(pkg_name)
    return {
        "name": meta["Name"],
        "summary": meta["Summary"],
        "has_version": str(bool(metadata.version(pkg_name))),
    }


def main() -> None:
    print("=== Querying Installed `pip` Distribution via `importlib.metadata` ===")
    info = inspect_distribution("pip")
    print(f"  Package Name    : {info['name']}")
    print(f"  Version Present : {info['has_version']}")
    print(f"  Summary         : {info['summary']}")


if __name__ == "__main__":
    main()
```

### Example 03: Parsing `requirements.txt` Specifiers & Semantic Version Constraints
File: [`example_03_requirements_parser_and_semver_constraints.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/14_Virtual_Environments_and_Pip/example_03_requirements_parser_and_semver_constraints.py)

```python
"""
Phase 5 - Topic 14: Virtual Environments and pip
Example 03: Parsing `requirements.txt` Specifiers & Semantic Version Constraints

Demonstrates:
  - Parsing a `requirements.txt` file (ignoring comments `#` and blank lines)
  - Understanding version specifiers: pinned (`==`), compatible release (`~=`), and range (`>=,<`)
"""

import re


REQ_LINE_RE = re.compile(
    r"^(?P<package>[A-Za-z0-9_.-]+)\s*(?P<operator>==|~=|>=|<=|>|<|!=)?\s*(?P<version>[0-9A-Za-z.*+-]+)?$"
)


def parse_requirements(raw_text: str) -> list[dict[str, str | None]]:
    """Parse non-comment lines from a `requirements.txt` content string."""
    parsed: list[dict[str, str | None]] = []
    for raw_line in raw_text.splitlines():
        # Strip inline comments and surrounding whitespace
        clean = raw_line.split("#", maxsplit=1)[0].strip()
        if not clean:
            continue
        match = REQ_LINE_RE.match(clean)
        if not match:
            raise ValueError(f"Invalid requirement line: {clean!r}")
        parsed.append(match.groupdict())
    return parsed


def main() -> None:
    sample_requirements = """
    # Production dependencies
    fastapi == 0.115.0        # Exact pin for reproducible builds
    pydantic ~= 2.9.0         # Compatible release: >= 2.9.0, < 2.10.0
    uvicorn >= 0.30.0
    pytest                    # Unpinned (dev tool)
    """

    print("=== Parsing `requirements.txt` Specifiers ===")
    for item in parse_requirements(sample_requirements):
        print(f"  package={item['package']:<10} | op={str(item['operator']):<4} | version={item['version']}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== 1. Virtual Environment Detection (`sys.prefix != sys.base_prefix`) ===
  In Virtual Environment? : False (sys.prefix != sys.base_prefix)
  Executable Name         : 'python.exe'
  Site-packages configured: True

=== 2. Standard CLI Commands for `venv` Lifecycle ===
  Create venv                    -> `python -m venv .venv`
  Activate (Windows PowerShell)  -> `.venv\Scripts\Activate.ps1`
  Activate (Linux/macOS)         -> `source .venv/bin/activate`
  Deactivate                     -> `deactivate`
```

### Output — Example 02
```text
=== Querying Installed `pip` Distribution via `importlib.metadata` ===
  Package Name    : pip
  Version Present : True
  Summary         : The PyPA recommended tool for installing Python packages.
```

### Output — Example 03
```text
=== Parsing `requirements.txt` Specifiers ===
  package=fastapi    | op===   | version=0.115.0
  package=pydantic   | op=~=   | version=2.9.0
  package=uvicorn    | op=>=   | version=0.30.0
  package=pytest     | op=None | version=None
```

---

## 7. Code Explanation

1. **`sys.prefix != sys.base_prefix` (Example 01):** Works reliably even if you invoke `.venv/Scripts/python.exe script.py` directly **without** running the shell `Activate` script (unlike checking `os.environ.get("VIRTUAL_ENV")`, which is only set by shell activation).
2. **`importlib.metadata` (Example 02):** Added in Python 3.8, `importlib.metadata` replaces the deprecated `pkg_resources` library for reading `.dist-info` metadata at runtime.
3. **Compatible Release `~=` (Example 03):** `pydantic ~= 2.9.0` expands to `>= 2.9.0, == 2.9.*` (`< 2.10.0`), while `pydantic ~= 2.9` expands to `>= 2.9, == 2.*` (`< 3.0.0`).

---

## 8. Common Mistakes

1. **Committing the `.venv/` Directory to Git:**
   - Virtual environments contain OS-specific binary wheels (`.pyd` on Windows vs `.so` on Linux) and hardcoded absolute paths in `pyvenv.cfg`. **Never commit `.venv/`**—always add `.venv/` to `.gitignore` and commit `requirements.txt` or `pyproject.toml` instead.
2. **Running `pip freeze > requirements.txt` Inside the Global System Environment:**
   - Dumps dozens of unrelated system packages into your project's `requirements.txt`. Always activate your project's `.venv` first.
3. **Moving or Renaming a `.venv/` Folder After Creation:**
   - Script shebangs inside `.venv/Scripts/` store the original creation path; if you rename the parent project folder, delete `.venv` and recreate it with `python -m venv .venv && python -m pip install -r requirements.txt`.

---

## 9. Practice Questions

1. **Easy:** Write a function `require_virtualenv() -> None` that raises a descriptive `RuntimeError` if `sys.prefix == sys.base_prefix`.
2. **Medium:** Write a function `find_unpinned_packages(req_text: str) -> list[str]` that parses a `requirements.txt` string and returns all package names that do not use strict `==` pinning.
3. **Hard:** Write a semantic version comparator `satisfies_tilde_equals(installed: str, target: str) -> bool` that checks whether `installed` (e.g., `"2.9.4"`) satisfies `~= target` (e.g., `"2.9.1"`).

---

## 10. Interview Questions

### Q1: Do you HAVE to run `source .venv/bin/activate` to use a virtual environment (e.g., in a systemd service or cron job)?
**Answer:** **No!** Activating a venv in a shell merely prepends `.venv/bin` (or `.venv\Scripts`) to your shell's `PATH`. In production `systemd` units, Dockerfiles, or cron jobs, you can invoke the venv's Python binary directly by path (`/app/.venv/bin/python main.py`), and Python will automatically detect `pyvenv.cfg` and use the venv's `site-packages`.

### Q2: What is the difference between a Source Distribution (`sdist`, `.tar.gz`) and a Wheel (`.whl`) in `pip`?
**Answer:**
- **Wheel (`.whl`):** A pre-built binary/bytecode archive following PEP 427. `pip` installs wheels simply by unpacking them into `site-packages/`—no compiler required, fast and deterministic.
- **Source Distribution (`sdist`, `.tar.gz`):** Raw source code that `pip` must build locally (and compile C/C++/Rust extensions if any) during installation.

### Q3: What is `pyproject.toml` (PEP 518 / PEP 621), and how does it relate to `requirements.txt`?
**Answer:** `pyproject.toml` is the modern unified standard file for declaring a Python project's build system, abstract dependencies (`dependencies = ["fastapi>=0.115"]`), and tool configurations (`ruff`, `pytest`, `mypy`), whereas `requirements.txt` (or `uv.lock` / `poetry.lock`) pins the concrete transitive dependency graph for reproducible deployment.
