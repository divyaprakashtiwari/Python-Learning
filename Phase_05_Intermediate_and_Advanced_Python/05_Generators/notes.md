# Phase 5 — Topic 05: Generators

## 1. Introduction

**Generators** are Python's most ergonomic way to create lazy iterators without writing boilerplate classes with `__iter__` and `__next__`. Any function that contains the `yield` keyword automatically becomes a **generator function**: calling it does not run its body immediately, but instead returns a **generator iterator object** whose execution frame pauses at each `yield` and resumes right where it left off on the next `next()` call.

Alongside generator functions, **generator expressions** (`(expr for x in iterable)`) let you build memory-efficient streaming pipelines in a single line.

---

## 2. Why is it used?

1. **Zero Boilerplate Lazy Iterators:** Replaces 25 lines of `__init__`, `__iter__`, and `__next__` state-machine code with a natural loop containing `yield`.
2. **Massive Memory Savings:** A list comprehension of 100,000 integers allocates ~800 KB upfront, whereas a generator expression over 100,000 (or 100 billion) integers occupies a constant **200 bytes** in RAM.
3. **Composable Streaming Pipelines:** Chaining multiple generators (`stage3(stage2(stage1(lines)))`) pulls one item at a time through the entire pipeline without materializing intermediate lists.
4. **Subgenerator Delegation (`yield from`):** Cleanly delegates iteration (including `.send()` and `.throw()` signals and return values) to nested generators or recursive tree traversals.

---

## 3. Syntax

```python
from typing import Iterator

# 1. Generator Function using `yield`
def count_up_to(limit: int) -> Iterator[int]:
    current = 1
    while current <= limit:
        yield current
        current += 1

# 2. Delegating to a Sub-Iterable or Recursive Generator with `yield from`
def chain_two(a: list[int], b: list[int]) -> Iterator[int]:
    yield from a
    yield from b

# 3. Generator Expression (Parentheses instead of Square Brackets)
squares_gen = (n * n for n in range(1_000_000) if n % 2 == 0)
total = sum(n * n for n in range(100))  # Parentheses optional when sole argument
```

---

## 4. Explanation (Step-by-Step)

1. **Generator Lifecycle States (`inspect.getgeneratorstate`):**
   - `GEN_CREATED`: Returned by calling `gen = my_gen_func()`, before the first `next(gen)`.
   - `GEN_RUNNING`: Currently executing statements inside the generator frame.
   - `GEN_SUSPENDED`: Paused at a `yield` expression; all local variables and the instruction pointer are frozen on the heap.
   - `GEN_CLOSED`: Exhausted (after raising `StopIteration` or calling `gen.close()`).
2. **How `return` Works Inside a Generator:**
   - Reaching the end of a generator function (or an explicit `return value`) raises `StopIteration(value)`.
   - When a parent generator delegates via `result = yield from subgenerator()`, the `value` attached to `StopIteration(value)` becomes the assignment result of the `yield from` expression!
3. **Resource Cleanup in Generators (`try / finally` and `.close()`):**
   - If a caller stops iterating early (e.g., `break` in a `for` loop), calling `gen.close()` injects `GeneratorExit` at the paused `yield` point so `finally:` blocks or `with` blocks inside the generator still execute.

---

## 5. Minimum 3 Examples

### Example 01: Generator Functions (`yield`) & Frame Suspension Lifecycle
File: [`example_01_yield_lifecycle_and_state_suspension.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/05_Generators/example_01_yield_lifecycle_and_state_suspension.py)

```python
"""
Phase 5 - Topic 05: Generators
Example 01: Generator Functions (`yield`) & Frame Suspension Lifecycle

Demonstrates:
  - How the presence of `yield` turns a function into a generator factory
  - Tracing execution pause and resumption across `next()` calls
  - Inspecting generator states (`GEN_CREATED`, `GEN_SUSPENDED`, `GEN_CLOSED`) via `inspect.getgeneratorstate()`
"""

import inspect
from typing import Iterator


def deployment_pipeline() -> Iterator[str]:
    """Yield deployment stages one by one, pausing local state between yields."""
    print("    [generator] Starting pipeline setup...")
    yield "Stage 1: Build Docker Image"
    print("    [generator] Resumed after Stage 1...")
    yield "Stage 2: Run Integration Tests"
    print("    [generator] Resumed after Stage 2...")
    yield "Stage 3: Rollout to Production"
    print("    [generator] Pipeline complete! Exiting function -> StopIteration.")


def main() -> None:
    print("=== Tracing Generator Suspension & Resumption ===")
    gen = deployment_pipeline()
    print(f"  State before first next(): {inspect.getgeneratorstate(gen)}")

    for step in range(1, 4):
        stage = next(gen)
        print(f"  Step {step} received: {stage!r} | state={inspect.getgeneratorstate(gen)}")

    try:
        next(gen)
    except StopIteration:
        print(f"  State after StopIteration: {inspect.getgeneratorstate(gen)}")


if __name__ == "__main__":
    main()
```

### Example 02: Subgenerator Delegation with `yield from` & Recursive Tree Flattening
File: [`example_02_yield_from_delegation_and_tree_flattening.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/05_Generators/example_02_yield_from_delegation_and_tree_flattening.py)

```python
"""
Phase 5 - Topic 05: Generators
Example 02: Subgenerator Delegation with `yield from` & Recursive Tree Flattening

Demonstrates:
  - Delegating iteration to sub-iterables cleanly using `yield from`
  - Flattening arbitrarily nested lists recursively in O(depth) memory using `yield from`
  - Capturing a subgenerator's `return` value via `result = yield from subgen()`
"""

from typing import Iterator


def flatten_nested(items: list[object]) -> Iterator[int]:
    """Recursively yield all integers from arbitrarily nested lists using `yield from`."""
    for element in items:
        if isinstance(element, list):
            yield from flatten_nested(element)
        elif isinstance(element, int):
            yield element


def chunk_checksum_subgen(chunk: list[int]) -> Iterator[int]:
    """Yield each number in `chunk` and return their sum as the generator's StopIteration value."""
    running = 0
    for num in chunk:
        running += num
        yield num
    return running


def stream_with_audit(batches: list[list[int]]) -> Iterator[int]:
    """Delegate to `chunk_checksum_subgen` and capture its `return` value via `yield from`."""
    for idx, batch in enumerate(batches, start=1):
        batch_sum = yield from chunk_checksum_subgen(batch)
        print(f"    [audit] Batch #{idx} finished with sum = {batch_sum}")


def main() -> None:
    print("=== 1. Recursive Nested List Flattening with `yield from` ===")
    nested: list[object] = [1, [2, 3, [4, 5]], [], [[6], 7]]
    print(f"  Flattened: {list(flatten_nested(nested))}")

    print("\n=== 2. Capturing Subgenerator Return Value (`total = yield from ...`) ===")
    streamed = list(stream_with_audit([[10, 20], [5, 15, 25]]))
    print(f"  All yielded items: {streamed}")


if __name__ == "__main__":
    main()
```

### Example 03: Generator Expressions, Lazy Streaming Pipelines, & `sys.getsizeof()` Memory Comparison
File: [`example_03_generator_expressions_and_streaming_pipeline.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/05_Generators/example_03_generator_expressions_and_streaming_pipeline.py)

```python
"""
Phase 5 - Topic 05: Generators
Example 03: Generator Expressions, Lazy Streaming Pipelines, & `sys.getsizeof()` Memory Comparison

Demonstrates:
  - Comparing memory usage of a 100,000-element list comprehension vs a generator expression
  - Building a multi-stage lazy log processing pipeline where zero intermediate lists are allocated
"""

import sys
from typing import Iterable, Iterator


def parse_status_codes(raw_logs: Iterable[str]) -> Iterator[tuple[str, int]]:
    """Stage 1: Parse `'ENDPOINT STATUS_CODE'` lines lazily."""
    for line in raw_logs:
        endpoint, code_str = line.strip().split()
        yield endpoint, int(code_str)


def filter_server_errors(parsed: Iterable[tuple[str, int]]) -> Iterator[str]:
    """Stage 2: Yield only endpoints with 5xx HTTP status codes."""
    return (f"{ep} (HTTP {code})" for ep, code in parsed if 500 <= code < 600)


def main() -> None:
    print("=== 1. Memory Footprint: List Comprehension vs Generator Expression ===")
    list_comp = [x * x for x in range(100_000)]
    gen_expr = (x * x for x in range(100_000))
    print(f"  List comprehension (100k ints) : {sys.getsizeof(list_comp):>9,} bytes")
    print(f"  Generator expression (100k)    : {sys.getsizeof(gen_expr):>9,} bytes (constant O(1)!)")

    print("\n=== 2. Multi-Stage Lazy Streaming Pipeline ===")
    raw_log_stream = [
        "/api/users 200",
        "/api/orders 502",
        "/api/health 200",
        "/api/payments 504",
        "/api/cart 404",
    ]
    pipeline = filter_server_errors(parse_status_codes(raw_log_stream))
    print(f"  Pipeline object: {type(pipeline).__name__}")
    print(f"  5xx Alerts     : {list(pipeline)}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== Tracing Generator Suspension & Resumption ===
  State before first next(): GEN_CREATED
    [generator] Starting pipeline setup...
  Step 1 received: 'Stage 1: Build Docker Image' | state=GEN_SUSPENDED
    [generator] Resumed after Stage 1...
  Step 2 received: 'Stage 2: Run Integration Tests' | state=GEN_SUSPENDED
    [generator] Resumed after Stage 2...
  Step 3 received: 'Stage 3: Rollout to Production' | state=GEN_SUSPENDED
    [generator] Pipeline complete! Exiting function -> StopIteration.
  State after StopIteration: GEN_CLOSED
```

### Output — Example 02
```text
=== 1. Recursive Nested List Flattening with `yield from` ===
  Flattened: [1, 2, 3, 4, 5, 6, 7]

=== 2. Capturing Subgenerator Return Value (`total = yield from ...`) ===
    [audit] Batch #1 finished with sum = 30
    [audit] Batch #2 finished with sum = 45
  All yielded items: [10, 20, 5, 15, 25]
```

### Output — Example 03
```text
=== 1. Memory Footprint: List Comprehension vs Generator Expression ===
  List comprehension (100k ints) :   800,984 bytes
  Generator expression (100k)    :       200 bytes (constant O(1)!)

=== 2. Multi-Stage Lazy Streaming Pipeline ===
  Pipeline object: generator
  5xx Alerts     : ['/api/orders (HTTP 502)', '/api/payments (HTTP 504)']
```

---

## 7. Code Explanation

1. **`inspect.getgeneratorstate(gen)` (Example 01):** Shows that calling `deployment_pipeline()` executes **zero lines** of `deployment_pipeline` (`GEN_CREATED`) until the first `next(gen)` call advances execution up to the first `yield` (`GEN_SUSPENDED`).
2. **`batch_sum = yield from chunk_checksum_subgen(batch)` (Example 02):** `yield from` transparently forwards every `yield num` straight to the outer caller, and when `chunk_checksum_subgen` executes `return running`, `yield from` catches `StopIteration(running)` and assigns `running` to `batch_sum`.
3. **Memory Comparison (Example 03):** `sys.getsizeof(list_comp)` is `800,984` bytes (just for the pointer array, plus the integer objects), whereas `sys.getsizeof(gen_expr)` is `200` bytes regardless of whether `range()` spans `100_000` or `10**12`.

---

## 8. Common Mistakes

1. **Expecting Argument Validation Inside a Generator Function to Run Immediately on Call:**
   - Because calling a generator function only returns a `GEN_CREATED` generator object, a `if page_size <= 0: raise ValueError(...)` check at the top of a generator function **will not run until the first `next()` call**! If eager validation is required, validate in a regular wrapper function that returns an inner `_gen()`.
2. **Catching `GeneratorExit` and Yielding Another Value:**
   - Inside a generator's `try / except`, catching `GeneratorExit` (or bare `except:`) and executing another `yield` raises `RuntimeError: generator ignored GeneratorExit`.
3. **Manually Raising `StopIteration` Inside a Generator (PEP 479):**
   - Since Python 3.7, raising `StopIteration` explicitly inside a generator is converted into a `RuntimeError`. Use `return` to terminate a generator cleanly.
4. **Assuming Generators Support `len()` or Indexing (`gen[0]`):**
   - Generators do not know their length in advance and do not support random access; use `itertools.islice(gen, start, stop)` to slice a generator lazily.

---

## 9. Practice Questions

1. **Easy:** Write an infinite generator `fibonacci_stream() -> Iterator[int]` and use `itertools.islice()` to grab the first 10 Fibonacci numbers.
2. **Medium:** Write a generator `sliding_window(iterable: Iterable[int], k: int) -> Iterator[tuple[int, ...]]` using `collections.deque(maxlen=k)` that yields all contiguous windows of length `k` in $O(k)$ memory.
3. **Hard:** Write a Bidirectional Accumulator coroutine generator using `received = yield current_average` that accepts new numbers via `.send(value)` and yields the running average at every step.

---

## 10. Interview Questions

### Q1: Why did PEP 479 change uncaught `StopIteration` inside a generator into `RuntimeError`?
**Answer:** Prior to Python 3.7, if a function called inside a generator (such as `next(other_iter)`) accidentally raised an unhandled `StopIteration`, the generator silently terminated as if it had finished normally, hiding bugs. PEP 479 ensures that only a `return` (or falling off the end of the generator body) terminates the generator; an uncaught `StopIteration` inside the body raises `RuntimeError("generator raised StopIteration")`.

### Q2: When should you prefer a list comprehension over a generator expression?
**Answer:**
- Prefer a **list comprehension** when you need to iterate over the results **multiple times**, need `len()` or indexing (`result[0]`, `result[-1]`), or plan to sort/mutate the result in place.
- Prefer a **generator expression** when making a **single pass** (e.g., `sum(...)`, `any(...)`, `all(...)`, `max(...)`) or streaming large datasets where allocating the full list would waste memory.

### Q3: What is the difference between `for item in subgen: yield item` and `yield from subgen`?
**Answer:** While both yield the elements of `subgen` during basic `for` loops, `yield from subgen` also forwards `.send()`, `.throw()`, and `.close()` calls directly into `subgen` and returns `subgen`'s `return` value (`StopIteration.value`) as the value of the `yield from` expression.
