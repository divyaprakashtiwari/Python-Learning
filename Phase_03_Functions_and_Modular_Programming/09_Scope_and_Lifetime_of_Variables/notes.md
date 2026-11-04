# Phase 3 — Topic 09: Scope and Lifetime of Variables

## 1. Introduction

Every variable in a Python program has two fundamental properties:
1. **Scope (Visibility — *Where* can this variable name be accessed?):** Determined statically by where the variable is assigned in the source code, governed by Python's **LEGB Rule** (**L**ocal $\rightarrow$ **E**nclosing $\rightarrow$ **G**lobal $\rightarrow$ **B**uilt-in).
2. **Lifetime (Duration — *How long* does this variable stay alive in memory?):** Determined dynamically at runtime by the lifespan of the namespace (stack frame, closure cell, or module) holding the reference.

---

## 2. Why is it used?

- **Namespace Isolation:** Local scope guarantees that naming a variable `temp` or `i` inside one function will never accidentally overwrite a variable named `temp` or `i` in another function.
- **Stateful Encapsulation (`nonlocal` & Closures):** Enclosing scope allows inner functions to remember and update private state across calls without exposing mutable global variables.
- **Preventing `UnboundLocalError` Bugs:** Understanding how Python decides whether a variable is local at **compile time** prevents one of the most confusing runtime exceptions beginners face.

---

## 3. Syntax

```python
GLOBAL_COUNTER = 0  # [G] Global Scope


def outer():
    enclosing_state = 10  # [E] Enclosing Scope

    def inner():
        nonlocal enclosing_state  # Allows rebinding `enclosing_state` in [E]
        global GLOBAL_COUNTER     # Allows rebinding `GLOBAL_COUNTER` in [G]
        local_var = 5             # [L] Local Scope
        enclosing_state += local_var
        GLOBAL_COUNTER += 1
```

---

## 4. Explanation (Step-by-Step)

### Step 1: The LEGB Name Resolution Rule
Whenever your code reads a variable name, Python searches four namespaces in strict order and stops at the first match:
1. **L — Local:** Inside the currently executing function (or comprehension).
2. **E — Enclosing (Nonlocal):** Inside any outer `def` functions that wrap the current function (from innermost to outermost).
3. **G — Global (Module):** At the top level of the current `.py` module file.
4. **B — Built-in:** Python's preloaded `builtins` module (`len`, `print`, `range`, `ValueError`, etc.).
- If the name is not found in any of the four scopes, Python raises a `NameError`.

### Step 2: Variable Lifetime
- **Local variables** are born when a function is called (a new stack frame is pushed) and destroyed as soon as the function returns (the stack frame is popped and objects with zero remaining references are garbage-collected).
- **Enclosing variables captured by a closure** have an **extended lifetime**: Python stores them in a special `cell` object (`func.__closure__`) so they stay alive as long as the returned inner function exists—even after the outer function has finished!
- **Global variables** stay alive from the moment the module is imported until the Python process terminates.

### Step 3: Why `UnboundLocalError` Happens (Compile-Time Scope Analysis)
Python decides whether a variable name inside a function is **Local** when compiling the function's bytecode (`def`), **not** line-by-line at runtime:
- **Rule:** If a variable is **assigned to anywhere** inside a function body (`x = ...` or `x += ...`) and is not declared `global` or `nonlocal`, Python marks `x` as a **Local variable for the entire function**.
- If you try to read `print(x)` on line 1 before `x += 1` on line 2, Python looks up `x` in the Local scope (ignoring any global `x`!) and raises `UnboundLocalError: cannot access local variable 'x' where it is not associated with a value`.

### Step 4: No Block Scope in Python (`if`, `for`, `while`, `try`)
Unlike C++, Java, or JavaScript (`let`/`const`), **`if/else` blocks, `for`/`while` loops, and `try/except` blocks do NOT create a new scope in Python**. Variables assigned inside an `if` block or `for` loop header belong to the surrounding function's Local scope (or Global scope) and remain accessible after the block ends!

---

## 5. Minimum 3 Examples

### Example 1: The LEGB Rule (Local -> Enclosing -> Global -> Built-in) & Variable Lifetime
File: `example_01_legb_rule_and_lifetime.py`

```python
# [G] GLOBAL SCOPE: lives for the entire duration of the module
APP_THEME = "dark-global"


def outer_dashboard() -> None:
    # [E] ENCLOSING SCOPE: lives while `outer_dashboard` (or a closure) is active
    APP_THEME = "solarized-enclosing"

    def inner_widget() -> None:
        # [L] LOCAL SCOPE: created when `inner_widget()` is called, destroyed on return
        APP_THEME = "high-contrast-local"
        # [B] BUILT-IN SCOPE: `len` is resolved from Python's `builtins` module
        print(f"    [L - Local]     inner_widget sees APP_THEME = {APP_THEME!r} (len={len(APP_THEME)})")

    inner_widget()
    print(f"  [E - Enclosing] outer_dashboard sees APP_THEME = {APP_THEME!r}")


def read_global_without_shadowing() -> None:
    """When no Local or Enclosing `APP_THEME` exists, Python falls back to Global."""
    print(f"  [G - Global]    read_global sees APP_THEME     = {APP_THEME!r}")


def main() -> None:
    print("=== 1. Demonstrating the LEGB Name Resolution Hierarchy ===")
    outer_dashboard()
    read_global_without_shadowing()
    print(f"  [Module Root]   Global APP_THEME is still      = {APP_THEME!r}")

    print("\n=== 2. Inspecting Local vs Global Namespace Dictionaries ===")
    local_sample = 42
    print(f"  'local_sample' in locals()  : {'local_sample' in locals()}")
    print(f"  'local_sample' in globals() : {'local_sample' in globals()}")
    print(f"  'APP_THEME'    in globals() : {'APP_THEME' in globals()}")


if __name__ == "__main__":
    main()
```

---

### Example 2: The `UnboundLocalError` Trap & The `global` Keyword
File: `example_02_unbound_local_error_and_global.py`

```python
request_counter = 100


def buggy_increment() -> None:
    """
    Raises `UnboundLocalError`!
    Because `request_counter += 1` assigns to `request_counter`, Python marks
    `request_counter` as a LOCAL variable for the entire function at compile time.
    """
    print(request_counter)  # Tries to read uninitialized local `request_counter`!
    request_counter += 1


def increment_with_global() -> int:
    """Explicitly tells Python that `request_counter` refers to the module global."""
    global request_counter
    request_counter += 1
    return request_counter


def increment_pure(current_count: int) -> int:
    """Preferred production pattern: pass state in and return new state (no `global`)."""
    return current_count + 1


def main() -> None:
    print("=== 1. Catching the Compile-Time `UnboundLocalError` Trap ===")
    try:
        buggy_increment()
    except UnboundLocalError as err:
        print(f"  Caught expected UnboundLocalError: {err}")

    print("\n=== 2. Rebinding Module State with `global` ===")
    print(f"  Before `increment_with_global()` : request_counter = {request_counter}")
    increment_with_global()
    increment_with_global()
    print(f"  After 2 calls                    : request_counter = {request_counter}")

    print("\n=== 3. Pure Function Alternative (No Global Mutation) ===")
    clean_count = increment_pure(request_counter)
    print(f"  Pure return value                : {clean_count} (global still {request_counter})")


if __name__ == "__main__":
    main()
```

---

### Example 3: The `nonlocal` Keyword & Stateful Closures (Extended Variable Lifetime)
File: `example_03_nonlocal_and_closure_state.py`

```python
from typing import Callable


def make_rate_limiter(max_calls: int) -> Callable[[str], str]:
    """
    Return a closure that tracks `remaining_calls` in its enclosing scope.
    Even after `make_rate_limiter` returns, `remaining_calls` stays alive in a cell!
    """
    remaining_calls = max_calls

    def call_api(endpoint: str) -> str:
        nonlocal remaining_calls
        if remaining_calls <= 0:
            return f"429 Too Many Requests: {endpoint} blocked (0 remaining)"
        remaining_calls -= 1
        return f"200 OK: {endpoint} (remaining quota: {remaining_calls})"

    return call_api


def demonstrate_block_scope_leak() -> None:
    """Show that `if` and `for` blocks share the function's local scope."""
    if True:
        leaked_from_if = "I was defined inside an `if` block"
    for loop_item in ("alpha", "beta", "gamma"):
        pass

    print(f"  Accessible after `if`  : {leaked_from_if!r}")
    print(f"  Accessible after `for` : loop_item = {loop_item!r}")


def main() -> None:
    print("=== 1. Stateful Closure with `nonlocal` (Extended Lifetime) ===")
    limiter = make_rate_limiter(2)
    print(f"  Call 1 : {limiter('/v1/pay')}")
    print(f"  Call 2 : {limiter('/v1/pay')}")
    print(f"  Call 3 : {limiter('/v1/pay')}")
    # Inspect the closure cell that keeps `remaining_calls` alive:
    cell_val = limiter.__closure__[0].cell_contents
    print(f"  Closure cell contents  : remaining_calls = {cell_val}")

    print("\n=== 2. Loops and `if` Blocks Do NOT Create a Separate Scope ===")
    demonstrate_block_scope_leak()


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_legb_rule_and_lifetime.py`)
```text
=== 1. Demonstrating the LEGB Name Resolution Hierarchy ===
    [L - Local]     inner_widget sees APP_THEME = 'high-contrast-local' (len=19)
  [E - Enclosing] outer_dashboard sees APP_THEME = 'solarized-enclosing'
  [G - Global]    read_global sees APP_THEME     = 'dark-global'
  [Module Root]   Global APP_THEME is still      = 'dark-global'

=== 2. Inspecting Local vs Global Namespace Dictionaries ===
  'local_sample' in locals()  : True
  'local_sample' in globals() : False
  'APP_THEME'    in globals() : True
```

### Output — Example 2 (`example_02_unbound_local_error_and_global.py`)
```text
=== 1. Catching the Compile-Time `UnboundLocalError` Trap ===
  Caught expected UnboundLocalError: cannot access local variable 'request_counter' where it is not associated with a value

=== 2. Rebinding Module State with `global` ===
  Before `increment_with_global()` : request_counter = 100
  After 2 calls                    : request_counter = 102

=== 3. Pure Function Alternative (No Global Mutation) ===
  Pure return value                : 103 (global still 102)
```

### Output — Example 3 (`example_03_nonlocal_and_closure_state.py`)
```text
=== 1. Stateful Closure with `nonlocal` (Extended Lifetime) ===
  Call 1 : 200 OK: /v1/pay (remaining quota: 1)
  Call 2 : 200 OK: /v1/pay (remaining quota: 0)
  Call 3 : 429 Too Many Requests: /v1/pay blocked (0 remaining)
  Closure cell contents  : remaining_calls = 0

=== 2. Loops and `if` Blocks Do NOT Create a Separate Scope ===
  Accessible after `if`  : 'I was defined inside an `if` block'
  Accessible after `for` : loop_item = 'gamma'
```

---

## 7. Code Explanation

1. **Shadowing Without Overwriting (`example_01`):** Assigning `APP_THEME = "high-contrast-local"` inside `inner_widget` creates a **new local variable** that temporarily shadows the outer `APP_THEME` names; it does not overwrite `outer_dashboard`'s or the module's `APP_THEME`.
2. **`UnboundLocalError` (`example_02`):** Even though `print(request_counter)` appears *before* `request_counter += 1`, Python's compiler already classified `request_counter` as a local variable for the whole function body of `buggy_increment`.
3. **Closure Cell Inspection (`example_03`):** `limiter.__closure__[0].cell_contents` reveals the live integer `0` stored inside the closure cell after `make_rate_limiter(2)` has returned.

---

## 8. Common Mistakes

1. **Shadowing Built-in Names (`list = [1, 2, 3]`, `id = 5`, `str = "abc"`, `sum = 0`):**
   - Assigning a variable named `list` or `sum` in Local or Global scope shadows the built-in `list()` or `sum()` function (because **L** and **G** are searched before **B** in LEGB!). Later calling `list("hello")` raises `TypeError: 'list' object is not callable`.
2. **Thinking `global` is needed to mutate a global list or dictionary in-place:**
   - Calling `GLOBAL_LIST.append(10)` or `GLOBAL_DICT["k"] = "v"` inside a function **does NOT require `global`**, because `.append()` and `["k"] =` mutate the object without rebinding the variable name `GLOBAL_LIST`. You only need `global` when *reassigning* the name itself (`GLOBAL_LIST = []`).
3. **Assuming a variable initialized inside an `if` branch always exists if the `if` condition was `False`:**
   - Because Python has no block declaration separate from assignment, if `if False: result = 10` is skipped, reading `result` after the `if` raises `UnboundLocalError`. Always initialize `result = None` before conditional branches.

---

## 9. Practice Questions

1. **Easy — Trace LEGB Resolution:**
   Write a script with a global `TAX = 0.05`, an outer function defining `TAX = 0.12`, and an inner function defining `TAX = 0.18`. Have each level print its `TAX`, then delete the local assignment in the inner function and observe how it falls back to `0.12`.

2. **Medium — Running Average Accumulator with `nonlocal`:**
   Write `make_running_average()` that returns a closure `add_sample(val: float) -> float`. Use `nonlocal count, total` so each call updates both the running count and running sum and returns the updated mean.

3. **Hard — Bank Account Factory Using Closures (Multiple Inner Functions):**
   Write `create_wallet(initial_balance: float)` that stores `balance` in an enclosing variable and returns a dictionary of three closures: `{"deposit": ..., "withdraw": ..., "get_balance": ...}` that share and update the same `nonlocal balance`.

---

## 10. Interview Questions

### Q1: Why does `GLOBAL_CACHE["user"] = "Aarav"` work inside a function without the `global` keyword, whereas `GLOBAL_COUNT += 1` raises `UnboundLocalError`?
**Answer:**
- `GLOBAL_CACHE["user"] = "Aarav"` calls `GLOBAL_CACHE.__setitem__("user", "Aarav")`. It only **reads** the variable name `GLOBAL_CACHE` (via LEGB lookup) and mutates the dictionary object in-place; it does **not** assign a new object reference to the name `GLOBAL_CACHE`.
- `GLOBAL_COUNT += 1` expands to `GLOBAL_COUNT = GLOBAL_COUNT + 1`, which **assigns** to the name `GLOBAL_COUNT`. Any assignment to a bare variable name inside a function makes that name local to the function at compile time unless declared `global` or `nonlocal`.

### Q2: What is the difference between `global` and `nonlocal` in Python?
**Answer:**
- **`global`** binds a variable name to the **module-level (Global) namespace**, even if there are enclosing functions in between. If the global variable does not exist yet, assigning to it creates it at the module level.
- **`nonlocal`** (introduced in Python 3) binds a variable name to the nearest **enclosing function scope** (excluding the global module scope). The variable **must already exist** in an enclosing function scope at compile time, or Python raises a `SyntaxError`.

### Q3: Does a list comprehension `[x for x in range(5)]` leak the loop variable `x` into the surrounding scope in Python 3?
**Answer:**
**No** in Python 3 (unlike Python 2, where `[x for x in range(5)]` leaked `x`!). In Python 3, list/dict/set comprehensions and generator expressions execute inside their own implicit **local function scope**, so `x` does not leak out. (Note: the walrus operator `:=` inside a comprehension *intentionally* binds into the enclosing scope, and a regular `for x in range(5):` loop *does* bind `x` in the surrounding scope.)
