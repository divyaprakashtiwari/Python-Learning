# Phase 5 — Topic 15: Type Hints

## 1. Introduction

**Type Hints** (introduced in PEP 484 and modernized through Python 3.10–3.13) allow you to annotate variables, function parameters, return values, and generic classes with explicit static type metadata. While the Python interpreter **does not enforce type hints at runtime** by default, static type checkers (`mypy`, `pyright`, `pyre`), IDEs (autocomplete & refactoring), and runtime validation libraries (`Pydantic`, `FastAPI`, `dataclasses`) rely heavily on them.

---

## 2. Why is it used?

1. **Catching `TypeError` and `AttributeError` Before Running Code:** Static type checkers flag `None` dereferences (`Optional` / `X | None` bugs), argument order mistakes, and missing dictionary keys in milliseconds during CI.
2. **Self-Documenting Signatures:** `def fetch_users(ids: list[int], timeout: float | None = None) -> dict[int, User]:` immediately tells callers what to pass and what is returned without reading the implementation.
3. **Structural Duck Typing (`typing.Protocol`):** Lets you type-check against an object's *capabilities* (methods/attributes) rather than forcing rigid class inheritance.
4. **Runtime Schema Generation (`get_type_hints()`):** Powers modern frameworks like FastAPI, Typer, and Pydantic.

---

## 3. Syntax

```python
from collections.abc import Callable, Iterable
from typing import Final, Literal, NotRequired, Protocol, TypedDict

# 1. Built-in Collection Generics (Python 3.9+) & Union `|` (Python 3.10+)
def summarize(items: list[int], scale: float | None = None) -> tuple[int, float]:
    ...

# 2. Python 3.12+ Generic Function & Type Alias Syntax (PEP 695)
type JSONPrimitive = str | int | float | bool | None

def first_item[T](seq: Iterable[T]) -> T | None:
    return next(iter(seq), None)

# 3. TypedDict, Literal, and Final
MAX_CONNECTIONS: Final[int] = 100
Mode = Literal["read", "write"]

class EventRecord(TypedDict):
    event_id: str
    retries: NotRequired[int]
```

---

## 4. Explanation (Step-by-Step)

1. **Modern Syntax Evolution (Python 3.9 -> 3.12+):**
   - **Python 3.9 (PEP 585):** Use built-in `list[int]`, `dict[str, int]`, `set[str]`, `tuple[int, ...]` instead of deprecated `typing.List`, `typing.Dict`, `typing.Set`, `typing.Tuple`.
   - **Python 3.10 (PEP 604):** Use `int | str` instead of `typing.Union[int, str]` and `str | None` instead of `typing.Optional[str]`.
   - **Python 3.12 (PEP 695):** Declare type parameters inline with `def func[T](x: T) -> T:` and `class Box[T]:` instead of manually importing and instantiating `T = TypeVar("T")`.
2. **Nominal vs Structural Subtyping (`ABC` vs `Protocol`):**
   - **Nominal (`abc.ABC`):** A class is only considered a subtype if it explicitly inherits `class MyWidget(RenderableABC):`.
   - **Structural (`typing.Protocol`, PEP 544):** Any class that implements the required methods (`def render(self) -> str:`) automatically satisfies `Renderable` even if it comes from a third-party library and never inherits from `Renderable`!
3. **Why Annotate Input Parameters with Abstract Interfaces (`Iterable`, `Sequence`, `Mapping`):**
   - Annotating a parameter as `items: list[int]` rejects callers who pass a `tuple[int, ...]`, `set[int]`, or generator! Prefer `collections.abc.Iterable[int]` or `Sequence[int]` for read-only function parameters, and concrete types (`list[int]`) for return values.

---

## 5. Minimum 3 Examples

### Example 01: Modern Built-in Generics (`list[int]`), Union Operator (`X | Y`), & `Callable`
File: [`example_01_modern_unions_collections_and_callable.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/15_Type_Hints/example_01_modern_unions_collections_and_callable.py)

```python
"""
Phase 5 - Topic 15: Type Hints
Example 01: Modern Built-in Generics (`list[int]`), Union Operator (`X | Y`), & `Callable`

Demonstrates:
  - Python 3.9+ built-in generic collection syntax (`list[str]`, `dict[str, int]`, `tuple[int, ...]`)
  - Python 3.10+ union operator `int | float | None` (replacing `Union` and `Optional`)
  - Annotating higher-order functions with `collections.abc.Callable[[ArgType], ReturnType]`
"""

from collections.abc import Callable


def apply_discount(
    prices: list[float],
    coupon_pct: float | None,
    rounding_fn: Callable[[float], float] = round,
) -> dict[str, float]:
    """Compute subtotal and final total with optional coupon discount."""
    subtotal = sum(prices)
    factor = 1.0 - (coupon_pct / 100.0) if coupon_pct is not None else 1.0
    final_total = rounding_fn(subtotal * factor)
    return {"subtotal": subtotal, "final_total": final_total}


def main() -> None:
    print("=== 1. Invoking Type-Annotated Function ===")
    cart = [499.0, 1200.0, 301.0]
    summary_with_coupon = apply_discount(cart, coupon_pct=15.0)
    summary_no_coupon = apply_discount(cart, coupon_pct=None)
    print(f"  With 15% coupon : {summary_with_coupon}")
    print(f"  With None coupon: {summary_no_coupon}")

    print("\n=== 2. Inspecting Function `__annotations__` Dict ===")
    for param, annotation in apply_discount.__annotations__.items():
        print(f"  {param:<13} -> {annotation}")


if __name__ == "__main__":
    main()
```

### Example 02: Generic Functions & Classes (Python 3.12+ `[T]` Syntax) and `TypedDict`
File: [`example_02_generics_typevar_and_typeddict.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/15_Type_Hints/example_02_generics_typevar_and_typeddict.py)

```python
"""
Phase 5 - Topic 15: Type Hints
Example 02: Generic Functions & Classes (Python 3.12+ `[T]` Syntax) and `TypedDict`

Demonstrates:
  - Python 3.12+ PEP 695 generic type parameter syntax `def first[T](items: list[T]) -> T:`
    and `class Box[T]:`
  - Typing structured JSON-like dictionaries with `typing.TypedDict` and `NotRequired`
"""

from typing import NotRequired, TypedDict


class UserPayload(TypedDict):
    """Typed dictionary schema for a JSON API user object."""

    id: int
    username: str
    email: NotRequired[str]


class Stack[T]:
    """Generic LIFO Stack using Python 3.12+ `class Stack[T]:` syntax."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()


def head_or_default[T](items: list[T], default: T) -> T:
    """Generic function returning the first element or `default`."""
    return items[0] if items else default


def main() -> None:
    print("=== 1. Python 3.12+ Generic Function & Class (`[T]`) ===")
    int_stack = Stack[int]()
    int_stack.push(10)
    int_stack.push(20)
    print(f"  Popped from Stack[int]: {int_stack.pop()}")
    print(f"  head_or_default([], 'fallback'): {head_or_default([], 'fallback')!r}")

    print("\n=== 2. Structured Dictionary Schema with `TypedDict` ===")
    user: UserPayload = {"id": 101, "username": "aarav"}
    print(f"  TypedDict instance (runtime dict): {user} | type={type(user).__name__}")


if __name__ == "__main__":
    main()
```

### Example 03: `Literal`, `Final`, `Protocol` (Structural Subtyping), & `typing.get_type_hints()`
File: [`example_03_literal_final_protocol_and_get_type_hints.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/15_Type_Hints/example_03_literal_final_protocol_and_get_type_hints.py)

```python
"""
Phase 5 - Topic 15: Type Hints
Example 03: `Literal`, `Final`, `Protocol` (Structural Subtyping), & `typing.get_type_hints()`

Demonstrates:
  - Restricting allowed values to specific constants with `Literal["r", "w"]`
  - Marking constants against reassignment with `Final`
  - Structural duck-typing with `typing.Protocol` (`@runtime_checkable`)
  - Resolving type annotations at runtime with `typing.get_type_hints()`
"""

from typing import Final, Literal, Protocol, get_type_hints, runtime_checkable


MAX_RETRIES: Final[int] = 3
LogLevel = Literal["DEBUG", "INFO", "ERROR"]


@runtime_checkable
class Renderable(Protocol):
    """Any object with a `.render() -> str` method satisfies `Renderable` (no inheritance needed!)."""

    def render(self) -> str: ...


class MarkdownBadge:
    """Does NOT inherit from `Renderable`, but implements `.render() -> str`."""

    def __init__(self, label: str) -> None:
        self.label = label

    def render(self) -> str:
        return f"**[{self.label}]**"


def emit_log(level: LogLevel, widget: Renderable) -> str:
    return f"[{level}] {widget.render()} (max_retries={MAX_RETRIES})"


def main() -> None:
    print("=== 1. Structural Subtyping with `Protocol` (`@runtime_checkable`) ===")
    badge = MarkdownBadge("BUILD PASSING")
    print(f"  isinstance(badge, Renderable): {isinstance(badge, Renderable)}")
    print(f"  emit_log output              : {emit_log('INFO', badge)}")

    print("\n=== 2. Runtime Introspection via `typing.get_type_hints()` ===")
    hints = get_type_hints(emit_log)
    for name, tp in hints.items():
        print(f"  {name:<8} -> {tp}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== 1. Invoking Type-Annotated Function ===
  With 15% coupon : {'subtotal': 2000.0, 'final_total': 1700}
  With None coupon: {'subtotal': 2000.0, 'final_total': 2000}

=== 2. Inspecting Function `__annotations__` Dict ===
  prices        -> list[float]
  coupon_pct    -> float | None
  rounding_fn   -> collections.abc.Callable[[float], float]
  return        -> dict[str, float]
```

### Output — Example 02
```text
=== 1. Python 3.12+ Generic Function & Class (`[T]`) ===
  Popped from Stack[int]: 20
  head_or_default([], 'fallback'): 'fallback'

=== 2. Structured Dictionary Schema with `TypedDict` ===
  TypedDict instance (runtime dict): {'id': 101, 'username': 'aarav'} | type=dict
```

### Output — Example 03
```text
=== 1. Structural Subtyping with `Protocol` (`@runtime_checkable`) ===
  isinstance(badge, Renderable): True
  emit_log output              : [INFO] **[BUILD PASSING]** (max_retries=3)

=== 2. Runtime Introspection via `typing.get_type_hints()` ===
  level    -> typing.Literal['DEBUG', 'INFO', 'ERROR']
  widget   -> <class '__main__.Renderable'>
  return   -> <class 'str'>
```

---

## 7. Code Explanation

1. **`tuple[int, str]` vs `tuple[int, ...]` (Example 01):** Unlike `list[int]`, a `tuple` annotation normally specifies fixed positional element types (`tuple[int, str]` = 2-element tuple). To annotate a homogeneous variable-length tuple, use an ellipsis: `tuple[int, ...]`.
2. **`TypedDict` (Example 02):** At runtime, a `TypedDict` instance is just a standard `dict` with zero wrapper overhead (`type(user) is dict`), while static type checkers verify exact key names and value types.
3. **`@runtime_checkable` on `Protocol` (Example 03):** By default, `Protocol` is checked only by static type checkers (`mypy`/`pyright`). Decorating a `Protocol` with `@runtime_checkable` allows `isinstance(badge, Renderable)` to check at runtime whether the required attributes/methods exist.

---

## 8. Common Mistakes

1. **Using `any` (Built-in Function) Instead of `typing.Any` or `object`:**
   - Lowercase `any` is the built-in boolean function (`any([True, False])`). For an unrestricted dynamic type, use `typing.Any` (disables type checking) or `object` (the safe top type that forces callers to narrow with `isinstance` before calling methods).
2. **Writing `tuple[int]` When You Mean Variable-Length `tuple[int, ...]`:**
   - `tuple[int]` means a **1-element tuple** `(42,)`, not a tuple of arbitrary length!
3. **Assuming Type Hints Automatically Validate Runtime Input:**
   - `def set_age(age: int):` will happily accept `set_age("not-an-int")` at runtime unless you use a runtime validator (like `isinstance` or Pydantic).

---

## 9. Practice Questions

1. **Easy:** Annotate a function `parse_pair(raw: str) -> tuple[str, int] | None` and a higher-order function `retry_task[T](task: Callable[[], T], retries: int = 3) -> T`.
2. **Medium:** Define a `Protocol` named `SupportsClose` with `def close(self) -> None: ...` and write a generic function `use_and_close[T: SupportsClose](resource: T, action: Callable[[T], None]) -> None`.
3. **Hard:** Write a runtime `@typechecked` decorator using `inspect.signature(func)` and `typing.get_type_hints(func)` that validates simple argument types (`int`, `str`, `float`) at call time.

---

## 10. Interview Questions

### Q1: What is the difference between `typing.Any` and `object` in Python type hints?
**Answer:**
- Every type is assignable to both `Any` and `object`.
- However, `object` is **type-safe**: the type checker only allows operations valid on all objects (`==`, `isinstance`, `str()`) until you narrow the type with `if isinstance(x, str):`.
- `Any` **turns off static type checking completely** for that variable, allowing arbitrary method calls (`x.non_existent_method()`) that may crash at runtime. Always prefer `object` (or generics `[T]`) over `Any`.

### Q2: Why is `list[T]` invariant while `Sequence[T]` is covariant?
**Answer:**
- Suppose `Dog` is a subclass of `Animal`. If `list` were covariant, you could pass a `list[Dog]` to a function expecting `list[Animal]`, and that function could legally execute `animals.append(Cat())`—corrupting the caller's `list[Dog]` with a `Cat`! Therefore, mutable containers like `list[T]` and `dict[K, V]` are **invariant**.
- Read-only interfaces like `collections.abc.Sequence[T]` and `Iterable[T]` have no `.append()` mutation methods, so they are safely **covariant** (`Sequence[Dog]` is a subtype of `Sequence[Animal]`).

### Q3: Why is `typing.get_type_hints(obj)` preferred over reading `obj.__annotations__` directly?
**Answer:** `get_type_hints()` automatically resolves stringified forward references (such as `"TreeNode"` or `from __future__ import annotations` strings) back into actual Python type objects and merges inherited annotations across base classes.
