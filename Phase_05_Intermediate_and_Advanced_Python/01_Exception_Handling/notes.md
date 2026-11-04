# Phase 5 — Topic 01: Exception Handling

## 1. Introduction

**Exception Handling** is Python's structured mechanism for detecting, responding to, and recovering from runtime errors without crashing the entire program. Instead of returning magic error codes (like `-1` or `None`) from every function and manually checking them after every call, Python raises an **Exception object** that unwinds the call stack until a matching `except` handler catches it.

Mastering Python's full `try / except / else / finally` lifecycle, custom domain exception hierarchies, exception chaining (`raise ... from err`), and Python 3.11+ `ExceptionGroup` / `except*` is essential for writing resilient production systems.

---

## 2. Why is it used?

1. **Graceful Degradation:** Network timeouts, missing configuration keys, malformed user JSON, or division by zero can be caught and converted into helpful error responses instead of terminating the process.
2. **Separation of Happy Path and Error Path:** Business logic stays clean inside `try:` and `else:`, while recovery logic is isolated inside specific `except` blocks.
3. **Guaranteed Resource Cleanup:** The `finally:` block (and context managers) executes regardless of whether the `try` block succeeded, raised an exception, or executed an early `return`.
4. **Rich Root-Cause Diagnostics:** Exception chaining (`raise HighLevelError(...) from low_level_err`) preserves the original traceback (`__cause__`) while presenting a clean domain-level abstraction to callers.

---

## 3. Syntax

```python
# 1. Full try / except / else / finally lifecycle
try:
    risky_result = perform_operation()
except (ValueError, KeyError) as err:
    handle_validation_error(err)
except Exception as err:
    log_unexpected_error(err)
    raise  # Re-raise the active exception preserving its traceback
else:
    # Runs ONLY if `try` succeeded with zero exceptions
    commit_result(risky_result)
finally:
    # Runs ALWAYS (even on return, break, continue, or unhandled exception)
    release_resources()


# 2. Custom Exception Hierarchy & Chaining
class DomainError(Exception):
    """Base exception for our application."""

class ConfigError(DomainError):
    pass

try:
    port = int(config["PORT"])
except KeyError as err:
    raise ConfigError("Missing PORT setting") from err


# 3. ExceptionGroup & except* (Python 3.11+)
try:
    raise ExceptionGroup("Batch errors", [ValueError("bad val"), TypeError("bad type")])
except* ValueError as val_group:
    print(val_group.exceptions)
except* TypeError as type_group:
    print(type_group.exceptions)
```

---

## 4. Explanation (Step-by-Step)

1. **`BaseException` vs `Exception` Hierarchy:**
   - `BaseException` is the root of all exceptions. Directly beneath it sit system-exit signals (`SystemExit`, `KeyboardInterrupt`, `GeneratorExit`) and `Exception`.
   - Application code should **never** use a bare `except:` or `except BaseException:` unless immediately re-raising, because doing so swallows `Ctrl+C` (`KeyboardInterrupt`) and `sys.exit()` (`SystemExit`). Always catch specific subclasses of `Exception`.
2. **Why `else:` Exists:**
   - Any code placed inside `try:` after the risky line might accidentally raise an exception of the same type that your `except:` block was meant to catch for the first line. Putting follow-up success code in `else:` narrows the `try` scope to the exact line that is expected to fail.
3. **Explicit Exception Chaining (`from err` vs `from None`):**
   - `raise CustomError("msg") from err` sets `__cause__ = err` and prints `"The above exception was the direct cause of the following exception:"`.
   - `raise CustomError("msg") from None` suppresses the lower-level traceback when the internal implementation detail would only confuse end users.
4. **EAFP vs LBYL:**
   - **LBYL (Look Before You Leap):** Check preconditions (`if key in d:`) before acting. Can suffer from Time-Of-Check to Time-Of-Use (TOCTOU) race conditions in concurrent or filesystem code.
   - **EAFP (Easier to Ask Forgiveness than Permission):** Attempt the operation directly inside `try:` and catch the specific exception (`KeyError`, `FileNotFoundError`). Idiomatic in Python.

---

## 5. Minimum 3 Examples

### Example 01: Complete `try / except / else / finally` Lifecycle
File: [`example_01_try_except_else_finally_lifecycle.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/01_Exception_Handling/example_01_try_except_else_finally_lifecycle.py)

```python
"""
Phase 5 - Topic 01: Exception Handling
Example 01: The Complete `try / except / else / finally` Execution Lifecycle

Demonstrates:
  - Catching specific exceptions (`ValueError`, `ZeroDivisionError`) instead of bare `except:`
  - Why code that should only run when `try` succeeds belongs in `else:` (not inside `try:`)
  - Why cleanup logic belongs in `finally:` (runs whether an exception occurred or not)
"""


def parse_and_divide(raw_numerator: str, raw_denominator: str) -> float | None:
    """Parse two strings as floats and return their quotient, tracing all 4 blocks."""
    print(f"  --- Input: ({raw_numerator!r}, {raw_denominator!r}) ---")
    try:
        numerator = float(raw_numerator)
        denominator = float(raw_denominator)
        quotient = numerator / denominator
    except ValueError as err:
        print(f"    [except ValueError] Invalid number format: {err}")
        return None
    except ZeroDivisionError:
        print("    [except ZeroDivisionError] Denominator cannot be zero!")
        return None
    else:
        # Runs ONLY if the `try` block completed with ZERO exceptions
        rounded = round(quotient, 4)
        print(f"    [else] Division succeeded cleanly -> {rounded}")
        return rounded
    finally:
        # Runs ALWAYS (even when `except` or `else` executes a `return` statement!)
        print("    [finally] Releasing parser resources")


def main() -> None:
    print("=== Tracing `try / except / else / finally` Across 3 Scenarios ===")
    parse_and_divide("45", "6")
    parse_and_divide("forty-five", "6")
    parse_and_divide("45", "0")


if __name__ == "__main__":
    main()
```

### Example 02: Custom Domain Exceptions & Exception Chaining (`raise ... from err`)
File: [`example_02_exception_chaining_and_custom_exceptions.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/01_Exception_Handling/example_02_exception_chaining_and_custom_exceptions.py)

```python
"""
Phase 5 - Topic 01: Exception Handling
Example 02: Custom Domain Exceptions & Exception Chaining (`raise ... from err`)

Demonstrates:
  - Defining a custom exception class with structured diagnostic attributes
  - Wrapping low-level exceptions (`KeyError`) into domain exceptions (`ConfigurationError`)
    using `raise ... from err` so `__cause__` is preserved for debugging
"""


class ConfigurationError(Exception):
    """Domain-specific exception raised when required app configuration is invalid."""

    def __init__(self, setting_key: str, reason: str) -> None:
        super().__init__(f"Config key {setting_key!r} failed: {reason}")
        self.setting_key = setting_key
        self.reason = reason


def load_database_port(raw_env: dict[str, str]) -> int:
    """Extract and validate `DB_PORT` from `raw_env`, chaining underlying errors."""
    try:
        raw_port = raw_env["DB_PORT"]
        port = int(raw_port)
    except KeyError as err:
        raise ConfigurationError("DB_PORT", "missing required environment variable") from err
    except ValueError as err:
        raise ConfigurationError("DB_PORT", f"must be an integer, got {raw_env['DB_PORT']!r}") from err

    if not (1024 <= port <= 65535):
        raise ConfigurationError("DB_PORT", f"port {port} outside unprivileged range 1024..65535")
    return port


def main() -> None:
    print("=== 1. Valid Configuration ===")
    port = load_database_port({"DB_PORT": "5432"})
    print(f"  Loaded DB_PORT = {port}")

    print("\n=== 2. Catching Chained Domain Exceptions (`__cause__`) ===")
    test_envs = [
        {},
        {"DB_PORT": "not-a-port"},
        {"DB_PORT": "80"},
    ]
    for env in test_envs:
        try:
            load_database_port(env)
        except ConfigurationError as err:
            cause_name = type(err.__cause__).__name__ if err.__cause__ else "None"
            print(f"  Caught ConfigurationError: {err} | __cause__={cause_name}")


if __name__ == "__main__":
    main()
```

### Example 03: EAFP vs LBYL Style & `ExceptionGroup` / `except*` (Python 3.11+)
File: [`example_03_eafp_vs_lbyl_and_exception_groups.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/01_Exception_Handling/example_03_eafp_vs_lbyl_and_exception_groups.py)

```python
"""
Phase 5 - Topic 01: Exception Handling
Example 03: EAFP vs LBYL Style & `ExceptionGroup` / `except*` (Python 3.11+)

Demonstrates:
  - LBYL ("Look Before You Leap") vs Pythonic EAFP ("Easier to Ask Forgiveness than Permission")
  - Adding contextual notes to exceptions with `err.add_note()` (Python 3.11+)
  - Handling multiple concurrent failures with `ExceptionGroup` and `except*` (Python 3.11+)
"""


def lookup_price_lbyl(catalog: dict[str, dict[str, float]], category: str, item: str) -> float:
    """LBYL: Multiple pre-checks before accessing nested keys."""
    if category in catalog and item in catalog[category]:
        return catalog[category][item]
    return 0.0


def lookup_price_eafp(catalog: dict[str, dict[str, float]], category: str, item: str) -> float:
    """EAFP: Attempt the direct lookup and catch `KeyError` on miss."""
    try:
        return catalog[category][item]
    except KeyError:
        return 0.0


def validate_batch_records(records: list[dict[str, object]]) -> None:
    """Collect all validation errors across a batch into an `ExceptionGroup` (Python 3.11+)."""
    errors: list[Exception] = []
    for idx, rec in enumerate(records):
        if "id" not in rec:
            err = KeyError("Missing 'id' field")
            err.add_note(f"Occurred at batch row index {idx}")
            errors.append(err)
        elif not isinstance(rec["id"], int):
            err_type = TypeError(f"Expected int 'id', got {type(rec['id']).__name__}")
            err_type.add_note(f"Occurred at batch row index {idx}")
            errors.append(err_type)

    if errors:
        raise ExceptionGroup("Batch validation failed", errors)


def main() -> None:
    print("=== 1. Comparing LBYL vs EAFP Nested Lookups ===")
    catalog = {"electronics": {"keyboard": 2499.0}}
    print(f"  Hit  (LBYL / EAFP) : {lookup_price_lbyl(catalog, 'electronics', 'keyboard')} / {lookup_price_eafp(catalog, 'electronics', 'keyboard')}")
    print(f"  Miss (LBYL / EAFP) : {lookup_price_lbyl(catalog, 'books', 'novel')} / {lookup_price_eafp(catalog, 'books', 'novel')}")

    print("\n=== 2. Handling Multiple Concurrent Errors with `ExceptionGroup` & `except*` ===")
    batch = [{"id": 101}, {}, {"id": "bad-id"}]
    try:
        validate_batch_records(batch)
    except* KeyError as key_group:
        for e in key_group.exceptions:
            print(f"  [except* KeyError]  {e} | notes={getattr(e, '__notes__', [])}")
    except* TypeError as type_group:
        for e in type_group.exceptions:
            print(f"  [except* TypeError] {e} | notes={getattr(e, '__notes__', [])}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== Tracing `try / except / else / finally` Across 3 Scenarios ===
  --- Input: ('45', '6') ---
    [else] Division succeeded cleanly -> 7.5
    [finally] Releasing parser resources
  --- Input: ('forty-five', '6') ---
    [except ValueError] Invalid number format: could not convert string to float: 'forty-five'
    [finally] Releasing parser resources
  --- Input: ('45', '0') ---
    [except ZeroDivisionError] Denominator cannot be zero!
    [finally] Releasing parser resources
```

### Output — Example 02
```text
=== 1. Valid Configuration ===
  Loaded DB_PORT = 5432

=== 2. Catching Chained Domain Exceptions (`__cause__`) ===
  Caught ConfigurationError: Config key 'DB_PORT' failed: missing required environment variable | __cause__=KeyError
  Caught ConfigurationError: Config key 'DB_PORT' failed: must be an integer, got 'not-a-port' | __cause__=ValueError
  Caught ConfigurationError: Config key 'DB_PORT' failed: port 80 outside unprivileged range 1024..65535 | __cause__=None
```

### Output — Example 03
```text
=== 1. Comparing LBYL vs EAFP Nested Lookups ===
  Hit  (LBYL / EAFP) : 2499.0 / 2499.0
  Miss (LBYL / EAFP) : 0.0 / 0.0

=== 2. Handling Multiple Concurrent Errors with `ExceptionGroup` & `except*` ===
  [except* KeyError]  "Missing 'id' field" | notes=['Occurred at batch row index 1']
  [except* TypeError] Expected int 'id', got str | notes=['Occurred at batch row index 2']
```

---

## 7. Code Explanation

1. **`parse_and_divide` (Example 01):** Notice that even though `except` and `else` both execute `return` statements, Python pauses the return just long enough to execute `finally:` before handing the return value back to the caller.
2. **`ConfigurationError` & `from err` (Example 02):** By calling `super().__init__(...)` and storing `self.setting_key` and `self.reason`, callers can programmatically inspect why configuration failed while `err.__cause__` preserves the original `KeyError` or `ValueError`.
3. **`except*` and `add_note()` (Example 03):** Unlike standard `except`, where only the **first** matching handler runs, `except*` can execute **multiple** clauses in sequence—one for the `KeyError` sub-group and another for the `TypeError` sub-group. `err.add_note(...)` attaches context strings without altering the exception's `args`.

---

## 8. Common Mistakes

1. **Using a Bare `except:` or Silently Passing (`except Exception: pass`):**
   - Swallows syntax typos (`NameError`), type bugs (`TypeError`), and `KeyboardInterrupt`, turning obvious bugs into silent data corruption.
2. **Returning Inside a `finally:` Block:**
   - Placing `return` inside `finally:` **silently discards** any unhandled exception that was currently propagating out of the `try:` block! Never `return`, `break`, or `continue` from inside `finally:`.
3. **Using `raise err` Instead of Bare `raise` When Re-raising:**
   - Inside an `except Exception as err:` block, writing `raise` preserves the original traceback, whereas `raise err` appends an extra frame at the re-raise line.
4. **Ordering Broad Exceptions Before Specific Ones:**
   - Writing `except LookupError:` before `except KeyError:` makes the `KeyError` handler unreachable dead code because `KeyError` is a subclass of `LookupError`.

---

## 9. Practice Questions

1. **Easy:** Write a function `safe_int_list(items: list[str]) -> tuple[list[int], list[str]]` that converts valid integer strings into a list of `int`s and collects invalid strings into a second list using `try / except ValueError / else`.
2. **Medium:** Create a custom exception hierarchy `PaymentError(Exception)` with subclasses `InsufficientFundsError` and `InvalidCurrencyError`. Write a function `process_payment(balance: float, amount: float, currency: str) -> float` that raises the appropriate exception with structured attributes.
3. **Hard:** Write a batch file parser function `run_tasks(tasks: list[callable])` that runs every callable in a list, attaches its task index via `.add_note()`, and raises an `ExceptionGroup` if one or more tasks failed. Handle `ValueError` and `RuntimeError` separately using `except*`.

---

## 10. Interview Questions

### Q1: What happens if an exception is raised inside `try`, not caught by `except`, and the `finally` block executes a `return` statement?
**Answer:** The unhandled exception is **completely suppressed** and discarded, and the function returns the value from the `finally` block as if nothing went wrong. This is considered a severe anti-pattern (flagged by linters as `B012`).

### Q2: What is the difference between `__cause__` and `__context__` on a Python exception object?
**Answer:**
- `__context__` is set **implicitly** whenever a new exception is raised while another exception is already being handled inside an `except` or `finally` block (`"During handling of the above exception, another exception occurred"`).
- `__cause__` is set **explicitly** when you write `raise NewError(...) from original_err` (`"The above exception was the direct cause of the following exception"`). Setting `from None` sets `__suppress_context__ = True`.

### Q3: How does `except*` (Python 3.11+) differ from a normal `except` clause?
**Answer:** A normal `except` clause matches a single exception and at most **one** `except` clause executes per `try` statement. By contrast, `except*` splits an `ExceptionGroup` by matching types: **multiple** `except*` clauses can execute during a single `try` block, each receiving a sub-`ExceptionGroup` containing all matching exceptions, and any remaining unmatched exceptions in the group are automatically re-raised afterward.
