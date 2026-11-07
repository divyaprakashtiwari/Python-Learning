# Phase 6 — Section A: Complexity Analysis — Topic 02: Space Complexity

## 1. Introduction

**Space Complexity** measures how the memory required by an algorithm scales with the size of its input $N$. In interviews and algorithm analysis, we distinguish between:
- **Total Space Complexity:** The memory occupied by the input data itself **plus** any extra memory allocated during execution.
- **Auxiliary Space Complexity:** **Only the extra/temporary memory** allocated by the algorithm beyond the input—including temporary arrays/hash maps, slices, and **recursive call-stack frames**.

When an interviewer asks *"Can you solve this in $O(1)$ space?"*, they mean **$O(1)$ auxiliary space**.

---

## 2. Why is it used?

1. **Preventing `MemoryError` and Out-Of-Memory (OOM) Container Kills:** Cloud workers and Kubernetes pods have strict RAM limits; an $O(n^2)$ DP table on $N = 50,000$ attempts to allocate $2.5 \times 10^9$ cells (~20 GB) and crashes immediately, whereas space-optimized $O(n)$ DP uses only 400 KB.
2. **Preventing `RecursionError` Stack Overflows:** Python's default recursion limit is `1000` frames (`sys.getrecursionlimit()`). An unoptimized $O(n)$-depth recursion on a list or skewed tree of $N = 5,000$ nodes crashes unless converted to an $O(1)$-space iterative loop or an explicit stack.
3. **Time-Space Tradeoffs:** Frequently, spending $O(n)$ auxiliary memory on a hash map (`dict`/`set`) or memoization cache reduces time complexity from $O(n^2)$ or $O(2^n)$ down to $O(n)$.

---

## 3. Syntax

```python
# 1. O(1) Auxiliary Space — in-place swap using a fixed number of scalar variables
left, right = 0, len(arr) - 1
while left < right:
    arr[left], arr[right] = arr[right], arr[left]
    left += 1
    right -= 1

# 2. O(n) Auxiliary Space — allocating a new container or slice proportional to N
reversed_copy = arr[::-1]
seen_map = {val: idx for idx, val in enumerate(arr)}

# 3. O(n) Call-Stack Space — linear recursion depth N
def sum_recursive(n: int) -> int:
    return 0 if n == 0 else n + sum_recursive(n - 1)
```

---

## 4. Explanation (Step-by-Step)

1. **In-Place ($O(1)$ Auxiliary Space) vs Out-of-Place ($O(n)$ Auxiliary Space):**
   - An **in-place** algorithm mutates the input structure directly using only a constant number of scalar index/pointer variables (`left`, `right`, `curr`, `prev`), regardless of how large $N$ grows.
2. **Why Recursion Costs Memory Even Without Lists or Dicts:**
   - Every active function call pushes a **stack frame** onto the call stack storing its local variables, parameters, and return address.
   - The call-stack space of a recursive algorithm is proportional to the **maximum depth of the recursion tree** active at any single moment—**not** the total number of recursive calls made!
   - Example: Naive recursive Fibonacci `fib(n - 1) + fib(n - 2)` makes $O(2^n)$ total calls, but because `fib(n - 1)` finishes and pops its frames before `fib(n - 2)` starts, at most $N$ frames exist on the stack simultaneously $\implies$ **$O(n)$ auxiliary space**.
3. **Hidden Memory Allocations in Python:**
   - Slicing (`arr[1:]`, `s[::-1]`) allocates a brand-new copy of the sliced elements.
   - `sorted(arr)` allocates a new list of size $N$ ($O(n)$ space); even `arr.sort()` (Timsort) uses up to $O(n)$ temporary merge buffer space in the worst case ($O(1)$ on already-sorted runs).

---

## 5. Minimum 3 Examples

### Example 01: Auxiliary Space $O(1)$ In-Place Array Reversal vs $O(n)$ Out-of-Place Copy
File: [`example_01_auxiliary_space_o1_in_place_vs_on_copy.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/A_Complexity_Analysis/02_Space_Complexity/example_01_auxiliary_space_o1_in_place_vs_on_copy.py)

```python
"""
Phase 6 - Section A (Complexity Analysis) - Topic 02: Space Complexity
Example 01: Auxiliary Space O(1) In-Place Array Reversal vs O(n) Out-of-Place Copy

Demonstrates:
  - Total Space vs Auxiliary Space (extra memory allocated beyond the input itself)
  - Reversing a list in O(1) auxiliary space using two pointers vs O(n) slice allocation
"""


def reverse_out_of_place_on(nums: list[int]) -> list[int]:
    """Allocate a brand-new list of length N -> O(n) auxiliary space."""
    return nums[::-1]


def reverse_in_place_o1(nums: list[int]) -> None:
    """Swap elements in-place using two scalar index variables -> O(1) auxiliary space."""
    left = 0
    right = len(nums) - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1


def main() -> None:
    original = [10, 20, 30, 40, 50]

    print("=== 1. Out-of-Place Reversal (`O(n)` Auxiliary Space) ===")
    copied = reverse_out_of_place_on(original)
    print(f"  New object allocated? {copied is not original} | Result: {copied}")

    print("\n=== 2. In-Place Two-Pointer Reversal (`O(1)` Auxiliary Space) ===")
    before_id = id(original)
    reverse_in_place_o1(original)
    print(f"  Same list object in memory? {id(original) == before_id} | Result: {original}")


if __name__ == "__main__":
    main()
```

### Example 02: Recursion Call-Stack Space — $O(n)$ Linear Recursion vs $O(1)$ Iterative Loop
File: [`example_02_recursion_call_stack_space_depth.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/A_Complexity_Analysis/02_Space_Complexity/example_02_recursion_call_stack_space_depth.py)

```python
"""
Phase 6 - Section A (Complexity Analysis) - Topic 02: Space Complexity
Example 02: Recursion Call-Stack Space — O(n) Linear Recursion vs O(1) Iterative Loop

Demonstrates:
  - Why recursive functions without extra arrays still consume O(depth) auxiliary space
    on the Python call stack
  - Measuring peak recursion frame depth explicitly
"""


def factorial_recursive(n: int, current_depth: int = 1) -> tuple[int, int]:
    """Return `(n!, max_stack_depth_reached)` -> O(n) call-stack space."""
    if n <= 1:
        return 1, current_depth
    sub_fact, max_depth = factorial_recursive(n - 1, current_depth + 1)
    return n * sub_fact, max_depth


def factorial_iterative(n: int) -> tuple[int, int]:
    """Return `(n!, stack_frames_used)` -> O(1) auxiliary space."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result, 1


def main() -> None:
    print("=== Comparing Call-Stack Frame Depth: Recursive O(n) vs Iterative O(1) ===")
    for n in [5, 10]:
        rec_val, rec_depth = factorial_recursive(n)
        iter_val, iter_depth = factorial_iterative(n)
        print(
            f"  n={n:>2}: value={rec_val:>7} | "
            f"Recursive stack frames={rec_depth:>2} (O(n)) | Iterative frames={iter_depth} (O(1))"
        )


if __name__ == "__main__":
    main()
```

### Example 03: Time-Space Tradeoff — $O(n^2)$ Time / $O(1)$ Space vs $O(n)$ Time / $O(n)$ Space (`Two Sum`)
File: [`example_03_time_space_tradeoff_memoization.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/A_Complexity_Analysis/02_Space_Complexity/example_03_time_space_tradeoff_memoization.py)

```python
"""
Phase 6 - Section A (Complexity Analysis) - Topic 02: Space Complexity
Example 03: Time-Space Tradeoff — O(n^2) Time / O(1) Space vs O(n) Time / O(n) Space (`Two Sum`)

Demonstrates:
  - Trading O(n) extra hash-map memory to reduce time complexity from O(n^2) to O(n)
"""


def two_sum_brute_force_o1_space(nums: list[int], target: int) -> tuple[tuple[int, int] | None, int]:
    """O(n^2) time, O(1) auxiliary space: check all pairs without extra containers."""
    checks = 0
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            checks += 1
            if nums[i] + nums[j] == target:
                return (i, j), checks
    return None, checks


def two_sum_hashmap_on_space(nums: list[int], target: int) -> tuple[tuple[int, int] | None, int, int]:
    """O(n) time, O(n) auxiliary space: store seen values in a hash map."""
    seen: dict[int, int] = {}
    checks = 0
    for idx, val in enumerate(nums):
        checks += 1
        complement = target - val
        if complement in seen:
            return (seen[complement], idx), checks, len(seen)
        seen[val] = idx
    return None, checks, len(seen)


def main() -> None:
    nums = [3, 8, 12, 19, 25, 31, 44, 50, 62, 77]
    target = 139  # 62 + 77 at indices (8, 9)

    print("=== Time-Space Tradeoff on `two_sum` (N=10, target=139) ===")
    pair_bf, checks_bf = two_sum_brute_force_o1_space(nums, target)
    pair_hm, checks_hm, dict_entries = two_sum_hashmap_on_space(nums, target)

    print(f"  Brute Force (O(1) space, O(n^2) time) -> pair={pair_bf}, loop checks={checks_bf}, dict_size=0")
    print(f"  Hash Map    (O(n) space, O(n) time)   -> pair={pair_hm}, loop checks={checks_hm}, dict_size={dict_entries}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== 1. Out-of-Place Reversal (`O(n)` Auxiliary Space) ===
  New object allocated? True | Result: [50, 40, 30, 20, 10]

=== 2. In-Place Two-Pointer Reversal (`O(1)` Auxiliary Space) ===
  Same list object in memory? True | Result: [50, 40, 30, 20, 10]
```

### Output — Example 02
```text
=== Comparing Call-Stack Frame Depth: Recursive O(n) vs Iterative O(1) ===
  n= 5: value=    120 | Recursive stack frames= 5 (O(n)) | Iterative frames=1 (O(1))
  n=10: value=3628800 | Recursive stack frames=10 (O(n)) | Iterative frames=1 (O(1))
```

### Output — Example 03
```text
=== Time-Space Tradeoff on `two_sum` (N=10, target=139) ===
  Brute Force (O(1) space, O(n^2) time) -> pair=(8, 9), loop checks=45, dict_size=0
  Hash Map    (O(n) space, O(n) time)   -> pair=(8, 9), loop checks=10, dict_size=9
```

---

## 7. Code Explanation

1. **In-Place Swap `reverse_in_place_o1` (Example 01):** Uses only two integer variables (`left` and `right`) whether `nums` has 5 elements or 50,000,000 elements—making its auxiliary space strictly $O(1)$.
2. **Call-Stack Depth (Example 02):** `factorial_recursive(10)` holds 10 pending frames simultaneously on the call stack waiting for base case `n == 1` to return, whereas `factorial_iterative(10)` updates `result` inside a single stack frame.
3. **Time-Space Tradeoff (Example 03):** By investing $O(n)$ space in `seen: dict[int, int]`, each element only needs an $O(1)$ hash lookup for `target - val`, slashing the number of checks from $\binom{N}{2} = 45$ down to $10$.

---

## 8. Common Mistakes

1. **Claiming a Recursive Algorithm Uses $O(1)$ Space Because It Allocates No Arrays:**
   - Call-stack frames count toward auxiliary space! A recursive DFS on a binary tree of height $H$ uses $O(H)$ auxiliary space ($O(\log n)$ for balanced trees, $O(n)$ for skewed trees).
2. **Assuming Python Performs Tail-Call Elimination (TCO):**
   - Unlike Scheme or Haskell, Python **intentionally does not optimize tail recursion** (to preserve complete stack traces for debugging). A tail-recursive function in Python still consumes $O(n)$ stack space!
3. **Using `[expr for x in seq]` Inside `sum()` or `any()`:**
   - `sum([x * x for x in range(n)])` allocates an $O(n)$ list in RAM before summing. Removing the square brackets `sum(x * x for x in range(n))` uses a generator expression in **$O(1)$ space**.

---

## 9. Practice Questions

1. **Easy:** Convert an $O(n)$-space DP array for computing the $n$-th Fibonacci number (`dp = [0] * (n + 1)`) into an **$O(1)$-space** iterative function that keeps only the last two values `prev2, prev1`.
2. **Medium:** Write an in-place $O(1)$-auxiliary-space function `move_zeroes_to_end(nums: list[int]) -> None` that shifts all non-zero elements to the front while preserving their relative order.
3. **Hard:** Explain why standard Merge Sort requires $O(n)$ auxiliary space on arrays, whereas Quick Sort (using Lomuto/Hoare in-place partitioning and recursing on the smaller partition first) requires only $O(\log n)$ auxiliary stack space even in the worst case.

---

## 10. Interview Questions

### Q1: What is the auxiliary space complexity of naive recursive `fib(n)` (`return fib(n-1) + fib(n-2)`)?
**Answer:** **$O(n)$**, NOT $O(2^n)$! Even though $O(2^n)$ total calls are executed over time, the left branch `fib(n - 1)` unwinds and frees its stack frames before the right branch `fib(n - 2)` is called. At any single instant, the call stack is at most $n$ frames deep.

### Q2: Does Python support Tail Recursion Optimization (TCO)?
**Answer:** **No.** Guido van Rossum explicitly rejected TCO in Python because TCO destroys stack frames, which would corrupt tracebacks and dynamic frame inspection (`sys._getframe()`). Any linear recursion in Python costs $O(n)$ stack space; rewrite tail recursion as a `while` loop for $O(1)$ space.

### Q3: Does the output container returned by a function count toward Auxiliary Space?
**Answer:** By convention, if the problem specification **requires** returning a new structure of size $K$ (e.g., *"Return a list of all $N$ subsets"*), the required output container itself is often separated from the *working auxiliary space*, though you should always state both clearly in an interview: *"Excluding the required output array, working auxiliary space is $O(\dots)$; including the output, total space is $O(\dots)$."*
