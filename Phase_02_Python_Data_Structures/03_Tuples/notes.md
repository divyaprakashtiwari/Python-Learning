# Topic 03: Tuples

---

## 1. Introduction

A **Tuple (`tuple`)** is an ordered, **immutable** sequence of elements usually enclosed in parentheses (`(10, 20, 30)`). Once a tuple is created, you cannot add, remove, or replace its element slots.

Think of a `list` as a changeable checklist of similar items (like a shopping list), and a `tuple` as a fixed, heterogeneous **record** (like a database row `(id, name, email)`, an `(x, y)` coordinate pair, or an `(R, G, B)` color value).

---

## 2. Why is it used?

1. **Hashable Dictionary Keys & Set Elements:** Because lists are mutable, you cannot store a `[row, col]` list in a `visited` set or use it as a `dict` key (`TypeError: unhashable type: 'list'`). Tuples `(row, col)` are immutable and **hashable**, making them essential for Graph BFS/DFS and Memoization (`@lru_cache`).
2. **Multi-Value Function Returns:** Returning `return low, high` automatically packs the values into a tuple that callers can unpack cleanly (`min_val, max_val = get_bounds(arr)`).
3. **Data Integrity & Lower Memory Overhead:** Tuples guarantee that a function won't accidentally mutate your sequence and allocate a single compact block in CPython memory.

---

## 3. Syntax

```python
# 1. Creation (Note the trailing comma for a 1-element tuple!)
empty_tuple = ()
single_item_tuple = (42,)      # Without comma, (42) is just an int!
point = (10, 20)
implicit_packing = 10, 20, 30  # Parentheses are optional when packing

# 2. Unpacking & Extended (*) Unpacking
x, y = point
first, *middle, last = (1, 2, 3, 4, 5)  # first=1, middle=[2, 3, 4], last=5

# 3. Built-in Tuple Methods (only 2 methods since tuples are immutable!)
count_of_two = (1, 2, 2, 3).count(2)    # 2
first_index = (10, 20, 30).index(20)    # 1
```

---

## 4. Explanation (Tuple Immutability vs Contained Object Mutability)

A tuple stores **immutable object references (pointers)** in fixed slots:
- You can **never** reassign a slot (`t[0] = 99` raises `TypeError`).
- However, if slot `t[1]` points to a **mutable list** (`t = ("A", [1, 2])`), the list itself can still be mutated via `t[1].append(3)`!
- **Hashability Rule:** A tuple is hashable (usable as a `dict` key or `set` element) **if and only if** all of its elements are also hashable (`("A", (1, 2))` is hashable; `("A", [1, 2])` is **not** hashable).

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_tuple_creation_and_unpacking.py`](example_01_tuple_creation_and_unpacking.py)
- [`example_02_tuples_as_hashable_dict_keys.py`](example_02_tuples_as_hashable_dict_keys.py)
- [`example_03_namedtuple_and_memory_efficiency.py`](example_03_namedtuple_and_memory_efficiency.py)

### Example 1: Tuple Creation, Single-Element Trailing Comma, and Unpacking (`example_01_tuple_creation_and_unpacking.py`)

```python
def compute_min_max_avg(numbers: list[float]) -> tuple[float, float, float]:
    """Return (minimum, maximum, average) packaged as a 3-element tuple."""
    return (min(numbers), max(numbers), sum(numbers) / len(numbers))


def main() -> None:
    print("=== 1. Single-Element Tuple vs Parenthesized Integer ===")
    not_a_tuple = (42)
    single_tuple = (42,)
    print(f"(42)  -> value={not_a_tuple}, type={type(not_a_tuple).__name__}")
    print(f"(42,) -> value={single_tuple}, type={type(single_tuple).__name__}")

    print("\n=== 2. Extended Iterable Unpacking (first, *middle, last) ===")
    lap_times = (58.2, 57.9, 59.1, 58.4, 56.8)
    opening_lap, *middle_laps, final_lap = lap_times
    print(f"Opening Lap : {opening_lap}s")
    print(f"Middle Laps : {middle_laps}")
    print(f"Final Lap   : {final_lap}s")

    print("\n=== 3. Unpacking Multi-Value Function Return ===")
    lowest, highest, mean = compute_min_max_avg([82.0, 91.5, 76.0, 94.5])
    print(f"Min: {lowest:.1f} | Max: {highest:.1f} | Avg: {mean:.2f}")


if __name__ == "__main__":
    main()
```

### Example 2: Tuples as Hashable Dictionary Keys (`example_02_tuples_as_hashable_dict_keys.py`)

```python
def main() -> None:
    grid_obstacles: dict[tuple[int, int], str] = {
        (0, 0): "Start Tower",
        (2, 4): "Laser Wall",
        (5, 7): "Goal Portal",
    }

    print("=== 1. Tuples as (row, col) Dictionary Keys ===")
    for coord in [(0, 0), (2, 4), (3, 3)]:
        feature = grid_obstacles.get(coord, "Empty Tile")
        print(f"  Coordinate {coord} -> {feature}")

    grades = ("A", "B", "A", "C", "A", "B")
    print("\n=== 2. Tuple Built-in Methods (.count & .index) ===")
    print(f"Grades Tuple      : {grades}")
    print(f"Count of 'A'      : {grades.count('A')}")
    print(f"First index of 'B': {grades.index('B')}")

    print("\n=== 3. Mutable List Inside a Tuple ===")
    student_record = ("STU-101", ["Math", "Physics"])
    student_record[1].append("Computer Science")
    print(f"Updated inner list inside tuple: {student_record}")


if __name__ == "__main__":
    main()
```

### Example 3: `collections.namedtuple` and Memory Efficiency (`example_03_namedtuple_and_memory_efficiency.py`)

```python
from collections import namedtuple
import sys

GeoPoint = namedtuple("GeoPoint", ["city", "lat", "lon"])


def main() -> None:
    print("=== 1. Readable Records with collections.namedtuple ===")
    hq = GeoPoint(city="Bengaluru", lat=12.9716, lon=77.5946)
    print(f"NamedTuple repr : {hq}")
    print(f"By Attribute    : city={hq.city}, lat={hq.lat}, lon={hq.lon}")
    print(f"By Index [0]    : {hq[0]} (100% backward-compatible with tuple!)")

    print("\n=== 2. Memory Footprint: tuple vs list ===")
    sample_tuple = tuple(range(1000))
    sample_list = list(range(1000))
    tuple_bytes = sys.getsizeof(sample_tuple)
    list_bytes = sys.getsizeof(sample_list)
    print(f"1000-element tuple size : {tuple_bytes} bytes")
    print(f"1000-element list size  : {list_bytes} bytes")
    print(f"Tuple uses fewer bytes? : {tuple_bytes < list_bytes}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== 1. Single-Element Tuple vs Parenthesized Integer ===
(42)  -> value=42, type=int
(42,) -> value=(42,), type=tuple

=== 2. Extended Iterable Unpacking (first, *middle, last) ===
Opening Lap : 58.2s
Middle Laps : [57.9, 59.1, 58.4]
Final Lap   : 56.8s

=== 3. Unpacking Multi-Value Function Return ===
Min: 76.0 | Max: 94.5 | Avg: 86.00
```

### Output for Example 2:
```text
=== 1. Tuples as (row, col) Dictionary Keys ===
  Coordinate (0, 0) -> Start Tower
  Coordinate (2, 4) -> Laser Wall
  Coordinate (3, 3) -> Empty Tile

=== 2. Tuple Built-in Methods (.count & .index) ===
Grades Tuple      : ('A', 'B', 'A', 'C', 'A', 'B')
Count of 'A'      : 3
First index of 'B': 1

=== 3. Mutable List Inside a Tuple ===
Updated inner list inside tuple: ('STU-101', ['Math', 'Physics', 'Computer Science'])
```

### Output for Example 3:
```text
=== 1. Readable Records with collections.namedtuple ===
NamedTuple repr : GeoPoint(city='Bengaluru', lat=12.9716, lon=77.5946)
By Attribute    : city=Bengaluru, lat=12.9716, lon=77.5946
By Index [0]    : Bengaluru (100% backward-compatible with tuple!)

=== 2. Memory Footprint: tuple vs list ===
1000-element tuple size : 8040 bytes
1000-element list size  : 8056 bytes
Tuple uses fewer bytes? : True
```

---

## 7. Code Explanation

- **`single_tuple = (42,)`** — It is actually the **comma** `,` that creates a tuple in Python, not the parentheses! `(42)` is just a mathematical grouping expression around `42`.
- **`opening_lap, *middle_laps, final_lap = lap_times`** — The starred target `*middle_laps` collects all intermediate elements into a `list` (even if 0 elements remain, in which case `middle_laps` is `[]`).
- **`GeoPoint = namedtuple(...)`** — Creates a lightweight tuple subclass whose fields can be accessed both by name (`hq.city`) and by index (`hq[0]`).

---

## 8. Common Mistakes

1. **Omitting the Comma in a Single-Element Tuple (`("hello")`):**
   Writing `for item in ("hello"):` iterates over the 5 characters `'h', 'e', 'l', 'l', 'o'` because `("hello")` is a `str`, not a 1-element tuple! Write `("hello",)`.
2. **Using `(x for x in range(5))` Expecting a Tuple Comprehension:**
   Parentheses around a comprehension create a **Generator Expression** (`<generator object>`), not a `tuple`! To build a tuple from a comprehension, wrap it in `tuple(x for x in range(5))`.
3. **Trying to Hash a Tuple Containing a List:**
   `hash((1, [2, 3]))` raises `TypeError: unhashable type: 'list'`. Convert inner lists to tuples `(1, (2, 3))` before using them as `dict` keys.

---

## 9. Practice Questions

1. **Easy:** Given a list of `(name, age, city)` tuples, unpack each tuple inside a `for` loop (`for name, age, city in records:`) and print a formatted summary.
2. **Medium:** Write a function `closest_pair_to_origin(points: list[tuple[int, int]]) -> tuple[int, int]` that sorts or scans 2D coordinate tuples by their squared Euclidean distance `x*x + y*y` from `(0, 0)`.
3. **Hard:** Given the puzzle expression `t = (1, [10, 20]); t[1] += [30]`, explain why Python raises a `TypeError: 'tuple' object does not support item assignment` **and yet** `t` still becomes `(1, [10, 20, 30])`!

---

## 10. Interview Questions

### Q1: What happens when you execute `t = (1, [10, 20]); t[1] += [30]`?
**Answer:** This is a famous Python interview brainteaser! `t[1] += [30]` executes in two steps:
1. It calls `list.__iadd__` on `t[1]`, which mutates the list **in-place** to `[10, 20, 30]` and returns the mutated list.
2. It attempts to assign the returned list back into `t[1]`, which raises `TypeError: 'tuple' object does not support item assignment`.
Therefore, **both** things happen: a `TypeError` is raised, and `t[1]` has already been mutated to `[10, 20, 30]`! (Using `t[1].append(30)` avoids step 2 and raises no error.)

### Q2: When is a `tuple` hashable and when is it unhashable?
**Answer:** A tuple is hashable (`hash(t)` succeeds) if and only if **every element recursively contained inside it is also hashable**. `(1, "a", (2, 3))` is hashable, whereas `(1, "a", [2, 3])` raises `TypeError: unhashable type: 'list'`.

### Q3: Why are tuples faster to construct and smaller in memory than lists?
**Answer:** Because a tuple's length is fixed at creation time, CPython allocates the tuple header and the pointer array in a **single contiguous memory block** with zero extra over-allocation, whereas a `list` requires two separate memory allocations (the list header object + a separate resizable pointer array with spare capacity).
