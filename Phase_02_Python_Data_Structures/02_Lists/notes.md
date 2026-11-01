# Topic 02: Lists

---

## 1. Introduction

A **List (`list`)** in Python is an ordered, **mutable** collection of elements enclosed in square brackets (`[10, 20, 30]`). Under the hood, CPython implements a `list` not as a linked list, but as a **dynamic array of object references (pointers)**.

Because it is a dynamic array:
- Accessing or updating any index (`arr[i]`) takes **`O(1)` constant time**.
- Appending or popping at the **end** of the list (`arr.append(x)`, `arr.pop()`) takes **`O(1)` amortized time**.
- Inserting or deleting at the **front or middle** (`arr.insert(0, x)`, `arr.pop(0)`) takes **`O(n)` linear time** because all subsequent elements must shift in memory.

---

## 2. Why is it used?

Lists are Python's primary workhorse collection:
1. **Dynamic Datasets:** Storing API query results, shopping carts, or user feeds whose size grows and shrinks at runtime.
2. **Stack Implementation in DSA:** A standard Python `list` using `.append(x)` (push) and `.pop()` (pop) is the fastest way to implement a LIFO Stack in `O(1)` time.
3. **Sorting & Ranking:** Python's built-in **Timsort** (`.sort()` and `sorted()`) sorts lists in `O(n log n)` worst-case and `O(n)` best-case time on nearly sorted data.

---

## 3. Syntax

```python
# 1. Creation
nums = [10, 20, 30]
empty_list = []

# 2. Adding Elements
nums.append(40)           # [10, 20, 30, 40] -> O(1) amortized
nums.extend([50, 60])     # [10, 20, 30, 40, 50, 60] -> O(k)
nums.insert(0, 5)         # [5, 10, 20, 30, 40, 50, 60] -> O(n)

# 3. Removing Elements
last = nums.pop()         # Removes & returns 60 -> O(1)
first = nums.pop(0)       # Removes & returns 5  -> O(n)
nums.remove(30)           # Removes first occurrence of value 30 -> O(n)

# 4. Sorting & Copying
sorted_copy = sorted(nums, reverse=True)
nums.sort()               # In-place sort (returns None!)
clone = nums.copy()       # Shallow copy
```

---

## 4. Explanation (Time Complexity & Dynamic Array Over-Allocation)

| Operation | Python Code | Time Complexity | Why? |
| :--- | :--- | :--- | :--- |
| Index Lookup / Assignment | `arr[i]`, `arr[i] = v` | `O(1)` | Direct pointer arithmetic offset |
| Append to End | `arr.append(v)` | `O(1)` amortized | CPython over-allocates extra capacity |
| Pop from End | `arr.pop()` | `O(1)` | Decrements size counter |
| Insert / Pop at Index `i` | `arr.insert(i, v)`, `arr.pop(i)` | `O(n)` | Shifts `n - i` elements in memory |
| Search / Count / Remove by Value | `v in arr`, `arr.index(v)`, `arr.remove(v)` | `O(n)` | Scans elements sequentially |
| Sort | `arr.sort()`, `sorted(arr)` | `O(n log n)` | Hybrid Merge Sort + Insertion Sort (Timsort) |

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_list_crud_and_slicing.py`](example_01_list_crud_and_slicing.py)
- [`example_02_sorting_reversing_and_custom_keys.py`](example_02_sorting_reversing_and_custom_keys.py)
- [`example_03_aliasing_copying_and_2d_pitfall.py`](example_03_aliasing_copying_and_2d_pitfall.py)

### Example 1: List Creation, CRUD Operations, and Slice Assignment (`example_01_list_crud_and_slicing.py`)

```python
def main() -> None:
    tasks = ["Setup Git", "Learn Variables", "Master Loops"]
    print("=== 1. Adding Elements: append(), extend(), insert() ===")
    print(f"Initial Tasks      : {tasks}")

    tasks.append("Study Lists")                     # O(1) amortized
    tasks.extend(["Practice Tuples", "Build Sets"]) # O(k) where k is number of new items
    tasks.insert(1, "Configure IDE")                # O(n) shifts elements right
    print(f"After Additions    : {tasks}")

    print("\n=== 2. Removing Elements: pop() and remove() ===")
    last_task = tasks.pop()                         # O(1) removes & returns last item
    second_task = tasks.pop(1)                      # O(n) removes & returns index 1
    tasks.remove("Learn Variables")                 # O(n) removes first matching value
    print(f"Popped Last        : {last_task!r}")
    print(f"Popped Index 1     : {second_task!r}")
    print(f"Remaining Tasks    : {tasks}")

    print("\n=== 3. Slice Assignment (In-Place Replacement) ===")
    scores = [10, 20, 99, 99, 50]
    scores[2:4] = [30, 40]
    print(f"Fixed Scores       : {scores}")


if __name__ == "__main__":
    main()
```

### Example 2: Sorting (`sort()` vs `sorted()`) and Custom `key` Functions (`example_02_sorting_reversing_and_custom_keys.py`)

```python
def main() -> None:
    latencies_ms = [48, 12, 105, 19, 32]

    print("=== 1. sorted(list) vs list.sort() ===")
    ascending_copy = sorted(latencies_ms)
    print(f"Original (unchanged) : {latencies_ms}")
    print(f"sorted() new list    : {ascending_copy}")

    latencies_ms.sort(reverse=True)
    print(f"In-place .sort(desc) : {latencies_ms}")

    print("\n=== 2. Custom Key Sorting (Case-Insensitive & By Length) ===")
    words = ["banana", "Apple", "fig", "Cherry", "date"]
    print(f"Case-Insensitive     : {sorted(words, key=str.lower)}")
    print(f"By Word Length       : {sorted(words, key=len)}")

    print("\n=== 3. Multi-Criteria Sorting (Highest Score, then Alphabetical Name) ===")
    candidates = [
        ("Rohan", 88),
        ("Aarav", 95),
        ("Divya", 95),
        ("Sneha", 88),
    ]
    ranked = sorted(candidates, key=lambda item: (-item[1], item[0]))
    for rank, (name, score) in enumerate(ranked, start=1):
        print(f"  Rank #{rank}: {name:<6} (Score: {score})")


if __name__ == "__main__":
    main()
```

### Example 3: List Aliasing vs Copying and the 2D Grid Trap (`example_03_aliasing_copying_and_2d_pitfall.py`)

```python
def main() -> None:
    print("=== 1. Reference Aliasing (`b = a`) vs Shallow Copy (`a.copy()`) ===")
    original = [10, 20, 30]
    alias = original
    safe_copy = original.copy()

    alias.append(40)
    print(f"Original after alias.append(40) : {original}")
    print(f"Safe Copy (unaffected)          : {safe_copy}")

    print("\n=== 2. The Classic 2D Grid Trap: [[0] * 3] * 3 ===")
    buggy_grid = [[0] * 3] * 3
    buggy_grid[0][0] = 99
    print(f"Buggy Grid after setting [0][0]=99 (ALL rows mutated!):")
    for row in buggy_grid:
        print(f"  {row}")

    print("\n=== 3. Safe 2D Grid Initialization: [[0] * 3 for _ in range(3)] ===")
    safe_grid = [[0] * 3 for _ in range(3)]
    safe_grid[0][0] = 99
    print(f"Safe Grid after setting [0][0]=99 (Only row 0 mutated):")
    for row in safe_grid:
        print(f"  {row}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== 1. Adding Elements: append(), extend(), insert() ===
Initial Tasks      : ['Setup Git', 'Learn Variables', 'Master Loops']
After Additions    : ['Setup Git', 'Configure IDE', 'Learn Variables', 'Master Loops', 'Study Lists', 'Practice Tuples', 'Build Sets']

=== 2. Removing Elements: pop() and remove() ===
Popped Last        : 'Build Sets'
Popped Index 1     : 'Configure IDE'
Remaining Tasks    : ['Setup Git', 'Master Loops', 'Study Lists', 'Practice Tuples']

=== 3. Slice Assignment (In-Place Replacement) ===
Fixed Scores       : [10, 20, 30, 40, 50]
```

### Output for Example 2:
```text
=== 1. sorted(list) vs list.sort() ===
Original (unchanged) : [48, 12, 105, 19, 32]
sorted() new list    : [12, 19, 32, 48, 105]
In-place .sort(desc) : [105, 48, 32, 19, 12]

=== 2. Custom Key Sorting (Case-Insensitive & By Length) ===")
Case-Insensitive     : ['Apple', 'banana', 'Cherry', 'date', 'fig']
By Word Length       : ['fig', 'date', 'Apple', 'banana', 'Cherry']

=== 3. Multi-Criteria Sorting (Highest Score, then Alphabetical Name) ===
  Rank #1: Aarav  (Score: 95)
  Rank #2: Divya  (Score: 95)
  Rank #3: Rohan  (Score: 88)
  Rank #4: Sneha  (Score: 88)
```

### Output for Example 3:
```text
=== 1. Reference Aliasing (`b = a`) vs Shallow Copy (`a.copy()`) ===
Original after alias.append(40) : [10, 20, 30, 40]
Safe Copy (unaffected)          : [10, 20, 30]

=== 2. The Classic 2D Grid Trap: [[0] * 3] * 3 ===
Buggy Grid after setting [0][0]=99 (ALL rows mutated!):
  [99, 0, 0]
  [99, 0, 0]
  [99, 0, 0]

=== 3. Safe 2D Grid Initialization: [[0] * 3 for _ in range(3)] ===
Safe Grid after setting [0][0]=99 (Only row 0 mutated):
  [99, 0, 0]
  [0, 0, 0]
  [0, 0, 0]
```

---

## 7. Code Explanation

- **`append(x)` vs `extend(iterable)`:** `[1, 2].append([3, 4])` nests the list as a single element `[1, 2, [3, 4]]`, whereas `[1, 2].extend([3, 4])` unpacks and appends each item `[1, 2, 3, 4]`.
- **`key=lambda item: (-item[1], item[0])`:** Negating numeric scores (`-item[1]`) sorts scores in **descending** order while keeping the tie-breaker `item[0]` (student name) in **ascending** alphabetical order!
- **`[[0] * 3] * 3` Trap:** Multiplying an outer list repeats references to the **exact same inner list object**. Always initialize 2D DP tables and grids using `[[0] * cols for _ in range(rows)]`.

---

## 8. Common Mistakes

1. **Assigning the Result of `.sort()` or `.append()` (`nums = nums.sort()`):**
   In-place list methods (`.sort()`, `.reverse()`, `.append()`, `.extend()`) return **`None`** to remind you that they mutated the list in-place! Writing `nums = nums.sort()` overwrites `nums` with `None`.
2. **Using `[[0] * M] * N` for 2D Matrices:**
   Causes every row to share the same memory reference. Use `[[0] * M for _ in range(N)]`.
3. **Using `list.pop(0)` Inside a Loop (Queue Anti-Pattern):**
   Calling `pop(0)` `N` times takes `O(N^2)` total time. Use `collections.deque.popleft()` (`O(1)`) instead.

---

## 9. Practice Questions

1. **Easy:** Write a function `rotate_right_by_k(nums: list[int], k: int) -> list[int]` that rotates a list to the right by `k` steps using slicing (`k %= len(nums)`).
2. **Medium:** Write a function `move_zeros_in_place(nums: list[int]) -> None` that moves all `0`s to the end of the list in `O(n)` time and `O(1)` extra space while preserving the relative order of non-zero elements.
3. **Hard:** Write a function `merge_sorted_lists(a: list[int], b: list[int]) -> list[int]` that merges two already-sorted lists into one sorted list in `O(len(a) + len(b))` time without calling `.sort()` or `sorted()`.

---

## 10. Interview Questions

### Q1: How can `list.append(x)` have `O(1)` amortized time complexity if arrays have fixed sizes in memory?
**Answer:** CPython allocates a contiguous array with **extra spare capacity** (over-allocation). Most `.append()` calls simply write into the next free slot in `O(1)` time. Only when the capacity is full does CPython allocate a new array (~1.125x larger) and copy the pointers over. Averaged across $N$ appends, the cost per append is strictly **`O(1)` amortized**.

### Q2: What sorting algorithm does Python's `list.sort()` use, and is it stable?
**Answer:** Python uses **Timsort** (designed by Tim Peters—and since Python 3.11, **Powersort** for merge policy), a hybrid of Merge Sort and Insertion Sort. It is **stable** (elements with equal keys keep their original relative order), runs in **`O(n log n)`** worst-case time, and achieves **`O(n)`** best-case time on already-sorted or nearly-sorted arrays.

### Q3: What is the difference between `del nums[:]`, `nums.clear()`, and `nums = []`?
**Answer:**
- `nums.clear()` and `del nums[:]` empty the existing list object **in-place**, so any other variable referencing that same list also sees it become empty.
- `nums = []` rebinds the local variable `nums` to a **brand-new** empty list, leaving any other aliases pointing to the old list untouched.
