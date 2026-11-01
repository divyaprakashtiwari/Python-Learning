# Python Quick Syntax Reference (`CHEATSHEET.md`)

A comprehensive, beginner-to-advanced quick reference for Python syntax, data structures, OOP, functional utilities, and DSA snippets.

---

## 1. Variables, Data Types & Type Casting

```python
# Dynamic typing (no type declaration required)
age = 21                    # int
gpa = 3.85                  # float
name = "Aarav"              # str
is_placed = True            # bool
nothing = None              # NoneType

# Constants (PEP 8 naming convention)
MAX_RETRIES = 3
PI = 3.14159

# Type checking & casting
print(type(age))            # <class 'int'>
print(isinstance(age, int)) # True
num_str = str(42)           # "42"
parsed_int = int("42")      # 42
parsed_float = float("3.5") # 3.5
```

---

## 2. Input, Output & String Formatting

```python
# Console Input (always returns a string)
# user_name = input("Enter name: ")
# count = int(input("Enter count: "))

# f-Strings (Python 3.6+, recommended)
item = "Notebook"
price = 49.956
print(f"Item: {item} | Price: Rs.{price:.2f}")  # Item: Notebook | Price: Rs.49.96

# Custom separator and line ending
print("2026", "11", "01", sep="-", end="\n")    # 2026-11-01
```

---

## 3. Operators

| Category | Operators | Example |
| :--- | :--- | :--- |
| **Arithmetic** | `+`, `-`, `*`, `/` (float div), `//` (floor div), `%` (modulo), `**` (power) | `17 // 5 == 3`, `2 ** 3 == 8` |
| **Comparison** | `==`, `!=`, `<`, `>`, `<=`, `>=` | `10 >= 5` |
| **Logical** | `and`, `or`, `not` | `x > 0 and x < 10` |
| **Bitwise** | `&`, `\|`, `^`, `~`, `<<`, `>>` | `5 & 3 == 1`, `1 << 3 == 8` |
| **Identity** | `is`, `is not` | `val is None` |
| **Membership** | `in`, `not in` | `"a" in "apple"` |

---

## 4. Control Flow (Conditionals & Loops)

```python
# if / elif / else
score = 85
if score >= 90:
    grade = "A+"
elif score >= 80:
    grade = "A"
else:
    grade = "B"

# Ternary expression
status = "Pass" if score >= 40 else "Fail"

# For loop with range(start, stop, step)
for i in range(0, 10, 2):
    if i == 4:
        continue    # Skip current iteration
    if i == 8:
        break       # Exit loop early

# While loop
n = 3
while n > 0:
    n -= 1
```

---

## 5. Core Data Structures & Time Complexities

| Data Structure | Syntax | Mutable? | Ordered? | Lookup Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **List** | `[1, 2, 3]` | Yes | Yes | `O(n)` by value, `O(1)` by index |
| **Tuple** | `(1, 2, 3)` | No | Yes | `O(n)` by value, `O(1)` by index |
| **Set** | `{1, 2, 3}` | Yes | No | `O(1)` average |
| **Dictionary** | `{"a": 1, "b": 2}` | Yes | Yes (3.7+) | `O(1)` average by key |
| **Deque** | `deque([1, 2])` | Yes | Yes | `O(1)` append/pop at both ends |

```python
# List Slicing: list[start:stop:step]
nums = [10, 20, 30, 40, 50]
print(nums[1:4])    # [20, 30, 40]
print(nums[::-1])   # [50, 40, 30, 20, 10] (Reversed copy)

# Comprehensions
squares = [x * x for x in range(6) if x % 2 == 0]  # [0, 4, 16]
square_map = {x: x * x for x in range(4)}          # {0: 0, 1: 1, 2: 4, 3: 9}
```

---

## 6. Functions & Functional Tools

```python
def calculate_total(base: float, tax_rate: float = 0.18, *discounts, **metadata) -> float:
    """Calculate total after discounts and tax."""
    discounted = base - sum(discounts)
    return round(discounted * (1 + tax_rate), 2)

# Lambda, map, filter
double = lambda x: x * 2
evens = list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4]))
```

---

## 7. Object-Oriented Programming (OOP)

```python
class BankAccount:
    bank_name = "Python National Bank"  # Class variable

    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner = owner              # Public instance variable
        self._balance = balance         # Protected convention

    def deposit(self, amount: float) -> None:
        self._balance += amount

    def __repr__(self) -> str:
        return f"BankAccount(owner={self.owner!r}, balance={self._balance})"
```

---

## 8. Essential DSA Library Imports

```python
from collections import Counter, defaultdict, deque
import heapq
from bisect import bisect_left, bisect_right
from functools import lru_cache
import math

# Min-Heap operations
heap = []
heapq.heappush(heap, 10)
smallest = heapq.heappop(heap)

# Max-Heap trick (negate numbers)
heapq.heappush(heap, -25)
largest = -heapq.heappop(heap)

# Memoization for Dynamic Programming / Recursion
@lru_cache(maxsize=None)
def fib(n: int) -> int:
    return n if n <= 1 else fib(n - 1) + fib(n - 2)
```
