"""
Topic 04: Functions
Question 06: Recursion (Deep Dive)

Master recursive algorithms and the call stack in Python:
- Base case vs recursive case mechanics and call stack frame visualization
- sys.getrecursionlimit() and handling RecursionError
- The Tail Call Optimization (TCO) reality in Python & accumulator refactoring
- Tree recursion & memoization optimization with functools.lru_cache
- Arbitrarily nested list flattening (heterogeneous elements)
- Recursive binary search: pointer-based O(log N) vs slice-copy anti-pattern
- Backtracking recursion: generating string permutations
- Tower of Hanoi recursive solver with step verification (2^N - 1 moves)
- Virtual file-system directory tree traversal and disk quota calculator
- Recursive descent mathematical expression parser (grammar evaluator)
"""

import functools
import sys
from typing import Any, Dict, List, Optional, Tuple, Union


# ============================================================
# Q1: Base Case, Recursive Case, and Call Stack Anatomy
# ============================================================
# Question: Implement factorial recursively with call stack tracing.
# Explain the fundamental rule: every recursive function must have at least one base case
# that terminates recursion and a recursive step that progresses toward the base case.

print("=== Q1: Base Case and Call Stack Anatomy ===")

call_depth_trace: List[str] = []

def factorial_traced(n: int, depth: int = 0) -> int:
    indent = "  " * depth
    call_depth_trace.append(f"{indent}-> factorial({n})")
    
    # Base Case: stop recursion when n <= 1
    if n <= 1:
        call_depth_trace.append(f"{indent}<- base case reached: returning 1")
        return 1

    # Recursive Case: n * factorial(n - 1)
    sub_result = factorial_traced(n - 1, depth + 1)
    result = n * sub_result
    call_depth_trace.append(f"{indent}<- factorial({n}) returning {result}")
    return result

fact_5 = factorial_traced(5)
print(f"  5! = {fact_5}")
print("  Call stack unwinding sequence (first 6 events):")
for event in call_depth_trace[:6]:
    print(f"    {event}")

assert fact_5 == 120
assert "-> factorial(5)" in call_depth_trace[0]

# Explanation: Each recursive call pushes a new frame onto Python's execution call stack.
# When the base case returns, stack frames unwind in reverse (LIFO) order.


# ============================================================
# Q2: Recursion Limits and RecursionError Handling
# ============================================================
# Question: Inspect Python's default recursion limit via `sys.getrecursionlimit()`.
# Demonstrate that infinite recursion raises `RecursionError` rather than crashing the OS.

print("\n=== Q2: RecursionLimit & RecursionError ===")

current_limit = sys.getrecursionlimit()
print(f"  Current Python recursion limit: {current_limit} frames")

def runaway_recursion(count: int) -> int:
    return runaway_recursion(count + 1)

caught_recursion_error = False
try:
    runaway_recursion(1)
except RecursionError as err:
    caught_recursion_error = True
    print(f"  Caught expected RecursionError: {err}")

assert caught_recursion_error
assert current_limit >= 1000

# Explanation: Python guards against C-stack overflow by enforcing a maximum recursion depth
# (default 1000). Exceeding it raises `RecursionError` cleanly.


# ============================================================
# Q3: Tail Recursion & Accumulator Pattern (No TCO in CPython)
# ============================================================
# Question: Explain why Python does NOT optimize tail-recursive calls (no Tail Call Optimization).
# Refactor a recursive sum function to use an accumulator, and compare it with the iterative version.

print("\n=== Q3: Accumulator Pattern vs Iterative Loop ===")

# Standard recursion: work is done DURING stack unwinding: N + sum(N-1)
def sum_natural_head(n: int) -> int:
    if n <= 0:
        return 0
    return n + sum_natural_head(n - 1)

# Tail-recursive style: work is done BEFORE call using accumulator
def sum_natural_tail(n: int, accumulator: int = 0) -> int:
    if n <= 0:
        return accumulator
    return sum_natural_tail(n - 1, accumulator + n)

# Iterative transformation (Pythonic standard for large N)
def sum_natural_iter(n: int) -> int:
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

res_head = sum_natural_head(10)
res_tail = sum_natural_tail(10)
res_iter = sum_natural_iter(10)

print(f"  Head recursion result: {res_head}")
print(f"  Tail recursion result: {res_tail}")
print(f"  Iterative result:      {res_iter}")

assert res_head == res_tail == res_iter == 55

# Explanation: Guido van Rossum deliberately chose NOT to implement TCO in CPython
# to preserve complete stack traces for debugging and inspection. For large depths,
# use iterative loops or math formulas (n * (n + 1) // 2).


# ============================================================
# Q4: Tree Recursion & Memoization with functools.lru_cache
# ============================================================
# Question: Demonstrate how naive Fibonacci tree recursion exhibits exponential O(2^N)
# time complexity, and how `@functools.lru_cache` reduces it to linear O(N) via memoization.

print("\n=== Q4: Tree Recursion & Memoization ===")

naive_call_count = 0

def fib_naive(n: int) -> int:
    global naive_call_count
    naive_call_count += 1
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

@functools.lru_cache(maxsize=None)
def fib_memoized(n: int) -> int:
    if n <= 1:
        return n
    return fib_memoized(n - 1) + fib_memoized(n - 2)

# Test naive on n = 20
naive_call_count = 0
val_naive = fib_naive(20)
calls_20 = naive_call_count

# Test memoized on n = 20
val_memo = fib_memoized(20)
cache_info = fib_memoized.cache_info()

print(f"  fib(20) = {val_memo}")
print(f"  Naive recursive call count:    {calls_20:,} calls (Exponential explosion!)")
print(f"  Memoized cache stats:          hits={cache_info.hits}, misses={cache_info.misses}")

assert val_naive == val_memo == 6765
assert calls_20 == 21891  # 21,891 calls for just n=20!
assert cache_info.misses == 21  # Linear O(N) evaluation

# Explanation: Tree recursion without memoization re-evaluates overlapping subproblems
# exponentially. `lru_cache` stores computed returns in a dict, making repeated calls O(1).


# ============================================================
# Q5: Arbitrarily Nested List Deep Flattening
# ============================================================
# Question: Write a recursive function to flatten a list containing arbitrarily nested
# lists, tuples, and scalar elements into a single flat list.

print("\n=== Q5: Deep List Flattening ===")

nested_data = [1, [2, [3, 4], 5], [[6]], [7, [8, [9, 10]]]]

def deep_flatten(items: Any) -> List[Any]:
    flat: List[Any] = []
    if isinstance(items, (list, tuple)):
        for item in items:
            flat.extend(deep_flatten(item))
    else:
        flat.append(items)
    return flat

flattened_result = deep_flatten(nested_data)
print(f"  Original nested:   {nested_data}")
print(f"  Deeply flattened:  {flattened_result}")

assert flattened_result == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
assert deep_flatten([]) == []
assert deep_flatten([[[[42]]]]) == [42]

# Explanation: At each depth, if an item is a sequence container, we recursively
# unpack its elements; otherwise, we append the scalar base value.


# ============================================================
# Q6: Recursive Binary Search: Pointer-Based O(log N)
# ============================================================
# Question: Implement recursive binary search using index boundaries `(low, high)` in O(log N)
# time. Explain why using list slicing `arr[:mid]` is an anti-pattern (O(N) memory copy).

print("\n=== Q6: Pointer-Based Recursive Binary Search ===")

sorted_array = [3, 9, 14, 19, 25, 33, 42, 56, 68, 77, 89, 94]

def binary_search_recursive(arr: List[int], target: int, low: int, high: int) -> int:
    """O(log N) time and O(log N) stack frames by passing pointers without copying array."""
    if low > high:
        return -1  # Base Case: target not found

    mid = (low + high) // 2
    if arr[mid] == target:
        return mid  # Base Case: found target
    elif arr[mid] > target:
        return binary_search_recursive(arr, target, low, mid - 1)
    else:
        return binary_search_recursive(arr, target, mid + 1, high)

idx_33 = binary_search_recursive(sorted_array, 33, 0, len(sorted_array) - 1)
idx_50 = binary_search_recursive(sorted_array, 50, 0, len(sorted_array) - 1)

print(f"  Target 33 index: {idx_33}")
print(f"  Target 50 index: {idx_50}")

assert idx_33 == 5
assert idx_50 == -1

# Explanation: Slicing `arr[:mid]` copies half the array in memory on every call,
# converting an O(log N) algorithm into O(N) time and memory. Passing `low` and `high` pointers preserves O(log N).


# ============================================================
# Q7: Backtracking Recursion: String Permutations
# ============================================================
# Question: Generate all unique permutations of a string using recursive backtracking
# (choose, explore, un-choose).

print("\n=== Q7: Recursive Backtracking (Permutations) ===")

def generate_permutations(text: str) -> List[str]:
    results: List[str] = []
    chars = list(text)

    def _backtrack(start: int) -> None:
        if start == len(chars):
            results.append("".join(chars))
            return

        seen_at_depth = set()
        for i in range(start, len(chars)):
            # Avoid duplicate permutations if identical letters exist
            if chars[i] in seen_at_depth:
                continue
            seen_at_depth.add(chars[i])

            # 1. Choose: swap character to current position
            chars[start], chars[i] = chars[i], chars[start]
            
            # 2. Explore: recurse for remaining positions
            _backtrack(start + 1)
            
            # 3. Un-choose (Backtrack): restore swap state
            chars[start], chars[i] = chars[i], chars[start]

    _backtrack(0)
    return results

perms_abc = generate_permutations("ABC")
print(f"  Permutations of 'ABC' ({len(perms_abc)} total): {perms_abc}")

assert len(perms_abc) == 6  # 3! = 6
assert set(perms_abc) == {"ABC", "ACB", "BAC", "BCA", "CAB", "CBA"}

# Explanation: Backtracking uses recursion to traverse decision trees, reverting state changes
# upon return so parallel exploration branches operate on pristine data structures.


# ============================================================
# Q8: Tower of Hanoi Recursive Solver
# ============================================================
# Question: Solve the Tower of Hanoi problem for N disks. Prove that the minimum number
# of moves required is 2^N - 1, and verify disk placement rules (no larger disk on smaller).

print("\n=== Q8: Tower of Hanoi Solver ===")

def solve_hanoi(n: int, source: str, target: str, auxiliary: str, moves_log: List[Tuple[int, str, str]]) -> None:
    """
    Moves n disks from source to target using auxiliary peg.
    1) Move n-1 disks from source to auxiliary.
    2) Move disk n from source to target.
    3) Move n-1 disks from auxiliary to target.
    """
    if n == 1:
        moves_log.append((1, source, target))
        return

    # Step 1: Move top n-1 disks to auxiliary peg
    solve_hanoi(n - 1, source, auxiliary, target, moves_log)
    
    # Step 2: Move largest disk to target peg
    moves_log.append((n, source, target))
    
    # Step 3: Move n-1 disks from auxiliary to target peg
    solve_hanoi(n - 1, auxiliary, target, source, moves_log)

moves_3: List[Tuple[int, str, str]] = []
solve_hanoi(3, "A", "C", "B", moves_3)

print(f"  Tower of Hanoi for 3 disks ({len(moves_3)} moves):")
for disk, src, dst in moves_3:
    print(f"    Move disk {disk} from {src} -> {dst}")

# 3 disks requires 2^3 - 1 = 7 moves
assert len(moves_3) == 7
assert moves_3[0] == (1, "A", "C")
assert moves_3[-1] == (1, "A", "C")

# Test 4 disks: 2^4 - 1 = 15 moves
moves_4: List[Tuple[int, str, str]] = []
solve_hanoi(4, "A", "C", "B", moves_4)
assert len(moves_4) == 15

# Explanation: The recurrence relation T(N) = 2*T(N-1) + 1 yields T(N) = 2^N - 1,
# a classic demonstration of divide-and-conquer recursion.


# ============================================================
# Q9: Virtual File Tree Traversal & Disk Usage Calculator
# ============================================================
# Question: Model a virtual hierarchical filesystem with files and folders.
# Recursively calculate total directory size and collect all file paths matching an extension.

print("\n=== Q9: Virtual File Tree Directory Traversal ===")

virtual_filesystem = {
    "name": "root",
    "type": "dir",
    "children": [
        {"name": "index.html", "type": "file", "size_kb": 12},
        {
            "name": "src",
            "type": "dir",
            "children": [
                {"name": "app.py", "type": "file", "size_kb": 45},
                {"name": "utils.py", "type": "file", "size_kb": 20},
                {
                    "name": "assets",
                    "type": "dir",
                    "children": [
                        {"name": "logo.png", "type": "file", "size_kb": 150},
                        {"name": "styles.css", "type": "file", "size_kb": 30}
                    ]
                }
            ]
        },
        {"name": "README.md", "type": "file", "size_kb": 8}
    ]
}

def calculate_tree_size(node: Dict[str, Any]) -> int:
    """Recursively computes total size in KB."""
    if node["type"] == "file":
        return int(node.get("size_kb", 0))
    return sum(calculate_tree_size(child) for child in node.get("children", []))

def find_files_by_extension(node: Dict[str, Any], ext: str, current_path: str = "") -> List[str]:
    """Recursively finds all file paths ending with specified extension."""
    path = f"{current_path}/{node['name']}" if current_path else node["name"]
    matches = []
    
    if node["type"] == "file":
        if node["name"].endswith(ext):
            matches.append(path)
    else:
        for child in node.get("children", []):
            matches.extend(find_files_by_extension(child, ext, path))
            
    return matches

total_kb = calculate_tree_size(virtual_filesystem)
py_files = find_files_by_extension(virtual_filesystem, ".py")

print(f"  Total filesystem disk usage: {total_kb} KB")
print(f"  Python files discovered:     {py_files}")

assert total_kb == (12 + 45 + 20 + 150 + 30 + 8)  # 265 KB
assert len(py_files) == 2
assert "root/src/app.py" in py_files
assert "root/src/utils.py" in py_files

# Explanation: Filesystem directory structures are tree structures of arbitrary depth.
# Recursive traversal naturally maps to the parent-child node hierarchy.


# ============================================================
# Q10: Recursive Descent Expression Evaluator
# ============================================================
# Question: Implement a miniature recursive descent parser that evaluates arithmetic
# expressions supporting +, -, *, /, and nested parentheses with proper operator precedence.

print("\n=== Q10: Recursive Descent Expression Parser ===")

class SimpleParser:
    """
    Grammar:
      expr   = term (( '+' | '-' ) term)*
      term   = factor (( '*' | '/' ) factor)*
      factor = number | '(' expr ')'
    """
    def __init__(self, expression: str):
        # Remove whitespace
        self.tokens = expression.replace(" ", "")
        self.pos = 0

    def parse(self) -> float:
        result = self._expr()
        if self.pos < len(self.tokens):
            raise ValueError(f"Unexpected token at position {self.pos}: '{self.tokens[self.pos]}'")
        return result

    def _expr(self) -> float:
        value = self._term()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in ("+", "-"):
            op = self.tokens[self.pos]
            self.pos += 1
            right = self._term()
            value = (value + right) if op == "+" else (value - right)
        return value

    def _term(self) -> float:
        value = self._factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in ("*", "/"):
            op = self.tokens[self.pos]
            self.pos += 1
            right = self._factor()
            value = (value * right) if op == "*" else (value / right)
        return value

    def _factor(self) -> float:
        if self.tokens[self.pos] == "(":
            self.pos += 1  # Skip '('
            value = self._expr()
            if self.pos >= len(self.tokens) or self.tokens[self.pos] != ")":
                raise ValueError("Mismatched parenthesis: missing ')'")
            self.pos += 1  # Skip ')'
            return value

        # Parse number literal
        start = self.pos
        while self.pos < len(self.tokens) and (self.tokens[self.pos].isdigit() or self.tokens[self.pos] == "."):
            self.pos += 1
        
        num_str = self.tokens[start:self.pos]
        if not num_str:
            raise ValueError(f"Expected number at index {start}")
        return float(num_str)

eval1 = SimpleParser("3 + 5 * 2").parse()              # Precedence: 3 + 10 = 13
eval2 = SimpleParser("(3 + 5) * 2").parse()            # Parentheses: 8 * 2 = 16
eval3 = SimpleParser("100 / (2 + 3) * 4").parse()      # 100 / 5 * 4 = 80
eval4 = SimpleParser("2 * (3 + (4 * 5)) - 6").parse()  # 2 * 23 - 6 = 40

print(f"  '3 + 5 * 2'          = {eval1}")
print(f"  '(3 + 5) * 2'        = {eval2}")
print(f"  '100 / (2 + 3) * 4'  = {eval3}")
print(f"  '2*(3+(4*5))-6'      = {eval4}")

assert eval1 == 13.0
assert eval2 == 16.0
assert eval3 == 80.0
assert eval4 == 40.0

print("\nAll 10 recursion questions executed and asserted successfully!")
