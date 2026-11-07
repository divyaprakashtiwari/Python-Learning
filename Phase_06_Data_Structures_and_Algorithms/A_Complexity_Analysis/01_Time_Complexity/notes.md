# Phase 6 — Section A: Complexity Analysis — Topic 01: Time Complexity

## 1. Introduction

**Time Complexity** quantifies how the number of elementary operations an algorithm executes grows as a function of the input size $N$. Rather than measuring raw wall-clock seconds—which fluctuate depending on CPU speed, background processes, and interpreter version—time complexity counts **machine-independent primitive steps** (comparisons, arithmetic operations, array index accesses, hash probes) to predict how an algorithm scales from $N = 10$ to $N = 10^7$.

---

## 2. Why is it used?

1. **Predicting Scalability Before Deployment:** An $O(n^2)$ nested loop takes less than 1 millisecond on $N = 100$ in development, but takes **100 billion operations (~20 minutes)** when production traffic hits $N = 300,000$.
2. **Coding Interview & Competitive Programming Constraints:** Online judges enforce ~1–2 second time limits ($\approx 10^7\text{–}10^8$ primitive operations in Python). Knowing $N$ immediately tells you which time complexity class is required:
   - $N \le 20 \implies O(2^n)$ or $O(n!)$
   - $N \le 2,000 \implies O(n^2)$
   - $N \le 10^5 \implies O(n \log n)$ or $O(n)$
   - $N \ge 10^9 \implies O(\log n)$ or $O(1)$
3. **Choosing the Right Python Built-in Container:** Knowing that `x in my_list` is $O(n)$ while `x in my_set` / `x in my_dict` is $O(1)$ average prevents accidental quadratic bottlenecks.

---

## 3. Syntax

```python
# 1. O(1) Constant Time — closed-form math, dict/set lookup, list.append()
total = (n * (n + 1)) // 2

# 2. O(log n) Logarithmic Time — halving the problem space each step
while n > 0:
    n //= 2

# 3. O(n) Linear Time — single pass over N elements
total = sum(items)

# 4. O(n log n) Linearithmic Time — sorting (Timsort / Merge Sort) or N binary searches
sorted_items = sorted(items)

# 5. O(n^2) Quadratic Time — nested loops over N x N pairs
for i in range(n):
    for j in range(n):
        ...
```

---

## 4. Explanation (Step-by-Step)

1. **What Counts as an $O(1)$ Primitive Operation in Python?**
   - Integer/float arithmetic (`a + b`), variable assignment, list indexing (`arr[i]`), `list.append(x)` (amortized), `deque.popleft()`, and `dict` / `set` key lookup (`k in d`, average case).
2. **Hidden $O(n)$ Operations Inside Single Lines of Python Code:**
   - Just because a statement has no visible `for` loop does **not** mean it runs in $O(1)$ time!
   - `x in my_list`, `my_list.index(x)`, `my_list.count(x)`, `my_list.pop(0)`, `my_list.insert(0, x)`, `arr[:]`, `min(arr)`, `max(arr)`, and `sum(arr)` all scan or shift $N$ elements in **$O(n)$** time.
   - Placing `if x in my_list:` inside a `for x in other_list:` loop silently turns a single loop into an **$O(n \cdot m)$** quadratic algorithm!
3. **Sequential vs Nested Composition Rules:**
   - **Sequential blocks add:** Running an $O(n)$ loop followed by an $O(n^2)$ loop costs $O(n + n^2) = O(n^2)$.
   - **Nested blocks multiply:** Running an $O(\log n)$ binary search inside an $O(n)$ loop costs $O(n \times \log n) = O(n \log n)$.

---

## 5. Minimum 3 Examples

### Example 01: Counting Exact Primitive Operations — $O(1)$ Formula vs $O(n)$ Loop vs $O(n^2)$ Nested Loop
File: [`example_01_counting_operations_o1_on_on2.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/A_Complexity_Analysis/01_Time_Complexity/example_01_counting_operations_o1_on_on2.py)

```python
"""
Phase 6 - Section A (Complexity Analysis) - Topic 01: Time Complexity
Example 01: Counting Exact Primitive Operations — O(1) Formula vs O(n) Loop vs O(n^2) Nested Loop

Demonstrates:
  - Why operation counts (not raw wall-clock seconds alone) measure algorithmic time complexity
  - Comparing Gauss's O(1) closed-form sum against an O(n) single loop and O(n^2) nested unit-addition loop
"""


def sum_o1_formula(n: int) -> tuple[int, int]:
    """Return `(total, step_count)` using Gauss's O(1) formula `n * (n + 1) // 2`."""
    steps = 1
    return (n * (n + 1)) // 2, steps


def sum_on_loop(n: int) -> tuple[int, int]:
    """Return `(total, step_count)` using a single O(n) loop."""
    total = 0
    steps = 0
    for i in range(1, n + 1):
        total += i
        steps += 1
    return total, steps


def sum_on2_nested(n: int) -> tuple[int, int]:
    """Return `(total, step_count)` using a naive O(n^2) nested loop."""
    total = 0
    steps = 0
    for i in range(1, n + 1):
        for _ in range(i):
            total += 1
            steps += 1
    return total, steps


def main() -> None:
    print("=== Operation Count Scaling Across Input Sizes N ===")
    print(f"  {'N':>5} | {'O(1) Steps':>12} | {'O(n) Steps':>12} | {'O(n^2) Steps':>14} | {'All Sums Equal?':>15}")
    print("  " + "-" * 68)
    for n in [10, 50, 200]:
        s1, c1 = sum_o1_formula(n)
        s2, c2 = sum_on_loop(n)
        s3, c3 = sum_on2_nested(n)
        equal = s1 == s2 == s3
        print(f"  {n:>5} | {c1:>12,} | {c2:>12,} | {c3:>14,} | {str(equal):>15}")


if __name__ == "__main__":
    main()
```

### Example 02: Logarithmic $O(\log n)$ Halving & Linearithmic $O(n \log n)$ Divide-and-Conquer
File: [`example_02_logarithmic_and_nlogn_step_counter.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/A_Complexity_Analysis/01_Time_Complexity/example_02_logarithmic_and_nlogn_step_counter.py)

```python
"""
Phase 6 - Section A (Complexity Analysis) - Topic 01: Time Complexity
Example 02: Logarithmic O(log n) Halving & Linearithmic O(n log n) Divide-and-Conquer

Demonstrates:
  - How repeatedly halving a search space (`n //= 2`) finishes in at most `floor(log2(n)) + 1` steps
  - How running an O(log n) halving loop for each of `n` elements produces O(n log n) total steps
"""

import math


def count_halving_steps(n: int) -> int:
    """Count how many times `n` can be halved before reaching 0 -> O(log n)."""
    steps = 0
    current = n
    while current > 0:
        current //= 2
        steps += 1
    return steps


def count_n_log_n_steps(n: int) -> int:
    """Perform an O(log n) halving trace for each of `n` items -> O(n log n)."""
    total_steps = 0
    for _ in range(n):
        total_steps += count_halving_steps(n)
    return total_steps


def main() -> None:
    print("=== O(log n) and O(n log n) Step Counts vs Theoretical `floor(log2(n)) + 1` ===")
    for n in [8, 64, 1024, 1_048_576]:
        log_steps = count_halving_steps(n)
        expected = math.floor(math.log2(n)) + 1
        print(f"  N = {n:>9,} -> O(log n) steps = {log_steps:>2} (expected={expected:>2})")

    print("\n=== O(n log n) Total Steps on Moderate Input Sizes ===")
    for n in [16, 128, 1024]:
        print(f"  N = {n:>5,} -> O(n log n) steps = {count_n_log_n_steps(n):>8,}")


if __name__ == "__main__":
    main()
```

### Example 03: Python Built-in Container Lookup Complexity — `list` $O(n)$ vs `set` $O(1)$
File: [`example_03_list_vs_set_lookup_benchmark.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/A_Complexity_Analysis/01_Time_Complexity/example_03_list_vs_set_lookup_benchmark.py)

```python
"""
Phase 6 - Section A (Complexity Analysis) - Topic 01: Time Complexity
Example 03: Python Built-in Container Lookup Complexity — `list` O(n) vs `set` O(1)

Demonstrates:
  - Why `x in my_list` scans sequentially in O(n) comparisons, whereas `x in my_set`
    computes `hash(x)` and probes the hash table in O(1) average comparisons
  - Reducing an O(n * m) duplicate intersection problem to O(n + m) using a `set`
"""


class TrackedInt(int):
    """Subclass of `int` that counts how many `==` equality comparisons are performed."""

    comparisons = 0

    def __eq__(self, other: object) -> bool:
        TrackedInt.comparisons += 1
        return super().__eq__(other)

    def __hash__(self) -> int:
        return super().__hash__()


def main() -> None:
    items_list = [TrackedInt(i) for i in range(500)]
    items_set = set(items_list)
    target = TrackedInt(499)  # Worst-case position at the very end of the list

    print("=== Comparing Equality Comparisons for Lookup of Last Element (N=500) ===")
    TrackedInt.comparisons = 0
    found_in_list = target in items_list
    list_comps = TrackedInt.comparisons

    TrackedInt.comparisons = 0
    found_in_set = target in items_set
    set_comps = TrackedInt.comparisons

    print(f"  target in list (O(n)) : found={found_in_list} | equality comparisons = {list_comps}")
    print(f"  target in set  (O(1)) : found={found_in_set} | equality comparisons = {set_comps}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== Operation Count Scaling Across Input Sizes N ===
      N |   O(1) Steps |   O(n) Steps |   O(n^2) Steps | All Sums Equal?
  --------------------------------------------------------------------
     10 |            1 |           10 |             55 |            True
     50 |            1 |           50 |          1,275 |            True
    200 |            1 |          200 |         20,100 |            True
```

### Output — Example 02
```text
=== O(log n) and O(n log n) Step Counts vs Theoretical `floor(log2(n)) + 1` ===
  N =         8 -> O(log n) steps =  4 (expected= 4)
  N =        64 -> O(log n) steps =  7 (expected= 7)
  N =     1,024 -> O(log n) steps = 11 (expected=11)
  N = 1,048,576 -> O(log n) steps = 21 (expected=21)

=== O(n log n) Total Steps on Moderate Input Sizes ===
  N =    16 -> O(n log n) steps =       80
  N =   128 -> O(n log n) steps =    1,024
  N = 1,024 -> O(n log n) steps =   11,264
```

### Output — Example 03
```text
=== Comparing Equality Comparisons for Lookup of Last Element (N=500) ===
  target in list (O(n)) : found=True | equality comparisons = 500
  target in set  (O(1)) : found=True | equality comparisons = 1
```

---

## 7. Code Explanation

1. **Step Counting (Example 01):** Notice that when $N$ increases $20\times$ (from `10` to `200`), the $O(n)$ loop increases $20\times$ (`10` to `200` steps), while the $O(n^2)$ nested loop explodes by $\approx 365\times$ (`55` to `20,100` steps), and the $O(1)$ Gauss formula stays at `1` step.
2. **Halving `n //= 2` (Example 02):** Even when $N$ exceeds one million (`1,048,576`), an $O(\log n)$ loop finishes in just **21 steps** because $2^{20} = 1,048,576$.
3. **`TrackedInt` Equality Counter (Example 03):** Instrumenting `__eq__` proves deterministically (without noisy wall-clock timers) that `target in items_list` executes `500` comparisons while `target in items_set` jumps directly to the hash bucket and executes `1` comparison.

---

## 8. Common Mistakes

1. **Assuming Every Nested Loop Is Automatically $O(n^2)$:**
   - In Sliding Window or Monotonic Stack algorithms, an inner `while` loop advances a pointer `left += 1` that **never resets**. Because `left` can advance at most $N$ times across the entire outer loop, the total time complexity is **$O(n)$**, not $O(n^2)$!
2. **Forgetting String Concatenation `s += ch` Inside a Loop Can Be $O(n^2)$:**
   - Because Python strings are immutable, repeated concatenation copies the growing string; always collect pieces in a `list` and call `"".join(pieces)` in $O(n)$.
3. **Slicing Inside a Recursive Call (`binary_search(arr[:mid])`):**
   - `arr[:mid]` copies $N/2$ elements in $O(n)$ time! Slicing inside binary search degrades $O(\log n)$ time into $O(n)$ time ($T(n) = T(n/2) + O(n) = O(n)$). Always pass `low` and `high` index pointers instead of slicing.

---

## 9. Practice Questions

1. **Easy:** What is the time complexity of checking if an integer $N$ is prime by testing divisibility up to $\lfloor\sqrt{N}\rfloor$? Implement `is_prime_sqrt(n: int) -> tuple[bool, int]` returning both the result and the exact number of `%` checks.
2. **Medium:** Analyze the time complexity of the harmonic series nested loop:
   ```python
   for i in range(1, n + 1):
       for j in range(i, n + 1, i):  # Step size is `i`!
           count += 1
   ```
   (Hint: $n/1 + n/2 + n/3 + \dots + n/n = O(n \log n)$).
3. **Hard:** Given two lists `a` (length $N$) and `b` (length $M$), implement `find_common_elements(a, b)` in $O(N + M)$ average time and compare its operation count against the naive $O(N \cdot M)$ list-membership approach.

---

## 10. Interview Questions

### Q1: What is the time complexity of `for i in range(1, n + 1): for j in range(1, n + 1, i):`?
**Answer:** **$O(n \log n)$**, NOT $O(n^2)$! For a given outer `i`, the inner loop steps by `i`, so it executes $\lfloor n / i \rfloor$ times. Summing over $i = 1 \dots n$ gives $n \sum_{i=1}^{n} \frac{1}{i} = n \cdot H_n = \Theta(n \log n)$, which is the exact reason the Sieve of Eratosthenes runs in $O(n \log \log n)$ / $O(n \log n)$ time.

### Q2: Why does `arr[:mid]` inside recursive binary search ruin the $O(\log n)$ time complexity?
**Answer:** Creating a slice `arr[:mid]` allocates and copies $n/2$ elements ($O(n)$ work). By the Master Theorem, $T(n) = T(n/2) + \Theta(n)$ resolves to **$O(n)$** total time ($n/2 + n/4 + n/8 + \dots = n$). Passing `low` and `high` integer indices keeps each step $O(1)$, preserving $O(\log n)$ time.

### Q3: What is the time complexity of `len(obj)` on a Python `list`, `dict`, `set`, or `str`?
**Answer:** Strictly **$O(1)$**. Every CPython variable-size built-in container (`PyVarObject`) stores its current element count in a C struct header field (`ob_size` / `ma_used`), so `len(obj)` simply reads that integer field without iterating.
