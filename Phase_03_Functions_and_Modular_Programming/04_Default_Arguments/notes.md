# Phase 3 — Topic 04: Default Arguments

## 1. Introduction

**Default arguments** allow a function parameter to assume a predefined fallback value whenever the caller omits that argument at the call site.

For example, in `def build_connection_url(host: str, port: int = 5432):`, the parameter `port` is optional—calling `build_connection_url("localhost")` automatically sets `port` to `5432`, while calling `build_connection_url("localhost", 5433)` overrides the default.

While default arguments make APIs concise and beginner-friendly, they also hide one of the most famous interview pitfalls in Python: **default values are evaluated only ONCE when the `def` statement is executed, not re-evaluated on every function call.**

---

## 2. Why is it used?

- **Clean Call Sites (Convention over Configuration):** Callers only need to supply the core required arguments (`open("data.txt")`) while still having the flexibility to override optional parameters (`open("data.txt", mode="w", encoding="utf-8")`).
- **Backward-Compatible API Evolution:** You can add new parameters to an existing production function without breaking hundreds of existing call sites—as long as the new parameters have sensible default values.
- **Selective Keyword Overrides:** When a function has 5 optional parameters with defaults, a caller can override just the 5th parameter by name (`timeout_sec=5`) without repeating the first 4 defaults.

---

## 3. Syntax

```python
# 1. Required parameters MUST come before default parameters
def connect(host: str, port: int = 5432, use_ssl: bool = True) -> str:
    ...

# 2. SAFE pattern for mutable default arguments (using `None` sentinel)
def add_item(item: str, bucket: list[str] | None = None) -> list[str]:
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

---

## 4. Explanation (Step-by-Step)

### Step 1: Parameter Ordering Rule
In any function signature, **non-default (required) parameters must appear before default (optional) parameters**:
- Valid: `def f(a, b, c=10, d=20):`
- Invalid (`SyntaxError: non-default argument follows default argument`): `def f(a=10, b):`
  *(Exception: keyword-only parameters after `*` can mix required and default parameters freely because they are never matched positionally.)*

### Step 2: When Are Default Values Evaluated? (Definition Time!)
When Python executes a `def` block:
1. It evaluates every default expression (`5432`, `True`, `[]`, `time.monotonic()`) **right then and there** once.
2. It stores those resulting objects in a tuple attribute on the function object called **`func.__defaults__`** (and a dict called **`func.__kwdefaults__`** for keyword-only defaults).
3. Whenever the function is called with an omitted argument, Python simply binds the parameter name to the pre-existing object sitting inside `func.__defaults__`.

### Step 3: The Mutable Default Argument Trap (`tags=[]` vs `tags=None`)
Because `func.__defaults__` is created once at definition time:
- If a default value is **mutable** (`def append_tag(tag, tags=[]):`), the **exact same list object** inside `__defaults__` is reused and mutated across every single call that omits `tags`!
- **The Fix:** Always default mutable parameters to `None` (`tags: list[str] | None = None`) and initialize a brand-new list inside the function body (`if tags is None: tags = []`).

---

## 5. Minimum 3 Examples

### Example 1: Optional Parameters with Default Values & Ordering Rules
File: `example_01_basic_default_arguments.py`

```python
def build_connection_url(
    host: str,
    database: str,
    port: int = 5432,
    use_ssl: bool = True,
    timeout_sec: int = 30,
) -> str:
    """Build a PostgreSQL connection string with sensible production defaults."""
    ssl_mode = "require" if use_ssl else "disable"
    return (
        f"postgresql://{host}:{port}/{database}"
        f"?sslmode={ssl_mode}&connect_timeout={timeout_sec}"
    )


def main() -> None:
    print("=== 1. Using All Default Arguments ===")
    url_default = build_connection_url("db.internal.local", "analytics")
    print(f"  Default call          : {url_default}")

    print("\n=== 2. Overriding Defaults Positionally ===")
    url_custom_port = build_connection_url("localhost", "dev_db", 5433, False)
    print(f"  Positional override   : {url_custom_port}")

    print("\n=== 3. Overriding a Specific Default by Keyword ===")
    # Skip `port` and `use_ssl` defaults and override only `timeout_sec`
    url_custom_timeout = build_connection_url(
        "db.internal.local",
        "analytics",
        timeout_sec=5,
    )
    print(f"  Keyword skip override : {url_custom_timeout}")


if __name__ == "__main__":
    main()
```

---

### Example 2: The Mutable Default Argument Trap (`items=[]` vs `items=None`)
File: `example_02_mutable_default_argument_trap.py`

```python
def append_tag_buggy(tag: str, tags: list[str] = []) -> list[str]:
    """BUGGY: Default list `[]` is created once at `def` time and shared across calls!"""
    tags.append(tag)
    return tags


def append_tag_safe(tag: str, tags: list[str] | None = None) -> list[str]:
    """SAFE: Uses immutable `None` sentinel and creates a fresh list per call."""
    if tags is None:
        tags = []
    tags.append(tag)
    return tags


def main() -> None:
    print("=== 1. The Mutable Default Argument Trap (`tags=[]`) ===")
    print(f"  Before any call, __defaults__ = {append_tag_buggy.__defaults__}")
    call_1 = append_tag_buggy("python")
    print(f"  Call 1 (`append_tag_buggy('python')`)  -> {call_1}")
    call_2 = append_tag_buggy("backend")
    print(f"  Call 2 (`append_tag_buggy('backend')`) -> {call_2}  (LEAKED from Call 1!)")
    print(f"  After 2 calls,  __defaults__ = {append_tag_buggy.__defaults__}")
    print(f"  Are `call_1` and `call_2` the exact same list? {call_1 is call_2}")

    print("\n=== 2. The Canonical Fix (`tags: list[str] | None = None`) ===")
    safe_1 = append_tag_safe("python")
    print(f"  Call 1 (`append_tag_safe('python')`)   -> {safe_1}")
    safe_2 = append_tag_safe("backend")
    print(f"  Call 2 (`append_tag_safe('backend')`)  -> {safe_2}  (Clean fresh list!)")
    print(f"  Are `safe_1` and `safe_2` the exact same list? {safe_1 is safe_2}")

    # Passing an explicit list still works as expected
    existing = ["urgent"]
    safe_3 = append_tag_safe("hotfix", existing)
    print(f"  Call 3 (with existing list)            -> {safe_3}")


if __name__ == "__main__":
    main()
```

---

### Example 3: Dynamic Default Evaluation Time (`datetime` / Memoization Cache)
File: `example_03_evaluation_time_and_kwdefaults.py`

```python
import time


def log_with_frozen_default(
    message: str,
    timestamp: float = time.monotonic(),
) -> str:
    """PITFALL: `time.monotonic()` runs ONCE when `def` is executed!"""
    return f"[t={timestamp:.4f}] {message}"


def log_with_dynamic_default(
    message: str,
    timestamp: float | None = None,
) -> str:
    """CORRECT: Evaluates `time.monotonic()` fresh when `timestamp` is omitted."""
    if timestamp is None:
        timestamp = time.monotonic()
    return f"[t={timestamp:.4f}] {message}"


def fibonacci_cached(n: int, _cache: dict[int, int] = {0: 0, 1: 1}) -> int:
    """Intentional mutable default `_cache` for O(n) memoization."""
    if n not in _cache:
        _cache[n] = fibonacci_cached(n - 1) + fibonacci_cached(n - 2)
    return _cache[n]


def main() -> None:
    print("=== 1. Frozen Timestamp Default Pitfall ===")
    first_frozen = log_with_frozen_default("Server starting")
    time.sleep(0.02)
    second_frozen = log_with_frozen_default("Server ready (20ms later)")
    print(f"  {first_frozen}")
    print(f"  {second_frozen}  <-- IDENTICAL timestamp!")

    print("\n=== 2. Dynamic Timestamp Default (`None` Sentinel) ===")
    first_dyn = log_with_dynamic_default("Server starting")
    time.sleep(0.02)
    second_dyn = log_with_dynamic_default("Server ready (20ms later)")
    print(f"  {first_dyn}")
    print(f"  {second_dyn}  <-- Updated timestamp!")

    print("\n=== 3. Intentional Mutable Default for Memoization ===")
    print(f"  fibonacci_cached(10) = {fibonacci_cached(10)}")
    print(f"  fibonacci_cached(20) = {fibonacci_cached(20)}")
    print(f"  Cached keys count    = {len(fibonacci_cached.__defaults__[0])}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_basic_default_arguments.py`)
```text
=== 1. Using All Default Arguments ===
  Default call          : postgresql://db.internal.local:5432/analytics?sslmode=require&connect_timeout=30

=== 2. Overriding Defaults Positionally ===
  Positional override   : postgresql://localhost:5433/dev_db?sslmode=disable&connect_timeout=30

=== 3. Overriding a Specific Default by Keyword ===
  Keyword skip override : postgresql://db.internal.local:5432/analytics?sslmode=require&connect_timeout=5
```

### Output — Example 2 (`example_02_mutable_default_argument_trap.py`)
```text
=== 1. The Mutable Default Argument Trap (`tags=[]`) ===
  Before any call, __defaults__ = ([],)
  Call 1 (`append_tag_buggy('python')`)  -> ['python']
  Call 2 (`append_tag_buggy('backend')`) -> ['python', 'backend']  (LEAKED from Call 1!)
  After 2 calls,  __defaults__ = (['python', 'backend'],)
  Are `call_1` and `call_2` the exact same list? True

=== 2. The Canonical Fix (`tags: list[str] | None = None`) ===
  Call 1 (`append_tag_safe('python')`)   -> ['python']
  Call 2 (`append_tag_safe('backend')`)  -> ['backend']  (Clean fresh list!)
  Are `safe_1` and `safe_2` the exact same list? False
  Call 3 (with existing list)            -> ['urgent', 'hotfix']
```

### Output — Example 3 (`example_03_evaluation_time_and_kwdefaults.py`)
```text
=== 1. Frozen Timestamp Default Pitfall ===
  [t=339741.6300] Server starting
  [t=339741.6300] Server ready (20ms later)  <-- IDENTICAL timestamp!

=== 2. Dynamic Timestamp Default (`None` Sentinel) ===
  [t=339741.6502] Server starting
  [t=339741.6706] Server ready (20ms later)  <-- Updated timestamp!

=== 3. Intentional Mutable Default for Memoization ===
  fibonacci_cached(10) = 55
  fibonacci_cached(20) = 6765
  Cached keys count    = 21
```

---

## 7. Code Explanation

1. **Selective Override (`example_01`):** `build_connection_url("db.internal.local", "analytics", timeout_sec=5)` leaves `port=5432` and `use_ssl=True` untouched while overriding only the final parameter `timeout_sec`.
2. **`__defaults__` Inspection (`example_02`):** `append_tag_buggy.__defaults__` starts as `([],)` before any call and mutates into `(['python', 'backend'],)` after two calls, proving that the default list lives inside the function object's `__defaults__` tuple.
3. **Frozen Timestamp vs Dynamic Timestamp (`example_03`):** `timestamp: float = time.monotonic()` runs `time.monotonic()` once when the module loads. Even if the server runs for 30 days, every call that omits `timestamp` gets the exact module-import timestamp! Using `None` fixes it.

---

## 8. Common Mistakes

1. **Using `[]`, `{}`, or `set()` as a default parameter value:**
   - Always use `None` as the default and create the mutable container inside the function body.
2. **Using `tags = tags or []` instead of `if tags is None: tags = []`:**
   - What if the caller intentionally passes an empty list `my_list = []` expecting your function to mutate `my_list` in-place? Because `[]` is falsy, `tags = tags or []` discards the caller's `my_list` and creates a different list! Always test `if tags is None:`.
3. **Calling functions like `datetime.now()`, `uuid.uuid4()`, or `random.randint()` in a default parameter expression:**
   - Those calls execute **once** at function definition time, so every invocation receives the exact same timestamp, UUID, or random number.

---

## 9. Practice Questions

1. **Easy — Greeting Formatter with Default Punctuation:**
   Write a function `format_greeting(name: str, greeting: str = "Hello", punctuation: str = "!") -> str` and test calling it with 1, 2, and 3 arguments.

2. **Medium — Safe User Role Assigner (Fixing Mutable Default):**
   Write `assign_role(username: str, role: str = "viewer", permissions: dict[str, list[str]] | None = None) -> dict[str, list[str]]` that safely initializes a new dictionary when `permissions` is `None`, appends `role` to `permissions[username]`, and returns the dictionary. Verify that two separate calls do not share state.

3. **Hard — Custom Sentinel Object When `None` Is a Valid Argument:**
   Sometimes `None` itself is a meaningful value a caller wants to pass (e.g., setting a cache key's value to `None`), so `None` cannot be used to detect an omitted argument. Create a module-level sentinel `_MISSING = object()` and write `set_config(key: str, value: object = _MISSING)` that distinguishes `set_config("theme")` (omitted -> defaults to `"dark"`) from `set_config("theme", None)` (explicitly set to `None`).

---

## 10. Interview Questions

### Q1: What is the output of calling `def f(x, items=[]): items.append(x); return items` three times: `f(1)`, `f(2)`, `f(3)`? Why?
**Answer:**
- `f(1)` returns `[1]`
- `f(2)` returns `[1, 2]`
- `f(3)` returns `[1, 2, 3]`
All three return references to the **exact same list** (`[1, 2, 3]`). Python evaluates default argument expressions **once** when the `def` statement is executed and stores the resulting object in `f.__defaults__`. Every call that omits `items` binds `items` to `f.__defaults__[0]`.

### Q2: Why does `tags = tags or []` have a subtle bug compared to `if tags is None: tags = []`?
**Answer:**
In Python, an empty list `[]` is **falsy** (`bool([]) == False`). If a caller passes their own empty list `caller_list = []; append_tag("v1", caller_list)` expecting `caller_list` to be populated in-place, `tags = tags or []` evaluates `[] or []` and creates a **new** list object, leaving `caller_list` empty. Checking `if tags is None:` only creates a new list when the argument was truly omitted (or explicitly `None`).

### Q3: Where does Python store default values for regular parameters vs keyword-only parameters?
**Answer:**
- Default values for positional-or-keyword parameters are stored in a `tuple` attribute named **`func.__defaults__`**.
- Default values for keyword-only parameters (those defined after `*` or `*args`) are stored in a `dict` attribute named **`func.__kwdefaults__`** mapping parameter names to their default objects.
