# Top Python & DSA Interview Questions (`INTERVIEW_QUESTIONS.md`)

A curated handbook of frequently asked Python and Data Structures & Algorithms interview questions for software engineering placements and coding rounds.

---

## Part 1: Python Fundamentals & Internals

### 1. Is Python compiled or interpreted?
**Answer:** Python is an **interpreted** language, though it uses an intermediate compilation step. When you run a `.py` file, Python first compiles the source code into **bytecode** (`.pyc`), which is then executed line-by-line by the **Python Virtual Machine (PVM)**.

### 2. What is the difference between `==` and `is` in Python?
**Answer:**
- `==` (Equality Operator) checks whether two variables have the **same value**.
- `is` (Identity Operator) checks whether two variables point to the **exact same object in memory** (`id(a) == id(b)`).

### 3. Why are strings and tuples immutable in Python, and what does that mean?
**Answer:** Immutability means once an object is created in memory, its contents cannot be altered in-place. Modifying a string creates a brand-new string object. This makes strings and tuples thread-safe and **hashable**, allowing them to be used as dictionary keys and set elements.

---

## Part 2: Python Data Structures

### 4. What is the difference between a `list` and a `tuple`?
**Answer:**
- **Mutability:** Lists (`[]`) are mutable; tuples (`()`) are immutable.
- **Memory & Speed:** Tuples consume less memory and are slightly faster to iterate over because Python allocates a fixed-size memory block.
- **Hashability:** Tuples of immutable elements can be used as `dict` keys; lists cannot.

### 5. How do Python Dictionaries achieve `O(1)` average lookup time?
**Answer:** Python dictionaries are implemented as **Hash Tables**. When you insert or look up `d[key]`, Python computes `hash(key)` to determine an index in an underlying array of buckets. Collisions are resolved using **open addressing** with random probing.

### 6. Why is using `list.pop(0)` bad for queues, and what should you use instead?
**Answer:** `list.pop(0)` shifts every remaining element in the list one position to the left, taking `O(n)` time. Instead, use `collections.deque` and call `popleft()`, which runs in `O(1)` constant time.

---

## Part 3: Functions, Scope & OOP

### 7. Why is `def append_item(item, target=[]):` a dangerous anti-pattern?
**Answer:** Default arguments in Python are evaluated **only once** when the `def` statement is executed, not each time the function is called. All calls that omit `target` share the **same mutable list**. Instead, use `target=None` and initialize `if target is None: target = []` inside the function.

### 8. What is the LEGB Rule in Python?
**Answer:** LEGB defines the order in which Python resolves variable names:
1. **L — Local:** Inside the current function.
2. **E — Enclosing:** Inside enclosing functions (for nested functions/closures).
3. **G — Global:** At the top level of the module.
4. **B — Built-in:** Preassigned names in Python's `builtins` module (`len`, `print`, `range`).

### 9. Difference between `@staticmethod` and `@classmethod`?
**Answer:**
- `@classmethod` receives the class `cls` as its first parameter. It can access/modify class state and is commonly used to build **alternative constructors**.
- `@staticmethod` receives neither `self` nor `cls`. It behaves like a plain function grouped inside the class namespace for logical organization.

---

## Part 4: Advanced Python

### 10. How do Generators save memory compared to Lists?
**Answer:** A list comprehension `[x*x for x in range(10**7)]` computes and stores all 10 million values in RAM immediately. A generator expression or function using `yield` computes values **lazily** one at a time on demand, using `O(1)` auxiliary memory.

### 11. What is the difference between Shallow Copy and Deep Copy?
**Answer:**
- **Shallow Copy (`copy.copy`)** creates a new outer container, but inserts **references** to the nested inner objects. Mutating a nested list affects both copies.
- **Deep Copy (`copy.deepcopy`)** recursively clones the outer container and **all nested objects**, making the two structures completely independent.

---

## Part 5: Data Structures & Algorithms (DSA)

### 12. When can Binary Search be applied beyond sorted arrays?
**Answer:** Binary Search (`O(log n)`) can be applied to any problem with a **monotonic search space** ("Binary Search on Answer")—where if a condition is `True` for value `x`, it remains `True` for all values `> x` (or `< x`). Examples include Koko Eating Bananas, Allocate Minimum Pages, and Aggressive Cows.

### 13. What is the difference between Memoization and Tabulation in Dynamic Programming?
**Answer:**
- **Memoization (Top-Down):** Recursive approach that caches results of subproblems in a hash map or array (`@lru_cache`). Computes only reachable states but carries recursion stack overhead.
- **Tabulation (Bottom-Up):** Iterative approach that fills a DP table starting from base cases. Avoids recursion limit issues and often allows space optimization (`O(n)` to `O(1)`).
