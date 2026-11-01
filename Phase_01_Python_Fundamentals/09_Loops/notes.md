# Topic 09: Loops (`for`, `while`)

---

## 1. Introduction

A **Loop** is a control structure that repeats a block of code multiple times without forcing you to copy and paste the same statement over and over.

Python provides two types of loops:
1. **`for` Loop (Definite Iteration):** Iterates directly over the items of any sequence or iterable (`range`, `list`, `str`, `tuple`, `dict`, `set`). Use `for` when you know the collection or number of iterations ahead of time.
2. **`while` Loop (Indefinite / Condition-Controlled Iteration):** Repeats a block of code as long as a boolean condition remains `True`. Use `while` when the number of iterations depends on a dynamic condition (such as Two Pointers `while left < right:`, Binary Search `while low <= high:`, or extracting digits `while n > 0:`).

---

## 2. Why is it used?

Loops are essential across every domain of software engineering and DSA:
1. **Batch Processing:** Iterating over thousands of customer orders, log lines, or database rows.
2. **Matrix & Grid Traversal:** Nested `for` loops visit every `(row, col)` cell in a 2D array or image grid.
3. **Core DSA Paradigms:** Sliding Window, Two Pointers, Binary Search, BFS Queue processing (`while queue:`), and Dynamic Programming tabulation all rely on `for` and `while` loops.

---

## 3. Syntax

```python
# 1. for loop with range(start, stop, step)
for i in range(1, 6):
    print(i)  # Prints 1, 2, 3, 4, 5

# 2. for loop with enumerate() for index + value
for index, item in enumerate(["a", "b", "c"], start=0):
    print(index, item)

# 3. while loop
count = 3
while count > 0:
    print(count)
    count -= 1  # Crucial: update state so loop terminates!
```

---

## 4. Explanation (How `range()` and Loops Work Step by Step)

1. **How `range(start, stop, step)` Works:**
   - `range(5)` produces `0, 1, 2, 3, 4` (`start` defaults to `0`, `step` defaults to `1`, and **`stop` is always exclusive**).
   - `range(2, 10, 2)` produces `2, 4, 6, 8`.
   - `range(5, 0, -1)` counts backward: `5, 4, 3, 2, 1`.
   - **Memory Efficiency:** `range(1_000_000_000)` does **not** allocate a billion integers in RAM; it computes the next integer lazily in `O(1)` memory.
2. **How a `while` Loop Executes:**
   - Before each iteration, Python evaluates the condition (`while remaining > 0:`).
   - If `True`, the loop body executes, and then Python jumps back to re-test the condition.
   - If `False`, the loop exits immediately and execution continues on the first unindented line below the loop.

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_print_numbers.py`](example_01_print_numbers.py)
- [`example_02_multiplication_table.py`](example_02_multiplication_table.py)
- [`example_03_sum_of_numbers.py`](example_03_sum_of_numbers.py)

### Example 1: Printing Number Sequences (`example_01_print_numbers.py`)

```python
def main() -> None:
    print("=== 1. Numbers 1 to 10 using range(1, 11) ===")
    for num in range(1, 11):
        print(num, end=" ")
    print()

    print("\n=== 2. Even Numbers 2 to 20 using range(2, 21, 2) ===")
    evens = [n for n in range(2, 21, 2)]
    print(evens)

    print("\n=== 3. Countdown using range(5, 0, -1) ===")
    for sec in range(5, 0, -1):
        print(f"T-minus {sec}...", end=" ")
    print("Liftoff!")

    print("\n=== 4. Indexed Iteration with enumerate() ===")
    milestones = ["Variables", "Data Types", "Conditionals", "Loops"]
    for step_no, topic in enumerate(milestones, start=1):
        print(f"  Milestone #{step_no}: {topic}")


if __name__ == "__main__":
    main()
```

### Example 2: Multiplication Table Generator (`example_02_multiplication_table.py`)

```python
def print_single_table(number: int, limit: int = 10) -> None:
    print(f"=== Multiplication Table of {number} ===")
    for multiplier in range(1, limit + 1):
        product = number * multiplier
        print(f"  {number:>2} x {multiplier:>2} = {product:>3}")


def print_multiplication_grid(size: int = 5) -> None:
    print(f"\n=== {size}x{size} Nested Loop Multiplication Grid ===")
    header = "    | " + " ".join(f"{col:>3}" for col in range(1, size + 1))
    print(header)
    print("-" * len(header))
    for row in range(1, size + 1):
        row_cells = " ".join(f"{row * col:>3}" for col in range(1, size + 1))
        print(f" {row:>2} | {row_cells}")


def main() -> None:
    print_single_table(7, limit=10)
    print_multiplication_grid(size=5)


if __name__ == "__main__":
    main()
```

### Example 3: Summing Numbers (`for` Accumulator vs `while` Digit Extraction) (`example_03_sum_of_numbers.py`)

```python
def sum_first_n_numbers(n: int) -> int:
    """Compute 1 + 2 + ... + n using an explicit for-loop accumulator."""
    total = 0
    for current in range(1, n + 1):
        total += current
    return total


def sum_of_digits(number: int) -> int:
    """Extract and sum all digits of a non-negative integer using a while loop."""
    remaining = abs(number)
    digit_sum = 0
    while remaining > 0:
        last_digit = remaining % 10
        digit_sum += last_digit
        remaining //= 10
    return digit_sum


def main() -> None:
    n = 100
    loop_sum = sum_first_n_numbers(n)
    formula_sum = n * (n + 1) // 2
    print("=== 1. Sum of First N Natural Numbers ===")
    print(f"Sum of 1..{n} (for loop)      : {loop_sum}")
    print(f"Sum of 1..{n} (Gauss formula) : {formula_sum}")

    print("\n=== 2. Sum of Digits using a while Loop ===")
    for sample in [9875, 2026, 100001]:
        print(f"  Number: {sample:>6} -> Sum of digits: {sum_of_digits(sample)}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== 1. Numbers 1 to 10 using range(1, 11) ===
1 2 3 4 5 6 7 8 9 10 

=== 2. Even Numbers 2 to 20 using range(2, 21, 2) ===
[2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

=== 3. Countdown using range(5, 0, -1) ===
T-minus 5... T-minus 4... T-minus 3... T-minus 2... T-minus 1... Liftoff!

=== 4. Indexed Iteration with enumerate() ===
  Milestone #1: Variables
  Milestone #2: Data Types
  Milestone #3: Conditionals
  Milestone #4: Loops
```

### Output for Example 2:
```text
=== Multiplication Table of 7 ===
   7 x  1 =   7
   7 x  2 =  14
   7 x  3 =  21
   7 x  4 =  28
   7 x  5 =  35
   7 x  6 =  42
   7 x  7 =  49
   7 x  8 =  56
   7 x  9 =  63
   7 x 10 =  70

=== 5x5 Nested Loop Multiplication Grid ===
    |   1   2   3   4   5
-------------------------
  1 |   1   2   3   4   5
  2 |   2   4   6   8  10
  3 |   3   6   9  12  15
  4 |   4   8  12  16  20
  5 |   5  10  15  20  25
```

### Output for Example 3:
```text
=== 1. Sum of First N Natural Numbers ===
Sum of 1..100 (for loop)      : 5050
Sum of 1..100 (Gauss formula) : 5050

=== 2. Sum of Digits using a while Loop ===
  Number:   9875 -> Sum of digits: 29
  Number:   2026 -> Sum of digits: 10
  Number: 100001 -> Sum of digits: 2
```

---

## 7. Code Explanation

- **`range(1, 11)`** — Because the `stop` value is exclusive, `range(1, 11)` stops right before `11`, yielding `1` through `10`.
- **`enumerate(milestones, start=1)`** — Yields `(index, element)` pairs so you never need the anti-pattern `for i in range(len(milestones)):`.
- **`last_digit = remaining % 10` and `remaining //= 10`** — The universal arithmetic idiom for peeling off digits of a base-10 integer from right to left in `O(log10(N))` iterations.

---

## 8. Common Mistakes

1. **Off-by-One Errors in `range()`:**
   Writing `range(1, 10)` when you want `1` to `10` inclusive only iterates up to `9`. Always write `range(1, n + 1)` for `1..n` inclusive.
2. **Infinite `while` Loops:**
   Forgetting to update the loop variable inside a `while` loop (`remaining //= 10` or `i += 1`) causes the condition to stay `True` forever, freezing the program.
3. **Mutating a List While Iterating Over It:**
   ```python
   # WRONG: Removing items shifts elements left, causing the loop to skip adjacent items!
   for x in nums:
       if x % 2 == 0:
           nums.remove(x)
   # CORRECT: Build a filtered list comprehension or iterate over a copy nums[:]
   nums = [x for x in nums if x % 2 != 0]
   ```

---

## 9. Practice Questions

1. **Easy:** Write a `for` loop that calculates the factorial of a non-negative integer `n` (`n! = 1 * 2 * ... * n`, with `0! = 1`).
2. **Medium:** Write a `while` loop that reverses an integer `n` mathematically (e.g., `1234 -> 4321`) without converting it to a string (`rev = rev * 10 + n % 10`).
3. **Hard:** Write a function `collatz_steps(n: int) -> list[int]` using a `while` loop that generates the Collatz sequence starting at `n` until it reaches `1` (if `n` is even, `n = n // 2`; if `n` is odd, `n = 3 * n + 1`).

---

## 10. Interview Questions

### Q1: Why is `range(10**9)` instantaneous and memory-safe in Python 3?
**Answer:** In Python 3, `range` is an immutable **lazy sequence object** (like `xrange` in Python 2). It only stores three integers in memory—`start`, `stop`, and `step`—and computes elements on the fly during iteration or indexing in `O(1)` space.

### Q2: Why is `for item in collection:` preferred over `for i in range(len(collection)):`?
**Answer:** Iterating directly over `collection` (or using `enumerate(collection)` when the index is needed) uses Python's Iterator Protocol directly, avoids redundant `len()` and `__getitem__` index lookups on every step, and works on any iterable (including `set`s, `dict`s, files, and generators that do not support indexing).

### Q3: What is the time complexity of extracting all digits of a positive integer `N` using `while N > 0: N //= 10`?
**Answer:** Each iteration divides `N` by `10`, so the loop runs `floor(log10(N)) + 1` times. The time complexity is **`O(log10(N))`** (or `O(d)` where `d` is the number of digits) and space complexity is **`O(1)`**.
