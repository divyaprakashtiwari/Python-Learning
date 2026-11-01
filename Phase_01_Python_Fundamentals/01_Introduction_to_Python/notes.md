# Topic 01: Introduction to Python

---

## 1. Introduction

**Python** is a high-level, interpreted, general-purpose programming language created by **Guido van Rossum** and first released in **1991**.

In simple, beginner-friendly terms:
- **High-level** means you write code that looks very close to plain English (`print("Hello")` instead of managing memory addresses or hardware registers).
- **Interpreted** means you do not have to manually run a separate compiler step before executing your program—Python reads and runs your `.py` script directly.
- **Dynamically typed** means you do not need to declare variable types ahead of time (`x = 10` automatically knows `10` is an integer).

---

## 2. Why is it used?

Python is one of the most widely used programming languages in the world because it balances **developer productivity** with a **massive ecosystem**:

1. **Web & Backend Engineering:** Powers backends at Instagram, Spotify, Netflix, and Dropbox using frameworks like **Django** and **FastAPI**.
2. **Data Science, AI & Machine Learning:** The standard language for AI/ML research and production with **NumPy**, **Pandas**, **PyTorch**, and **Scikit-Learn**.
3. **Automation & DevOps:** Automates repetitive file operations, cloud infrastructure scripts, and CI/CD pipelines.
4. **Coding Interviews & DSA:** Its clean, concise syntax lets you focus on algorithmic logic rather than verbose boilerplate during timed coding interviews.

---

## 3. Syntax

Unlike C, C++, or Java, Python does **not** use curly braces `{}` or semicolons `;` to group statements. Instead, Python uses **indentation** (4 spaces per level by PEP 8 convention) and newlines:

```python
# Single-line comment starts with '#'

def main() -> None:
    message = "Hello, Python World!"
    print(message)

if __name__ == "__main__":
    main()
```

---

## 4. Explanation (How Python Works Step by Step)

When you run `python script.py` in your terminal, Python executes your program in three main stages:

```
+---------------------+      +-------------------------+      +--------------------------------+
|  1. Source Code     | ---> |  2. Bytecode Compiler   | ---> |  3. Python Virtual Machine     |
|     (script.py)     |      |     (.pyc in memory)    |      |     (PVM executes instructions)|
+---------------------+      +-------------------------+      +--------------------------------+
```

1. **Lexing & Parsing:** Python reads your `.py` file and checks for syntax or indentation errors.
2. **Compilation to Bytecode:** Python translates your source code into low-level, platform-independent instructions called **Bytecode** (cached inside `__pycache__/` when importing modules).
3. **Execution by the PVM (Python Virtual Machine):** The PVM reads each bytecode instruction and executes it on your CPU.

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_greeting_and_zen.py`](example_01_greeting_and_zen.py)
- [`example_02_runtime_environment_info.py`](example_02_runtime_environment_info.py)
- [`example_03_bytecode_disassembly.py`](example_03_bytecode_disassembly.py)

### Example 1: Greeting, Basic Calculation, and Core Principles (`example_01_greeting_and_zen.py`)

```python
def main() -> None:
    learner_name = "Divya Prakash"
    course_title = "Complete Python Notes: Beginner to Advanced DSA"
    print(f"Welcome, {learner_name}!")
    print(f"Course: {course_title}")
    print("-" * 55)

    daily_study_hours = 2.5
    days_in_month = 30
    monthly_hours = daily_study_hours * days_in_month
    print(f"Studying {daily_study_hours} hrs/day = {monthly_hours} hrs/month")

    zen_highlights = [
        "Beautiful is better than ugly.",
        "Explicit is better than implicit.",
        "Simple is better than complex.",
        "Readability counts.",
    ]
    print("\nKey Principles of Python (PEP 20):")
    for index, principle in enumerate(zen_highlights, start=1):
        print(f"  {index}. {principle}")


if __name__ == "__main__":
    main()
```

### Example 2: Inspecting the Python Runtime Environment (`example_02_runtime_environment_info.py`)

```python
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
```

### Example 3: How Python Executes Code via Bytecode (`example_03_bytecode_disassembly.py`)

```python
import dis


def calculate_rectangle_area(length: int, width: int) -> int:
    """Return the area of a rectangle."""
    area = length * width
    return area


def main() -> None:
    length = 12
    width = 5
    result = calculate_rectangle_area(length, width)

    print(f"Rectangle Dimensions : {length} x {width}")
    print(f"Calculated Area      : {result}")
    print("\n=== Compiled Bytecode Instructions (Code Object) ===")
    code_obj = calculate_rectangle_area.__code__
    print(f"Function Name        : {code_obj.co_name}")
    print(f"Local Variables      : {code_obj.co_varnames}")
    print(f"Bytecode Instruction Count: {len( list(dis.get_instructions(calculate_rectangle_area)) )}")
    print("\nInstruction Listing:")
    for instr in dis.get_instructions(calculate_rectangle_area):
        print(f"  Offset {instr.offset:>2}: {instr.opname:<18} {instr.argrepr}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
Welcome, Divya Prakash!
Course: Complete Python Notes: Beginner to Advanced DSA
-------------------------------------------------------
Studying 2.5 hrs/day = 75.0 hrs/month

Key Principles of Python (PEP 20):
  1. Beautiful is better than ugly.
  2. Explicit is better than implicit.
  3. Simple is better than complex.
  4. Readability counts.
```

### Output for Example 2:
```text
=== Python Runtime Environment Summary ===
Python Implementation : CPython
Python Version        : 3.13.7
Compiler Used         : MSC v.1944 64 bit (AMD64)
Operating System      : Windows (11)
Version Tuple         : major=3, minor=13, micro=7
```

### Output for Example 3:
```text
Rectangle Dimensions : 12 x 5
Calculated Area      : 60

=== Compiled Bytecode Instructions (Code Object) ===
Function Name        : calculate_rectangle_area
Local Variables      : ('length', 'width', 'area')
Bytecode Instruction Count: 6

Instruction Listing:
  Offset  0: RESUME             
  Offset  2: LOAD_FAST_LOAD_FAST length, width
  Offset  4: BINARY_OP          *
  Offset  8: STORE_FAST         area
  Offset 10: LOAD_FAST          area
  Offset 12: RETURN_VALUE       
```

---

## 7. Code Explanation

- **`if __name__ == "__main__":`** — This is Python's standard entry-point guard. It ensures `main()` runs when you execute the file directly (`python example_01_greeting_and_zen.py`), but prevents it from running unintentionally if another file imports it.
- **`print("-" * 55)`** — Multiplying a string by an integer repeats that string `55` times, creating a clean horizontal divider.
- **`platform.python_implementation()`** — Returns `"CPython"`, which is the official reference implementation of Python written in C.
- **`dis.get_instructions(func)`** — Uses Python's built-in disassembler module (`dis`) to inspect the exact bytecode instructions (`LOAD_FAST`, `BINARY_OP`, `RETURN_VALUE`) executed by the Python Virtual Machine.

---

## 8. Common Mistakes

1. **Inconsistent Indentation (`IndentationError`):**
   ```python
   # WRONG: Accidental leading space on the second line
   print("Line 1")
    print("Line 2")  # Raises IndentationError: unexpected indent
   ```
   Always use **4 spaces** per indentation level and never mix tabs and spaces.

2. **Case Sensitivity Mistakes (`NameError`):**
   Python is strictly case-sensitive. Writing `Print("Hello")` instead of lowercase `print("Hello")` raises `NameError: name 'Print' is not defined`.

3. **Running Python Code Inside the Interactive Shell vs Terminal:**
   Typing `python script.py` inside the `>>>` Python REPL prompt causes a `SyntaxError`. Run `python script.py` from your OS terminal (PowerShell, Command Prompt, or Bash).

---

## 9. Practice Questions

1. **Easy:** Write a Python program that prints your full name, your target role (e.g., `"Software Development Engineer"`), and calculates how many hours you will study in `365` days at `2` hours per day.
2. **Medium:** Write a script using the `sys` and `platform` modules that checks if the current Python version is at least `3.10`. Print `"Modern Python Environment"` if true, or `"Upgrade Recommended"` otherwise.
3. **Hard:** Write a Python function `compute_perimeter(length, width)` that returns `2 * (length + width)`, and use the `dis` module to count and display every bytecode instruction generated for that function.

---

## 10. Interview Questions

### Q1: Is Python purely an interpreted language, or does it compile code?
**Answer:** Python uses both compilation and interpretation. When you run a script, Python first **compiles** the `.py` source code into intermediate **bytecode** (`.pyc`), and then the **Python Virtual Machine (PVM)** **interprets** that bytecode line by line.

### Q2: What is CPython, and how does it differ from PyPy, Jython, or IronPython?
**Answer:**
- **CPython:** The default and official implementation of Python written in C.
- **PyPy:** An alternative implementation featuring a Just-In-Time (JIT) compiler for faster execution of long-running pure-Python loops.
- **Jython:** Runs Python on the Java Virtual Machine (JVM).
- **IronPython:** Runs Python on the .NET runtime.

### Q3: What is PEP 8, and why is it important?
**Answer:** **PEP 8** (Python Enhancement Proposal 8) is the official style guide for Python code. It standardizes 4-space indentation, `snake_case` for variables/functions, `PascalCase` for classes, and `UPPER_CASE` for constants so that all Python code across teams is uniform and readable.
