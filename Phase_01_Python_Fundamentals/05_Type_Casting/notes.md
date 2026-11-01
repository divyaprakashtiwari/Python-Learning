# Topic 05: Type Casting

---

## 1. Introduction

**Type Casting** (also called **Type Conversion**) is the process of converting a value from one data type into another—for example, converting the string `"42"` read from user input or a CSV file into the integer `42` so you can perform arithmetic with it.

Python supports two forms of type conversion:
1. **Implicit Type Casting (Coercion):** Python automatically converts a narrower numeric type (`int`) into a wider numeric type (`float`) to prevent data loss (`4 + 1.5 -> 5.5`).
2. **Explicit Type Casting:** You manually call constructor functions like `int()`, `float()`, `str()`, `bool()`, `list()`, `tuple()`, `set()`, or `dict()`.

---

## 2. Why is it used?

In real-world applications, data rarely arrives in the exact type your algorithm needs:
1. **User Input & CLI Arguments:** `input()` and environment variables always return `str`. You must cast them to `int` or `float` before doing math.
2. **Data Cleaning & Deduplication:** Converting a `list` to a `set` (`set(items)`) instantly removes duplicate records in `O(n)` time.
3. **JSON & API Serialization:** Numbers or tuples often need to be cast to `str` or `list` when formatting logs, URLs, or payloads.

---

## 3. Syntax

```python
# Numeric & String Conversions
num_int = int("250")            # "250" -> 250
num_from_bin = int("1011", 2)   # Binary string "1011" -> 11
num_float = float("99.95")      # "99.95" -> 99.95
text = str(2026)                # 2026 -> "2026"
flag = bool(1)                  # 1 -> True

# Collection Conversions
chars = list("abc")             # ['a', 'b', 'c']
unique = set([1, 2, 2, 3])      # {1, 2, 3}
frozen = tuple([10, 20])        # (10, 20)
mapping = dict([("a", 1)])      # {'a': 1}
```

---

## 4. Explanation (Step-by-Step Rules of Type Casting)

1. **Why Python Is Strongly Typed:** Unlike JavaScript (where `"5" + 3` silently becomes `"53"`), Python is **strongly typed**. Adding `"5" + 3` raises `TypeError: can only concatenate str (not "int") to str`. You must explicitly choose `int("5") + 3` (`8`) or `"5" + str(3)` (`"53"`).
2. **`int(float_value)` Truncates Toward Zero:** `int(9.99)` returns `9` and `int(-9.99)` returns `-9`. It strips the decimal portion without rounding.
3. **Truthiness (`bool(x)`):**
   - **Falsy (`False`):** `0`, `0.0`, `0j`, `""`, `[]`, `()`, `{}`, `set()`, `None`, `False`.
   - **Truthy (`True`):** Every other non-empty or non-zero object (including `"False"` and `"0"`, because they are non-empty strings!).

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_implicit_vs_explicit_casting.py`](example_01_implicit_vs_explicit_casting.py)
- [`example_02_truthiness_and_bool_casting.py`](example_02_truthiness_and_bool_casting.py)
- [`example_03_collection_type_conversions.py`](example_03_collection_type_conversions.py)

### Example 1: Implicit Coercion vs Explicit Type Casting (`example_01_implicit_vs_explicit_casting.py`)

```python
def main() -> None:
    items_count = 4          # int
    unit_weight_kg = 1.75    # float
    total_weight = items_count + unit_weight_kg  # int is widened to float
    print("=== 1. Implicit Type Casting ===")
    print(f"{items_count} (int) + {unit_weight_kg} (float) = {total_weight} ({type(total_weight).__name__})")

    raw_price_str = "1299.95"
    price_float = float(raw_price_str)
    truncated_int = int(price_float)   # Truncates toward zero (does NOT round)
    rounded_int = round(price_float)

    print("\n=== 2. Explicit Numeric & String Casting ===")
    print(f"String {raw_price_str!r} -> float : {price_float}")
    print(f"float {price_float} -> int()  : {truncated_int} (truncated toward zero)")
    print(f"float {price_float} -> round(): {rounded_int} (rounded to nearest integer)")

    binary_str = "11010"
    hex_str = "FF"
    print("\n=== 3. Base Conversion with int(str, base) ===")
    print(f"Binary {binary_str!r} (base 2)  -> int: {int(binary_str, 2)}")
    print(f"Hex    {hex_str!r} (base 16) -> int: {int(hex_str, 16)}")


if __name__ == "__main__":
    main()
```

### Example 2: Boolean Casting (`bool()`) — Truthy vs Falsy Values (`example_02_truthiness_and_bool_casting.py`)

```python
def main() -> None:
    falsy_values = [0, 0.0, 0j, "", [], (), {}, set(), None, False]
    truthy_values = [1, -5, 0.001, "False", "0", [0], (None,), {"k": 1}]

    print("=== 1. Falsy Values (bool(x) is Always False) ===")
    for val in falsy_values:
        print(f"  bool({val!r:<8}) -> {bool(val)}")

    print("\n=== 2. Truthy Values (bool(x) is Always True) ===")
    for val in truthy_values:
        print(f"  bool({val!r:<8}) -> {bool(val)}")


if __name__ == "__main__":
    main()
```

### Example 3: Casting Between Collections (`example_03_collection_type_conversions.py`)

```python
def main() -> None:
    word = "algorithm"
    char_list = list(word)
    rejoined_word = "".join(char_list)
    print("=== 1. String and List Conversion ===")
    print(f"list({word!r}) -> {char_list}")
    print(f"''.join(char_list) -> {rejoined_word!r}")

    raw_submissions = [104, 101, 102, 104, 101, 105]
    unique_sorted = sorted(set(raw_submissions))
    unique_order_preserved = list(dict.fromkeys(raw_submissions))

    print("\n=== 2. Deduplication via Collection Casting ===")
    print(f"Raw Submissions          : {raw_submissions}")
    print(f"Sorted Unique (via set)  : {unique_sorted}")
    print(f"Order-Preserved Unique   : {unique_order_preserved}")

    key_value_pairs = [("host", "localhost"), ("port", 8080), ("debug", True)]
    config_dict = dict(key_value_pairs)
    frozen_keys = tuple(config_dict.keys())
    print("\n=== 3. Pairs to Dict & Tuple ===")
    print(f"Config Dict : {config_dict}")
    print(f"Frozen Keys : {frozen_keys}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== 1. Implicit Type Casting ===
4 (int) + 1.75 (float) = 5.75 (float)

=== 2. Explicit Numeric & String Casting ===
String '1299.95' -> float : 1299.95
float 1299.95 -> int()  : 1299 (truncated toward zero)
float 1299.95 -> round(): 1300 (rounded to nearest integer)

=== 3. Base Conversion with int(str, base) ===
Binary '11010' (base 2)  -> int: 26
Hex    'FF' (base 16) -> int: 255
```

### Output for Example 2:
```text
=== 1. Falsy Values (bool(x) is Always False) ===
  bool(0       ) -> False
  bool(0.0     ) -> False
  bool(0j      ) -> False
  bool(''      ) -> False
  bool([]      ) -> False
  bool(()      ) -> False
  bool({}      ) -> False
  bool(set()   ) -> False
  bool(None    ) -> False
  bool(False   ) -> False

=== 2. Truthy Values (bool(x) is Always True) ===
  bool(1       ) -> True
  bool(-5      ) -> True
  bool(0.001   ) -> True
  bool('False' ) -> True
  bool('0'     ) -> True
  bool([0]     ) -> True
  bool((None,) ) -> True
  bool({'k': 1}) -> True
```

### Output for Example 3:
```text
=== 1. String and List Conversion ===
list('algorithm') -> ['a', 'l', 'g', 'o', 'r', 'i', 't', 'h', 'm']
''.join(char_list) -> 'algorithm'

=== 2. Deduplication via Collection Casting ===
Raw Submissions          : [104, 101, 102, 104, 101, 105]
Sorted Unique (via set)  : [101, 102, 104, 105]
Order-Preserved Unique   : [104, 101, 102, 105]

=== 3. Pairs to Dict & Tuple ===
Config Dict : {'host': 'localhost', 'port': 8080, 'debug': True}
Frozen Keys : ('host', 'port', 'debug')
```

---

## 7. Code Explanation

- **`int("1299.95")` vs `int(float("1299.95"))`** — Passing a decimal string directly to `int("1299.95")` raises `ValueError: invalid literal for int() with base 10: '1299.95'`. You must first convert it to a `float("1299.95")` and then wrap that in `int()`.
- **`int(binary_str, 2)`** — The second argument to `int()` specifies the numeral base (`2` to `36`).
- **`list(dict.fromkeys(raw_submissions))`** — Because Python dictionaries preserve insertion order (since Python 3.7) and reject duplicate keys, `list(dict.fromkeys(seq))` is the standard idiom to deduplicate a sequence while preserving the original order.

---

## 8. Common Mistakes

1. **Passing a Decimal String Directly to `int()`:**
   ```python
   # WRONG: Raises ValueError!
   val = int("45.67")
   # CORRECT:
   val = int(float("45.67"))
   ```
2. **Expecting `bool("False")` or `bool("0")` to be `False`:**
   Any non-empty string in Python is truthy (`bool("False") == True`). To parse a boolean from a configuration string, check `raw.strip().lower() in {"true", "1", "yes"}`.
3. **Using `str(char_list)` Instead of `"".join(char_list)`:**
   `str(['a', 'b'])` produces the literal string `"['a', 'b']"` (with brackets and quotes), whereas `"".join(['a', 'b'])` produces `"ab"`.

---

## 9. Practice Questions

1. **Easy:** Given `price_str = "499.75"` and `qty_str = "3"`, cast both strings to the appropriate numeric types and calculate the total cost as both a `float` and a truncated `int`.
2. **Medium:** Write a function `parse_boolean(text: str) -> bool` that safely converts strings like `"True"`, `"YES"`, `"1"`, `"false"`, `"No"`, `"0"` (case-insensitive, with extra spaces) into their proper Python `bool` value.
3. **Hard:** Given a list of binary strings `["101", "1111", "10000", "101", "1111"]`, convert all of them to base-10 integers, remove duplicates while preserving their original order of appearance, and return the result as an immutable `tuple`.

---

## 10. Interview Questions

### Q1: Why is Python described as both "Dynamically Typed" and "Strongly Typed"?
**Answer:**
- **Dynamically Typed:** Variable names are not bound to a static type at compile time; a variable can reference an `int` now and a `str` later.
- **Strongly Typed:** Objects themselves have strict types, and Python refuses to perform unsafe implicit conversions between incompatible types (e.g., `"10" + 5` raises a `TypeError` instead of silently coercing).

### Q2: What is the difference between `int(-3.7)` and `math.floor(-3.7)`?
**Answer:** `int(-3.7)` truncates **toward zero**, returning `-3`. `math.floor(-3.7)` rounds **down toward negative infinity** (the largest integer `<= -3.7`), returning `-4` (which is also how `//` floor division behaves).

### Q3: How can you remove duplicates from a list in `O(n)` time while preserving the original order?
**Answer:** Use `list(dict.fromkeys(items))`. Unlike `list(set(items))` (which loses the original ordering), `dict.fromkeys()` preserves first-seen insertion order in `O(n)` average time.
