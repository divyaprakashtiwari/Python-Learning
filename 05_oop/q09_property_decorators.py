"""
Topic 05: Object-Oriented Programming (OOP)
Question 09: Property Decorators (Deep Dive)

Master Python properties and the descriptor protocol:
- Tripartite property anatomy: @property (getter), @setter, and @deleter
- Computed read-only attributes (dynamically calculated derived state)
- Lazy evaluation and caching with functools.cached_property & cache invalidation
- Type and range validation with boundary constraint enforcement
- Property inheritance: overriding getters and setters in subclasses
- Property factories: generating reusable validated properties
- The property descriptor anatomy (__get__, __set__, __delete__)
- Soft deprecation of legacy attributes using warnings.warn inside properties
- Multi-attribute dependent validation (relational invariant enforcement)
- Production-grade NetworkInterface entity with telemetry metrics and health scoring
"""

import functools
import time
import warnings
from typing import Any, Callable, Dict, List, Optional, Tuple


# ============================================================
# Q1: The Tripartite Property Anatomy (Getter, Setter, Deleter)
# ============================================================
# Question: Implement a `Person` class demonstrating all three property access hooks:
# getter (`@property`), setter (`@name.setter`), and deleter (`@name.deleter`).

print("=== Q1: Getter, Setter, and Deleter Anatomy ===")

class Person:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    # 1. Getter
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    # 2. Setter
    @full_name.setter
    def full_name(self, value: str) -> None:
        parts = value.strip().split(" ", 1)
        self.first_name = parts[0]
        self.last_name = parts[1] if len(parts) > 1 else ""

    # 3. Deleter
    @full_name.deleter
    def full_name(self) -> None:
        print("  [DELETER] Resetting full_name fields.")
        self.first_name = ""
        self.last_name = ""

p = Person("Guido", "van Rossum")

# Read via getter
print(f"  Full name (getter): '{p.full_name}'")
assert p.full_name == "Guido van Rossum"

# Mutate via setter
p.full_name = "Tim Peters"
print(f"  After setter:       first='{p.first_name}', last='{p.last_name}'")
assert p.first_name == "Tim"
assert p.last_name == "Peters"

# Delete via deleter
del p.full_name
assert p.full_name == ""
assert p.first_name == "" and p.last_name == ""

# Explanation: `@property` turns methods into attributes. The getter executes on read,
# `@prop.setter` executes on assignment (`=`), and `@prop.deleter` executes on `del`.


# ============================================================
# Q2: Computed Read-Only Derived Properties
# ============================================================
# Question: Implement a `Circle` class where `radius` is the primary state,
# while `diameter`, `circumference`, and `area` are computed read-only properties.

print("\n=== Q2: Computed Read-Only Properties ===")

import math

class Circle:
    def __init__(self, radius: float):
        self._radius = float(radius)

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = float(value)

    # Derived computed properties
    @property
    def diameter(self) -> float:
        return self._radius * 2.0

    @property
    def circumference(self) -> float:
        return round(2.0 * math.pi * self._radius, 2)

    @property
    def area(self) -> float:
        return round(math.pi * (self._radius ** 2), 2)

c = Circle(5.0)
print(f"  Radius: {c.radius}, Diameter: {c.diameter}, Area: {c.area}")
assert c.diameter == 10.0
assert c.circumference == 31.42
assert c.area == 78.54

# Update radius and verify derived properties immediately reflect new value
c.radius = 10.0
assert c.diameter == 20.0
assert c.area == 314.16

# Verify read-only enforcement on area
caught_area_write = False
try:
    c.area = 500.0  # type: ignore
except AttributeError:
    caught_area_write = True

assert caught_area_write

# Explanation: Computed properties prevent state desynchronization bugs by computing
# dependent values on-the-fly rather than caching duplicate variables.


# ============================================================
# Q3: Lazy Evaluation & Caching with functools.cached_property
# ============================================================
# Question: Use `@functools.cached_property` to lazily compute an expensive metric on first access,
# cache it in `__dict__`, and demonstrate cache invalidation via `del obj.property`.

print("\n=== Q3: functools.cached_property & Invalidation ===")

expensive_computations = 0

class LargeDatasetAnalyzer:
    def __init__(self, raw_data: List[int]):
        self.data = raw_data

    @functools.cached_property
    def heavy_aggregate_sum(self) -> int:
        global expensive_computations
        expensive_computations += 1
        # Simulate heavy CPU processing
        return sum(x ** 2 for x in self.data)

analyzer = LargeDatasetAnalyzer(list(range(100)))

# First access: calculates and caches
expensive_computations = 0
val1 = analyzer.heavy_aggregate_sum
assert expensive_computations == 1

# Second access: retrieved instantly from instance __dict__ without recomputing!
val2 = analyzer.heavy_aggregate_sum
assert expensive_computations == 1
assert val1 == val2

print(f"  First call computed: {val1} (computations: 1)")
print(f"  Second call cached:  {val2} (computations: 1)")

# Cache Invalidation: deleting the property name from instance clears the cache!
del analyzer.heavy_aggregate_sum
val3 = analyzer.heavy_aggregate_sum
print(f"  After cache invalidation: {val3} (recomputed!)")
assert expensive_computations == 2

# Explanation: `@functools.cached_property` computes once, stores the result in
# `instance.__dict__['name']`, and serves subsequent accesses at dictionary-lookup speed.


# ============================================================
# Q4: Type & Range Validation with Normalization
# ============================================================
# Question: Implement an `UserRegistration` entity that normalizes username (trimmed, lowercase)
# and validates that age is an integer between 13 and 120.

print("\n=== Q4: Validation & Normalization in Setters ===")

class UserRegistration:
    def __init__(self, username: str, age: int):
        self.username = username  # Triggers setter
        self.age = age            # Triggers setter

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, val: str) -> None:
        if not isinstance(val, str) or not val.strip():
            raise TypeError("Username must be a non-empty string")
        clean = val.strip().lower()
        if len(clean) < 3:
            raise ValueError("Username must be at least 3 characters long")
        self._username = clean

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, val: int) -> None:
        if not isinstance(val, int):
            raise TypeError(f"Age must be int, got {type(val).__name__}")
        if not (13 <= val <= 120):
            raise ValueError(f"Age {val} out of permitted range [13, 120]")
        self._age = val

user = UserRegistration("  ALICE_DEV  ", 28)
print(f"  Normalized username: '{user.username}', age: {user.age}")
assert user.username == "alice_dev"
assert user.age == 28

# Test invalid age boundary
caught_age_err = False
try:
    user.age = 10  # Below 13
except ValueError as err:
    caught_age_err = True
    print(f"  Caught invalid age error: {err}")

assert caught_age_err

# Explanation: Calling property setters inside `__init__` (`self.prop = val`)
# ensures that initialization logic shares identical validation guarantees with subsequent mutations.


# ============================================================
# Q5: Property Inheritance & Subclass Overriding
# ============================================================
# Question: Demonstrate how a subclass can override only a property getter or setter,
# while preserving the parent class implementation using `SuperClass.property.getter(...)`.

print("\n=== Q5: Property Inheritance & Overrides ===")

class BaseAccount:
    def __init__(self, balance: float):
        self._balance = float(balance)

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, val: float) -> None:
        if val < 0:
            raise ValueError("Negative balance not allowed in BaseAccount")
        self._balance = float(val)

class OverdraftAccount(BaseAccount):
    # Subclass permits balance down to -$500 overdraft
    @BaseAccount.balance.setter
    def balance(self, val: float) -> None:
        if val < -500.0:
            raise ValueError("Balance exceeds -$500 overdraft limit!")
        self._balance = float(val)

overdraft_acc = OverdraftAccount(100.0)
overdraft_acc.balance = -250.0  # Permitted in subclass!

print(f"  Overdraft balance: ${overdraft_acc.balance:.2f}")
assert overdraft_acc.balance == -250.0

# Exceeding overdraft limit
caught_overdraft_limit = False
try:
    overdraft_acc.balance = -600.0
except ValueError as err:
    caught_overdraft_limit = True
    print(f"  Caught overdraft limit: {err}")

assert caught_overdraft_limit

# Explanation: To override a property setter in a subclass without redefining the getter,
# use the syntax `@BaseClass.property_name.setter`.


# ============================================================
# Q6: Property Factories (Reusable Property Generators)
# ============================================================
# Question: Implement a reusable property factory `bounded_quantity(min_val, max_val)`
# that dynamically creates validated property descriptors without duplicate class code.

print("\n=== Q6: Property Factories ===")

def bounded_quantity(min_val: float, max_val: float):
    """Factory generating validated numeric properties."""
    def prop_decorator(storage_name: str) -> property:
        def getter(self: Any) -> float:
            return getattr(self, storage_name)

        def setter(self: Any, value: float) -> None:
            if not (min_val <= value <= max_val):
                raise ValueError(f"Value {value} out of bounds [{min_val}, {max_val}]")
            setattr(self, storage_name, float(value))

        return property(getter, setter)
    return prop_decorator

class VolumeControl:
    volume = bounded_quantity(0.0, 100.0)("_volume")
    bass = bounded_quantity(-10.0, 10.0)("_bass")

    def __init__(self, initial_vol: float = 50.0, initial_bass: float = 0.0):
        self.volume = initial_vol
        self.bass = initial_bass

stereo = VolumeControl(initial_vol=75.0, initial_bass=2.0)
print(f"  Initial Volume: {stereo.volume}, Bass: {stereo.bass}")
assert stereo.volume == 75.0
assert stereo.bass == 2.0

# Verify boundaries
caught_vol_err = False
try:
    stereo.volume = 120.0
except ValueError:
    caught_vol_err = True

assert caught_vol_err

# Explanation: Functions that return `property(getter, setter)` allow creating
# customized, parameterized descriptors without building full Descriptor classes.


# ============================================================
# Q7: The Property Descriptor Protocol (__get__, __set__, __delete__)
# ============================================================
# Question: Prove that Python's built-in `property` is itself a descriptor.
# Inspect `property.__get__`, `property.__set__`, and `property.__delete__`.

print("\n=== Q7: Property Descriptor Protocol Anatomy ===")

class SampleRecord:
    def __init__(self, value: int):
        self._val = value

    @property
    def val(self) -> int:
        return self._val

    @val.setter
    def val(self, new_val: int) -> None:
        self._val = new_val

prop_obj = SampleRecord.val
print(f"  SampleRecord.val type: {type(prop_obj).__name__}")

# Verify that property implements the full descriptor protocol
has_get = hasattr(prop_obj, "__get__")
has_set = hasattr(prop_obj, "__set__")
has_delete = hasattr(prop_obj, "__delete__")

print(f"  Implements __get__:    {has_get}")
print(f"  Implements __set__:    {has_set}")
print(f"  Implements __delete__: {has_delete}")

assert has_get and has_set and has_delete
assert isinstance(prop_obj, property)

# Explanation: A Python property is a data descriptor. When you write `x.prop`,
# Python translates it to `PropertyClass.prop.__get__(x, PropertyClass)`.


# ============================================================
# Q8: Soft Deprecation with warnings.warn in Properties
# ============================================================
# Question: Refactor an API entity where `cost` was renamed to `price`.
# Use a property to issue a `DeprecationWarning` when `cost` is accessed or modified,
# while maintaining full backwards compatibility.

print("\n=== Q8: Soft Deprecation via Properties ===")

class ProductItem:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = float(price)

    # Deprecated attribute 'cost' redirects to 'price' with warning
    @property
    def cost(self) -> float:
        warnings.warn(
            "'cost' is deprecated and will be removed in v3.0; use 'price' instead.",
            category=DeprecationWarning,
            stacklevel=2
        )
        return self.price

    @cost.setter
    def cost(self, val: float) -> None:
        warnings.warn(
            "Setting 'cost' is deprecated; use 'price' instead.",
            category=DeprecationWarning,
            stacklevel=2
        )
        self.price = float(val)

item = ProductItem("Laptop Stand", 45.0)

# Accessing legacy 'cost' emits warning
with warnings.catch_warnings(record=True) as caught_warnings:
    warnings.simplefilter("always")
    legacy_val = item.cost
    item.cost = 50.0

print(f"  Retrieved legacy cost: ${legacy_val:.2f}, updated price: ${item.price:.2f}")
print(f"  Captured DeprecationWarnings count: {len(caught_warnings)}")

assert legacy_val == 45.0
assert item.price == 50.0
assert len(caught_warnings) == 2
assert issubclass(caught_warnings[0].category, DeprecationWarning)

# Explanation: Properties allow non-breaking schema migrations, emitting warnings
# to nudge developers to update calls without breaking existing integration code.


# ============================================================
# Q9: Multi-Attribute Dependent Validation
# ============================================================
# Question: Implement a `DateRange` entity where updating either `start_date` or `end_date`
# automatically verifies that `end_date >= start_date`.

print("\n=== Q9: Cross-Attribute Dependent Validation ===")

class DateRange:
    def __init__(self, start_day: int, end_day: int):
        if end_day < start_day:
            raise ValueError(f"end_day ({end_day}) cannot precede start_day ({start_day})")
        self._start_day = start_day
        self._end_day = end_day

    @property
    def start_day(self) -> int:
        return self._start_day

    @start_day.setter
    def start_day(self, val: int) -> None:
        if val > self._end_day:
            raise ValueError(f"Cannot set start_day to {val}: exceeds current end_day {self._end_day}")
        self._start_day = val

    @property
    def end_day(self) -> int:
        return self._end_day

    @end_day.setter
    def end_day(self, val: int) -> None:
        if val < self._start_day:
            raise ValueError(f"Cannot set end_day to {val}: precedes current start_day {self._start_day}")
        self._end_day = val

dr = DateRange(5, 20)
dr.start_day = 10
dr.end_day = 25
print(f"  Valid DateRange: [{dr.start_day}..{dr.end_day}]")
assert dr.start_day == 10 and dr.end_day == 25

# Attempt invalid change: setting start_day after end_day
caught_range_err = False
try:
    dr.start_day = 30  # Exceeds end_day 25
except ValueError as err:
    caught_range_err = True
    print(f"  Caught range error: {err}")

assert caught_range_err

# Explanation: Properties can evaluate interdependent state across multiple instance attributes,
# upholding complex relational domain invariants.


# ============================================================
# Q10: Production-Grade Monitored Network Interface Entity
# ============================================================
# Question: Build a `NetworkInterface` entity with:
# - Read-only computed properties: total bytes transferred, error rate percentage, health status
# - Validated setters: link speed in Mbps
# - Telemetry metrics recording and status categorization

print("\n=== Q10: Domain Entity: Monitored NetworkInterface ===")

class NetworkInterface:
    def __init__(self, iface_name: str, speed_mbps: int = 1000):
        self.name = iface_name
        self.speed_mbps = speed_mbps  # Validated via setter
        self._rx_bytes: int = 0
        self._tx_bytes: int = 0
        self._errors: int = 0
        self._packets_total: int = 0

    @property
    def speed_mbps(self) -> int:
        return self._speed_mbps

    @speed_mbps.setter
    def speed_mbps(self, val: int) -> None:
        allowed_speeds = {10, 100, 1000, 10000, 40000, 100000}
        if val not in allowed_speeds:
            raise ValueError(f"Unsupported link speed: {val} Mbps. Allowed: {sorted(list(allowed_speeds))}")
        self._speed_mbps = val

    def record_traffic(self, rx: int, tx: int, packets: int, error_count: int = 0) -> None:
        """Simulate ingesting packet telemetry."""
        self._rx_bytes += rx
        self._tx_bytes += tx
        self._packets_total += packets
        self._errors += error_count

    @property
    def total_bytes(self) -> int:
        return self._rx_bytes + self._tx_bytes

    @property
    def total_megabytes(self) -> float:
        return round(self.total_bytes / (1024 * 1024), 2)

    @property
    def error_rate_percent(self) -> float:
        if self._packets_total == 0:
            return 0.0
        return round((self._errors / self._packets_total) * 100.0, 3)

    @property
    def health_status(self) -> str:
        """Derived health score based on link errors."""
        rate = self.error_rate_percent
        if rate == 0.0:
            return "OPTIMAL"
        elif rate < 1.0:
            return "DEGRADED"
        return "CRITICAL"

iface = NetworkInterface("eth0", speed_mbps=10000)
iface.record_traffic(rx=50_000_000, tx=70_000_000, packets=100_000, error_count=5)

print(f"  Interface:        {iface.name} ({iface.speed_mbps} Mbps)")
print(f"  Total Data:       {iface.total_megabytes} MB")
print(f"  Error Rate:       {iface.error_rate_percent}%")
print(f"  Health Status:    {iface.health_status}")

assert iface.total_bytes == 120_000_000
assert iface.total_megabytes == 114.44
assert iface.error_rate_percent == 0.005
assert iface.health_status == "DEGRADED"

# Test invalid link speed
caught_bad_speed = False
try:
    iface.speed_mbps = 555
except ValueError:
    caught_bad_speed = True

assert caught_bad_speed

print("\nAll 10 property decorator questions executed and asserted successfully!")
