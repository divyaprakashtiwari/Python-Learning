# Phase 3 — Topic 03: Return Statements

## 1. Introduction

The **`return` statement** immediately ends a function's execution, pops its stack frame from the call stack, and sends an object back to the caller.

In Python:
- Every function returns a value. If a function has no `return` statement—or uses a bare `return` with no expression—it automatically returns the singleton object `None`.
- You can use multiple `return` statements at different branches of a function (such as **Early Return Guard Clauses**).
- You can return multiple values separated by commas (`return a, b, c`), which Python packs into a single `tuple` (or a `NamedTuple` for named attribute access).
- Because functions are first-class objects, a function can even create and `return` another function!

---

## 2. Why is it used?

- **Decoupling Computation from I/O:** Returning values instead of printing them allows the caller to decide whether to store the result in a database, pass it into another function, assert it in a unit test, or display it in a UI.
- **Flattening Control Flow (Guard Clauses):** Using early `return` statements for invalid inputs eliminates deeply nested `if/else` pyramids ("Arrow Anti-Pattern"), keeping the main logic unindented and easy to read.
- **Rich Multi-Value Outputs:** Returning `(is_valid, result, error_message)` or a `NamedTuple` lets a single function communicate both status and payload without mutating global variables.

---

## 3. Syntax

```python
# 1. Returning a single expression
def square(n: int) -> int:
    return n * n

# 2. Early return guard clause + implicit/explicit None
def process_item(item: str | None) -> None:
    if item is None:
        return  # Bare `return` immediately exits and returns `None`
    print(f"Processing: {item}")

# 3. Returning multiple values (packed into a tuple)
def min_and_max(nums: list[int]) -> tuple[int, int]:
    return min(nums), max(nums)

low, high = min_and_max([4, 9, 1, 7])
```

---

## 4. Explanation (Step-by-Step)

### Step 1: Immediate Exit & Dead Code
The moment Python executes a `return` statement, the function terminates. Any lines written directly below an unconditional `return` in the same block are **unreachable ("dead code")** and will never run.

### Step 2: Early Return Guard Clauses
Instead of wrapping an entire function inside 3 or 4 nested `if` blocks:
```python
# Guard Clauses check preconditions at the top and return early on failure
if age < 21:
    return "Rejected: Underage"
if credit_score < 700:
    return "Rejected: Low Credit Score"
return "Approved"
```
Each guard clause eliminates an invalid case immediately so the reader doesn't have to keep track of open `else` branches.

### Step 3: Returning Multiple Values (`tuple` vs `NamedTuple`)
When you write `return True, dividend // divisor, dividend % divisor`, Python does **not** return three separate objects on the C stack—it constructs a single `tuple` `(True, 5, 4)` and returns that object reference. At the call site, `ok, q, r = ...` unpacks the tuple into separate variables.
When returning 3 or more values, returning a `typing.NamedTuple` gives callers the best of both worlds: tuple unpacking (`lo, hi, avg, n = stats`) **and** self-documenting attribute access (`stats.mean`).

### Step 4: `return` Inside `try ... finally`
If a `try` block executes a `return` statement, Python evaluates the return expression, **runs the `finally` block first** (to guarantee cleanup such as closing files or database cursors), and then hands the return value back to the caller.

---

## 5. Minimum 3 Examples

### Example 1: Early Return Guard Clauses vs Deeply Nested Conditionals
File: `example_01_early_return_guard_clauses.py`

```python
def approve_loan_nested(age: int, credit_score: int, annual_income: float) -> str:
    """Deeply nested validation (harder to read and maintain)."""
    if age >= 21:
        if credit_score >= 700:
            if annual_income >= 300000.0:
                return "APPROVED: Eligible for Prime Rate Loan"
            else:
                return "REJECTED: Annual income below INR 3,00,000"
        else:
            return "REJECTED: Credit score below 700"
    else:
        return "REJECTED: Applicant must be at least 21 years old"


def approve_loan_guard_clauses(
    age: int,
    credit_score: int,
    annual_income: float,
) -> str:
    """Flat, readable validation using Early Return Guard Clauses."""
    if age < 21:
        return "REJECTED: Applicant must be at least 21 years old"
    if credit_score < 700:
        return "REJECTED: Credit score below 700"
    if annual_income < 300000.0:
        return "REJECTED: Annual income below INR 3,00,000"

    # Happy path is completely unindented at the bottom
    return "APPROVED: Eligible for Prime Rate Loan"


def log_audit_event(event: str) -> None:
    """Function with no explicit return statement returns `None`."""
    print(f"  [AUDIT LOG] {event}")


def main() -> None:
    print("=== 1. Comparing Nested vs Early Return Guard Clauses ===")
    test_applicants = [
        (19, 750, 500000.0),
        (28, 640, 500000.0),
        (28, 760, 220000.0),
        (30, 780, 850000.0),
    ]
    for age, score, income in test_applicants:
        res_nested = approve_loan_nested(age, score, income)
        res_guards = approve_loan_guard_clauses(age, score, income)
        assert res_nested == res_guards
        print(f"  Applicant (age={age}, score={score}, income={income:,.0f}) -> {res_guards}")

    print("\n=== 2. Implicit `None` Return When No `return` Is Reached ===")
    return_val = log_audit_event("Loan batch processing completed")
    print(f"  Return value of `log_audit_event` : {return_val!r} (type: {type(return_val).__name__})")


if __name__ == "__main__":
    main()
```

---

### Example 2: Returning Multiple Values (Tuple Packing, Unpacking & `NamedTuple`)
File: `example_02_returning_multiple_values.py`

```python
from typing import NamedTuple


class DescriptiveStats(NamedTuple):
    """Self-documenting container for summary statistics."""

    minimum: float
    maximum: float
    mean: float
    count: int


def divmod_with_status(dividend: int, divisor: int) -> tuple[bool, int, int]:
    """Return (is_valid, quotient, remainder) as a packed 3-tuple."""
    if divisor == 0:
        return False, 0, 0
    return True, dividend // divisor, dividend % divisor


def compute_stats(values: list[float]) -> DescriptiveStats:
    """Return multiple named statistics that support both indexing and `.attribute` access."""
    if not values:
        return DescriptiveStats(0.0, 0.0, 0.0, 0)
    return DescriptiveStats(
        minimum=min(values),
        maximum=max(values),
        mean=round(sum(values) / len(values), 2),
        count=len(values),
    )


def main() -> None:
    print("=== 1. Returning Multiple Values via Tuple Packing ===")
    raw_return = divmod_with_status(29, 5)
    print(f"  Raw return object : {raw_return} (type: {type(raw_return).__name__})")

    # Unpacking directly into 3 variables
    ok, quotient, remainder = divmod_with_status(29, 5)
    print(f"  Unpacked values   : ok={ok}, quotient={quotient}, remainder={remainder}")

    ok_zero, _, _ = divmod_with_status(29, 0)
    print(f"  Divide by zero    : ok={ok_zero}")

    print("\n=== 2. Returning `NamedTuple` for Readable Multi-Value Returns ===")
    latencies_ms = [12.4, 18.9, 9.2, 24.5, 15.0]
    stats = compute_stats(latencies_ms)
    print(f"  NamedTuple repr   : {stats}")
    print(f"  Attribute access  : min={stats.minimum}ms, max={stats.maximum}ms, mean={stats.mean}ms")

    # Still supports tuple unpacking!
    lo, hi, avg, n = stats
    print(f"  Tuple unpacking   : lo={lo}, hi={hi}, avg={avg}, n={n}")


if __name__ == "__main__":
    main()
```

---

### Example 3: Returning Functions (Factory Pattern) & Returning Inside `try/finally`
File: `example_03_returning_functions_and_finally.py`

```python
from typing import Callable


def make_multiplier(factor: int) -> Callable[[int], int]:
    """Return a newly created function that multiplies its input by `factor`."""

    def multiply(number: int) -> int:
        return number * factor

    return multiply


def query_with_cleanup(query: str) -> str:
    """Demonstrate that `finally` executes even when `try` hits a `return` statement."""
    execution_steps: list[str] = []
    try:
        execution_steps.append(f"1. Executing query: {query}")
        return " | ".join(execution_steps) + " -> [Returned from try]"
    finally:
        # Runs right before the function actually exits to the caller
        print("  [finally block] Closing database cursor cleanly before returning!")


def main() -> None:
    print("=== 1. Returning a Function (Function Factory) ===")
    double = make_multiplier(2)
    triple = make_multiplier(3)
    print(f"  `double` object : {double.__name__} | double(14) = {double(14)}")
    print(f"  `triple` object : {triple.__name__} | triple(14) = {triple(14)}")

    print("\n=== 2. `return` Inside `try ... finally` ===")
    result = query_with_cleanup("SELECT id FROM orders")
    print(f"  Caller received : {result}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_early_return_guard_clauses.py`)
```text
=== 1. Comparing Nested vs Early Return Guard Clauses ===
  Applicant (age=19, score=750, income=500,000) -> REJECTED: Applicant must be at least 21 years old
  Applicant (age=28, score=640, income=500,000) -> REJECTED: Credit score below 700
  Applicant (age=28, score=760, income=220,000) -> REJECTED: Annual income below INR 3,00,000
  Applicant (age=30, score=780, income=850,000) -> APPROVED: Eligible for Prime Rate Loan

=== 2. Implicit `None` Return When No `return` Is Reached ===
  [AUDIT LOG] Loan batch processing completed
  Return value of `log_audit_event` : None (type: NoneType)
```

### Output — Example 2 (`example_02_returning_multiple_values.py`)
```text
=== 1. Returning Multiple Values via Tuple Packing ===
  Raw return object : (True, 5, 4) (type: tuple)
  Unpacked values   : ok=True, quotient=5, remainder=4
  Divide by zero    : ok=False

=== 2. Returning `NamedTuple` for Readable Multi-Value Returns ===
  NamedTuple repr   : DescriptiveStats(minimum=9.2, maximum=24.5, mean=16.0, count=5)
  Attribute access  : min=9.2ms, max=24.5ms, mean=16.0ms
  Tuple unpacking   : lo=9.2, hi=24.5, avg=16.0, n=5
```

### Output — Example 3 (`example_03_returning_functions_and_finally.py`)
```text
=== 1. Returning a Function (Function Factory) ===
  `double` object : multiply | double(14) = 28
  `triple` object : multiply | triple(14) = 42

=== 2. `return` Inside `try ... finally` ===
  [finally block] Closing database cursor cleanly before returning!
  Caller received : 1. Executing query: SELECT id FROM orders -> [Returned from try]
```

---

## 7. Code Explanation

1. **Guard Clauses (`example_01`):** `approve_loan_guard_clauses` checks each failure condition at the top and returns early. Notice there is not a single `else:` keyword needed, because `return` already exits the function.
2. **Tuple Unpacking & Throwaway `_` (`example_02`):** In `ok_zero, _, _ = divmod_with_status(29, 0)`, `_` is the conventional Python variable name for unpacked values that the caller intentionally ignores.
3. **`NamedTuple` (`example_02`):** `DescriptiveStats` inherits from `tuple`, so it has zero per-instance dictionary overhead while allowing `stats.minimum` and `stats.mean` instead of cryptic `stats[0]` and `stats[2]`.
4. **`make_multiplier` (`example_03`):** Returns the inner function object `multiply` (without `()`). The returned function remembers `factor` from its enclosing scope.

---

## 8. Common Mistakes

1. **Putting `return` inside a `for` loop in the `else` branch of a search:**
   ```python
   # WRONG: Exits on the very first element whether it matches or not!
   def contains_even_wrong(nums: list[int]) -> bool:
       for n in nums:
           if n % 2 == 0:
               return True
           else:
               return False  # <-- BUG! Stops after checking index 0!

   # CORRECT: Only return False AFTER the entire loop finishes without finding a match
   def contains_even_right(nums: list[int]) -> bool:
       for n in nums:
           if n % 2 == 0:
               return True
       return False
   ```
2. **Returning inconsistent types across branches:**
   - Having one branch return a `list` (`return [1, 2]`) and another branch return `False` or `-1` forces every caller to write `isinstance()` checks. Prefer returning an empty list `[]` or `list[int] | None`.
3. **Putting a `return` statement inside a `finally` block:**
   - A `return` inside `finally` silently **overwrites** the `try` block's return value and **swallows any unhandled exceptions** raised in the `try` block! Never `return` from `finally`.

---

## 9. Practice Questions

1. **Easy — First Vowel Finder with Early Return:**
   Write a function `first_vowel_index(word: str) -> int` that loops through `word` and immediately returns the index of the first vowel (`a, e, i, o, u`, case-insensitive), or returns `-1` after the loop if no vowel exists.

2. **Medium — Password Strength Report (`NamedTuple` Return):**
   Define a `NamedTuple` called `PasswordReport(is_strong: bool, score: int, missing_rules: list[str])`. Write `evaluate_password(pwd: str) -> PasswordReport` that checks length $\ge 8$, contains a digit, and contains an uppercase letter, returning the structured report.

3. **Hard — Function Factory for Range Validators:**
   Write a higher-order function `make_range_validator(min_val: float, max_val: float)` that returns a function `validate(x: float) -> tuple[bool, str]` checking whether `min_val <= x <= max_val`.

---

## 10. Interview Questions

### Q1: What happens when a function in Python has `return a, b, c`? Does Python return three separate objects?
**Answer:**
No—a Python function always returns a **single object reference**. The comma syntax `a, b, c` constructs a single `tuple` object `(a, b, c)` and returns a reference to that tuple. At the call site, `x, y, z = func()` uses sequence unpacking to bind the elements of the returned tuple to `x`, `y`, and `z`.

### Q2: In what order do things happen if a `try` block executes `return get_value()` and there is a `finally` block?
**Answer:**
1. Python evaluates the return expression `get_value()` inside the `try` block and temporarily stores the resulting object reference on the internal evaluation stack.
2. Before exiting the function, Python executes the `finally` block.
3. Once `finally` completes (assuming `finally` does not raise an exception or execute its own `return`), Python returns the saved value from step 1 to the caller.

### Q3: Why is returning `[]` (an empty list) often preferred over returning `None` when a search/filter function finds no results?
**Answer:**
Returning an empty collection (`[]`) instead of `None` (known as the **Null Object Pattern** for collections) allows callers to iterate over or chain operations on the result (`for item in find_users():`) immediately without risking `TypeError: 'NoneType' object is not iterable`. `None` should be reserved for functions that look up a *single* item (`find_user_by_id(id) -> User | None`).
