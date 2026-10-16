"""
Topic 01: Python Basics
Question 09: Variable Swapping and Multiple Assignment

Master Python's powerful assignment features: simultaneous assignment,
swapping, unpacking, starred expressions, and walrus operator.
"""

# ============================================================
# Q1: Pythonic variable swapping
# ============================================================
# Question: Swap two variables without a temporary variable.
# Show how Python makes this work under the hood.

print("=== Q1: Variable Swapping ===")

a, b = 10, 20
print(f"  Before: a={a}, b={b}")
a, b = b, a
print(f"  After:  a={a}, b={b}")

# Under the hood: Python creates a tuple (b, a) first, then unpacks
# This is equivalent to:
# temp = (b, a)
# a = temp[0]
# b = temp[1]

# Swap three variables (rotate)
x, y, z = 1, 2, 3
print(f"\n  Before: x={x}, y={y}, z={z}")
x, y, z = y, z, x
print(f"  Rotated: x={x}, y={y}, z={z}")

# Traditional swap (other languages)
a, b = 10, 20
temp = a
a = b
b = temp
print(f"\n  Traditional swap: a={a}, b={b}")

# Explanation: Python's swap (a, b = b, a) works because the right side
# is fully evaluated as a tuple BEFORE any assignment happens.
# This is atomic and can't fail halfway. Works for any number of variables.


# ============================================================
# Q2: Multiple assignment patterns
# ============================================================
# Question: Demonstrate all forms of multiple assignment in Python.

print("\n=== Q2: Multiple Assignment Patterns ===")

# Same value to multiple variables
a = b = c = 0
print(f"  a = b = c = 0:  a={a}, b={b}, c={c}")
# WARNING: This shares the SAME object for mutable types!

# Simultaneous assignment (tuple unpacking)
name, age, city = "Divya", 21, "Delhi"
print(f"  name={name}, age={age}, city={city}")

# From a list
data = [100, 200, 300]
x, y, z = data
print(f"  Unpacked list: x={x}, y={y}, z={z}")

# From a string
a, b, c = "ABC"
print(f"  Unpacked string: a={a!r}, b={b!r}, c={c!r}")

# Mutable gotcha with chained assignment
list1 = list2 = [1, 2, 3]
list1.append(4)
print(f"\n  Chained assignment gotcha:")
print(f"  list1 = list2 = [1,2,3]; list1.append(4)")
print(f"  list1 = {list1}")
print(f"  list2 = {list2}")  # Also [1,2,3,4]!
print(f"  Same object: {list1 is list2}")

# Fix: create independent copies
list1 = [1, 2, 3]
list2 = [1, 2, 3]  # Separate object
list1.append(4)
print(f"\n  Independent lists:")
print(f"  list1 = {list1}, list2 = {list2}")

# Explanation: `a = b = c = 0` makes all three point to the SAME object.
# For immutable types (int, str) this is fine. For mutable types (list, dict)
# it creates an aliasing bug -- modifying one affects all.


# ============================================================
# Q3: Extended unpacking with * (starred expressions)
# ============================================================
# Question: Use the * operator to capture "the rest" during unpacking.

print("\n=== Q3: Extended Unpacking with * ===")

# Head and tail
first, *rest = [1, 2, 3, 4, 5]
print(f"  first={first}, rest={rest}")

# Init and last
*init, last = [1, 2, 3, 4, 5]
print(f"  init={init}, last={last}")

# Head, middle, tail
first, *middle, last = [1, 2, 3, 4, 5]
print(f"  first={first}, middle={middle}, last={last}")

# With only two elements
first, *rest = [1, 2]
print(f"  Two items: first={first}, rest={rest}")

# With only one element
(solo,) = [1]
print(f"  One item: solo={solo}")

# Starred can be empty
first, *rest = [1]
print(f"  Star empty: first={first}, rest={rest}")

# Nested unpacking
(a, b), (c, d) = [1, 2], [3, 4]
print(f"\n  Nested: a={a}, b={b}, c={c}, d={d}")

# Deep nesting
data = ("Divya", (95, 88, 92), "Delhi")
name, (math_s, sci, eng), city = data
print(f"  Deep: name={name}, scores=({math_s},{sci},{eng}), city={city}")

# Practical: Processing CSV-like data
records = [
    "Divya,21,Student",
    "Amit,25,Developer",
    "Priya,23,Designer",
]
print(f"\n  CSV parsing:")
for record in records:
    name, age, role = record.split(",")
    print(f"    {name:<8} age={age:>3} role={role}")

# Explanation: The * operator in unpacking captures remaining items as a list.
# Only ONE starred variable is allowed per unpacking. It can appear at any
# position. Nested unpacking matches the structure of the data.


# ============================================================
# Q4: Unpacking in function calls
# ============================================================
# Question: Use * and ** for unpacking arguments to function calls.

print("\n=== Q4: Unpacking in Function Calls ===")

def greet(name, age, city):
    print(f"    {name} ({age}) from {city}")

# Unpack list/tuple with *
args = ["Divya", 21, "Delhi"]
print("  * unpacking:")
greet(*args)

# Unpack dict with **
kwargs = {"name": "Amit", "age": 25, "city": "Mumbai"}
print("  ** unpacking:")
greet(**kwargs)

# Mix of positional and unpacking
extra_args = [25, "Pune"]
print("  Mixed:")
greet("Rahul", *extra_args)

# Merging dictionaries with **
defaults = {"color": "blue", "size": "medium", "count": 1}
overrides = {"color": "red", "count": 5}
merged = {**defaults, **overrides}
print(f"\n  Merged dict: {merged}")

# Merging lists with *
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = [*list1, *list2]
print(f"  Merged list: {combined}")

# Creating a tuple/set
unique = {*list1, *list2, 7, 8}
print(f"  Merged set:  {sorted(unique)}")

# Explanation: * unpacks iterables, ** unpacks dictionaries.
# When merging dicts with **, later keys override earlier ones.
# This is Python's clean alternative to dict.update() or list.extend().
# Python 3.9+ also supports dict1 | dict2 for merging dicts.


# ============================================================
# Q5: Unpacking with enumerate, zip, and comprehensions
# ============================================================
# Question: Combine unpacking with iteration tools.

print("\n=== Q5: Unpacking in Iterations ===")

# Unpacking with enumerate
fruits = ["apple", "banana", "cherry"]
print("  enumerate unpacking:")
for i, fruit in enumerate(fruits, 1):
    print(f"    {i}. {fruit}")

# Unpacking with zip
names = ["Divya", "Amit", "Priya"]
scores = [95, 88, 72]
grades = ["A", "B", "C"]

print("\n  zip unpacking:")
for name, score, grade in zip(names, scores, grades):
    print(f"    {name:<8} scored {score} (grade {grade})")

# Unpacking in comprehensions
pairs = [(1, 'a'), (2, 'b'), (3, 'c')]
numbers = [n for n, _ in pairs]
letters = [l for _, l in pairs]
print(f"\n  Numbers: {numbers}")
print(f"  Letters: {letters}")

# Dict comprehension with unpacking
name_score = dict(zip(names, scores))
print(f"  Dict from zip: {name_score}")

# Transpose a matrix using zip
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
transposed = list(zip(*matrix))
print(f"\n  Original:   {matrix}")
print(f"  Transposed: {[list(row) for row in transposed]}")

# Explanation: enumerate gives (index, value) pairs for unpacking.
# zip combines iterables into tuples for parallel iteration.
# zip(*matrix) is a clever transpose trick: * unpacks the rows as
# separate arguments to zip, which re-groups by column position.


# ============================================================
# Q6: Walrus operator (:=) for assignment expressions
# ============================================================
# Question: Use := to assign and test in one expression.
# Show practical patterns where it simplifies code.

print("\n=== Q6: Walrus Operator (:=) ===")

# Basic usage: assign and use in one expression
# Without walrus:
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
n = len(data)
if n > 5:
    print(f"  List has {n} items (more than 5)")

# With walrus:
if (n := len(data)) > 5:
    print(f"  Walrus: List has {n} items (more than 5)")

# In while loops (classic use case)
# Simulating reading lines from input
lines = iter(["hello", "world", "quit", "ignored"])
print("\n  Reading until 'quit':")
while (line := next(lines, None)) is not None and line != "quit":
    print(f"    Read: {line!r}")

# In list comprehensions (filter and transform)
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# Without walrus: compute twice
results_old = [(x, x**2) for x in numbers if x**2 > 20]
# With walrus: compute once
results_new = [(x, sq) for x in numbers if (sq := x**2) > 20]
print(f"\n  Squares > 20: {results_new}")

# In conditional chains
import re
text = "My phone number is 123-456-7890"
if (match := re.search(r'\d{3}-\d{3}-\d{4}', text)):
    print(f"  Found phone: {match.group()}")

# Explanation: The walrus operator (:=) assigns a value to a variable
# as part of an expression. It's useful in while loops, if chains,
# and comprehensions to avoid redundant computation or extra lines.
# It was added in Python 3.8 (PEP 572).


# ============================================================
# Q7: Augmented assignment with unpacking
# ============================================================
# Question: Combine augmented assignment with data structures.
# Show patterns for accumulating and reducing data.

print("\n=== Q7: Assignment Patterns for Data Accumulation ===")

# Accumulating into a list
result = []
for i in range(5):
    result += [i ** 2]  # += extends the list
print(f"  Accumulated squares: {result}")

# Accumulating into a dict
word_count = {}
text = "the cat sat on the mat the cat"
for word in text.split():
    word_count[word] = word_count.get(word, 0) + 1
print(f"  Word counts: {word_count}")

# Running total pattern
values = [10, 20, 30, 40, 50]
total = 0
running = []
for v in values:
    total += v
    running.append(total)
print(f"  Running totals: {running}")

# Using setdefault for grouping
students = [
    ("CS", "Divya"), ("CS", "Amit"),
    ("Math", "Priya"), ("CS", "Rahul"),
    ("Math", "Sneha"),
]
by_dept = {}
for dept, name in students:
    by_dept.setdefault(dept, []).append(name)
print(f"  Grouped: {by_dept}")

# Min/Max tracking
data = [5, 2, 8, 1, 9, 3, 7]
min_val = max_val = data[0]
for val in data[1:]:
    if val < min_val:
        min_val = val
    if val > max_val:
        max_val = val
print(f"  Data: {data}")
print(f"  Min: {min_val}, Max: {max_val}")

# Explanation: These patterns show how assignment works with data
# accumulation. dict.get(key, default) avoids KeyError. setdefault
# creates a default value if the key doesn't exist. Running totals
# and min/max tracking are fundamental algorithmic patterns.


# ============================================================
# Q8: Destructuring assignments from function returns
# ============================================================
# Question: Functions returning multiple values and unpacking them.

print("\n=== Q8: Destructuring Function Returns ===")

def analyze_list(data):
    """Return multiple statistics about a list."""
    if not data:
        return 0, 0, 0, 0, []  # length, sum, min, max, sorted
    return len(data), sum(data), min(data), max(data), sorted(data)

nums = [34, 12, 87, 5, 63, 29]

# Unpack all return values
length, total, smallest, largest, ordered = analyze_list(nums)
print(f"  Data:     {nums}")
print(f"  Length:   {length}")
print(f"  Sum:      {total}")
print(f"  Min:      {smallest}")
print(f"  Max:      {largest}")
print(f"  Sorted:   {ordered}")

# Ignore some return values with _
_, total, _, _, _ = analyze_list(nums)
print(f"\n  Just the sum: {total}")

# Use * to capture some returns
length, *_, ordered = analyze_list(nums)
print(f"  Length and sorted: {length}, {ordered}")

# Named tuple for clarity (better than plain tuples)
from collections import namedtuple
Stats = namedtuple('Stats', ['count', 'total', 'minimum', 'maximum'])

def get_stats(data):
    """Return named statistics."""
    return Stats(
        count=len(data),
        total=sum(data),
        minimum=min(data),
        maximum=max(data),
    )

stats = get_stats(nums)
print(f"\n  Named tuple: {stats}")
print(f"  stats.count = {stats.count}")
print(f"  stats.total = {stats.total}")

# Explanation: Python functions can return multiple values (as a tuple).
# Unpacking makes this clean. Use _ for ignored values, * for partial capture.
# For functions returning many values, consider namedtuple or dataclass
# instead of plain tuples for better readability and self-documentation.


# ============================================================
# Q9: Chained assignment pitfalls and best practices
# ============================================================
# Question: Identify and avoid common assignment mistakes.

print("\n=== Q9: Assignment Pitfalls ===")

# Pitfall 1: Mutable default argument
def add_item(item, lst=[]):  # DANGER: shared default!
    lst.append(item)
    return lst

print("  Pitfall 1: Mutable default argument")
r1 = add_item("a")
r2 = add_item("b")
print(f"    add_item('a') = {r1}")
print(f"    add_item('b') = {r2}")  # ['a', 'b'] -- not just ['b']!
print(f"    Same list!     {r1 is r2}")

# Fix:
def add_item_fixed(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

r1 = add_item_fixed("a")
r2 = add_item_fixed("b")
print(f"    Fixed: {r1}, {r2}")

# Pitfall 2: Augmented assignment creates new variable in function
x = 10
def try_modify():
    # x += 1  # UnboundLocalError! Python sees x as local
    pass

print(f"\n  Pitfall 2: x += 1 in function creates local variable")
print(f"    Would cause UnboundLocalError without 'global x'")

# Pitfall 3: Shallow copy vs assignment
original = [[1, 2], [3, 4]]
shallow = original.copy()
shallow[0][0] = 99
print(f"\n  Pitfall 3: Shallow copy")
print(f"    original = {original}")  # [[99, 2], [3, 4]] -- affected!

import copy
original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)
deep[0][0] = 99
print(f"    Deep copy: original = {original}")  # Unchanged

# Explanation: Mutable default arguments are a classic Python gotcha.
# Always use None as default and create new mutable objects inside.
# Shallow copy only copies the top level; nested objects are shared.
# Use copy.deepcopy() when you need fully independent copies.


# ============================================================
# Q10: Pattern matching with assignment (Python 3.10+)
# ============================================================
# Question: Use structural pattern matching for complex assignments.

import sys

print("\n=== Q10: Advanced Assignment Patterns ===")

# Simulate match-case for older Python compatibility
def process_command(command):
    """Process different command structures."""
    parts = command.split()

    if len(parts) == 0:
        return "Empty command"
    elif len(parts) == 1:
        action = parts[0]
        if action == "quit":
            return "Quitting..."
        elif action == "help":
            return "Available: quit, move <x> <y>, greet <name>"
        return f"Unknown command: {action}"
    elif len(parts) == 2:
        action, arg = parts
        if action == "greet":
            return f"Hello, {arg}!"
        return f"Unknown: {action} {arg}"
    elif len(parts) == 3:
        action, arg1, arg2 = parts
        if action == "move":
            try:
                x, y = int(arg1), int(arg2)
                return f"Moving to ({x}, {y})"
            except ValueError:
                return "Invalid coordinates"
        return f"Unknown: {action}"
    else:
        return f"Too many arguments: {len(parts)}"

# If Python 3.10+, also show match-case syntax
commands = ["help", "greet Divya", "move 10 20", "quit", "move a b", ""]
for cmd in commands:
    result = process_command(cmd)
    print(f"  '{cmd}' -> {result}")

# Python 3.10+ match-case version (shown as comment for compatibility):
# match command.split():
#     case ["quit"]:
#         return "Quitting..."
#     case ["greet", name]:
#         return f"Hello, {name}!"
#     case ["move", x, y]:
#         return f"Moving to ({x}, {y})"
#     case _:
#         return "Unknown command"

print(f"\n  Python version: {sys.version}")
if sys.version_info >= (3, 10):
    print("  match-case is available!")
else:
    print("  match-case requires Python 3.10+")

# Explanation: Structural pattern matching (match-case, Python 3.10+) is
# the most powerful form of unpacking/assignment in Python. It can match
# and destructure complex data shapes. For older Python, achieve similar
# results with if/elif chains and manual unpacking.
