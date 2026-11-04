# Phase 3 — Topic 02: Parameters and Arguments

## 1. Introduction

Developers often use the words **parameter** and **argument** interchangeably, but in computer science and Python documentation they represent two distinct sides of a function call:

- **Parameter (Formal Parameter):** The placeholder variable name listed inside the parentheses of a `def` header (e.g., `def greet(name):` — here `name` is the parameter).
- **Argument (Actual Argument):** The concrete value or object passed into the function when it is called (e.g., `greet("Aarav")` — here `"Aarav"` is the argument).

Understanding how Python binds actual arguments to formal parameters—and how object references behave across function boundaries—is critical for avoiding subtle side-effect bugs in interviews and production code.

---

## 2. Why is it used?

- **Generalization:** Parameters allow a single function implementation to operate on millions of different inputs without rewriting its body.
- **API Safety (`/` and `*`):** Python 3.8+ lets library authors control *how* callers pass arguments—enforcing positional-only (`/`), positional-or-keyword, or keyword-only (`*`) boundaries so APIs remain readable and refactor-safe.
- **Memory Efficiency:** Because Python passes **object references** rather than copying entire arrays or dictionaries on every call, passing a 10-million-element list to a helper function takes $O(1)$ time and $O(1)$ stack space.

---

## 3. Syntax

```python
# 1. Standard formal parameters in definition
def create_invoice(customer_id: int, amount: float) -> str:
    return f"Invoice #{customer_id}: ${amount:.2f}"

# Passing actual arguments at the call site
create_invoice(101, 49.99)


# 2. Full Parameter Boundary Syntax (Python 3.8+, PEP 570 & PEP 3102)
def api_endpoint(
    pos_only_1,
    pos_only_2,
    /,                  # <-- Everything LEFT of `/` is POSITIONAL-ONLY
    standard_param,     # <-- Between `/` and `*` is POSITIONAL-OR-KEYWORD
    *,                  # <-- Everything RIGHT of `*` is KEYWORD-ONLY
    kw_only_flag=False,
):
    pass
```

---

## 4. Explanation (Step-by-Step)

### Step 1: Argument Evaluation Before Call
When Python encounters `schedule_appointment(user.upper(), f"{hour}:00")`, it **evaluates all argument expressions from left to right first** before jumping into the function body.

### Step 2: Binding by Object Reference ("Pass-by-Object-Reference")
People frequently ask: *"Is Python pass-by-value or pass-by-reference?"*
The accurate answer is **Pass-by-Object-Reference** (also called *Call-by-Sharing*):
1. When you call `func(my_var)`, the formal parameter inside `func` becomes a **new local variable name (alias)** pointing to the **exact same object in memory** as `my_var`.
2. **Reassigning** the parameter inside the function (`param = new_value`) only rebinds the local name to a different object—it **never** changes the caller's variable.
3. **Mutating** the object through the parameter (`param.append(x)` or `param[0] = 99`) modifies the shared object in heap memory—which **is** visible to the caller if the object is mutable (`list`, `dict`, `set`).

### Step 3: Parameter Passing Boundaries (`/` and `*`)
| Region in `def` Signature | Syntax Rule | Why Use It? |
| :--- | :--- | :--- |
| Left of `/` | **Positional-Only** | Allows renaming internal parameter names later without breaking callers; prevents clashes with `**kwargs`. |
| Between `/` and `*` | **Positional-or-Keyword** | Default Python behavior; flexible for callers. |
| Right of `*` | **Keyword-Only** | Forces callers to name boolean flags and options explicitly (`instant_settlement=True` instead of a mysterious `True`). |

---

## 5. Minimum 3 Examples

### Example 1: Formal Parameters vs Actual Arguments & Signature Inspection
File: `example_01_parameters_vs_arguments.py`

```python
import inspect


def schedule_appointment(patient_name: str, doctor_name: str, time_slot: str) -> str:
    """Return a formatted appointment confirmation string."""
    # `patient_name`, `doctor_name`, and `time_slot` are FORMAL PARAMETERS
    return f"Confirmed: {patient_name} with Dr. {doctor_name} at {time_slot}"


def main() -> None:
    print("=== 1. Formal Parameters vs Actual Arguments ===")
    # "Aarav", "Mehta", and "10:30 AM" are ACTUAL ARGUMENTS
    confirmation_1 = schedule_appointment("Aarav", "Mehta", "10:30 AM")
    print(f"  Call 1 (Correct Order) : {confirmation_1}")

    # Swapping positional arguments changes which parameter receives which value
    confirmation_2 = schedule_appointment("Mehta", "Aarav", "10:30 AM")
    print(f"  Call 2 (Swapped Order) : {confirmation_2}")

    print("\n=== 2. Passing Variables and Expressions as Arguments ===")
    user = "Priya"
    specialist = "Sharma"
    hour = 14
    # Expressions are evaluated BEFORE being bound to formal parameters
    confirmation_3 = schedule_appointment(
        user.upper(),
        specialist,
        f"{hour}:00 HRS",
    )
    print(f"  Call 3 (Expressions)   : {confirmation_3}")

    print("\n=== 3. Inspecting Formal Parameters at Runtime ===")
    sig = inspect.signature(schedule_appointment)
    print(f"  Function Signature     : {sig}")
    for idx, (param_name, param_obj) in enumerate(sig.parameters.items(), start=1):
        print(
            f"  Param #{idx}: name={param_name!r:<14} | "
            f"annotation={param_obj.annotation.__name__:<4} | "
            f"kind={param_obj.kind.description}"
        )


if __name__ == "__main__":
    main()
```

---

### Example 2: Pass-by-Object-Reference (Immutable vs Mutable Arguments)
File: `example_02_pass_by_object_reference.py`

```python
def try_to_increment_number(score: int) -> int:
    """Reassign an immutable integer parameter inside the function."""
    print(f"    [Inside start] score={score}, id matches caller: True")
    score = score + 10  # Creates a brand-new int object; rebinds local `score`
    print(f"    [Inside after] score={score} (rebound to new int object)")
    return score


def mutate_cart_in_place(cart: list[str], new_item: str) -> None:
    """Mutate the caller's list directly via `.append()`."""
    cart.append(new_item)


def rebind_cart_locally(cart: list[str], new_item: str) -> list[str]:
    """Reassign the local parameter `cart` to a new list without mutating caller."""
    cart = cart + [new_item]  # `+` creates a brand-new list object
    return cart


def main() -> None:
    print("=== 1. Immutable Argument (`int`) - Caller Variable Unchanged ===")
    player_score = 50
    returned_score = try_to_increment_number(player_score)
    print(f"  Caller `player_score` after call : {player_score} (unchanged!)")
    print(f"  Returned value                   : {returned_score}")

    print("\n=== 2. Mutable Argument (`list`) - In-Place Mutation Affects Caller ===")
    shopping_cart = ["Laptop", "Mouse"]
    print(f"  Before `mutate_cart_in_place`    : {shopping_cart}")
    mutate_cart_in_place(shopping_cart, "Keyboard")
    print(f"  After  `mutate_cart_in_place`    : {shopping_cart} (mutated!)")

    print("\n=== 3. Mutable Argument (`list`) - Local Reassignment Does NOT Mutate ===")
    new_cart = rebind_cart_locally(shopping_cart, "Monitor")
    print(f"  Caller `shopping_cart`           : {shopping_cart} (unchanged!)")
    print(f"  Returned `new_cart`              : {new_cart}")

    print("\n=== 4. Defensive Copying at Call Site (`cart.copy()`) ===")
    mutate_cart_in_place(shopping_cart.copy(), "Headphones")
    print(f"  Caller `shopping_cart` after copy: {shopping_cart} (protected!)")


if __name__ == "__main__":
    main()
```

---

### Example 3: Positional-Only (`/`) and Keyword-Only (`*`) Parameter Dividers
File: `example_03_positional_only_and_keyword_only.py`

```python
def transfer_funds(
    sender_acct: str,
    receiver_acct: str,
    /,  # Everything to the LEFT of `/` is POSITIONAL-ONLY
    amount: float,  # Between `/` and `*` is POSITIONAL-OR-KEYWORD
    *,  # Everything to the RIGHT of `*` is KEYWORD-ONLY
    currency: str = "INR",
    instant_settlement: bool = False,
) -> str:
    """Execute a bank transfer with strict parameter passing boundaries."""
    mode = "IMPS-Instant" if instant_settlement else "NEFT-Standard"
    return (
        f"[{mode}] {sender_acct} -> {receiver_acct} : "
        f"{currency} {amount:,.2f}"
    )


def main() -> None:
    print("=== 1. Valid Calls Respecting `/` and `*` Boundaries ===")
    # `amount` passed positionally
    receipt_1 = transfer_funds("ACCT-101", "ACCT-202", 15000.0)
    print(f"  Valid Call 1 : {receipt_1}")

    # `amount` passed by keyword, plus keyword-only arguments
    receipt_2 = transfer_funds(
        "ACCT-101",
        "ACCT-202",
        amount=42500.50,
        currency="USD",
        instant_settlement=True,
    )
    print(f"  Valid Call 2 : {receipt_2}")

    print("\n=== 2. Violating Positional-Only (`/`) Rule ===")
    try:
        # Passing `sender_acct` by keyword is forbidden because it is before `/`
        transfer_funds(sender_acct="ACCT-101", receiver_acct="ACCT-202", amount=500.0)
    except TypeError as err:
        print(f"  Caught expected TypeError: {err}")

    print("\n=== 3. Violating Keyword-Only (`*`) Rule ===")
    try:
        # Passing `currency` positionally is forbidden because it is after `*`
        transfer_funds("ACCT-101", "ACCT-202", 500.0, "EUR")
    except TypeError as err:
        print(f"  Caught expected TypeError: {err}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_parameters_vs_arguments.py`)
```text
=== 1. Formal Parameters vs Actual Arguments ===
  Call 1 (Correct Order) : Confirmed: Aarav with Dr. Mehta at 10:30 AM
  Call 2 (Swapped Order) : Confirmed: Mehta with Dr. Aarav at 10:30 AM

=== 2. Passing Variables and Expressions as Arguments ===
  Call 3 (Expressions)   : Confirmed: PRIYA with Dr. Sharma at 14:00 HRS

=== 3. Inspecting Formal Parameters at Runtime ===
  Function Signature     : (patient_name: str, doctor_name: str, time_slot: str) -> str
  Param #1: name='patient_name' | annotation=str  | kind=positional or keyword
  Param #2: name='doctor_name'  | annotation=str  | kind=positional or keyword
  Param #3: name='time_slot'    | annotation=str  | kind=positional or keyword
```

### Output — Example 2 (`example_02_pass_by_object_reference.py`)
```text
=== 1. Immutable Argument (`int`) - Caller Variable Unchanged ===
    [Inside start] score=50, id matches caller: True
    [Inside after] score=60 (rebound to new int object)
  Caller `player_score` after call : 50 (unchanged!)
  Returned value                   : 60

=== 2. Mutable Argument (`list`) - In-Place Mutation Affects Caller ===
  Before `mutate_cart_in_place`    : ['Laptop', 'Mouse']
  After  `mutate_cart_in_place`    : ['Laptop', 'Mouse', 'Keyboard'] (mutated!)

=== 3. Mutable Argument (`list`) - Local Reassignment Does NOT Mutate ===
  Caller `shopping_cart`           : ['Laptop', 'Mouse', 'Keyboard'] (unchanged!)
  Returned `new_cart`              : ['Laptop', 'Mouse', 'Keyboard', 'Monitor']

=== 4. Defensive Copying at Call Site (`cart.copy()`) ===
  Caller `shopping_cart` after copy: ['Laptop', 'Mouse', 'Keyboard'] (protected!)
```

### Output — Example 3 (`example_03_positional_only_and_keyword_only.py`)
```text
=== 1. Valid Calls Respecting `/` and `*` Boundaries ===
  Valid Call 1 : [NEFT-Standard] ACCT-101 -> ACCT-202 : INR 15,000.00
  Valid Call 2 : [IMPS-Instant] ACCT-101 -> ACCT-202 : USD 42,500.50

=== 2. Violating Positional-Only (`/`) Rule ===
  Caught expected TypeError: transfer_funds() got some positional-only arguments passed as keyword arguments: 'sender_acct, receiver_acct'

=== 3. Violating Keyword-Only (`*`) Rule ===
  Caught expected TypeError: transfer_funds() takes 3 positional arguments but 4 were given
```

---

## 7. Code Explanation

1. **Positional Binding (`example_01`):** In `schedule_appointment("Aarav", "Mehta", "10:30 AM")`, Python binds arguments by index position (`0 -> patient_name`, `1 -> doctor_name`, `2 -> time_slot`). Swapping two string arguments silently produces logically wrong output (`Mehta with Dr. Aarav`) because both are `str`.
2. **`cart.append(new_item)` vs `cart = cart + [new_item]` (`example_02`):**
   - `cart.append(new_item)` mutates the existing list object in-place. Because the caller's `shopping_cart` points to that exact same list object, the caller sees `"Keyboard"` added.
   - `cart = cart + [new_item]` creates a **new** list in memory and points the local variable `cart` to it, leaving the caller's `shopping_cart` completely untouched.
   - Warning: `cart += [new_item]` on a `list` calls `list.__iadd__`, which mutates the list **in-place** just like `.extend()`!
3. **`/` and `*` Dividers (`example_03`):**
   - `sender_acct, receiver_acct, /` means those first two parameters can **only** be passed positionally.
   - `*, currency="INR", instant_settlement=False` means those two parameters can **only** be passed by keyword name.

---

## 8. Common Mistakes

1. **Assuming `items = items + [x]` and `items += [x]` behave the same on a list parameter:**
   ```python
   def add_a(items: list[int]) -> None:
       items = items + [99]  # Rebinds local `items` to a NEW list; caller NOT mutated

   def add_b(items: list[int]) -> None:
       items += [99]         # Calls `items.extend([99])` IN-PLACE; caller IS mutated!
   ```
2. **Expecting a swap function `def swap(a, b): a, b = b, a` to swap variables in the caller:**
   - Rebinding `a` and `b` inside `swap` only swaps the local parameter names inside `swap`'s stack frame. The caller's variables are untouched. Instead, return `b, a` and unpack at the call site: `x, y = swap(x, y)`.
3. **Accidentally mutating an input list while sorting or popping inside a helper function:**
   - Calling `numbers.sort()` or `numbers.pop()` inside `calculate_median(numbers)` permanently alters the caller's list. Use `sorted(numbers)` (which returns a new list) so your function remains free of surprise side effects.
4. **Confusing the order of `/` and `*` in a function signature:**
   - `/` (positional-only divider) must always come **before** `*` (keyword-only divider): `def f(pos_only, /, standard, *, kw_only):`. Putting `*` before `/` is a `SyntaxError`.

---

## 9. Practice Questions

1. **Easy — Temperature Converter with Positional-Only Input:**
   Write a function `celsius_to_kelvin(celsius: float, /) -> float` where `celsius` is strictly positional-only. Test calling it positionally (`celsius_to_kelvin(25.0)`) and verify that calling `celsius_to_kelvin(celsius=25.0)` raises a `TypeError`.

2. **Medium — Safe List Normalizer (Non-Mutating vs In-Place):**
   Write a function `remove_negatives(values: list[int], *, in_place: bool = False) -> list[int]`.
   - When `in_place=False` (default), return a new list containing only non-negative numbers without modifying the caller's list.
   - When `in_place=True`, mutate the caller's list in-place (e.g., using `values[:] = ...`) and return it.

3. **Hard — Signature Validator Using `inspect`:**
   Write a helper `describe_parameters(func)` that uses `inspect.signature(func)` to return a dictionary categorizing parameter names into three lists: `{"positional_only": [...], "positional_or_keyword": [...], "keyword_only": [...]}`.

---

## 10. Interview Questions

### Q1: Is Python pass-by-value or pass-by-reference?
**Answer:**
Neither in the traditional C/C++ sense. Python uses **Pass-by-Object-Reference** (also known as **Call-by-Sharing**). When an argument is passed to a function, the formal parameter receives a copy of the *reference* to the object, not a copy of the object itself.
- Reassigning the parameter inside the function (`x = 10`) only changes where the local parameter points; it never affects the caller's variable.
- Mutating a mutable object through the parameter (`x.append(10)`) modifies the underlying object in memory, which is visible to the caller.

### Q2: Why does `def bump(lst): lst += [1]` modify the caller's list, whereas `def bump(tpl): tpl += (1,)` does not modify the caller's tuple?
**Answer:**
Augmented assignment (`+=`) invokes the `__iadd__` dunder method if the type implements it, falling back to `__add__` otherwise:
- `list` is **mutable** and implements `__iadd__` as an in-place extension (`list.extend`), mutating the shared list object.
- `tuple` is **immutable** and does not implement in-place mutation, so `tpl += (1,)` falls back to `tpl = tpl + (1,)`, creating a brand-new tuple and rebinding only the local variable `tpl`.

### Q3: Why did Python 3.8 introduce positional-only parameters (`/`) when Python already had positional-or-keyword parameters?
**Answer:**
1. **API Evolution:** If a parameter can be passed by keyword, its internal variable name becomes part of the public API—renaming `def sqrt(x):` to `def sqrt(value):` would break callers doing `sqrt(x=9)`. Marking it `def sqrt(x, /):` frees library authors to rename parameters later.
2. **Preventing Keyword Collisions with `**kwargs`:** In functions like `def update_cache(key, /, **kwargs):`, making `key` positional-only allows `kwargs` to safely contain a key literally named `"key"` (`update_cache("user_1", key="admin")`) without raising `TypeError: got multiple values for argument 'key'`.
