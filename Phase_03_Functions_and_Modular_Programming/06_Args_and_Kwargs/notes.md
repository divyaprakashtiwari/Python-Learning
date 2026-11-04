# Phase 3 — Topic 06: `*args` and `**kwargs`

## 1. Introduction

Sometimes you don't know in advance how many arguments a caller will pass to your function—think of `print("a", "b", "c", "d")` or a generic logging decorator that wraps any function in your codebase.

Python solves this with **variadic parameters**:
- **`*args` (Variable Positional Parameters):** Packs any number of extra positional arguments into a **`tuple`**.
- **`**kwargs` (Variable Keyword Parameters):** Packs any number of extra keyword arguments (`key=value`) into a **`dict`**.

*(Note: The names `args` and `kwargs` are universal Python conventions, but the asterisks `*` and `**` are the actual syntax—`*item_prices` or `**columns` work identically and are often more descriptive!)*

---

## 2. Why is it used?

- **Flexible Aggregators & Builders:** Functions like `max()`, `print()`, `os.path.join()`, or custom SQL/HTML builders can accept 1, 5, or 100 inputs naturally without forcing the caller to wrap arguments in a list first.
- **Transparent Argument Forwarding (Decorators & Subclassing):** A wrapper function or subclass `__init__` can accept `(*args, **kwargs)` and forward them directly to the wrapped function (`func(*args, **kwargs)`) or parent class (`super().__init__(*args, **kwargs)`) without hardcoding the inner signature.
- **Extensible Plugin & Event Hooks:** Event handlers can accept `**kwargs` so future versions of a framework can pass additional metadata without breaking older plugins.

---

## 3. Syntax

```python
# 1. Packing variable positional arguments into a tuple (`*args`)
def sum_all(*numbers: float) -> float:
    # Inside the function, `numbers` is a `tuple[float, ...]`
    return sum(numbers)

# 2. Packing variable keyword arguments into a dict (`**kwargs`)
def build_tag(tag_name: str, **attributes: object) -> str:
    # Inside the function, `attributes` is a `dict[str, object]`
    ...

# 3. Canonical 5-Part Parameter Order in a Python Signature:
def full_signature(
    pos_only, /,           # 1. Positional-only parameters
    standard,              # 2. Positional-or-keyword parameters
    *args,                 # 3. Variable positional tuple
    kw_only=True,          # 4. Keyword-only parameters
    **kwargs,              # 5. Variable keyword dictionary (MUST be last!)
):
    pass
```

---

## 4. Explanation (Step-by-Step)

### Step 1: Packing vs Unpacking (`*` and `**` Dual Meaning)
The `*` and `**` operators do opposite jobs depending on where they appear:

| Location | `*` Operator | `**` Operator |
| :--- | :--- | :--- |
| **In `def` header (Packing)** | Packs remaining positional arguments into a **`tuple`**. | Packs remaining keyword arguments into a **`dict`**. |
| **In function call (Unpacking)** | Unpacks any iterable (`list`, `tuple`, `set`) into separate positional arguments. | Unpacks a mapping (`dict`) into separate `key=value` keyword arguments. |

### Step 2: Canonical 5-Part Parameter Order
If you combine multiple parameter kinds in a single `def` header, Python enforces this exact left-to-right order:
1. Positional-only parameters (`a, b, /`)
2. Standard positional-or-keyword parameters (`c, d=1`)
3. Variable positional parameter (`*args`) — *or bare `*` if no variable positional args are accepted*
4. Keyword-only parameters (`e, f=2`)
5. Variable keyword parameter (`**kwargs`) — **must always be the very last parameter**

### Step 3: Forwarding `(*args, **kwargs)`
When writing a wrapper function:
```python
def wrapper(*args, **kwargs):
    # `args` is a tuple; `kwargs` is a dict
    return target_function(*args, **kwargs)  # Unpacks them right back out!
```
In the `def wrapper(*args, **kwargs):` line, `*` and `**` **pack** all incoming arguments. In the `target_function(*args, **kwargs)` call, `*` and `**` **unpack** them back into individual positional and keyword arguments.

---

## 5. Minimum 3 Examples

### Example 1: Variable Positional Arguments (`*args` Tuple Packing & `*` Unpacking)
File: `example_01_variable_positional_args.py`

```python
def calculate_invoice_total(
    tax_rate: float,
    *item_prices: float,
) -> tuple[float, float, float]:
    """
    Calculate (subtotal, tax_amount, grand_total) for 0 or more item prices.
    `tax_rate` is a required first parameter; `*item_prices` packs the rest into a tuple.
    """
    print(f"    [Inside] item_prices={item_prices} (type: {type(item_prices).__name__})")
    subtotal = sum(item_prices)
    tax_amount = round(subtotal * tax_rate, 2)
    grand_total = round(subtotal + tax_amount, 2)
    return subtotal, tax_amount, grand_total


def main() -> None:
    print("=== 1. Calling `*item_prices` with Varying Counts of Arguments ===")
    sub_1, tax_1, total_1 = calculate_invoice_total(0.18, 499.0, 1299.0, 200.0)
    print(f"  3 items -> subtotal={sub_1:.2f}, tax={tax_1:.2f}, total={total_1:.2f}")

    sub_0, tax_0, total_0 = calculate_invoice_total(0.18)
    print(f"  0 items -> subtotal={sub_0:.2f}, tax={tax_0:.2f}, total={total_0:.2f}")

    print("\n=== 2. Unpacking a List into `*item_prices` Using `*cart_prices` ===")
    cart_prices = [150.0, 350.0, 500.0, 250.0]
    sub_2, tax_2, total_2 = calculate_invoice_total(0.12, *cart_prices)
    print(f"  Unpacked list -> subtotal={sub_2:.2f}, tax={tax_2:.2f}, total={total_2:.2f}")


if __name__ == "__main__":
    main()
```

---

### Example 2: Variable Keyword Arguments (`**kwargs` Dict Packing) & Canonical Order
File: `example_02_variable_keyword_kwargs.py`

```python
def build_sql_insert(
    table_name: str,
    /,
    *tags: str,
    ignore_duplicates: bool = False,
    **columns: object,
) -> str:
    """
    Demonstrate all 5 parameter categories in a single signature:
      1. `table_name`        : Positional-only (before `/`)
      2. `*tags`             : Variable positional tuple
      3. `ignore_duplicates` : Keyword-only with default (after `*tags`)
      4. `**columns`         : Variable keyword dictionary
    """
    verb = "INSERT OR IGNORE INTO" if ignore_duplicates else "INSERT INTO"
    col_names = ", ".join(columns.keys())
    col_vals = ", ".join(repr(v) for v in columns.values())
    comment = f"/* tags: {', '.join(tags)} */ " if tags else ""
    return f"{comment}{verb} {table_name} ({col_names}) VALUES ({col_vals});"


def main() -> None:
    print("=== 1. Inspecting `**columns` Packing & Full Signature Order ===")
    query_1 = build_sql_insert(
        "users",
        "audit",
        "v2",
        ignore_duplicates=True,
        id=101,
        username="aarav_dev",
        active=True,
    )
    print(f"  Generated SQL 1 :\n    {query_1}")

    query_2 = build_sql_insert(
        "products",
        sku="LAP-900",
        price=74999.50,
        in_stock=15,
    )
    print(f"  Generated SQL 2 :\n    {query_2}")


if __name__ == "__main__":
    main()
```

---

### Example 3: Transparent Argument Forwarding (`*args, **kwargs`) in Wrapper Functions
File: `example_03_forwarding_args_and_kwargs.py`

```python
from typing import Any, Callable


def call_with_telemetry(
    func: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Log the function call signature, forward `*args, **kwargs`, and return result."""
    pos_repr = [repr(a) for a in args]
    kw_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
    all_args_str = ", ".join(pos_repr + kw_repr)

    print(f"  [TELEMETRY] Calling {func.__name__}({all_args_str})")
    result = func(*args, **kwargs)
    print(f"  [TELEMETRY] {func.__name__} returned -> {result!r}")
    return result


def compute_shipping(weight_kg: float, zone: str, *, express: bool = False) -> float:
    """Target business function with positional and keyword-only parameters."""
    base = weight_kg * (120.0 if zone == "INTL" else 45.0)
    return base * (1.5 if express else 1.0)


def main() -> None:
    print("=== Forwarding `*args` and `**kwargs` Through a Generic Wrapper ===")
    cost_std = call_with_telemetry(compute_shipping, 2.5, "DOMESTIC")
    print(f"  Final Standard Cost : INR {cost_std:.2f}\n")

    cost_exp = call_with_telemetry(compute_shipping, 4.0, zone="INTL", express=True)
    print(f"  Final Express Cost  : INR {cost_exp:.2f}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_variable_positional_args.py`)
```text
=== 1. Calling `*item_prices` with Varying Counts of Arguments ===
    [Inside] item_prices=(499.0, 1299.0, 200.0) (type: tuple)
  3 items -> subtotal=1998.00, tax=359.64, total=2357.64
    [Inside] item_prices=() (type: tuple)
  0 items -> subtotal=0.00, tax=0.00, total=0.00

=== 2. Unpacking a List into `*item_prices` Using `*cart_prices` ===
    [Inside] item_prices=(150.0, 350.0, 500.0, 250.0) (type: tuple)
  Unpacked list -> subtotal=1250.00, tax=150.00, total=1400.00
```

### Output — Example 2 (`example_02_variable_keyword_kwargs.py`)
```text
=== 1. Inspecting `**columns` Packing & Full Signature Order ===
  Generated SQL 1 :
    /* tags: audit, v2 */ INSERT OR IGNORE INTO users (id, username, active) VALUES (101, 'aarav_dev', True);
  Generated SQL 2 :
    INSERT INTO products (sku, price, in_stock) VALUES ('LAP-900', 74999.5, 15);
```

### Output — Example 3 (`example_03_forwarding_args_and_kwargs.py`)
```text
=== Forwarding `*args` and `**kwargs` Through a Generic Wrapper ===
  [TELEMETRY] Calling compute_shipping(2.5, 'DOMESTIC')
  [TELEMETRY] compute_shipping returned -> 112.5
  Final Standard Cost : INR 112.50

  [TELEMETRY] Calling compute_shipping(4.0, zone='INTL', express=True)
  [TELEMETRY] compute_shipping returned -> 720.0
  Final Express Cost  : INR 720.00
```

---

## 7. Code Explanation

1. **Zero Extra Arguments (`example_01`):** Calling `calculate_invoice_total(0.18)` with no extra arguments binds `item_prices` to the empty tuple `()`. It does not raise an error.
2. **List Unpacking (`example_01`):** Passing `cart_prices` directly (`calculate_invoice_total(0.12, cart_prices)`) would pack the list itself as a single element inside a 1-tuple `([150.0, ...],)` and fail inside `sum()`. Prefixing `*cart_prices` unpacks the 4 floats as separate positional arguments.
3. **Positional-Only + `**kwargs` (`example_02`):** Because `table_name` is before `/`, a caller could even pass a column named `table_name="archived"` inside `**columns` without colliding with the first parameter!
4. **Transparent Forwarding (`example_03`):** `call_with_telemetry` knows nothing about `weight_kg`, `zone`, or `express`, yet forwards them seamlessly to `compute_shipping`.

---

## 8. Common Mistakes

1. **Forgetting the `*` when forwarding `args` to another `*args` function:**
   - Inside `def wrapper(*args):`, the variable `args` is a `tuple`. If you call `target(args)` instead of `target(*args)`, you pass a single tuple object as the first argument instead of unpacking the elements!
2. **Putting parameters after `**kwargs`:**
   - `def func(**kwargs, debug=False):` is a `SyntaxError`. `**kwargs` must always be the very last parameter in a function definition.
3. **Overusing `**kwargs` when explicit keyword arguments are known:**
   - Accepting `**kwargs` everywhere hides parameter names from IDE autocomplete and static type checkers (`mypy`/`pyright`). Only use `**kwargs` when keys are genuinely dynamic or being forwarded to another function.

---

## 9. Practice Questions

1. **Easy — Flexible Path Joiner:**
   Write a function `build_url(base_domain: str, *path_segments: str, https: bool = True) -> str` that joins `base_domain` and any number of `path_segments` with `"/"` (stripping leading/trailing slashes from segments) and prefixes `"https://"` or `"http://"`.

2. **Medium — HTML Element Builder (`*children` and `**attrs`):**
   Write `html_element(tag: str, *children: str, **attrs: object) -> str` that renders an HTML tag. Note that `class` is a reserved keyword in Python, so if `attrs` contains `"class_"`, render it as `class="..."`. Example: `html_element("div", "Hello", "World", id="main", class_="card")` -> `'<div id="main" class="card">HelloWorld</div>'`.

3. **Hard — Retry Wrapper Using `*args` and `**kwargs`:**
   Write `retry_call(func, *args, max_attempts: int = 3, **kwargs)` that calls `func(*args, **kwargs)` up to `max_attempts` times if `func` raises a `ValueError`, returning the result on success or re-raising the last `ValueError` after `max_attempts`.

---

## 10. Interview Questions

### Q1: What are the runtime types of `args` and `kwargs` inside `def func(*args, **kwargs):`?
**Answer:**
- `args` is always a **`tuple`** (specifically `()` if no extra positional arguments were passed).
- `kwargs` is always a **`dict[str, Any]`** (specifically `{}` if no extra keyword arguments were passed).

### Q2: Why is `args` packed into an immutable `tuple` instead of a mutable `list`?
**Answer:**
1. **Performance:** Tuples are fixed-size and faster for CPython to allocate on function entry than dynamic lists.
2. **Safety:** Prevents accidental in-place mutation of the argument sequence when inspecting or forwarding `args`.

### Q3: Suppose `def f(x, /, **kwargs):` is defined. What happens when you call `f(10, x=20)`?
**Answer:**
It succeeds without error!Inside `f`, the positional-only parameter `x` is bound to `10`, and `kwargs` is bound to `{'x': 20}`. Because `x` is positional-only (`/`), its name is not reserved in the keyword argument namespace, so `x=20` is cleanly captured by `**kwargs` instead of raising `TypeError: got multiple values for argument 'x'`.
