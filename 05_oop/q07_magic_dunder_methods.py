"""
Topic 05: Object-Oriented Programming (OOP)
Question 07: Magic / Dunder Methods (Deep Dive)

Master Python's data model and special dunder methods:
- Representation and formatting: __repr__, __str__, and custom __format__ specifiers
- Rich comparisons (__lt__, __eq__) with functools.total_ordering
- Arithmetic dunders: forward (__add__), reflected/right-hand (__radd__), and in-place (__iadd__)
- Container protocol: __len__, __getitem__, __setitem__, __delitem__, and __contains__
- Iteration protocol: __iter__ and __next__ with StopIteration
- Callable instances with __call__ (stateful function objects)
- Context manager protocol: __enter__ and __exit__ with exception suppression
- Attribute interception: __getattr__ vs __getattribute__ and avoiding recursion in __setattr__
- Type conversion dunders: __bool__, __int__, __float__
- Production-grade Custom DataSeries entity supporting vectorized math and slice filtering
"""

import functools
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union


# ============================================================
# Q1: String Conversion & Custom Formatting (__format__)
# ============================================================
# Question: Implement a `Currency` class supporting `__str__`, `__repr__`, and
# custom formatting codes in `__format__` (e.g. `f"{price:USD}"`, `f"{price:EUR}"`).

print("=== Q1: __repr__, __str__, and Custom __format__ ===")

class Currency:
    CONVERSIONS_TO_USD = {"USD": 1.0, "EUR": 1.08, "GBP": 1.25, "INR": 0.012}

    def __init__(self, amount: float, code: str = "USD"):
        self.amount = float(amount)
        self.code = code.upper()

    def __repr__(self) -> str:
        return f"Currency({self.amount!r}, {self.code!r})"

    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.code}"

    def __format__(self, format_spec: str) -> str:
        """Handles custom format specs like f'{val:EUR}' or f'{val:.2f}'."""
        if not format_spec:
            return str(self)
        
        target_code = format_spec.upper()
        if target_code in self.CONVERSIONS_TO_USD:
            # Convert self to USD, then from USD to target currency
            usd_val = self.amount * self.CONVERSIONS_TO_USD.get(self.code, 1.0)
            target_val = usd_val / self.CONVERSIONS_TO_USD[target_code]
            return f"{target_val:.2f} {target_code}"
        
        # Fall back to standard numeric formatting on amount
        return format(self.amount, format_spec)

price = Currency(100.0, "USD")

print(f"  str(price):       '{str(price)}'")
print(f"  repr(price):      '{repr(price)}'")
print(f"  Formatted to EUR: '{price:EUR}'")
print(f"  Formatted to GBP: '{price:GBP}'")

assert str(price) == "100.00 USD"
assert repr(price) == "Currency(100.0, 'USD')"
assert f"{price:EUR}" == "92.59 EUR"
assert f"{price:GBP}" == "80.00 GBP"

# Explanation: `__format__` is invoked by `format(obj, spec)` and f-strings `f"{obj:spec}"`,
# allowing objects to define their own custom formatting grammar.


# ============================================================
# Q2: Rich Comparisons & functools.total_ordering
# ============================================================
# Question: Implement a `Version` class (`Major.Minor.Patch`). Use `functools.total_ordering`
# by defining only `__eq__` and `__lt__`, and demonstrate that all 6 operators work.

print("\n=== Q2: Rich Comparisons with @total_ordering ===")

@functools.total_ordering
class Version:
    def __init__(self, major: int, minor: int, patch: int):
        self.version_tuple = (major, minor, patch)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return self.version_tuple == other.version_tuple

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return self.version_tuple < other.version_tuple

    def __repr__(self) -> str:
        return f"Version({self.version_tuple[0]}, {self.version_tuple[1]}, {self.version_tuple[2]})"

v1 = Version(1, 2, 0)
v2 = Version(1, 2, 1)
v3 = Version(2, 0, 0)
v1_copy = Version(1, 2, 0)

# All 6 comparison operators derived automatically!
assert v1 < v2
assert v1 <= v2
assert v1 == v1_copy
assert v2 > v1
assert v3 >= v2
assert v1 != v3

# Sorting versions uses __lt__
sorted_versions = sorted([v3, v1, v2])
print(f"  Sorted versions: {sorted_versions}")
assert sorted_versions == [v1, v2, v3]

# Explanation: `@functools.total_ordering` automatically generates `__le__`, `__gt__`,
# and `__ge__` from `__eq__` and `__lt__`, avoiding repetitive comparison boilerplate.


# ============================================================
# Q3: Arithmetic: Forward (__add__), Reflected (__radd__), In-Place (__iadd__)
# ============================================================
# Question: Implement a 2D Vector class supporting:
# 1) Vector + Vector (__add__)
# 2) Vector + scalar (__add__)
# 3) scalar + Vector (__radd__)
# 4) Vector += Vector (__iadd__)

print("\n=== Q3: Arithmetic, Reflected, and In-Place Dunders ===")

class Vector:
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    # 1. Forward addition: self + other
    def __add__(self, other: Union["Vector", float, int]) -> "Vector":
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        elif isinstance(other, (int, float)):
            return Vector(self.x + other, self.y + other)
        return NotImplemented

    # 2. Reflected addition: other + self (when other does not know how to add Vector)
    def __radd__(self, other: Union[float, int]) -> "Vector":
        return self.__add__(other)

    # 3. In-place addition: self += other (mutates self and returns self)
    def __iadd__(self, other: Union["Vector", float, int]) -> "Vector":
        if isinstance(other, Vector):
            self.x += other.x
            self.y += other.y
            return self
        elif isinstance(other, (int, float)):
            self.x += other
            self.y += other
            return self
        return NotImplemented

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

vec1 = Vector(2.0, 3.0)
vec2 = Vector(5.0, 1.0)

# Vector + Vector
v_sum = vec1 + vec2
print(f"  vec1 + vec2:       {v_sum}")
assert v_sum.x == 7.0 and v_sum.y == 4.0

# Vector + scalar
v_plus_num = vec1 + 10
print(f"  vec1 + 10:         {v_plus_num}")
assert v_plus_num.x == 12.0 and v_plus_num.y == 13.0

# Reflected: scalar + Vector (Python calls Vector.__radd__)
v_reflected = 100 + vec1
print(f"  100 + vec1:        {v_reflected}")
assert v_reflected.x == 102.0 and v_reflected.y == 103.0

# In-place addition (identity preserved)
initial_id = id(vec1)
vec1 += Vector(10.0, 10.0)
print(f"  vec1 after +=:     {vec1} (Same instance: {id(vec1) == initial_id})")
assert vec1.x == 12.0 and vec1.y == 13.0
assert id(vec1) == initial_id

# Explanation: If `a + b` fails (`a.__add__(b)` returns `NotImplemented`),
# Python tries reflected addition `b.__radd__(a)`. In-place `__iadd__` mutates without reallocating.


# ============================================================
# Q4: Container Protocol (__len__, __getitem__, __setitem__, __delitem__, __contains__)
# ============================================================
# Question: Implement a custom indexed collection `CustomDictionary` that supports
# length check, key/slice indexing, mutation, deletion, and membership (`in`).

print("\n=== Q4: Container Protocol Dunders ===")

class CustomDictionary:
    def __init__(self, **initial_data: Any):
        self._data: Dict[str, Any] = dict(initial_data)

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __delitem__(self, key: str) -> None:
        del self._data[key]

    def __contains__(self, key: Any) -> bool:
        return key in self._data

store = CustomDictionary(host="localhost", port=8080)

# 1. __len__
assert len(store) == 2

# 2. __getitem__ & __setitem__
store["timeout"] = 30
assert store["timeout"] == 30

# 3. __contains__
assert "host" in store
assert "password" not in store

# 4. __delitem__
del store["port"]
assert "port" not in store
assert len(store) == 2

print(f"  Container dunders successfully implemented (len={len(store)}).")

# Explanation: Emulating container protocols enables custom classes to participate
# seamlessly in standard Python idioms (`len()`, `[]`, `del`, `in`).


# ============================================================
# Q5: Iteration Protocol (__iter__ and __next__)
# ============================================================
# Question: Build a `FibonacciSequence` generator class using `__iter__` and `__next__`.
# Enforce an iteration limit using `StopIteration`.

print("\n=== Q5: Iteration Protocol (__iter__ & __next__) ===")

class FibonacciSequence:
    def __init__(self, limit_count: int):
        self.limit = limit_count
        self.count = 0
        self.a = 0
        self.b = 1

    def __iter__(self) -> "FibonacciSequence":
        """An iterable returns an iterator (here self)."""
        return self

    def __next__(self) -> int:
        """Returns the next element or raises StopIteration when exhausted."""
        if self.count >= self.limit:
            raise StopIteration
        
        val = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return val

fib_gen = FibonacciSequence(7)
fib_numbers = list(fib_gen)

print(f"  First 7 Fibonacci numbers via __iter__/__next__: {fib_numbers}")
assert fib_numbers == [0, 1, 1, 2, 3, 5, 8]

# Verify StopIteration when called past exhaustion
caught_stop = False
try:
    next(fib_gen)
except StopIteration:
    caught_stop = True
assert caught_stop

# Explanation: The Python iterator protocol requires `__iter__()` (returns the iterator object)
# and `__next__()` (returns successive items or raises `StopIteration`).


# ============================================================
# Q6: Callable Objects with __call__
# ============================================================
# Question: Implement a stateful rate-limiting function object using `__call__`.
# Show how instances can be called like standard functions `limiter()`.

print("\n=== Q6: Callable Instances via __call__ ===")

class ExecutionCounter:
    def __init__(self, max_allowed: int):
        self.max_allowed = max_allowed
        self.total_calls = 0

    def __call__(self, task_name: str) -> str:
        """Invoked when instance is called like a function: obj(args)."""
        if self.total_calls >= self.max_allowed:
            raise RuntimeError(f"Quota exceeded! Maximum {self.max_allowed} calls reached.")
        
        self.total_calls += 1
        return f"Executed task '{task_name}' (Call #{self.total_calls})"

# Instance acts as a function
counter_fn = ExecutionCounter(max_allowed=2)

r1 = counter_fn("Data Ingestion")
r2 = counter_fn("Index Build")

print(f"  Call 1: {r1}")
print(f"  Call 2: {r2}")
assert counter_fn.total_calls == 2

# 3rd call exceeds quota
caught_quota = False
try:
    counter_fn("Cleanup")
except RuntimeError as err:
    caught_quota = True
    print(f"  Caught expected quota error: {err}")

assert caught_quota
assert callable(counter_fn)

# Explanation: Implementing `__call__` allows instances of classes to be called as functions.
# This is widely used for stateful closures, middleware, and ML models (`model(inputs)`).


# ============================================================
# Q7: Context Manager Protocol (__enter__ and __exit__)
# ============================================================
# Question: Build a custom context manager `TemporarySilence` that suppresses
# specific exception types by returning `True` from `__exit__`.

print("\n=== Q7: Context Managers & Exception Suppression ===")

class TemporarySilence:
    def __init__(self, *suppress_types: type):
        self.suppress_types = suppress_types
        self.suppressed_exception: Optional[BaseException] = None

    def __enter__(self) -> "TemporarySilence":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None and issubclass(exc_type, self.suppress_types):
            self.suppressed_exception = exc_val
            # Returning True SUPPRESSES the exception!
            return True
        # Returning False allows the exception to propagate
        return False

# 1. Suppress ZeroDivisionError
with TemporarySilence(ZeroDivisionError) as silence:
    val = 10 / 0  # Would crash standard code!

print(f"  Suppressed exception cleanly: {silence.suppressed_exception}")
assert isinstance(silence.suppressed_exception, ZeroDivisionError)

# 2. Unhandled exception propagates
caught_unhandled = False
try:
    with TemporarySilence(ZeroDivisionError):
        raise KeyError("Unsuppressed error")
except KeyError:
    caught_unhandled = True

assert caught_unhandled

# Explanation: `__enter__` prepares the runtime context. `__exit__` receives any exception details.
# Returning `True` from `__exit__` swallows the exception; returning `False` re-raises it.


# ============================================================
# Q8: Attribute Access Hooks: __getattr__ vs __getattribute__ vs __setattr__
# ============================================================
# Question: Demonstrate the difference between:
# 1) `__getattr__`: called ONLY when an attribute is NOT found in `__dict__`
# 2) `__getattribute__`: called unconditionally for EVERY attribute access
# Avoid infinite recursion when implementing `__setattr__`.

print("\n=== Q8: Attribute Interception Dunders ===")

class FallbackDictionaryRecord:
    def __init__(self):
        # Must use super().__setattr__ or self.__dict__ to avoid infinite recursion!
        super().__setattr__("_store", {"existing_key": 42})

    def __getattr__(self, name: str) -> Any:
        """Called ONLY when name is NOT present on the instance."""
        store = self.__dict__.get("_store", {})
        if name in store:
            return store[name]
        return f"DYNAMIC_FALLBACK_{name.upper()}"

    def __setattr__(self, name: str, value: Any) -> None:
        """Intercepts all attribute assignments."""
        if name == "_store":
            super().__setattr__(name, value)
        else:
            self._store[name] = value

rec = FallbackDictionaryRecord()

# 1. Reading existing attribute
rec.title = "Python Deep Dive"
print(f"  Existing attribute:  rec.title = '{rec.title}'")
assert rec.title == "Python Deep Dive"

# 2. Reading missing attribute triggers __getattr__
fallback_val = rec.non_existent_field
print(f"  Missing attribute:   rec.non_existent_field = '{fallback_val}'")
assert fallback_val == "DYNAMIC_FALLBACK_NON_EXISTENT_FIELD"

# Explanation: `__getattr__` is a safe fallback for missing attributes.
# Inside `__setattr__`, calling `self.name = value` causes infinite recursion;
# always delegate to `super().__setattr__(name, value)`.


# ============================================================
# Q9: Type Conversion Dunders (__bool__, __int__, __float__)
# ============================================================
# Question: Implement boolean truthiness (`__bool__`) and numeric conversions (`__int__`, `__float__`)
# for a `Measurement` object.

print("\n=== Q9: Type Conversion Dunders ===")

class Measurement:
    def __init__(self, value_cm: float):
        self.value_cm = float(value_cm)

    def __bool__(self) -> bool:
        """False if measurement is zero or negative; True otherwise."""
        return self.value_cm > 0.0

    def __int__(self) -> int:
        return int(self.value_cm)

    def __float__(self) -> float:
        return float(self.value_cm)

m_pos = Measurement(15.7)
m_zero = Measurement(0.0)

print(f"  bool(m_pos):   {bool(m_pos)} (15.7 cm > 0)")
print(f"  bool(m_zero):  {bool(m_zero)} (0.0 cm is False)")
print(f"  int(m_pos):    {int(m_pos)}")
print(f"  float(m_pos):  {float(m_pos)}")

assert bool(m_pos) is True
assert bool(m_zero) is False
assert int(m_pos) == 15
assert float(m_pos) == 15.7

# Explanation: `__bool__` determines how objects evaluate in `if obj:` conditionals.
# If `__bool__` is not defined, Python falls back to `__len__()` (0 is False, >0 is True).


# ============================================================
# Q10: Production-Grade Custom DataSeries Object
# ============================================================
# Question: Implement a miniature Pandas-like `DataSeries` entity that implements:
# 1) Vectorized addition, multiplication (`series + 5`, `series * 2`)
# 2) Positional & slice indexing (`series[0]`, `series[1:3]`)
# 3) Boolean masking (`series[series > 10]`)
# 4) Formatting and aggregation statistics

print("\n=== Q10: Domain Entity: DataSeries Object ===")

class DataSeries:
    def __init__(self, values: List[float], label: str = "series"):
        self.values = [float(v) for v in values]
        self.label = label

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, item: Any) -> Any:
        if isinstance(item, slice):
            return DataSeries(self.values[item], label=f"{self.label}_slice")
        elif isinstance(item, list) and all(isinstance(b, bool) for b in item):
            # Boolean indexing mask!
            filtered = [val for val, mask in zip(self.values, item) if mask]
            return DataSeries(filtered, label=f"{self.label}_filtered")
        return self.values[item]

    def __gt__(self, threshold: float) -> List[bool]:
        """Vectorized comparison: returns list of booleans."""
        return [v > threshold for v in self.values]

    def __add__(self, other: Union[float, int, "DataSeries"]) -> "DataSeries":
        if isinstance(other, (int, float)):
            return DataSeries([v + other for v in self.values], label=self.label)
        elif isinstance(other, DataSeries):
            if len(self) != len(other):
                raise ValueError("Series lengths must match for addition")
            return DataSeries([a + b for a, b in zip(self.values, other.values)], label=self.label)
        return NotImplemented

    def __repr__(self) -> str:
        return f"DataSeries({self.values}, label='{self.label}')"

    def mean(self) -> float:
        return round(sum(self.values) / len(self.values), 2) if self.values else 0.0

s1 = DataSeries([10.0, 25.0, 5.0, 40.0], label="metrics")

# 1. Vectorized scalar addition: s1 + 5
s_plus_5 = s1 + 5
print(f"  Vectorized + 5: {s_plus_5.values}")
assert s_plus_5.values == [15.0, 30.0, 10.0, 45.0]

# 2. Slice indexing: s1[1:3]
s_slice = s1[1:3]
print(f"  Slice [1:3]:    {s_slice.values}")
assert s_slice.values == [25.0, 5.0]

# 3. Vectorized comparison & Boolean masking: s1[s1 > 15]
mask = s1 > 15.0
print(f"  Mask (s1 > 15): {mask}")
assert mask == [False, True, False, True]

filtered_series = s1[mask]
print(f"  Filtered (>15): {filtered_series.values}")
assert filtered_series.values == [25.0, 40.0]
assert filtered_series.mean() == 32.5

print("\nAll 10 magic dunder method questions executed and asserted successfully!")
