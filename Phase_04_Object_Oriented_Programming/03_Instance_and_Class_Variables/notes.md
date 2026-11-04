# Phase 4 — Topic 03: Instance and Class Variables

## 1. Introduction

In Python classes, attributes fall into two distinct scopes depending on where they are defined and assigned:

1. **Class Variables:** Defined directly inside the `class` body (outside any method). A single copy lives in `ClassName.__dict__` and is **shared across every instance** of the class (and its subclasses).
2. **Instance Variables:** Assigned on `self` (typically inside `__init__`, e.g., `self.username = username`). Each object gets its **own independent copy** stored in `self.__dict__`.

---

## 2. Why is it used?

- **Memory Efficiency & Shared Constants:** Storing class-level constants (`gst_rate = 0.18`, `company_domain = "techcorp.in"`, `MAX_RETRIES = 3`) once on the class avoids duplicating identical strings or floats across 1,000,000 instances.
- **Class-Wide Counters & Registries:** Class variables can track how many instances have been created (`CloudSubscription.active_subscriptions += 1`) or maintain a registry of active connections.
- **Per-Instance Customization (Shadowing):** A class variable can provide a sensible default (`default_access_level = 1`) that individual instances can selectively override (`emp.default_access_level = 5`) without affecting other instances.

---

## 3. Syntax

```python
class CloudSubscription:
    # 1. CLASS VARIABLE (shared by all instances)
    gst_rate: float = 0.18

    def __init__(self, tenant_name: str, monthly_base_fee: float) -> None:
        # 2. INSTANCE VARIABLES (unique to each instance `self`)
        self.tenant_name = tenant_name
        self.monthly_base_fee = monthly_base_fee
```

---

## 4. Explanation (Step-by-Step)

### Step 1: Python's Two-Tier Attribute Lookup Chain
When you read an attribute via `obj.attr`:
1. **Check `obj.__dict__` first (Instance Namespace):** If `"attr"` exists on the instance itself, Python returns that value immediately.
2. **Fallback to `type(obj).__dict__` (Class Namespace & MRO):** If `"attr"` is not in `obj.__dict__`, Python looks up `"attr"` in the class (and then parent classes).

### Step 2: Reading vs Assigning (`self.attr` Shadowing)
- Writing `ClassName.gst_rate = 0.12` updates the **class variable** for all instances that haven't shadowed it.
- Writing `sub_a.gst_rate = 0.0` (or `self.gst_rate = 0.0` inside an instance method) does **NOT** modify `ClassName.gst_rate`! Instead, it creates a new instance variable `"gst_rate"` inside `sub_a.__dict__` that **shadows** the class variable for `sub_a` only.
- Running `del sub_a.gst_rate` deletes the instance shadow from `sub_a.__dict__`, so `sub_a.gst_rate` once again falls back to `ClassName.gst_rate`.

### Step 3: The Mutable Class Variable Trap
Never define a mutable container (`roles: list[str] = []` or `cache: dict = {}`) as a class variable if each instance is supposed to have its own data!
- Because `u1.roles.append("admin")` mutates the list in-place (without rebinding `u1.roles`), Python finds `roles` on the class and mutates the **shared class list**, leaking `"admin"` to every other user instance (`u2`, `u3`, ...).
- Always initialize per-instance mutable containers (`self.roles = []`) inside `__init__`.

---

## 5. Minimum 3 Examples

### Example 1: Shared Class Variables vs Per-Object Instance Variables
File: `example_01_instance_vs_class_variables.py`

```python
class CloudSubscription:
    """Models a SaaS subscription with a shared class-level GST rate and instance counter."""

    # Class variables (shared across all instances, stored in `CloudSubscription.__dict__`)
    gst_rate: float = 0.18
    active_subscriptions: int = 0

    def __init__(self, tenant_name: str, monthly_base_fee: float) -> None:
        # Instance variables (unique per object, stored in `self.__dict__`)
        self.tenant_name = tenant_name
        self.monthly_base_fee = monthly_base_fee
        # Increment the class variable on the class itself
        CloudSubscription.active_subscriptions += 1

    def total_monthly_bill(self) -> float:
        """Read `self.gst_rate` (which falls back to `CloudSubscription.gst_rate`)."""
        return round(self.monthly_base_fee * (1.0 + self.gst_rate), 2)


def main() -> None:
    print("=== 1. Creating Instances & Tracking Class-Level Counter ===")
    sub_a = CloudSubscription("Acme Corp", 10000.0)
    sub_b = CloudSubscription("Zenith Labs", 25000.0)
    print(f"  Active subscriptions : {CloudSubscription.active_subscriptions}")
    print(f"  Acme bill (18% GST)  : INR {sub_a.total_monthly_bill():,.2f}")
    print(f"  Zenith bill (18% GST): INR {sub_b.total_monthly_bill():,.2f}")

    print("\n=== 2. Updating a Class Variable on the Class Affects All Instances ===")
    CloudSubscription.gst_rate = 0.12
    print(f"  Acme bill (12% GST)  : INR {sub_a.total_monthly_bill():,.2f}")
    print(f"  Zenith bill (12% GST): INR {sub_b.total_monthly_bill():,.2f}")


if __name__ == "__main__":
    main()
```

---

### Example 2: Attribute Shadowing (`self.attr = ...` vs `Class.attr = ...`)
File: `example_02_shadowing_class_variables.py`

```python
class EmployeeBadge:
    """Demonstrates class attribute lookup and per-instance shadowing."""

    company_domain: str = "techcorp.in"
    default_access_level: int = 1

    def __init__(self, username: str) -> None:
        self.username = username

    def email(self) -> str:
        return f"{self.username}@{self.company_domain}"


def main() -> None:
    emp_1 = EmployeeBadge("aarav")
    emp_2 = EmployeeBadge("priya")

    print("=== 1. Before Shadowing: Both Read From `EmployeeBadge.__dict__` ===")
    print(f"  emp_1.__dict__ : {emp_1.__dict__}")
    print(f"  emp_1.email()  : {emp_1.email()} | level={emp_1.default_access_level}")
    print(f"  emp_2.email()  : {emp_2.email()} | level={emp_2.default_access_level}")

    print("\n=== 2. Shadowing `company_domain` on `emp_1` Only ===")
    # Creates `'company_domain'` inside `emp_1.__dict__`; does NOT touch `EmployeeBadge`!
    emp_1.company_domain = "contractor.techcorp.in"
    print(f"  emp_1.__dict__ : {emp_1.__dict__}")
    print(f"  emp_1.email()  : {emp_1.email()} (uses shadowed instance attribute)")
    print(f"  emp_2.email()  : {emp_2.email()} (still uses class attribute!)")

    print("\n=== 3. Deleting the Shadow Restores Fallback to Class Variable ===")
    del emp_1.company_domain
    print(f"  After `del emp_1.company_domain`, emp_1.email() : {emp_1.email()}")


if __name__ == "__main__":
    main()
```

---

### Example 3: The Mutable Class Variable Trap (`roles = []` on Class vs `self`)
File: `example_03_mutable_class_variable_trap.py`

```python
class BuggyUserProfile:
    """BUGGY: `roles` is a mutable class variable shared by EVERY user instance!"""

    roles: list[str] = []

    def __init__(self, username: str) -> None:
        self.username = username


class SafeUserProfile:
    """SAFE: Each instance gets its own independent `self.roles` list in `__init__`."""

    def __init__(self, username: str) -> None:
        self.username = username
        self.roles: list[str] = []


def main() -> None:
    print("=== 1. The Mutable Class Variable Trap (`BuggyUserProfile`) ===")
    u1 = BuggyUserProfile("alice")
    u2 = BuggyUserProfile("bob")
    u1.roles.append("admin")
    print(f"  u1 ('alice') roles : {u1.roles}")
    print(f"  u2 ('bob')   roles : {u2.roles}  <-- Bob accidentally became admin!")
    print(f"  u1.roles is u2.roles: {u1.roles is u2.roles}")

    print("\n=== 2. The Fix: Initialize Mutable Attributes Inside `__init__` ===")
    s1 = SafeUserProfile("alice")
    s2 = SafeUserProfile("bob")
    s1.roles.append("admin")
    print(f"  s1 ('alice') roles : {s1.roles}")
    print(f"  s2 ('bob')   roles : {s2.roles}  <-- Clean and isolated!")
    print(f"  s1.roles is s2.roles: {s1.roles is s2.roles}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_instance_vs_class_variables.py`)
```text
=== 1. Creating Instances & Tracking Class-Level Counter ===
  Active subscriptions : 2
  Acme bill (18% GST)  : INR 11,800.00
  Zenith bill (18% GST): INR 29,500.00

=== 2. Updating a Class Variable on the Class Affects All Instances ===
  Acme bill (12% GST)  : INR 11,200.00
  Zenith bill (12% GST): INR 28,000.00
```

### Output — Example 2 (`example_02_shadowing_class_variables.py`)
```text
=== 1. Before Shadowing: Both Read From `EmployeeBadge.__dict__` ===
  emp_1.__dict__ : {'username': 'aarav'}
  emp_1.email()  : aarav@techcorp.in | level=1
  emp_2.email()  : priya@techcorp.in | level=1

=== 2. Shadowing `company_domain` on `emp_1` Only ===
  emp_1.__dict__ : {'username': 'aarav', 'company_domain': 'contractor.techcorp.in'}
  emp_1.email()  : aarav@contractor.techcorp.in (uses shadowed instance attribute)
  emp_2.email()  : priya@techcorp.in (still uses class attribute!)

=== 3. Deleting the Shadow Restores Fallback to Class Variable ===
  After `del emp_1.company_domain`, emp_1.email() : aarav@techcorp.in
```

### Output — Example 3 (`example_03_mutable_class_variable_trap.py`)
```text
=== 1. The Mutable Class Variable Trap (`BuggyUserProfile`) ===
  u1 ('alice') roles : ['admin']
  u2 ('bob')   roles : ['admin']  <-- Bob accidentally became admin!
  u1.roles is u2.roles: True

=== 2. The Fix: Initialize Mutable Attributes Inside `__init__` ===
  s1 ('alice') roles : ['admin']
  s2 ('bob')   roles : []  <-- Clean and isolated!
  s1.roles is s2.roles: False
```

---

## 7. Code Explanation

1. **Incrementing a Class Counter (`example_01`):** Inside `__init__`, we wrote `CloudSubscription.active_subscriptions += 1` (or `type(self).active_subscriptions += 1`) instead of `self.active_subscriptions += 1`. Had we written `self.active_subscriptions += 1`, it would have read `0` from the class and created an instance variable `self.active_subscriptions = 1` on each instance without ever incrementing the class counter past `1`!
2. **Shadowing Mechanics (`example_02`):** Before `emp_1.company_domain = ...`, `emp_1.__dict__` only contains `{'username': 'aarav'}`. Assigning to `emp_1.company_domain` inserts `'company_domain'` into `emp_1.__dict__`, shadowing `EmployeeBadge.company_domain`.
3. **Mutable Class Variable Leak (`example_03`):** `u1.roles is u2.roles` is `True` in `BuggyUserProfile` because neither `u1` nor `u2` has `'roles'` in its own `__dict__`; both resolve to `BuggyUserProfile.roles`.

---

## 8. Common Mistakes

1. **Writing `self.count += 1` instead of `ClassName.count += 1` when updating an immutable class counter:**
   - `self.count += 1` expands to `self.count = self.count + 1`. The right side reads `ClassName.count`, and the left side creates an **instance variable** `self.count` on `self`, leaving `ClassName.count` unchanged!
2. **Putting `items = []` at the top of a class thinking it acts like a Java/C# field declaration:**
   - In Python, class-level assignments execute once when the `class` statement runs and create **shared class variables** (analogous to `static` fields in Java/C#), not per-instance fields!
3. **Trying to access an instance variable through the class (`CloudSubscription.tenant_name`):**
   - Instance variables live in `instance.__dict__`, not `Class.__dict__`, so `CloudSubscription.tenant_name` raises `AttributeError`.

---

## 9. Practice Questions

1. **Easy — Serial Number Auto-Incrementer:**
   Create a `SensorDevice` class with a class variable `_next_serial: int = 1000`. In `__init__(self, location: str)`, assign `self.serial_no = SensorDevice._next_serial` and increment `SensorDevice._next_serial` by `1` so every new sensor gets a unique sequential serial number.

2. **Medium — Per-Instance Tax Rate Override:**
   Create a `ProductItem(name: str, price: float)` class with a class variable `tax_rate: float = 0.18` and method `final_price(self) -> float`. Demonstrate overriding `tax_rate = 0.05` on a single tax-exempt medical product instance while other products continue using the class-level `0.18` rate, then restore the default on that instance using `del`.

3. **Hard — Subclass-Aware Instance Counter:**
   Using `type(self).instance_count += 1` vs `BaseClass.instance_count += 1`, demonstrate the difference when a subclass `PremiumAccount(BankAccount)` defines its own `instance_count = 0`.

---

## 10. Interview Questions

### Q1: What happens when you execute `self.x += 1` inside a method if `x = 10` is a class variable (`int`) vs if `x = [10]` is a class variable (`list`)?
**Answer:**
- If `x = 10` (`int`, **immutable**): `self.x += 1` evaluates `self.x + 1` (`11`) and assigns it to `self.x`, creating a new **instance variable** in `self.__dict__` while leaving `Class.x` at `10`.
- If `x = [10]` (`list`, **mutable**): `self.x += [20]` invokes `list.__iadd__`, which mutates the shared class list **in-place** (`[10, 20]`) AND also binds `'x'` in `self.__dict__` pointing to that same mutated list!

### Q2: Why do type annotations at the class body level (like `name: str` without `= value`) NOT create class variables?
**Answer:**
A bare type annotation `name: str` (with no `=` assignment) only adds an entry to `Class.__annotations__ = {'name': str}` for static type checkers (`mypy`) and `@dataclass`; it does **not** bind `"name"` in `Class.__dict__`. Only an assignment (`name: str = "default"`) creates a class variable.

### Q3: Should a method read a class variable via `self.gst_rate` or `CloudSubscription.gst_rate`?
**Answer:**
- Use **`self.gst_rate`** (or `type(self).gst_rate`) if you want subclasses or individual instances to be able to override `gst_rate` polymorphically.
- Use **`CloudSubscription.gst_rate`** only when you explicitly want to bypass instance/subclass overrides (or when mutating a class-wide counter shared by the entire hierarchy).
