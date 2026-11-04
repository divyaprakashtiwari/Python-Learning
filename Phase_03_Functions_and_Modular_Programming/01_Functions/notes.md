# Topic 01: Functions

---

## 1. Introduction

A **Function** is a named, reusable block of code designed to perform a single, well-defined task. You define a function once using the `def` keyword and call (invoke) it as many times as needed by writing `function_name(arguments)`.

In Python, **functions are first-class objects**—meaning a function is an object in memory just like an `int`, `str`, or `list`. You can assign a function to a variable, store functions inside a dictionary, pass a function as an argument to another function, and return a function from another function!

---

## 2. Why is it used?

1. **The DRY Principle (*Don't Repeat Yourself*):** Instead of copying and pasting 15 lines of tax-calculation code across 10 files, you write `calculate_tax()` once. If tax rules change, you update a single function.
2. **Single-Responsibility Decomposition:** Breaking a 300-line script into 8 small, focused functions makes every step easy to read, debug, and unit-test independently.
3. **Namespace Isolation:** Variables created inside a function are local to that function, preventing accidental variable name collisions across a large project.

---

## 3. Syntax

```python
def function_name(param1: int, param2: int) -> int:
    """Docstring explaining what the function does, its inputs, and return value."""
    result = param1 + param2
    return result


# Calling (invoking) the function
answer = function_name(10, 20)
```

---

## 4. Explanation (How Function Definition & Invocation Work)

1. **Definition Time (`def`):**
   - When Python executes `def calculate_bmi(...):`, it does **not** run the body of the function yet.
   - Instead, it compiles the function body into a bytecode `code` object, wraps it in a `function` object in memory, attaches its docstring to `__doc__`, and binds the name `calculate_bmi` to that object.
2. **Call Time (`calculate_bmi(68.0, 1.75)`):**
   - The parentheses `()` trigger execution (`CALL` bytecode instruction).
   - Python creates a brand-new **Stack Frame** (local namespace) for this call, binds parameters `weight_kg = 68.0` and `height_m = 1.75`, and executes the body line by line.
   - When `return` is reached (or the body ends, which implicitly returns `None`), the stack frame is popped and the return value is handed back to the caller.

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_defining_and_calling_functions.py`](example_01_defining_and_calling_functions.py)
- [`example_02_functions_as_first_class_objects.py`](example_02_functions_as_first_class_objects.py)
- [`example_03_modular_decomposition_pipeline.py`](example_03_modular_decomposition_pipeline.py)

### Example 1: Defining and Calling Functions (`example_01_defining_and_calling_functions.py`)

```python
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Compute Body Mass Index (BMI) given weight in kg and height in meters."""
    if height_m <= 0:
        raise ValueError("Height must be strictly positive.")
    return round(weight_kg / (height_m ** 2), 2)


def classify_bmi(bmi: float) -> str:
    """Return the WHO health category corresponding to a BMI value."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25.0:
        return "Normal Weight"
    elif bmi < 30.0:
        return "Overweight"
    return "Obese"


def main() -> None:
    profiles = [
        ("Divya", 68.0, 1.75),
        ("Aarav", 82.0, 1.72),
        ("Sneha", 50.0, 1.68),
    ]

    print("=== 1. Reusable Function Calls (DRY Principle) ===")
    for name, weight, height in profiles:
        bmi_val = calculate_bmi(weight, height)
        category = classify_bmi(bmi_val)
        print(f"  {name:<6} | Weight: {weight:>4.1f}kg, Height: {height:.2f}m -> BMI: {bmi_val:>5.2f} ({category})")

    print("\n=== 2. Inspecting Function Docstrings (__doc__) ===")
    print(f"calculate_bmi.__doc__ : {calculate_bmi.__doc__!r}")


if __name__ == "__main__":
    main()
```

### Example 2: Functions as First-Class Objects (`example_02_functions_as_first_class_objects.py`)

```python
from typing import Callable


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def apply_operation(func: Callable[[float, float], float], x: float, y: float) -> float:
    """Higher-order function that accepts another function `func` and invokes it."""
    return func(x, y)


def main() -> None:
    compute = multiply
    print("=== 1. Assigning a Function to a Variable ===")
    print(f"compute(6, 7) via alias : {compute(6, 7)}")

    operations: dict[str, Callable[[float, float], float]] = {
        "ADD": add,
        "SUB": subtract,
        "MUL": multiply,
    }
    print("\n=== 2. Dictionary Dispatch Table ===")
    commands = [("ADD", 15, 5), ("SUB", 15, 5), ("MUL", 15, 5)]
    for op_name, x, y in commands:
        handler = operations[op_name]
        result = apply_operation(handler, x, y)
        print(f"  Command {op_name}({x}, {y}) -> {result}")


if __name__ == "__main__":
    main()
```

### Example 3: Single-Responsibility Decomposition (`example_03_modular_decomposition_pipeline.py`)

```python
def validate_items(items: list[tuple[str, int, float]]) -> bool:
    """Return True if the order is non-empty and all quantities/prices are positive."""
    if not items:
        return False
    return all(qty > 0 and price >= 0.0 for _, qty, price in items)


def compute_subtotal(items: list[tuple[str, int, float]]) -> float:
    """Sum (quantity * unit_price) across all line items."""
    return sum(qty * price for _, qty, price in items)


def apply_coupon_discount(subtotal: float, coupon_code: str) -> float:
    """Apply flat percentage discount based on coupon code."""
    discounts = {"SAVE10": 0.10, "FESTIVE20": 0.20}
    rate = discounts.get(coupon_code.upper(), 0.0)
    return round(subtotal * (1.0 - rate), 2)


def generate_order_summary(items: list[tuple[str, int, float]], coupon: str = "") -> str:
    """Coordinator function composing validation, subtotal, and discount helpers."""
    if not validate_items(items):
        return "ERROR: Invalid order items."
    raw_subtotal = compute_subtotal(items)
    discounted = apply_coupon_discount(raw_subtotal, coupon)
    gst_total = round(discounted * 1.18, 2)
    return (
        f"Subtotal: Rs.{raw_subtotal:.2f} | "
        f"After Coupon ({coupon or 'NONE'}): Rs.{discounted:.2f} | "
        f"Final (incl. 18% GST): Rs.{gst_total:.2f}"
    )


def main() -> None:
    cart = [
        ("DSA Course", 1, 1500.0),
        ("Mock Interviews", 2, 500.0),
    ]
    print("=== Single-Responsibility Order Pipeline ===")
    print(generate_order_summary(cart, coupon="FESTIVE20"))
    print(generate_order_summary(cart, coupon=""))
    print(generate_order_summary([], coupon="SAVE10"))


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== 1. Reusable Function Calls (DRY Principle) ===
  Divya  | Weight: 68.0kg, Height: 1.75m -> BMI: 22.20 (Normal Weight)
  Aarav  | Weight: 82.0kg, Height: 1.72m -> BMI: 27.72 (Overweight)
  Sneha  | Weight: 50.0kg, Height: 1.68m -> BMI: 17.72 (Underweight)

=== 2. Inspecting Function Docstrings (__doc__) ===
calculate_bmi.__doc__ : 'Compute Body Mass Index (BMI) given weight in kg and height in meters.'
```

### Output for Example 2:
```text
=== 1. Assigning a Function to a Variable ===
compute(6, 7) via alias : 42

=== 2. Dictionary Dispatch Table ===
  Command ADD(15, 5) -> 20
  Command SUB(15, 5) -> 10
  Command MUL(15, 5) -> 75
```

### Output for Example 3:
```text
=== Single-Responsibility Order Pipeline ===
Subtotal: Rs.2500.00 | After Coupon (FESTIVE20): Rs.2000.00 | Final (incl. 18% GST): Rs.2360.00
Subtotal: Rs.2500.00 | After Coupon (NONE): Rs.2500.00 | Final (incl. 18% GST): Rs.2950.00
ERROR: Invalid order items.
```

---

## 7. Code Explanation

- **`compute = multiply` vs `compute = multiply(6, 7)`:** Writing `multiply` **without parentheses** passes a reference to the function object itself. Writing `multiply(6, 7)` **with parentheses** calls the function immediately and assigns its return value `42`.
- **`operations: dict[str, Callable[[float, float], float]]`:** Maps string command names to function objects so `operations[op_name]` resolves the right handler in `O(1)` time without a long `if/elif` chain.

---

## 8. Common Mistakes

1. **Printing Inside a Function Instead of Returning (`print` vs `return`):**
   ```python
   # WRONG: Prints 15, but returns None!
   def add_bad(a, b):
       print(a + b)

   total = add_bad(5, 10) + 20  # Raises TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
   ```
   Always `return` computed values from logic functions and let the caller decide whether to print them.
2. **Accidentally Calling a Function When Passing It as a Callback:**
   Writing `sorted(words, key=str.lower())` calls `str.lower()` with no arguments and raises a `TypeError`. Pass the function reference **without parentheses**: `sorted(words, key=str.lower)`.
3. **Calling a Function Before Its `def` Statement Executes:**
   Unlike C# or JavaScript function hoisting, Python executes top-to-bottom. A function's `def` statement must execute before any line actually calls that function.

---

## 9. Practice Questions

1. **Easy:** Write a pure function `celsius_to_fahrenheit(c: float) -> float` and `fahrenheit_to_celsius(f: float) -> float` and verify that converting `100.0 C -> F -> C` returns `100.0`.
2. **Medium:** Build a calculator dispatch dictionary supporting `"+"`, `"-"`, `"*"`, `"/"`, `"//"`, and `"%"` that maps each operator string to a function and safely handles division by zero.
3. **Hard:** Write a higher-order function `compose(f, g)` that takes two single-argument functions `f` and `g` and returns a new function `h(x)` that computes `f(g(x))`.

---

## 10. Interview Questions

### Q1: What does it mean that "functions are first-class citizens" in Python?
**Answer:** It means functions are treated like any other object (`int`, `str`, `dict`) at runtime:
1. They can be assigned to variables.
2. They can be stored in data structures (lists, dicts, sets).
3. They can be passed as arguments to higher-order functions (`map`, `filter`, `sorted(key=...)`).
4. They can be returned from other functions (enabling closures and decorators).

### Q2: What is a Pure Function, and why are pure functions easier to test?
**Answer:** A **Pure Function** has two properties:
1. Given the same inputs, it **always returns the exact same output** (deterministic).
2. It has **zero side effects** (it does not mutate global variables, modify input lists in-place, or perform I/O).
Because pure functions do not depend on hidden external state, they are thread-safe, cacheable (`@lru_cache`), and trivial to unit-test.

### Q3: What does a Python function return if it has no `return` statement (or a bare `return`)?
**Answer:** Every Python function implicitly returns **`None`** if execution reaches the end of the function body without hitting an explicit `return value` statement.
