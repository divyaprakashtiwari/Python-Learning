# Phase 4 — Topic 02: Constructors

## 1. Introduction

In Object-Oriented Programming, a **constructor** is the special mechanism responsible for creating and setting up a new object when a class is instantiated (`acct = BankVaultAccount("SBI-1001", "Aarav")`).

In Python, object construction is actually a **two-step process** handled by two special dunder ("double underscore") methods:
1. **`__new__(cls, ...)` (The Allocator):** Creates and returns the raw, uninitialized instance in memory. (Rarely overridden except for Singletons or subclassing immutable types like `str`, `int`, or `tuple`.)
2. **`__init__(self, ...)` (The Initializer):** Receives the newly created `self` instance from `__new__` and populates its initial attributes and validates invariants.

---

## 2. Why is it used?

- **Guaranteed Valid State (Fail-Fast Invariants):** By requiring mandatory parameters and validating them inside `__init__`, an object can **never** exist in an incomplete or invalid state (such as a bank account with a negative opening balance or missing account number).
- **Automatic Setup:** Every instance automatically receives its required attributes, default values, and derived fields upon creation without requiring the caller to call a separate `.setup()` method.
- **Multiple Construction Pathways (`@classmethod`):** While Python allows only one `__init__` per class, `@classmethod` factories (`from_dict`, `from_csv_row`, `from_json`) provide clean, named alternative constructors.

---

## 3. Syntax

```python
class BankVaultAccount:
    # 1. Standard Initializer (`__init__` must ALWAYS return `None`)
    def __init__(self, account_number: str, opening_balance: float = 0.0) -> None:
        if opening_balance < 0:
            raise ValueError("opening_balance cannot be negative")
        self.account_number = account_number
        self.balance = opening_balance

    # 2. Alternative Constructor using `@classmethod`
    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "BankVaultAccount":
        return cls(str(data["account_number"]), float(str(data["opening_balance"])))
```

---

## 4. Explanation (Step-by-Step)

### Step 1: `__new__` vs `__init__`
| Feature | `__new__(cls, ...)` | `__init__(self, ...)` |
| :--- | :--- | :--- |
| **Role** | **Allocates** the object in memory | **Initializes** attributes on `self` |
| **First Parameter** | `cls` (the class being instantiated) | `self` (the newly allocated instance) |
| **Return Value** | **Must return the new instance** | **Must return `None`** (raising `TypeError` otherwise) |
| **When to Override** | Subclassing immutable types (`str`, `tuple`), Singletons, object caching | 99% of everyday classes |

### Step 2: Why Python Doesn't Have Java/C++ Constructor Overloading
If you define two `def __init__(self, ...)` methods inside the same Python class, the second `def __init__` simply **overwrites** the first one in the class namespace!
Instead, Python uses:
1. **Default arguments** in `__init__` (`opening_balance: float = 0.0`), and
2. **`@classmethod` factory methods** (`EventTicket.from_csv_row(...)`, `EventTicket.from_dict(...)`, `datetime.fromisoformat(...)`), which are even clearer than overloaded constructors because each factory has a self-documenting name.

---

## 5. Minimum 3 Examples

### Example 1: `__init__` Initializer with Validation, Defaults, and Derived Attributes
File: `example_01_init_validation_and_defaults.py`

```python
class BankVaultAccount:
    """Represents a validated bank account whose invariants are enforced at construction."""

    def __init__(
        self,
        account_number: str,
        holder_name: str,
        opening_balance: float = 0.0,
        currency: str = "INR",
    ) -> None:
        # 1. Fail-fast invariant validation inside `__init__`
        if not account_number.strip():
            raise ValueError("account_number cannot be empty")
        if opening_balance < 0:
            raise ValueError(f"opening_balance cannot be negative (got {opening_balance})")

        # 2. Normalized & direct attributes
        self.account_number = account_number.strip().upper()
        self.holder_name = holder_name.strip().title()
        self.balance = round(opening_balance, 2)
        self.currency = currency.upper()

        # 3. Derived attribute computed automatically during initialization
        self.is_high_net_worth = self.balance >= 1_000_000.0

    def summary(self) -> str:
        tier = "HNW-Priority" if self.is_high_net_worth else "Standard"
        return (
            f"[{self.account_number}] {self.holder_name:<15} | "
            f"{self.currency} {self.balance:>12,.2f} ({tier})"
        )


def main() -> None:
    print("=== 1. Valid Construction (With Defaults and Overrides) ===")
    acct_1 = BankVaultAccount(" sbi-1001 ", "aarav sharma")
    acct_2 = BankVaultAccount("hdfc-2040", "priya patel", 2_500_000.0)
    print(f"  {acct_1.summary()}")
    print(f"  {acct_2.summary()}")

    print("\n=== 2. Rejecting Invalid State in `__init__` ===")
    try:
        BankVaultAccount("ICICI-999", "Rohan", opening_balance=-500.0)
    except ValueError as err:
        print(f"  Caught expected ValueError: {err}")


if __name__ == "__main__":
    main()
```

---

### Example 2: Two-Step Object Creation (`__new__` Allocator vs `__init__` Initializer)
File: `example_02_new_vs_init_and_singleton.py`

```python
class DatabaseConnectionPool:
    """Singleton class: `__new__` ensures only one pool instance is ever allocated."""

    _instance: "DatabaseConnectionPool | None" = None
    _initialized: bool = False

    def __new__(cls, *args: object, **kwargs: object) -> "DatabaseConnectionPool":
        print(f"    [1. __new__] Checking if {cls.__name__} singleton exists...")
        if cls._instance is None:
            print("    [1. __new__] Allocating brand-new instance via super().__new__(cls)")
            cls._instance = super().__new__(cls)
        else:
            print("    [1. __new__] Returning existing singleton instance!")
        return cls._instance

    def __init__(self, max_connections: int = 10) -> None:
        print(f"    [2. __init__] Running initializer (already initialized={self._initialized})")
        if not self._initialized:
            self.max_connections = max_connections
            self._initialized = True


class UpperSlug(str):
    """Subclassing immutable `str`: value must be transformed inside `__new__`, not `__init__`!"""

    def __new__(cls, raw_text: str) -> "UpperSlug":
        normalized = raw_text.strip().upper().replace(" ", "-")
        return super().__new__(cls, normalized)


def main() -> None:
    print("=== 1. Tracing `__new__` Followed by `__init__` (Singleton Pool) ===")
    pool_a = DatabaseConnectionPool(max_connections=20)
    pool_b = DatabaseConnectionPool(max_connections=99)
    print(f"  pool_a is pool_b        : {pool_a is pool_b}")
    print(f"  pool_b.max_connections  : {pool_b.max_connections} (preserved from first init!)")

    print("\n=== 2. Customizing Immutable Type Creation in `__new__` ===")
    slug = UpperSlug("  python oop constructors  ")
    print(f"  UpperSlug value         : {slug!r} | isinstance(slug, str)={isinstance(slug, str)}")


if __name__ == "__main__":
    main()
```

---

### Example 3: Alternative Constructors Using `@classmethod` (`from_dict`, `from_csv_row`)
File: `example_03_alternative_classmethod_constructors.py`

```python
from datetime import datetime


class EventTicket:
    """Represents a concert/conference ticket with multiple construction pathways."""

    def __init__(self, event_name: str, attendee: str, price: float, event_date: str) -> None:
        self.event_name = event_name
        self.attendee = attendee
        self.price = price
        self.event_date = event_date

    @classmethod
    def from_csv_row(cls, csv_line: str) -> "EventTicket":
        """Alternative constructor #1: parse a comma-separated string."""
        name, attendee, price_str, date_str = [part.strip() for part in csv_line.split(",")]
        return cls(name, attendee, float(price_str), date_str)

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "EventTicket":
        """Alternative constructor #2: build from a JSON/dict payload."""
        return cls(
            event_name=str(payload["event_name"]),
            attendee=str(payload["attendee"]),
            price=float(str(payload["price"])),
            event_date=str(payload["event_date"]),
        )

    @classmethod
    def complimentary_vip(cls, event_name: str, attendee: str) -> "EventTicket":
        """Alternative constructor #3: create a free VIP pass for today's date."""
        today_str = datetime(2026, 11, 4).strftime("%Y-%m-%d")
        return cls(f"{event_name} [VIP]", attendee, 0.0, today_str)

    def format_ticket(self) -> str:
        return (
            f"Ticket({self.event_name!r}, attendee={self.attendee!r}, "
            f"price=INR {self.price:,.2f}, date={self.event_date})"
        )


def main() -> None:
    print("=== Constructing `EventTicket` via 4 Different Pathways ===")
    t1 = EventTicket("PyCon India", "Divya", 2500.0, "2026-11-15")
    t2 = EventTicket.from_csv_row("Cloud Summit, Aarav, 1800.50, 2026-12-01")
    t3 = EventTicket.from_dict(
        {
            "event_name": "AI Workshop",
            "attendee": "Priya",
            "price": 999.0,
            "event_date": "2026-11-20",
        }
    )
    t4 = EventTicket.complimentary_vip("PyCon India", "Keynote Speaker")

    for idx, ticket in enumerate((t1, t2, t3, t4), start=1):
        print(f"  Pathway #{idx} : {ticket.format_ticket()}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_init_validation_and_defaults.py`)
```text
=== 1. Valid Construction (With Defaults and Overrides) ===
  [SBI-1001] Aarav Sharma    | INR         0.00 (Standard)
  [HDFC-2040] Priya Patel     | INR 2,500,000.00 (HNW-Priority)

=== 2. Rejecting Invalid State in `__init__` ===
  Caught expected ValueError: opening_balance cannot be negative (got -500.0)
```

### Output — Example 2 (`example_02_new_vs_init_and_singleton.py`)
```text
=== 1. Tracing `__new__` Followed by `__init__` (Singleton Pool) ===
    [1. __new__] Checking if DatabaseConnectionPool singleton exists...
    [1. __new__] Allocating brand-new instance via super().__new__(cls)
    [2. __init__] Running initializer (already initialized=False)
    [1. __new__] Checking if DatabaseConnectionPool singleton exists...
    [1. __new__] Returning existing singleton instance!
    [2. __init__] Running initializer (already initialized=True)
  pool_a is pool_b        : True
  pool_b.max_connections  : 20 (preserved from first init!)

=== 2. Customizing Immutable Type Creation in `__new__` ===
  UpperSlug value         : 'PYTHON-OOP-CONSTRUCTORS' | isinstance(slug, str)=True
```

### Output — Example 3 (`example_03_alternative_classmethod_constructors.py`)
```text
=== Constructing `EventTicket` via 4 Different Pathways ===
  Pathway #1 : Ticket('PyCon India', attendee='Divya', price=INR 2,500.00, date=2026-11-15)
  Pathway #2 : Ticket('Cloud Summit', attendee='Aarav', price=INR 1,800.50, date=2026-12-01)
  Pathway #3 : Ticket('AI Workshop', attendee='Priya', price=INR 999.00, date=2026-11-20)
  Pathway #4 : Ticket('PyCon India [VIP]', attendee='Keynote Speaker', price=INR 0.00, date=2026-11-04)
```

---

## 7. Code Explanation

1. **Fail-Fast Validation (`example_01`):** Raising `ValueError` inside `__init__` immediately aborts construction so the caller never receives a broken `BankVaultAccount` reference.
2. **Why `Singleton` Needs `_initialized` (`example_02`):** Whenever `__new__(cls)` returns an instance of `cls`, Python **always calls `__init__` on that returned instance**—even if `__new__` returned an already-existing singleton! Guarding `__init__` with `if not self._initialized:` prevents the second call `DatabaseConnectionPool(max_connections=99)` from overwriting `max_connections=20`.
3. **Why `cls(...)` Is Used in `@classmethod` (`example_03`):** Inside `from_csv_row(cls, ...)`, calling `cls(...)` instead of hardcoding `EventTicket(...)` ensures that if a subclass `VIPTicket(EventTicket)` calls `VIPTicket.from_csv_row(...)`, it returns an instance of `VIPTicket`!

---

## 8. Common Mistakes

1. **Trying to `return self` (or any non-`None` value) from `__init__`:**
   - Writing `return self` inside `__init__` raises `TypeError: __init__() should return None, not '...'`. Python returns the instance automatically after `__init__` finishes.
2. **Writing `def _init_(self):` with single underscores instead of double underscores `__init__`:**
   - A single-underscore `def _init_(self):` is treated as an ordinary method that is **never called automatically** on instantiation, leading to `AttributeError` when trying to access uninitialized attributes.
3. **Defining multiple `def __init__` methods expecting C++/Java constructor overloading:**
   - Only the last `def __init__` in the class body survives. Use default arguments or `@classmethod` factory methods instead.

---

## 9. Practice Questions

1. **Easy — Validated `Temperature` Constructor:**
   Create a `Temperature` class whose `__init__(self, kelvin: float)` raises `ValueError` if `kelvin < 0.0` (below absolute zero). Add `@classmethod` constructors `from_celsius(cls, c: float)` and `from_fahrenheit(cls, f: float)`.

2. **Medium — Immutable ` Coordinate2D` Subclassing `tuple` (`__new__`):**
   Subclass `tuple` to create `Coordinate2D(x, y)` using `def __new__(cls, x: float, y: float)` that stores `(round(x, 4), round(y, 4))` and exposes `.x` and `.y` properties.

3. **Hard — Object Interning / Flyweight Cache in `__new__`:**
   Create a `Currency(code: str)` class that caches instances by uppercase `code` (`"INR"`, `"USD"`) in a class dictionary `_cache` inside `__new__` so that `Currency("inr") is Currency("INR")` evaluates to `True`.

---

## 10. Interview Questions

### Q1: Is `__init__` the actual constructor in Python?
**Answer:**
Strictly speaking, `__init__` is the **initializer**, while **`__new__`** is the actual allocator/constructor. When `MyClass(x)` is called, `MyClass.__new__(MyClass, x)` allocates the object in memory and returns it, and then `MyClass.__init__(instance, x)` initializes its attributes. Together they form the construction lifecycle.

### Q2: Under what condition does Python skip calling `__init__` after `__new__` finishes?
**Answer:**
If `__new__(cls, ...)` returns an object that is **not** an instance of `cls` (for example, returning `None` or an instance of a completely unrelated class), Python **does not** call `cls.__init__`.

### Q3: Why can't you modify the string value of a `class UpperStr(str):` subclass inside `__init__`?
**Answer:**
Because `str` (like `int`, `float`, `tuple`, and `frozenset`) is **immutable**. By the time `__init__(self, ...)` is called, the underlying immutable string memory buffer has already been allocated and locked by `str.__new__`. Therefore, any transformation of an immutable built-in subclass must happen inside `__new__` before calling `super().__new__(cls, transformed_value)`.
