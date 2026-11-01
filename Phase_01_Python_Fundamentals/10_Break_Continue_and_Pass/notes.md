# Topic 10: `break`, `continue`, and `pass`

---

## 1. Introduction

While writing loops and conditional blocks, you often need fine-grained control over the flow of execution:
1. **`break`** — Immediately terminates the innermost enclosing `for` or `while` loop and jumps to the first statement after the loop.
2. **`continue`** — Skips the remaining lines in the **current iteration** of the loop and immediately moves to the next iteration.
3. **`pass`** — A null operation (no-op placeholder). When executed, nothing happens. It is used where Python syntax requires an indented block (such as an empty function, class, or `if` branch), but you don't want any code to run yet.

---

## 2. Why is it used?

1. **Performance Optimization (`break`):** If you are searching a list of 1,000,000 items and find the target at index `3`, `break` stops the loop immediately instead of wasting 999,996 unnecessary checks.
2. **Clean Loop Guard Clauses (`continue`):** Instead of wrapping the entire body of a loop inside deeply nested `if` statements, `continue` lets you skip blank lines, comments, or invalid records right at the top of the loop.
3. **Incremental Architecture (`pass`):** Lets you sketch out class hierarchies, custom exceptions (`class CustomError(Exception): pass`), and function signatures before implementing their bodies.

---

## 3. Syntax

```python
for item in collection:
    if should_ignore(item):
        continue        # Skip to next item

    if is_target(item):
        print("Found!")
        break           # Exit loop completely
else:
    # Optional loop-else: runs ONLY if the loop did NOT hit `break`
    print("Target was never found.")

# Syntactic placeholder
def upcoming_feature() -> None:
    pass
```

---

## 4. Explanation (Step-by-Step Control Flow)

```
Loop Iteration Starts
  │
  ├──> Hits `continue`? ──Yes──> Skip rest of body; jump to NEXT iteration
  │
  ├──> Hits `break`?    ──Yes──> Terminate loop immediately (skip `else:` block)
  │
  └──> Hits `pass`?     ──Yes──> Do nothing; continue executing the very next line
```

### Understanding Python's `for ... else` and `while ... else`:
Beginners are often surprised that `for` and `while` loops can have an `else:` clause!
- Think of `else:` on a loop as **`nobreak:`**.
- The `else:` block executes **if and only if** the loop finishes normally without encountering a `break` statement.

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_break_and_for_else_search.py`](example_01_break_and_for_else_search.py)
- [`example_02_continue_log_sanitizer.py`](example_02_continue_log_sanitizer.py)
- [`example_03_pass_placeholders_and_stubs.py`](example_03_pass_placeholders_and_stubs.py)

### Example 1: `break` for Early Termination and `for...else` (`example_01_break_and_for_else_search.py`)

```python
def find_transaction(transactions: list[dict], target_id: str) -> None:
    print(f"Searching for Transaction ID {target_id!r}...")
    for index, txn in enumerate(transactions):
        if txn["id"] == target_id:
            print(f"  [FOUND at index {index}] Amount: Rs.{txn['amount']} | Status: {txn['status']}")
            break
    else:
        print(f"  [NOT FOUND] Transaction {target_id!r} does not exist.")


def is_prime_with_for_else(n: int) -> bool:
    """Check primality using a for...else loop and break."""
    if n < 2:
        return False
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            break
    else:
        return True
    return False


def main() -> None:
    ledger = [
        {"id": "TXN-101", "amount": 500, "status": "SUCCESS"},
        {"id": "TXN-102", "amount": 1200, "status": "PENDING"},
        {"id": "TXN-103", "amount": 850, "status": "SUCCESS"},
    ]
    print("=== 1. Early Exit with break and for...else ===")
    find_transaction(ledger, "TXN-102")
    find_transaction(ledger, "TXN-999")

    print("\n=== 2. Prime Number Verification using for...else ===")
    for candidate in [2, 15, 29, 49, 97]:
        print(f"  is_prime({candidate:>2}) -> {is_prime_with_for_else(candidate)}")


if __name__ == "__main__":
    main()
```

### Example 2: Using `continue` to Sanitize Sensor Logs (`example_02_continue_log_sanitizer.py`)

```python
def process_sensor_readings(raw_lines: list[str]) -> list[float]:
    valid_celsius: list[float] = []

    for line_no, raw in enumerate(raw_lines, start=1):
        cleaned = raw.strip()

        if not cleaned or cleaned.startswith("#"):
            continue

        if cleaned == "ERR_SENSOR_TIMEOUT":
            print(f"  [Line {line_no}] Skipping sensor timeout warning.")
            continue

        reading = float(cleaned)
        valid_celsius.append(reading)
        print(f"  [Line {line_no}] Recorded valid temperature: {reading:.1f} C")

    return valid_celsius


def main() -> None:
    log_feed = [
        "# Weather Station Batch 01",
        "24.5",
        "",
        "ERR_SENSOR_TIMEOUT",
        "26.0",
        "# Mid-day calibration",
        "27.5",
    ]
    print("=== Sensor Data Pipeline (continue in action) ===")
    valid = process_sensor_readings(log_feed)
    print(f"\nValid Readings Collected ({len(valid)}): {valid}")
    print(f"Average Temperature: {sum(valid) / len(valid):.2f} C")


if __name__ == "__main__":
    main()
```

### Example 3: Using `pass` as a Syntactic Placeholder (`example_03_pass_placeholders_and_stubs.py`)

```python
class PaymentGatewayError(Exception):
    """Custom domain exception that needs no extra methods beyond Exception."""
    pass


class NotificationService:
    """Skeleton service interface designed before concrete implementation."""

    def send_email(self, recipient: str, subject: str) -> None:
        pass

    def send_sms(self, phone: str, message: str) -> None:
        pass


def main() -> None:
    print("=== 1. Instantiating Stub Class with `pass` ===")
    notifier = NotificationService()
    notifier.send_email("student@example.com", "Welcome to Python DSA")
    print("Stub method executed cleanly with no-op `pass` (returned None).")

    print("\n=== 2. Catching Custom Exception Defined with `pass` ===")
    try:
        raise PaymentGatewayError("Gateway timeout after 5000ms")
    except PaymentGatewayError as exc:
        print(f"Caught {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== 1. Early Exit with break and for...else ===
Searching for Transaction ID 'TXN-102'...
  [FOUND at index 1] Amount: Rs.1200 | Status: PENDING
Searching for Transaction ID 'TXN-999'...
  [NOT FOUND] Transaction 'TXN-999' does not exist.

=== 2. Prime Number Verification using for...else ===
  is_prime( 2) -> True
  is_prime(15) -> False
  is_prime(29) -> True
  is_prime(49) -> False
  is_prime(97) -> True
```

### Output for Example 2:
```text
=== Sensor Data Pipeline (continue in action) ===
  [Line 2] Recorded valid temperature: 24.5 C
  [Line 4] Skipping sensor timeout warning.
  [Line 5] Recorded valid temperature: 26.0 C
  [Line 7] Recorded valid temperature: 27.5 C

Valid Readings Collected (3): [24.5, 26.0, 27.5]
Average Temperature: 26.00 C
```

### Output for Example 3:
```text
=== 1. Instantiating Stub Class with `pass` ===
Stub method executed cleanly with no-op `pass` (returned None).

=== 2. Catching Custom Exception Defined with `pass` ===
Caught PaymentGatewayError: Gateway timeout after 5000ms
```

---

## 7. Code Explanation

- **`for divisor in range(2, int(n ** 0.5) + 1): ... else: return True`** — If any divisor divides `n` evenly, `break` jumps out of the loop and skips the `else` block, returning `False`. If no divisor is found up to `sqrt(n)`, the loop finishes naturally and the `else` block returns `True` without needing a separate `is_prime = True` boolean flag!
- **`if not cleaned or cleaned.startswith("#"): continue`** — Filters out noise at the top of the loop so the main parsing logic stays flat and readable.

---

## 8. Common Mistakes

1. **Confusing `pass` with `continue`:**
   ```python
   for x in [1, 2, 3]:
       if x == 2:
           pass       # Does NOTHING! print(x) below STILL executes for x == 2!
       print(x)
   ```
   `pass` does **not** skip the rest of the loop body—`continue` does!
2. **Putting `continue` Before Updating the Counter in a `while` Loop:**
   ```python
   # WRONG: Infinite loop when i == 2 because i += 1 is skipped!
   i = 0
   while i < 5:
       if i == 2:
           continue
       i += 1
   ```
   Always increment your `while` counter before `continue` (or use a `for` loop).
3. **Thinking `break` Exits All Outer Nested Loops:**
   `break` only exits the **innermost** loop in which it appears. To exit multiple nested loops at once, wrap the search in a function and use `return`.

---

## 9. Practice Questions

1. **Easy:** Write a loop from `1` to `30` that skips all multiples of `3` using `continue`, and stops completely if the number exceeds `22` using `break`.
2. **Medium:** Given a list of integers `nums` and a target sum `limit`, accumulate numbers into a running total, skipping negative numbers with `continue`, and `break` as soon as adding the next number would exceed `limit`.
3. **Hard:** Write a function `find_first_duplicate(nums: list[int]) -> int | None` that uses a `set` and a `for ... else` loop with `break` to print and return the first element that appears more than once, or prints `"All elements are unique"` in the `else` block.

---

## 10. Interview Questions

### Q1: When does the `else` block of a `for` or `while` loop execute in Python?
**Answer:** The `else` block of a loop executes **only when the loop terminates normally** (i.e., the `for` iterator is exhausted or the `while` condition becomes `False`). If the loop exits early via `break`, `return`, or an unhandled exception, the `else` block is skipped.

### Q2: Why can't you just use a `# comment` instead of `pass` in an empty function or class?
**Answer:** The Python parser completely strips `# comments` during tokenization before checking indentation grammar. An indented block containing only a comment appears completely empty to the parser and raises `IndentationError: expected an indented block`. `pass` (or a docstring / `...` Ellipsis literal) is an actual AST statement that satisfies the grammar.

### Q3: How do you break out of two nested `for` loops simultaneously in Python?
**Answer:** The cleanest Pythonic way is to extract the nested loops into a helper function and use `return (row, col)` as soon as the target is found. Alternatively, iterate over `itertools.product(rows, cols)` in a single flat loop and use a single `break`.
