# Topic 04: Data Types

---

## 1. Introduction

A **Data Type** defines the kind of value an object holds and what operations can be performed on it. For example, you can divide two numbers (`10 / 2`), and you can uppercase a string (`"hello".upper()`), but you cannot divide a string by a number (`"hello" / 2` raises a `TypeError`).

In Python, **everything is an object**, and every object has a specific data type that you can inspect at any time using `type(value)` or `isinstance(value, ExpectedType)`.

---

## 2. Why is it used?

Understanding Python's built-in data types is essential because:
1. **Memory & Performance:** Choosing a `set` instead of a `list` for membership checks speeds up lookups from `O(n)` to `O(1)`.
2. **Financial Accuracy:** Knowing how binary `float` works prevents rounding bugs in banking or billing software (where `decimal.Decimal` is required).
3. **Bug Prevention:** Knowing which types are **mutable** (can be modified in-place) vs **immutable** (cannot be modified in-place) prevents accidental side effects across functions.

---

## 3. Syntax

```python
# Numeric Types
count: int = 100
price: float = 99.95
wave: complex = 2 + 3j

# Boolean, String, and None
is_valid: bool = True
title: str = "Python DSA"
empty_slot: None = None

# Collection Types
items_list: list[int] = [1, 2, 3]
point_tuple: tuple[int, int] = (10, 20)
unique_set: set[str] = {"a", "b"}
user_dict: dict[str, int] = {"id": 101}
```

---

## 4. Explanation (Complete Classification of Python Data Types)

| Category | Type Name | Example | Mutable? | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Numeric** | `int` | `42`, `-7`, `0b101` | Immutable | Arbitrary-precision whole numbers (never overflow!) |
| **Numeric** | `float` | `3.14`, `6.02e23` | Immutable | 64-bit IEEE-754 double-precision decimal numbers |
| **Numeric** | `complex` | `3 + 4j` | Immutable | Complex numbers with `.real` and `.imag` parts |
| **Boolean** | `bool` | `True`, `False` | Immutable | Logical truth values (`bool` is a subclass of `int`: `True == 1`, `False == 0`) |
| **Text Sequence** | `str` | `"Hello"` | Immutable | Unicode character sequences |
| **Sequence** | `list` | `[1, 2, 3]` | **Mutable** | Ordered, resizable collection of elements |
| **Sequence** | `tuple` | `(1, 2, 3)` | Immutable | Ordered, fixed-size collection of elements |
| **Sequence** | `range` | `range(0, 10)` | Immutable | Lazy sequence of integers commonly used in loops |
| **Set** | `set` | `{1, 2, 3}` | **Mutable** | Unordered collection of unique, hashable elements |
| **Mapping** | `dict` | `{"k": "v"}` | **Mutable** | Key-value hash map preserving insertion order |
| **Null** | `NoneType` | `None` | Immutable | Singleton object representing the absence of a value |

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_primitive_and_numeric_types.py`](example_01_primitive_and_numeric_types.py)
- [`example_02_collection_types_overview.py`](example_02_collection_types_overview.py)
- [`example_03_mutability_and_float_precision.py`](example_03_mutability_and_float_precision.py)

### Example 1: Primitive and Numeric Data Types (`example_01_primitive_and_numeric_types.py`)

```python
def main() -> None:
    regular_int = 42
    binary_literal = 0b101010       # 42 in binary
    hex_literal = 0x2A              # 42 in hexadecimal
    huge_int = 10 ** 30             # 1 followed by 30 zeros

    pi_approx = 3.14159
    avogadro = 6.022e23
    impedance = 3 + 4j

    is_verified = True
    greeting = "Namaste Python"
    missing_value = None

    print("=== Python Primitive & Numeric Data Types ===")
    print(f"regular_int    : {regular_int} (bin={binary_literal}, hex={hex_literal}) -> {type(regular_int).__name__}")
    print(f"huge_int       : {huge_int} -> {type(huge_int).__name__}")
    print(f"pi_approx      : {pi_approx}, avogadro={avogadro:.3e} -> {type(pi_approx).__name__}")
    print(f"impedance      : {impedance} (real={impedance.real}, imag={impedance.imag}, abs={abs(impedance)}) -> {type(impedance).__name__}")
    print(f"is_verified    : {is_verified} (isinstance of int: {isinstance(is_verified, int)}) -> {type(is_verified).__name__}")
    print(f"greeting       : {greeting!r} (length={len(greeting)}) -> {type(greeting).__name__}")
    print(f"missing_value  : {missing_value} -> {type(missing_value).__name__}")


if __name__ == "__main__":
    main()
```

### Example 2: Built-in Collection Data Types (`example_02_collection_types_overview.py`)

```python
def main() -> None:
    languages_list = ["Python", "C++", "Java"]               # Ordered, mutable
    coordinates_tuple = (28.61, 77.20)                       # Ordered, immutable
    unique_tags_set = {"dsa", "python", "backend", "dsa"}    # Unordered, unique elements
    student_dict = {"name": "Divya", "phase": 1}             # Key-value mapping
    raw_bytes = b"HTTP/1.1"                                  # Immutable byte sequence

    samples = [
        ("languages_list", languages_list),
        ("coordinates_tuple", coordinates_tuple),
        ("unique_tags_set", unique_tags_set),
        ("student_dict", student_dict),
        ("raw_bytes", raw_bytes),
    ]

    print("=== Built-in Collection Data Types ===")
    for label, obj in samples:
        display_val = sorted(obj) if isinstance(obj, set) else obj
        print(f"{label:<18} | Type: {type(obj).__name__:<6} | Len: {len(obj)} | Value: {display_val}")


if __name__ == "__main__":
    main()
```

### Example 3: Mutable vs Immutable Types & Floating-Point Precision (`example_03_mutability_and_float_precision.py`)

```python
from decimal import Decimal
import math


def main() -> None:
    print("=== 1. Immutable (int/str) vs Mutable (list) ===")
    word = "Py"
    initial_word_id = id(word)
    word += "thon"
    print(f"String after '+=' changed memory ID : {initial_word_id != id(word)} (Value: {word})")

    numbers = [10, 20]
    initial_list_id = id(numbers)
    numbers.append(30)
    print(f"List after '.append()' kept same ID : {initial_list_id == id(numbers)} (Value: {numbers})")

    print("\n=== 2. Floating-Point Precision (0.1 + 0.2) ===")
    float_sum = 0.1 + 0.2
    print(f"Raw float (0.1 + 0.2)            : {float_sum:.17f}")
    print(f"Direct equality (0.1 + 0.2 == 0.3): {float_sum == 0.3}")
    print(f"Safe check with math.isclose()   : {math.isclose(float_sum, 0.3)}")

    exact_sum = Decimal("0.1") + Decimal("0.2")
    print(f"Exact Decimal('0.1') + Decimal('0.2') == Decimal('0.3'): {exact_sum == Decimal('0.3')} (Value: {exact_sum})")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== Python Primitive & Numeric Data Types ===
regular_int    : 42 (bin=42, hex=42) -> int
huge_int       : 1000000000000000000000000000000 -> int
pi_approx      : 3.14159, avogadro=6.022e+23 -> float
impedance      : (3+4j) (real=3.0, imag=4.0, abs=5.0) -> complex
is_verified    : True (isinstance of int: True) -> bool
greeting       : 'Namaste Python' (length=14) -> str
missing_value  : None -> NoneType
```

### Output for Example 2:
```text
=== Built-in Collection Data Types ===
languages_list     | Type: list   | Len: 3 | Value: ['Python', 'C++', 'Java']
coordinates_tuple  | Type: tuple  | Len: 2 | Value: (28.61, 77.2)
unique_tags_set    | Type: set    | Len: 3 | Value: ['backend', 'dsa', 'python']
student_dict       | Type: dict   | Len: 2 | Value: {'name': 'Divya', 'phase': 1}
raw_bytes          | Type: bytes  | Len: 8 | Value: b'HTTP/1.1'
```

### Output for Example 3:
```text
=== 1. Immutable (int/str) vs Mutable (list) ===
String after '+=' changed memory ID : True (Value: Python)
List after '.append()' kept same ID : True (Value: [10, 20, 30])

=== 2. Floating-Point Precision (0.1 + 0.2) ===
Raw float (0.1 + 0.2)            : 0.30000000000000004
Direct equality (0.1 + 0.2 == 0.3): False
Safe check with math.isclose()   : True
Exact Decimal('0.1') + Decimal('0.2') == Decimal('0.3'): True (Value: 0.3)
```

---

## 7. Code Explanation

- **`0b101010` and `0x2A`** — Python supports binary (`0b`), octal (`0o`), and hexadecimal (`0x`) integer literals natively.
- **`isinstance(is_verified, int)`** — In Python, `bool` inherits directly from `int`. `True` behaves like `1` and `False` behaves like `0` (`True + True == 2`).
- **`math.isclose(0.1 + 0.2, 0.3)`** — Because binary floating-point numbers cannot represent `0.1` or `0.2` with exact finite bits, `0.1 + 0.2` evaluates to `0.30000000000000004`. Always use `math.isclose()` for float comparisons or `decimal.Decimal` for currency math.

---

## 8. Common Mistakes

1. **Creating an Empty Set with `{}`:**
   Writing `empty = {}` creates an empty **dictionary** (`dict`), not a `set`! To create an empty set, you must write `empty_set = set()`.
2. **Creating a 1-Element Tuple Without a Trailing Comma:**
   Writing `single = (5)` is just the integer `5` inside parentheses (`type(single)` is `int`). A 1-element tuple requires a trailing comma: `single = (5,)`.
3. **Comparing Floats with `==`:**
   Never write `if 0.1 + 0.2 == 0.3:`. Use `math.isclose(a, b)` instead.

---

## 9. Practice Questions

1. **Easy:** Create one variable of each primitive type (`int`, `float`, `bool`, `str`, `None`) and print both its value and `type(var).__name__`.
2. **Medium:** Write a function `count_types(items: list)` that takes a mixed list like `[1, "a", 2.5, True, None, 10]` and returns a dictionary counting how many items belong to each exact type name (`type(x).__name__`).
3. **Hard:** Write a financial billing function using `decimal.Decimal` that computes the exact compound interest on `Decimal("10000.00")` at `7.5%` annual interest over `3` years without any binary floating-point drift.

---

## 10. Interview Questions

### Q1: Why don't integers overflow in Python 3 like they do in C++ or Java?
**Answer:** In Python 3, the `int` type has **arbitrary precision** (formerly `long` in Python 2). Python dynamically allocates more bytes in memory as an integer grows larger, limited only by available RAM.

### Q2: Why does `isinstance(True, int)` return `True`?
**Answer:** For historical reasons, Python's `bool` type was introduced in Python 2.3 as a subclass of `int` (`issubclass(bool, int) == True`), where `True` has integer value `1` and `False` has integer value `0`. If you need to check for an `int` while excluding `bool`, check `type(x) is int` or `isinstance(x, int) and not isinstance(x, bool)`.

### Q3: What is the difference between `type(x) == int` and `isinstance(x, int)`?
**Answer:** `type(x) is int` checks for an **exact** type match and ignores inheritance, whereas `isinstance(x, int)` returns `True` for `int` and any subclass of `int` (such as `bool` or custom subclasses).
