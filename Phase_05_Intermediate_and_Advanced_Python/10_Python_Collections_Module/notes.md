# Phase 5 — Topic 10: Python Collections Module

## 1. Introduction

Python's built-in `collections` module provides high-performance, specialized container datatypes that extend `dict`, `list`, `set`, and `tuple`. Mastering `Counter`, `defaultdict`, `deque`, `namedtuple`, and `ChainMap` is one of the highest-leverage skills for writing clean, optimal Python code in both production engineering and coding interviews.

---

## 2. Why is it used?

1. **Zero Boilerplate Frequency & Grouping (`Counter`, `defaultdict`):** Replaces 6-line `if key not in d:` loops with single-line C-accelerated structures.
2. **True $O(1)$ Queue Operations (`deque`):** Standard Python `list.pop(0)` and `list.insert(0, x)` shift all $N$ elements in $O(n)$ time. `collections.deque` (a doubly-linked list of fixed-size C blocks) executes `.appendleft()` and `.popleft()` in guaranteed $O(1)$ time.
3. **Self-Documenting Tuples (`namedtuple`):** Gives tuple elements readable attribute names (`point.x`, `point.y`) with zero per-instance `__dict__` memory overhead.
4. **Zero-Copy Dictionary Layering (`ChainMap`):** Views multiple dictionaries (`CLI flags -> Env vars -> Defaults`) as a single mapping without merging or copying them.

---

## 3. Syntax

```python
from collections import Counter, defaultdict, deque, namedtuple, ChainMap

# 1. Counter (Multiset)
freq = Counter("abracadabra")
top_two = freq.most_common(2)           # [('a', 5), ('b', 2)]

# 2. defaultdict (Auto-initializing dict)
graph: defaultdict[int, list[int]] = defaultdict(list)
graph[1].append(2)                      # Automatically calls `list()` for missing key `1`

# 3. deque (Double-Ended Queue)
dq = deque([1, 2, 3], maxlen=5)
dq.appendleft(0)
leftmost = dq.popleft()

# 4. namedtuple & ChainMap
 Edge = namedtuple("Edge", ["u", "v", "weight"])
layered = ChainMap(override_dict, default_dict)
```

---

## 4. Explanation (Step-by-Step)

1. **`Counter`:**
   - A `dict` subclass mapping hashable elements to integer counts.
   - Accessing a missing key `c[missing]` returns `0` instead of raising `KeyError` (and does **not** insert `missing` into the counter).
   - Supports multiset operators: `c1 + c2` (add counts), `c1 - c2` (subtract, keeping only positive counts), `c1 & c2` ($\min$ intersection), and `c1 | c2` ($\max$ union).
2. **`defaultdict(default_factory)`:**
   - Overrides `__missing__(key)` to call `default_factory()` (such as `list`, `int`, `set`, or `lambda: ...`), insert the result under `key`, and return it.
   - Note: `d[missing_key]` triggers `__missing__` and inserts the key, whereas `d.get(missing_key)` returns `None` **without** modifying the dictionary.
3. **`deque(iterable, maxlen=None)`:**
   - Ideal for BFS graph/tree traversals, sliding window algorithms, and bounded ring buffers.
   - When `maxlen` is set and the deque is full, appending to one end automatically discards the oldest element from the opposite end in $O(1)$ time.
4. **`ChainMap(*maps)`:**
   - Lookups search the underlying mappings from left to right until the key is found. Mutations (`cm[k] = v`) always write to the **first** mapping (`cm.maps[0]`).

---

## 5. Minimum 3 Examples

### Example 01: `Counter` (Multiset Frequency Analysis) & `defaultdict` (Automatic Grouping)
File: [`example_01_counter_and_defaultdict.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/10_Python_Collections_Module/example_01_counter_and_defaultdict.py)

```python
"""
Phase 5 - Topic 10: Python Collections Module
Example 01: `Counter` (Multiset Frequency Analysis) & `defaultdict` (Automatic Grouping)

Demonstrates:
  - Counting frequencies, finding `.most_common(k)`, and multiset arithmetic (`+`, `-`, `&`) with `Counter`
  - Grouping items without `KeyError` boilerplate using `defaultdict(list)` and `defaultdict(int)`
"""

from collections import Counter, defaultdict


def main() -> None:
    print("=== 1. `Counter` Frequency Counting & `.most_common()` ===")
    words = ["python", "rust", "python", "go", "python", "rust", "c++"]
    counts = Counter(words)
    print(f"  Counter        : {counts}")
    print(f"  Top 2 languages: {counts.most_common(2)}")
    print(f"  Missing key lookup (`counts['java']`): {counts['java']} (returns 0, never KeyError!)")

    print("\n=== 2. `Counter` Multiset Arithmetic (`+` and `-`) ===")
    warehouse_a = Counter(keyboard=5, mouse=10)
    warehouse_b = Counter(keyboard=3, monitor=4)
    combined = warehouse_a + warehouse_b
    print(f"  Combined inventory : {dict(combined)}")

    print("\n=== 3. Grouping Records with `defaultdict(list)` ===")
    employees = [
        ("Engineering", "Aarav"),
        ("Design", "Diya"),
        ("Engineering", "Rohan"),
        ("Design", "Meera"),
    ]
    by_dept: defaultdict[str, list[str]] = defaultdict(list)
    for dept, name in employees:
        by_dept[dept].append(name)
    print(f"  Grouped by department: {dict(by_dept)}")


if __name__ == "__main__":
    main()
```

### Example 02: `deque` — O(1) Double-Ended Queue, Ring Buffer (`maxlen`), & `.rotate()`
File: [`example_02_deque_o1_ends_and_bounded_window.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/10_Python_Collections_Module/example_02_deque_o1_ends_and_bounded_window.py)

```python
"""
Phase 5 - Topic 10: Python Collections Module
Example 02: `deque` — O(1) Double-Ended Queue, Ring Buffer (`maxlen`), & `.rotate()`

Demonstrates:
  - O(1) `.appendleft()` and `.popleft()` on `collections.deque` (vs O(n) `list.pop(0)`)
  - Bounded ring buffer using `deque(maxlen=3)` to retain only the N most recent events
  - Circular rotation with `dq.rotate(k)`
"""

from collections import deque


def main() -> None:
    print("=== 1. O(1) Double-Ended Queue Operations (`appendleft` / `popleft`) ===")
    task_queue: deque[str] = deque(["normal-1", "normal-2"])
    task_queue.append("normal-3")
    task_queue.appendleft("URGENT-0")  # O(1) front insertion
    print(f"  Queue after urgent arrival: {list(task_queue)}")
    print(f"  Dispatched first (`popleft`): {task_queue.popleft()!r} -> remaining: {list(task_queue)}")

    print("\n=== 2. Bounded Sliding Ring Buffer (`deque(maxlen=3)`) ===")
    recent_errors: deque[str] = deque(maxlen=3)
    for idx in range(1, 6):
        recent_errors.append(f"ERR-10{idx}")
        print(f"  After ERR-10{idx}: {list(recent_errors)}")

    print("\n=== 3. Round-Robin Schedule via `deque.rotate(-1)` ===")
    on_call = deque(["Alice", "Bob", "Charlie"])
    for week in range(1, 4):
        print(f"  Week {week} primary on-call: {on_call[0]} (rotation={list(on_call)})")
        on_call.rotate(-1)


if __name__ == "__main__":
    main()
```

### Example 03: `collections.namedtuple` & `ChainMap` Layered Configs
File: [`example_03_namedtuple_and_chainmap.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/10_Python_Collections_Module/example_03_namedtuple_and_chainmap.py)

```python
"""
Phase 5 - Topic 10: Python Collections Module
Example 03: `collections.namedtuple` & `ChainMap` Layered Configs

Demonstrates:
  - Lightweight immutable tuple subclasses with named fields (`_replace`, `_asdict`)
  - Layered configuration lookup (`CLI args -> Env Vars -> Defaults`) without copying dicts using `ChainMap`
"""

from collections import ChainMap, namedtuple


Point2D = namedtuple("Point2D", ["x", "y"], defaults=[0, 0])


def main() -> None:
    print("=== 1. `namedtuple` -- Memory-Efficient Tuple with Named Attributes ===")
    p1 = Point2D(10, 25)
    p2 = p1._replace(x=50)
    print(f"  p1: {p1} | p1.x={p1.x}, p1[1]={p1[1]}")
    print(f"  p2 (`p1._replace(x=50)`): {p2} | _asdict()={p2._asdict()}")

    print("\n=== 2. `ChainMap` -- Layered Config Hierarchy (CLI -> Env -> Defaults) ===")
    defaults = {"host": "localhost", "port": 8080, "timeout": 30}
    env_vars = {"port": 9000}
    cli_args = {"timeout": 5}

    # Searches `cli_args` first, then `env_vars`, then `defaults`
    config = ChainMap(cli_args, env_vars, defaults)
    print(f"  Effective host    : {config['host']} (from defaults)")
    print(f"  Effective port    : {config['port']} (overridden by env_vars)")
    print(f"  Effective timeout : {config['timeout']} (overridden by cli_args)")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== 1. `Counter` Frequency Counting & `.most_common()` ===
  Counter        : Counter({'python': 3, 'rust': 2, 'go': 1, 'c++': 1})
  Top 2 languages: [('python', 3), ('rust', 2)]
  Missing key lookup (`counts['java']`): 0 (returns 0, never KeyError!)

=== 2. `Counter` Multiset Arithmetic (`+` and `-`) ===
  Combined inventory : {'keyboard': 8, 'mouse': 10, 'monitor': 4}

=== 3. Grouping Records with `defaultdict(list)` ===
  Grouped by department: {'Engineering': ['Aarav', 'Rohan'], 'Design': ['Diya', 'Meera']}
```

### Output — Example 02
```text
=== 1. O(1) Double-Ended Queue Operations (`appendleft` / `popleft`) ===
  Queue after urgent arrival: ['URGENT-0', 'normal-1', 'normal-2', 'normal-3']
  Dispatched first (`popleft`): 'URGENT-0' -> remaining: ['normal-1', 'normal-2', 'normal-3']

=== 2. Bounded Sliding Ring Buffer (`deque(maxlen=3)`) ===
  After ERR-101: ['ERR-101']
  After ERR-102: ['ERR-101', 'ERR-102']
  After ERR-103: ['ERR-101', 'ERR-102', 'ERR-103']
  After ERR-104: ['ERR-102', 'ERR-103', 'ERR-104']
  After ERR-105: ['ERR-103', 'ERR-104', 'ERR-105']

=== 3. Round-Robin Schedule via `deque.rotate(-1)` ===
  Week 1 primary on-call: Alice (rotation=['Alice', 'Bob', 'Charlie'])
  Week 2 primary on-call: Bob (rotation=['Bob', 'Charlie', 'Alice'])
  Week 3 primary on-call: Charlie (rotation=['Charlie', 'Alice', 'Bob'])
```

### Output — Example 03
```text
=== 1. `namedtuple` -- Memory-Efficient Tuple with Named Attributes ===
  p1: Point2D(x=10, y=25) | p1.x=10, p1[1]=25
  p2 (`p1._replace(x=50)`): Point2D(x=50, y=25) | _asdict()={'x': 50, 'y': 25}

=== 2. `ChainMap` -- Layered Config Hierarchy (CLI -> Env -> Defaults) ===
  Effective host    : localhost (from defaults)
  Effective port    : 9000 (overridden by env_vars)
  Effective timeout : 5 (overridden by cli_args)
```

---

## 7. Code Explanation

1. **`Counter.most_common(k)` (Example 01):** Uses `heapq.nlargest` internally when $k$ is small relative to the number of unique elements, running in $O(U \log k)$ time instead of sorting all $U$ unique keys.
2. **`deque(maxlen=3)` (Example 02):** Creates a fixed-capacity sliding window. When `"ERR-104"` is appended, `"ERR-101"` is automatically evicted from the left in $O(1)$ time.
3. **`ChainMap(cli_args, env_vars, defaults)` (Example 03):** Holds references to the three existing dicts in `config.maps`. If `defaults["host"]` is later updated in place, `config["host"]` reflects the change immediately because no copy was made.

---

## 8. Common Mistakes

1. **Passing an Instance Instead of a Callable to `defaultdict`:**
   - Writing `defaultdict([])` raises `TypeError: first argument must be callable or None`. Always pass the factory type or callable: `defaultdict(list)` or `defaultdict(lambda: 100)`.
2. **Accidental Key Creation When Reading a `defaultdict`:**
   - Checking `if d["missing_key"] == 0:` on `defaultdict(int)` **inserts `"missing_key": 0` into `d`**! Use `if "missing_key" in d:` or `d.get("missing_key", 0)` when you don't want to mutate `d`.
3. **Random-Access Indexing in the Middle of a Large `deque` (`dq[50_000]`):**
   - While `dq[0]` and `dq[-1]` are $O(1)$, indexing the middle of a `deque` (`dq[i]`) requires walking pointers across blocks in $O(n)$ time! Use a `list` if you need $O(1)$ random access in the middle.

---

## 9. Practice Questions

1. **Easy:** Given two strings `s` and `t`, write a one-liner function `can_construct_ransom_note(note: str, magazine: str) -> bool` using `Counter` subtraction or `<=` comparison (Python 3.10+ `Counter(note) <= Counter(magazine)`).
2. **Medium:** Write a function `group_anagrams(words: list[str]) -> list[list[str]]` using `defaultdict(list)` keyed by `tuple(sorted(w))`.
3. **Hard:** Implement a `MovingAverageWindow(size: int)` class using `collections.deque(maxlen=size)` and a running sum attribute so `.next(val)` computes the window average in strictly $O(1)$ time per call (without calling `sum(dq)`).

---

## 10. Interview Questions

### Q1: What is the time complexity of `deque.popleft()` vs `list.pop(0)`, and why?
**Answer:**
- `list` is implemented as a contiguous dynamic array of pointers in C. `list.pop(0)` must shift all $N - 1$ remaining pointers one slot left via `memmove`, costing **$O(n)$** time.
- `deque` is implemented as a doubly-linked list of fixed-size 64-element C blocks. `deque.popleft()` simply increments the head index pointer (and frees a block when empty), costing strictly **$O(1)$** time.

### Q2: Is `OrderedDict` still useful now that regular `dict` preserves insertion order (since Python 3.7)?
**Answer:** Yes, in two specific cases:
1. `OrderedDict.move_to_end(key, last=True)` and `OrderedDict.popitem(last=False)` allow $O(1)$ LRU cache reordering and FIFO popping.
2. `OrderedDict` equality (`od1 == od2`) is **order-sensitive**, whereas regular `dict` equality (`{"a": 1, "b": 2} == {"b": 2, "a": 1}`) is `True` regardless of order.

### Q3: How does `Counter.subtract()` differ from the `-` operator on two `Counter` objects?
**Answer:**
- `c1 - c2` returns a **new** `Counter` and **discards** any keys whose resulting count is zero or negative (multiset behavior).
- `c1.subtract(c2)` mutates `c1` **in place** and **preserves** zero and negative counts.
