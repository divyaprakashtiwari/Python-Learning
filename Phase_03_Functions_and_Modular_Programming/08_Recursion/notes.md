# Phase 3 — Topic 08: Recursion

## 1. Introduction

**Recursion** is a problem-solving technique where a function calls **itself** on smaller, simpler instances of the same problem until it reaches a trivial **base case** that can be answered directly.

Every valid recursive function has two essential parts:
1. **Base Case:** The stopping condition that returns a value immediately without making another recursive call.
2. **Recursive Step:** The logic that shrinks the input toward the base case and combines the recursive result.

---

## 2. Why is it used?

- **Hierarchical & Tree-Shaped Data:** File systems, HTML/DOM trees, nested JSON configurations, and Abstract Syntax Trees (ASTs) have arbitrary depth where writing nested `for` loops is impossible, whereas recursion handles any depth in a few lines of code.
- **Divide-and-Conquer Algorithms:** Classic algorithms like Binary Search, Merge Sort, and Quick Sort split a problem into subproblems of half the size ($O(\log n)$ depth).
- **Backtracking & Dynamic Programming:** Generating permutations, subsets, solving N-Queens/Sudoku, and top-down memoized Dynamic Programming (`@lru_cache`) are naturally expressed recursively.

---

## 3. Syntax

```python
def recursive_function(problem_input):
    # 1. Base Case: Stop recursion when input is smallest/trivial
    if is_trivial(problem_input):
        return base_value

    # 2. Recursive Step: Call self with a strictly smaller input
    smaller_input = shrink(problem_input)
    sub_result = recursive_function(smaller_input)
    return combine(problem_input, sub_result)
```

---

## 4. Explanation (Step-by-Step)

### Step 1: Winding vs Unwinding on the Call Stack
When `factorial_traced(4)` runs:
1. **Winding Phase (Pushing Stack Frames):**
   - `factorial(4)` pauses waiting for `factorial(3)`
   - `factorial(3)` pauses waiting for `factorial(2)`
   - `factorial(2)` pauses waiting for `factorial(1)`
2. **Base Case Hit:**
   - `factorial(1)` returns `1` immediately.
3. **Unwinding Phase (Popping Stack Frames):**
   - `factorial(2)` computes `2 * 1 = 2` and pops.
   - `factorial(3)` computes `3 * 2 = 6` and pops.
   - `factorial(4)` computes `4 * 6 = 24` and pops.

### Step 2: Space Complexity of Recursion ($O(\text{depth})$)
Every active recursive call occupies a stack frame in memory holding its local variables and return address. Therefore, a recursive function with maximum depth $d$ uses **$O(d)$ auxiliary call-stack space**—even if it allocates no lists or dictionaries!

### Step 3: Tree Recursion & Memoization (`@lru_cache`)
When a function makes **two or more** recursive calls per frame (like `fib(n - 1) + fib(n - 2)`), the call tree branches exponentially ($O(2^n)$ calls) if subproblems overlap. Decorating the function with `@functools.lru_cache(maxsize=None)` caches each computed input so every unique state runs only once, collapsing time complexity from $O(2^n)$ (`21,891` calls for $n=20$) to $O(n)$ (`21` calls)!

### Step 4: Python's Recursion Limit (`sys.getrecursionlimit()`)
To prevent a runaway recursive function from crashing the underlying C process with a C stack overflow segfault, CPython enforces a maximum call stack depth of **`1000` frames** by default (inspectable via `sys.getrecursionlimit()`), raising a catchable `RecursionError` if exceeded.

---

## 5. Minimum 3 Examples

### Example 1: Anatomy of Recursion (Base Case, Recursive Step & Call Stack Trace)
File: `example_01_call_stack_trace_and_base_case.py`

```python
def factorial_traced(n: int, depth: int = 0) -> int:
    """Compute n! while printing the winding and unwinding call stack frames."""
    indent = "  " * (depth + 1)
    print(f"{indent}-> Enter factorial_traced(n={n})")

    # 1. Base Case: stops the recursion
    if n <= 1:
        print(f"{indent}<- Base case reached! Returning 1")
        return 1

    # 2. Recursive Step: problem reduced from `n` to `n - 1`
    sub_result = factorial_traced(n - 1, depth + 1)
    total = n * sub_result
    print(f"{indent}<- Unwinding n={n}: {n} * {sub_result} = {total}")
    return total


def power_fast(base: int, exp: int) -> int:
    """Compute `base ** exp` in O(log exp) time using binary exponentiation."""
    if exp == 0:
        return 1
    half = power_fast(base, exp // 2)
    if exp % 2 == 0:
        return half * half
    return base * half * half


def main() -> None:
    print("=== 1. Call Stack Trace for `factorial_traced(4)` ===")
    ans = factorial_traced(4)
    print(f"  Final Result: 4! = {ans}")

    print("\n=== 2. O(log n) Recursive Binary Exponentiation ===")
    print(f"  power_fast(2, 10) = {power_fast(2, 10)}")
    print(f"  power_fast(3, 7)  = {power_fast(3, 7)}")


if __name__ == "__main__":
    main()
```

---

### Example 2: Divide-and-Conquer Recursion & Nested Tree/JSON Flattening
File: `example_02_divide_and_conquer_and_tree_traversal.py`

```python
from typing import Any


def binary_search_recursive(
    arr: list[int],
    target: int,
    low: int,
    high: int,
) -> int:
    """Return index of `target` in sorted `arr[low..high]`, or -1 if absent."""
    if low > high:
        return -1  # Base case: search space exhausted

    mid = (low + high) // 2
    if arr[mid] == target:
        return mid  # Base case: target found
    if target < arr[mid]:
        return binary_search_recursive(arr, target, low, mid - 1)
    return binary_search_recursive(arr, target, mid + 1, high)


def flatten_nested_json(
    data: dict[str, Any],
    parent_key: str = "",
    sep: str = ".",
) -> dict[str, Any]:
    """Recursively flatten an arbitrarily nested dictionary into dot-separated keys."""
    flat: dict[str, Any] = {}
    for key, value in data.items():
        full_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict) and value:
            # Recursive step: merge flattened sub-dictionary
            flat.update(flatten_nested_json(value, full_key, sep=sep))
        else:
            # Base case: leaf value
            flat[full_key] = value
    return flat


def main() -> None:
    print("=== 1. Recursive Binary Search ===")
    sorted_ids = [102, 115, 128, 144, 159, 173, 188, 205]
    for target in (144, 205, 130):
        idx = binary_search_recursive(sorted_ids, target, 0, len(sorted_ids) - 1)
        print(f"  Search target={target:<3} -> index={idx}")

    print("\n=== 2. Flattening Arbitrary-Depth Nested Config via Recursion ===")
    nested_config = {
        "service": "payment-api",
        "database": {
            "primary": {"host": "db-01.internal", "port": 5432},
            "pool": {"max_size": 20},
        },
        "feature_flags": {"enable_upi": True},
    }
    flattened = flatten_nested_json(nested_config)
    for k, v in flattened.items():
        print(f"  {k:<28} = {v!r}")


if __name__ == "__main__":
    main()
```

---

### Example 3: Tree Recursion, Memoization (`@lru_cache`), and `RecursionError`
File: `example_03_memoization_and_recursion_limit.py`

```python
from functools import lru_cache
import sys

naive_call_count = 0
memo_call_count = 0


def fib_naive(n: int) -> int:
    """O(2^n) naive tree recursion - recomputes overlapping subproblems."""
    global naive_call_count
    naive_call_count += 1
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


@lru_cache(maxsize=None)
def fib_memoized(n: int) -> int:
    """O(n) memoized recursion - each state `n` is computed only ONCE."""
    global memo_call_count
    memo_call_count += 1
    if n <= 1:
        return n
    return fib_memoized(n - 1) + fib_memoized(n - 2)


def tower_of_hanoi(
    n_disks: int,
    source: str,
    auxiliary: str,
    target: str,
    moves: list[str],
) -> None:
    """Record the sequence of moves to transfer `n_disks` from `source` to `target`."""
    if n_disks == 1:
        moves.append(f"Disk 1: {source} -> {target}")
        return
    tower_of_hanoi(n_disks - 1, source, target, auxiliary, moves)
    moves.append(f"Disk {n_disks}: {source} -> {target}")
    tower_of_hanoi(n_disks - 1, auxiliary, source, target, moves)


def main() -> None:
    print("=== 1. Naive O(2^n) vs Memoized O(n) Fibonacci (n=20) ===")
    ans_naive = fib_naive(20)
    ans_memo = fib_memoized(20)
    print(f"  fib(20) = {ans_naive} (matches memoized: {ans_naive == ans_memo})")
    print(f"  Naive recursive calls made    : {naive_call_count:,}")
    print(f"  Memoized recursive calls made : {memo_call_count:,}")

    print("\n=== 2. Tower of Hanoi (3 Disks) ===")
    hanoi_moves: list[str] = []
    tower_of_hanoi(3, "A", "B", "C", hanoi_moves)
    for step_no, move in enumerate(hanoi_moves, start=1):
        print(f"  Step {step_no}: {move}")

    print("\n=== 3. Recursion Depth Limit & `RecursionError` ===")
    print(f"  Default sys.getrecursionlimit() = {sys.getrecursionlimit()}")

    def infinite_recurse(x: int) -> int:
        return infinite_recurse(x + 1)

    try:
        infinite_recurse(0)
    except RecursionError as err:
        print(f"  Caught expected RecursionError  : {err}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_call_stack_trace_and_base_case.py`)
```text
=== 1. Call Stack Trace for `factorial_traced(4)` ===
  -> Enter factorial_traced(n=4)
    -> Enter factorial_traced(n=3)
      -> Enter factorial_traced(n=2)
        -> Enter factorial_traced(n=1)
        <- Base case reached! Returning 1
      <- Unwinding n=2: 2 * 1 = 2
    <- Unwinding n=3: 3 * 2 = 6
  <- Unwinding n=4: 4 * 6 = 24
  Final Result: 4! = 24

=== 2. O(log n) Recursive Binary Exponentiation ===
  power_fast(2, 10) = 1024
  power_fast(3, 7)  = 2187
```

### Output — Example 2 (`example_02_divide_and_conquer_and_tree_traversal.py`)
```text
=== 1. Recursive Binary Search ===
  Search target=144 -> index=3
  Search target=205 -> index=7
  Search target=130 -> index=-1

=== 2. Flattening Arbitrary-Depth Nested Config via Recursion ===
  service                      = 'payment-api'
  database.primary.host        = 'db-01.internal'
  database.primary.port        = 5432
  database.pool.max_size       = 20
  feature_flags.enable_upi     = True
```

### Output — Example 3 (`example_03_memoization_and_recursion_limit.py`)
```text
=== 1. Naive O(2^n) vs Memoized O(n) Fibonacci (n=20) ===
  fib(20) = 6765 (matches memoized: True)
  Naive recursive calls made    : 21,891
  Memoized recursive calls made : 21

=== 2. Tower of Hanoi (3 Disks) ===
  Step 1: Disk 1: A -> C
  Step 2: Disk 2: A -> B
  Step 3: Disk 1: C -> B
  Step 4: Disk 3: A -> C
  Step 5: Disk 1: B -> A
  Step 6: Disk 2: B -> C
  Step 7: Disk 1: A -> C

=== 3. Recursion Depth Limit & `RecursionError` ===
  Default sys.getrecursionlimit() = 1000
  Caught expected RecursionError  : maximum recursion depth exceeded
```

---

## 7. Code Explanation

1. **Binary Exponentiation (`example_01`):** Instead of multiplying `base` $n$ times ($O(n)$ depth), `power_fast(base, exp)` computes `half = power_fast(base, exp // 2)` once and squares it (`half * half`), reaching `exp == 0` in at most $\lfloor\log_2(\text{exp})\rfloor + 1$ calls.
2. **Pass Index Bounds Instead of Slicing (`example_02`):** In `binary_search_recursive(arr, target, low, high)`, we pass integer indices `low` and `high` rather than slicing `arr[:mid]`. Slicing a list copies $O(n)$ elements at every step, which would degrade Binary Search from $O(\log n)$ time to $O(n)$ time!
3. **Memoization Impact (`example_03`):** For `n = 20`, `fib_naive` makes `21,891` calls because it recomputes `fib(18)`, `fib(17)`, ..., `fib(2)` thousands of times. `@lru_cache` computes each `n` from `0` to `20` once (`21` calls total).

---

## 8. Common Mistakes

1. **Forgetting the `return` keyword before the recursive call:**
   ```python
   # BUG: Returns `None` when unwinding!
   def binary_search_buggy(arr, target, low, high):
       ...
       if target < arr[mid]:
           binary_search_buggy(arr, target, low, mid - 1)  # Missing `return`!
   ```
   If a function returns a value in its base case, every recursive branch must also `return` the result of its recursive call.
2. **Slicing lists (`arr[1:]`) inside recursive calls:**
   - Writing `def sum_list(arr): return 0 if not arr else arr[0] + sum_list(arr[1:])` copies the remaining list at every step, turning an $O(n)$ traversal into **$O(n^2)$ time and $O(n^2)$ memory**! Pass an index `idx: int = 0` instead.
3. **Missing or unreachable base case (e.g., `if n == 0` when `n` starts negative or steps by 2):**
   - Use defensive inequalities (`if n <= 0:` or `if low > high:`) so odd/negative inputs don't skip past the base case and trigger `RecursionError`.

---

## 9. Practice Questions

1. **Easy — Recursive Digit Sum:**
   Write a recursive function `sum_of_digits(n: int) -> int` that returns the sum of digits of a non-negative integer `n` (e.g., `sum_of_digits(9427) -> 22`) using `n % 10` and `n // 10` without converting `n` to a string.

2. **Medium — Recursive Palindrome Checker (Using Index Pointers):**
   Write `is_palindrome_recursive(s: str, left: int = 0, right: int | None = None) -> bool` that checks if `s` is a palindrome in $O(n)$ time without slicing `s`.

3. **Hard — Deep Sum of Arbitrarily Nested Lists:**
   Write `deep_sum(nested: list[Any]) -> int` that computes the sum of all integers inside a jagged nested list of arbitrary depth (e.g., `deep_sum([1, [2, [3, 4], []], 5]) -> 15`).

---

## 10. Interview Questions

### Q1: Does Python support Tail Call Optimization (TCO)?
**Answer:**
**No.** Even if a recursive call is in tail position (the very last operation before returning), CPython intentionally does **not** eliminate the stack frame. Guido van Rossum rejected TCO in Python because:
1. TCO destroys stack traces, making debugging much harder.
2. In Python, functions can be rebound dynamically at runtime, making static tail-call replacement unsafe.
Therefore, linear tail recursion in Python still consumes $O(n)$ stack space and hits `RecursionError` around $n = 1000$; rewrite simple linear tail-recursions as `while` loops.

### Q2: What is the time and space complexity of `def fib(n): return n if n <= 1 else fib(n-1) + fib(n-2)` without memoization?
**Answer:**
- **Time Complexity:** $O(2^n)$ (more tightly $\Theta(\phi^n)$ where $\phi \approx 1.618$), because each call branches into two recursive calls.
- **Space Complexity:** **$O(n)$** (NOT $O(2^n)$!), because at any single moment in time, the call stack only holds a single root-to-leaf path of length at most $n$ frames (`fib(n) -> fib(n-1) -> ... -> fib(1)`). Frames are popped as branches finish.

### Q3: When should you prefer recursion over iteration in Python interviews?
**Answer:**
- **Prefer Iteration (`for`/`while`)** for simple linear sequences ($1\text{D}$ arrays, linked lists, sliding windows, binary search) to achieve $O(1)$ auxiliary space and avoid `RecursionError` on inputs with $N > 1000$.
- **Prefer Recursion** for trees, graphs (DFS), divide-and-conquer (Merge Sort / Quick Sort where depth is $O(\log N)$), backtracking (subsets, permutations), and nested recursive structures (JSON/ASTs).
