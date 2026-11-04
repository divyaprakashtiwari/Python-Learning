# Phase 5 — Topic 12: Enumerate and Zip

## 1. Introduction

**`enumerate()`** and **`zip()`** are two of the most idiomatic built-in iterator tools in Python.
- `enumerate(iterable, start=0)` pairs each element of an iterable with an automatic running counter `(index, value)`, eliminating manual `for i in range(len(seq)):` indexing.
- `zip(*iterables, strict=False)` aggregates elements from two or more iterables in lockstep, yielding `(a_i, b_i, ...)` tuples lazily.

Together, they make parallel sequence processing, dictionary construction, and 2D matrix transposition concise and bug-free.

---

## 2. Why is it used?

1. **Works on Any Iterable (Not Just Indexable Sequences):** `range(len(obj))` fails on generators, files, and sets because they have no `len()` or `obj[i]`. `enumerate(stream)` works on **any** iterable!
2. **Eliminates Off-By-One & Manual Counter Bugs:** `enumerate(items, start=1)` handles 1-based numbering automatically without `i += 1` boilerplate.
3. **Lockstep Parallel Iteration & Validation (`zip(..., strict=True)`):** Python 3.10+ `strict=True` raises `ValueError` immediately if parallel sequences have mismatched lengths instead of silently dropping trailing data.
4. **One-Line Matrix Transposition (`zip(*matrix)`):** Unpacking rows into `zip(*matrix)` pivots rows into columns in a single expression.

---

## 3. Syntax

```python
from itertools import zip_longest

# 1. enumerate(iterable, start=0) -> lazy enumerate iterator of (index, item)
for idx, val in enumerate(["a", "b", "c"], start=1):
    print(idx, val)  # (1, 'a'), (2, 'b'), (3, 'c')

# 2. zip(*iterables, strict=False) -> lazy zip iterator of tuples
for k, v in zip(keys, values, strict=True):
    ...

# 3. Unzipping & Transposing via Star-Unpacking `*`
cols = list(zip(*matrix, strict=True))

# 4. Padding Uneven Iterables Instead of Truncating
padded = list(zip_longest(seq_a, seq_b, fillvalue=None))
```

---

## 4. Explanation (Step-by-Step)

1. **How `enumerate()` Works:**
   - Returns a lazy `enumerate` iterator object. On each `next()` call, it pulls the next value from the underlying iterable and yields `(current_counter, value)`, then increments `current_counter`.
2. **How `zip()` Handles Unequal Lengths:**
   - **Default (`strict=False`):** Stops as soon as the **shortest** input iterable is exhausted.
   - **Strict (`strict=True`, Python 3.10+):** Raises `ValueError` if one iterable finishes before another—essential when zipping table column headers with row values or model predictions with ground-truth labels.
   - **Padding (`itertools.zip_longest(*iterables, fillvalue=None)`):** Continues until the **longest** iterable is exhausted, substituting `fillvalue` for shorter iterables.
3. **Why `zip(*matrix)` Transposes a 2D Matrix:**
   - If `matrix = [[1, 2, 3], [4, 5, 6]]`, then `*matrix` unpacks the two rows as separate arguments: `zip([1, 2, 3], [4, 5, 6])`.
   - `zip` then pairs the 0th elements `(1, 4)`, 1st elements `(2, 5)`, and 2nd elements `(3, 6)`—which are the exact columns of `matrix`!

---

## 5. Minimum 3 Examples

### Example 01: `enumerate(iterable, start=...)` — Clean Index + Value Iteration
File: [`example_01_enumerate_start_index_and_unpacking.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/12_Enumerate_and_Zip/example_01_enumerate_start_index_and_unpacking.py)

```python
"""
Phase 5 - Topic 12: Enumerate and Zip
Example 01: `enumerate(iterable, start=...)` — Clean Index + Value Iteration

Demonstrates:
  - Replacing error-prone `for i in range(len(seq)):` loops with `enumerate()`
  - Setting a custom 1-based starting index (`start=1`) for human-readable rankings and line numbers
  - Building an O(1) value-to-index lookup dictionary via `{val: idx for idx, val in enumerate(seq)}`
"""


def main() -> None:
    runners = ["Aarav", "Diya", "Rohan", "Meera"]

    print("=== 1. 1-Based Leaderboard with `enumerate(runners, start=1)` ===")
    for rank, name in enumerate(runners, start=1):
        print(f"  Rank #{rank}: {name}")

    print("\n=== 2. Building an Value -> First-Index Map Using `enumerate` ===")
    index_map = {name: idx for idx, name in enumerate(runners)}
    print(f"  Index map: {index_map}")


if __name__ == "__main__":
    main()
```

### Example 02: `zip()` — Parallel Iteration, Dictionary Construction, & `strict=True` (Python 3.10+)
File: [`example_02_zip_parallel_iteration_and_strict_mode.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/12_Enumerate_and_Zip/example_02_zip_parallel_iteration_and_strict_mode.py)

```python
"""
Phase 5 - Topic 12: Enumerate and Zip
Example 02: `zip()` — Parallel Iteration, Dictionary Construction, & `strict=True` (Python 3.10+)

Demonstrates:
  - Iterating over multiple sequences in lockstep with `zip()`
  - Constructing dictionaries cleanly with `dict(zip(keys, values))`
  - Catching silent length-mismatch bugs immediately with `zip(..., strict=True)` (Python 3.10+)
"""


def main() -> None:
    headers = ["id", "username", "role"]
    row = [101, "aarav_dev", "admin"]

    print("=== 1. Building a Dictionary from Parallel Lists (`dict(zip(keys, values))`) ===")
    record = dict(zip(headers, row, strict=True))
    print(f"  Constructed dict: {record}")

    print("\n=== 2. Default Shortest-Truncation vs `strict=True` Guard ===")
    names = ["Alice", "Bob", "Charlie"]
    scores = [95, 88]  # Oops: missing Charlie's score!

    print(f"  Default `list(zip(names, scores))` : {list(zip(names, scores))} (silently dropped 'Charlie'!)")
    try:
        list(zip(names, scores, strict=True))
    except ValueError as err:
        print(f"  `zip(..., strict=True)` caught bug  : ValueError -> {err}")


if __name__ == "__main__":
    main()
```

### Example 03: Matrix Transposition (`zip(*matrix)`), Unzipping Pairs, & `itertools.zip_longest`
File: [`example_03_matrix_transpose_unzip_and_zip_longest.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/12_Enumerate_and_Zip/example_03_matrix_transpose_unzip_and_zip_longest.py)

```python
"""
Phase 5 - Topic 12: Enumerate and Zip
Example 03: Matrix Transposition (`zip(*matrix)`), Unzipping Pairs, & `itertools.zip_longest`

Demonstrates:
  - Transposing a 2D matrix (rows <-> columns) in one line using star-unpacking `zip(*matrix)`
  - Unzipping a list of `(x, y)` tuples back into separate `xs` and `ys` tuples
  - Padding uneven sequences instead of truncating using `itertools.zip_longest(..., fillvalue=...)`
"""

from itertools import zip_longest


def main() -> None:
    print("=== 1. 2D Matrix Transposition with `zip(*matrix)` ===")
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
    ]
    transposed = [list(col) for col in zip(*matrix, strict=True)]
    print(f"  Original (2x3)   : {matrix}")
    print(f"  Transposed (3x2) : {transposed}")

    print("\n=== 2. Unzipping `[(k, v), ...]` Pairs with `zip(*pairs)` ===")
    pairs = [("a", 10), ("b", 20), ("c", 30)]
    letters, numbers = zip(*pairs)
    print(f"  Letters : {letters} | Numbers : {numbers}")

    print("\n=== 3. Padding Uneven Iterables with `itertools.zip_longest` ===")
    q1_sales = [120, 150, 180]
    q2_sales = [140]
    padded = list(zip_longest(q1_sales, q2_sales, fillvalue=0))
    print(f"  zip_longest(..., fillvalue=0): {padded}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== 1. 1-Based Leaderboard with `enumerate(runners, start=1)` ===
  Rank #1: Aarav
  Rank #2: Diya
  Rank #3: Rohan
  Rank #4: Meera

=== 2. Building an Value -> First-Index Map Using `enumerate` ===
  Index map: {'Aarav': 0, 'Diya': 1, 'Rohan': 2, 'Meera': 3}
```

### Output — Example 02
```text
=== 1. Building a Dictionary from Parallel Lists (`dict(zip(keys, values))`) ===
  Constructed dict: {'id': 101, 'username': 'aarav_dev', 'role': 'admin'}

=== 2. Default Shortest-Truncation vs `strict=True` Guard ===
  Default `list(zip(names, scores))` : [('Alice', 95), ('Bob', 88)] (silently dropped 'Charlie'!)
  `zip(..., strict=True)` caught bug  : ValueError -> zip() argument 2 is shorter than argument 1
```

### Output — Example 03
```text
=== 1. 2D Matrix Transposition with `zip(*matrix)` ===
  Original (2x3)   : [[1, 2, 3], [4, 5, 6]]
  Transposed (3x2) : [[1, 4], [2, 5], [3, 6]]

=== 2. Unzipping `[(k, v), ...]` Pairs with `zip(*pairs)` ===
  Letters : ('a', 'b', 'c') | Numbers : (10, 20, 30)

=== 3. Padding Uneven Iterables with `itertools.zip_longest` ===
  zip_longest(..., fillvalue=0): [(120, 140), (150, 0), (180, 0)]
```

---

## 7. Code Explanation

1. **`enumerate(runners, start=1)` (Example 01):** Starts the counter at `1` while still reading `runners` from index `0`! A common beginner misconception is thinking `start=1` skips `runners[0]`—it does **not** skip any element; it only offsets the counter value.
2. **`zip(headers, row, strict=True)` (Example 02):** Guarantees that no column is silently dropped if `row` has fewer or more cells than `headers`.
3. **`letters, numbers = zip(*pairs)` (Example 03):** Passing `*pairs` unpacks the list of 2-tuples as arguments to `zip()`, which collects all first elements into `letters` and all second elements into `numbers`.

---

## 8. Common Mistakes

1. **Thinking `enumerate(seq, start=1)` Starts at `seq[1]`:**
   - `start=1` sets the **starting counter number** to `1` while still yielding `seq[0]` first (`(1, seq[0])`). To skip `seq[0]` while keeping true indices, use `itertools.islice(enumerate(seq), 1, None)`.
2. **Unpacking Improperly When Nesting `enumerate` and `zip`:**
   - In `enumerate(zip(a, b))`, each yielded item is `(idx, (x, y))`—a 2-tuple whose second item is a nested tuple! You must unpack with parentheses: `for idx, (x, y) in enumerate(zip(a, b)):`. Writing `for idx, x, y in enumerate(zip(a, b)):` raises `ValueError: not enough values to unpack (expected 3, got 2)`.
3. **Calling `zip(*[])` on an Empty List of Pairs:**
   - If `pairs = []`, `zip(*pairs)` returns an empty iterator, so `xs, ys = zip(*[])` raises `ValueError: not enough values to unpack`. Guard with `if pairs:` first.

---

## 9. Practice Questions

1. **Easy:** Given `nums = [10, 25, 30, 45, 50]`, use `enumerate()` and `zip(nums, nums[1:])` to check whether the list is strictly increasing and report the first index where the order breaks.
2. **Medium:** Write a function `rotate_matrix_90_clockwise(matrix: list[list[int]]) -> list[list[int]]` in one line using `zip(*matrix[::-1])`.
3. **Hard:** Write a function `chunk_fixed(iterator, size: int)` using the classic `[iter(iterator)] * size` + `zip(*..., strict=False)` idiom, and compare it with Python 3.12's `itertools.batched()`.

---

## 10. Interview Questions

### Q1: How does `zip(*([iter(seq)] * k))` group an iterable into $k$-tuples, and why does it work?
**Answer:** `[iter(seq)] * k` creates a list containing **$k$ references to the exact same single iterator object**. Unpacking those $k$ identical iterator references into `zip(*...)` causes `zip` to call `next()` on the shared iterator $k$ times per step, pulling $k$ consecutive elements into each tuple! (In Python 3.12+, `itertools.batched(seq, k)` is the clearer built-in replacement.)

### Q2: How do you correctly unpack `enumerate(zip(names, scores))` in a `for` loop?
**Answer:** Use nested tuple unpacking:
```python
for idx, (name, score) in enumerate(zip(names, scores)):
    ...
```

### Q3: When does `zip(a, b, strict=True)` raise `ValueError`—at creation time or during iteration?
**Answer:** **During iteration**, at the exact moment one of the underlying iterables raises `StopIteration` while another still has elements remaining. Because `zip()` is lazy and works on arbitrary iterators (which may not have a known `len()`), it cannot check lengths upfront when `zip()` is called.
