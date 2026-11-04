# Phase 4 — Topic 05: Inheritance

## 1. Introduction

**Inheritance** is an Object-Oriented Programming mechanism that allows a new class (called the **child class**, **subclass**, or **derived class**) to inherit attributes and methods from an existing class (called the **parent class**, **base class**, or **superclass**).

Inheritance models an **`IS-A` relationship**:
- A `FullTimeDeveloper` **IS-A** `Employee`.
- An `InsufficientFundsError` **IS-A** `CardDeclinedError`, which **IS-A** `PaymentError`, which **IS-A** `Exception`.

---

## 2. Why is it used?

- **Code Reuse (DRY Principle):** Shared attributes (`emp_id`, `name`) and methods (`badge_label()`) are written once in the parent class `Employee` and automatically inherited by every subclass.
- **Hierarchical Exception Handling:** Because `InsufficientFundsError` inherits from `PaymentError`, a caller can write `except PaymentError:` to catch all payment-related failures with a single handler, or `except InsufficientFundsError:` to handle just that specific case.
- **Polymorphic Substitution (Liskov Substitution Principle):** Any function expecting an `Employee` object can seamlessly accept a `FullTimeDeveloper` or `HourlyContractor` instance.

---

## 3. Syntax

```python
# 1. Parent / Base Class
class Employee:
    def __init__(self, emp_id: str, name: str) -> None:
        self.emp_id = emp_id
        self.name = name

    def badge_label(self) -> str:
        return f"[{self.emp_id}] {self.name}"


# 2. Child / Subclass (`class Child(Parent):`)
class FullTimeDeveloper(Employee):
    def __init__(self, emp_id: str, name: str, primary_lang: str) -> None:
        # Delegate parent initialization via `super()`
        super().__init__(emp_id, name)
        self.primary_lang = primary_lang
```

---

## 4. Explanation (Step-by-Step)

### Step 1: How `super().__init__(...)` Works
When a subclass defines its own `__init__`, it **overrides** the parent's `__init__`—meaning Python will **not** call `Parent.__init__` automatically!
To ensure parent attributes (`self.emp_id`, `self.name`) are initialized, the child's `__init__` calls **`super().__init__(emp_id, name)`**, which delegates to the next class in the Method Resolution Order (`__mro__`).

### Step 2: `isinstance()` vs `issubclass()` vs `type() is`
- **`isinstance(obj, Class)`:** Returns `True` if `obj` is an instance of `Class` **or any subclass of `Class`**. (`isinstance(dev, Employee) -> True`)
- **`type(obj) is Class`:** Checks exact class match only, ignoring inheritance (`type(dev) is Employee -> False`). Always prefer `isinstance()` in OOP code.
- **`issubclass(Sub, Parent)`:** Checks whether a **class** `Sub` inherits from `Parent` (`issubclass(FullTimeDeveloper, Employee) -> True`).

### Step 3: Inheritance (`IS-A`) vs Composition (`HAS-A`)
One of the most important software design rules is **"Favor Composition over Inheritance"** when there is no true `IS-A` relationship:
- Use **Inheritance (`IS-A`)** when the child class truly is a specialized version of the parent (`CardDeclinedError` IS-A `PaymentError`).
- Use **Composition (`HAS-A`)** when a class simply needs to *use* another object's functionality (`SecureDocumentVault` **HAS-A** `AuditLogger` stored in `self.logger`). Inheriting from `AuditLogger` or `list` would expose internal methods onto `SecureDocumentVault`'s public interface!

---

## 5. Minimum 3 Examples

### Example 1: Single Inheritance (`Parent` -> `Child`) and Reusing Base Behavior
File: `example_01_single_inheritance_and_super.py`

```python
class Employee:
    """Base class sharing common identity and badge logic for all staff."""

    def __init__(self, emp_id: str, name: str) -> None:
        self.emp_id = emp_id
        self.name = name

    def badge_label(self) -> str:
        return f"[{self.emp_id}] {self.name}"


class FullTimeDeveloper(Employee):
    """Inherits from `Employee` and adds salary + tech stack."""

    def __init__(self, emp_id: str, name: str, monthly_salary: float, primary_lang: str) -> None:
        super().__init__(emp_id, name)  # Initialize `emp_id` and `name` in `Employee`
        self.monthly_salary = monthly_salary
        self.primary_lang = primary_lang

    def compute_monthly_payout(self) -> float:
        return self.monthly_salary


class HourlyContractor(Employee):
    """Inherits from `Employee` and computes payout from hourly rate * hours logged."""

    def __init__(self, emp_id: str, name: str, hourly_rate: float, hours_logged: float) -> None:
        super().__init__(emp_id, name)
        self.hourly_rate = hourly_rate
        self.hours_logged = hours_logged

    def compute_monthly_payout(self) -> float:
        return round(self.hourly_rate * self.hours_logged, 2)


def main() -> None:
    dev = FullTimeDeveloper("EMP-101", "Aarav", 140000.0, "Python")
    contractor = HourlyContractor("CNT-502", "Priya", 1800.0, 65.0)

    print("=== 1. Subclasses Inherit `badge_label()` and Add Specialized Payouts ===")
    print(f"  {dev.badge_label():<20} | Payout: INR {dev.compute_monthly_payout():,.2f} ({dev.primary_lang})")
    print(f"  {contractor.badge_label():<20} | Payout: INR {contractor.compute_monthly_payout():,.2f}")

    print("\n=== 2. Verifying `isinstance()` and `issubclass()` ===")
    print(f"  isinstance(dev, FullTimeDeveloper) : {isinstance(dev, FullTimeDeveloper)}")
    print(f"  isinstance(dev, Employee)          : {isinstance(dev, Employee)} (IS-A Employee!)")
    print(f"  issubclass(HourlyContractor, Employee) : {issubclass(HourlyContractor, Employee)}")


if __name__ == "__main__":
    main()
```

---

### Example 2: Multilevel Inheritance (`Grandparent -> Parent -> Child`) & Custom Exceptions
File: `example_02_multilevel_inheritance_hierarchy.py`

```python
class PaymentError(Exception):
    """Base domain exception for all payment failures (Level 1)."""

    def __init__(self, transaction_id: str, message: str) -> None:
        super().__init__(f"[{transaction_id}] {message}")
        self.transaction_id = transaction_id


class CardDeclinedError(PaymentError):
    """Specialized payment error for bank card declines (Level 2)."""

    def __init__(self, transaction_id: str, decline_code: str, message: str) -> None:
        super().__init__(transaction_id, f"Declined ({decline_code}): {message}")
        self.decline_code = decline_code


class InsufficientFundsError(CardDeclinedError):
    """Specific decline reason with shortfall calculation (Level 3)."""

    def __init__(self, transaction_id: str, required: float, available: float) -> None:
        shortfall = round(required - available, 2)
        super().__init__(
            transaction_id,
            decline_code="INSUFFICIENT_FUNDS",
            message=f"Shortfall of INR {shortfall:,.2f}",
        )
        self.shortfall = shortfall


def main() -> None:
    print("=== 1. Raising and Catching a 3-Level Exception Hierarchy ===")
    try:
        raise InsufficientFundsError("TXN-9081", required=5000.0, available=3200.0)
    except PaymentError as err:
        # Caught by the base `PaymentError` handler!
        print(f"  Caught as `PaymentError` : {err}")
        print(f"  Actual runtime class     : {type(err).__name__}")
        if isinstance(err, InsufficientFundsError):
            print(f"  Shortfall attribute      : INR {err.shortfall:,.2f}")

    print("\n=== 2. Inspecting the Method Resolution Order (`__mro__`) ===")
    mro_names = [cls.__name__ for cls in InsufficientFundsError.__mro__]
    print(f"  MRO chain : {' -> '.join(mro_names)}")


if __name__ == "__main__":
    main()
```

---

### Example 3: Inheritance (`IS-A`) vs Composition (`HAS-A`)
File: `example_03_inheritance_vs_composition.py`

```python
class AuditLogger:
    """Reusable component for recording structured audit events."""

    def __init__(self) -> None:
        self.entries: list[str] = []

    def record(self, actor: str, action: str) -> None:
        self.entries.append(f"actor={actor} | action={action}")


class SecureDocumentVault:
    """
    Uses COMPOSITION (`HAS-A` AuditLogger) instead of inheriting from `AuditLogger` or `list`.
    Callers cannot accidentally call `.clear()` or `.pop()` on the vault!
    """

    def __init__(self, vault_name: str) -> None:
        self.vault_name = vault_name
        self._documents: dict[str, str] = {}
        self.logger = AuditLogger()  # HAS-A relationship (Composition)

    def store_document(self, user: str, doc_id: str, content: str) -> None:
        self._documents[doc_id] = content
        self.logger.record(user, f"stored {doc_id}")

    def read_document(self, user: str, doc_id: str) -> str:
        self.logger.record(user, f"read {doc_id}")
        return self._documents.get(doc_id, "<NOT FOUND>")


def main() -> None:
    print("=== Composition (`HAS-A`): `SecureDocumentVault` + `AuditLogger` ===")
    vault = SecureDocumentVault("Legal-Contracts")
    vault.store_document("aarav", "DOC-01", "Non-Disclosure Agreement")
    content = vault.read_document("priya", "DOC-01")
    print(f"  Retrieved document : {content!r}")
    print("  Audit trail entries:")
    for entry in vault.logger.entries:
        print(f"    - {entry}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_single_inheritance_and_super.py`)
```text
=== 1. Subclasses Inherit `badge_label()` and Add Specialized Payouts ===
  [EMP-101] Aarav      | Payout: INR 140,000.00 (Python)
  [CNT-502] Priya      | Payout: INR 117,000.00

=== 2. Verifying `isinstance()` and `issubclass()` ===
  isinstance(dev, FullTimeDeveloper) : True
  isinstance(dev, Employee)          : True (IS-A Employee!)
  issubclass(HourlyContractor, Employee) : True
```

### Output — Example 2 (`example_02_multilevel_inheritance_hierarchy.py`)
```text
=== 1. Raising and Catching a 3-Level Exception Hierarchy ===
  Caught as `PaymentError` : [TXN-9081] Declined (INSUFFICIENT_FUNDS): Shortfall of INR 1,800.00
  Actual runtime class     : InsufficientFundsError
  Shortfall attribute      : INR 1,800.00

=== 2. Inspecting the Method Resolution Order (`__mro__`) ===
  MRO chain : InsufficientFundsError -> CardDeclinedError -> PaymentError -> Exception -> BaseException -> object
```

### Output — Example 3 (`example_03_inheritance_vs_composition.py`)
```text
=== Composition (`HAS-A`): `SecureDocumentVault` + `AuditLogger` ===
  Retrieved document : 'Non-Disclosure Agreement'
  Audit trail entries:
    - actor=aarav | action=stored DOC-01
    - actor=priya | action=read DOC-01
```

---

## 7. Code Explanation

1. **Chaining `super().__init__()` (`example_01` & `example_02`):** `InsufficientFundsError.__init__` calls `super().__init__` (`CardDeclinedError`), which calls `super().__init__` (`PaymentError`), which calls `super().__init__` (`Exception`). Every layer initializes its own attributes (`shortfall`, `decline_code`, `transaction_id`, and `Exception.args`).
2. **Method Resolution Order (`__mro__` in `example_02`):** Python searches attributes along `InsufficientFundsError -> CardDeclinedError -> PaymentError -> Exception -> BaseException -> object`.
3. **Composition Encapsulation (`example_03`):** Because `SecureDocumentVault` holds `self._documents` and `self.logger` via composition rather than inheriting from `dict` or `AuditLogger`, callers can only interact with the vault through `store_document()` and `read_document()`.

---

## 8. Common Mistakes

1. **Forgetting to call `super().__init__(...)` when overriding `__init__` in a subclass:**
   - Unlike Java or C++, Python does **not** implicitly invoke the parent's no-arg `__init__` when a child defines `__init__`. Forgetting `super().__init__(...)` leaves all parent instance attributes uninitialized, causing `AttributeError` later!
2. **Hardcoding `ParentClass.__init__(self, ...)` instead of `super().__init__(...)`:**
   - Calling `Employee.__init__(self, ...)` directly bypasses Python's Cooperative MRO and causes parent classes to be initialized multiple times in multiple inheritance hierarchies. Always use `super().__init__(...)`.
3. **Inheriting from a class when there is no `IS-A` relationship (e.g., `class Stack(list):`):**
   - If `Stack` inherits from `list`, a caller can call `stack.insert(0, x)`, `stack.sort()`, or `stack[2] = 99`, violating the LIFO invariant of a stack! A `Stack` **HAS-A** internal list (`self._items = []`), it is not a `list`.

---

## 9. Practice Questions

1. **Easy — Vehicle Hierarchy:**
   Create a base class `Vehicle(brand: str, max_speed_kmh: int)` and a subclass `ElectricCar(Vehicle)` that adds `battery_kwh: float` and `range_km(self) -> float` (assuming $6.5 \text{ km per kWh}$).

2. **Medium — Bank Account Hierarchy (`SavingsAccount` & `OverdraftAccount`):**
   Create `BankAccount(acct_no, balance)` with `deposit()` and `withdraw()`. Create `SavingsAccount(BankAccount)` with `apply_annual_interest(rate_pct)` and `OverdraftAccount(BankAccount)` that overrides `withdraw()` to allow balances down to `-overdraft_limit`.

3. **Hard — Refactoring Misused Inheritance into Composition:**
   Write a `BoundedQueue(capacity: int)` class that uses **composition** (an internal `collections.deque`) instead of inheriting from `list` or `deque`, exposing only `enqueue(item)`, `dequeue()`, and `is_full() -> bool`.

---

## 10. Interview Questions

### Q1: Does Python automatically call the parent class's `__init__` when a subclass defines its own `__init__`?
**Answer:**
**No.** Lookups for `__init__` follow the standard MRO: if the subclass defines `__init__`, Python calls `Subclass.__init__` and stops. To run the parent's initialization logic as well, the subclass must explicitly call `super().__init__(...)`. (However, if the subclass does *not* define `__init__` at all, Python automatically walks up the MRO and calls the parent's `__init__`.)

### Q2: Why is `isinstance(bool_val, int)` equal to `True` in Python (`isinstance(True, int) == True`)?
**Answer:**
For historical backward compatibility (Python added `bool` in version 2.3), **`bool` is a subclass of `int`** (`issubclass(bool, int) == True`), where `True == 1` and `False == 0`. This is a classic interview gotcha when validating JSON inputs: if you want to check for an integer while rejecting booleans, write `isinstance(x, int) and not isinstance(x, bool)`.

### Q3: When should you choose Composition over Inheritance?
**Answer:**
Apply the **`IS-A` vs `HAS-A` test** and the **Liskov Substitution Principle (LSP)**:
- If every valid operation on `Parent` is also valid and meaningful on `Child` (`Child` IS-A `Parent`), use **Inheritance**.
- If `Child` only wants to reuse part of `Parent`'s implementation while hiding or forbidding other methods of `Parent`, or if `Child` needs to swap out the component behavior dynamically at runtime, use **Composition (`HAS-A`)**.
