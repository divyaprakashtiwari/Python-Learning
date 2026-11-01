# Topic 07: Operators

---

## 1. Introduction

**Operators** are special symbols or keywords that perform computations, comparisons, or logical checks on one or more values (called **operands**). For example, in `price * quantity`, `*` is the multiplication operator and `price` and `quantity` are its operands.

Python organizes operators into 7 distinct families:
1. **Arithmetic Operators** (`+`, `-`, `*`, `/`, `//`, `%`, `**`)
2. **Assignment Operators** (`=`, `+=`, `-=`, `*=`, `//=`, `:=`)
3. **Comparison (Relational) Operators** (`==`, `!=`, `<`, `>`, `<=`, `>=`)
4. **Logical Operators** (`and`, `or`, `not`)
5. **Bitwise Operators** (`&`, `|`, `^`, `~`, `<<`, `>>`)
6. **Identity Operators** (`is`, `is not`)
7. **Membership Operators** (`in`, `not in`)

---

## 2. Why is it used?

Every algorithm in software development and DSA relies on operators:
- **Binary Search & Array Indexing** depend on floor division (`mid = (low + high) // 2`).
- **Circular Queues & Hashing** depend on the modulo operator (`next_idx = (idx + 1) % capacity`).
- **Guard Conditions** depend on short-circuit logical operators (`idx < len(arr) and arr[idx] == target`).
- **Fast Subset & Flag Checks** depend on bitwise operators (`&`, `|`, `^`, `<<`).

---

## 3. Syntax

```python
# 1. Arithmetic
quotient = 17 // 5       # 3 (Floor division)
remainder = 17 % 5       # 2 (Modulo)
power = 2 ** 8           # 256 (Exponentiation)

# 2. Chained Comparison & Logical
is_valid_score = 0 <= score <= 100
can_proceed = is_logged_in and not is_suspended

# 3. Identity & Membership
is_missing = result is None
found = "python" in {"python", "java", "c++"}

# 4. Walrus Assignment Expression (Python 3.8+)
if (length := len(items)) > 0:
    print(length)
```

---

## 4. Explanation (Key Operator Mechanics & Precedence)

1. **`/` vs `//`:**
   - `/` (**True Division**) always returns a `float` (`10 / 2 == 5.0`).
   - `//` (**Floor Division**) divides and rounds **down** toward negative infinity (`17 // 5 == 3`, `-17 // 5 == -4`).
2. **Short-Circuit Evaluation (`and` / `or`):**
   - In `A and B`, if `A` is falsy, Python immediately returns `A` **without evaluating `B`**.
   - In `A or B`, if `A` is truthy, Python immediately returns `A` **without evaluating `B`**.
3. **Operator Precedence (Highest to Lowest):**
   1. `()` (Parentheses)
   2. `**` (Exponentiation — right-associative: `2 ** 3 ** 2 == 2 ** 9 == 512`)
   3. `+x`, `-x`, `~x` (Unary signs and bitwise NOT)
   4. `*`, `/`, `//`, `%` (Multiplication, Division, Modulo)
   5. `+`, `-` (Addition, Subtraction)
   6. `<<`, `>>` (Bitwise shifts)
   7. `&` -> `^` -> `|` (Bitwise AND, XOR, OR)
   8. `==`, `!=`, `<`, `<=`, `>`, `>=`, `is`, `in` (Comparisons, Identity, Membership)
   9. `not` -> `and` -> `or` (Logical NOT, AND, OR)

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_arithmetic_and_division_operators.py`](example_01_arithmetic_and_division_operators.py)
- [`example_02_comparison_and_logical_short_circuit.py`](example_02_comparison_and_logical_short_circuit.py)
- [`example_03_bitwise_identity_and_membership.py`](example_03_bitwise_identity_and_membership.py)

### Example 1: Arithmetic Operators (`/`, `//`, `%`, `**`) and Time Conversion (`example_01_arithmetic_and_division_operators.py`)

```python
def format_duration(total_seconds: int) -> str:
    """Convert total seconds into HH:MM:SS using floor division (//) and modulo (%)."""
    hours = total_seconds // 3600
    remaining_after_hours = total_seconds % 3600
    minutes = remaining_after_hours // 60
    seconds = remaining_after_hours % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def main() -> None:
    a, b = 17, 5
    print("=== 1. Core Arithmetic Operators ===")
    print(f"{a} + {b}  = {a + b}   (Addition)")
    print(f"{a} - {b}  = {a - b}   (Subtraction)")
    print(f"{a} * {b}  = {a * b}   (Multiplication)")
    print(f"{a} / {b}  = {a / b}  (True Division -> always float)")
    print(f"{a} // {b} = {a // b}    (Floor Division -> quotient)")
    print(f"{a} % {b}  = {a % b}    (Modulo -> remainder)")
    print(f"2 ** 10 = {2 ** 10} (Exponentiation)")

    print("\n=== 2. Negative Floor Division & Modulo Invariant ===")
    neg_a = -17
    print(f"{neg_a} // {b} = {neg_a // b} (rounds down toward -infinity)")
    print(f"{neg_a} % {b}  = {neg_a % b}  (because (-4 * 5) + 3 == -17)")

    print("\n=== 3. Real-World Seconds to HH:MM:SS Converter ===")
    for sec in [3661, 7384, 86399]:
        print(f"  {sec:>5} seconds -> {format_duration(sec)}")


if __name__ == "__main__":
    main()
```

### Example 2: Chained Comparisons and Logical Short-Circuit Evaluation (`example_02_comparison_and_logical_short_circuit.py`)

```python
def is_safe_ratio(numerator: int, denominator: int) -> bool:
    """Safely check if numerator / denominator >= 2 without ZeroDivisionError."""
    return denominator != 0 and (numerator / denominator) >= 2.0


def main() -> None:
    print("=== 1. Mathematical Chained Comparisons ===")
    for exam_score in [45, 78, 95]:
        is_distinction = 75 <= exam_score <= 100
        print(f"Score {exam_score}: 75 <= score <= 100 -> {is_distinction}")

    print("\n=== 2. Short-Circuit Evaluation Guard ===")
    print(f"is_safe_ratio(10, 2) : {is_safe_ratio(10, 2)}")
    print(f"is_safe_ratio(10, 0) : {is_safe_ratio(10, 0)} (No ZeroDivisionError!)")

    print("\n=== 3. Value Return Behavior of `or` and `and` ===")
    configured_host = ""
    effective_host = configured_host or "localhost"
    print(f"Fallback host via `or`: {effective_host!r}")


if __name__ == "__main__":
    main()
```

### Example 3: Bitwise, Identity (`is`), Membership (`in`), and Walrus (`:=`) Operators (`example_03_bitwise_identity_and_membership.py`)

```python
def main() -> None:
    READ = 0b100     # 4
    WRITE = 0b010    # 2
    EXEC = 0b001     # 1

    user_perms = READ | WRITE  # Grant Read and Write (0b110 = 6)
    print("=== 1. Bitwise Permission Flags ===")
    print(f"User Permissions Mask : {bin(user_perms)} ({user_perms})")
    print(f"Has READ permission?  : {bool(user_perms & READ)}")
    print(f"Has EXEC permission?  : {bool(user_perms & EXEC)}")

    user_perms ^= WRITE
    print(f"After toggling WRITE  : Has WRITE = {bool(user_perms & WRITE)}")

    print("\n=== 2. Identity (is) vs Equality (==) ===")
    list_a = [1, 2, 3]
    list_b = [1, 2, 3]
    print(f"list_a == list_b (same content) : {list_a == list_b}")
    print(f"list_a is list_b (same object)  : {list_a is list_b}")

    allowed_roles = {"admin", "instructor", "maintainer"}
    candidate_role = "instructor"
    print("\n=== 3. Membership & Walrus Operator (:=) ===")
    print(f"{candidate_role!r} in allowed_roles : {candidate_role in allowed_roles}")

    sample_text = "Python Operators Mastery"
    if (n := len(sample_text)) > 15:
        print(f"Sample text has length {n} (> 15 characters)")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== 1. Core Arithmetic Operators ===
17 + 5  = 22   (Addition)
17 - 5  = 12   (Subtraction)
17 * 5  = 85   (Multiplication)
17 / 5  = 3.4  (True Division -> always float)
17 // 5 = 3    (Floor Division -> quotient)
17 % 5  = 2    (Modulo -> remainder)
2 ** 10 = 1024 (Exponentiation)

=== 2. Negative Floor Division & Modulo Invariant ===
-17 // 5 = -4 (rounds down toward -infinity)
-17 % 5  = 3  (because (-4 * 5) + 3 == -17)

=== 3. Real-World Seconds to HH:MM:SS Converter ===
   3661 seconds -> 01:01:01
   7384 seconds -> 02:03:04
  86399 seconds -> 23:59:59
```

### Output for Example 2:
```text
=== 1. Mathematical Chained Comparisons ===
Score 45: 75 <= score <= 100 -> False
Score 78: 75 <= score <= 100 -> True
Score 95: 75 <= score <= 100 -> True

=== 2. Short-Circuit Evaluation Guard ===
is_safe_ratio(10, 2) : True
is_safe_ratio(10, 0) : False (No ZeroDivisionError!)

=== 3. Value Return Behavior of `or` and `and` ===
Fallback host via `or`: 'localhost'
```

### Output for Example 3:
```text
=== 1. Bitwise Permission Flags ===
User Permissions Mask : 0b110 (6)
Has READ permission?  : True
Has EXEC permission?  : False
After toggling WRITE  : Has WRITE = False

=== 2. Identity (is) vs Equality (==) ===
list_a == list_b (same content) : True
list_a is list_b (same object)  : False

=== 3. Membership & Walrus Operator (:=) ===
'instructor' in allowed_roles : True
Sample text has length 24 (> 15 characters)
```

---

## 7. Code Explanation

- **`-17 % 5 == 3`** — Unlike C/C++ (where `-17 % 5` is `-2`), Python's modulo result always takes the sign of the **divisor (`5`)**, which makes cyclic array indexing (`(i - 1) % n`) work seamlessly even for negative indices.
- **`75 <= exam_score <= 100`** — Python evaluates `exam_score` only once and checks `75 <= exam_score and exam_score <= 100`.
- **`if (n := len(sample_text)) > 15:`** — The Walrus operator (`:=`) assigns `len(sample_text)` to `n` and simultaneously returns `n` for the `> 15` comparison, avoiding calling `len()` twice.

---

## 8. Common Mistakes

1. **Using `^` for Exponentiation Instead of `**`:**
   In Python, `^` is **Bitwise XOR**, not exponentiation! `2 ^ 3` evaluates to `1` (`0b010 ^ 0b011 == 0b001`), whereas `2 ** 3` evaluates to `8`.
2. **Using `is` to Compare Strings or Integers:**
   Never write `if status is "active":` or `if count is 1000:`. Only use `is` / `is not` for singleton checks like `if value is None:`. Always use `==` for value equality.
3. **Confusing Bitwise `&` / `|` with Logical `and` / `or`:**
   Bitwise `&` has higher precedence than comparison operators (`x == 1 & y == 2` is parsed as `x == (1 & y) == 2`). Use `and` and `or` for boolean conditions.

---

## 9. Practice Questions

1. **Easy:** Write an ATM note dispenser function that takes an amount (e.g., `3850`) and uses `//` and `%` to calculate the minimum number of `500`, `200`, `100`, and `50` rupee notes required.
2. **Medium:** Write a function `is_leap_year(year: int) -> bool` in a single boolean expression using `%`, `and`, and `or` (`divisible by 400` OR (`divisible by 4` AND `not divisible by 100`)).
3. **Hard:** Without using `/`, `//`, or `*`, use bitwise shift operators (`<<` and `>>`) and `&` to check if an integer `n` is odd (`n & 1`), multiply `n` by `8` (`n << 3`), and divide `n` by `4` (`n >> 2`).

---

## 10. Interview Questions

### Q1: What does `"Hello" or "World"` evaluate to, and what does `"Hello" and "World"` evaluate to?
**Answer:**
- `"Hello" or "World"` returns `"Hello"` because `or` returns the **first truthy operand** (or the last operand if all are falsy).
- `"Hello" and "World"` returns `"World"` because `and` returns the **first falsy operand** (or the last operand if all are truthy).

### Q2: Why does `-3 ** 2` evaluate to `-9` instead of `9`?
**Answer:** Exponentiation `**` has higher operator precedence than unary negation `-`. Therefore, `-3 ** 2` is parsed as `-(3 ** 2) = -9`. To square `-3`, you must use parentheses: `(-3) ** 2 == 9`.

### Q3: Why is `x in my_set` (`O(1)`) drastically faster than `x in my_list` (`O(n)`)?
**Answer:** The `in` operator delegates to the container's `__contains__` method. For a `list`, Python scans elements sequentially from index `0` (`O(n)`). For a `set` or `dict`, Python hashes `x` and jumps directly to the hash bucket in `O(1)` average time.
