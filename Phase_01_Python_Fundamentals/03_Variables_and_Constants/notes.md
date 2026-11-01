# Topic 03: Variables and Constants

---

## 1. Introduction

A **variable** is a named label that points to a value (an object) stored in your computer's memory. Unlike languages such as C or Java where a variable acts like a fixed-type box in memory, a Python variable acts like a **sticky note (reference)** attached to an object.

A **constant** is a variable whose value is meant to remain unchanged throughout the entire execution of a program (such as `PI = 3.14159` or `MAX_LOGIN_ATTEMPTS = 5`).

---

## 2. Why is it used?

Variables and constants are fundamental to every program because:
1. **Reusability:** Instead of repeating `0.18` in 50 tax calculations, you store `GST_RATE = 0.18` once and reference it everywhere.
2. **Readability (No "Magic Numbers"):** `if retry_count > MAX_RETRIES:` is immediately understandable, whereas `if x > 3:` forces readers to guess what `3` means.
3. **State Tracking:** Programs track changing data—like bank balances, loop counters, or game scores—by rebinding variables over time.

---

## 3. Syntax

```python
from typing import Final

# 1. Standard Variable (snake_case per PEP 8)
user_age = 21
account_balance = 4500.75

# 2. Multiple Assignment (Tuple Unpacking)
x, y, z = 10, 20, 30

# 3. Chained Assignment (for immutable values)
a = b = c = 0

# 4. Constant Convention (UPPER_SNAKE_CASE + typing.Final)
MAX_CONNECTIONS: Final[int] = 100
```

### Valid Variable Naming Rules in Python:
1. Must start with a letter (`a-z`, `A-Z`) or an underscore (`_`).
2. Cannot start with a digit (`1st_place = 10` is a `SyntaxError`).
3. Can only contain alphanumeric characters and underscores (`a-z`, `A-Z`, `0-9`, `_`).
4. Case-sensitive (`score`, `Score`, and `SCORE` are three different variables).
5. Cannot be a reserved Python keyword (`if`, `for`, `class`, `def`, `return`, `True`, `None`, etc.).

---

## 4. Explanation (How Variables Work in Memory)

When you execute `score = 100`:
1. Python creates an `int` object with value `100` in heap memory.
2. Python creates the name `score` in the current namespace and points it to that `int` object.
3. If you later write `score = 105`, Python creates a **new** `int` object `105` and moves the `score` label to point to `105`.

```
Step 1: score = 100
  [ score ] --------> ( int: 100 )

Step 2: score = 105
  [ score ] --------> ( int: 105 )
                      ( int: 100 )  <-- Garbage collected if no other reference exists
```

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_variable_assignment_and_rebinding.py`](example_01_variable_assignment_and_rebinding.py)
- [`example_02_multiple_assignment_and_swapping.py`](example_02_multiple_assignment_and_swapping.py)
- [`example_03_constants_and_memory_references.py`](example_03_constants_and_memory_references.py)

### Example 1: Variable Assignment, Dynamic Typing, and Rebinding (`example_01_variable_assignment_and_rebinding.py`)

```python
def main() -> None:
    student_name = "Divya Prakash"
    completed_topics = 2
    completion_rate = 16.67
    is_active_learner = True

    print("=== Initial Variable Bindings ===")
    print(f"Student Name      : {student_name} (type: {type(student_name).__name__})")
    print(f"Completed Topics  : {completed_topics} (type: {type(completed_topics).__name__})")
    print(f"Completion Rate   : {completion_rate}% (type: {type(completion_rate).__name__})")
    print(f"Active Learner    : {is_active_learner} (type: {type(is_active_learner).__name__})")

    completed_topics = completed_topics + 1
    print(f"\nAfter completing Topic 03, completed_topics = {completed_topics}")

    status_indicator: int | str = 200
    print(f"Status Indicator (as int) : {status_indicator} ({type(status_indicator).__name__})")
    status_indicator = "OK - All Checks Passed"
    print(f"Status Indicator (as str) : {status_indicator} ({type(status_indicator).__name__})")


if __name__ == "__main__":
    main()
```

### Example 2: Multiple Assignment, Chained Assignment, and Swapping (`example_02_multiple_assignment_and_swapping.py`)

```python
def main() -> None:
    latitude, longitude, city = 28.6139, 77.2090, "New Delhi"
    print("=== Multiple Assignment ===")
    print(f"City: {city} | Coordinates: ({latitude}, {longitude})")

    wins = losses = draws = 0
    wins += 3
    draws += 1
    print("\n=== Chained Initialization ===")
    print(f"Match Record -> Wins: {wins}, Draws: {draws}, Losses: {losses}")

    primary_server = "srv-mumbai-01"
    backup_server = "srv-bangalore-02"
    print("\n=== Variable Swapping (Failover Simulation) ===")
    print(f"Before Failover -> Primary: {primary_server} | Backup: {backup_server}")

    primary_server, backup_server = backup_server, primary_server
    print(f"After Failover  -> Primary: {primary_server} | Backup: {backup_server}")


if __name__ == "__main__":
    main()
```

### Example 3: Constants (`UPPER_SNAKE_CASE` & `typing.Final`) and Object Identity (`example_03_constants_and_memory_references.py`)

```python
from typing import Final

SPEED_OF_LIGHT_M_S: Final[int] = 299_792_458
GST_RATE: Final[float] = 0.18
DEFAULT_CURRENCY: Final[str] = "INR"


def calculate_invoice_total(base_amount: float) -> float:
    """Calculate total invoice amount using the module-level GST_RATE constant."""
    tax_amount = base_amount * GST_RATE
    return round(base_amount + tax_amount, 2)


def main() -> None:
    course_price = 1500.00
    final_price = calculate_invoice_total(course_price)

    print("=== Constants in Action ===")
    print(f"Speed of Light : {SPEED_OF_LIGHT_M_S:,} m/s")
    print(f"Base Price     : {DEFAULT_CURRENCY} {course_price:.2f}")
    print(f"GST Rate       : {GST_RATE * 100:.0f}%")
    print(f"Final Invoice  : {DEFAULT_CURRENCY} {final_price:.2f}")

    a = 100
    b = a
    print("\n=== Object Reference Verification ===")
    print(f"a == b                 : {a == b}")
    print(f"a is b (same memory)   : {a is b}")
    b = 200
    print(f"After rebinding b=200  : a={a}, b={b}, (a is b)={a is b}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== Initial Variable Bindings ===
Student Name      : Divya Prakash (type: str)
Completed Topics  : 2 (type: int)
Completion Rate   : 16.67% (type: float)
Active Learner    : True (type: bool)

After completing Topic 03, completed_topics = 3
Status Indicator (as int) : 200 (int)
Status Indicator (as str) : OK - All Checks Passed (str)
```

### Output for Example 2:
```text
=== Multiple Assignment ===
City: New Delhi | Coordinates: (28.6139, 77.209)

=== Chained Initialization ===
Match Record -> Wins: 3, Draws: 1, Losses: 0

=== Variable Swapping (Failover Simulation) ===
Before Failover -> Primary: srv-mumbai-01 | Backup: srv-bangalore-02
After Failover  -> Primary: srv-bangalore-02 | Backup: srv-mumbai-01
```

### Output for Example 3:
```text
=== Constants in Action ===
Speed of Light : 299,792,458 m/s
Base Price     : INR 1500.00
GST Rate       : 18%
Final Invoice  : INR 1770.00

=== Object Reference Verification ===
a == b                 : True
a is b (same memory)   : True
After rebinding b=200  : a=100, b=200, (a is b)=False
```

---

## 7. Code Explanation

- **`primary_server, backup_server = backup_server, primary_server`** — Python evaluates the right-hand side first as a temporary tuple `(backup_server, primary_server)` and then unpacks those two references into the left-hand variables in a single step.
- **`299_792_458`** — Python allows underscores `_` as visual digit separators in numeric literals (PEP 515) to make large numbers easy to read.
- **`Final[float]`** — Imported from `typing`, `Final` tells static type checkers (like Mypy or Pylance) to flag an error if any code tries to reassign the constant.

---

## 8. Common Mistakes

1. **Shadowing Built-in Functions (`list`, `str`, `sum`, `max`, `id`):**
   ```python
   # WRONG: Overwrites the built-in sum() function!
   sum = 10 + 20
   # Later in the same file:
   total = sum([1, 2, 3])  # Raises TypeError: 'int' object is not callable
   ```
   Always use descriptive names like `total_sum` or `items_list`.

2. **Chained Assignment with Mutable Objects (`a = b = []`):**
   ```python
   # WRONG: Both a and b point to the exact same list in memory!
   a = b = []
   a.append(1)
   print(b)  # Outputs [1]!
   ```
   Only use chained assignment (`x = y = 0`) with **immutable** types (`int`, `float`, `str`, `bool`, `None`).

3. **Unpacking Mismatch (`ValueError`):**
   Writing `x, y = 1, 2, 3` raises `ValueError: too many values to unpack (expected 2)`. The number of variables on the left must match the number of values on the right.

---

## 9. Practice Questions

1. **Easy:** Create three variables (`item_name`, `quantity`, `unit_price`) on a single line using multiple assignment, and calculate the total cost.
2. **Medium:** Given three variables `a = 10`, `b = 20`, `c = 30`, rotate their values in a single line of Python so that `a` becomes `20`, `b` becomes `30`, and `c` becomes `10`.
3. **Hard:** Define a constant `EARTH_GRAVITY: Final[float] = 9.80665` and write a function that computes the weight (`mass * gravity`) and potential energy (`mass * gravity * height`) of an object, returning both values unpacked into two separate variables.

---

## 10. Interview Questions

### Q1: Does Python have true hardware-enforced constants like `const` in C++ or `final` in Java?
**Answer:** At runtime, Python does not enforce constants at the interpreter level. Instead, Python relies on the **PEP 8 naming convention (`UPPER_SNAKE_CASE`)** and static type-checker enforcement via **`typing.Final`** (or read-only `@property` attributes / `Enum` classes when runtime protection is needed).

### Q2: How does `a, b = b, a` work under the hood without a temporary variable?
**Answer:** Python evaluates the right-hand side `b, a` first, pushing both object references onto the evaluation stack, and then executes the `SWAP` bytecode instruction to bind them to `a` and `b` in reversed order.

### Q3: What happens to the old value in memory when a variable is reassigned?
**Answer:** Python uses **Reference Counting** (plus a cyclic Garbage Collector). Each object tracks how many variables point to it. When an object's reference count drops to `0`, Python automatically reclaims its memory.
