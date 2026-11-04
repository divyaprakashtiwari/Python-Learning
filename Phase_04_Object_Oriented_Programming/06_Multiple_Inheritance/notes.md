# Phase 4 — Topic 06: Multiple Inheritance

## 1. Introduction

**Multiple Inheritance** occurs when a class inherits from **more than one direct parent class** (`class Child(ParentA, ParentB):`).

While some languages (like Java and C#) forbid multiple inheritance of classes due to the **Diamond Problem** (ambiguity when two parent classes inherit from a common ancestor), Python supports multiple inheritance safely and deterministically using the **C3 Superclass Linearization algorithm** and **cooperative `super()`**.

---

## 2. Why is it used?

- **The Mixin Pattern (Modular Capabilities):** In frameworks like Django, FastAPI, and Python's standard library (`socketserver.ThreadingMixIn`, `collections.abc`), small single-purpose **Mixin classes** (`JSONSerializableMixin`, `IdentifiableMixin`, `LoginRequiredMixin`) are combined with a primary base class to compose capabilities without creating bloated god-classes.
- **Layered Middleware Pipelines:** Combining orthogonal cross-cutting layers (`AuthLayer`, `RateLimitLayer`) that cooperatively process requests along the Method Resolution Order (MRO).

---

## 3. Syntax

```python
# 1. Multiple Inheritance syntax (Mixins listed LEFT-TO-RIGHT before Primary Base Class)
class CustomerInvoice(JSONSerializableMixin, IdentifiableMixin, BaseModel):
    pass

# 2. Inspecting the Method Resolution Order (MRO)
print(CustomerInvoice.mro())      # Returns `list[type]`
print(CustomerInvoice.__mro__)    # Returns `tuple[type, ...]`
```

---

## 4. Explanation (Step-by-Step)

### Step 1: The Diamond Problem
Suppose we have a diamond-shaped hierarchy:
```text
        BaseNode
        /      \
  AuthLayer   RateLimitLayer
        \      /
   APIGatewayEndpoint
```
If `APIGatewayEndpoint` calls `super().process()`, which parent runs first—`AuthLayer` or `RateLimitLayer`? And when `AuthLayer` calls `super().process()`, does it jump straight to `BaseNode` (causing `BaseNode` to run **twice**), or does it visit `RateLimitLayer` first?

### Step 2: Python's Solution — C3 Linearization (`__mro__`) & Cooperative `super()`
Python computes a flat, linear **Method Resolution Order (MRO)** list using **C3 Linearization**, which guarantees three rules:
1. **Children precede parents:** A subclass always appears before its base classes.
2. **Left-to-right declaration order is preserved:** In `class D(B, C):`, `B` always appears before `C`.
3. **Monotonicity (Shared ancestors come last):** A shared base class (`BaseNode`) is visited only **after** all subclasses that inherit from it (`AuthLayer` and `RateLimitLayer`) have been visited!

Thus the MRO of `APIGatewayEndpoint` is:
$$\text{APIGatewayEndpoint} \rightarrow \text{AuthLayer} \rightarrow \text{RateLimitLayer} \rightarrow \text{BaseNode} \rightarrow \text{object}$$

**Crucial Insight:** `super()` in Python does **NOT** mean "call my parent class"! It means **"call the next class in the active instance's MRO"**! That is why inside `AuthLayer.process()`, `super().process()` calls its sibling `RateLimitLayer.process()`, and `BaseNode.process()` runs **exactly once**.

### Step 3: Cooperative `__init__` with `**kwargs`
When multiple parent classes in a diamond define `__init__` with different parameters (`latitude`, `battery_pct`), positional arguments don't know which class needs which argument. By using keyword-only parameters and forwarding `**kwargs` via `super().__init__(**kwargs)`, each class peels off its own keyword arguments and passes the rest along the MRO until `object.__init__()` receives empty `{}`.

---

## 5. Minimum 3 Examples

### Example 1: The Diamond Problem and C3 Linearization (`__mro__` & `mro()`)
File: `example_01_diamond_problem_and_mro.py`

```python
class BaseNode:
    """Top of the diamond (Class A)."""

    def process(self) -> list[str]:
        return ["BaseNode.process"]


class AuthLayer(BaseNode):
    """Left branch of the diamond (Class B)."""

    def process(self) -> list[str]:
        return ["AuthLayer.process"] + super().process()


class RateLimitLayer(BaseNode):
    """Right branch of the diamond (Class C)."""

    def process(self) -> list[str]:
        return ["RateLimitLayer.process"] + super().process()


class APIGatewayEndpoint(AuthLayer, RateLimitLayer):
    """Bottom of the diamond (Class D inheriting from B and C)."""

    def process(self) -> list[str]:
        return ["APIGatewayEndpoint.process"] + super().process()


def main() -> None:
    print("=== 1. Inspecting C3 Linearization MRO (`APIGatewayEndpoint.mro()`) ===")
    mro_names = [cls.__name__ for cls in APIGatewayEndpoint.mro()]
    print(f"  MRO : {' -> '.join(mro_names)}")

    print("\n=== 2. Cooperative `super()` Traversal Across the Diamond ===")
    endpoint = APIGatewayEndpoint()
    execution_chain = endpoint.process()
    for step_idx, step_name in enumerate(execution_chain, start=1):
        print(f"  Step {step_idx}: {step_name}")
    print(f"  Notice `BaseNode.process` ran exactly ONCE (not twice)!")


if __name__ == "__main__":
    main()
```

---

### Example 2: The Mixin Pattern (`JSONSerializableMixin`, `IdentifiableMixin`)
File: `example_02_mixin_pattern_architecture.py`

```python
import json


class JSONSerializableMixin:
    """Mixin providing `.to_json()` serialization for any object with `__dict__`."""

    def to_json(self) -> str:
        public_data = {
            k: v for k, v in self.__dict__.items() if not k.startswith("_")
        }
        return json.dumps(public_data, sort_keys=True)


class IdentifiableMixin:
    """Mixin providing a canonical `<ClassName#id>` display tag."""

    id: str | int

    def identity_tag(self) -> str:
        return f"<{self.__class__.__name__}#{self.id}>"


class BaseModel:
    """Core domain base class."""

    def __init__(self, record_id: str) -> None:
        self.id = record_id


class CustomerInvoice(JSONSerializableMixin, IdentifiableMixin, BaseModel):
    """Combines Mixins (left) with the primary `BaseModel` (right)."""

    def __init__(self, record_id: str, customer: str, total_inr: float) -> None:
        super().__init__(record_id)
        self.customer = customer
        self.total_inr = total_inr
        self._internal_secret = "do-not-serialize"


def main() -> None:
    print("=== Combining Orthogonal Mixin Classes with a Domain Model ===")
    inv = CustomerInvoice("INV-2026-09", "Aarav Tech", 59000.0)
    print(f"  Identity Tag (`IdentifiableMixin`)     : {inv.identity_tag()}")
    print(f"  JSON Payload (`JSONSerializableMixin`) : {inv.to_json()}")
    print(f"  MRO : {[c.__name__ for c in CustomerInvoice.mro()]}")


if __name__ == "__main__":
    main()
```

---

### Example 3: Cooperative `__init__` with `**kwargs` & Catching Invalid MRO Hierarchies
File: `example_03_cooperative_super_and_mro_conflict.py`

```python
from typing import Any


class RootEntity:
    """Root class that strips no kwargs and calls `super().__init__()` (`object`)."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class GPSLocatable(RootEntity):
    """Initializes `latitude` and `longitude` and forwards remaining `**kwargs`."""

    def __init__(self, *, latitude: float, longitude: float, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.latitude = latitude
        self.longitude = longitude


class BatteryPowered(RootEntity):
    """Initializes `battery_pct` and forwards remaining `**kwargs`."""

    def __init__(self, *, battery_pct: int, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.battery_pct = battery_pct


class DeliveryDrone(GPSLocatable, BatteryPowered):
    """Cooperatively initializes `drone_id`, `GPSLocatable`, and `BatteryPowered`."""

    def __init__(self, drone_id: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.drone_id = drone_id


def main() -> None:
    print("=== 1. Cooperative Multiple Inheritance `__init__` Using `**kwargs` ===")
    drone = DeliveryDrone(
        "DRN-404",
        latitude=12.9716,
        longitude=77.5946,
        battery_pct=88,
    )
    print(
        f"  Drone {drone.drone_id}: coords=({drone.latitude}, {drone.longitude}), "
        f"battery={drone.battery_pct}%"
    )

    print("\n=== 2. Catching an Inconsistent MRO Graph (`TypeError`) ===")

    class X:
        pass

    class Y(X):
        pass

    try:
        # `X` precedes `Y` in `class Bad(X, Y)`, which contradicts `Y(X)` where `Y` precedes `X`!
        class BadHierarchy(X, Y):
            pass
    except TypeError as err:
        print(f"  Caught expected MRO TypeError: {err}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_diamond_problem_and_mro.py`)
```text
=== 1. Inspecting C3 Linearization MRO (`APIGatewayEndpoint.mro()`) ===
  MRO : APIGatewayEndpoint -> AuthLayer -> RateLimitLayer -> BaseNode -> object

=== 2. Cooperative `super()` Traversal Across the Diamond ===
  Step 1: APIGatewayEndpoint.process
  Step 2: AuthLayer.process
  Step 3: RateLimitLayer.process
  Step 4: BaseNode.process
  Notice `BaseNode.process` ran exactly ONCE (not twice)!
```

### Output — Example 2 (`example_02_mixin_pattern_architecture.py`)
```text
=== Combining Orthogonal Mixin Classes with a Domain Model ===
  Identity Tag (`IdentifiableMixin`)     : <CustomerInvoice#INV-2026-09>
  JSON Payload (`JSONSerializableMixin`) : {"customer": "Aarav Tech", "id": "INV-2026-09", "total_inr": 59000.0}
  MRO : ['CustomerInvoice', 'JSONSerializableMixin', 'IdentifiableMixin', 'BaseModel', 'object']
```

### Output — Example 3 (`example_03_cooperative_super_and_mro_conflict.py`)
```text
=== 1. Cooperative Multiple Inheritance `__init__` Using `**kwargs` ===
  Drone DRN-404: coords=(12.9716, 77.5946), battery=88%

=== 2. Catching an Inconsistent MRO Graph (`TypeError`) ===
  Caught expected MRO TypeError: Cannot create a consistent method resolution order (MRO) for bases X, Y
```

---

## 7. Code Explanation

1. **Sibling Call via `super()` (`example_01`):** Look closely at `AuthLayer(BaseNode)`: `AuthLayer` does **not** inherit from `RateLimitLayer`, yet when `endpoint.process()` runs, `super().process()` inside `AuthLayer` calls `RateLimitLayer.process()`! That is because `super()` follows `type(self).__mro__` (`APIGatewayEndpoint.mro()`).
2. **Mixin Ordering Convention (`example_02`):** Mixins (`JSONSerializableMixin`, `IdentifiableMixin`) are placed **to the left** of the primary base class (`BaseModel`) so that if a Mixin overrides a method, the Mixin's version is found first in the MRO.
3. **Inconsistent MRO Rejection (`example_03`):** In `class BadHierarchy(X, Y):` where `class Y(X):`, the base list `(X, Y)` demands that `X` come before `Y`, while `Y(X)` demands that subclass `Y` come before parent `X`. C3 Linearization detects this cycle/contradiction immediately when the `class` statement executes and raises `TypeError`.

---

## 8. Common Mistakes

1. **Calling `ParentA.__init__(self)` and `ParentB.__init__(self)` explicitly in a diamond hierarchy:**
   - If both `ParentA` and `ParentB` inherit from `Root` and call `Root.__init__(self)`, `Root.__init__` will execute **twice**! Always use `super().__init__(...)` across all classes in the hierarchy.
2. **Putting the base class before Mixin classes (`class MyView(BaseView, AuthMixin):`):**
   - If `BaseView` defines a terminal method (that doesn't call `super()`), listing `BaseView` first means `AuthMixin`'s overridden method will be shadowed and never reached! List Mixins first (`class MyView(AuthMixin, BaseView):`).
3. **Giving a Mixin its own stateful `__init__` when it doesn't need one:**
   - Pure Mixins should ideally provide methods that operate on existing attributes or properties rather than requiring complex `__init__` arguments.

---

## 9. Practice Questions

1. **Easy — Trace MRO by Hand and Verify:**
   Given `class A: pass`, `class B(A): pass`, `class C(A): pass`, `class D(B, C): pass`, `class E(C, A): pass`, and `class F(D, E): pass`, predict `F.mro()` by hand and verify it in Python.

2. **Medium — `ComparableMixin`:**
   Write a `ComparableMixin` that requires a single `.sort_key()` method on `self` and automatically implements `__lt__`, `__le__`, `__gt__`, and `__ge__` using `self.sort_key()`. Mix it into a `JobTask(priority: int, name: str)` class and sort a list of tasks.

3. **Hard — Cooperative Request Pipeline:**
   Build a diamond hierarchy `BaseHandler` $\leftarrow$ (`LoggingHandler`, `CompressionHandler`) $\leftarrow$ `ProductionHandler` where each `.handle(payload: str) -> str` wraps or transforms `super().handle(payload)`.

---

## 10. Interview Questions

### Q1: What does `super()` actually return in Python, and why doesn't it just mean "parent class"?
**Answer:**
`super()` returns a **proxy object** that delegates method lookups to the **next class after the current class in `type(self).__mro__`**. In single inheritance, the next class in the MRO happens to be the direct parent class. In multiple inheritance (`class D(B, C):`), the next class after `B` in `D.__mro__` is `B`'s sibling `C`, not `B`'s parent!

### Q2: What algorithm does Python use to compute the Method Resolution Order (MRO), and what are its guarantees?
**Answer:**
Python uses the **C3 Superclass Linearization** algorithm (introduced in Python 2.3). It guarantees:
1. **Subclass before superclass:** A derived class is always searched before its base classes.
2. **Local precedence order:** If `class D(B, C):` is declared, `B` is searched before `C`.
3. **Monotonicity:** Extending a hierarchy never reverses the relative lookup order of existing base classes. If no linear ordering satisfies all three constraints, Python raises `TypeError: Cannot create a consistent method resolution order (MRO)`.

### Q3: What is a Mixin class in Python?
**Answer:**
A **Mixin** is a small class designed to be inherited alongside a primary base class via multiple inheritance to "mix in" a focused, orthogonal set of methods (such as `JSONSerializableMixin` or `ThreadingMixIn`). A Mixin is not meant to be instantiated on its own (`IS-A` does not apply in isolation; rather, it provides a capability).
