# Phase 5 — Topic 06: Decorators

## 1. Introduction

A **Decorator** is a higher-order callable that takes an existing function (or class), wraps or enhances its behavior with cross-cutting logic (like logging, authentication, caching, timing, or retry policies), and returns the modified callable—all without changing a single line inside the original function's body.

In Python, `@my_decorator` placed directly above `def target():` is clean syntactic sugar for `target = my_decorator(target)`.

---

## 2. Why is it used?

1. **Separation of Cross-Cutting Concerns (DRY Principle):** Instead of copy-pasting timer, permission-check, or retry code at the top of 50 API endpoints, you write `@require_auth` or `@retry(max_attempts=3)` once and apply it declaratively.
2. **Metadata Preservation (`@functools.wraps`):** Properly written decorators retain the wrapped function's `__name__`, `__doc__`, type annotations, and `__wrapped__` pointer so debuggers, `help()`, Sphinx, and FastAPI/Pydantic inspection continue to work.
3. **Composable Behavior via Stacking:** Multiple decorators can be stacked (`@cache`, `@audit_call`, `@validate_types`) to layer independent behaviors cleanly.

---

## 3. Syntax

```python
import functools
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

# 1. Standard 2-Layer Function Decorator
def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# 2. Parameterized 3-Layer Decorator Factory
def repeat(times: int) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result: R
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator
```

---

## 4. Explanation (Step-by-Step)

1. **Decoration Time vs Call Time:**
   - **Decoration time (Import time):** Python evaluates `@decorator` as soon as the `def` statement is loaded, replacing `func` with `wrapper`.
   - **Call time (Runtime):** Whenever callers invoke `func(...)`, they are actually invoking `wrapper(*args, **kwargs)`.
2. **Why `@functools.wraps(func)` Is Essential:**
   - Without `@functools.wraps(func)`, replacing `compute_emi` with `wrapper` overwrites `compute_emi.__name__` with `'wrapper'` and erases `compute_emi.__doc__` and `__annotations__`.
   - `@functools.wraps(func)` copies `__module__`, `__name__`, `__qualname__`, `__doc__`, and `__annotations__` onto `wrapper`, and sets `wrapper.__wrapped__ = func` so you can always access the original undecorated function.
3. **Parameterized Decorator Factories (3 Layers):**
   - When you write `@retry(max_attempts=3)`, Python **first** calls `retry(max_attempts=3)`, which must return a **decorator** function (`def decorator(func):`), which in turn returns `def wrapper(*args, **kwargs):`.
4. **Decorator Stacking Order (Bottom-Up Application, Top-Down Execution):**
   ```python
   @outer
   @inner
   def f(): ...
   ```
   is equivalent to `f = outer(inner(f))`. At call time, `outer`'s wrapper runs **first**, calling `inner`'s wrapper, which calls `f()`.

---

## 5. Minimum 3 Examples

### Example 01: Function Decorators & Preserving Metadata with `@functools.wraps`
File: [`example_01_function_decorator_and_functools_wraps.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/06_Decorators/example_01_function_decorator_and_functools_wraps.py)

```python
"""
Phase 5 - Topic 06: Decorators
Example 01: Function Decorators & Preserving Metadata with `@functools.wraps`

Demonstrates:
  - How `@decorator` syntax is syntactic sugar for `func = decorator(func)`
  - Forwarding arbitrary arguments with `*args, **kwargs`
  - Why `@functools.wraps(func)` is critical to preserve `__name__`, `__doc__`, and `__wrapped__`
"""

import functools
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def audit_call(func: Callable[P, R]) -> Callable[P, R]:
    """Log function entry and exit while preserving original function metadata."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        arg_list = [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
        print(f"  [audit] Calling {func.__name__}({', '.join(arg_list)})")
        result = func(*args, **kwargs)
        print(f"  [audit] {func.__name__} returned {result!r}")
        return result

    return wrapper


@audit_call
def compute_emi(principal: float, annual_rate: float, months: int = 12) -> float:
    """Compute monthly EMI for a loan."""
    monthly_rate = annual_rate / (12 * 100)
    emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / (
        (1 + monthly_rate) ** months - 1
    )
    return round(emi, 2)


def main() -> None:
    print("=== 1. Invoking `@audit_call` Decorated Function ===")
    monthly = compute_emi(100_000, 12.0, months=12)
    print(f"  Result: Rs.{monthly}")

    print("\n=== 2. Inspecting Preserved Metadata (`@functools.wraps`) ===")
    print(f"  __name__ : {compute_emi.__name__!r}")
    print(f"  __doc__  : {compute_emi.__doc__!r}")
    print(f"  Has __wrapped__? {hasattr(compute_emi, '__wrapped__')}")


if __name__ == "__main__":
    main()
```

### Example 02: Parameterized Decorator Factories (`@retry(max_attempts=3)`)
File: [`example_02_parameterized_decorator_factory_retry.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/06_Decorators/example_02_parameterized_decorator_factory_retry.py)

```python
"""
Phase 5 - Topic 06: Decorators
Example 02: Parameterized Decorator Factories (`@retry(max_attempts=3)`)

Demonstrates:
  - Building a 3-layer decorator factory that accepts configuration arguments
  - Automatically retrying transient failures before succeeding or re-raising
"""

import functools
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def retry(
    max_attempts: int = 3,
    catch_exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator factory that retries `func` up to `max_attempts` times on matching exceptions."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except catch_exceptions as err:
                    print(f"  [retry] Attempt {attempt}/{max_attempts} failed: {err}")
                    if attempt == max_attempts:
                        raise
            raise RuntimeError("Unreachable")

        return wrapper

    return decorator


def main() -> None:
    attempts_made = 0

    @retry(max_attempts=3, catch_exceptions=(ConnectionError,))
    def fetch_remote_profile(user_id: int) -> dict[str, object]:
        nonlocal attempts_made
        attempts_made += 1
        if attempts_made < 3:
            raise ConnectionError(f"Transient socket timeout on try #{attempts_made}")
        return {"user_id": user_id, "status": "ok", "attempts": attempts_made}

    print("=== Testing Parameterized `@retry(max_attempts=3)` Decorator ===")
    profile = fetch_remote_profile(42)
    print(f"  Success on attempt #{attempts_made}: {profile}")


if __name__ == "__main__":
    main()
```

### Example 03: Stacking Multiple Decorators & Class-Based Stateful Decorators
File: [`example_03_decorator_stacking_and_class_decorators.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/06_Decorators/example_03_decorator_stacking_and_class_decorators.py)

```python
"""
Phase 5 - Topic 06: Decorators
Example 03: Stacking Multiple Decorators & Class-Based Stateful Decorators

Demonstrates:
  - Stacking order of multiple decorators (`@outer` above `@inner` means `outer(inner(func))`)
  - Implementing a class-based decorator using `__call__` to track invocation counts
"""

import functools
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def html_tag(tag: str) -> Callable[[Callable[P, str]], Callable[P, str]]:
    """Wrap the string return value of a function in `<tag>...</tag>`."""

    def decorator(func: Callable[P, str]) -> Callable[P, str]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
            return f"<{tag}>{func(*args, **kwargs)}</{tag}>"

        return wrapper

    return decorator


class CallCounter:
    """Class-based decorator that counts how many times a function is invoked."""

    def __init__(self, func: Callable[P, R]) -> None:
        functools.update_wrapper(self, func)
        self.func = func
        self.call_count = 0

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        self.call_count += 1
        return self.func(*args, **kwargs)


@html_tag("div")
@html_tag("strong")
def render_headline(title: str) -> str:
    return title.strip()


@CallCounter
def add_numbers(a: int, b: int) -> int:
    return a + b


def main() -> None:
    print("=== 1. Stacking Decorators (`@html_tag('div')` over `@html_tag('strong')`) ===")
    print(f"  Output: {render_headline('Python 3.13 Released')}")

    print("\n=== 2. Class-Based Decorator Tracking Call Counts (`__call__`) ===")
    print(f"  Call 1: {add_numbers(10, 20)} | call_count={add_numbers.call_count}")
    print(f"  Call 2: {add_numbers(5, 7)}  | call_count={add_numbers.call_count}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== 1. Invoking `@audit_call` Decorated Function ===
  [audit] Calling compute_emi(100000, 12.0, months=12)
  [audit] compute_emi returned 8884.88
  Result: Rs.8884.88

=== 2. Inspecting Preserved Metadata (`@functools.wraps`) ===
  __name__ : 'compute_emi'
  __doc__  : 'Compute monthly EMI for a loan.'
  Has __wrapped__? True
```

### Output — Example 02
```text
=== Testing Parameterized `@retry(max_attempts=3)` Decorator ===
  [retry] Attempt 1/3 failed: Transient socket timeout on try #1
  [retry] Attempt 2/3 failed: Transient socket timeout on try #2
  Success on attempt #3: {'user_id': 42, 'status': 'ok', 'attempts': 3}
```

### Output — Example 03
```text
=== 1. Stacking Decorators (`@html_tag('div')` over `@html_tag('strong')`) ===
  Output: <div><strong>Python 3.13 Released</strong></div>

=== 2. Class-Based Decorator Tracking Call Counts (`__call__`) ===
  Call 1: 30 | call_count=1
  Call 2: 12  | call_count=2
```

---

## 7. Code Explanation

1. **`ParamSpec("P")` and `TypeVar("R")` (Examples 01–03):** Introduced in Python 3.10, `ParamSpec` lets type checkers (`mypy`/`pyright`) preserve the exact parameter signature `(principal: float, annual_rate: float, months: int = 12) -> float` across `wrapper(*args: P.args, **kwargs: P.kwargs) -> R`.
2. **3-Layer `retry` Factory (Example 02):** `retry(...)` validates `max_attempts`, returns `decorator`, which takes `func` and returns `wrapper`. Inside `wrapper`, transient `catch_exceptions` are caught up to `max_attempts - 1` times and re-raised on the final attempt.
3. **`CallCounter` with `functools.update_wrapper` (Example 03):** Inside a class-based decorator's `__init__`, `functools.update_wrapper(self, func)` performs the exact same metadata copying that `@functools.wraps(func)` does for nested functions.

---

## 8. Common Mistakes

1. **Forgetting to Return the Result of `func(*args, **kwargs)` Inside `wrapper`:**
   - Calling `func(*args, **kwargs)` without `return func(*args, **kwargs)` causes every decorated function to silently return `None`!
2. **Writing `@my_decorator()` With Parentheses on a Non-Parameterized Decorator (or Vice Versa):**
   - A 2-layer decorator is used as `@audit_call` (no parentheses). A 3-layer factory is used as `@retry(max_attempts=3)` (with parentheses).
3. **Omitting `@functools.wraps(func)`:**
   - Breaks FastAPI dependency injection, pytest fixtures, `pickle`, and documentation generators that inspect `__name__` and `__annotations__`.
4. **Calling `func()` Inside the Decorator Instead of Inside `wrapper()`:**
   - Executing `func()` inside `decorator(func)` runs the function once at import time instead of on every call.

---

## 9. Practice Questions

1. **Easy:** Write a `@timer` decorator using `time.perf_counter()` in a `try / finally` block that prints the execution duration in milliseconds even if the wrapped function raises an exception.
2. **Medium:** Write a parameterized `@enforce_types` decorator that inspects `func.__annotations__` at call time and raises `TypeError` if any positional argument does not match its annotated type.
3. **Hard:** Write a decorator `@ flexible_retry` that works **both** with parentheses (`@flexible_retry(max_attempts=5)`) and without parentheses (`@flexible_retry`) by checking `if _func is None:`.

---

## 10. Interview Questions

### Q1: How can you call the original undecorated function if it has been wrapped with `@functools.wraps`?
**Answer:** Access the `__wrapped__` attribute set by `@functools.wraps`: `compute_emi.__wrapped__(100_000, 12.0)`. This is widely used in unit tests when you want to test core function logic without triggering rate-limiting or retry decorators.

### Q2: In what order do stacked decorators `@A`, `@B`, `@C` execute?
**Answer:**
- **Decoration time (bottom-up):** `@C` wraps `func` first, `@B` wraps the result of `C(func)`, and `@A` wraps the result of `B(C(func))` (`func = A(B(C(func)))`).
- **Call time (top-down):** Calling `func()` enters `A.wrapper` first -> `B.wrapper` -> `C.wrapper` -> original `func`.

### Q3: How do you write a decorator that can be used both as `@my_dec` and `@my_dec(opt=1)`?
**Answer:** Define `def my_dec(_func: Callable | None = None, *, opt: int = 1):`. If `_func is None` (called with keyword args as `@my_dec(opt=2)`), return `decorator`; otherwise (called bare as `@my_dec`), immediately return `decorator(_func)`.
