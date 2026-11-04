# Phase 4 — Topic 10: Method Overriding

## 1. Introduction

**Method Overriding** occurs when a subclass defines a method (or `@property`) with the **exact same name** as a method in its parent class, allowing the subclass to customize, replace, or extend the inherited behavior.

When a method is called on an object (`order.calculate_total()`), Python uses **Dynamic Dispatch**: it looks up `calculate_total` starting from `type(order)` at runtime, so the subclass's overridden version executes instead of the parent's version.

---

## 2. Why is it used?

- **Specializing Behavior Without Duplicating Code:** An `ExpressAirOrder` can reuse `StandardShippingOrder.calculate_total()` via `super().calculate_total()` and simply add its priority air surcharge on top.
- **Customizing Framework Hooks:** Web frameworks (Django class-based views), GUI toolkits, and unit-test runners (`unittest.TestCase.setUp`) rely on subclasses overriding specific hook methods.
- **Static Safety with `@typing.override` (Python 3.12+):** Decorating overridden methods with `@override` lets static type checkers catch typos if the parent method is ever renamed or removed.

---

## 3. Syntax

```python
from typing import override


class StandardShippingOrder:
    def calculate_total(self) -> float:
        return self.subtotal + (self.weight_kg * 50.0)


class ExpressAirOrder(StandardShippingOrder):
    # Cooperative Extension Override using `@override` and `super()`
    @override
    def calculate_total(self) -> float:
        base_total = super().calculate_total()
        return base_total + 350.0
```

---

## 4. Explanation (Step-by-Step)

### Step 1: Two Styles of Method Overriding
1. **Complete Replacement Override:** The subclass method computes and returns a new result without calling `super()`.
2. **Cooperative Extension Override:** The subclass method calls `super().method_name(...)` first (or last) to preserve the parent's logic and builds upon it.

### Step 2: How Dynamic Dispatch Works When a Parent Method Calls `self.helper()`
Suppose `BaseReportGenerator.generate(self)` is inherited (not overridden) by `CustomPDFReportGenerator`, and inside `generate(self)`, it calls `self.format_header()`.
When `pdf_gen.generate()` is called:
1.What is `type(self)` inside `BaseReportGenerator.generate(self)`? **`CustomPDFReportGenerator`!**
2. Therefore, `self.format_header()` searches `CustomPDFReportGenerator.__mro__` from the very beginning and invokes **`CustomPDFReportGenerator.format_header()`**!
3. Conversely, if `BaseReportGenerator` wants an internal helper that subclasses **cannot** accidentally override, naming it `__security_stamp` mangles it to `_BaseReportGenerator__security_stamp`, isolating it from `CustomPDFReportGenerator`.

### Step 3: The Liskov Substitution Principle (LSP) & `@typing.override`
When overriding a method:
- **Keep compatible parameters and return types:** If `BaseRateLimiter.check_quota(used: int)` returns `tuple[bool, int]`, an overridden `EnterpriseRateLimiter.check_quota` must also accept `int` and return `tuple[bool, int]` so polymorphic callers never crash.
- **Use `@typing.override` (Python 3.12+, PEP 698):** Explicitly marks a method as overriding an ancestor method so tools like `mypy` and `pyright` flag an error if you misspell the parent method name.

---

## 5. Minimum 3 Examples

### Example 1: Replacing vs Extending Parent Methods (`super().method()`)
File: `example_01_replacing_vs_extending_with_super.py`

```python
class StandardShippingOrder:
    """Base order with standard shipping calculation."""

    def __init__(self, order_id: str, subtotal: float, weight_kg: float) -> None:
        self.order_id = order_id
        self.subtotal = subtotal
        self.weight_kg = weight_kg

    def shipping_label(self) -> str:
        return f"[STANDARD-SURFACE] Order {self.order_id}"

    def calculate_total(self) -> float:
        """Base total = subtotal + INR 50 per kg shipping."""
        shipping_cost = self.weight_kg * 50.0
        return round(self.subtotal + shipping_cost, 2)


class ExpressAirOrder(StandardShippingOrder):
    """
    1. Replaces `shipping_label()` completely.
    2. Extends `calculate_total()` by calling `super().calculate_total()` + air surcharge.
    """

    def __init__(
        self,
        order_id: str,
        subtotal: float,
        weight_kg: float,
        priority_surcharge: float = 350.0,
    ) -> None:
        super().__init__(order_id, subtotal, weight_kg)
        self.priority_surcharge = priority_surcharge

    # 1. Complete Replacement Override
    def shipping_label(self) -> str:
        return f"[EXPRESS-AIR-PRIORITY] Order {self.order_id}"

    # 2. Cooperative Extension Override via `super()`
    def calculate_total(self) -> float:
        base_total = super().calculate_total()
        return round(base_total + self.priority_surcharge, 2)


def main() -> None:
    std_order = StandardShippingOrder("ORD-101", subtotal=2000.0, weight_kg=3.0)
    air_order = ExpressAirOrder("ORD-202", subtotal=2000.0, weight_kg=3.0)

    print("=== 1. Base Class Behavior (`StandardShippingOrder`) ===")
    print(f"  {std_order.shipping_label():<35} -> Total: INR {std_order.calculate_total():,.2f}")

    print("\n=== 2. Overridden Subclass Behavior (`ExpressAirOrder`) ===")
    print(f"  {air_order.shipping_label():<35} -> Total: INR {air_order.calculate_total():,.2f}")


if __name__ == "__main__":
    main()
```

---

### Example 2: Dynamic Dispatch Trap (Parent Method Calling an Overridden Child Method)
File: `example_02_dynamic_dispatch_and_self_lookup.py`

```python
class BaseReportGenerator:
    """Base class whose `generate()` calls `self.format_header()` and `self.__security_stamp()`."""

    def format_header(self) -> str:
        return "=== BASE REPORT ==="

    def __security_stamp(self) -> str:
        """Private name-mangled method (`_BaseReportGenerator__security_stamp`)."""
        return "STAMP:VERIFIED-BASE"

    def generate(self) -> str:
        # `self.format_header()` is dispatched dynamically on `type(self)`!
        # `self.__security_stamp()` is mangled to `_BaseReportGenerator__security_stamp`!
        return f"{self.format_header()} | {self.__security_stamp()}"


class CustomPDFReportGenerator(BaseReportGenerator):
    """Overrides `format_header()` and defines its own `__security_stamp()`."""

    def format_header(self) -> str:
        return "=== CUSTOM PDF REPORT ==="

    def __security_stamp(self) -> str:
        """Mangled to `_CustomPDFReportGenerator__security_stamp` (does NOT override base!)."""
        return "STAMP:UNVERIFIED-CHILD"


def main() -> None:
    print("=== Dynamic Dispatch on `self.format_header()` vs Name-Mangled `__security_stamp()` ===")
    base_gen = BaseReportGenerator()
    pdf_gen = CustomPDFReportGenerator()

    print(f"  base_gen.generate() : {base_gen.generate()}")
    print(f"  pdf_gen.generate()  : {pdf_gen.generate()}")
    print("  Notice `pdf_gen.generate()` used Child's `format_header()`,")
    print("  but kept Base's `__security_stamp()` due to name mangling!")


if __name__ == "__main__":
    main()
```

---

### Example 3: The Liskov Substitution Principle (LSP) & `@typing.override` (Python 3.12+)
File: `example_03_liskov_substitution_and_override_decorator.py`

```python
from typing import override


class BaseRateLimiter:
    """Base rate limiter allowing 60 requests per minute."""

    @property
    def max_requests_per_min(self) -> int:
        return 60

    def check_quota(self, used_requests: int) -> tuple[bool, int]:
        """Return `(is_allowed, remaining_quota)`."""
        remaining = max(0, self.max_requests_per_min - used_requests)
        return used_requests < self.max_requests_per_min, remaining


class EnterpriseRateLimiter(BaseRateLimiter):
    """Overrides the `max_requests_per_min` property and extends `check_quota`."""

    def __init__(self, burst_bonus: int = 200) -> None:
        self.burst_bonus = burst_bonus

    @property
    @override
    def max_requests_per_min(self) -> int:
        return 1000 + self.burst_bonus

    @override
    def check_quota(self, used_requests: int) -> tuple[bool, int]:
        # Preserves exact input/output contract `(bool, int)` required by LSP
        return super().check_quota(used_requests)


def simulate_traffic(limiter: BaseRateLimiter, current_load: int) -> None:
    """Works seamlessly with `BaseRateLimiter` or any LSP-compliant subclass."""
    allowed, rem = limiter.check_quota(current_load)
    print(
        f"  [{type(limiter).__name__:<21}] load={current_load:<4} | "
        f"limit={limiter.max_requests_per_min:<4} -> allowed={allowed}, remaining={rem}"
    )


def main() -> None:
    print("=== Overriding `@property` & Methods with `@typing.override` (Python 3.12+) ===")
    free_tier = BaseRateLimiter()
    enterprise_tier = EnterpriseRateLimiter(burst_bonus=500)

    simulate_traffic(free_tier, 80)
    simulate_traffic(enterprise_tier, 80)


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_replacing_vs_extending_with_super.py`)
```text
=== 1. Base Class Behavior (`StandardShippingOrder`) ===
  [STANDARD-SURFACE] Order ORD-101    -> Total: INR 2,150.00

=== 2. Overridden Subclass Behavior (`ExpressAirOrder`) ===
  [EXPRESS-AIR-PRIORITY] Order ORD-202 -> Total: INR 2,500.00
```

### Output — Example 2 (`example_02_dynamic_dispatch_and_self_lookup.py`)
```text
=== Dynamic Dispatch on `self.format_header()` vs Name-Mangled `__security_stamp()` ===
  base_gen.generate() : === BASE REPORT === | STAMP:VERIFIED-BASE
  pdf_gen.generate()  : === CUSTOM PDF REPORT === | STAMP:VERIFIED-BASE
  Notice `pdf_gen.generate()` used Child's `format_header()`,
  but kept Base's `__security_stamp()` due to name mangling!
```

### Output — Example 3 (`example_03_liskov_substitution_and_override_decorator.py`)
```text
=== Overriding `@property` & Methods with `@typing.override` (Python 3.12+) ===
  [BaseRateLimiter      ] load=80   | limit=60   -> allowed=False, remaining=0
  [EnterpriseRateLimiter] load=80   | limit=1500 -> allowed=True, remaining=1420
```

---

## 7. Code Explanation

1. **Extending with `super()` (`example_01`):** `ExpressAirOrder.calculate_total()` calls `super().calculate_total()` (`2000 + 3 * 50 = 2150.0`) and adds `self.priority_surcharge` (`350.0`), producing `2500.0`.
2. **Name Mangling Prevents Override (`example_02`):** Inside `BaseReportGenerator.generate()`, `self.__security_stamp()` is compiled to `self._BaseReportGenerator__security_stamp()`, so defining `def __security_stamp(self)` in `CustomPDFReportGenerator` creates `_CustomPDFReportGenerator__security_stamp()` and does **not** override the parent's private method.
3. **Overriding a `@property` (`example_03`):** Even when `EnterpriseRateLimiter.check_quota()` calls `super().check_quota(used_requests)`, inside `BaseRateLimiter.check_quota` the expression `self.max_requests_per_min` dynamically dispatches to `EnterpriseRateLimiter.max_requests_per_min` (`1500`)!

---

## 8. Common Mistakes

1. **Accidentally calling `self.calculate_total()` instead of `super().calculate_total()` inside an overridden method:**
   - Calling `self.calculate_total()` inside `ExpressAirOrder.calculate_total()` calls the child method again, causing an immediate `RecursionError`!
2. **Narrowing accepted parameters in an overridden method (violating LSP):**
   - If `Parent.save(self, data: str, compress: bool = False)` accepts an optional `compress` parameter, and `Child.save(self, data: str)` drops `compress`, any caller passing `obj.save("hello", compress=True)` crashes with `TypeError` on `Child`!
3. **Misspelling the overridden method name (`def calcluate_total(self):`):**
   - Without `@typing.override`, a typo silently creates a brand-new method while leaving the parent method un-overridden.

---

## 9. Practice Questions

1. **Easy — Discounted Cart Override:**
   Create `ShoppingCart` with `total_price(self) -> float` and a subclass `VIPShoppingCart(ShoppingCart)` that overrides `total_price(self)` using `super().total_price()` to apply a 10% discount on orders above `INR 1000`.

2. **Medium — Logging File Writer Override:**
   Create `TextWriter` with `write_line(self, line: str) -> str` and `TimestampedTextWriter(TextWriter)` that overrides `write_line` by prepending `[2026-11-04]` before delegating to `super().write_line(...)`.

3. **Hard — Overriding Both Getter and Setter of a `@property` in a Subclass:**
   Create `Account` with a `balance` `@property` and `@balance.setter` (allowing any float), and a subclass `MinimumBalanceAccount(Account)` that overrides `@Account.balance.setter` to reject values below `1000.0` before calling `super(MinimumBalanceAccount, MinimumBalanceAccount).balance.__set__(self, value)`.

---

## 10. Interview Questions

### Q1: Look at `class A: def f(self): return self.g(); def g(self): return "A"` and `class B(A): def g(self): return "B"`. What does `B().f()` return, and why?
**Answer:**
It returns **`"B"`**!
When `B().f()` is invoked, `self` is the `B` instance. Inside `A.f(self)`, the expression `self.g()` looks up `"g"` starting from `type(self).__mro__` (`[B, A, object]`), finding `B.g` first.

### Q2: How does `class A: def f(self): return self.__g(); def __g(self): return "A"` and `class B(A): def __g(self): return "B"` change the output of `B().f()`?
**Answer:**
Now `B().f()` returns **`"A"`**!
Because `__g` starts with two underscores, Python mangles `self.__g()` inside class `A` to `self._A__g()`, and mangles `def __g` inside class `B` to `_B__g`. Thus `B`'s method does not override `_A__g`.

### Q3: What is the Liskov Substitution Principle ( the "L" in SOLID), and how does it apply to method overriding?
**Answer:**
Formulated by Barbara Liskov, LSP states that if `S` is a subtype of `T`, objects of type `T` may be replaced with objects of type `S` without altering the correctness of the program. For method overriding, this means a subclass method must accept **at least** the same inputs as the parent method (contravariance/compatibility of parameters), return a **compatible output type** (covariance of return types), and not strengthen preconditions or weaken postconditions.
