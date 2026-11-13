# Stack Implementation (Array vs Linked Stack, $O(1)$ `MinStack` & Shunting-Yard RPN)

---

## 1. Introduction

A **Stack** is a linear **Last-In, First-Out (LIFO)** abstract data type in which all insertions (`push`) and removals (`pop`) take place at a single end called the **top**:

$$\text{Bottom } [10, \; 20, \; 30, \; 40] \leftarrow \text{Top (`push(50)` / `pop() -> 40`)}$$

Every core Stack operation runs in **$O(1)$ time**:
- **`push(x)`**: Place element `x` on top of the stack.
- **`pop()`**: Remove and return the top element (raises `IndexError` on an empty stack).
- **`peek()` / `top()`**: Read the top element without removing it.
- **`is_empty()` / `__len__()`**: Check whether the stack has 0 elements.

---

## 2. Why is it used?

1. **Function Call Stack & Recursion Simulation:** Every CPU thread maintains a hardware/runtime call stack storing local variables and return addresses. Any recursive algorithm (DFS, tree traversals, Quick Sort) can be converted into an iterative algorithm using an explicit stack to avoid `RecursionError`.
2. **Undo / Redo History & Backtracking:** Text editors, graphics suites, and state-space search engines push state snapshots onto an undo stack and pop them when backtracking.
3. **Syntax Parsing, Compilers & Calculators:** Validating nested parentheses/HTML tags (LeetCode 20), converting infix expressions into postfix via **Dijkstra's Shunting-Yard Algorithm**, and evaluating **Reverse Polish Notation (RPN)** bytecode instructions (LeetCode 150) — including CPython's own stack-based bytecode virtual machine!
4. **$O(1)$ Aggregate Queries (`MinStack` / `MaxStack`):** Maintaining running minimums or maximums alongside stack operations in $O(1)$ worst-case time (LeetCode 155).

---

## 3. Syntax

### A. Idiomatic Python Stack Using a Built-in `list`
```python
stack: list[int] = []
stack.append(10)        # push(10)  -> amortized O(1)
stack.append(20)        # push(20)  -> amortized O(1)
top_val = stack[-1]     # peek()    -> O(1)
popped = stack.pop()    # pop()     -> amortized O(1)
```

### B. Paired Tuple `MinStack` ($O(1)$ Time for `push`, `pop`, `top`, `get_min`)
```python
class MinStack:
    def __init__(self) -> None:
        self._stack: list[tuple[int, int]] = []  # (val, min_so_far)

    def push(self, val: int) -> None:
        cur_min = val if not self._stack else min(val, self._stack[-1][1])
        self._stack.append((val, cur_min))

    def pop(self) -> int:
        return self._stack.pop()[0]

    def get_min(self) -> int:
        return self._stack[-1][1]
```

---

## 4. Explanation (Step-by-Step)

### 1. Dynamic Array Stack (`list`) vs Linked List Stack (`_StackNode`)

| Property | `ArrayStack` (`list`) | `LinkedStack` (`_StackNode`) |
| :--- | :--- | :--- |
| **`push(x)` Time** | Amortized $O(1)$ (occasional $O(n)$ resize) | Strict worst-case $O(1)$ |
| **`pop()` Time** | Amortized $O(1)$ | Strict worst-case $O(1)$ |
| **Memory Locality** | Contiguous array (CPU L1/L2 cache-friendly) | Scattered heap nodes (pointer chasing) |
| **Per-Element Overhead** | ~8 bytes per pointer slot | ~48+ bytes per node object |

In Python, `list` (`append` / `pop`) is almost always faster than a custom linked-list stack due to contiguous C-array cache locality.

### 2. How Single-Stack Mathematical Delta `MinStack` Achieves $O(1)$ Extra Space
Suppose the current minimum is $\text{min\_val}$ and we push a new strictly smaller value $x < \text{min\_val}$:
- Instead of pushing $x$ directly, we push the encoded sentinel:
  $$\text{encoded} = 2x - \text{min\_val}$$
  and update $\text{min\_val} = x$.
- Why is $\text{encoded}$ guaranteed to act as a recognizable flag when popping later?
  Because $x < \text{old\_min\_val} \implies x - \text{old\_min\_val} < 0 \implies 2x - \text{old\_min\_val} < x = \text{new\_min\_val}$!
- Thus, whenever the top of the stack is **strictly less than `self._min_val`**, we know it is an encoded sentinel! The true value at that position is `self._min_val`, and when popping it we recover the previous minimum via:
  $$\text{old\_min\_val} = 2 \cdot \text{new\_min\_val} - \text{encoded}$$

---

## 5. Minimum 3 Examples

### Example 1: Array-Backed Stack (`list`) vs Pointer-Backed Linked Stack (`_StackNode`)
File: [`example_01_array_and_linked_list_stack.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/F_Stacks_and_Queues/01_Stack_Implementation/example_01_array_and_linked_list_stack.py)

```python
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class ArrayStack(Generic[T]):
    """LIFO Stack backed by a dynamic array (Python list)."""

    def __init__(self) -> None:
        self._data: List[T] = []

    def push(self, item: T) -> None:
        self._data.append(item)

    def pop(self) -> T:
        if not self._data:
            raise IndexError("pop from an empty ArrayStack")
        return self._data.pop()

    def peek(self) -> T:
        if not self._data:
            raise IndexError("peek from an empty ArrayStack")
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)

    def to_list_top_down(self) -> List[T]:
        return list(reversed(self._data))
```

---

### Example 2: `MinStack` — Paired Tuple Stack vs Single-Stack Mathematical Delta
File: [`example_02_min_stack_o1_time_and_space.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/F_Stacks_and_Queues/01_Stack_Implementation/example_02_min_stack_o1_time_and_space.py)

```python
class DeltaEncodedMinStack:
    """
    Stores a single integer per entry using `2*val - prev_min` encoding whenever a
    new minimum arrives, achieving O(1) auxiliary memory overhead.
    """

    def __init__(self) -> None:
        self._stack: List[int] = []
        self._min_val: int = 0

    def push(self, val: int) -> None:
        if not self._stack:
            self._stack.append(val)
            self._min_val = val
        elif val >= self._min_val:
            self._stack.append(val)
        else:
            encoded = 2 * val - self._min_val
            self._stack.append(encoded)
            self._min_val = val

    def pop(self) -> int:
        if not self._stack:
            raise IndexError("pop from empty DeltaEncodedMinStack")
        raw_top = self._stack.pop()
        if raw_top >= self._min_val:
            return raw_top
        else:
            actual_val = self._min_val
            self._min_val = 2 * self._min_val - raw_top
            return actual_val
```

---

### Example 3: Balanced Brackets Validator, Shunting-Yard & RPN Evaluator
File: [`example_03_balanced_brackets_and_rpn_calculator.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/F_Stacks_and_Queues/01_Stack_Implementation/example_03_balanced_brackets_and_rpn_calculator.py)

```python
def is_valid_parentheses(s: str) -> bool:
    matching_open: Dict[str, str] = {")": "(", "]": "[", "}": "{"}
    stack: List[str] = []

    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in matching_open:
            if not stack or stack.pop() != matching_open[ch]:
                return False
    return len(stack) == 0


def eval_rpn(tokens: List[str]) -> int:
    stack: List[int] = []
    for token in tokens:
        if token in {"+", "-", "*", "/"}:
            right = stack.pop()
            left = stack.pop()
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            elif token == "*":
                stack.append(left * right)
            else:
                stack.append(int(left / right))
        else:
            stack.append(int(token))
    return stack[0]
```

---

## 6. Output

### Output — Example 1 (`example_01_array_and_linked_list_stack.py`)
```text
========================================================================
ArrayStack (`list`) vs LinkedStack (`_StackNode`) LIFO Verification
========================================================================
After pushing 4 call frames:
  ArrayStack  (top -> bottom): ['query_db()', 'validate_token()', 'parse_request()', 'main()']
  LinkedStack (top -> bottom): ['query_db()', 'validate_token()', 'parse_request()', 'main()']
  Current Top (`peek()`)     : query_db() == query_db()

Unwinding call stack via `pop()`:
  Popped frame: query_db()         | Remaining depth: 3
  Popped frame: validate_token()   | Remaining depth: 2
  Popped frame: parse_request()    | Remaining depth: 1
  Popped frame: main()             | Remaining depth: 0
```

### Output — Example 2 (`example_02_min_stack_o1_time_and_space.py`)
```text
========================================================================
MinStack O(1) `get_min()`: Paired Tuple Stack vs Single-Stack Delta
========================================================================
Pushing stream: [10, 5, 8, 2, 12, -3, 4]
  push(10) -> top = 10, get_min() = 10
  push( 5) -> top =  5, get_min() =  5
  push( 8) -> top =  8, get_min() =  5
  push( 2) -> top =  2, get_min() =  2
  push(12) -> top = 12, get_min() =  2
  push(-3) -> top = -3, get_min() = -3
  push( 4) -> top =  4, get_min() = -3

Popping elements one by one:
  pop() ->  4 | new top = -3, new get_min() = -3
  pop() -> -3 | new top = 12, new get_min() =  2
  pop() -> 12 | new top =  2, new get_min() =  2
  pop() ->  2 | new top =  8, new get_min() =  5
  pop() ->  8 | new top =  5, new get_min() =  5
  pop() ->  5 | new top = 10, new get_min() = 10
```

### Output — Example 3 (`example_03_balanced_brackets_and_rpn_calculator.py`)
```text
========================================================================
1. Balanced Brackets Validator (LeetCode 20)
========================================================================
  {[()()]}     -> Valid: True
  ([)]         -> Valid: False
  ((()         -> Valid: False
  {[]}()       -> Valid: True

========================================================================
2. Infix -> Postfix (Shunting-Yard) & RPN Evaluation (LeetCode 150)
========================================================================
Infix  : 3 + 4 * ( 2 - 5 )
Postfix: ['3', '4', '2', '5', '-', '*', '+']
Result : -9

Infix  : 10 + 6 / ( 9 - 3 ) * -11 + 17 + 5
Postfix: ['10', '6', '9', '3', '-', '/', '-11', '*', '+', '17', '+', '5', '+']
Result : 21
```

---

## 7. Code Explanation

1. **Why Operand Order Matters When Popping in `eval_rpn` (`right = stack.pop(); left = stack.pop()`):**
   In a binary expression `left - right` or `left / right`, `left` was pushed **first** and `right` was pushed **second** (so `right` sits on top of the stack). Popping `right` first and `left` second ensures non-commutative operations (`-` and `/`) are evaluated in the right order!
2. **Why `int(left / right)` is Used Instead of `left // right` in `eval_rpn`:**
   Python's floor division `//` rounds toward $-\infty$ (`6 // -132 == -1`), whereas C/Java/LeetCode integer division truncates toward $0$ (`int(6 / -132) == 0`).

---

## 8. Common Mistakes

1. **Using `list.insert(0, x)` and `list.pop(0)` as a Stack Top:**
   Inserting or popping at index `0` of a Python `list` shifts all $n$ elements in memory, degrading every stack operation from **$O(1)$ to $O(n)$**! Always use the **right end** (`list.append(x)` and `list.pop()`) as the top of the stack.
2. **Returning `True` in `is_valid_parentheses` Without Checking `len(stack) == 0`:**
   On an input with unclosed opening brackets like `"((()"`, the loop finishes without a mismatch, so you must verify that the stack is empty at the end.
3. **Only Maintaining a Single `min_val` Variable Without History in `MinStack`:**
   If you only track `self.min_val = min(self.min_val, x)`, what happens when the minimum element is popped? Without either paired tuples, a shadow min-stack, or `2*val - prev_min` delta encoding, recomputing the minimum after `pop()` degrades to $O(n)$.

---

## 9. Practice Questions

1. **Easy — Simplify Unix File Path (LeetCode 71):**
   Given an absolute Unix path string (e.g., `"/home/user/Documents/../Pictures/./a.png"`), split by `"/"` and use a stack to process `".."` (pop directory) and `"."` (no-op) to return the canonical path `"/home/user/Pictures/a.png"`.
2. **Medium — Decode String (LeetCode 394):**
   Given an encoded string like `"3[a2[c]]"`, use a stack of `(prev_string, repeat_count)` pairs to decode it into `"accaccacc"` in $O(n)$ time.
3. **Hard — Basic Calculator with Parentheses, `+`, `-`, and Unary Negation (LeetCode 224):**
   Evaluate a mathematical string expression containing `(`, `)`, `+`, `-`, spaces, and multi-digit integers in a single $O(n)$ pass using a sign-and-accumulator stack.

---

## 10. Interview Questions

### Q1: In a 2-stack `MinStack` (one main stack and one auxiliary `min_stack` that only pushes when `val <= min_stack[-1]`), why must the condition be `val <= min_stack[-1]` and not `val < min_stack[-1]`?
**Answer:** If duplicate minimum values are pushed (e.g., pushing `2`, `5`, `2`) and you only push strictly smaller values onto `min_stack`, then `min_stack` contains only a single `2`. When the top `2` is popped from the main stack and popped from `min_stack`, `min_stack` loses `2` even though the first `2` is still inside the main stack! Using `<=` preserves duplicate minimums accurately.

### Q2: Does the `2*val - prev_min` delta-encoding trick have any drawback in languages with fixed-width 32-bit/64-bit integers (C++, Java, Rust)?
**Answer:** Yes — `2 * val - prev_min` can cause **signed integer overflow** when `val = INT_MIN` and `prev_min = INT_MAX` unless you widen the stack storage type (e.g., `long long` in C++). In Python, `int` has arbitrary precision, so `2 * val - prev_min` never overflows!

### Q3: How does Python's `collections.deque` compare to `list` when used purely as a LIFO Stack?
**Answer:** Both support $O(1)$ `append()` and `pop()`. `list` uses a single contiguous array of object pointers (faster random access and slightly better cache locality when no reallocation occurs), whereas `collections.deque` is a doubly linked list of 64-element blocks (strict worst-case $O(1)$ with zero reallocation spikes).

