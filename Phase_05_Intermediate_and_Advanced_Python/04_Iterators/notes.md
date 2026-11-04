# Phase 5 — Topic 04: Iterators

## 1. Introduction

An **Iterator** is the stateful engine behind every `for` loop, unpacking assignment, comprehension, and `in` membership check in Python. While an **Iterable** (like a `list`, `tuple`, `dict`, or `str`) is a container that *can be looped over*, an **Iterator** is the bookmark object that remembers *where you currently are* in the sequence and produces the next element on demand when passed to `next()`.

Understanding the **Iterator Protocol** (`__iter__` and `__next__`) unlocks lazy evaluation—computing values one at a time in $O(1)$ memory instead of materializing millions of items upfront.

---

## 2. Why is it used?

1. **Constant $O(1)$ Memory Footprint:** An iterator over 100 million database rows or paginate offsets holds only the current cursor state in RAM, not a 100-million-element list.
2. **Unified Looping Interface:** Because `for x in obj:` relies strictly on `iter(obj)` and `next(it)`, the exact same loop syntax works over lists, files, network sockets, trees, and infinite streams.
3. **Composable Pipelines:** Functions like `zip()`, `enumerate()`, `map()`, `filter()`, and `itertools` consume and return iterators that chain together without intermediate list allocations.

---

## 3. Syntax

```python
# 1. Built-in Iterator Functions
iterator = iter(iterable)               # Calls iterable.__iter__()
first_item = next(iterator)             # Calls iterator.__next__(); raises StopIteration if exhausted
safe_item = next(iterator, "DEFAULT")   # Returns "DEFAULT" instead of raising StopIteration

# 2. Custom Iterator Class Implementing the Iterator Protocol
class CounterIterator:
    def __init__(self, low: int, high: int) -> None:
        self._current = low
        self._high = high

    def __iter__(self) -> "CounterIterator":
        return self

    def __next__(self) -> int:
        if self._current > self._high:
            raise StopIteration
        val = self._current
        self._current += 1
        return val
```

---

## 4. Explanation (Step-by-Step)

1. **Iterable vs Iterator (Crucial Distinction):**
   - **Iterable:** Any object implementing `__iter__()` that returns an **Iterator** (or implementing `__getitem__()` starting at index `0`). Examples: `list`, `str`, `dict`, `range`.
   - **Iterator:** Any object implementing **both** `__iter__()` (which returns `self`) and `__next__()` (which returns the next value or raises `StopIteration`).
   - Every **Iterator** is also an **Iterable** (because it has `__iter__`), but a `list` is an **Iterable**, **not** an **Iterator** (`next([1, 2])` raises `TypeError: 'list' object is not an iterator`).
2. **How Python Executes `for x in iterable:`:**
   - Step 1: Calls `it = iter(iterable)` once before the loop starts.
   - Step 2: Repeatedly calls `x = next(it)` and runs the loop body.
   - Step 3: When `next(it)` raises `StopIteration`, catches it silently and exits the loop.
3. **Single-Pass Exhaustion:**
   - Once an iterator raises `StopIteration`, it stays exhausted forever—subsequent calls to `next(it)` must continue raising `StopIteration`, and `list(it)` returns `[]`.
   - To make a custom collection reusable across multiple `for` loops, separate the **Iterable** container class from the **Iterator** cursor class (or return a generator from `__iter__`).

---

## 5. Minimum 3 Examples

### Example 01: The Iterator Protocol Under the Hood (`iter()`, `next()`, and `StopIteration`)
File: [`example_01_iter_next_and_stop_iteration_protocol.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/04_Iterators/example_01_iter_next_and_stop_iteration_protocol.py)

```python
"""
Phase 5 - Topic 04: Iterators
Example 01: The Iterator Protocol Under the Hood (`iter()`, `next()`, and `StopIteration`)

Demonstrates:
  - How Python's `for item in iterable:` loop actually desugars to `iter()` + `while True: next()`
  - Passing a default sentinel value to `next(iterator, default)` to avoid `StopIteration`
"""


def manual_for_loop(iterable: list[str]) -> None:
    """Manually emulate a Python `for` loop using `iter()` and `next()`."""
    iterator = iter(iterable)  # Calls iterable.__iter__()
    print(f"  Created iterator object: {type(iterator).__name__}")
    while True:
        try:
            item = next(iterator)  # Calls iterator.__next__()
        except StopIteration:
            print("  [StopIteration caught] Loop terminated cleanly.")
            break
        else:
            print(f"    -> Yielded item: {item!r}")


def main() -> None:
    print("=== 1. Emulating `for` Loop with `iter()`, `next()`, and `StopIteration` ===")
    manual_for_loop(["alpha", "beta", "gamma"])

    print("\n=== 2. Safe Pulling with Default Sentinel `next(it, default)` ===")
    tasks_iter = iter(["deploy-db", "run-migrations"])
    print(f"  Pull 1: {next(tasks_iter, '<queue-empty>')}")
    print(f"  Pull 2: {next(tasks_iter, '<queue-empty>')}")
    print(f"  Pull 3: {next(tasks_iter, '<queue-empty>')}")


if __name__ == "__main__":
    main()
```

### Example 02: Building a Custom Stateful Iterator Class (`__iter__` and `__next__`)
File: [`example_02_custom_iterator_class_dunder_iter_next.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/04_Iterators/example_02_custom_iterator_class_dunder_iter_next.py)

```python
"""
Phase 5 - Topic 04: Iterators
Example 02: Building a Custom Stateful Iterator Class (`__iter__` and `__next__`)

Demonstrates:
  - Implementing a custom `PaginatedRangeIterator` that computes slices lazily on demand in O(1) memory
  - Why an iterator's `__iter__` method must `return self`
"""


class PaginatedRangeIterator:
    """Lazy iterator yielding `(page_number, start_offset, end_offset)` tuples."""

    def __init__(self, total_items: int, page_size: int) -> None:
        if page_size <= 0:
            raise ValueError("page_size must be positive")
        self.total_items = total_items
        self.page_size = page_size
        self._current_offset = 0
        self._page_num = 0

    def __iter__(self) -> "PaginatedRangeIterator":
        return self

    def __next__(self) -> tuple[int, int, int]:
        if self._current_offset >= self.total_items:
            raise StopIteration
        self._page_num += 1
        start = self._current_offset
        end = min(start + self.page_size, self.total_items)
        self._current_offset = end
        return (self._page_num, start, end)


def main() -> None:
    print("=== Lazy Pagination Iterator Over 25 Items (page_size=10) ===")
    pager = PaginatedRangeIterator(total_items=25, page_size=10)
    for page_no, start_idx, end_idx in pager:
        print(f"  Page {page_no}: slice[{start_idx}:{end_idx}] ({end_idx - start_idx} items)")


if __name__ == "__main__":
    main()
```

### Example 03: Reusable Iterable vs Single-Pass Iterator Exhaustion Trap
File: [`example_03_iterable_vs_iterator_exhaustion.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/04_Iterators/example_03_iterable_vs_iterator_exhaustion.py)

```python
"""
Phase 5 - Topic 04: Iterators
Example 03: Reusable Iterable vs Single-Pass Iterator Exhaustion Trap

Demonstrates:
  - The crucial distinction between an **Iterable** (a container whose `__iter__` returns a
    fresh iterator each time) and an **Iterator** (which is exhausted after a single pass)
  - Using `iter(callable, sentinel)` two-argument form for sentinel-driven iteration
"""


class SinglePassFibonacci:
    """ANTI-PATTERN for reusable containers: acts as its own iterator (exhausts after 1 loop)."""

    def __init__(self, count: int) -> None:
        self.count = count
        self._index = 0
        self._a, self._b = 0, 1

    def __iter__(self) -> "SinglePassFibonacci":
        return self

    def __next__(self) -> int:
        if self._index >= self.count:
            raise StopIteration
        val = self._a
        self._a, self._b = self._b, self._a + self._b
        self._index += 1
        return val


class ReusableFibonacciIterable:
    """BEST PRACTICE: `__iter__` returns a fresh iterator instance on every loop."""

    def __init__(self, count: int) -> None:
        self.count = count

    def __iter__(self) -> SinglePassFibonacci:
        return SinglePassFibonacci(self.count)


def main() -> None:
    print("=== 1. Single-Pass Iterator Exhaustion Trap ===")
    single_pass = SinglePassFibonacci(6)
    print(f"  Pass 1: {list(single_pass)}")
    print(f"  Pass 2: {list(single_pass)}  <-- Empty! Already exhausted")

    print("\n=== 2. Reusable Iterable Returning Fresh Iterators ===")
    reusable = ReusableFibonacciIterable(6)
    print(f"  Pass 1: {list(reusable)}")
    print(f"  Pass 2: {list(reusable)}  <-- Works repeatedly!")

    print("\n=== 3. Two-Argument `iter(callable, sentinel)` Form ===")
    buffer = ["chunk-1", "chunk-2", "EOF", "ignored-chunk"]
    cursor = iter(buffer)
    # Calls `lambda: next(cursor)` repeatedly until it returns `"EOF"`
    chunks = list(iter(lambda: next(cursor), "EOF"))
    print(f"  Read chunks until 'EOF' sentinel: {chunks}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== 1. Emulating `for` Loop with `iter()`, `next()`, and `StopIteration` ===
  Created iterator object: list_iterator
    -> Yielded item: 'alpha'
    -> Yielded item: 'beta'
    -> Yielded item: 'gamma'
  [StopIteration caught] Loop terminated cleanly.

=== 2. Safe Pulling with Default Sentinel `next(it, default)` ===
  Pull 1: deploy-db
  Pull 2: run-migrations
  Pull 3: <queue-empty>
```

### Output — Example 02
```text
=== Lazy Pagination Iterator Over 25 Items (page_size=10) ===
  Page 1: slice[0:10] (10 items)
  Page 2: slice[10:20] (10 items)
  Page 3: slice[20:25] (5 items)
```

### Output — Example 03
```text
=== 1. Single-Pass Iterator Exhaustion Trap ===
  Pass 1: [0, 1, 1, 2, 3, 5]
  Pass 2: []  <-- Empty! Already exhausted

=== 2. Reusable Iterable Returning Fresh Iterators ===
  Pass 1: [0, 1, 1, 2, 3, 5]
  Pass 2: [0, 1, 1, 2, 3, 5]  <-- Works repeatedly!

=== 3. Two-Argument `iter(callable, sentinel)` Form ===
  Read chunks until 'EOF' sentinel: ['chunk-1', 'chunk-2']
```

---

## 7. Code Explanation

1. **`next(tasks_iter, '<queue-empty>')` (Example 01):** Supplying a second argument to `next()` catches `StopIteration` internally and returns the sentinel default value, which is ideal for peeking at the first item of a stream (`first = next(it, None)`).
2. **`PaginatedRangeIterator` (Example 02):** Instead of precomputing a list of page tuples, `__next__()` updates `self._current_offset` and `self._page_num` incrementally and raises `StopIteration` once `self._current_offset >= self.total_items`.
3. **`ReusableFibonacciIterable` vs `SinglePassFibonacci` (Example 03):** `ReusableFibonacciIterable.__iter__()` instantiates a brand-new `SinglePassFibonacci` cursor every time `iter()` is called, allowing unlimited independent loops (even nested loops!) over the same sequence.

---

## 8. Common Mistakes

1. **Looping Twice Over an Iterator Variable (`zip`, `map`, `filter`, or generator):**
   - `pairs = zip(a, b); list(pairs); list(pairs)` — the second `list(pairs)` is always `[]` because `zip` returns a single-pass iterator, not a reusable container.
2. **Forgetting `__iter__(self) -> self` on a Custom Iterator Class:**
   - If a class defines `__next__` without `__iter__`, calling `next(obj)` works, but `for x in obj:` fails with `TypeError: 'MyClass' object is not iterable`.
3. **Mutating a `list` or `dict` While Iterating Over It:**
   - Adding or deleting keys in a `dict` during iteration raises `RuntimeError: dictionary changed size during iteration`. Removing items from a `list` while iterating skips elements because indices shift left.
4. **Resetting State Inside `__iter__` on a Self-Iterator:**
   - Resetting `self._index = 0` inside `__iter__` breaks nested loops (`for x in obj: for y in obj:`) because both loops share the same cursor attribute! Always return a separate iterator object from `__iter__`.

---

## 9. Practice Questions

1. **Easy:** Write a custom iterator class `StepRange(start: int, stop: int, step: int)` that mimics `range()` for positive integer steps using `__iter__` and `__next__`.
2. **Medium:** Write a class `BatchIterator(items: list, batch_size: int)` that yields non-overlapping sub-lists of size `batch_size` (with the final batch containing any remaining items).
3. **Hard:** Implement a `PeekingIterator` wrapper around any iterator that provides a `.peek()` method returning the next element **without advancing** the iterator, alongside standard `__next__()` and `.has_next()`.

---

## 10. Interview Questions

### Q1: Why is `range(1_000_000)` an Iterable but NOT an Iterator in Python 3?
**Answer:**
- `range` supports `len()`, indexing (`range(10)[5]`), and multiple independent `for` loops because calling `iter(range(10))` returns a fresh `range_iterator` each time.
- Calling `next(range(10))` directly raises `TypeError: 'range' object is not an iterator`.

### Q2: How can you check at runtime whether an object is an Iterable vs an Iterator?
**Answer:** Use `collections.abc`:
- `isinstance(obj, collections.abc.Iterable)` checks for `__iter__` (note: `iter(obj)` is even more complete as it also covers legacy `__getitem__` sequences).
- `isinstance(obj, collections.abc.Iterator)` checks for both `__iter__` and `__next__` (or `iter(obj) is obj`).

### Q3: What is the two-argument form of `iter(callable, sentinel)` used for?
**Answer:** `iter(callable, sentinel)` creates an iterator that calls `callable()` with zero arguments on each step until the return value equals `sentinel`, at which point it raises `StopIteration`. It is commonly used for chunked binary file reading: `for chunk in iter(lambda: fh.read(4096), b""): ...`.
