# Phase 5 — Topic 11: Map, Filter and Reduce

## 1. Introduction

**`map()`**, **`filter()`**, and **`functools.reduce()`** are the three classic higher-order functional programming primitives in Python. They allow you to transform, select, and aggregate sequences by passing functions as first-class arguments rather than writing explicit `for` loops with temporary accumulator lists.

In Python 3, both `map()` and `filter()` return **lazy iterators** (computing elements on demand in $O(1)$ memory), while `reduce()` lives in the `functools` standard library module and folds an iterable down into a single cumulative value.

---

## 2. Why is it used?

1. **Zero-Lambda C-Speed Dispatch:** When you already have an existing function or method (like `map(str.strip, lines)`, `map(int, tokens)`, or `reduce(operator.mul, nums, 1)`), `map` and `reduce` avoid Python stack-frame overhead per element.
2. **Lazy Pipeline Composition:** Because `map()` and `filter()` return iterators, chaining `filter(pred, map(transform, stream))` processes items one by one with zero intermediate list allocations.
3. **Expressive Multi-Iterable Mapping:** `map(func, iter1, iter2, iter3)` zips and applies a multi-argument function across parallel sequences in a single step.

---

## 3. Syntax

```python
import functools
import operator

# 1. map(function, iterable, *more_iterables) -> lazy map iterator
squared_iter = map(pow, [2, 3, 4], [2, 2, 2])      # 4, 9, 16

# 2. filter(predicate_or_None, iterable) -> lazy filter iterator
evens_iter = filter(lambda x: x % 2 == 0, [1, 2, 3, 4])
non_empty = filter(None, ["a", "", None, "b"])     # 'a', 'b'

# 3. functools.reduce(function, iterable[, initializer]) -> single value
product = functools.reduce(operator.mul, [2, 3, 4], 1)  # 24
```

---

## 4. Explanation (Step-by-Step)

1. **`map(func, *iterables)`:**
   - Pulls one element from each iterable and yields `func(x1, x2, ...)`.
   - If multiple iterables of unequal length are passed, `map()` stops as soon as the **shortest** iterable is exhausted.
2. **`filter(predicate, iterable)`:**
   - When `predicate` is a callable, yields every `item` for which `bool(predicate(item))` is `True`.
   - When `predicate` is `None` (`filter(None, iterable)`), yields every `item` that is itself truthy (`bool(item) is True`).
3. **`functools.reduce(func, iterable, initializer)`:**
   - Repeatedly applies `accumulator = func(accumulator, next_item)` from left to right.
   - **Always pass an explicit `initializer`** (e.g., `0` for addition, `1` for multiplication, `{}` for dict merging) so that calling `reduce()` on an empty iterable returns `initializer` instead of crashing with `TypeError: reduce() of empty iterable with no initial value`.
4. **When to Prefer Comprehensions / Generator Expressions:**
   - When the transformation requires writing an inline `lambda` (e.g., `map(lambda x: x * 2, items)`), PEP 8 and Pythonic style prefer `[x * 2 for x in items]` or `(x * 2 for x in items)` for readability.
   - When passing an already-named function (`map(int, row)`, `map(str.lower, words)`), `map()` is concise and fast.

---

## 5. Minimum 3 Examples

### Example 01: `map()` — Lazy Transformation on Single and Multiple Parallel Iterables
File: [`example_01_map_single_and_multiple_iterables.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/11_Map_Filter_and_Reduce/example_01_map_single_and_multiple_iterables.py)

```python
"""
Phase 5 - Topic 11: Map, Filter and Reduce
Example 01: `map()` — Lazy Transformation on Single and Multiple Parallel Iterables

Demonstrates:
  - Transforming a sequence lazily with `map(func, iterable)`
  - Passing multiple iterables to `map(func, iter1, iter2)` (stops at the shortest iterable)
  - Side-by-side comparison with equivalent list/generator comprehensions
"""


def format_price(amount: float, tax_rate: float) -> str:
    return f"Rs.{amount * (1 + tax_rate):,.2f}"


def main() -> None:
    print("=== 1. Single-Iterable `map(str.strip, ...)` ===")
    raw_tags = ["  python ", "dsa\n", "\tbackend  "]
    cleaned_map = map(str.strip, raw_tags)
    print(f"  map object (lazy iterator): {type(cleaned_map).__name__}")
    print(f"  Materialized list         : {list(cleaned_map)}")

    print("\n=== 2. Multi-Iterable `map(func, prices, taxes)` ===")
    base_prices = [1000.0, 2500.0, 500.0]
    tax_rates = [0.18, 0.28, 0.05]
    formatted = list(map(format_price, base_prices, tax_rates))
    print(f"  Formatted with tax        : {formatted}")

    print("\n=== 3. Equivalent List Comprehension Comparison ===")
    comp_result = [format_price(p, t) for p, t in zip(base_prices, tax_rates)]
    print(f"  Matches comprehension?    : {formatted == comp_result}")


if __name__ == "__main__":
    main()
```

### Example 02: `filter()` — Predicate Filtering, `filter(None, ...)`, & `itertools.filterfalse`
File: [`example_02_filter_predicates_and_none_truthiness.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/11_Map_Filter_and_Reduce/example_02_filter_predicates_and_none_truthiness.py)

```python
"""
Phase 5 - Topic 11: Map, Filter and Reduce
Example 02: `filter()` — Predicate Filtering, `filter(None, ...)`, & `itertools.filterfalse`

Demonstrates:
  - Filtering elements lazily using a predicate function `filter(pred, iterable)`
  - Passing `None` as the predicate (`filter(None, iterable)`) to strip all falsy values
  - Inverting the predicate with `itertools.filterfalse()`
"""

from itertools import filterfalse


def is_valid_port(port: int) -> bool:
    return 1024 <= port <= 65535


def main() -> None:
    print("=== 1. Predicate Filtering with `filter(is_valid_port, ...)` ===")
    candidate_ports = [22, 80, 5432, 8080, 70000, -1, 3000]
    valid = list(filter(is_valid_port, candidate_ports))
    invalid = list(filterfalse(is_valid_port, candidate_ports))
    print(f"  Valid unprivileged ports (`filter`)      : {valid}")
    print(f"  Rejected ports (`itertools.filterfalse`) : {invalid}")

    print("\n=== 2. Truthiness Filtering with `filter(None, iterable)` ===")
    messy_inputs = ["aarav", "", None, "diya", "   ".strip(), "rohan", 0]
    truthy_only = list(filter(None, messy_inputs))
    print(f"  After `filter(None, messy_inputs)`       : {truthy_only}")


if __name__ == "__main__":
    main()
```

### Example 03: `functools.reduce()` — Accumulators, Initializers, & `operator` Module Helpers
File: [`example_03_functools_reduce_and_comprehensions.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/11_Map_Filter_and_Reduce/example_03_functools_reduce_and_comprehensions.py)

```python
"""
Phase 5 - Topic 11: Map, Filter and Reduce
Example 03: `functools.reduce()` — Accumulators, Initializers, & `operator` Module Helpers

Demonstrates:
  - Folding a sequence into a single value using `functools.reduce(func, iterable, initializer)`
  - Combining `reduce` with `operator.mul` and dictionary merging (`operator.or_`)
  - Running prefix accumulations with `itertools.accumulate()`
"""

import functools
from itertools import accumulate
import operator


def main() -> None:
    numbers = [2, 3, 4, 5]

    print("=== 1. Product Calculation via `reduce(operator.mul, numbers, 1)` ===")
    product = functools.reduce(operator.mul, numbers, 1)
    running_products = list(accumulate(numbers, operator.mul))
    print(f"  Final product (`reduce`)          : {product}")
    print(f"  Running products (`accumulate`)   : {running_products}")

    print("\n=== 2. Why Always Supply an `initializer` for Empty Sequences ===")
    empty_list: list[int] = []
    safe_product = functools.reduce(operator.mul, empty_list, 1)
    print(f"  reduce(operator.mul, [], 1)       : {safe_product} (no TypeError on empty input!)")

    print("\n=== 3. Merging a List of Dictionaries with `reduce(operator.or_, ...)` ===")
    patches = [{"a": 1, "b": 2}, {"b": 20, "c": 30}, {"d": 40}]
    merged = functools.reduce(operator.or_, patches, {})
    print(f"  Merged dictionary                 : {merged}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== 1. Single-Iterable `map(str.strip, ...)` ===
  map object (lazy iterator): map
  Materialized list         : ['python', 'dsa', 'backend']

=== 2. Multi-Iterable `map(func, prices, taxes)` ===
  Formatted with tax        : ['Rs.1,180.00', 'Rs.3,200.00', 'Rs.525.00']

=== 3. Equivalent List Comprehension Comparison ===
  Matches comprehension?    : True
```

### Output — Example 02
```text
=== 1. Predicate Filtering with `filter(is_valid_port, ...)` ===
  Valid unprivileged ports (`filter`)      : [5432, 8080, 3000]
  Rejected ports (`itertools.filterfalse`) : [22, 80, 70000, -1]

=== 2. Truthiness Filtering with `filter(None, iterable)` ===
  After `filter(None, messy_inputs)`       : ['aarav', 'diya', 'rohan']
```

### Output — Example 03
```text
=== 1. Product Calculation via `reduce(operator.mul, numbers, 1)` ===
  Final product (`reduce`)          : 120
  Running products (`accumulate`)   : [2, 6, 24, 120]

=== 2. Why Always Supply an `initializer` for Empty Sequences ===
  reduce(operator.mul, [], 1)       : 1 (no TypeError on empty input!)

=== 3. Merging a List of Dictionaries with `reduce(operator.or_, ...)` ===
  Merged dictionary                 : {'a': 1, 'b': 20, 'c': 30, 'd': 40}
```

---

## 7. Code Explanation

1. **`map(str.strip, raw_tags)` (Example 01):** Passes the unbound `str.strip` method directly to `map()`. CPython invokes `str.strip(item)` in C without creating a Python lambda frame.
2. **`filter(None, messy_inputs)` (Example 02):** Passing `None` as the first argument to `filter()` is a built-in fast path that drops `""`, `None`, `0`, `False`, and empty containers.
3. **`reduce(operator.or_, patches, {})` (Example 03):** Uses the bitwise/dict-union operator (`|` via `operator.or_`) to fold a list of partial configuration dictionaries into a single merged dictionary.

---

## 8. Common Mistakes

1. **Expecting `map()` or `filter()` to Return a `list` in Python 3:**
   - In Python 2, `map()` and `filter()` returned `list`s. In Python 3, they return single-pass lazy iterators (`<map object>`, `<filter object>`). Wrap in `list(...)` if you need a concrete list or multiple passes.
2. **Using `filter(None, nums)` When `0` Is a Valid Number:**
   - Because `bool(0)` is `False`, `filter(None, [10, 0, 20, None])` removes **both** `None` and `0` (`[10, 20]`)! To drop only `None`, use `[x for x in nums if x is not None]`.
3. **Using `reduce(lambda a, b: a + b, strings)` to Join Strings:**
   - Repeated string concatenation inside `reduce()` is $O(n^2)$. Always use `"".join(strings)` ($O(n)$) or `math.prod(nums)` / `sum(nums)` when dedicated built-ins exist.

---

## 9. Practice Questions

1. **Easy:** Use `map()` and `str.title` to normalize a list of lowercase city names `["bengaluru", "new delhi", "mumbai"]`.
2. **Medium:** Use `functools.reduce()` and `operator.xor` to find the single non-duplicate integer in `[4, 1, 2, 1, 2]` in $O(n)$ time and $O(1)$ space.
3. **Hard:** Write a function `compose(*functions)` using `functools.reduce()` that returns a single composed callable applying the functions from right to left (`compose(f, g, h)(x) == f(g(h(x)))`).

---

## 10. Interview Questions

### Q1: Why was `reduce()` moved from built-ins into `functools` in Python 3?
**Answer:** Guido van Rossum noted that 90% of `reduce()` calls in real-world code were either `sum()`, `all()`, `any()`, or `math.prod()`, while complex nested `reduce(lambda acc, x: ..., ...)` expressions were much harder to read than a 3-line `for` loop. Moving `reduce` to `functools` kept it available for genuine functional folds (like `operator.xor` or function composition) while encouraging readable built-ins like `sum()`.

### Q2: What is the difference between `functools.reduce()` and `itertools.accumulate()`?
**Answer:**
- `functools.reduce(func, iterable)` returns **only the single final accumulated value**.
- `itertools.accumulate(iterable, func)` returns a **lazy iterator yielding every intermediate running accumulation** (e.g., prefix sums or prefix products) up to the final value.

### Q3: What happens if you pass two lists of lengths 3 and 5 to `map(func, list_a, list_b)`?
**Answer:** `map()` stops gracefully after **3 elements** (the length of the shortest iterable) without raising an error, just like `zip()`.
