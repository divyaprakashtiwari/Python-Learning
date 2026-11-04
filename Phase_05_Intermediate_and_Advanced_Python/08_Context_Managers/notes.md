# Phase 5 — Topic 08: Context Managers

## 1. Introduction

A **Context Manager** is an object that defines the runtime context to be established when entering a `with` statement (`__enter__`) and guarantees deterministic teardown logic when exiting the `with` block (`__exit__`)—regardless of whether the block finishes normally, executes an early `return`, or raises an unhandled exception.

Beyond file I/O (`with open(...)`), context managers are the standard Pythonic pattern for managing database transactions, thread/async locks (`with lock:`), temporary directory/environment changes, network sessions, and test mocks.

---

## 2. Why is it used?

1. **Deterministic Resource Cleanup:** Eliminates repetitive `try / finally` boilerplate across callers while guaranteeing that locks are released, connections are returned to pools, and temporary state is restored.
2. **Atomic Transaction Semantics:** `__exit__(self, exc_type, exc_val, exc_tb)` receives full details of any exception raised inside the `with` block, allowing a database transaction context manager to automatically `COMMIT` when `exc_type is None` and `ROLLBACK` when `exc_type is not None`.
3. **Ergonomic Authoring (`@contextlib.contextmanager`):** Turns any single-`yield` generator function wrapped in `try / finally` into a full context manager without writing a class.
4. **Dynamic Resource Composition (`contextlib.ExitStack`):** Safely manages a dynamic runtime-determined number of resources in a single `with` block.

---

## 3. Syntax

```python
from contextlib import contextmanager, ExitStack, suppress
from types import TracebackType
from typing import Iterator

# 1. Class-Based Context Manager Protocol
class ManagedResource:
    def __enter__(self) -> "ManagedResource":
        # Acquire resource
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        # Release resource
        return False  # False = propagate exceptions; True = suppress exception

# 2. Generator-Based Context Manager
@contextmanager
def managed_resource() -> Iterator[str]:
    resource = "acquired"
    try:
        yield resource
    finally:
        # Cleanup guaranteed even if caller raises inside `with` block
        pass
```

---

## 4. Explanation (Step-by-Step)

1. **Exact Execution Flow of `with EXPR as VAR:`:**
   - Step 1: Evaluates `mgr = EXPR`.
   - Step 2: Calls `val = mgr.__enter__()` and binds `VAR = val` (if `as VAR` is present). Note that `VAR` is bound to **the return value of `__enter__()`**, not necessarily `mgr` itself!
   - Step 3: Executes the body of the `with` block.
   - Step 4:
     - If the body exited without an exception, calls `mgr.__exit__(None, None, None)`.
     - If the body raised an exception `exc`, calls `should_suppress = mgr.__exit__(type(exc), exc, exc.__traceback__)`. If `should_suppress` is truthy (`True`), the exception is swallowed; if falsy (`False` or `None`), the exception continues propagating outward.
2. **How `@contextlib.contextmanager` Works:**
   - Code **before** `yield` runs inside `__enter__()`; the yielded value becomes the `as target` variable.
   - When the `with` block exits normally, the generator resumes after `yield`.
   - When the `with` block raises an exception, `__exit__()` injects that exception directly into the paused `yield` point via `gen.throw(exc)`! That is why **wrapping `yield` in `try: ... finally:` is mandatory** inside `@contextmanager` functions.

---

## 5. Minimum 3 Examples

### Example 01: Class-Based Context Manager (`__enter__` and `__exit__`) — Database Transaction Simulator
File: [`example_01_class_context_manager_enter_exit.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/08_Context_Managers/example_01_class_context_manager_enter_exit.py)

```python
"""
Phase 5 - Topic 08: Context Managers
Example 01: Class-Based Context Manager (`__enter__` and `__exit__`) — Database Transaction Simulator

Demonstrates:
  - Implementing the Context Manager protocol (`__enter__` and `__exit__`) on a custom class
  - Automatic `COMMIT` when the `with` block exits cleanly (`exc_type is None`)
  - Automatic `ROLLBACK` when an exception occurs inside the `with` block (`exc_type is not None`)
"""

from types import TracebackType


class TransactionalList:
    """Wrap a list in an atomic transaction: commit on clean exit, rollback on exception."""

    def __init__(self, target: list[str]) -> None:
        self._target = target
        self._working_copy: list[str] = []

    def __enter__(self) -> list[str]:
        self._working_copy = list(self._target)
        print(f"  [__enter__] Transaction started (snapshot={self._working_copy})")
        return self._working_copy

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        if exc_type is None:
            self._target[:] = self._working_copy
            print(f"  [__exit__]  COMMIT succeeded -> {self._target}")
        else:
            print(f"  [__exit__]  ROLLBACK triggered due to {exc_type.__name__}: {exc_val}")
        # Returning False propagates any exception outward instead of swallowing it
        return False


def main() -> None:
    ledger = ["tx-100"]

    print("=== 1. Successful Transaction (`exc_type is None` -> COMMIT) ===")
    with TransactionalList(ledger) as working:
        working.append("tx-101")
        working.append("tx-102")
    print(f"  Ledger after commit: {ledger}")

    print("\n=== 2. Failed Transaction (`RuntimeError` -> ROLLBACK) ===")
    try:
        with TransactionalList(ledger) as working:
            working.append("tx-corrupted")
            raise RuntimeError("Payment gateway rejected batch")
    except RuntimeError:
        print(f"  Ledger after rollback (unchanged!): {ledger}")


if __name__ == "__main__":
    main()
```

### Example 02: Generator-Based Context Managers with `@contextlib.contextmanager`
File: [`example_02_contextlib_contextmanager_decorator.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/08_Context_Managers/example_02_contextlib_contextmanager_decorator.py)

```python
"""
Phase 5 - Topic 08: Context Managers
Example 02: Generator-Based Context Managers with `@contextlib.contextmanager`

Demonstrates:
  - Writing concise context managers using `@contextlib.contextmanager` and `try / yield / finally`
  - Why wrapping `yield` inside `try ... finally` is mandatory so cleanup still runs on exceptions
"""

from contextlib import contextmanager
import os
from pathlib import Path
import tempfile
from typing import Iterator


@contextmanager
def temporary_working_directory(target_dir: Path) -> Iterator[Path]:
    """Temporarily switch `os.getcwd()` to `target_dir` and restore original cwd on exit."""
    original_cwd = Path.cwd()
    os.chdir(target_dir)
    print(f"  [enter] Switched working directory to: {Path.cwd().name}")
    try:
        yield target_dir
    finally:
        os.chdir(original_cwd)
        print(f"  [exit]  Restored working directory to: {Path.cwd().name}")


def main() -> None:
    start_dir = Path.cwd()
    print(f"=== Starting in `{start_dir.name}` ===")

    with tempfile.TemporaryDirectory() as tmp_str:
        sandbox_dir = Path(tmp_str) / "workspace_sandbox"
        sandbox_dir.mkdir()
        try:
            with temporary_working_directory(sandbox_dir):
                marker = Path("inside_temp.txt")
                marker.write_text("hello", encoding="utf-8")
                print(f"  Inside block: created {marker.name} (exists={marker.exists()})")
                raise ValueError("Simulated error inside context block")
        except ValueError as err:
            print(f"  Caught expected error outside block: {err}")

    print(f"=== Verified cwd restored after exception: {Path.cwd() == start_dir} ===")


if __name__ == "__main__":
    main()
```

### Example 03: Standard `contextlib` Power Tools (`suppress`, `redirect_stdout`, and `ExitStack`)
File: [`example_03_suppress_redirect_stdout_and_exitstack.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/08_Context_Managers/example_03_suppress_redirect_stdout_and_exitstack.py)

```python
"""
Phase 5 - Topic 08: Context Managers
Example 03: Standard `contextlib` Power Tools (`suppress`, `redirect_stdout`, and `ExitStack`)

Demonstrates:
  - `contextlib.suppress()`: declarative replacement for `try: ... except FileNotFoundError: pass`
  - `contextlib.redirect_stdout()`: capturing `print()` output into an `io.StringIO` buffer
  - `contextlib.ExitStack()`: dynamically entering an arbitrary number of context managers at runtime
"""

from contextlib import ExitStack, redirect_stdout, suppress
import io
from pathlib import Path
import tempfile


def main() -> None:
    print("=== 1. `contextlib.suppress` for Intentional Error Ignoring ===")
    with suppress(FileNotFoundError):
        Path("non_existent_temp_file_12345.tmp").unlink()
    print("  Cleanly ignored missing file deletion via `with suppress(FileNotFoundError):`")

    print("\n=== 2. Capturing `print()` Output with `contextlib.redirect_stdout` ===")
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print("Line A captured in memory")
        print("Line B captured in memory")
    captured_lines = buffer.getvalue().splitlines()
    print(f"  Captured {len(captured_lines)} lines: {captured_lines}")

    print("\n=== 3. Dynamic Multi-File Management with `contextlib.ExitStack` ===")
    with tempfile.TemporaryDirectory() as tmp_dir:
        paths = [Path(tmp_dir) / f"shard_{i}.txt" for i in range(3)]
        with ExitStack() as stack:
            handles = [stack.enter_context(open(p, mode="w", encoding="utf-8")) for p in paths]
            for idx, fh in enumerate(handles):
                fh.write(f"Shard #{idx} payload\n")
        # All 3 files are guaranteed closed upon exiting `ExitStack`
        print(f"  All {len(paths)} handles closed? {[fh.closed for fh in handles]}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== 1. Successful Transaction (`exc_type is None` -> COMMIT) ===
  [__enter__] Transaction started (snapshot=['tx-100'])
  [__exit__]  COMMIT succeeded -> ['tx-100', 'tx-101', 'tx-102']
  Ledger after commit: ['tx-100', 'tx-101', 'tx-102']

=== 2. Failed Transaction (`RuntimeError` -> ROLLBACK) ===
  [__enter__] Transaction started (snapshot=['tx-100', 'tx-101', 'tx-102'])
  [__exit__]  ROLLBACK triggered due to RuntimeError: Payment gateway rejected batch
  Ledger after rollback (unchanged!): ['tx-100', 'tx-101', 'tx-102']
```

### Output — Example 02
```text
=== Starting in `Python Learning` ===
  [enter] Switched working directory to: workspace_sandbox
  Inside block: created inside_temp.txt (exists=True)
  [exit]  Restored working directory to: Python Learning
  Caught expected error outside block: Simulated error inside context block
=== Verified cwd restored after exception: True ===
```

### Output — Example 03
```text
=== 1. `contextlib.suppress` for Intentional Error Ignoring ===
  Cleanly ignored missing file deletion via `with suppress(FileNotFoundError):`

=== 2. Capturing `print()` Output with `contextlib.redirect_stdout` ===
  Captured 2 lines: ['Line A captured in memory', 'Line B captured in memory']

=== 3. Dynamic Multi-File Management with `contextlib.ExitStack` ===
  All 3 handles closed? [True, True, True]
```

---

## 7. Code Explanation

1. **`TransactionalList` (Example 01):** `__enter__` returns a shallow copy `self._working_copy`. All mutations inside the `with` block affect only `_working_copy`. In `__exit__`, if `exc_type is None`, the slice assignment `self._target[:] = self._working_copy` commits the changes in place; otherwise, `_working_copy` is discarded.
2. **`@contextmanager` + `try / finally` (Example 02):** Even though `raise ValueError(...)` occurred inside the `with` block, `@contextmanager` threw the `ValueError` into the suspended `yield`, triggering the `finally:` block to restore `os.chdir(original_cwd)`.
3. **`ExitStack` (Example 03):** When you don't know until runtime how many files or locks need to be acquired (e.g., `paths` has $N$ elements), `stack.enter_context(...)` registers each context manager on a LIFO stack and unwinds all of them in reverse order on exit.

---

## 8. Common Mistakes

1. **Forgetting `try / finally` Around `yield` in `@contextmanager`:**
   - Without `try / finally`, any exception raised inside the `with` block causes the generator to unwind at `yield` **without executing the teardown lines after `yield`**!
2. **Accidentally Returning a Truthy Value from `__exit__`:**
   - Returning `True` (or any non-empty object) from `__exit__` tells Python to **swallow** any exception raised inside the `with` block. Always return `False` (or `None`) unless your context manager is specifically designed to suppress exceptions (like `contextlib.suppress`).
3. **Yielding More Than Once in a `@contextmanager` Function:**
   - `@contextmanager` generators must execute **exactly one `yield`**. Yielding a second time raises `RuntimeError: generator didn't stop`.

---

## 9. Practice Questions

1. **Easy:** Write a `@contextmanager` named ` execution_timer(label: str)` using `time.perf_counter()` that yields a dictionary `stats = {}` and populates `stats["elapsed_ms"]` in its `finally` block.
2. **Medium:** Write a class-based context manager `TemporaryEnvVar(key: str, value: str)` that sets `os.environ[key] = value` on enter and restores the previous value (or deletes `key` if it was absent) on exit.
3. **Hard:** Inherit from `contextlib.ContextDecorator` to build a ` ProfileBlock` class that can be used **both** as a `with ProfileBlock():` context manager and as a `@ProfileBlock()` function decorator!

---

## 10. Interview Questions

### Q1: What does the `as var` clause in `with expression as var:` bind `var` to?
**Answer:** `var` is bound to **the return value of `expression.__enter__()`**, **not** the result of `expression` itself. For files, `open(...)` returns a `TextIOWrapper` whose `__enter__()` happens to `return self`, but in general `__enter__()` can return any helper object (like a database cursor or working snapshot).

### Q2: How does `contextlib.ContextDecorator` work?
**Answer:** Inheriting from `ContextDecorator` (which `@contextlib.contextmanager` also uses automatically since Python 3.2!) lets a context manager double as a `@decorator` on functions: each call to the decorated function is automatically wrapped inside `with self:`.

### Q3: When should you use `contextlib.ExitStack`?
**Answer:**
1. When entering a **variable number** of context managers determined at runtime (e.g., opening a list of $N$ shard files).
2. When some context managers are entered **conditionally** (`if use_tls: stack.enter_context(...)`) without duplicating the body of the `with` block.
3. When registering arbitrary cleanup callbacks (`stack.callback(cleanup_fn, arg)`) alongside regular context managers.
