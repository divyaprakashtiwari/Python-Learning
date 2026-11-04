# Phase 4 — Topic 11: Magic/Dunder Methods

## 1. Introduction

**Magic methods**—officially called **Special Methods** and affectionately pronounced **"Dunder" (Double UNDERscore) methods**—are hooks surrounded by double underscores (`__init__`, `__repr__`, `__eq__`, `__len__`, `__add__`, `__enter__`) that allow your custom classes to integrate seamlessly with Python's built-in syntax and standard library functions.

This design is the heart of the **Python Data Model**: you almost never call a dunder method directly (`v.__len__()`). Instead, you use Python's natural syntax (`len(v)`, `v1 + v2`, `v1 == v2`, `with session:`), and the Python interpreter invokes the corresponding dunder method behind the scenes!

---

## 2. Why is it used?

- **Debugging & Logging Clarity (`__repr__` & `__str__`):** Without `__repr__`, printing a custom object outputs a cryptic memory address (`<__main__.SemanticVersion object at 0x000001...>`). Implementing `__repr__` turns every log line, REPL output, and traceback into readable developer output.
- **Value Semantics & Hashing (`__eq__`, `__lt__`, `__hash__`):** Enables custom domain objects to be compared with `==`, sorted with `sorted()`, and stored as keys in `dict` or elements in `set`.
- **Natural Domain Syntax:** Mathematical objects (`Vector2D`, `Matrix`, `Money`) can use `+` and `*`; batch jobs or ML models can be called like functions (`model(inputs)` via `__call__`); resources can manage cleanup via `with` (`__enter__`/`__exit__`).

---

## 3. Syntax

```python
class Vector2D:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    # 1. String Representation (`repr(v)` and `str(v)`)
    def __repr__(self) -> str:
        return f"Vector2D({self.x}, {self.y})"

    # 2. Value Equality (`v1 == v2`)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2D):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    # 3. Binary Operator Overloading (`v1 + v2`)
    def __add__(self, other: "Vector2D") -> "Vector2D":
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)
```

---

## 4. Explanation (Step-by-Step)

### Step 1: `__repr__` vs `__str__`
| Dunder Method | Triggered By | Target Audience & Goal |
| :--- | :--- | :--- |
| **`__repr__(self)`** | `repr(obj)`, `f"{obj!r}"`, interactive REPL, and **printing inside lists/dicts** (`print([obj])`) | **Developers:** Unambiguous string—ideally valid Python code that could recreate the object (`SemanticVersion(3, 12, 0)`). **If you only implement one, implement `__repr__`** (because `str()` falls back to `__repr__` if `__str__` is missing!). |
| **`__str__(self)`** | `str(obj)`, `print(obj)`, `f"{obj}"` | **End Users:** Concise, human-friendly display (`v3.12.0`). |

### Step 2: The `__eq__` and `__hash__` Contract
- By default, custom classes inherit `object.__eq__` (identity `is`) and `object.__hash__`.
- **Critical Rule:** As soon as you define a custom `def __eq__(self, other):` on a class, **Python automatically sets `Class.__hash__ = None`**, making instances **unhashable** (`TypeError: unhashable type` if placed in a `set` or `dict` key)!
- Why? Because hash tables require the invariant: **`if a == b, then hash(a) == hash(b)`**. If your class is **immutable**, you can restore hashability by implementing `def __hash__(self) -> int: return hash((self._field1, self._field2))`. (Never implement `__hash__` on a mutable class whose equality fields can change!)

### Step 3: Returning `NotImplemented` (Not `NotImplementedError`!) in Binary Dunders
In `__eq__`, `__lt__`, `__add__`, or `__mul__`, when `other` is an unsupported type, return the singleton value **`NotImplemented`** (do **not** raise `NotImplementedError`!):
- Returning `NotImplemented` tells Python to try the **reflected dunder method** on the right-hand operand (`other.__radd__(self)` or `other.__rmul__(self)`), and only raise `TypeError` (or return `False` for `==`) if both sides return `NotImplemented`.

### Step 4: Essential Dunder Protocols Reference
| Protocol | Dunder Methods | Python Syntax Unlocked |
| :--- | :--- | :--- |
| **Representation** | `__repr__`, `__str__`, `__format__` | `repr(x)`, `str(x)`, `print(x)`, `f"{x}"` |
| **Comparison & Hashing** | `__eq__`, `__lt__`, `__le__`, `__gt__`, `__ge__`, `__hash__` | `==`, `<`, `sorted()`, `set`, `dict` keys |
| **Arithmetic** | `__add__`, `__radd__`, `__sub__`, `__mul__`, `__rmul__`, `__abs__` | `a + b`, `a - b`, `a * k`, `k * a`, `abs(a)` |
| **Truthiness** | `__bool__` (falls back to `__len__ != 0`) | `if obj:`, `bool(obj)` |
| **Container / Sequence** | `__len__`, `__getitem__`, `__setitem__`, `__contains__`, `__iter__` | `len(c)`, `c[i]`, `c[i] = v`, `x in c`, `for x in c:` |
| **Callable Object** | `__call__` | `obj(arg1, arg2)` |
| **Context Manager** | `__enter__`, `__exit__` | `with obj as resource:` |

---

## 5. Minimum 3 Examples

### Example 1: String Representation (`__repr__` vs `__str__`) & Equality/Hashing (`__eq__`, `__hash__`)
File: `example_01_repr_str_eq_and_hash.py`

```python
class SemanticVersion:
    """Immutable semantic version `(major, minor, patch)` supporting `==`, `<`, `set`, and `dict`."""

    def __init__(self, major: int, minor: int, patch: int) -> None:
        self._major = major
        self._minor = minor
        self._patch = patch

    def _as_tuple(self) -> tuple[int, int, int]:
        return (self._major, self._minor, self._patch)

    def __repr__(self) -> str:
        """Developer representation (used in lists, dicts, REPL, and tracebacks)."""
        return f"SemanticVersion({self._major}, {self._minor}, {self._patch})"

    def __str__(self) -> str:
        """User-facing display string (used by `print(v)` and `f'{v}'`)."""
        return f"v{self._major}.{self._minor}.{self._patch}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        return self._as_tuple() == other._as_tuple()

    def __lt__(self, other: "SemanticVersion") -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        return self._as_tuple() < other._as_tuple()

    def __hash__(self) -> int:
        """Required when `__eq__` is defined so instances remain hashable in sets/dicts."""
        return hash(self._as_tuple())


def main() -> None:
    v1 = SemanticVersion(3, 12, 0)
    v2 = SemanticVersion(3, 12, 0)
    v3 = SemanticVersion(3, 13, 7)

    print("=== 1. `__str__` vs `__repr__` ===")
    print(f"  str(v1)   / f'{{v1}}'   : {v1}")
    print(f"  repr(v1)  / f'{{v1!r}}' : {v1!r}")
    print(f"  Inside a list [v1, v3]  : {[v1, v3]} (containers always use __repr__!)")

    print("\n=== 2. Value Equality (`__eq__`), Sorting (`__lt__`), and Hashing (`__hash__`) ===")
    print(f"  v1 == v2 : {v1 == v2} | v1 is v2 : {v1 is v2}")
    print(f"  Sorted   : {sorted([v3, v1])}")
    unique_versions = {v1, v2, v3}
    print(f"  Set deduplication len({{v1, v2, v3}}) : {len(unique_versions)} -> {unique_versions}")


if __name__ == "__main__":
    main()
```

---

### Example 2: Arithmetic Operators (`__add__`, `__mul__`, `__rmul__`) & Truthiness (`__bool__`)
File: `example_02_arithmetic_and_comparison_dunders.py`

```python
import math


class Vector2D:
    """2D Euclidean vector supporting `+`, scalar `*`, `abs()`, and `bool()`."""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector2D({self.x}, {self.y})"

    def __add__(self, other: "Vector2D") -> "Vector2D":
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> "Vector2D":
        """Handles `vec * 3.0`."""
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector2D":
        """Handles reflected `3.0 * vec` when left operand (`float`) returns NotImplemented."""
        return self.__mul__(scalar)

    def __abs__(self) -> float:
        """Handles `abs(vec)` -> Euclidean magnitude."""
        return math.hypot(self.x, self.y)

    def __bool__(self) -> bool:
        """Zero vector `Vector2D(0, 0)` is falsy; all other vectors are truthy."""
        return bool(self.x or self.y)


def main() -> None:
    v_a = Vector2D(3.0, 4.0)
    v_b = Vector2D(1.0, -2.0)
    v_zero = Vector2D(0.0, 0.0)

    print("=== 1. Arithmetic Dunder Methods (`+`, `*`, Reflected `__rmul__`) ===")
    print(f"  v_a + v_b   = {v_a + v_b}")
    print(f"  v_a * 2.5   = {v_a * 2.5}  (calls v_a.__mul__(2.5))")
    print(f"  2.5 * v_a   = {2.5 * v_a}  (calls v_a.__rmul__(2.5))")

    print("\n=== 2. Magnitude (`__abs__`) and Truthiness (`__bool__`) ===")
    print(f"  abs(v_a)    = {abs(v_a)} | bool(v_a)    = {bool(v_a)}")
    print(f"  abs(v_zero) = {abs(v_zero)} | bool(v_zero) = {bool(v_zero)}")


if __name__ == "__main__":
    main()
```

---

### Example 3: Container (`__len__`, `__getitem__`), Callable (`__call__`), and Context Manager (`__enter__`, `__exit__`)
File: `example_03_container_callable_and_context_dunders.py`

```python
from typing import Iterator


class BatchJobSession:
    """
    Demonstrates Container (`__len__`, `__getitem__`, `__iter__`),
    Callable (`__call__`), and Context Manager (`__enter__`, `__exit__`) dunders.
    """

    def __init__(self, session_name: str) -> None:
        self.session_name = session_name
        self._tasks: list[str] = []
        self.is_open: bool = False

    # 1. Context Manager Protocol (`with BatchJobSession(...) as session:`)
    def __enter__(self) -> "BatchJobSession":
        self.is_open = True
        print(f"  [__enter__] Opened session '{self.session_name}'")
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> bool:
        self.is_open = False
        print(f"  [__exit__ ] Closed session '{self.session_name}' ({len(self)} tasks queued)")
        return False  # Do not suppress exceptions

    # 2. Callable Protocol (`session("task_name")` adds a task)
    def __call__(self, task_name: str) -> None:
        if not self.is_open:
            raise RuntimeError("Cannot queue tasks when session is closed")
        self._tasks.append(task_name)

    # 3. Container Protocol (`len(session)`, `session[i]`, `for t in session`)
    def __len__(self) -> int:
        return len(self._tasks)

    def __getitem__(self, index: int) -> str:
        return self._tasks[index]

    def __iter__(self) -> Iterator[str]:
        return iter(self._tasks)


def main() -> None:
    print("=== Using `__enter__`, `__call__`, `__len__`, `__getitem__`, and `__exit__` ===")
    with BatchJobSession("Nightly-ETL") as job:
        # Calling the `job` object like a function invokes `job.__call__(...)`!
        job("extract_users")
        job("transform_orders")
        job("load_warehouse")

        print(f"  len(job)   : {len(job)}")
        print(f"  job[0]     : {job[0]!r}")
        print(f"  All tasks  : {list(job)}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_repr_str_eq_and_hash.py`)
```text
=== 1. `__str__` vs `__repr__` ===
  str(v1)   / f'{v1}'   : v3.12.0
  repr(v1)  / f'{v1!r}' : SemanticVersion(3, 12, 0)
  Inside a list [v1, v3]  : [SemanticVersion(3, 12, 0), SemanticVersion(3, 13, 7)] (containers always use __repr__!)

=== 2. Value Equality (`__eq__`), Sorting (`__lt__`), and Hashing (`__hash__`) ===
  v1 == v2 : True | v1 is v2 : False
  Sorted   : [SemanticVersion(3, 12, 0), SemanticVersion(3, 13, 7)]
  Set deduplication len({v1, v2, v3}) : 2 -> {SemanticVersion(3, 13, 7), SemanticVersion(3, 12, 0)}
```

### Output — Example 2 (`example_02_arithmetic_and_comparison_dunders.py`)
```text
=== 1. Arithmetic Dunder Methods (`+`, `*`, Reflected `__rmul__`) ===
  v_a + v_b   = Vector2D(4.0, 2.0)
  v_a * 2.5   = Vector2D(7.5, 10.0)  (calls v_a.__mul__(2.5))
  2.5 * v_a   = Vector2D(7.5, 10.0)  (calls v_a.__rmul__(2.5))

=== 2. Magnitude (`__abs__`) and Truthiness (`__bool__`) ===
  abs(v_a)    = 5.0 | bool(v_a)    = True
  abs(v_zero) = 0.0 | bool(v_zero) = False
```

### Output — Example 3 (`example_03_container_callable_and_context_dunders.py`)
```text
=== Using `__enter__`, `__call__`, `__len__`, `__getitem__`, and `__exit__` ===
  [__enter__] Opened session 'Nightly-ETL'
  len(job)   : 3
  job[0]     : 'extract_users'
  All tasks  : ['extract_users', 'transform_orders', 'load_warehouse']
  [__exit__ ] Closed session 'Nightly-ETL' (3 tasks queued)
```

---

## 7. Code Explanation

1. **Why Containers Use `__repr__` (`example_01`):** Even though `print(v1)` uses `__str__` (`v3.12.0`), printing a list `print([v1, v3])` always invokes `__repr__` on its elements (`[SemanticVersion(3, 12, 0), SemanticVersion(3, 13, 7)]`) so strings inside containers aren't ambiguous.
2. **Why `2.5 * v_a` Needs `__rmul__` (`example_02`):** In `2.5 * v_a`, Python first calls `(2.5).__mul__(v_a)` on `float`. Because `float` knows nothing about `Vector2D`, `float.__mul__` returns `NotImplemented`. Python then falls back to the reflected method `v_a.__rmul__(2.5)`!
3. **Context Manager `__exit__` Return Value (`example_03`):** Returning `False` (or `None`) from `__exit__` propagates any exception raised inside the `with` block; returning `True` suppresses the exception.

---

## 8. Common Mistakes

1. **Implementing `__str__` without implementing `__repr__`:**
   - If you only implement `__str__`, then `print(obj)` looks nice, but `print([obj])`, debugger watches, and tracebacks still display `<__main__.MyClass object at 0x...>`. Always implement `__repr__` first!
2. **Confusing `return NotImplemented` with `raise NotImplementedError`:**
   - In binary operator dunders (`__eq__`, `__add__`, `__lt__`), raising `NotImplementedError` crashes immediately instead of letting Python try the reflected operator on the right-hand operand. Return the singleton object `NotImplemented`.
3. **Inventing your own double-underscore method names (`def __my_custom_hook__(self):`):**
   - Names both starting and ending with `__` are reserved exclusively by the Python language specification for current and future dunder protocols. Never invent custom `__name__` methods.

---

## 9. Practice Questions

1. **Easy — `@functools.total_ordering` on `BookPageCount`:**
   Decorate a class `Book(title: str, pages: int)` with `@functools.total_ordering` and implement only `__repr__`, `__eq__`, and `__lt__`. Verify that `<=`, `>`, and `>=` work automatically.

2. **Medium — Stateful Retry Counter Using `__call__`:**
   Create a class `StatefulMultiplier(factor: float)` that tracks `self.call_count: int = 0` and implements `__call__(self, value: float) -> float` so an instance can be passed directly into `map(multiplier_obj, [1, 2, 3, 4])` while recording how many elements it processed.

3. **Hard — Custom Polynomial Class (`__add__`, `__call__`, `__repr__`, `__eq__`):**
   Create a `Polynomial(coeffs: list[float])` class where `p(x)` evaluates the polynomial at `x` via `__call__`, `p1 + p2` adds two polynomials via `__add__`, and `len(p)` returns the degree.

---

## 10. Interview Questions

### Q1: Why does a class become unhashable (`TypeError: unhashable type`) as soon as you define `__eq__` without defining `__hash__`?
**Answer:**
Hash tables (`dict` and `set`) rely on the strict invariant that **equal objects must have equal hashes** (`a == b` $\implies$ `hash(a) == hash(b)`). The default `object.__hash__` is based on memory address (`id(self)`). If you override `__eq__` to compare attribute values without updating `__hash__`, two distinct instances with identical attributes would have `a == b` (`True`) but `hash(a) != hash(b)`, corrupting dictionary/set lookups! Therefore, Python automatically sets `__hash__ = None` when `__eq__` is defined unless you explicitly define `__hash__`.

### Q2: If a class defines neither `__bool__` nor `__len__`, what is `bool(instance)`? What if it defines `__len__`?
**Answer:**
- If a class defines neither `__bool__` nor `__len__`, every instance is **truthy** (`bool(instance) is True`).
- If a class defines `__bool__`, `bool(instance)` calls `instance.__bool__()`.
- If a class does not define `__bool__` but defines `__len__`, `bool(instance)` falls back to **`len(instance) != 0`** (just like empty lists/dicts are falsy!).

### Q3: When `a + b` is evaluated in Python, what is the exact lookup sequence for `__add__` and `__radd__`?
**Answer:**
1. *(Special case first)*: If `type(b)` is a **proper subclass** of `type(a)` and overrides `__radd__`, Python calls `b.__radd__(a)` first so the more specialized subclass can control the operation.
2. Otherwise, Python calls `a.__add__(b)`.
3. If `a.__add__(b)` returns `NotImplemented` (and `type(a) is not type(b)`), Python calls `b.__radd__(a)`.
4. If that also returns `NotImplemented`, Python raises `TypeError: unsupported operand type(s) for +`.
