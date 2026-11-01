# Topic 08: Conditional Statements (`if`, `elif`, `else`)

---

## 1. Introduction

**Conditional Statements** allow a program to make decisions and execute different blocks of code depending on whether a condition evaluates to `True` or `False`.

Without conditionals, a script would execute every single line in a fixed straight line from top to bottom. With `if`, `elif` (short for *else if*), `else`, ternary expressions, and `match-case`, your program can adapt dynamically to user inputs, edge cases, and business rules.

---

## 2. Why is it used?

Conditional logic is the backbone of software decision-making:
1. **Access Control & Security:** Checking if a user is authenticated and authorized before returning sensitive data.
2. **Pricing, Tax & Grading Slabs:** Applying tiered tax brackets, shipping discounts, or university grades (`if`, `elif`, `else`).
3. **Algorithm Base Cases & Branching:** Binary search (`if arr[mid] == target:` / `elif arr[mid] < target:` / `else:`) and recursion base cases (`if n <= 1: return n`) rely entirely on conditionals.

---

## 3. Syntax

```python
# 1. Standard if / elif / else chain
if score >= 90:
    grade = "A+"
elif score >= 75:
    grade = "A"
else:
    grade = "B"

# 2. Ternary Conditional Expression (single-line value selection)
status = "Adult" if age >= 18 else "Minor"

# 3. Structural Pattern Matching (Python 3.10+)
match command:
    case "start" | "run":
        print("Starting service...")
    case "stop":
        print("Stopping service...")
    case _:
        print("Unknown command")
```

---

## 4. Explanation (Step-by-Step Execution Flow)

1. **Top-to-Bottom Mutual Exclusion (`if` -> `elif` -> `else`):**
   - Python evaluates the `if` condition first. If it is truthy, Python runs its indented block and **skips the entire rest of the `elif`/`else` chain**.
   - If the `if` condition is falsy, Python checks each `elif` condition in order until one evaluates to `True`.
   - If none of the `if` or `elif` conditions match, the optional `else` block executes as a catch-all fallback.
2. **Multiple Independent `if` Statements vs `elif`:**
   - Using `if ... elif ...` tests **mutually exclusive** branches (at most one branch executes).
   - Writing two separate `if` statements (`if cond1:` followed by `if cond2:`) tests **both** conditions independently.
3. **Guard Clauses Over Deep Nesting:**
   Instead of nesting `if` inside `if` four levels deep ("arrow anti-pattern"), return early when preconditions fail. This keeps the main "happy path" unindented and clean.

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_if_elif_else_grading_system.py`](example_01_if_elif_else_grading_system.py)
- [`example_02_guard_clauses_and_loan_eligibility.py`](example_02_guard_clauses_and_loan_eligibility.py)
- [`example_03_ternary_and_structural_match_case.py`](example_03_ternary_and_structural_match_case.py)

### Example 1: Multi-Way Branching — University Grading System (`example_01_if_elif_else_grading_system.py`)

```python
def evaluate_student_performance(marks: int) -> tuple[str, str]:
    """Return (grade, scholarship_status) for a given score out of 100."""
    if not (0 <= marks <= 100):
        return ("INVALID", "Score must be between 0 and 100")

    if marks >= 90:
        return ("O (Outstanding)", "100% Tuition Waiver")
    elif marks >= 80:
        return ("A+ (Excellent)", "50% Tuition Waiver")
    elif marks >= 70:
        return ("A (Very Good)", "25% Book Grant")
    elif marks >= 50:
        return ("B (Pass)", "Standard Enrollment")
    else:
        return ("F (Reappear)", "Mandatory Remedial Coaching")


def main() -> None:
    test_scores = [94, 83, 72, 58, 35, 105]
    print("=== University Grading & Scholarship Evaluator ===")
    for score in test_scores:
        grade, remark = evaluate_student_performance(score)
        print(f"Marks: {score:>3} -> Grade: {grade:<17} | Benefit: {remark}")


if __name__ == "__main__":
    main()
```

### Example 2: Clean Guard Clauses for Placement Eligibility (`example_02_guard_clauses_and_loan_eligibility.py`)

```python
def check_placement_drive_eligibility(
    cgpa: float,
    active_backlogs: int,
    attendance_pct: float,
    graduation_year: int,
) -> str:
    """Validate whether a candidate can sit for the campus placement drive."""
    if graduation_year != 2027:
        return "ineligible: Only Class of 2027 candidates are eligible."
    if active_backlogs > 0:
        return f"ineligible: {active_backlogs} active backlog(s) must be cleared first."
    if cgpa < 7.0:
        return f"ineligible: CGPA {cgpa:.2f} is below the 7.00 cutoff."
    if attendance_pct < 75.0:
        return f"ineligible: Attendance {attendance_pct:.1f}% is below 75.0%."

    if cgpa >= 8.5:
        return "ELIGIBLE: Super-Dream & Dream Companies"
    return "ELIGIBLE: Dream & Core Companies"


def main() -> None:
    candidates = [
        ("Divya", 8.9, 0, 91.0, 2027),
        ("Rohan", 7.6, 0, 82.5, 2027),
        ("Sneha", 8.2, 1, 88.0, 2027),
        ("Kabir", 6.5, 0, 80.0, 2027),
    ]

    print("=== Campus Placement Eligibility Audit ===")
    for name, cgpa, backlogs, attendance, batch in candidates:
        verdict = check_placement_drive_eligibility(cgpa, backlogs, attendance, batch)
        print(f"{name:<6} (CGPA={cgpa}, Backlogs={backlogs}) -> {verdict}")


if __name__ == "__main__":
    main()
```

### Example 3: Ternary Conditional Expression and `match-case` (`example_03_ternary_and_structural_match_case.py`)

```python
def describe_http_response(status_code: int) -> str:
    """Classify an HTTP status code using Python 3.10+ match-case."""
    match status_code:
        case 200 | 201:
            return "Success: Request completed"
        case 301 | 302:
            return "Redirection: Resource moved"
        case 400:
            return "Client Error: Bad request syntax"
        case 401 | 403:
            return "Security Error: Unauthorized or Forbidden"
        case 404:
            return "Client Error: Resource not found"
        case code if 500 <= code < 600:
            return f"Server Error ({code}): Internal service failure"
        case _:
            return f"Unknown HTTP status code: {status_code}"


def main() -> None:
    print("=== 1. Ternary Conditional Expression ===")
    for cart_total in [350, 750]:
        shipping_fee = 0 if cart_total >= 500 else 49
        print(f"Cart: Rs.{cart_total} -> Shipping Fee: Rs.{shipping_fee}")

    print("\n=== 2. Structural Pattern Matching (match-case) ===")
    for code in [200, 301, 403, 404, 503, 999]:
        print(f"HTTP {code} -> {describe_http_response(code)}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== University Grading & Scholarship Evaluator ===
Marks:  94 -> Grade: O (Outstanding)   | Benefit: 100% Tuition Waiver
Marks:  83 -> Grade: A+ (Excellent)    | Benefit: 50% Tuition Waiver
Marks:  72 -> Grade: A (Very Good)     | Benefit: 25% Book Grant
Marks:  58 -> Grade: B (Pass)          | Benefit: Standard Enrollment
Marks:  35 -> Grade: F (Reappear)      | Benefit: Mandatory Remedial Coaching
Marks: 105 -> Grade: INVALID           | Benefit: Score must be between 0 and 100
```

### Output for Example 2:
```text
=== Campus Placement Eligibility Audit ===
Divya  (CGPA=8.9, Backlogs=0) -> ELIGIBLE: Super-Dream & Dream Companies
Rohan  (CGPA=7.6, Backlogs=0) -> ELIGIBLE: Dream & Core Companies
Sneha  (CGPA=8.2, Backlogs=1) -> ineligible: 1 active backlog(s) must be cleared first.
Kabir  (CGPA=6.5, Backlogs=0) -> ineligible: CGPA 6.50 is below the 7.00 cutoff.
```

### Output for Example 3:
```text
=== 1. Ternary Conditional Expression ===
Cart: Rs.350 -> Shipping Fee: Rs.49
Cart: Rs.750 -> Shipping Fee: Rs.0

=== 2. Structural Pattern Matching (match-case) ===
HTTP 200 -> Success: Request completed
HTTP 301 -> Redirection: Resource moved
HTTP 403 -> Security Error: Unauthorized or Forbidden
HTTP 404 -> Client Error: Resource not found
HTTP 503 -> Server Error (503): Internal service failure
HTTP 999 -> Unknown HTTP status code: 999
```

---

## 7. Code Explanation

- **Ordering `if` / `elif` Thresholds:** In `evaluate_student_performance(marks)`, we check `marks >= 90` **before** `marks >= 80`. When `marks >= 80` is reached, we already know `marks < 90` because the `marks >= 90` branch did not trigger.
- **`case 200 | 201:`** — Inside `match-case`, the pipe symbol `|` acts as an OR pattern, matching either `200` or `201`.
- **`case code if 500 <= code < 600:`** — Demonstrates a **pattern guard** (`if ...`) inside `match-case` that binds the matched value to `code` and checks a range condition.
- **`case _:`** — The wildcard pattern `_` acts as the default catch-all branch (like `default:` in C/Java `switch` statements).

---

## 8. Common Mistakes

1. **Wrong Threshold Order in `if`/`elif` Ladders:**
   ```python
   # WRONG: Every score >= 50 matches the very first branch!
   if marks >= 50:
       grade = "B"
   elif marks >= 90:  # Dead code! Never reached!
       grade = "O"
   ```
   Always order range checks from **most restrictive to least restrictive** (descending for `>=`, ascending for `<=`).

2. **Classic Boolean Trap (`if role == "admin" or "editor":`):**
   ```python
   # WRONG: "editor" is a non-empty string, so it is ALWAYS truthy!
   if role == "admin" or "editor":  # Always evaluates to True!
   # CORRECT:
   if role in {"admin", "editor"}:
   ```

3. **Using `=` Instead of `==` Inside an `if` Condition:**
   Writing `if x = 5:` raises a `SyntaxError` in Python (which deliberately protects you from accidental assignment bugs common in C/C++).

---

## 9. Practice Questions

1. **Easy:** Write a function `classify_triangle(a: int, b: int, c: int) -> str` that first checks if three side lengths can form a valid triangle (`a + b > c`, `a + c > b`, and `b + c > a`), and then classifies it as `"Equilateral"`, `"Isosceles"`, or `"Scalene"`.
2. **Medium:** Write a progressive electricity bill calculator:
   - First `100` units: `Rs. 0 / unit` (Free)
   - Next `100` units (`101–200`): `Rs. 4.50 / unit`
   - Next `200` units (`201–400`): `Rs. 6.00 / unit`
   - Above `400` units: `Rs. 8.00 / unit`
3. **Hard:** Use Python 3.10+ Structural Pattern Matching (`match point:`) to classify a 2D coordinate tuple `(x, y)` into `"Origin"`, `"On X-Axis (x=...)"`, `"On Y-Axis (y=...)"`, or `"Quadrant I / II / III / IV"`.

---

## 10. Interview Questions

### Q1: How does Python's `match-case` (PEP 634) differ from a traditional C/Java `switch-case`?
**Answer:** Traditional `switch-case` only matches primitive constants (like integers or enums) and suffers from accidental fall-through unless `break` is written. Python's **Structural Pattern Matching** (`match-case`) never falls through automatically and can match and unpack **complex data structures**—such as tuples `(x, y)`, lists `[first, *rest]`, dictionaries `{"type": "click", "x": x}`, and class instances—while supporting `if` guards.

### Q2: When should you replace a long `if-elif-else` chain with a dictionary dispatch table?
**Answer:** When every branch compares the same variable for exact equality (`==`) against known constant keys, replacing a 15-branch `if-elif` chain (`O(k)` linear checks) with a dictionary lookup `handlers.get(action, default_handler)()` reduces lookup time to **`O(1)`** and makes the code cleaner and easier to extend.

### Q3: Why is `if items:` preferred over `if len(items) > 0:` in PEP 8?
**Answer:** PEP 8 recommends leveraging Python's built-in truthiness (`__bool__` / `__len__`) for sequences (`list`, `tuple`, `str`, `dict`, `set`). Empty containers are falsy and non-empty containers are truthy, making `if items:` both faster (avoids a global `len()` lookup) and more Pythonic. (Note: For `int`/`float` variables where `0` is a valid number, explicitly write `if count is not None:`).
