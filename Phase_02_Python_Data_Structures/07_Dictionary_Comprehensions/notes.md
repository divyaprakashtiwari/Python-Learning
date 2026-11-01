# Topic 07: Dictionary Comprehensions

---

## 1. Introduction

A **Dictionary Comprehension** (introduced in PEP 274) is a concise, expressive syntax for constructing a new dictionary from any iterable by specifying both a **key expression** and a **value expression** separated by a colon (`{key_expr: value_expr for item in iterable if condition}`).

Just as List Comprehensions replace `for` + `.append()` loops using `LIST_APPEND`, Dictionary Comprehensions replace `for` + `d[k] = v` loops using CPython's specialized **`MAP_ADD`** bytecode instruction!

---

## 2. Why is it used?

1. **Fast `O(1)` Index Lookup Tables in DSA:** Precomputing `{val: idx for idx, val in enumerate(arr)}` lets algorithms (such as reconstructing a Binary Tree from Preorder + Inorder traversals) find the index of any element in **`O(1)` time** instead of calling `arr.index(val)` (`O(n)`).
2. **Inverting Mappings:** Swapping keys and values (`{v: k for k, v in d.items()}`) in one line.
3. **Filtering & Sanitizing JSON/Config Objects:** Stripping whitespace from keys, dropping `None` values, or applying bulk transformations to dictionary values.

---

## 3. Syntax

```python
# 1. Basic Dict Comprehension
squares_map = {x: x * x for x in range(1, 6)}

# 2. From Existing Dict with Filter (`if` at the end)
passed = {name: score for name, score in scores.items() if score >= 50}

# 3. With Ternary Value Transformation (`if-else` in value_expr)
status_map = {name: ("Pass" if score >= 50 else "Fail") for name, score in scores.items()}

# 4. Inverting Key-Value Pairs
inverted = {val: key for key, val in original_dict.items()}
```

---

## 4. Explanation (How Dictionary Comprehensions Execute)

1. **Syntax Distinguisher (`:` Colon):**
   - `{x * x for x in nums}` (no colon) -> creates a **`set`**.
   - `{x: x * x for x in nums}` (with colon `key: value`) -> creates a **`dict`**.
2. **Duplicate Keys Overwrite Earlier Keys:**
   - If the `key_expr` evaluates to the same key multiple times during the comprehension, the **last evaluated value wins** (just like repeated `d[k] = v` assignments in a loop).
3. **Initializing Independent Mutable Values (`{k: [] for k in keys}`):**
   - Unlike `dict.fromkeys(keys, [])` (which shares a single list across all keys), `{k: [] for k in keys}` evaluates `[]` freshly on every iteration, giving each key its own independent list!

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_basic_dict_comprehensions_and_zip.py`](example_01_basic_dict_comprehensions_and_zip.py)
- [`example_02_filtering_and_transforming_dicts.py`](example_02_filtering_and_transforming_dicts.py)
- [`example_03_inverting_and_nested_dict_comprehensions.py`](example_03_inverting_and_nested_dict_comprehensions.py)

### Example 1: Building Dictionaries from Iterables, `zip()`, and `enumerate()` (`example_01_basic_dict_comprehensions_and_zip.py`)

```python
def main() -> None:
    cubes = {n: n ** 3 for n in range(1, 6)}
    print("=== 1. Number to Cube Mapping ===")
    print(f"Cubes Dict : {cubes}")

    headers = ["id", "name", "track"]
    row_values = [101, "Divya Prakash", "Python + DSA"]
    record_dict = {col: val for col, val in zip(headers, row_values)}
    print("\n=== 2. Pairing Lists via zip() ===")
    print(f"Row Record : {record_dict}")

    sorted_primes = [2, 3, 5, 7, 11, 13, 17]
    prime_to_index = {prime: idx for idx, prime in enumerate(sorted_primes)}
    print("\n=== 3. Value-to-Index Lookup Table ===")
    print(f"Lookup Table      : {prime_to_index}")
    print(f"Index of prime 13 : {prime_to_index[13]}")


if __name__ == "__main__":
    main()
```

### Example 2: Filtering, Discount Transformation, and Key Normalization (`example_02_filtering_and_transforming_dicts.py`)

```python
def main() -> None:
    product_prices = {
        "Mechanical Keyboard": 3500.0,
        "USB-C Cable": 299.0,
        "27-Inch Monitor": 18500.0,
        "Mouse Pad": 199.0,
        "Laptop Stand": 1200.0,
    }

    premium_items = {
        item: price
        for item, price in product_prices.items()
        if price >= 1000.0
    }
    print("=== 1. Filtered Premium Products (>= Rs. 1000) ===")
    print(f"Premium Items : {premium_items}")

    discounted_catalog = {
        item: round(price * 0.85, 2) if price >= 1000.0 else round(price * 0.95, 2)
        for item, price in product_prices.items()
    }
    print("\n=== 2. Tiered Discount Catalog ===")
    for name, new_price in discounted_catalog.items():
        print(f"  {name:<21} : Rs.{new_price:>8.2f}")

    raw_headers = {"  Content-Type ": "application/json", "X-Request-ID": "req-99"}
    normalized_headers = {k.strip().lower(): v for k, v in raw_headers.items()}
    print("\n=== 3. Normalized HTTP Headers ===")
    print(f"Normalized : {normalized_headers}")


if __name__ == "__main__":
    main()
```

### Example 3: Inverting Dictionaries and Nested Dict Comprehensions (`example_03_inverting_and_nested_dict_comprehensions.py`)

```python
def main() -> None:
    country_to_capital = {
        "India": "New Delhi",
        "Japan": "Tokyo",
        "France": "Paris",
    }
    capital_to_country = {capital: country for country, capital in country_to_capital.items()}
    print("=== 1. Inverted 1-to-1 Dictionary ===")
    print(f"Capital -> Country : {capital_to_country}")

    user_scores = {"Aarav": 90, "Divya": 95, "Rohan": 90}
    score_to_last_user = {score: user for user, score in user_scores.items()}
    print("\n=== 2. Collision Behavior When Inverting Non-Unique Values ===")
    print(f"Original           : {user_scores}")
    print(f"Inverted (90 overwritten by 'Rohan'): {score_to_last_user}")

    mult_table = {
        r: {c: r * c for c in range(1, 4)}
        for r in range(1, 4)
    }
    print("\n=== 3. Nested Dict Comprehension (3x3 Table) ===")
    for row_key, inner_dict in mult_table.items():
        print(f"  Row {row_key} -> {inner_dict}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== 1. Number to Cube Mapping ===
Cubes Dict : {1: 1, 2: 8, 3: 27, 4: 64, 5: 125}

=== 2. Pairing Lists via zip() ===
Row Record : {'id': 101, 'name': 'Divya Prakash', 'track': 'Python + DSA'}

=== 3. Value-to-Index Lookup Table ===
Lookup Table      : {2: 0, 3: 1, 5: 2, 7: 3, 11: 4, 13: 5, 17: 6}
Index of prime 13 : 5
```

### Output for Example 2:
```text
=== 1. Filtered Premium Products (>= Rs. 1000) ===
Premium Items : {'Mechanical Keyboard': 3500.0, '27-Inch Monitor': 18500.0, 'Laptop Stand': 1200.0}

=== 2. Tiered Discount Catalog ===
  Mechanical Keyboard   : Rs. 2975.00
  USB-C Cable           : Rs.  284.05
  27-Inch Monitor       : Rs.15725.00
  Mouse Pad             : Rs.  189.05
  Laptop Stand          : Rs. 1020.00

=== 3. Normalized HTTP Headers ===
Normalized : {'content-type': 'application/json', 'x-request-id': 'req-99'}
```

### Output for Example 3:
```text
=== 1. Inverted 1-to-1 Dictionary ===
Capital -> Country : {'New Delhi': 'India', 'Tokyo': 'Japan', 'Paris': 'France'}

=== 2. Collision Behavior When Inverting Non-Unique Values ===
Original           : {'Aarav': 90, 'Divya': 95, 'Rohan': 90}
Inverted (90 overwritten by 'Rohan'): {90: 'Rohan', 95: 'Divya'}

=== 3. Nested Dict Comprehension (3x3 Table) ===
  Row 1 -> {1: 1, 2: 2, 3: 3}
  Row 2 -> {1: 2, 2: 4, 3: 6}
  Row 3 -> {1: 3, 2: 6, 3: 9}
```

---

## 7. Code Explanation

- **`{prime: idx for idx, prime in enumerate(sorted_primes)}`:** `enumerate()` yields `(idx, prime)`, and our dictionary comprehension flips them to `prime: idx` so we can query any prime's index in `O(1)` time.
- **`{k.strip().lower(): v for k, v in raw_headers.items()}`:** Iterates over key-value pairs using `.items()` and normalizes every key while keeping the values intact.
- **`{r: {c: r * c for c in range(1, 4)} for r in range(1, 4)}`:** The value expression itself is another dictionary comprehension, producing a 2-level nested dictionary `mult_table[r][c]`.

---

## 8. Common Mistakes

1. **Forgetting `.items()` When Iterating Over an Existing Dictionary:**
   ```python
   # WRONG: Iterating over `d` directly only yields keys, raising ValueError: too many values to unpack!
   filtered = {k: v for k, v in d if v > 10}
   # CORRECT: Always call `.items()`
   filtered = {k: v for k, v in d.items() if v > 10}
   ```
2. **Inverting a Dictionary Whose Values Are Mutable Lists (`TypeError`):**
   If `d = {"CSE": ["Divya", "Rohan"]}`, writing `{v: k for k, v in d.items()}` raises `TypeError: unhashable type: 'list'` because lists cannot be dictionary keys!
3. **Silent Data Loss When Inverting Non-Unique Values:**
   As shown in Example 3, if two keys share the same value (`"Aarav": 90` and `"Rohan": 90`), `{v: k for k, v in d.items()}` overwrites `"Aarav"` with `"Rohan"`.

---

## 9. Practice Questions

1. **Easy:** Given a string `s = "programming"`, use a dictionary comprehension to map each unique character to its ASCII code (`ord(ch)`).
2. **Medium:** Given a dictionary of API response fields `payload = {"id": 10, "name": "Divya", "bio": None, "avatar": "", "active": False}`, write a dictionary comprehension that removes keys whose values are `None` or `""` **without** accidentally removing `"active": False` or `0`!
3. **Hard:** Given an adjacency matrix `adj_matrix` (`N x N` list of `0`s and `1`s), use a dictionary comprehension to convert it into an **Adjacency List** dictionary `{node: [neighbor for neighbor, edge in enumerate(row) if edge == 1] for node, row in enumerate(adj_matrix)}`.

---

## 10. Interview Questions

### Q1: Why is `{k: [] for k in keys}` much safer than `dict.fromkeys(keys, [])`?
**Answer:** `dict.fromkeys(keys, [])` evaluates its second argument `[]` **only once** before the method runs, binding every key in the dictionary to the **exact same list reference** in memory (appending to `d["a"]` mutates `d["b"]`). In contrast, `{k: [] for k in keys}` evaluates the value expression `[]` on **each iteration**, creating a brand-new list for every key.

### Q2: When is `dict(zip(keys, values))` preferred over `{k: v for k, v in zip(keys, values)}`?
**Answer:** When you do not need to transform or filter the keys or values, `dict(zip(keys, values))` is cleaner and runs entirely inside C code without per-item Python bytecode evaluation. Use a dictionary comprehension when you need an `if` filter or an expression like `{k.lower(): v * 2 for k, v in zip(keys, values)}`.

### Q3: How do you safely filter out `None` values from a dictionary without dropping legitimate falsy values like `0`, `False`, or `[]`?
**Answer:** Use identity comparison `if v is not None` instead of truthiness `if v`:
`clean_dict = {k: v for k, v in raw_dict.items() if v is not None}`.
