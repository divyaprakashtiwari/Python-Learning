# Topic 06: List Comprehensions

---

## 1. Introduction

A **List Comprehension** is a concise, declarative, and Pythonic syntax for creating a new list by transforming and/or filtering elements from an existing iterable in a single expression (`[expression for item in iterable if condition]`).

Not only are list comprehensions cleaner to read than 4-line `for` + `.append()` loops, they are also **faster in CPython** because they use the specialized `LIST_APPEND` bytecode instruction instead of looking up the `.append` method attribute on every iteration!

---

## 2. Why is it used?

1. **Data Transformation & Filtering Pipelines:** Extracting specific fields from API payloads, cleaning strings, or filtering numeric arrays in one readable line.
2. **Safe 2D Matrix & DP Table Initialization:** `dp = [[0] * cols for _ in range(rows)]` guarantees every row is an independent list in memory.
3. **Flattening & Matrix Operations:** Flattening nested lists or transposing matrices cleanly without verbose temporary buffers.

---

## 3. Syntax

```python
# 1. Pure Mapping (Transform every element)
squares = [x * x for x in range(1, 6)]                   # [1, 4, 9, 16, 25]

# 2. Filtering (`if` at the END -> reduces list length)
evens = [x for x in range(1, 11) if x % 2 == 0]          # [2, 4, 6, 8, 10]

# 3. Conditional Expression (`if-else` at the FRONT -> keeps same length)
labels = ["Even" if x % 2 == 0 else "Odd" for x in [1, 2, 3]]

# 4. Flattening a 2D List (Outer loop first, Inner loop second)
flat = [cell for row in matrix for cell in row]
```

---

## 4. Explanation (Step-by-Step Translation from `for` Loops)

### Rule 1: `if` at the End (Filter) vs `if-else` at the Front (Ternary Map)
- **Filter (`if` at the end):**
  ```python
  [x * 2 for x in nums if x > 0]
  ```
  Only positive `x` values are included; negative values are dropped.
- **Ternary Map (`if-else` at the front):**
  ```python
  [x if x > 0 else 0 for x in nums]
  ```
  Every element in `nums` produces an output element (negative numbers are replaced with `0`).

### Rule 2: Reading Multi-Clause Comprehensions Left-to-Right
In `[cell for row in matrix for cell in row]`, the `for` clauses appear in the **exact same top-to-bottom order** as traditional nested `for` loops:
```python
flat = []
for row in matrix:          # 1st clause (outer loop)
    for cell in row:        # 2nd clause (inner loop)
        flat.append(cell)   # Leftmost expression
```

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_mapping_and_filtering_comprehensions.py`](example_01_mapping_and_filtering_comprehensions.py)
- [`example_02_nested_flattening_and_matrix_transpose.py`](example_02_nested_flattening_and_matrix_transpose.py)
- [`example_03_set_and_generator_comprehensions.py`](example_03_set_and_generator_comprehensions.py)

### Example 1: Mapping, Filtering (`if`), and Ternary (`if-else`) (`example_01_mapping_and_filtering_comprehensions.py`)

```python
def main() -> None:
    numbers = list(range(1, 11))

    squares = [n * n for n in numbers]
    even_squares = [n * n for n in numbers if n % 2 == 0]
    parity_labels = [f"{n}:Even" if n % 2 == 0 else f"{n}:Odd" for n in numbers[:6]]

    print("=== 1. Mapping & Filtering List Comprehensions ===")
    print(f"Input Numbers (1..10) : {numbers}")
    print(f"All Squares           : {squares}")
    print(f"Even Squares (Filter) : {even_squares}")
    print(f"Parity Labels (if/else): {parity_labels}")

    raw_emails = ["  DIVYA@example.com ", "invalid_email", " aarav@startup.io  ", ""]
    clean_valid_emails = [
        email.strip().lower()
        for email in raw_emails
        if "@" in email
    ]
    print("\n=== 2. Cleaned & Validated Emails ===")
    print(f"Cleaned Emails        : {clean_valid_emails}")


if __name__ == "__main__":
    main()
```

### Example 2: Flattening 2D Lists, Cartesian Products & Matrix Transpose (`example_02_nested_flattening_and_matrix_transpose.py`)

```python
def main() -> None:
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
    ]

    flattened = [cell for row in matrix for cell in row]

    num_cols = len(matrix[0])
    transposed = [[row[col_idx] for row in matrix] for col_idx in range(num_cols)]

    print("=== 1. 2D Matrix Flattening & Transposition ===")
    print(f"Original 2x3 Matrix   : {matrix}")
    print(f"Flattened 1D List     : {flattened}")
    print(f"Transposed 3x2 Matrix : {transposed}")

    ranks = ["A", "K", "Q"]
    suits = ["Spades", "Hearts"]
    cards = [f"{r} of {s}" for r in ranks for s in suits]
    print("\n=== 2. Cartesian Product ===")
    print(f"Generated Cards ({len(cards)}) : {cards}")


if __name__ == "__main__":
    main()
```

### Example 3: List Comprehension `[...]` vs Set Comprehension `{...}` vs Generator `(...)` (`example_03_set_and_generator_comprehensions.py`)

```python
import sys


def main() -> None:
    words = ["apple", "Banana", "APPLE", "cherry", "banana", "Date"]

    lower_list = [w.lower() for w in words]
    unique_lower_set = {w.lower() for w in words}
    print("=== 1. List Comprehension vs Set Comprehension ===")
    print(f"List Comprehension (keeps duplicates) : {lower_list}")
    print(f"Set Comprehension (unique sorted)     : {sorted(unique_lower_set)}")

    list_comp = [x * x for x in range(10_000)]
    gen_expr = (x * x for x in range(10_000))

    print("\n=== 2. Memory Efficiency: [List Comp] vs (Generator Expr) ===")
    print(f"List Comprehension size (10,000 items): {sys.getsizeof(list_comp)} bytes")
    print(f"Generator Expression size (lazy O(1)) : {sys.getsizeof(gen_expr)} bytes")
    print(f"Sum via Generator Expression          : {sum(x * x for x in range(1, 6))}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== 1. Mapping & Filtering List Comprehensions ===
Input Numbers (1..10) : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
All Squares           : [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
Even Squares (Filter) : [4, 16, 36, 64, 100]
Parity Labels (if/else): ['1:Odd', '2:Even', '3:Odd', '4:Even', '5:Odd', '6:Even']

=== 2. Cleaned & Validated Emails ===
Cleaned Emails        : ['divya@example.com', 'aarav@startup.io']
```

### Output for Example 2:
```text
=== 1. 2D Matrix Flattening & Transposition ===
Original 2x3 Matrix   : [[1, 2, 3], [4, 5, 6]]
Flattened 1D List     : [1, 2, 3, 4, 5, 6]
Transposed 3x2 Matrix : [[1, 4], [2, 5], [3, 6]]

=== 2. Cartesian Product ===
Generated Cards (6) : ['A of Spades', 'A of Hearts', 'K of Spades', 'K of Hearts', 'Q of Spades', 'Q of Hearts']
```

### Output for Example 3:
```text
=== 1. List Comprehension vs Set Comprehension ===
List Comprehension (keeps duplicates) : ['apple', 'banana', 'apple', 'cherry', 'banana', 'date']
Set Comprehension (unique sorted)     : ['apple', 'banana', 'cherry', 'date']

=== 2. Memory Efficiency: [List Comp] vs (Generator Expr) ===
List Comprehension size (10,000 items): 85176 bytes
Generator Expression size (lazy O(1)) : 200 bytes
Sum via Generator Expression          : 55
```

---

## 7. Code Explanation

- **`[[row[col_idx] for row in matrix] for col_idx in range(num_cols)]`:** Here, the **outer** comprehension iterates over each `col_idx`, and for each column, the **inner** comprehension builds a new row list `[row[col_idx] for row in matrix]`.
- **`sum(x * x for x in range(1, 6))`:** Passing a generator expression directly to `sum()`, `max()`, `min()`, `any()`, or `all()` computes the result in **`O(1)` auxiliary memory** without allocating an intermediate list!

---

## 8. Common Mistakes

1. **Putting `if-else` at the End of a List Comprehension (`SyntaxError`):**
   ```python
   # WRONG: Raises SyntaxError!
   res = [x for x in nums if x > 0 else 0]
   # CORRECT: Put ternary if-else BEFORE the `for` keyword:
   res = [x if x > 0 else 0 for x in nums]
   ```
2. **Reversing the Loop Order When Flattening a 2D List (`NameError`):**
   Writing `[cell for cell in row for row in matrix]` raises `NameError: name 'row' is not defined` because `for row in matrix` must come **first**!
3. **Using a List Comprehension Purely for Side Effects (`[print(x) for x in nums]`):**
   This is a serious anti-pattern because it allocates and discards a useless list `[None, None, None, ...]`. Always use a normal `for x in nums: print(x)` loop for side effects.

---

## 9. Practice Questions

1. **Easy:** Use a list comprehension to extract all words from a sentence that start with a vowel (`a, e, i, o, u`, case-insensitive) and have length `>= 4`.
2. **Medium:** Use a single list comprehension with the Walrus operator (`:=`) to call `compute(x) = x * x - 1` on `range(1, 10)` only once per element and keep only results that are divisible by `3`.
3. **Hard:** Given two matrices `A` (`M x K`) and `B` (`K x N`), write a nested list comprehension that computes their matrix product `C = A * B` (`M x N`).

---

## 10. Interview Questions

### Q1: Why is `[x * 2 for x in range(1000)]` faster than a `for` loop calling `result.append(x * 2)`?
**Answer:** In a standard `for` loop, every iteration executes `LOAD_ATTR (append)` and `CALL` to invoke the Python method object. A list comprehension compiles directly to the specialized **`LIST_APPEND`** CPython bytecode instruction, bypassing method lookup and function call overhead on every element.

### Q2: Does the loop variable `x` inside `[x for x in range(5)]` leak into the surrounding scope in Python 3?
**Answer:** **No.** In Python 2, list comprehension loop variables leaked into the enclosing scope. In Python 3, comprehensions have their **own isolated local scope** (except for assignment expressions using the Walrus operator `:=`, which intentionally bind in the enclosing scope).

### Q3: When should you choose a Generator Expression `(x for x in ...)` over a List Comprehension `[x for x in ...]`?
**Answer:** Choose a **Generator Expression** whenever you only need to iterate over the results **once** (for example, inside `sum()`, `any()`, `all()`, `max()`, or streaming large files) so that memory usage stays **`O(1)`**. Choose a **List Comprehension** when you need to index, slice, sort, `len()`, or iterate over the results multiple times.
