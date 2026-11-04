# Phase 5 — Topic 07: Closures

## 1. Introduction

A **Closure** is a nested function object that remembers and retains access to variables from its enclosing lexical scope (`E` in the LEGB rule) **even after the outer function has finished executing and its stack frame has been destroyed**.

Closures are the foundational mechanism that makes Python decorators, function factories, callback handlers, and functional state encapsulation possible.

---

## 2. Why is it used?

1. **Lightweight Function Factories:** When you need a family of specialized functions (like tax calculators for different regions or multipliers) without defining an entire class hierarchy.
2. **Data Encapsulation Without `self`:** Enclosing variables stored in `__closure__` cells are naturally private to the inner function unless explicitly exposed.
3. **Powering Decorators:** Every function decorator (`wrapper(*args, **kwargs)`) is a closure that closes over the original `func` (and any decorator parameters).
4. **Stateful Callables (`nonlocal`):** A closure can maintain mutable state (counters, moving averages, memoization caches) across calls using `nonlocal`.

---

## 3. Syntax

```python
from typing import Callable

# 1. Read-Only Closure Capturing Enclosing Parameter
def make_exponentiator(power: int) -> Callable[[int], int]:
    def raise_to(base: int) -> int:
        return base ** power  # `power` is a free variable captured in `__closure__`
    return raise_to

square = make_exponentiator(2)
cube = make_exponentiator(3)

# 2. Mutable Stateful Closure Using `nonlocal`
def make_counter(start: int = 0) -> Callable[[], int]:
    current = start
    def increment() -> int:
        nonlocal current
        current += 1
        return current
    return increment
```

---

## 4. Explanation (Step-by-Step)

1. **What Qualifies as a Closure?**
   - Three conditions must be met:
     1. There is a nested function defined inside an enclosing function.
     2. The nested function references at least one **free variable** from the enclosing scope.
     3. The enclosing function returns (or passes out) the nested function object.
2. **How Python Implements Closures Under the Hood (`cell` Objects):**
   - Normally, local variables live on the C call stack and vanish when a function returns.
   - When the Python compiler sees that an inner function references an outer variable, it promotes that variable into a heap-allocated **`cell` object** stored in `inner.__closure__` (with variable names listed in `inner.__code__.co_freevars`).
3. **Why `nonlocal` Is Needed for Rebinding:**
   - Reading a free variable or mutating a mutable container (`cache[k] = v`) works without `nonlocal`.
   - Reassigning an immutable variable (`count += 1`) inside the inner function would normally create a brand-new local variable shadowing the outer one (raising `UnboundLocalError`). Declaring `nonlocal count` instructs Python to update the shared closure `cell` instead.
4. **The Classic Late-Binding Loop Trap:**
   - closures capture **variables (cells), not values at creation time**.
   - In `[lambda x: x + i for i in range(3)]`, all three lambdas point to the **same** cell `i`, which holds `2` after the loop ends.
   - Fix: bind the current value as a default parameter at definition time (`[lambda x, i=i: x + i for i in range(3)]`) or use `functools.partial`.

---

## 5. Minimum 3 Examples

### Example 01: Anatomy of a Closure — Free Variables & Inspecting `__closure__` Cells
File: [`example_01_closure_anatomy_and_cell_inspection.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/07_Closures/example_01_closure_anatomy_and_cell_inspection.py)

```python
"""
Phase 5 - Topic 07: Closures
Example 01: Anatomy of a Closure — Free Variables & Inspecting `__closure__` Cells

Demonstrates:
  - How an inner function retains access to enclosing scope variables even after
    the outer function has finished executing and its stack frame is gone
  - Inspecting `__code__.co_freevars` and `[cell.cell_contents for cell in fn.__closure__]`
"""

from typing import Callable


def make_tax_calculator(region: str, tax_rate: float) -> Callable[[float], float]:
    """Return a closure that remembers `region` and `tax_rate` from the enclosing scope."""

    def calculate(amount: float) -> float:
        total = round(amount * (1.0 + tax_rate), 2)
        print(f"  [{region} @ {tax_rate * 100:.1f}%] Rs.{amount:,.2f} -> Rs.{total:,.2f}")
        return total

    return calculate


def main() -> None:
    print("=== 1. Creating Independent Closures from the Same Factory ===")
    gst_standard = make_tax_calculator("IN-GST-18", 0.18)
    gst_luxury = make_tax_calculator("IN-GST-28", 0.28)

    gst_standard(1000.0)
    gst_luxury(1000.0)

    print("\n=== 2. Introspecting Closure Free Variables & Cell Contents ===")
    free_vars = gst_standard.__code__.co_freevars
    cell_values = [cell.cell_contents for cell in (gst_standard.__closure__ or ())]
    print(f"  co_freevars   : {free_vars}")
    print(f"  cell_contents : {dict(zip(free_vars, cell_values))}")


if __name__ == "__main__":
    main()
```

### Example 02: Stateful Closures with `nonlocal` vs Late-Binding Loop Pitfall
File: [`example_02_stateful_nonlocal_and_late_binding_trap.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/07_Closures/example_02_stateful_nonlocal_and_late_binding_trap.py)

```python
"""
Phase 5 - Topic 07: Closures
Example 02: Stateful Closures with `nonlocal` vs Late-Binding Loop Pitfall

Demonstrates:
  - Mutating enclosing state across calls using the `nonlocal` keyword
  - The classic late-binding closure trap in loops (`[lambda x: x + i for i in range(3)]`)
    and how to fix it with a default parameter (`i=i`)
"""

from typing import Callable


def make_moving_average() -> Callable[[float], float]:
    """Stateful closure tracking running total and count via `nonlocal`."""
    total = 0.0
    count = 0

    def add_sample(value: float) -> float:
        nonlocal total, count
        total += value
        count += 1
        return round(total / count, 2)

    return add_sample


def main() -> None:
    print("=== 1. Stateful Closure with `nonlocal` (Moving Average) ===")
    avg = make_moving_average()
    for reading in [10.0, 20.0, 45.0]:
        print(f"  Added {reading:>4.1f} -> running average = {avg(reading)}")

    print("\n=== 2. Classic Late-Binding Loop Trap vs Early-Binding Fix ===")
    # Buggy: all lambdas share the SAME cell for `i`, which ends at 2 after the loop!
    buggy_Adders = [lambda x: x + i for i in range(3)]
    # Fixed: `i=i` binds the current value of `i` as a default argument at creation time
    fixed_adders = [lambda x, i=i: x + i for i in range(3)]

    print(f"  Buggy [fn(10) for fn in buggy_Adders] : {[fn(10) for fn in buggy_Adders]} (all used i=2!)")
    print(f"  Fixed [fn(10) for fn in fixed_adders] : {[fn(10) for fn in fixed_adders]} (used i=0, 1, 2)")


if __name__ == "__main__":
    main()
```

### Example 03: Closure-Based Memoization Cache & Comparing Closures vs Single-Method Classes
File: [`example_03_closure_memoization_vs_callable_class.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/07_Closures/example_03_closure_memoization_vs_callable_class.py)

```python
"""
Phase 5 - Topic 07: Closures
Example 03: Closure-Based Memoization Cache & Comparing Closures vs Single-Method Classes

Demonstrates:
  - Building a custom memoization closure that caches expensive function results in a private dict
  - Exposing cache statistics (`stats`) as an attribute attached to the closure
"""

import functools
from typing import Callable


def memoize_unary(func: Callable[[int], int]) -> Callable[[int], int]:
    """Closure-based memoizer storing `(hits, misses)` and `cache` in enclosing scope."""
    cache: dict[int, int] = {}
    hits = 0
    misses = 0

    @functools.wraps(func)
    def wrapper(n: int) -> int:
        nonlocal hits, misses
        if n in cache:
            hits += 1
            return cache[n]
        misses += 1
        result = func(n)
        cache[n] = result
        return result

    def stats() -> dict[str, int]:
        return {"hits": hits, "misses": misses, "size": len(cache)}

    wrapper.stats = stats  # type: ignore[attr-defined]
    return wrapper


@memoize_unary
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def main() -> None:
    print("=== Closure-Based Memoization Cache on Recursive `fib(10)` ===")
    result = fib(10)
    print(f"  fib(10) = {result}")
    print(f"  Cache stats after fib(10): {fib.stats()}")  # type: ignore[attr-defined]

    print(f"  fib(8)  = {fib(8)} (instant cache hit!)")
    print(f"  Cache stats after fib(8) : {fib.stats()}")  # type: ignore[attr-defined]


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== 1. Creating Independent Closures from the Same Factory ===
  [IN-GST-18 @ 18.0%] Rs.1,000.00 -> Rs.1,180.00
  [IN-GST-28 @ 28.0%] Rs.1,000.00 -> Rs.1,280.00

=== 2. Introspecting Closure Free Variables & Cell Contents ===
  co_freevars   : ('region', 'tax_rate')
  cell_contents : {'region': 'IN-GST-18', 'tax_rate': 0.18}
```

### Output — Example 02
```text
=== 1. Stateful Closure with `nonlocal` (Moving Average) ===
  Added 10.0 -> running average = 10.0
  Added 20.0 -> running average = 15.0
  Added 45.0 -> running average = 25.0

=== 2. Classic Late-Binding Loop Trap vs Early-Binding Fix ===
  Buggy [fn(10) for fn in buggy_Adders] : [12, 12, 12] (all used i=2!)
  Fixed [fn(10) for fn in fixed_adders] : [10, 11, 12] (used i=0, 1, 2)
```

### Output — Example 03
```text
=== Closure-Based Memoization Cache on Recursive `fib(10)` ===
  fib(10) = 55
  Cache stats after fib(10): {'hits': 8, 'misses': 11, 'size': 11}
  fib(8)  = 21 (instant cache hit!)
  Cache stats after fib(8) : {'hits': 9, 'misses': 11, 'size': 11}
```

---

## 7. Code Explanation

1. **`__code__.co_freevars` and `__closure__` (Example 01):** Each call to `make_tax_calculator` allocates a distinct tuple of `cell` objects in `__closure__`, so `gst_standard` and `gst_luxury` never interfere with each other.
2. **`nonlocal total, count` (Example 02):** Because `float` and `int` are immutable, `total += value` rebinds `total` to a new float object. `nonlocal` directs that rebinding to the enclosing closure cell.
3. **Multiple Inner Functions Sharing the Same Closure Cells (Example 03):** Both `wrapper` and `stats` close over the exact same `hits`, `misses`, and `cache` cells—just like methods on an object share `self`, except `cache` cannot be accidentally mutated from outside unless accessed via `__closure__`.

---

## 8. Common Mistakes

1. **Late Binding Inside Loops (`for i in range(...)`):** Creating lambdas or `def` functions inside a loop that reference the loop variable `i` without binding `i=i` as a default argument causes all functions to see only the final value of `i`.
2. **Confusing `nonlocal` with `global`:** `global` always jumps straight to the module-level namespace (`G`), bypassing any enclosing functions (`E`). `nonlocal` searches only enclosing function scopes (`E`) and fails with a `SyntaxError` if the variable only exists at module level.
3. **Unbounded Closure Caches Causing Memory Leaks:** Storing a `dict` inside a long-lived closure without eviction (`maxsize`) retains references to all arguments and results for the lifetime of the closure (prefer `@functools.lru_cache(maxsize=128)` in production).

---

## 9. Practice Questions

1. **Easy:** Write a closure factory `make_prefix_logger(prefix: str) -> Callable[[str], str]` that returns a function formatting messages as `f"[{prefix}] {msg}"`.
2. **Medium:** Write a stateful closure `make_rate_limiter(max_calls: int) -> Callable[[], bool]` that returns `True` for the first `max_calls` invocations and `False` thereafter, plus a `.reset()` helper attribute attached to the returned function.
3. **Hard:** Write a function `make_bank_account(initial_balance: float)` that returns a `dict` of three closures (`"deposit"`, `"withdraw"`, `"get_balance"`) sharing a single private `balance` cell without using any `class` definition.

---

## 10. Interview Questions

### Q1: Why does `[lambda x: x * i for i in range(4)]` return `[6, 6, 6, 6]` when called with `2`?
**Answer:** Python closures are **late-binding** (lexical reference binding, not value binding). All four lambdas look up the variable `i` in the enclosing comprehension scope **when they are called**, by which time the loop has finished and `i == 3`. Thus every call computes `2 * 3 = 6`.

### Q2: Why do we need `nonlocal` to do `count += 1` in a closure, but we do NOT need `nonlocal` to do `cache[key] = value`?
**Answer:** `cache[key] = value` calls `cache.__setitem__(key, value)`, which **mutates** the existing dictionary object in place without changing which object the name `cache` points to. By contrast, `count += 1` (`count = count + 1`) **rebinds** the variable name `count` to a new `int` object, which Python treats as defining a new local variable unless `nonlocal count` is declared.

### Q3: When should you choose a closure over a class, and vice versa?
**Answer:**
- Choose a **closure** when you only need a single callable behavior (`__call__`) with 1–2 pieces of configuration or state (e.g., decorators, sort keys, callbacks).
- Choose a **class** when you need multiple public methods, inheritance, type-checked attributes, `__repr__`, or equality comparisons.
