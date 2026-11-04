# Phase 4 — Topic 08: Encapsulation

## 1. Introduction

**Encapsulation** is the Object-Oriented Programming principle of bundling data (attributes) and the methods that operate on that data inside a single class while **restricting direct, unvalidated external modification of internal state**.

Unlike Java or C++ (which enforce strict `public`, `protected`, and `private` compiler keywords), Python follows the philosophy *"We are all consenting adults here"* and achieves encapsulation through:
1. **Naming Conventions & Name Mangling:** `public`, `_protected` (single leading underscore), and `__private` (double leading underscore $\rightarrow$ `_ClassName__private`).
2. **Managed Attributes (`@property` & `@<name>.setter`):** Intercepting dot-notation attribute reads and writes (`node.gpu_count = 8`) with validation logic.
3. **Defensive Read-Only Views:** Returning immutable tuples or copies so external code cannot mutate internal lists or dictionaries in-place.

---

## 2. Why is it used?

- **Protecting Class Invariants:** Prevents external callers from setting invalid state (such as `node.gpu_count = -5` or mutating an internal `_tickers` list with invalid symbols).
- **Zero-Breakage Refactoring (`@property`):** You can start with a simple public attribute (`self.gpu_count = gpu_count`) and later convert it into a validated `@property` **without changing a single call site** across your codebase!
- **Preventing Subclass Attribute Collisions (`__private`):** Double-underscore name mangling ensures a subclass that accidentally defines `self.__pin_code` will not overwrite the parent class's `_SmartCardWallet__pin_code`.

---

## 3. Syntax

```python
class CloudGpuInstance:
    def __init__(self, instance_id: str, gpu_count: int) -> None:
        self._instance_id = instance_id  # Protected internal backing attribute
        self.gpu_count = gpu_count       # Calls `@gpu_count.setter`!

    # 1. Read-only property (Getter only)
    @property
    def instance_id(self) -> str:
        return self._instance_id

    # 2. Managed property (Getter + Validated Setter)
    @property
    def gpu_count(self) -> int:
        return self._gpu_count

    @gpu_count.setter
    def gpu_count(self, value: int) -> None:
        if value not in (1, 2, 4, 8):
            raise ValueError("gpu_count must be 1, 2, 4, or 8")
        self._gpu_count = value
```

---

## 4. Explanation (Step-by-Step)

### Step 1: Python's Three Visibility Tiers
| Naming Pattern | Example | Meaning in Python |
| :--- | :--- | :--- |
| **Public** | `self.card_id` | Part of the official public API; safe for anyone to read/use. |
| **Protected (Convention)** | `self._failed_attempts` | Internal implementation detail for this class and its subclasses. Linters (`pyright`/`flake8` rule `SLF001`) warn if external code accesses it. |
| **Private (Name Mangled)** | `self.__pin_code` | Automatically rewritten by the Python compiler to **`self._ClassName__pin_code`** so subclasses cannot accidentally override or collide with it. |

*(Note: Name mangling happens only when an identifier has **at least two leading underscores and at most one trailing underscore**, so dunder methods like `__init__` are never mangled.)*

### Step 2: Why `@property` Beats Java-Style `get_x()` / `set_x()`
In Java, developers must write `.getGpuCount()` and `.setGpuCount(8)` everywhere from day one just in case validation is needed later.
In Python, you expose clean attribute syntax `node.gpu_count`. When you decorate `def gpu_count(self)` with `@property`, Python creates a **data descriptor** on the class that intercepts:
- `node.gpu_count` $\rightarrow$ calls the `@property` getter
- `node.gpu_count = 8` $\rightarrow$ calls the `@gpu_count.setter` method
- `del node.gpu_count` $\rightarrow$ calls `@gpu_count.deleter` (if defined)

### Step 3: Protecting Internal Mutable Collections
Even if `self._tickers` is marked private/protected and exposed via a read-only `@property def tickers(self): return self._tickers`, a caller who runs `portfolio.tickers.append("BAD")` mutates the underlying list in-place!
- **Fix:** Return `tuple(self._tickers)` (or `self._tickers.copy()`, or `types.MappingProxyType(self._dict)` for dictionaries) from the property getter.

---

## 5. Minimum 3 Examples

### Example 1: Access Conventions (`public`, `_protected`, and `__private` Name Mangling)
File: `example_01_public_protected_and_name_mangling.py`

```python
class SmartCardWallet:
    """Demonstrates Python's 3-tier attribute visibility conventions."""

    def __init__(self, card_id: str, pin_code: str) -> None:
        self.card_id = card_id  # 1. Public attribute
        self._failed_attempts = 0  # 2. Protected attribute (convention)
        self.__pin_code = pin_code  # 3. Private attribute (name-mangled)

    def verify_pin(self, entered_pin: str) -> bool:
        """Public method providing controlled access to `__pin_code`."""
        if self._failed_attempts >= 3:
            return False
        if entered_pin == self.__pin_code:
            self._failed_attempts = 0
            return True
        self._failed_attempts += 1
        return False


def main() -> None:
    wallet = SmartCardWallet("CARD-7700", "4829")

    print("=== 1. Public and Protected Access ===")
    print(f"  Public `wallet.card_id`           : {wallet.card_id}")
    print(f"  Protected `wallet._failed_attempts`: {wallet._failed_attempts}")
    print(f"  verify_pin('0000') (wrong)        : {wallet.verify_pin('0000')}")
    print(f"  verify_pin('4829') (correct)      : {wallet.verify_pin('4829')}")

    print("\n=== 2. Direct Access to `__pin_code` Fails Due to Name Mangling ===")
    try:
        print(wallet.__pin_code)
    except AttributeError as err:
        print(f"  Caught expected AttributeError: {err}")

    print("\n=== 3. Inspecting Mangled Name in `wallet.__dict__` ===")
    print(f"  wallet.__dict__ keys : {list(wallet.__dict__.keys())}")
    # Name mangling prevents accidental collisions; it is not cryptographic security:
    print(f"  Mangled `_SmartCardWallet__pin_code` : {wallet._SmartCardWallet__pin_code!r}")


if __name__ == "__main__":
    main()
```

---

### Example 2: Pythonic Getters & Setters Using `@property` and `@<name>.setter`
File: `example_02_property_getters_and_setters.py`

```python
class CloudGpuInstance:
    """Encapsulates GPU count and hourly rate with validated `@property` descriptors."""

    def __init__(self, instance_id: str, gpu_count: int, hourly_rate_usd: float) -> None:
        self._instance_id = instance_id
        # Assigning to `self.gpu_count` inside `__init__` invokes the `@gpu_count.setter`!
        self.gpu_count = gpu_count
        self.hourly_rate_usd = hourly_rate_usd

    @property
    def instance_id(self) -> str:
        """Read-only property (no setter defined)."""
        return self._instance_id

    @property
    def gpu_count(self) -> int:
        """Getter for `gpu_count`."""
        return self._gpu_count

    @gpu_count.setter
    def gpu_count(self, value: int) -> None:
        """Validated setter for `gpu_count`."""
        if value not in (1, 2, 4, 8):
            raise ValueError(f"gpu_count must be 1, 2, 4, or 8 (got {value})")
        self._gpu_count = value

    @property
    def daily_cost_usd(self) -> float:
        """Computed read-only property derived from live state."""
        return round(self._gpu_count * self.hourly_rate_usd * 24, 2)


def main() -> None:
    print("=== 1. Reading and Updating `@property` via Clean Dot Syntax ===")
    node = CloudGpuInstance("gpu-a100-01", gpu_count=2, hourly_rate_usd=3.50)
    print(f"  Instance {node.instance_id}: {node.gpu_count} GPUs -> Daily Cost: ${node.daily_cost_usd:,.2f}")

    node.gpu_count = 8
    print(f"  Scaled to {node.gpu_count} GPUs            -> Daily Cost: ${node.daily_cost_usd:,.2f}")

    print("\n=== 2. Setter Rejects Invalid Values (`ValueError`) ===")
    try:
        node.gpu_count = 3
    except ValueError as err:
        print(f"  Caught expected ValueError: {err}")

    print("\n=== 3. Read-Only Property Rejects Reassignment (`AttributeError`) ===")
    try:
        node.instance_id = "hacked-id"
    except AttributeError as err:
        print(f"  Caught expected AttributeError: {err}")


if __name__ == "__main__":
    main()
```

---

### Example 3: Preventing Internal Collection Mutation (Defensive Copying & Read-Only Views)
File: `example_03_encapsulating_internal_collections.py`

```python
class InvestmentPortfolio:
    """Protects its internal holdings list from unauthorized external mutation."""

    def __init__(self, owner: str) -> None:
        self.owner = owner
        self._tickers: list[str] = []

    def add_ticker(self, symbol: str) -> None:
        cleaned = symbol.strip().upper()
        if not cleaned.isalpha() or len(cleaned) > 10:
            raise ValueError(f"Invalid ticker symbol: {symbol!r}")
        if cleaned not in self._tickers:
            self._tickers.append(cleaned)

    @property
    def tickers_leaky(self) -> list[str]:
        """DANGEROUS: Returns direct reference to internal `_tickers` list!"""
        return self._tickers

    @property
    def tickers(self) -> tuple[str, ...]:
        """SAFE: Returns an immutable `tuple` snapshot so callers cannot mutate `_tickers`."""
        return tuple(self._tickers)


def main() -> None:
    portfolio = InvestmentPortfolio("Divya")
    portfolio.add_ticker("TCS")
    portfolio.add_ticker("INFY")

    print("=== 1. Safe Encapsulated Property (`portfolio.tickers` -> `tuple`) ===")
    safe_view = portfolio.tickers
    print(f"  portfolio.tickers : {safe_view} (type: {type(safe_view).__name__})")

    print("\n=== 2. Demonstrating Why Returning Raw Internal Lists Breaks Encapsulation ===")
    portfolio.tickers_leaky.append("999_INVALID_TICKER!!!")
    print(f"  After external `.append()` on leaky property : {portfolio.tickers}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_public_protected_and_name_mangling.py`)
```text
=== 1. Public and Protected Access ===
  Public `wallet.card_id`           : CARD-7700
  Protected `wallet._failed_attempts`: 0
  verify_pin('0000') (wrong)        : False
  verify_pin('4829') (correct)      : True

=== 2. Direct Access to `__pin_code` Fails Due to Name Mangling ===
  Caught expected AttributeError: 'SmartCardWallet' object has no attribute '__pin_code'

=== 3. Inspecting Mangled Name in `wallet.__dict__` ===
  wallet.__dict__ keys : ['card_id', '_failed_attempts', '_SmartCardWallet__pin_code']
  Mangled `_SmartCardWallet__pin_code` : '4829'
```

### Output — Example 2 (`example_02_property_getters_and_setters.py`)
```text
=== 1. Reading and Updating `@property` via Clean Dot Syntax ===
  Instance gpu-a100-01: 2 GPUs -> Daily Cost: $168.00
  Scaled to 8 GPUs            -> Daily Cost: $672.00

=== 2. Setter Rejects Invalid Values (`ValueError`) ===
  Caught expected ValueError: gpu_count must be 1, 2, 4, or 8 (got 3)

=== 3. Read-Only Property Rejects Reassignment (`AttributeError`) ===
  Caught expected AttributeError: property 'instance_id' of 'CloudGpuInstance' object has no setter
```

### Output — Example 3 (`example_03_encapsulating_internal_collections.py`)
```text
=== 1. Safe Encapsulated Property (`portfolio.tickers` -> `tuple`) ===
  portfolio.tickers : ('TCS', 'INFY') (type: tuple)

=== 2. Demonstrating Why Returning Raw Internal Lists Breaks Encapsulation ===
  After external `.append()` on leaky property : ('TCS', 'INFY', '999_INVALID_TICKER!!!')
```

---

## 7. Code Explanation

1. **Assigning to Property Inside `__init__` (`example_02`):** Notice that inside `CloudGpuInstance.__init__`, we wrote `self.gpu_count = gpu_count` (without an underscore), while inside `@gpu_count.setter` we wrote `self._gpu_count = value` (with an underscore). That means validation runs automatically both during `__init__` AND on any later assignment!
2. **Name Mangling (`example_01`):** `self.__pin_code` is stored in `wallet.__dict__` under the key `'_SmartCardWallet__pin_code'`.

---

## 8. Common Mistakes

1. **Infinite Recursion Inside a `@property` Getter or Setter:**
   ```python
   @property
   def price(self) -> float:
       return self.price  # <-- INFINITE RECURSION! Calls getter `self.price` forever!
   ```
   Always store the backing value in a differently named attribute with a single leading underscore (`return self._price`).
2. **Assigning `wallet.__pin_code = "0000"` from outside the class thinking it updates the private attribute:**
   - Outside the `SmartCardWallet` class body, `wallet.__pin_code = "0000"` is **not** mangled! It simply creates a brand-new public attribute literally named `'__pin_code'` in `wallet.__dict__`, leaving `wallet._SmartCardWallet__pin_code` completely unchanged!
3. **Overusing `__private` (double underscore) everywhere instead of `_protected` (single underscore):**
   - Double underscore makes legitimate subclassing and unit-testing painful. PEP 8 recommends using single leading underscore `_attr` for 95% of non-public attributes, reserving `__attr` only when a class is designed to be subclassed and you want to prevent name clashes.

---

## 9. Practice Questions

1. **Easy — Validated `ExamScore` Property:**
   Create an `ExamScore` class with a `marks` `@property` and `@marks.setter` that enforces `0 <= marks <= 100` (raising `ValueError` otherwise) and a read-only `@property` `grade -> str` (`"A"` for $\ge 90$, `"B"` for $\ge 75$, etc.).

2. **Medium — Temperature Synchronization (`celsius` and `fahrenheit` Properties):**
   Create a `Thermometer` class backed by a single private `_celsius: float` attribute, exposing both `celsius` and `fahrenheit` with `@property` and `.setter` so updating either property automatically updates `_celsius`.

3. **Hard — Read-Only Dictionary View (`types.MappingProxyType`):**
   Create a `FeatureFlagStore` class holding `self._flags: dict[str, bool] = {}` and expose a `@property def flags(self) -> MappingProxyType[str, bool]` so callers can read `store.flags["dark_mode"]` in $O(1)$ time without copying the dict, while `store.flags["dark_mode"] = True` raises `TypeError`.

---

## 10. Interview Questions

### Q1: Does `__attr` (double leading underscore) make an attribute truly inaccessible from outside the class in Python?
**Answer:**
**No.** Python performs **name mangling**, rewriting `__attr` inside class `MyClass` to `_MyClass__attr` at compile time. Anyone outside the class can still access `obj._MyClass__attr`. The purpose of name mangling is **preventing accidental attribute name collisions in subclasses**, not security or access control.

### Q2: Why does `self.price = price` inside `__init__` trigger `@price.setter` instead of creating `'price'` in `self.__dict__`?
**Answer:**
Because `@property` creates a **data descriptor** (an object on the class that defines both `__get__` and `__set__`). In Python's descriptor lookup protocol, **data descriptors on the class take precedence over `self.__dict__`** on attribute read and attribute assignment!

### Q3: What happens if two methods in `@property` and `@price.setter` have different names (e.g., `def price(self)` and `@price.setter def set_price(self, val)`)?
**Answer:**
If the setter function is named `set_price` instead of `price`, the `@price.setter` decorator returns a modified property object and binds it to the name `set_price`, leaving `price` as a read-only property! The getter, setter, and deleter methods **must all share the exact same method name** (`def price(...)`).
