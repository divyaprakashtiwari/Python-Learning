"""
Topic 03: Data Structures
Question 09: Stack and Queue with Lists (and collections.deque Deep Dive)

Master Stack (LIFO) and Queue (FIFO) data structures in Python:
- Basic stack operations with list.append and list.pop
- Performance analysis: list.pop(0) O(N) anti-pattern vs collections.deque O(1)
- Delimiter syntax validation (balanced brackets and quotes)
- Reverse Polish Notation (RPN) stack calculator
- Monotonic stack: Next Greater Element in O(N)
- Min-Stack with O(1) minimum element tracking
- Implementing a FIFO Queue using two LIFO Stacks (amortized O(1))
- Breadth-First Search (BFS) shortest path in a 2D maze
- Sliding Window Maximum using Monotonic Deque
- Production-grade Undo/Redo command manager with bounded history
"""

import time
from collections import deque
from typing import Any, List, Optional, Tuple


# ============================================================
# Q1: Basic LIFO Stack via List
# ============================================================
# Question: Implement a custom Stack class using a Python list. Provide push, pop,
# peek, is_empty, size, and raise a custom StackUnderflowError when popping an empty stack.

print("=== Q1: LIFO Stack via List ===")

class StackUnderflowError(IndexError):
    """Raised when attempting to pop or peek from an empty stack."""
    pass

class ListStack:
    def __init__(self):
        self._items: List[Any] = []

    def push(self, item: Any) -> None:
        self._items.append(item)

    def pop(self) -> Any:
        if not self._items:
            raise StackUnderflowError("Cannot pop from an empty stack")
        return self._items.pop()

    def peek(self) -> Any:
        if not self._items:
            raise StackUnderflowError("Cannot peek into an empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

stack = ListStack()
assert stack.is_empty()
stack.push("Alpha")
stack.push("Beta")
stack.push("Gamma")

print(f"  Top element (peek): {stack.peek()}")
print(f"  Popped:             {stack.pop()}")
print(f"  New top element:    {stack.peek()}")
print(f"  Current size:       {len(stack)}")

assert stack.pop() == "Beta"
assert stack.pop() == "Alpha"

# Test underflow error
caught = False
try:
    stack.pop()
except StackUnderflowError:
    caught = True
assert caught, "Popping an empty stack must raise StackUnderflowError!"
print("  StackUnderflowError correctly caught on empty pop.")

# Explanation: Python lists are dynamic arrays. Appending to and popping from the end
# are amortized O(1) operations, making `list` a great default stack.


# ============================================================
# Q2: The `list.pop(0)` Anti-Pattern vs `collections.deque`
# ============================================================
# Question: Benchmark and explain why using `list.pop(0)` for a FIFO queue is an O(N)
# anti-pattern, whereas `collections.deque.popleft()` is strictly O(1).

print("\n=== Q2: list.pop(0) vs collections.deque.popleft() ===")

N_ITEMS = 25_000

# 1. Benchmarking list.pop(0)
lst = list(range(N_ITEMS))
t0 = time.perf_counter()
while lst:
    lst.pop(0)  # Requires shifting all remaining elements left in contiguous memory!
t_list = time.perf_counter() - t0

# 2. Benchmarking deque.popleft()
dq = deque(range(N_ITEMS))
t0 = time.perf_counter()
while dq:
    dq.popleft()  # Doubly linked block list; unlinks in O(1) without shifts
t_deque = time.perf_counter() - t0

print(f"  Popping {N_ITEMS:,} items with list.pop(0):      {t_list:.4f} s")
print(f"  Popping {N_ITEMS:,} items with deque.popleft(): {t_deque:.4f} s")
print(f"  collections.deque was approx {t_list / max(t_deque, 1e-9):.1f}x faster!")

assert t_deque < t_list

# Explanation: `list.pop(0)` is O(N) because all remaining N-1 memory pointers
# must be shifted left in contiguous RAM. `collections.deque` is implemented as a
# doubly linked list of fixed-size memory blocks, allowing true O(1) appends and pops on both ends.


# ============================================================
# Q3: Balanced Parentheses & Delimiter Validator
# ============================================================
# Question: Use a stack to validate whether code brackets and delimiters
# `()`, `[]`, `{}` are properly opened and closed in the correct nesting order.

print("\n=== Q3: Balanced Delimiter Validator ===")

def is_balanced(code_snippet: str) -> bool:
    """Validates balanced nesting of (), [], and {}."""
    opening = "({["
    closing = ")}]"
    matches = {")": "(", "}": "{", "]": "["}
    stack: List[str] = []

    for char in code_snippet:
        if char in opening:
            stack.append(char)
        elif char in closing:
            if not stack or stack[-1] != matches[char]:
                return False
            stack.pop()
            
    return len(stack) == 0

valid_cases = [
    "def foo(x): return [x * 2 for x in {1, 2, 3}]",
    "{[()]}",
    "()[]{}"
]

invalid_cases = [
    "def bar(x: return [x",
    "([)]",  # Interleaved / incorrect nesting
    "((())",  # Unclosed opening
    "())"     # Extra closing
]

for s in valid_cases:
    print(f"  Valid:   '{s[:30]}...' -> {is_balanced(s)}")
    assert is_balanced(s) is True

for s in invalid_cases:
    print(f"  Invalid: '{s}' -> {is_balanced(s)}")
    assert is_balanced(s) is False

# Explanation: The most recently opened bracket must be the first one closed (LIFO).
# A stack accurately tracks open brackets and verifies each matching closure.


# ============================================================
# Q4: Reverse Polish Notation (RPN) Postfix Evaluator
# ============================================================
# Question: Implement an expression evaluator for Postfix / Reverse Polish Notation.
# Support operators `+`, `-`, `*`, `/` (integer division truncating toward zero).

print("\n=== Q4: Postfix (RPN) Evaluator ===")

def eval_rpn(tokens: List[str]) -> int:
    """Evaluates Reverse Polish Notation tokens using an operand stack."""
    stack: List[int] = []

    for token in tokens:
        if token in {"+", "-", "*", "/"}:
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            elif token == "/":
                # Integer division truncating toward zero (same as int(a / b))
                stack.append(int(a / b))
        else:
            stack.append(int(token))

    return stack.pop()

# Example: (2 + 1) * 3 = 9
rpn_1 = ["2", "1", "+", "3", "*"]
res_1 = eval_rpn(rpn_1)
print(f"  RPN {rpn_1} -> {res_1}")
assert res_1 == 9

# Example: 4 + (13 / 5) = 6
rpn_2 = ["4", "13", "5", "/", "+"]
res_2 = eval_rpn(rpn_2)
print(f"  RPN {rpn_2} -> {res_2}")
assert res_2 == 6

# Example: ((10 * (6 / ((9 + 3) * -11))) + 17) + 5
rpn_3 = ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]
res_3 = eval_rpn(rpn_3)
print(f"  RPN complex -> {res_3}")
assert res_3 == 22

# Explanation: In postfix notation, operands precede their operator. When an
# operator is encountered, the top two operands are popped and the result pushed back.


# ============================================================
# Q5: Monotonic Stack: Next Greater Element (NGE)
# ============================================================
# Question: Given an array of integers, find the next greater element for each item
# in O(N) time. If no greater element exists to the right, output -1.

print("\n=== Q5: Monotonic Stack (Next Greater Element) ===")

def next_greater_elements(nums: List[int]) -> List[int]:
    """Finds next greater element for each index in O(N) using monotonic stack."""
    n = len(nums)
    result = [-1] * n
    # Stack stores indices of elements whose next greater has not yet been found
    stack: List[int] = []

    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            prev_idx = stack.pop()
            result[prev_idx] = nums[i]
        stack.append(i)

    return result

sample_arr = [4, 5, 2, 25, 7, 18]
nge_result = next_greater_elements(sample_arr)

print(f"  Input array:        {sample_arr}")
print(f"  Next greater array: {nge_result}")

assert nge_result == [5, 25, 25, -1, 18, -1]

# Explanation: A monotonic decreasing stack stores indices. When a larger number
# appears, it resolves all smaller pending elements currently on top of the stack in O(N) total time.


# ============================================================
# Q6: Min-Stack with O(1) Minimum Tracking
# ============================================================
# Question: Design a stack that supports push, pop, top, and retrieving the minimum
# element in constant O(1) time.

print("\n=== Q6: Min-Stack with O(1) get_min ===")

class MinStack:
    def __init__(self):
        # Store tuples of (value, current_min)
        self._stack: List[Tuple[int, int]] = []

    def push(self, val: int) -> None:
        if not self._stack:
            self._stack.append((val, val))
        else:
            curr_min = min(val, self._stack[-1][1])
            self._stack.append((val, curr_min))

    def pop(self) -> int:
        if not self._stack:
            raise IndexError("pop from empty MinStack")
        return self._stack.pop()[0]

    def top(self) -> int:
        if not self._stack:
            raise IndexError("top from empty MinStack")
        return self._stack[-1][0]

    def get_min(self) -> int:
        if not self._stack:
            raise IndexError("get_min from empty MinStack")
        return self._stack[-1][1]

min_stack = MinStack()
min_stack.push(10)
min_stack.push(20)
min_stack.push(5)
min_stack.push(15)

print(f"  Current Top: {min_stack.top()}, Current Min: {min_stack.get_min()}")
assert min_stack.get_min() == 5

# Pop 15 and 5
min_stack.pop()
popped_5 = min_stack.pop()
assert popped_5 == 5
print(f"  After popping 15 and 5 -> Top: {min_stack.top()}, New Min: {min_stack.get_min()}")
assert min_stack.get_min() == 10

# Explanation: By pairing each pushed element with the minimum element observed up
# to that point, popping automatically restores the previous minimum in O(1) time.


# ============================================================
# Q7: FIFO Queue Implemented via Two Stacks
# ============================================================
# Question: Implement a FIFO Queue using only two LIFO stacks (`in_stack` and `out_stack`).
# Demonstrate amortized O(1) enqueue and dequeue operations.

print("\n=== Q7: Two-Stack FIFO Queue ===")

class TwoStackQueue:
    def __init__(self):
        self._in_stack: List[Any] = []
        self._out_stack: List[Any] = []

    def enqueue(self, item: Any) -> None:
        """Enqueue is strictly O(1)."""
        self._in_stack.append(item)

    def _shift_stacks(self) -> None:
        """Transfer elements only when out_stack is completely empty."""
        if not self._out_stack:
            while self._in_stack:
                self._out_stack.append(self._in_stack.pop())

    def dequeue(self) -> Any:
        """Dequeue is amortized O(1)."""
        self._shift_stacks()
        if not self._out_stack:
            raise IndexError("dequeue from empty Queue")
        return self._out_stack.pop()

    def peek(self) -> Any:
        self._shift_stacks()
        if not self._out_stack:
            raise IndexError("peek into empty Queue")
        return self._out_stack[-1]

    def is_empty(self) -> bool:
        return not self._in_stack and not self._out_stack

q = TwoStackQueue()
for val in [100, 200, 300]:
    q.enqueue(val)

print(f"  Front element (peek): {q.peek()}")
print(f"  Dequeued: {q.dequeue()}")
q.enqueue(400)
print(f"  Dequeued: {q.dequeue()}")
print(f"  Dequeued: {q.dequeue()}")
print(f"  Dequeued: {q.dequeue()}")

assert q.is_empty()

# Explanation: Each element is pushed to `in_stack` once, transferred to `out_stack`
# once, and popped once. Total work per element is O(1) amortized.


# ============================================================
# Q8: Breadth-First Search (BFS) Shortest Path via Deque
# ============================================================
# Question: Find the shortest path length from Start (0, 0) to Goal in a 2D binary
# grid where 0 is walkable and 1 is a wall. Use a queue (FIFO BFS).

print("\n=== Q8: BFS Shortest Path with FIFO Queue ===")

def shortest_maze_path(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    """Computes shortest step distance using BFS queue."""
    rows, cols = len(grid), len(grid[0])
    if grid[start[0]][start[1]] == 1 or grid[end[0]][end[1]] == 1:
        return -1

    queue = deque([(start[0], start[1], 0)])  # (row, col, distance)
    visited = {start}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    while queue:
        r, c, dist = queue.popleft()
        if (r, c) == end:
            return dist

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, dist + 1))

    return -1  # Unreachable

maze = [
    [0, 0, 0, 0],
    [1, 1, 0, 1],
    [0, 0, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 0]
]

start_pt = (0, 0)
goal_pt = (4, 3)
steps = shortest_maze_path(maze, start_pt, goal_pt)

print(f"  Shortest path from {start_pt} to {goal_pt}: {steps} steps")
assert steps == 7

# Explanation: A FIFO queue explores cells in order of increasing distance.
# The first time the destination cell is popped from the queue, its distance is optimal.


# ============================================================
# Q9: Sliding Window Maximum using Monotonic Deque
# ============================================================
# Question: Given an array of integers and window size k, find the maximum element
# in each sliding window in O(N) time using a double-ended queue.

print("\n=== Q9: Sliding Window Maximum via Monotonic Deque ===")

def max_sliding_window(nums: List[int], k: int) -> List[int]:
    """Finds maximum in every sliding window of size k in O(N) time."""
    if not nums or k == 0:
        return []

    dq = deque()  # Stores indices of elements, maintaining values in descending order
    result = []

    for i, val in enumerate(nums):
        # 1. Remove indices that fell outside the current window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # 2. Maintain monotonic decreasing order: pop elements smaller than current
        while dq and nums[dq[-1]] < val:
            dq.pop()

        dq.append(i)

        # 3. Append the front of deque (maximum in window) once window reaches size k
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result

test_nums = [1, 3, -1, -3, 5, 3, 6, 7]
w_size = 3
window_maxima = max_sliding_window(test_nums, w_size)

print(f"  Array: {test_nums}, Window size: {w_size}")
print(f"  Sliding window maxima: {window_maxima}")

assert window_maxima == [3, 3, 5, 5, 6, 7]

# Explanation: A monotonic deque keeps indices of potential candidates. Because each
# index is pushed and popped at most once, total time complexity is strictly O(N).


# ============================================================
# Q10: Production-Grade Undo/Redo Engine with Bounded History
# ============================================================
# Question: Implement an Undo/Redo command manager for a text editor with a bounded
# history capacity. Support executing edits, undoing, redoing, and inspect history state.

print("\n=== Q10: Bounded Undo/Redo Command Manager ===")

class TextEditorManager:
    def __init__(self, max_history: int = 5):
        self.text: str = ""
        # Undo stack holds previous text snapshots
        self._undo_stack: deque = deque(maxlen=max_history)
        # Redo stack holds snapshots undone
        self._redo_stack: deque = deque(maxlen=max_history)

    def write(self, new_text: str) -> None:
        """Appends new text and records previous snapshot."""
        self._undo_stack.append(self.text)
        self._redo_stack.clear()  # New write invalidates redo history
        self.text += new_text

    def undo(self) -> bool:
        """Reverts to the latest snapshot from undo stack."""
        if not self._undo_stack:
            return False
        self._redo_stack.append(self.text)
        self.text = self._undo_stack.pop()
        return True

    def redo(self) -> bool:
        """Re-applies the most recently undone edit."""
        if not self._redo_stack:
            return False
        self._undo_stack.append(self.text)
        self.text = self._redo_stack.pop()
        return True

editor = TextEditorManager(max_history=5)
editor.write("Hello")
editor.write(" World")
editor.write("!")

print(f"  Initial Text:        '{editor.text}'")
assert editor.text == "Hello World!"

editor.undo()
print(f"  After 1 Undo:        '{editor.text}'")
assert editor.text == "Hello World"

editor.undo()
print(f"  After 2nd Undo:      '{editor.text}'")
assert editor.text == "Hello"

editor.redo()
print(f"  After Redo:          '{editor.text}'")
assert editor.text == "Hello World"

editor.write(" Python")
print(f"  After new write:     '{editor.text}'")
assert editor.text == "Hello World Python"
assert not editor.redo(), "Redo should be invalid after a new write action!"

print("\nAll 10 stack and queue questions executed and asserted successfully!")
