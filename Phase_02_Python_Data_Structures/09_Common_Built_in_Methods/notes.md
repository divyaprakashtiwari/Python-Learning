# Topic 09: Common Built-in Methods & Functions

---

## 1. Introduction

Python ships with a rich set of **built-in functions** (always available without any `import` statement) and universal **container methods** that work consistently across strings, lists, tuples, sets, and dictionaries.

Knowing these built-in functions saves you from reinventing the wheel—and because they are implemented directly in C inside CPython, they execute significantly faster than manual Python loops!

---

## 2. Why is it used?

1. **Expressive One-Line Aggregations:** `min(words, key=len)`, `max(scores, default=0)`, `sum(prices)`, `any(...)`, and `all(...)` replace verbose 6-line loops.
2. **Competitive Programming & Cryptography (`pow(base, exp, mod)`):** Python's 3-argument `pow(a, b, m)` computes $(a^b) \bmod m$ using binary exponentiation in **`O(log b)`** time, which is essential for modular arithmetic and Fermat's Little Theorem modular inverses `pow(a, MOD - 2, MOD)`.
3. **Clean Parallel Iteration (`zip`, `enumerate`, `reversed`):** Avoids manual index bookkeeping and off-by-one bugs.

---

## 3. Syntax

```python
# 1. Aggregation & Quantifiers
total = sum([10, 20, 30], start=0)
longest = max(["a", "abcd", "ab"], key=len, default="")
has_negative = any(x < 0 for x in nums)
all_positive = all(x > 0 for x in nums)

# 2. Sequence Iteration Utilities
for idx, val in enumerate(seq, start=1): ...
for a, b in zip(list1, list2, strict=False): ...
for item in reversed(seq): ...

# 3. Numeric & Division Utilities
quotient, remainder = divmod(17, 5)        # (3, 2)
mod_exp = pow(2, 1000, 1_000_000_007)      # (2**1000) % (10^9 + 7) in O(log b)
```

---

## 4. Explanation (Key Built-in Mechanics)

| Built-in Function | Purpose | Key Feature / Time Complexity |
| :--- | :--- | :--- |
| `len(obj)` | Returns item count | **`O(1)`** (reads cached C struct `ob_size` field!) |
| `sum(iterable, start=0)` | Sums numeric items | `O(n)` in C |
| `min(it, key=..., default=...)` | Returns smallest item | `default=` prevents `ValueError` on empty iterables |
| `max(it, key=..., default=...)` | Returns largest item | `key=` customizes comparison criterion |
| `any(iterable)` | `True` if at least 1 item is truthy | **Short-circuits** on the first `True`! (`False` on `[]`) |
| `all(iterable)` | `True` if every item is truthy | **Short-circuits** on the first `False`! (`True` on `[]`) |
| `divmod(a, b)` | Returns `(a // b, a % b)` | Computes quotient and remainder in one CPU division step |
| `pow(a, b, mod)` | Computes `(a ** b) % mod` | **`O(log b)`** binary exponentiation |
| `round(x, n)` | Rounds to `n` decimals | Uses **Banker's Rounding** (round half to even) |

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_aggregation_and_predicate_builtins.py`](example_01_aggregation_and_predicate_builtins.py)
- [`example_02_iteration_builtins_zip_enumerate_reversed.py`](example_02_iteration_builtins_zip_enumerate_reversed.py)
- [`example_03_numeric_and_inspection_builtins.py`](example_03_numeric_and_inspection_builtins.py)

### Example 1: Aggregation (`sum`, `min`, `max`) and Logic (`any`, `all`) (`example_01_aggregation_and_predicate_builtins.py`)

```python
def main() -> None:
    scores = [78, 92, 85, 64, 99]
    words = ["graph", "dp", "backtracking", "tree"]

    print("=== 1. Aggregation Built-ins: len(), sum(), min(), max() ===")
    print(f"Count (len)             : {len(scores)}")
    print(f"Total (sum)             : {sum(scores)}")
    print(f"Sum with base=100       : {sum(scores, start=100)}")
    print(f"Shortest Word (key=len) : {min(words, key=len)!r}")
    print(f"Longest Word (key=len)  : {max(words, key=len)!r}")
    print(f"Safe max on empty []    : {max([], default=-1)}")

    print("\n=== 2. Logical Quantifiers: any() and all() ===")
    all_passed = all(s >= 50 for s in scores)
    any_perfect = any(s == 100 for s in scores)
    any_distinction = any(s >= 95 for s in scores)
    print(f"Did ALL students score >= 50? : {all_passed}")
    print(f"Did ANY student score 100?    : {any_perfect}")
    print(f"Did ANY student score >= 95?  : {any_distinction}")


if __name__ == "__main__":
    main()
```

### Example 2: Sequence Iteration Built-ins (`enumerate`, `zip`, `reversed`) (`example_02_iteration_builtins_zip_enumerate_reversed.py`)

```python
def main() -> None:
    names = ["Divya", "Aarav", "Sneha"]
    cities = ["New Delhi", "Mumbai", "Bengaluru"]
    ranks = [1, 2, 3]

    zipped_profiles = list(zip(ranks, names, cities))
    print("=== 1. Pairing Multiple Iterables with zip() ===")
    print(f"Zipped Profiles : {zipped_profiles}")

    unzipped_ranks, unzipped_names, unzipped_cities = zip(*zipped_profiles)
    print("\n=== 2. Unzipping with zip(*zipped_profiles) ===")
    print(f"Unzipped Names  : {unzipped_names}")
    print(f"Unzipped Cities : {unzipped_cities}")

    print("\n=== 3. Reverse Iteration with reversed() ===")
    rev_names = list(reversed(names))
    print(f"Reversed Names  : {rev_names} (Original unchanged: {names})")


if __name__ == "__main__":
    main()
```

### Example 3: Numeric Built-ins (`divmod`, 3-Arg `pow`, `round`) and Inspection (`example_03_numeric_and_inspection_builtins.py`)

```python
def main() -> None:
    total_minutes = 135
    hours, mins = divmod(total_minutes, 60)
    print("=== 1. Simultaneous Quotient & Remainder with divmod() ===")
    print(f"divmod(135, 60) -> {hours} hours, {mins} minutes")

    MOD = 1_000_000_007
    fast_mod_pow = pow(2, 1000, MOD)
    print("\n=== 2. Fast Modular Exponentiation: pow(base, exp, mod) ===")
    print(f"pow(2, 1000, 10^9 + 7) = {fast_mod_pow}")

    print("\n=== 3. Banker's Rounding (round half to nearest even integer) ===")
    print(f"round(2.5) -> {round(2.5)}  (rounds to even 2)")
    print(f"round(3.5) -> {round(3.5)}  (rounds to even 4)")

    print("\n=== 4. Object Inspection Built-ins ===")
    print(f"isinstance(42, (int, float)) : {isinstance(42, (int, float))}")
    print(f"callable(len)                : {callable(len)}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== 1. Aggregation Built-ins: len(), sum(), min(), max() ===
Count (len)             : 5
Total (sum)             : 418
Sum with base=100       : 518
Shortest Word (key=len) : 'dp'
Longest Word (key=len)  : 'backtracking'
Safe max on empty []    : -1

=== 2. Logical Quantifiers: any() and all() ===
Did ALL students score >= 50? : True
Did ANY student score 100?    : False
Did ANY student score >= 95?  : True
```

### Output for Example 2:
```text
=== 1. Pairing Multiple Iterables with zip() ===
Zipped Profiles : [(1, 'Divya', 'New Delhi'), (2, 'Aarav', 'Mumbai'), (3, 'Sneha', 'Bengaluru')]

=== 2. Unzipping with zip(*zipped_profiles) ===
Unzipped Names  : ('Divya', 'Aarav', 'Sneha')
Unzipped Cities : ('New Delhi', 'Mumbai', 'Bengaluru')

=== 3. Reverse Iteration with reversed() ===
Reversed Names  : ['Sneha', 'Aarav', 'Divya'] (Original unchanged: ['Divya', 'Aarav', 'Sneha'])
```

### Output for Example 3:
```text
=== 1. Simultaneous Quotient & Remainder with divmod() ===
divmod(135, 60) -> 2 hours, 15 minutes

=== 2. Fast Modular Exponentiation: pow(base, exp, mod) ===
pow(2, 1000, 10^9 + 7) = 688423210

=== 3. Banker's Rounding (round half to nearest even integer) ===
round(2.5) -> 2  (rounds to even 2)
round(3.5) -> 4  (rounds to even 4)

=== 4. Object Inspection Built-ins ===
isinstance(42, (int, float)) : True
callable(len)                : True
```

---

## 7. Code Explanation

- **`max([], default=-1)`:** Calling `max([])` or `min([])` on an empty sequence raises `ValueError: max() iterable argument is empty`. Passing `default=-1` (or `default=None`) prevents crashes on empty inputs.
- **`pow(2, 1000, 1_000_000_007)`:** Instead of computing $2^{1000}$ first and then taking `%`, Python's 3-argument `pow(a, b, m)` reduces intermediate products modulo `m` at every squaring step in `O(log b)` time.
- **`round(2.5) == 2` and `round(3.5) == 4`:** Python 3 implements IEEE-754 **round-half-to-even (Banker's Rounding)** to eliminate upward statistical bias when summing thousands of rounded numbers.

---

## 8. Common Mistakes

1. **Calling `min()` or `max()` on Potentially Empty Filters Without `default=`:**
   `max(x for x in nums if x > 100)` crashes with `ValueError` if no element exceeds `100`. Always pass `default=None` or `default=0`: `max((x for x in nums if x > 100), default=0)`.
2. **Expecting `all([])` to Return `False`:**
   `all([])` returns **`True`** (**vacuous truth**: there are zero falsy elements in an empty list!). Conversely, `any([])` returns **`False`**.
3. **Silent Truncation in `zip()` When Lists Have Different Lengths:**
   By default, `zip([1, 2, 3], ['a', 'b'])` silently stops after 2 pairs and drops `3`. In Python 3.10+, pass `zip(a, b, strict=True)` to raise a `ValueError` if lengths do not match!

---

## 9. Practice Questions

1. **Easy:** Given a list of dictionaries representing products `[{"name": "Pen", "price": 20}, {"name": "Bag", "price": 950}]`, use `min()` and `max()` with `key=` to find the cheapest and most expensive product dictionaries.
2. **Medium:** Write a function `is_valid_sudoku_row(row: list[int]) -> bool` using `all()` and `set` that checks if a 9-element list contains only integers `1..9` with no duplicates.
3. **Hard:** Use `pow(a, m - 2, m)` (Fermat's Little Theorem) to compute the modular multiplicative inverse of `a` modulo prime `m = 1_000_000_007`, and verify that `(a * inv) % m == 1`.

---

## 10. Interview Questions

### Q1: How does `len(my_list)` run in `O(1)` time instead of counting elements in `O(n)`?
**Answer:** Every built-in Python container (`list`, `tuple`, `dict`, `set`, `str`) is backed by a `PyVarObject` C struct that maintains an explicit integer field (`ob_size` / `ma_used`) updated on every insertion or deletion. `len()` simply reads this integer in **`O(1)`** constant time.

### Q2: Why is `reversed(my_list)` preferred over `my_list[::-1]` when looping backward?
**Answer:** `my_list[::-1]` allocates a **full reversed copy** of the list in memory (`O(n)` space and `O(n)` copy time before the loop even starts). `reversed(my_list)` returns a lightweight **reverse iterator** in **`O(1)` time and `O(1)` memory** that walks backward over the existing list.

### Q3: Why does `(2 ** (10**7)) % 1000000007` time out in coding interviews while `pow(2, 10**7, 1000000007)` finishes in microseconds?
**Answer:** `(2 ** (10**7)) % m` first constructs a 10-million-bit integer in RAM before taking the remainder, consuming megabytes of memory and seconds of CPU time. `pow(2, 10**7, m)` performs **modular binary exponentiation**, keeping every intermediate integer smaller than $m^2$ and finishing in ~24 multiplications (`O(log(exp))`).
