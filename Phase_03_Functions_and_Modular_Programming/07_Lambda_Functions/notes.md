# Phase 3 — Topic 07: Lambda Functions

## 1. Introduction

A **`lambda` function** (also called an **anonymous function**) is a small, inline function defined using the `lambda` keyword instead of `def`.

Unlike `def`, which is a multi-line *statement* that binds a function to a name, a `lambda` is a **single expression** that evaluates to a function object on the fly and automatically returns the result of its body expression.

---

## 2. Why is it used?

- **Inline Callbacks (`key=` in `sorted`, `min`, `max`, `heapq`):** When sorting a list of dictionaries or tuples by a custom field (`sorted(users, key=lambda u: u["age"])`), defining a separate named `def` function just for a one-line key extractor clutters the module namespace.
- **Dispatch Tables:** Storing simple arithmetic or formatting rules directly inside a dictionary (`{"+": lambda a, b: a + b}`).
- **Functional Pipelines (`map`, `filter`, `reduce`) & GUI/Event Callbacks:** Passing short transformations inline where a callable is expected.

---

## 3. Syntax

```python
# General Syntax:
# lambda param1, param2, ... : single_expression

# 1. Zero parameters
get_default_port = lambda: 8080

# 2. Multiple parameters (automatically returns `x + y` without the `return` keyword)
add = lambda x, y: x + y

# 3. Inline usage as a sorting key (Idiomatic PEP 8 usage)
sorted_items = sorted(items, key=lambda item: (item["category"], -item["price"]))
```

---

## 4. Explanation (Step-by-Step)

### Step 1: `lambda` vs `def`
| Feature | `def` Statement | `lambda` Expression |
| :--- | :--- | :--- |
| **Syntax** | Multi-line block of statements | Single expression only |
| **`return` Keyword** | Explicit `return` required to return a value | Implicit—automatically returns the expression's value |
| **`__name__` Attribute** | Function's identifier (`'add_with_def'`) | Always `'<lambda>'` (harder to read in tracebacks) |
| **Statements Allowed?** | Loops, `try/except`, `if/elif/else`, assignments, docstrings | **No statements allowed** (only conditional expressions `a if cond else b`) |

### Step 2: Multi-Criteria Sorting with Tuple Keys
In Python, tuples are compared element-by-element from left to right. By returning a tuple from a `lambda` key:
```python
sorted(employees, key=lambda emp: (emp["dept"], -emp["salary"]))
```
Python first sorts employees alphabetically by `"dept"`, and whenever two employees share the same `"dept"`, it breaks ties using `-emp["salary"]` (highest salary first).

### Step 3: The Late-Binding Loop Closure Trap
When you create lambdas inside a loop or comprehension:
```python
buggy = [lambda x: x * i for i in range(4)]
```
The variable `i` inside `x * i` is **not** evaluated when the `lambda` is created; it is looked up when the `lambda` is **called** (after the loop has finished and `i == 3`). Thus every function in `buggy` multiplies by `3`!
- **The Fix:** Bind the current iteration's value to a default parameter (`lambda x, i=i: x * i`), because **default parameter values are evaluated at function creation time**.

---

## 5. Minimum 3 Examples

### Example 1: Anonymous `lambda` Syntax vs `def` Statements & Dispatch Tables
File: `example_01_lambda_syntax_vs_def.py`

```python
from typing import Callable


def add_with_def(a: float, b: float) -> float:
    """Standard named function defined with `def`."""
    return a + b


def main() -> None:
    print("=== 1. Comparing `def` vs `lambda` Function Objects ===")
    # Note: PEP 8 recommends `def` when binding a function to a variable name;
    # we bind `add_with_lambda` here purely to inspect its runtime attributes.
    add_with_lambda = lambda a, b: a + b  # noqa: E731

    print(f"  add_with_def(7, 5)    = {add_with_def(7, 5)} | __name__ = {add_with_def.__name__!r}")
    print(f"  add_with_lambda(7, 5) = {add_with_lambda(7, 5)} | __name__ = {add_with_lambda.__name__!r}")
    print(f"  Same runtime type?    : {type(add_with_def) is type(add_with_lambda)}")

    print("\n=== 2. Inline `lambda` Expressions in a Calculator Dispatch Table ===")
    operations: dict[str, Callable[[float, float], float]] = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: round(x / y, 4) if y != 0 else float("inf"),
        "**": lambda x, y: x**y,
    }
    for op_symbol in ("+", "-", "*", "/", "**"):
        result = operations[op_symbol](12.0, 3.0)
        print(f"  12.0 {op_symbol:<2} 3.0 = {result}")


if __name__ == "__main__":
    main()
```

---

### Example 2: Custom Sorting Keys (`sorted`, `min`, `max` with Multi-Criteria Tuples)
File: `example_02_custom_sorting_keys.py`

```python
def main() -> None:
    employees = [
        {"name": "Rohan", "dept": "Engineering", "salary": 145000, "tenure_yrs": 3},
        {"name": "Ananya", "dept": "Design", "salary": 115000, "tenure_yrs": 4},
        {"name": "Vikram", "dept": "Engineering", "salary": 175000, "tenure_yrs": 6},
        {"name": "Meera", "dept": "Design", "salary": 115000, "tenure_yrs": 2},
        {"name": "Kabir", "dept": "Engineering", "salary": 145000, "tenure_yrs": 5},
    ]

    print("=== 1. `min()` and `max()` with `key=lambda` ===")
    highest_paid = max(employees, key=lambda emp: emp["salary"])
    newest_hire = min(employees, key=lambda emp: emp["tenure_yrs"])
    print(f"  Highest Paid : {highest_paid['name']} (INR {highest_paid['salary']:,})")
    print(f"  Newest Hire  : {newest_hire['name']} ({newest_hire['tenure_yrs']} yrs)")

    print("\n=== 2. Multi-Criteria `sorted()` with Tuple Key ===")
    # Sort by:
    #   1. Department alphabetically (ascending)
    #   2. Salary descending (`-emp["salary"]`)
    #   3. Tenure descending (`-emp["tenure_yrs"]`)
    ranked = sorted(
        employees,
        key=lambda emp: (emp["dept"], -emp["salary"], -emp["tenure_yrs"]),
    )
    for rank, emp in enumerate(ranked, start=1):
        print(
            f"  #{rank} [{emp['dept']:<11}] {emp['name']:<7} | "
            f"Salary: INR {emp['salary']:,} | Tenure: {emp['tenure_yrs']}y"
        )


if __name__ == "__main__":
    main()
```

---

### Example 3: Functional Pipelines (`map`, `filter`) & The Late-Binding Loop Trap
File: `example_03_map_filter_and_late_binding_trap.py`

```python
def main() -> None:
    print("=== 1. `map()` and `filter()` with `lambda` ===")
    raw_prices = [120, 450, 80, 999, 310, 45]
    # Keep prices >= 100 and apply 18% GST
    premium_prices = list(filter(lambda p: p >= 100, raw_prices))
    prices_with_gst = list(map(lambda p: round(p * 1.18, 2), premium_prices))
    print(f"  Raw prices          : {raw_prices}")
    print(f"  Filtered (>= 100)   : {premium_prices}")
    print(f"  Mapped (+18% GST)   : {prices_with_gst}")

    print("\n=== 2. The Late-Binding Loop Closure Trap ===")
    # BUGGY: All 4 lambdas look up loop variable `i` AFTER the loop ends (`i == 3`)
    buggy_multipliers = [lambda x: x * i for i in range(4)]
    buggy_outputs = [fn(10) for fn in buggy_multipliers]
    print(f"  Buggy `[lambda x: x * i]` for x=10       -> {buggy_outputs} (all use i=3!)")

    # FIXED: Capture current `i` at each iteration as a default parameter `i=i`
    fixed_multipliers = [lambda x, i=i: x * i for i in range(4)]
    fixed_outputs = [fn(10) for fn in fixed_multipliers]
    print(f"  Fixed `[lambda x, i=i: x * i]` for x=10  -> {fixed_outputs} (0, 10, 20, 30!)")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_lambda_syntax_vs_def.py`)
```text
=== 1. Comparing `def` vs `lambda` Function Objects ===
  add_with_def(7, 5)    = 12 | __name__ = 'add_with_def'
  add_with_lambda(7, 5) = 12 | __name__ = '<lambda>'
  Same runtime type?    : True

=== 2. Inline `lambda` Expressions in a Calculator Dispatch Table ===
  12.0 +  3.0 = 15.0
  12.0 -  3.0 = 9.0
  12.0 *  3.0 = 36.0
  12.0 /  3.0 = 4.0
  12.0 ** 3.0 = 1728.0
```

### Output — Example 2 (`example_02_custom_sorting_keys.py`)
```text
=== 1. `min()` and `max()` with `key=lambda` ===
  Highest Paid : Vikram (INR 175,000)
  Newest Hire  : Meera (2 yrs)

=== 2. Multi-Criteria `sorted()` with Tuple Key ===
  #1 [Design     ] Ananya  | Salary: INR 115,000 | Tenure: 4y
  #2 [Design     ] Meera   | Salary: INR 115,000 | Tenure: 2y
  #3 [Engineering] Vikram  | Salary: INR 175,000 | Tenure: 6y
  #4 [Engineering] Kabir   | Salary: INR 145,000 | Tenure: 5y
  #5 [Engineering] Rohan   | Salary: INR 145,000 | Tenure: 3y
```

### Output — Example 3 (`example_03_map_filter_and_late_binding_trap.py`)
```text
=== 1. `map()` and `filter()` with `lambda` ===
  Raw prices          : [120, 450, 80, 999, 310, 45]
  Filtered (>= 100)   : [120, 450, 999, 310]
  Mapped (+18% GST)   : [141.6, 531.0, 1178.82, 365.8]

=== 2. The Late-Binding Loop Closure Trap ===
  Buggy `[lambda x: x * i]` for x=10       -> [30, 30, 30, 30] (all use i=3!)
  Fixed `[lambda x, i=i: x * i]` for x=10  -> [0, 10, 20, 30] (0, 10, 20, 30!)
```

---

## 7. Code Explanation

1. **Runtime Identity (`example_01`):** `type(add_with_def) is type(add_with_lambda)` is `True` (both are `<class 'function'>`). The only runtime difference is that `add_with_lambda.__name__` is the generic string `'<lambda>'`.
2. **Tie-Breaking Tuple Sort (`example_02`):** In `Engineering`, both Kabir and Rohan earn `145000`, so Python compares the third tuple element `-emp["tenure_yrs"]` (`-5 < -3`), placing Kabir (5y) ahead of Rohan (3y).
3. **Late-Binding Closure Fix (`example_03`):** Adding `i=i` in `lambda x, i=i: x * i` creates a local parameter `i` on each lambda whose default value is evaluated immediately during iteration `0, 1, 2, 3`.

---

## 8. Common Mistakes

1. **Assigning a `lambda` to a variable name (`f = lambda x: 2 * x`) instead of using `def`:**
   - PEP 8 explicitly warns against this (flake8 rule `E731`). `def f(x): return 2 * x` is just as short and gives `f` a real `__name__` for stack traces, debuggers, and docstrings.
2. **Writing `return` inside a `lambda`:**
   - `lambda x: return x * 2` is a `SyntaxError`. A `lambda` body is an expression whose value is returned automatically.
3. **Writing unreadable, deeply nested ternary expressions inside a `lambda`:**
   - If a `lambda` doesn't fit cleanly on a single line, extract it into a named `def` helper function with a clear name.

---

## 9. Practice Questions

1. **Easy — Sort Strings by Last Character:**
   Given `words = ["banana", "pie", "apple", "kiwi", "plum"]`, use `sorted()` with a `lambda` key to sort the words alphabetically by their **last character** (breaking ties by word length ascending).

2. **Medium — Product Inventory Sorter:**
   Given a list of product tuples `[("Mouse", 499, 12), ("Keyboard", 1499, 0), ("Monitor", 12999, 5), ("Cable", 199, 0)]` representing `(name, price, stock_qty)`, sort them using a `lambda` so that **in-stock items (`stock_qty > 0`) always appear before out-of-stock items**, and within each group items are ordered by `price` ascending.

3. **Hard — Event Handler Factory Without Late-Binding Bug:**
   Create a list of 5 button click handlers `handlers` for buttons `"BTN-1"` through `"BTN-5"` using a comprehension and `lambda` so that calling `handlers[k]()` returns `"Clicked BTN-{k+1}"` (not `"Clicked BTN-5"` for all of them).

---

## 10. Interview Questions

### Q1: Why can't a Python `lambda` contain statements like `if/else` blocks, `for` loops, or `try/except`?
**Answer:**
Guido van Rossum designed Python's grammar so that statements (which rely on indentation and newlines) cannot be nested inside expressions. Keeping `lambda` restricted to a single expression prevents developers from cramming multi-line control flow into unindented one-liners; whenever multi-statement logic is needed, a named `def` function is cleaner and easier to debug.

### Q2: What does `[fn(2) for fn in [lambda x: x + i for i in range(3)]]` evaluate to, and why?
**Answer:**
It evaluates to `[4, 4, 4]`, **not** `[2, 3, 4]`.
Inside the comprehension, `i` is a closure variable referencing the comprehension's loop variable. None of the three lambdas are called until *after* the comprehension loop finishes, at which point `i` has its final value `2`. Every lambda therefore computes `2 + 2 = 4`. Fixing it requires early binding via a default argument: `[lambda x, i=i: x + i for i in range(3)]`.

### Q3: When can `operator.itemgetter` or `operator.attrgetter` replace a `lambda` in `sorted()`?
**Answer:**
When a `lambda` simply extracts a dictionary key (`lambda d: d["salary"]`) or an object attribute (`lambda obj: obj.salary`), `operator.itemgetter("salary")` or `operator.attrgetter("salary")` runs in C without the Python frame call overhead of a `lambda`, making it slightly faster on large lists. However, `lambda` is required whenever you need arithmetic or custom expressions like `(d["dept"], -d["salary"])`.
