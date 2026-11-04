# Phase 4 — Topic 04: Instance, Class and Static Methods

## 1. Introduction

Inside a Python class, functions can be defined in three different ways depending on what implicit first argument they need:

1. **Instance Method (`def method(self, ...)`):** The default method type. Receives the **instance (`self`)** as its first parameter and can read or modify both instance attributes (`self.x`) and class attributes.
2. **Class Method (`@classmethod` + `def method(cls, ...)`):** Decorated with `@classmethod`. Receives the **class itself (`cls`)** as its first parameter—even when called on an instance! Used for alternative constructors (factories) and modifying class-level state.
3. **Static Method (`@staticmethod` + `def method(...)`):** Decorated with `@staticmethod`. Receives **neither `self` nor `cls`**. Behaves like a plain module function that lives inside the class namespace for logical grouping.

---

## 2. Why is it used?

- **Clear Intent:** A reader immediately knows that a `@staticmethod` will never mutate `self` or `cls`, whereas a `@classmethod` operates at the class level and an instance method operates on a specific object.
- **Inheritance-Safe Factories (`@classmethod`):** When a base class defines `@classmethod def from_packet(cls, ...): return cls(...)`, calling `TemperatureSensor.from_packet(...)` on a subclass automatically passes `cls = TemperatureSensor` and returns a `TemperatureSensor` instance!
- **Cohesive Domain Utilities (`@staticmethod`):** Format validators (`is_valid_ifsc`), checksum helpers, and unit converters that belong conceptually to a domain class can be called directly as `BankTransferValidator.is_valid_ifsc(code)` without instantiating a dummy object first.

---

## 3. Syntax

```python
class PaymentGateway:
    platform_fee_pct: float = 2.0

    def __init__(self, merchant_id: str) -> None:
        self.merchant_id = merchant_id

    # 1. Instance Method -> receives `self`
    def process_charge(self, amount: float) -> float:
        return amount * (1.0 - self.platform_fee_pct / 100.0)

    # 2. Class Method -> receives `cls`
    @classmethod
    def update_platform_fee(cls, new_fee_pct: float) -> None:
        cls.platform_fee_pct = new_fee_pct

    # 3. Static Method -> receives neither `self` nor `cls`
    @staticmethod
    def is_valid_card_amount(amount: float) -> bool:
        return 1.0 <= amount <= 500_000.0
```

---

## 4. Explanation (Step-by-Step)

### Comparison Matrix
| Feature | Instance Method | `@classmethod` | `@staticmethod` |
| :--- | :--- | :--- | :--- |
| **Decorator** | None | `@classmethod` | `@staticmethod` |
| **First Parameter** | `self` (the instance) | `cls` (the class) | None (only explicit args) |
| **Access Instance State (`self.x`)?** | Yes | No | No |
| **Access Class State (`cls.x`)?** | Yes (via `self` or `type(self)`) | Yes (via `cls`) | No (unless hardcoded) |
| **Callable on Class (`Class.m()`)?** | Only if `instance` passed manually | **Yes** (`cls` bound automatically) | **Yes** |
| **Callable on Instance (`obj.m()`)?** | **Yes** (`self` bound automatically) | **Yes** (`cls = type(obj)` bound) | **Yes** |
| **Primary Use Case** | Object behavior & state mutation | Alternative constructors & class state | Stateless validation / helper utilities |

---

## 5. Minimum 3 Examples

### Example 1: Side-by-Side Comparison (`self` vs `@classmethod cls` vs `@staticmethod`)
File: `example_01_comparing_three_method_types.py`

```python
class PaymentGateway:
    """Demonstrates all three method types in a payment processing service."""

    platform_fee_pct: float = 2.0

    def __init__(self, merchant_id: str, settlement_currency: str = "INR") -> None:
        self.merchant_id = merchant_id
        self.settlement_currency = settlement_currency

    # 1. INSTANCE METHOD: receives `self` (bound to a specific merchant instance)
    def process_charge(self, amount: float) -> str:
        if not self.is_valid_card_amount(amount):
            raise ValueError(f"Invalid charge amount: {amount}")
        fee = round(amount * (self.platform_fee_pct / 100.0), 2)
        net = round(amount - fee, 2)
        return (
            f"[{self.merchant_id}] Gross={self.settlement_currency} {amount:,.2f} | "
            f"Fee={fee:,.2f} ({self.platform_fee_pct}%) | Net={net:,.2f}"
        )

    # 2. CLASS METHOD: receives `cls` (the `PaymentGateway` class itself)
    @classmethod
    def update_platform_fee(cls, new_fee_pct: float) -> None:
        if new_fee_pct < 0 or new_fee_pct > 20:
            raise ValueError("Platform fee must be between 0% and 20%")
        cls.platform_fee_pct = new_fee_pct

    # 3. STATIC METHOD: receives neither `self` nor `cls` (pure validation helper)
    @staticmethod
    def is_valid_card_amount(amount: float) -> bool:
        return 1.0 <= amount <= 500_000.0


def main() -> None:
    print("=== 1. Calling `@staticmethod` Without Creating an Instance ===")
    print(f"  is_valid_card_amount(500.0) : {PaymentGateway.is_valid_card_amount(500.0)}")
    print(f"  is_valid_card_amount(0.25)  : {PaymentGateway.is_valid_card_amount(0.25)}")

    print("\n=== 2. Calling Instance Method (`process_charge`) ===")
    merchant = PaymentGateway("MERCH-88", "INR")
    print(f"  {merchant.process_charge(10000.0)}")

    print("\n=== 3. Calling `@classmethod` (`update_platform_fee`) ===")
    PaymentGateway.update_platform_fee(1.5)
    print(f"  After class-wide fee cut -> {merchant.process_charge(10000.0)}")


if __name__ == "__main__":
    main()
```

---

### Example 2: Why `@classmethod` Beats `@staticmethod` for Inheritance-Aware Factories
File: `example_02_classmethod_factories_and_inheritance.py`

```python
class BaseSensor:
    """Base IoT sensor with a `@classmethod` factory."""

    unit: str = "raw"

    def __init__(self, sensor_id: str, reading: float) -> None:
        self.sensor_id = sensor_id
        self.reading = reading

    @classmethod
    def from_packet(cls, packet: str) -> "BaseSensor":
        """`cls` dynamically refers to whichever subclass invoked `from_packet`!"""
        sensor_id, val_str = packet.split(":")
        return cls(sensor_id.strip(), float(val_str))

    def report(self) -> str:
        return f"[{self.__class__.__name__}] id={self.sensor_id} -> {self.reading} {self.unit}"


class TemperatureSensor(BaseSensor):
    """Subclass that inherits `from_packet` without rewriting it."""

    unit: str = "Celsius"


class PressureSensor(BaseSensor):
    """Another subclass that inherits `from_packet`."""

    unit: str = "kPa"


def main() -> None:
    print("=== `@classmethod` Factory Preserves Subclass Type Automatically ===")
    raw_sensor = BaseSensor.from_packet("SNS-01:42.0")
    temp_sensor = TemperatureSensor.from_packet("TMP-09:23.5")
    pres_sensor = PressureSensor.from_packet("PRS-04:101.3")

    for s in (raw_sensor, temp_sensor, pres_sensor):
        print(f"  {s.report():<52} | type={type(s).__name__}")


if __name__ == "__main__":
    main()
```

---

### Example 3: `@staticmethod` Validators/Checksums & Calling Them Polymorphically via `self`
File: `example_03_staticmethod_validators_and_utilities.py`

```python
class BankTransferValidator:
    """Groups stateless banking format & checksum algorithms with stateful transfer rules."""

    def __init__(self, daily_limit: float) -> None:
        self.daily_limit = daily_limit

    @staticmethod
    def is_valid_ifsc(code: str) -> bool:
        """
        Standard Indian IFSC format:
          - Exactly 11 characters
          - First 4 chars: uppercase letters (bank code)
          - 5th char: always '0'
          - Last 6 chars: alphanumeric (branch code)
        """
        return (
            len(code) == 11
            and code[:4].isalpha()
            and code[:4].isupper()
            and code[4] == "0"
            and code[5:].isalnum()
        )

    def validate_transfer(self, ifsc: str, amount: float) -> tuple[bool, str]:
        """Instance method combining `@staticmethod` format check + instance `daily_limit`."""
        if not self.is_valid_ifsc(ifsc):
            return False, f"Invalid IFSC format: {ifsc!r}"
        if amount <= 0 or amount > self.daily_limit:
            return False, f"Amount {amount:,.2f} exceeds daily limit {self.daily_limit:,.2f}"
        return True, f"Valid transfer of INR {amount:,.2f} to {ifsc}"


def main() -> None:
    print("=== 1. Direct Call on Class (`BankTransferValidator.is_valid_ifsc`) ===")
    for sample in ("SBIN0001234", "HDFC0123456", "sbin0001234", "SBIN1001234"):
        print(f"  IFSC {sample!r:<14} -> valid={BankTransferValidator.is_valid_ifsc(sample)}")

    print("\n=== 2. Instance Method Calling `@staticmethod` via `self` ===")
    validator = BankTransferValidator(daily_limit=100_000.0)
    for ifsc, amt in (("SBIN0001234", 45000.0), ("SBIN0001234", 250000.0), ("BADIFSC", 500.0)):
        ok, msg = validator.validate_transfer(ifsc, amt)
        print(f"  [{'OK' if ok else 'ERR':<3}] {msg}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_comparing_three_method_types.py`)
```text
=== 1. Calling `@staticmethod` Without Creating an Instance ===
  is_valid_card_amount(500.0) : True
  is_valid_card_amount(0.25)  : False

=== 2. Calling Instance Method (`process_charge`) ===
  [MERCH-88] Gross=INR 10,000.00 | Fee=200.00 (2.0%) | Net=9,800.00

=== 3. Calling `@classmethod` (`update_platform_fee`) ===
  After class-wide fee cut -> [MERCH-88] Gross=INR 10,000.00 | Fee=150.00 (1.5%) | Net=9,850.00
```

### Output — Example 2 (`example_02_classmethod_factories_and_inheritance.py`)
```text
=== `@classmethod` Factory Preserves Subclass Type Automatically ===
  [BaseSensor] id=SNS-01 -> 42.0 raw                   | type=BaseSensor
  [TemperatureSensor] id=TMP-09 -> 23.5 Celsius        | type=TemperatureSensor
  [PressureSensor] id=PRS-04 -> 101.3 kPa              | type=PressureSensor
```

### Output — Example 3 (`example_03_staticmethod_validators_and_utilities.py`)
```text
=== 1. Direct Call on Class (`BankTransferValidator.is_valid_ifsc`) ===
  IFSC 'SBIN0001234'  -> valid=True
  IFSC 'HDFC0123456'  -> valid=True
  IFSC 'sbin0001234'  -> valid=False
  IFSC 'SBIN1001234'  -> valid=False

=== 2. Instance Method Calling `@staticmethod` via `self` ===
  [OK ] Valid transfer of INR 45,000.00 to SBIN0001234
  [ERR] Amount 250,000.00 exceeds daily limit 100,000.00
  [ERR] Invalid IFSC format: 'BADIFSC'
```

---

## 7. Code Explanation

1. **Calling `@staticmethod` via `self` (`example_01` & `example_03`):** Inside `validate_transfer(self, ...)`, we called `self.is_valid_ifsc(ifsc)` instead of `BankTransferValidator.is_valid_ifsc(ifsc)`. Calling via `self` allows a subclass (e.g., `InternationalTransferValidator`) to override `is_valid_ifsc` if needed!
2. **Polymorphic `cls` in `@classmethod` (`example_02`):** When `TemperatureSensor.from_packet("TMP-09:23.5")` is called, `cls` inside `BaseSensor.from_packet` is `TemperatureSensor`, so `return cls(...)` constructs a `TemperatureSensor` instance with `unit = "Celsius"`.

---

## 8. Common Mistakes

1. **Adding `self` as the first parameter of a `@staticmethod`:**
   - Because `@staticmethod` disables automatic `self` binding, declaring `def is_valid(self, x):` under `@staticmethod` makes `self` a required first positional argument from the caller!
2. **Using `@staticmethod` for factory methods (`from_json`) instead of `@classmethod`:**
   - Hardcoding `return BaseSensor(...)` inside a `@staticmethod` means `TemperatureSensor.from_packet(...)` will return a `BaseSensor` instead of a `TemperatureSensor`. Always use `@classmethod` (`cls(...)`) for factories.
3. **Writing an instance method that never uses `self`:**
   - If a method never touches `self`, mark it `@staticmethod` (or move it to a module-level function) so callers don't have to instantiate an object just to call it.

---

## 9. Practice Questions

1. **Easy — Distance Converter Class:**
   Create a `Distance(meters: float)` class with:
   - An instance method `to_kilometers(self) -> float`
   - A `@classmethod` `from_miles(cls, miles: float) -> "Distance"` ($1 \text{ mile} = 1609.34 \text{ m}$)
   - A `@staticmethod` `is_positive_distance(val: float) -> bool`

2. **Medium — Password Policy Manager:**
   Create a `PasswordPolicy` class with a class variable `min_length = 8`, a `@classmethod` `set_min_length(cls, length: int)`, and a `@staticmethod` `has_special_char(text: str) -> bool`. Combine them in an instance method `check_user_password(self, username: str, password: str) -> bool` that also checks `username.lower() not in password.lower()`.

3. **Hard — Inheritable Document Parser Factory:**
   Create `Document(content: str)` and subclass `MarkdownDocument(Document)` where `@classmethod def from_lines(cls, lines: list[str])` joins lines and returns an instance of whichever class called it.

---

## 10. Interview Questions

### Q1: What is the difference between `@classmethod` and `@staticmethod` in Python?
**Answer:**
- **`@classmethod`** binds the first parameter to the **class (`cls`)** on which the method was called (`Class.method()` or `instance.method()`). It can access/modify class variables and instantiate `cls(...)` polymorphically across subclasses.
- **`@staticmethod`** binds **no** implicit first argument (`self` or `cls`). It is a regular function namespaced inside a class body that cannot access instance or class state unless passed explicitly.

### Q2: Can you call a `@classmethod` or `@staticmethod` on an instance (`obj.my_classmethod()`)?
**Answer:**
**Yes!**
- Calling `obj.my_classmethod()` automatically extracts `type(obj)` and passes it as `cls`.
- Calling `obj.my_staticmethod()` simply invokes the static function without passing `obj` or `type(obj)`.

### Q3: When should you use a `@staticmethod` vs a plain module-level function?
**Answer:**
- Use a **module-level function** when the helper is used by multiple classes in the module or is part of the module's general API.
- Use a **`@staticmethod`** when the helper is tightly coupled to a single class's domain concept (like `BankTransferValidator.is_valid_ifsc`) or when you want subclasses to be able to override the helper via `self.helper()`.
