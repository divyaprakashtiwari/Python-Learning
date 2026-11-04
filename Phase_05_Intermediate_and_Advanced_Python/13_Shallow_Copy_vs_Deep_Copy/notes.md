# Phase 5 — Topic 13: Shallow Copy vs Deep Copy

## 1. Introduction

In Python, assignment (`b = a`) **never copies an object**—it merely binds a second variable name (`b`) to the exact same object in memory (`a is b`). When you actually need a separate mutable copy, Python's `copy` module offers two distinct levels of duplication:
- **Shallow Copy (`copy.copy(x)`):** Allocates a new top-level container, but populates it with **references to the same inner child objects**.
- **Deep Copy (`copy.deepcopy(x)`):** Recursively allocates new containers **and** new copies of all nested child objects at every depth.

---

## 2. Why is it used?

1. **Preventing Accidental Shared-State Bugs:** Mutating a nested list inside a shallow-copied configuration dictionary silently mutates the original template dictionary too; `copy.deepcopy()` isolates nested state completely.
2. **Performance Optimization When Inner Elements Are Immutable:** If a list contains only immutable objects (`int`, `str`, `tuple`), a shallow copy (`list.copy()` or `[:]`) is $10\times$ faster than `deepcopy` and 100% safe because immutable elements cannot be mutated in place.
3. **Customizing Object Cloning (`__copy__` and `__deepcopy__`):** Allows classes holding non-copyable OS handles (sockets, locks) to clone data attributes while resetting or sharing system handles appropriately.

---

## 3. Syntax

```python
import copy

# 1. Assignment Aliasing (NO copy at all)
alias = original                 # alias is original -> True

# 2. Shallow Copy (New outer container; shared inner objects)
s1 = copy.copy(original)
s2 = original.copy()             # Built-in on list, dict, set
s3 = original[:]                 # Slice copy on sequences (list, tuple, str)

# 3. Deep Copy (New outer container AND recursive copies of all nested objects)
d1 = copy.deepcopy(original)
```

---

## 4. Explanation (Step-by-Step)

1. **Three Levels of Reference Sharing:**
   - **Aliasing (`b = a`):** `a is b` is `True`. Appending to `b` or mutating `b[0]` affects `a`.
   - **Shallow Copy (`b = copy.copy(a)`):** `a is b` is `False`, **but** `a[0] is b[0]` is `True`! Appending a new top-level item to `b` does **not** affect `a`, but mutating a mutable child (`b[0].append(x)`) **does** affect `a[0]`.
   - **Deep Copy (`b = copy.deepcopy(a)`):** `a is b` is `False` **and** `a[0] is b[0]` is `False` (for mutable children).
2. **How `copy.deepcopy` Avoids Infinite Loops on Cyclic Graphs (`memo` dict):**
   - Suppose list `a` contains a reference to itself (`a.append(a)`). A naive recursive copy would crash with `RecursionError`.
   - `copy.deepcopy(x, memo)` maintains a dictionary `memo` mapping `id(original_obj) -> new_clone`. Before copying any object, it checks if `id(obj)` is already in `memo`, returning the existing clone if found.
3. **Behavior on Immutable Types (`int`, `str`, `tuple` of immutables):**
   - Calling `copy.copy()` or `copy.deepcopy()` on an `int`, `str`, or a `tuple` containing only atomic immutables returns the **exact same object (`x is copy.deepcopy(x)`)** as an optimization—unless a `tuple` contains a mutable inner item like `([1, 2], "a")`, in which case `deepcopy` creates a new tuple with a cloned inner list!

---

## 5. Minimum 3 Examples

### Example 01: Assignment Aliasing (`=`) vs Shallow Copy (`copy.copy()`, `.copy()`, `[:]`)
File: [`example_01_assignment_aliasing_vs_shallow_copy.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/13_Shallow_Copy_vs_Deep_Copy/example_01_assignment_aliasing_vs_shallow_copy.py)

```python
"""
Phase 5 - Topic 13: Shallow Copy vs Deep Copy
Example 01: Assignment Aliasing (`=`) vs Shallow Copy (`copy.copy()`, `.copy()`, `[:]`)

Demonstrates:
  - Why `b = a` does NOT copy a list (both names point to the exact same object in memory)
  - How a shallow copy creates a new outer container (`a is not b`) whose top-level
    elements are independent when rebound
"""

import copy


def main() -> None:
    print("=== 1. Assignment Aliasing (`alias = original`) ===")
    original = [10, 20, 30]
    alias = original
    alias.append(40)
    print(f"  original is alias : {original is alias}")
    print(f"  original after alias.append(40): {original}")

    print("\n=== 2. Shallow Copy (`copy.copy`, `.copy()`, `[:]`) on Flat List ===")
    shallow_1 = copy.copy(original)
    shallow_2 = original.copy()
    shallow_3 = original[:]
    shallow_1.append(999)
    print(f"  original is shallow_1 : {original is shallow_1}")
    print(f"  original              : {original} (unaffected by shallow_1.append)")
    print(f"  shallow_1             : {shallow_1}")
    print(f"  All 3 shallow copy techniques equal? {shallow_1[:-1] == shallow_2 == shallow_3}")


if __name__ == "__main__":
    main()
```

### Example 02: The Nested Mutable Trap in Shallow Copies (`copy.copy` vs `copy.deepcopy`)
File: [`example_02_nested_mutation_bug_in_shallow_copy.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/13_Shallow_Copy_vs_Deep_Copy/example_02_nested_mutation_bug_in_shallow_copy.py)

```python
"""
Phase 5 - Topic 13: Shallow Copy vs Deep Copy
Example 02: The Nested Mutable Trap in Shallow Copies (`copy.copy` vs `copy.deepcopy`)

Demonstrates:
  - How a shallow copy of a nested dictionary/list shares references to inner mutable objects
  - How mutating an inner list in a shallow copy corrupts the original structure
  - How `copy.deepcopy()` recursively clones all nested mutable objects
"""

import copy


def main() -> None:
    base_template = {
        "env": "production",
        "Ports": [80, 443],
    }

    print("=== 1. Shallow Copy Shares Inner Mutable References ===")
    shallow_cfg = copy.copy(base_template)
    print(f"  Outer dicts distinct (`is`)? : {base_template is not shallow_cfg}")
    print(f"  Inner lists SHARED (`is`)?   : {base_template['Ports'] is shallow_cfg['Ports']}")

    shallow_cfg["Ports"].append(8080)  # Mutates the shared inner list!
    print(f"  base_template after shallow inner mutation: {base_template} (CORRUPTED!)")

    print("\n=== 2. Deep Copy (`copy.deepcopy`) Isolates All Nested Levels ===")
    clean_template = {"env": "production", "Ports": [80, 443]}
    deep_cfg = copy.deepcopy(clean_template)
    print(f"  Inner lists SHARED (`is`)?   : {clean_template['Ports'] is deep_cfg['Ports']}")

    deep_cfg["Ports"].append(9090)
    print(f"  clean_template : {clean_template} (completely untouched!)")
    print(f"  deep_cfg       : {deep_cfg}")


if __name__ == "__main__":
    main()
```

### Example 03: Circular References in `deepcopy` (`memo` dict) & Custom `__copy__` / `__deepcopy__`
File: [`example_03_deepcopy_memo_and_custom_copy_hooks.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/13_Shallow_Copy_vs_Deep_Copy/example_03_deepcopy_memo_and_custom_copy_hooks.py)

```python
"""
Phase 5 - Topic 13: Shallow Copy vs Deep Copy
Example 03: Circular References in `deepcopy` (`memo` dict) & Custom `__copy__` / `__deepcopy__`

Demonstrates:
  - How `copy.deepcopy()` handles cyclic/self-referential graphs without infinite recursion
    using its internal `memo` dictionary
  - Implementing custom `__copy__` and `__deepcopy__` hooks on a class
"""

import copy


class CacheNode:
    """Custom class controlling how shallow and deep copies behave."""

    def __init__(self, name: str, tags: list[str], connection_id: int) -> None:
        self.name = name
        self.tags = tags
        self.connection_id = connection_id

    def __copy__(self) -> "CacheNode":
        # Shallow copy: keep same `tags` list reference, preserve `connection_id`
        return CacheNode(self.name, self.tags, self.connection_id)

    def __deepcopy__(self, memo: dict[int, object]) -> "CacheNode":
        # Deep copy: clone `tags`, but reset `connection_id` to 0 for the new clone
        cloned_tags = copy.deepcopy(self.tags, memo)
        new_node = CacheNode(self.name, cloned_tags, connection_id=0)
        memo[id(self)] = new_node
        return new_node


def main() -> None:
    print("=== 1. Cyclic Graph Handling in `copy.deepcopy()` ===")
    cyclic: list[object] = ["root"]
    cyclic.append(cyclic)  # Self-reference!
    cloned_cyclic = copy.deepcopy(cyclic)
    print(f"  Cloned cyclic structure valid? {cloned_cyclic[1] is cloned_cyclic} (no RecursionError!)")

    print("\n=== 2. Custom `__copy__` vs `__deepcopy__` Hooks ===")
    node = CacheNode("redis-primary", ["fast", "lru"], connection_id=42)
    s_node = copy.copy(node)
    d_node = copy.deepcopy(node)
    print(f"  Shallow copy : tags shared={node.tags is s_node.tags} | connection_id={s_node.connection_id}")
    print(f"  Deep copy    : tags shared={node.tags is d_node.tags} | connection_id={d_node.connection_id}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== 1. Assignment Aliasing (`alias = original`) ===
  original is alias : True
  original after alias.append(40): [10, 20, 30, 40]

=== 2. Shallow Copy (`copy.copy`, `.copy()`, `[:]`) on Flat List ===
  original is shallow_1 : False
  original              : [10, 20, 30, 40] (unaffected by shallow_1.append)
  shallow_1             : [10, 20, 30, 40, 999]
  All 3 shallow copy techniques equal? True
```

### Output — Example 02
```text
=== 1. Shallow Copy Shares Inner Mutable References ===
  Outer dicts distinct (`is`)? : True
  Inner lists SHARED (`is`)?   : True
  base_template after shallow inner mutation: {'env': 'production', 'Ports': [80, 443, 8080]} (CORRUPTED!)

=== 2. Deep Copy (`copy.deepcopy`) Isolates All Nested Levels ===
  Inner lists SHARED (`is`)?   : False
  clean_template : {'env': 'production', 'Ports': [80, 443]} (completely untouched!)
  deep_cfg       : {'env': 'production', 'Ports': [80, 443, 9090]}
```

### Output — Example 03
```text
=== 1. Cyclic Graph Handling in `copy.deepcopy()` ===
  Cloned cyclic structure valid? True (no RecursionError!)

=== 2. Custom `__copy__` vs `__deepcopy__` Hooks ===
  Shallow copy : tags shared=True | connection_id=42
  Deep copy    : tags shared=False | connection_id=0
```

---

## 7. Code Explanation

1. **`shallow_1 = copy.copy(original)` (Example 01):** For a 1D list of immutable integers, a shallow copy is completely independent because integers cannot be mutated in place; appending to `shallow_1` resizes only `shallow_1`'s pointer array.
2. **`shallow_cfg["Ports"].append(8080)` (Example 02):** Because `shallow_cfg["Ports"]` points to the exact same `list` object as `base_template["Ports"]`, mutating it in place corrupts `base_template`.
3. **`__deepcopy__(self, memo)` (Example 03):** Custom `__deepcopy__` methods accept the `memo` dictionary and forward it to recursive `copy.deepcopy(attr, memo)` calls while registering `memo[id(self)] = new_node`.

---

## 8. Common Mistakes

1. **Initializing a 2D Grid With `grid = [[0] * cols] * rows`:**
   - The outer `* rows` performs a **shallow repetition of the exact same inner row reference**! Setting `grid[0][0] = 9` changes column 0 in **every row**. Always use `[[0] * cols for _ in range(rows)]`.
2. **Assuming `{**d}` or `dict(d)` Creates a Deep Copy:**
   - Dictionary unpacking `{**d}`, `d.copy()`, `dict(d)`, and `d | {}` all create **shallow copies**.
3. **Calling `copy.deepcopy()` on Objects Holding OS Resources (`threading.Lock`, Open Files, Sockets):**
   - OS handles and thread locks cannot be deep-copied and raise `TypeError: cannot pickle '_thread.lock' object` unless excluded via a custom `__deepcopy__`.

---

## 9. Practice Questions

1. **Easy:** Demonstrate why `board = [[0] * 3] * 3` is broken when assigning `board[0][1] = 5`, and write a function `make_grid(rows: int, cols: int, fill: int = 0) -> list[list[int]]` where every row is an independent list.
2. **Medium:** Write a function `clone_without_secrets(config: dict) -> dict` that deep-copies a nested dictionary while replacing the value of any key named `"password"` or `"api_key"` at any nesting depth with `"***"`.
3. **Hard:** Implement a doubly-linked list `Node(val, prev, next)` and verify that `copy.deepcopy(head)` clones the entire cyclic prev/next chain without raising `RecursionError`.

---

## 10. Interview Questions

### Q1: What does `t2 = copy.copy(t1)` vs `t3 = copy.deepcopy(t1)` do when `t1 = (1, [2, 3])`?
**Answer:**
- `copy.copy(t1)` returns the **exact same tuple** (`t2 is t1` is `True`) because `tuple` is immutable at the top level.
- `copy.deepcopy(t1)` inspects the tuple's elements, detects the mutable inner list `[2, 3]`, and constructs a **new tuple** `(1, [2, 3])` containing a newly cloned inner list (`t3 is t1` is `False`, and `t3[1] is t1[1]` is `False`).

### Q2: How does `copy.deepcopy()` prevent `RecursionError` on circular references?
**Answer:** It passes a `memo: dict[int, Any]` dictionary down every recursive call mapping `id(source_obj) -> cloned_obj` (and keeps a reference to `source_obj` alive so its memory address cannot be reused during the copy). When an already-visited `id(obj)` is encountered, `deepcopy` immediately returns `memo[id(obj)]`.

### Q3: Since Python 3.13, what is `copy.replace(obj, **changes)`?
**Answer:** Added in Python 3.13, `copy.replace(obj, **changes)` (which invokes `__replace__`) creates a shallow copy of immutable or data-style objects (`namedtuple`, `dataclass`, `datetime`, `Path`, etc.) with specified attributes replaced—standardizing `namedtuple._replace()` and `dataclasses.replace()` under one universal function.
