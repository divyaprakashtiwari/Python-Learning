# Topic 05: Dictionaries

---

## 1. Introduction

A **Dictionary (`dict`)** in Python is a mutable collection of **`key: value`** pairs enclosed in curly braces (`{"name": "Divya", "score": 95}`).

Under the hood, a Python `dict` is a high-performance **Hash Table** (also called a **Hash Map** or **Associative Array**):
- Keys must be **unique** and **hashable** (`str`, `int`, `float`, `bool`, `tuple` of immutables, `frozenset`).
- Values can be of **any data type** (mutable or immutable) and can repeat.
- Since **Python 3.7+**, dictionaries are officially guaranteed to **preserve insertion order**!
- Looking up `d[key]`, inserting `d[key] = val`, and deleting `del d[key]` all run in **`O(1)` average time**.

---

## 2. Why is it used?

Dictionaries are arguably the #1 most important data structure in both backend development and coding interviews:
1. **JSON & API Payloads:** Every JSON object parsed in Python maps directly to a `dict`.
2. **Frequency Counting & Caching:** Counting occurrences of elements or memoizing recursive subproblem states in `O(1)` time.
3. **Trading Space for Time in DSA:** Turning `O(n^2)` nested-loop searches (like Two Sum, Subarray Sum Equals `K`, or Group Anagrams) into **`O(n)` single-pass algorithms**.

---

## 3. Syntax

```python
# 1. Creation
user = {"id": 101, "name": "Divya"}
empty_dict = {}

# 2. Safe Lookup vs Direct Lookup
name = user["name"]                    # Raises KeyError if missing
role = user.get("role", "Student")     # Returns 'Student' if missing (No error!)

# 3. Insertion, Update & Removal
user["email"] = "divya@example.com"    # Insert or overwrite
removed_val = user.pop("email", None)  # Safe removal with default

# 4. Merging Dictionaries (Python 3.9+)
merged = defaults_dict | overrides_dict
defaults_dict |= overrides_dict        # In-place merge

# 5. Iteration Over Dynamic Views
for key, val in user.items():
    print(key, val)
```

---

## 4. Explanation (How CPython Compact Dictionaries Work)

1. **Hashing & Open Addressing:**
   - When you store `d["id"] = 101`, Python computes `hash("id")` and masks the bits to pick a slot in an internal index table.
   - If two distinct keys land on the same slot (**Hash Collision**), Python probes subsequent slots deterministically until an empty slot is found (**Open Addressing**).
2. **Why Python 3.6+ Dictionaries Are Compact & Ordered:**
   - Modern CPython splits the hash table into a tiny **sparse array of indices** and a **dense array of `(hash, key, value)` entries** appended in insertion order. This reduced dictionary memory usage by ~25% and made iteration preserve insertion order automatically!

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_dict_crud_get_and_views.py`](example_01_dict_crud_get_and_views.py)
- [`example_02_frequency_counter_and_grouping.py`](example_02_frequency_counter_and_grouping.py)
- [`example_03_two_sum_and_anagram_bucketing.py`](example_03_two_sum_and_anagram_bucketing.py)

### Example 1: Dictionary CRUD, Safe `.get()`, Views, and Merge (`|`) (`example_01_dict_crud_get_and_views.py`)

```python
def main() -> None:
    profile: dict[str, str | int] = {
        "username": "divya_tiwari",
        "role": "Learner",
        "streak_days": 15,
    }

    print("=== 1. Safe Lookup (.get) vs Direct Indexing ([]) ===")
    print(f"Username          : {profile['username']}")
    print(f"Missing key (.get): {profile.get('github_stars', 0)} (No KeyError!)")

    print("\n=== 2. Updating, Popping, and Merging (`|`) ===")
    profile["streak_days"] = 16
    extra_settings = {"role": "Contributor", "theme": "dark"}
    merged_profile = profile | extra_settings  # Right-hand values win on key collisions
    removed_theme = merged_profile.pop("theme", "default")
    print(f"Merged Profile    : {merged_profile}")
    print(f"Popped Theme      : {removed_theme!r}")

    print("\n=== 3. Iterating Over .keys(), .values(), and .items() ===")
    for key, value in merged_profile.items():
        print(f"  {key:<12} -> {value}")


if __name__ == "__main__":
    main()
```

### Example 2: Frequency Counting (`d.get`) and Grouping (`d.setdefault`) (`example_02_frequency_counter_and_grouping.py`)

```python
def count_word_frequencies(sentence: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in sentence.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def group_students_by_department(records: list[tuple[str, str]]) -> dict[str, list[str]]:
    departments: dict[str, list[str]] = {}
    for student_name, dept in records:
        departments.setdefault(dept, []).append(student_name)
    return departments


def main() -> None:
    text = "python dsa python backend dsa python"
    print("=== 1. Word Frequency Counter ===")
    freq = count_word_frequencies(text)
    print(f"Frequencies : {freq}")

    print("\n=== 2. Grouping Students by Department (.setdefault) ===")
    enrollments = [
        ("Divya", "CSE"),
        ("Aarav", "ECE"),
        ("Rohan", "CSE"),
        ("Sneha", "IT"),
        ("Kabir", "ECE"),
    ]
    grouped = group_students_by_department(enrollments)
    for dept, students in grouped.items():
        print(f"  {dept:<4} -> {students}")


if __name__ == "__main__":
    main()
```

### Example 3: Two Sum (Returning Indices) & Group Anagrams (`example_03_two_sum_and_anagram_bucketing.py`)

```python
def two_sum_indices(nums: list[int], target: int) -> tuple[int, int] | None:
    """Return indices of the two numbers that add up to `target` in O(n) time."""
    seen_index: dict[int, int] = {}
    for idx, value in enumerate(nums):
        complement = target - value
        if complement in seen_index:
            return (seen_index[complement], idx)
        seen_index[value] = idx
    return None


def group_anagrams(words: list[str]) -> list[list[str]]:
    """Group words that are anagrams of each other using a tuple key."""
    buckets: dict[tuple[str, ...], list[str]] = {}
    for word in words:
        signature = tuple(sorted(word))
        buckets.setdefault(signature, []).append(word)
    return list(buckets.values())


def main() -> None:
    print("=== 1. Two Sum (Returning Indices in O(n) Time) ===")
    nums = [2, 11, 7, 15]
    target = 9
    indices = two_sum_indices(nums, target)
    print(f"Array: {nums}, Target: {target} -> Indices: {indices}")

    print("\n=== 2. Group Anagrams ===")
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    grouped = group_anagrams(words)
    for group in grouped:
        print(f"  Anagram Group: {group}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== 1. Safe Lookup (.get) vs Direct Indexing ([]) ===
Username          : divya_tiwari
Missing key (.get): 0 (No KeyError!)

=== 2. Updating, Popping, and Merging (`|`) ===
Merged Profile    : {'username': 'divya_tiwari', 'role': 'Contributor', 'streak_days': 16}
Popped Theme      : 'dark'

=== 3. Iterating Over .keys(), .values(), and .items() ===
  username     -> divya_tiwari
  role         -> Contributor
  streak_days  -> 16
```

### Output for Example 2:
```text
=== 1. Word Frequency Counter ===
Frequencies : {'python': 3, 'dsa': 2, 'backend': 1}

=== 2. Grouping Students by Department (.setdefault) ===
  CSE  -> ['Divya', 'Rohan']
  ECE  -> ['Aarav', 'Kabir']
  IT   -> ['Sneha']
```

### Output for Example 3:
```text
=== 1. Two Sum (Returning Indices in O(n) Time) ===
Array: [2, 11, 7, 15], Target: 9 -> Indices: (0, 2)

=== 2. Group Anagrams ===
  Anagram Group: ['eat', 'tea', 'ate']
  Anagram Group: ['tan', 'nat']
  Anagram Group: ['bat']
```

---

## 7. Code Explanation

- **`counts[word] = counts.get(word, 0) + 1`:** Looks up the current count of `word` (returning `0` if `word` has not been seen yet), adds `1`, and writes the updated count back in a single clean line.
- **`departments.setdefault(dept, []).append(student_name)`:** If `dept` is not yet in `departments`, `.setdefault(dept, [])` inserts `dept: []` and returns that list so `.append(student_name)` works immediately.
- **`signature = tuple(sorted(word))`:** Sorting `"eat"`, `"tea"`, and `"ate"` produces `['a', 'e', 't']`. Because lists are unhashable, converting it to the tuple `('a', 'e', 't')` makes it a valid `dict` key!

---

## 8. Common Mistakes

1. **Checking `if k in d.keys():` or Searching Values Instead of Keys:**
   - `if k in d:` is already an `O(1)` key lookup; writing `d.keys()` is redundant.
   - However, `if v in d.values():` is **`O(n)`** because values are not hashed!
2. **Adding or Deleting Keys While Iterating Over a Dictionary (`RuntimeError`):**
   ```python
   # WRONG: Raises RuntimeError: dictionary changed size during iteration!
   for k, v in scores.items():
       if v < 40:
           del scores[k]
   # CORRECT: Iterate over a static list of keys `list(scores.keys())` or build a dict comprehension
   for k in list(scores.keys()):
       if scores[k] < 40:
           del scores[k]
   ```
3. **`dict.fromkeys(keys, [])` Shared List Trap:**
   `dict.fromkeys(["a", "b"], [])` assigns the **exact same list object** to both `"a"` and `"b"`! Instead, use `{k: [] for k in ["a", "b"]}`.

---

## 9. Practice Questions

1. **Easy:** Write a function `invert_unique_dict(d: dict[str, int]) -> dict[int, str]` that swaps keys and values when all values are unique, and write a second version `invert_grouping_dict(d: dict[str, int]) -> dict[int, list[str]]` that handles duplicate values by grouping keys into lists.
2. **Medium:** Write a function `first_non_repeating_char(s: str) -> str | None` that finds the first character in a string with frequency `1` in `O(n)` time using a dictionary.
3. **Hard:** Write a function `subarray_sum_equals_k(nums: list[int], k: int) -> int` (LeetCode 560) that counts how many contiguous subarrays sum to `k` in **`O(n)` time** using a running `prefix_sum` and a dictionary storing frequencies of previous prefix sums (`prefix_counts = {0: 1}`).

---

## 10. Interview Questions

### Q1: What happens in `{1: "int", True: "bool", 1.0: "float"}`?
**Answer:** It evaluates to **`{1: 'float'}`**! Because `1 == True == 1.0` and `hash(1) == hash(True) == hash(1.0)`, Python treats all three as the **same key**:
- First, key `1` is inserted with value `"int"`.
- Subsequent assignments for `True` and `1.0` keep the original key `1` (keys are not replaced on collision match), but **overwrite its value** to `"bool"` and then `"float"`.

### Q2: Are Python dictionaries ordered?
**Answer:** Yes! Starting in CPython 3.6 (as an implementation detail) and officially guaranteed across the Python language specification since **Python 3.7**, dictionaries preserve **key insertion order**. Updating an existing key's value does not change its position; deleting and re-inserting a key moves it to the end.

### Q3: What is the worst-case time complexity of dictionary lookup in Python, and why is it almost never hit in practice?
**Answer:** In the theoretical worst case where all $N$ keys collide into the same hash bucket, lookup degrades to `O(N)`. However, since Python 3.3 (PEP 456), Python randomizes its string/bytes hash seed (**SipHash**) on every interpreter startup to prevent hash-collision Denial-of-Service (DoS) attacks, guaranteeing **`O(1)` amortized time** in practice.
