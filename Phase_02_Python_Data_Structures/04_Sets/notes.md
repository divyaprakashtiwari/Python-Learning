# Topic 04: Sets

---

## 1. Introduction

A **Set (`set`)** in Python is an **unordered**, **mutable** collection of **unique, hashable** elements enclosed in curly braces (`{"Python", "SQL", "Git"}`) or constructed via `set()`.

Under the hood, a Python `set` is implemented as a **Hash Table** (just like a `dict`, but storing only keys without values). Because it uses hashing:
- Checking if an item exists (`x in my_set`), inserting an item (`my_set.add(x)`), and deleting an item (`my_set.discard(x)`) all run in **`O(1)` average time**!
- Duplicate elements are automatically eliminated.
- Because sets are unordered, they do **not** support indexing or slicing (`my_set[0]` raises `TypeError`).

---

## 2. Why is it used?

1. **Instant `O(1)` Membership Lookups:** Replacing `if user_id in banned_list:` (`O(n)`) with `if user_id in banned_set:` (`O(1)`) turns an `O(n^2)` loop into a blazing-fast `O(n)` algorithm.
2. **Visited Tracking in Graph & Grid DSA:** Every BFS and DFS algorithm uses `visited: set[tuple[int, int]] = set()` to prevent infinite cycles in `O(1)` time per node.
3. **Relational & Set-Theory Analytics:** Finding common users between two products (`A & B`), churned users (`A - B`), or combined unique visitors (`A | B`).

---

## 3. Syntax

```python
# 1. Creation (CRITICAL: {} creates an empty dict, NOT a set!)
empty_set = set()
tags = {"dsa", "python", "backend"}

# 2. Mutation
tags.add("sql")           # Add a single element -> O(1)
tags.update(["aws", "go"]) # Add multiple elements from an iterable
tags.discard("missing")   # Safe removal: does NOT raise an error if missing
tags.remove("go")         # Strict removal: raises KeyError if missing

# 3. Set Theory Operators
union_set = A | B          # Elements in A or B (or both)
inter_set = A & B          # Elements common to both A and B
diff_set  = A - B          # Elements in A but NOT in B
sym_diff  = A ^ B          # Elements in A or B, but NOT both

# 4. Immutable Set (Hashable!)
immutable_group = frozenset([1, 2, 3])
```

---

## 4. Explanation (How Hashing & Set Operations Work)

| Operation | Operator | Method Equivalent | Average Time Complexity |
| :--- | :--- | :--- | :--- |
| Membership check | `x in A` | — | `O(1)` |
| Add / Remove / Discard | — | `A.add(x)`, `A.remove(x)`, `A.discard(x)` | `O(1)` |
| Union | `A \| B` | `A.union(B)` | `O(len(A) + len(B))` |
| Intersection | `A & B` | `A.intersection(B)` | `O(min(len(A), len(B)))` |
| Difference | `A - B` | `A.difference(B)` | `O(len(A))` |
| Symmetric Difference | `A ^ B` | `A.symmetric_difference(B)` | `O(len(A) + len(B))` |
| Subset / Superset | `A <= B`, `A >= B` | `A.issubset(B)`, `A.issuperset(B)` | `O(len(A))` / `O(len(B))` |

> **Important Nuance (Operator vs Method):**
> Binary operators like `A | B` require **both** operands to be sets, whereas methods like `A.union([1, 2, 3])` accept **any iterable** as their argument!

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_set_crud_and_deduplication.py`](example_01_set_crud_and_deduplication.py)
- [`example_02_mathematical_set_operations.py`](example_02_mathematical_set_operations.py)
- [`example_03_frozenset_and_two_sum_lookup.py`](example_03_frozenset_and_two_sum_lookup.py)

### Example 1: Set Creation, `remove` vs `discard`, and `{1, True, 1.0}` (`example_01_set_crud_and_deduplication.py`)

```python
def main() -> None:
    print("=== 1. Creating Sets (Empty Set Must Use set()) ===")
    empty_dict = {}
    empty_set = set()
    print(f"{{}}     -> type: {type(empty_dict).__name__}")
    print(f"set()  -> type: {type(empty_set).__name__}")

    print("\n=== 2. Adding & Removing: add(), update(), discard(), remove() ===")
    skills = {"Python", "Git"}
    skills.add("SQL")
    skills.update(["Docker", "Python", "AWS"])  # Duplicate 'Python' ignored automatically
    skills.discard("Java")                      # No error if 'Java' is missing!
    skills.remove("Git")                        # Removes 'Git' (raises KeyError if missing)
    print(f"Current Skills (sorted for display): {sorted(skills)}")
    print(f"'Docker' in skills (O(1) lookup)   : {'Docker' in skills}")

    print("\n=== 3. The Classic Interview Puzzle: {1, True, 1.0} ===")
    puzzle_set = {1, True, 1.0}
    print(f"{{1, True, 1.0}} -> {puzzle_set} (Length: {len(puzzle_set)})")
    print(f"Why? 1 == True == 1.0 is {1 == True == 1.0} and hash(1) == hash(True) == hash(1.0)!")


if __name__ == "__main__":
    main()
```

### Example 2: Mathematical Set Theory Operations (`example_02_mathematical_set_operations.py`)

```python
def main() -> None:
    backend_team = {"Python", "SQL", "Docker", "Redis"}
    data_team = {"Python", "SQL", "Pandas", "Spark"}

    print("=== 1. Set Theory Operators ===")
    print(f"Backend Team              : {sorted(backend_team)}")
    print(f"Data Team                 : {sorted(data_team)}")
    print(f"Union (|)                 : {sorted(backend_team | data_team)}")
    print(f"Intersection (&)          : {sorted(backend_team & data_team)}")
    print(f"Difference (Backend - Data): {sorted(backend_team - data_team)}")
    print(f"Symmetric Diff (^)        : {sorted(backend_team ^ data_team)}")

    print("\n=== 2. Subset, Superset, and Disjoint Checks ===")
    core_requirements = {"Python", "SQL"}
    frontend_only = {"React", "TypeScript"}

    print(f"Are core_requirements a subset (<=) of backend_team? : {core_requirements <= backend_team}")
    print(f"Is backend_team a superset (>=) of core_requirements?: {backend_team >= core_requirements}")
    print(f"Are backend_team and frontend_only disjoint?         : {backend_team.isdisjoint(frontend_only)}")


if __name__ == "__main__":
    main()
```

### Example 3: `frozenset` as Dict Keys & `O(n)` Pair-Sum Detection (`example_03_frozenset_and_two_sum_lookup.py`)

```python
def has_pair_with_sum(nums: list[int], target: int) -> tuple[bool, tuple[int, int] | None]:
    """Return True and the pair if any two numbers in `nums` sum to `target` in O(n) time."""
    seen: set[int] = set()
    for num in nums:
        complement = target - num
        if complement in seen:
            return (True, (complement, num))
        seen.add(num)
    return (False, None)


def main() -> None:
    print("=== 1. Undirected Flight Routes using frozenset Keys ===")
    flight_fares: dict[frozenset[str], int] = {
        frozenset({"DEL", "BLR"}): 5400,
        frozenset({"BOM", "HYD"}): 3800,
    }
    route_query = frozenset({"BLR", "DEL"})
    print(f"Fare for BLR <-> DEL : Rs.{flight_fares[route_query]}")

    print("\n=== 2. O(n) Pair-Sum Existence Check Using a Set ===")
    prices = [120, 450, 300, 80, 620]
    for target_sum in [530, 999]:
        found, pair = has_pair_with_sum(prices, target_sum)
        print(f"  Target={target_sum} -> Found: {found}, Pair: {pair}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== 1. Creating Sets (Empty Set Must Use set()) ===
{}     -> type: dict
set()  -> type: set

=== 2. Adding & Removing: add(), update(), discard(), remove() ===
Current Skills (sorted for display): ['AWS', 'Docker', 'Python', 'SQL']
'Docker' in skills (O(1) lookup)   : True

=== 3. The Classic Interview Puzzle: {1, True, 1.0} ===
{1, True, 1.0} -> {1} (Length: 1)
Why? 1 == True == 1.0 is True and hash(1) == hash(True) == hash(1.0)!
```

### Output for Example 2:
```text
=== 1. Set Theory Operators ===
Backend Team              : ['Docker', 'Python', 'Redis', 'SQL']
Data Team                 : ['Pandas', 'Python', 'SQL', 'Spark']
Union (|)                 : ['Docker', 'Pandas', 'Python', 'Redis', 'SQL', 'Spark']
Intersection (&)          : ['Python', 'SQL']
Difference (Backend - Data): ['Docker', 'Redis']
Symmetric Diff (^)        : ['Docker', 'Pandas', 'Redis', 'Spark']

=== 2. Subset, Superset, and Disjoint Checks ===
Are core_requirements a subset (<=) of backend_team? : True
Is backend_team a superset (>=) of core_requirements?: True
Are backend_team and frontend_only disjoint?         : True
```

### Output for Example 3:
```text
=== 1. Undirected Flight Routes using frozenset Keys ===
Fare for BLR <-> DEL : Rs.5400

=== 2. O(n) Pair-Sum Existence Check Using a Set ===
  Target=530 -> Found: True, Pair: (450, 80)
  Target=999 -> Found: False, Pair: None
```

---

## 7. Code Explanation

- **`{1, True, 1.0}` evaluates to `{1}`:** A set considers two objects duplicates if `a == b` and `hash(a) == hash(b)`. In Python, `1 == True == 1.0` is `True`, so only the first element inserted (`1`) is kept!
- **`backend_team & data_team`:** Computes the intersection by iterating over the **smaller** set and checking membership in the larger set in `O(min(len(A), len(B)))` time.
- **`frozenset({"DEL", "BLR"})`:** Because standard `set` is mutable, you cannot put a `set` inside another `set` or use it as a `dict` key. `frozenset` is immutable and hashable, making it ideal for representing unordered pairs or graph edges.

---

## 8. Common Mistakes

1. **Writing `s = {}` to Create an Empty Set:**
   `{}` is an empty `dict`! Calling `s.add(1)` on `s = {}` raises `AttributeError: 'dict' object has no attribute 'add'`. Always use `s = set()`.
2. **Adding Mutable Objects (`list`, `dict`, `set`) to a Set:**
   `s.add([1, 2])` raises `TypeError: unhashable type: 'list'`. Convert lists to tuples (`s.add((1, 2))`) or sets to `frozenset`.
3. **Using `s.add("abc")` vs `s.update("abc")`:**
   `s.add("abc")` inserts the single string `"abc"`, whereas `s.update("abc")` iterates over the string and inserts `'a'`, `'b'`, and `'c'` separately.

---

## 9. Practice Questions

1. **Easy:** Write a function `is_pangram(sentence: str) -> bool` using a `set` that returns `True` if `sentence` contains every English letter `'a'` through `'z'` at least once.
2. **Medium:** Given three lists of student roll numbers enrolled in `Math`, `Physics`, and `CS`, use set operators to find: (a) students enrolled in all 3 courses, and (b) students enrolled in **exactly one** course.
3. **Hard:** Write a function `longest_consecutive_sequence(nums: list[int]) -> int` (LeetCode 128) that finds the length of the longest consecutive elements sequence (e.g., `[100, 4, 200, 1, 3, 2] -> 4` for `1, 2, 3, 4`) in strictly **`O(n)` time** using a `set` (only starting a streak count at `x` if `x - 1 not in num_set`).

---

## 10. Interview Questions

### Q1: Why does `longest_consecutive_sequence` using a `set` run in `O(n)` time instead of `O(n log n)` sorting?
**Answer:** By converting `nums` to `num_set = set(nums)` (`O(n)`) and only starting an inner `while curr + 1 in num_set:` loop when `x - 1 not in num_set` (meaning `x` is the true start of a streak), each number is visited at most twice across the entire execution, achieving **`O(n)`** time.

### Q2: What is the difference between `set.remove(x)`, `set.discard(x)`, and `set.pop()`?
**Answer:**
- `remove(x)` deletes `x` and raises a `KeyError` if `x` is not present.
- `discard(x)` deletes `x` if present and does nothing (no error) if `x` is missing.
- `pop()` removes and returns an **arbitrary** element from the set (raising `KeyError` if the set is empty).

### Q3: Why can't a mutable `list` be hashed and stored inside a `set`?
**Answer:** Hash tables locate elements by their `hash(x)` bucket. If an element mutated after being inserted into a `set`, its hash value would change while it was still sitting in the old bucket, breaking the hash table invariant and making the element impossible to find!
