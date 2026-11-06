# Phase 5 — Topic 16: Dataclasses

## 1. Introduction

**`@dataclass`** (from Python's built-in `dataclasses` module, PEP 557) is a class decorator that inspects class-level type annotations and automatically generates `__init__`, `__repr__`, `__eq__`, and optionally ordering methods (`__lt__`, `__le__`, `__gt__`, `__ge__`), hashing (`__hash__`), immutability (`frozen=True`), and `__slots__` (`slots=True`).

Dataclasses eliminate repetitive boilerplate in data-holding classes (DTOs, domain entities, configuration objects, and AST/tree nodes) while remaining regular Python classes that support methods, properties, and inheritance.

---

## 2. Why is it used?

1. **Zero Boilerplate Value Classes:** Turns 30 lines of repetitive `self.x = x`, `__repr__`, and `__eq__` code into 5 declarative lines.
2. **Built-In Safety Against Mutable Default Bugs:** Trying to write `tags: list[str] = []` inside a `@dataclass` raises `ValueError: mutable default <class 'list'> for field tags is not allowed: use default_factory` at class creation time!
3. **Immutable & Hashable Value Objects (`frozen=True`):** Generates `__hash__` and blocks attribute mutation, allowing instances to be used as `dict` keys or `set` members.
4. **Memory Optimization (`slots=True`, Python 3.10+):** Automatically generates `__slots__` from the annotated fields, cutting per-instance RAM footprint by ~40–50%.

---

## 3. Syntax

```python
from dataclasses import asdict, astuple, dataclass, field, replace

@dataclass(frozen=True, order=True, slots=True, kw_only=False)
class JobItem:
    priority: int
    name: str = field(compare=False)
    tags: tuple[str, ...] = field(default_factory=tuple, repr=False)

job = JobItem(1, "backup-db")
updated_job = replace(job, priority=0)
```

---

## 4. Explanation (Step-by-Step)

1. **What `@dataclass` Generates by Default (`init=True, repr=True, eq=True`):**
   - `__init__`: Accepts fields in declaration order.
   - `__repr__`: Formats `"ClassName(field1=val1, field2=val2)"`.
   - `__eq__`: Compares instances field-by-field as tuples of their attributes (`(self.f1, self.f2) == (other.f1, other.f2)`).
2. **`field(...)` Customization Options:**
   - `default_factory=callable`: Calls `callable()` (e.g., `list`, `dict`, `set`, `uuid.uuid4`) fresh for every new instance.
   - `repr=False`: Omits sensitive fields (like `api_key` or `password_hash`) from `__repr__` output.
   - `compare=False`: Excludes a field from `__eq__` and ordering (`<`, `>`) comparisons (ideal for priority queue items where only `priority` should be compared).
   - `init=False`: Excludes a computed field from `__init__` parameters so it can be populated inside `__post_init__`.
3. **Validation & Derived Attributes in `__post_init__(self)`:**
   - The generated `__init__` automatically calls `self.__post_init__()` as its very last step, making it the standard place to validate field invariants or compute derived attributes.

---

## 5. Minimum 3 Examples

### Example 01: `@dataclass` Fundamentals — Auto-Generated `__init__`, `__repr__`, and `__eq__`
File: [`example_01_dataclass_basics_init_repr_eq.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/16_Dataclasses/example_01_dataclass_basics_init_repr_eq.py)

```python
"""
Phase 5 - Topic 16: Dataclasses
Example 01: `@dataclass` Fundamentals — Auto-Generated `__init__`, `__repr__`, and `__eq__`

Demonstrates:
  - Eliminating boilerplate `__init__`, `__repr__`, and `__eq__` methods using `@dataclass`
  - Default field values and `dataclasses.asdict()` / `dataclasses.astuple()` conversion helpers
"""

from dataclasses import asdict, astuple, dataclass


@dataclass
class CourseModule:
    code: str
    title: str
    duration_hours: float = 2.5
    is_published: bool = True


def main() -> None:
    print("=== 1. Auto-Generated `__init__`, `__repr__`, and `__eq__` ===")
    m1 = CourseModule("PY-501", "Intermediate & Advanced Python", duration_hours=6.0)
    m2 = CourseModule("PY-501", "Intermediate & Advanced Python", duration_hours=6.0)
    print(f"  m1 repr        : {m1!r}")
    print(f"  m1 == m2       : {m1 == m2} (structural value equality, even though m1 is not m2!)")

    print("\n=== 2. Converting to `dict` and `tuple` (`asdict` / `astuple`) ===")
    print(f"  asdict(m1)     : {asdict(m1)}")
    print(f"  astuple(m1)    : {astuple(m1)}")


if __name__ == "__main__":
    main()
```

### Example 02: `field(default_factory=...)`, `__post_init__` Validation, & `repr=False`
File: [`example_02_field_default_factory_and_post_init.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/16_Dataclasses/example_02_field_default_factory_and_post_init.py)

```python
"""
Phase 5 - Topic 16: Dataclasses
Example 02: `field(default_factory=...)`, `__post_init__` Validation, & `InitVar`

Demonstrates:
  - Why `@dataclass` forbids mutable defaults (`tags: list[str] = []` raises `ValueError`)
    and how `field(default_factory=list)` gives each instance its own fresh list
  - Hiding sensitive fields from `__repr__` using `field(repr=False)`
  - Derived fields and validation in `__post_init__()`
"""

from dataclasses import dataclass, field


@dataclass
class APIClientConfig:
    base_url: str
    api_key: str = field(repr=False)
    timeout_sec: float = 10.0
    default_headers: list[str] = field(default_factory=list)
    normalized_url: str = field(init=False)

    def __post_init__(self) -> None:
        if self.timeout_sec <= 0:
            raise ValueError("timeout_sec must be positive")
        self.normalized_url = self.base_url.rstrip("/")


def main() -> None:
    print("=== 1. Safe Mutable Defaults (`default_factory=list`) & Hidden `repr=False` ===")
    c1 = APIClientConfig("https://api.example.com/", api_key="secret-token-123")
    c2 = APIClientConfig("https://auth.example.com/", api_key="secret-token-456")
    c1.default_headers.append("X-Request-ID")

    print(f"  c1 repr (api_key hidden!): {c1!r}")
    print(f"  c2 default_headers       : {c2.default_headers} (isolated from c1!)")

    print("\n=== 2. `__post_init__` Validation Guard ===")
    try:
        APIClientConfig("https://api.example.com", api_key="k", timeout_sec=-5.0)
    except ValueError as err:
        print(f"  Caught expected validation error: {err}")


if __name__ == "__main__":
    main()
```

### Example 03: Immutable, Hashable, Ordered, & Slotted Dataclasses (`frozen=True, order=True, slots=True`)
File: [`example_03_frozen_order_slots_and_replace.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/16_Dataclasses/example_03_frozen_order_slots_and_replace.py)

```python
"""
Phase 5 - Topic 16: Dataclasses
Example 03: Immutable, Hashable, Ordered, & Slotted Dataclasses (`frozen=True, order=True, slots=True`)

Demonstrates:
  - Creating immutable value objects (`frozen=True`) that can be used as `dict` keys or `set` members
  - Automatic comparison ordering (`order=True`) with `field(compare=False)` for non-sort fields
  - Memory/speed optimization via `slots=True` (Python 3.10+) and immutable updates via `replace()`
"""

from dataclasses import dataclass, field, replace


@dataclass(frozen=True, order=True, slots=True)
class PriorityTask:
    priority: int
    task_id: str = field(compare=False)


def main() -> None:
    print("=== 1. Sorting & Hashing with `@dataclass(frozen=True, order=True, slots=True)` ===")
    tasks = [
        PriorityTask(priority=3, task_id="cleanup-logs"),
        PriorityTask(priority=1, task_id="fix-prod-outage"),
        PriorityTask(priority=2, task_id="deploy-release"),
    ]
    print(f"  Sorted by priority : {sorted(tasks)}")
    task_set = {tasks[0], tasks[1]}
    print(f"  Usable in `set`?   : {len(task_set) == 2} | Has __dict__? {hasattr(tasks[0], '__dict__')}")

    print("\n=== 2. Creating Modified Clones of Frozen Dataclasses (`dataclasses.replace`) ===")
    escalated = replace(tasks[0], priority=0)
    print(f"  Original  : {tasks[0]}")
    print(f"  Escalated : {escalated}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== 1. Auto-Generated `__init__`, `__repr__`, and `__eq__` ===
  m1 repr        : CourseModule(code='PY-501', title='Intermediate & Advanced Python', duration_hours=6.0, is_published=True)
  m1 == m2       : True (structural value equality, even though m1 is not m2!)

=== 2. Converting to `dict` and `tuple` (`asdict` / `astuple`) ===
  asdict(m1)     : {'code': 'PY-501', 'title': 'Intermediate & Advanced Python', 'duration_hours': 6.0, 'is_published': True}
  astuple(m1)    : ('PY-501', 'Intermediate & Advanced Python', 6.0, True)
```

### Output — Example 02
```text
=== 1. Safe Mutable Defaults (`default_factory=list`) & Hidden `repr=False` ===
  c1 repr (api_key hidden!): APIClientConfig(base_url='https://api.example.com/', timeout_sec=10.0, default_headers=['X-Request-ID'], normalized_url='https://api.example.com')
  c2 default_headers       : [] (isolated from c1!)

=== 2. `__post_init__` Validation Guard ===
  Caught expected validation error: timeout_sec must be positive
```

### Output — Example 03
```text
=== 1. Sorting & Hashing with `@dataclass(frozen=True, order=True, slots=True)` ===
  Sorted by priority : [PriorityTask(priority=1, task_id='fix-prod-outage'), PriorityTask(priority=2, task_id='deploy-release'), PriorityTask(priority=3, task_id='cleanup-logs')]
  Usable in `set`?   : True | Has __dict__? False

=== 2. Creating Modified Clones of Frozen Dataclasses (`dataclasses.replace`) ===
  Original  : PriorityTask(priority=3, task_id='cleanup-logs')
  Escalated : PriorityTask(priority=0, task_id='cleanup-logs')
```

---

## 7. Code Explanation

1. **`asdict(m1)` and `astuple(m1)` (Example 01):** Recursively convert dataclass instances (including nested dataclasses) into plain dictionaries or tuples for JSON serialization or database insertion.
2. **`normalized_url: str = field(init=False)` (Example 02):** Declares `normalized_url` as a tracked field in `__repr__` and `__eq__` without requiring callers to pass it into `__init__`.
3. **`PriorityTask` with `field(compare=False)` (Example 03):** When pushing `(priority, task)` items into a `heapq` priority queue, standard tuples crash if two tasks tie on `priority` and `task` isn't comparable. Using `@dataclass(order=True)` with `task_id: str = field(compare=False)` compares **only** `priority`!

---

## 8. Common Mistakes

1. **Placing a Non-Default Field After a Field With a Default Value (Inheritance Trap):**
   - If `Base` has `x: int = 0` and `Sub(Base)` defines `y: int` (without a default), Python raises `TypeError: non-default argument 'y' follows default argument` unless you use `@dataclass(kw_only=True)` (Python 3.10+).
2. **Trying to Assign `self.attr = val` Inside `__post_init__` on a `frozen=True` Dataclass:**
   - Because `frozen=True` overrides `__setattr__` to raise `FrozenInstanceError`, setting a derived attribute inside `__post_init__` of a frozen dataclass requires `object.__setattr__(self, "normalized_url", value)`.
3. **Forgetting That `dataclasses.asdict()` Performs a Deep Copy:**
   - `asdict(instance)` recursively deep-copies every field. If you only need a fast shallow dictionary of top-level fields (and didn't use `slots=True`), `vars(instance)` (`instance.__dict__`) is much faster.

---

## 9. Practice Questions

1. **Easy:** Create a `@dataclass` named `Rectangle(width: float, height: float)` with a computed field `area: float = field(init=False)` populated in `__post_init__`.
2. **Medium:** Create a `@dataclass(frozen=True)` named `Money(amount_paise: int, currency: str = "INR")` that normalizes `currency` to uppercase in `__post_init__` using `object.__setattr__`.
3. **Hard:** Design a base dataclass `AuditBase` with `created_by: str = "system"` (`kw_only=True`) and subclass `Invoice(AuditBase)` with required positional fields `invoice_id: int` and `total: float`, demonstrating how `kw_only=True` solves the dataclass inheritance ordering problem.

---

## 10. Interview Questions

### Q1: How do you set a computed attribute inside `__post_init__` when `@dataclass(frozen=True)` is enabled?
**Answer:** Call `object.__setattr__(self, "field_name", computed_value)`. Direct assignment (`self.field_name = ...`) invokes the dataclass's frozen `__setattr__` guard and raises `dataclasses.FrozenInstanceError`.

### Q2: Why is `mutable: list = []` forbidden in `@dataclass`, whereas `class Regular: mutable = []` is allowed by Python syntax?
**Answer:** In a `@dataclass`, default values written on class attributes become default parameter values in the generated `__init__`. If `[]` were allowed directly, every instance initialized without passing that argument would share the **exact same list object**! `@dataclass` proactively detects unhashable/mutable defaults and raises `ValueError`, forcing you to write `field(default_factory=list)`.

### Q3: Compare `namedtuple`, `@dataclass`, `TypedDict`, and `Pydantic BaseModel`.
**Answer:**
- `namedtuple` / `typing.NamedTuple`: Immutable tuple subclass; unpackable and indexable by position; very low memory.
- `@dataclass`: Standard mutable or `frozen` class; supports methods, inheritance, `slots=True`, and `__post_init__`; **does not coerce or validate types at runtime** by default.
- `TypedDict`: Static type-checker schema for plain `dict` objects (zero runtime overhead).
- `Pydantic BaseModel`: Third-party library that performs **runtime type validation, coercion, and JSON schema generation**.
