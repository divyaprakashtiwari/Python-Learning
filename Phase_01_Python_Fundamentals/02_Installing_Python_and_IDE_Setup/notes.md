# Topic 02: Installing Python and IDE Setup

---

## 1. Introduction

Before writing and running Python programs on your computer, you need two components:
1. **The Python Interpreter (`python`):** The official program downloaded from [python.org](https://www.python.org/downloads/) that reads and executes your `.py` files.
2. **An Integrated Development Environment (IDE) or Code Editor:** A smart workspace (such as **VS Code**, **PyCharm**, or **Antigravity**) that provides syntax highlighting, auto-completion (IntelliSense), error detection (linting), and an integrated debugger.

---

## 2. Why is it used?

A proper Python installation and IDE setup is critical in real-world software engineering because:
1. **PATH Accessibility:** Adding Python to your system `PATH` lets you run `python` and `pip` from any folder in your terminal.
2. **Instant Error Feedback:** Modern IDEs catch syntax errors, undefined variables, and type mismatches **before** you even run the code.
3. **Interactive Debugging:** Instead of guessing why a loop fails, you can set breakpoints in your IDE and inspect variables step by step.
4. **Code Formatting (PEP 8):** Tools like `Black` or `Ruff` automatically format your code on save so it always looks professional.

---

## 3. Syntax

### Terminal Commands for Verifying Installation & Running Scripts

```bash
# Check installed Python version
python --version

# Check installed pip (package installer) version
pip --version

# Launch interactive Python REPL (Read-Eval-Print Loop)
python

# Run a Python script file
python path/to/script.py
```

---

## 4. Explanation (Step-by-Step Setup & Workflow)

### Step 1: Installing Python
1. **Windows:** Download the installer from `python.org`. **Crucial Step:** Check the box **"Add python.exe to PATH"** on the first installer screen before clicking *Install Now*.
2. **macOS:** Install via the official installer from `python.org` or Homebrew (`brew install python`).
3. **Linux (Ubuntu/Debian):** Pre-installed on most distributions, or install via `sudo apt update && sudo apt install python3 python3-venv python3-pip`.

### Step 2: Setting Up Your IDE (VS Code / Antigravity / PyCharm)
1. Install the **Python Extension** (provides Pylance IntelliSense, debugging, and test discovery).
2. Select your Python Interpreter (`Ctrl+Shift+P` -> **Python: Select Interpreter**).
3. Configure **Editor: Tab Size** to `4` and enable **Insert Spaces** so pressing `Tab` inserts 4 spaces per PEP 8.

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_verify_installation_and_paths.py`](example_01_verify_installation_and_paths.py)
- [`example_02_check_virtual_env_and_packages.py`](example_02_check_virtual_env_and_packages.py)
- [`example_03_ide_linting_and_pep8_demo.py`](example_03_ide_linting_and_pep8_demo.py)

### Example 1: Verifying Python Installation and Module Search Paths (`example_01_verify_installation_and_paths.py`)

```python
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
```

### Example 2: Checking Virtual Environment Status and Standard Tooling (`example_02_check_virtual_env_and_packages.py`)

```python
import importlib.util
import sys


def check_environment_readiness() -> None:
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
```

### Example 3: IDE Features Demo — Docstrings, Type Hints, and PEP 8 (`example_03_ide_linting_and_pep8_demo.py`)

```python
def format_student_badge(student_name: str, roll_number: int, track: str = "Python + DSA") -> str:
    """
    Create a formatted student badge string for IDE preview and console output.

    Args:
        student_name: Full name of the learner.
        roll_number: Unique numeric ID assigned to the learner.
        track: Enrolled curriculum track name.

    Returns:
        A single-line formatted badge string.
    """
    cleaned_name = student_name.strip().title()
    return f"[ID #{roll_number:04d}] {cleaned_name} | Track: {track}"


def main() -> None:
    badge_1 = format_student_badge("divya prakash tiwari", 1)
    badge_2 = format_student_badge("aarav sharma", 42, track="Backend Engineering")

    print("=== IDE-Friendly PEP 8 Code Output ===")
    print(badge_1)
    print(badge_2)
    print("\nFunction Docstring (__doc__) inspected by IDEs on hover:")
    first_doc_line = format_student_badge.__doc__.strip().splitlines()[0]
    print(f"  \"{first_doc_line}\"")
    print(f"Type Annotations (__annotations__): {format_student_badge.__annotations__}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== Python Installation Diagnostic ===
Executable Path exists : True
Python Version         : 3.13.7
Platform Identifier    : win32
Default Encoding       : utf-8

Top 3 Module Search Entries (Relative/Standard):
  1. 02_Installing_Python_and_IDE_Setup
  2. python313.zip
  3. DLLs
```

### Output for Example 2:
```text
=== Environment & Tooling Readiness ===
Running inside VirtualEnv (venv) : False

Standard Tooling Verification:
  - venv       : INSTALLED
  - pip        : INSTALLED
  - unittest   : INSTALLED
  - sqlite3    : INSTALLED
  - json       : INSTALLED
```

### Output for Example 3:
```text
=== IDE-Friendly PEP 8 Code Output ===
[ID #0001] Divya Prakash Tiwari | Track: Python + DSA
[ID #0042] Aarav Sharma | Track: Backend Engineering

Function Docstring (__doc__) inspected by IDEs on hover:
  "Create a formatted student badge string for IDE preview and console output."
Type Annotations (__annotations__): {'student_name': <class 'str'>, 'roll_number': <class 'int'>, 'track': <class 'str'>, 'return': <class 'str'>}
```

---

## 7. Code Explanation

- **`sys.executable`** — Returns the exact file path of the currently running Python interpreter binary (`python.exe`).
- **`sys.path`** — A list of directory strings that specifies the search path for modules whenever you write `import something`. The first entry (`sys.path[0]`) is the folder containing the script being executed.
- **`sys.prefix != sys.base_prefix`** — The standard programmatic check to detect whether Python is currently running inside an activated virtual environment (`venv`).
- **`__doc__` and `__annotations__`** — Special dunder attributes that store a function's docstring and type hints, which IDEs display when you hover over a function call.

---

## 8. Common Mistakes

1. **Forgetting to check "Add Python to PATH" on Windows:**
   Result: Typing `python` in the terminal says `'python' is not recognized as an internal or external command` or opens the Microsoft Store. Fix: Re-run the installer, click **Modify**, and check **Add Python to environment variables** (or use the `py` launcher on Windows).
2. **Naming your own script after a built-in module (`random.py`, `math.py`, `json.py`):**
   Because `sys.path[0]` is your current script directory, naming your file `math.py` shadows Python's built-in `math` module and causes `AttributeError: partially initialized module 'math' has no attribute 'sqrt'`.
3. **Running code with a different interpreter than the IDE's selected interpreter:**
   Always verify that your terminal's `python --version` matches the interpreter shown in the bottom status bar of your IDE.

---

## 9. Practice Questions

1. **Easy:** Write a Python script that prints your current working directory using `os.getcwd()` and prints the default text encoding using `sys.getdefaultencoding()`.
2. **Medium:** Write a function `check_modules(module_names: list[str])` that uses `importlib.util.find_spec` to return a dictionary mapping each module name to `True` (if installed) or `False` (if missing). Test it with `["math", "datetime", "non_existent_pkg"]`.
3. **Hard:** Write a script that inspects `sys.path` and checks whether the current working directory (`os.getcwd()`) is in `sys.path`, and counts how many directories in `sys.path` actually exist on disk using `os.path.isdir()`.

---

## 10. Interview Questions

### Q1: What happens if you name your Python file `random.py` and write `import random` inside it?
**Answer:** Python searches `sys.path` in order, starting with the directory containing the running script (`sys.path[0]`). It finds your local `random.py` instead of the standard library's `random` module, causing a circular import and an `AttributeError`.

### Q2: What is the difference between the Python REPL and running a `.py` script?
**Answer:** The **REPL** (Read-Eval-Print Loop, started by typing `python` with no arguments) executes statements interactively one at a time and immediately prints expression results, but loses state when closed. A **`.py` script** saves code permanently on disk so it can be version-controlled with Git, tested, and imported as a module.

### Q3: How does Python know whether it is running inside a virtual environment (`venv`)?
**Answer:** When a virtual environment is active, `sys.prefix` points to the virtual environment directory while `sys.base_prefix` points to the global Python installation directory. Therefore, `sys.prefix != sys.base_prefix` evaluates to `True`.
