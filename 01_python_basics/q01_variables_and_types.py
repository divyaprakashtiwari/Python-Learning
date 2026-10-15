"""
Topic 01: Python Basics
Question 01: Variables and Data Types

Master Python's fundamental data types by creating, inspecting,
and manipulating variables of every built-in type.
"""

# ============================================================
# Q1: Create variables of each basic type and print their types
# ============================================================
# Question: Create one variable of each type: int, float, str,
# bool, NoneType, complex. Print each variable and its type.

name = "Divya"           # str
age = 21                 # int
height = 5.9             # float
is_student = True        # bool
nothing = None           # NoneType
imaginary = 3 + 4j       # complex

print("=== Q1: Basic Variable Types ===")
for var, label in [(name, "name"), (age, "age"), (height, "height"),
                   (is_student, "is_student"), (nothing, "nothing"),
                   (imaginary, "imaginary")]:
    print(f"  {label} = {var!r:<20} type = {type(var).__name__}")

# Explanation: Python is dynamically typed — you don't declare types.
# type() returns the class of a value; __name__ gives a readable string.
# Output:
#   name = 'Divya'             type = str
#   age = 21                   type = int
#   height = 5.9               type = float
#   is_student = True          type = bool
#   nothing = None             type = NoneType
#   imaginary = (3+4j)         type = complex


# ============================================================
# Q2: Check if two variables point to the same object (id & is)
# ============================================================
# Question: Create two variables with the same integer value (e.g., 256)
# and check whether they share the same memory address using id() and `is`.
# Then do the same with a large integer (e.g., 1000). Explain the difference.

print("\n=== Q2: Identity vs Equality ===")
a = 256
b = 256
print(f"  a = {a}, b = {b}")
print(f"  a == b : {a == b}")       # True (same value)
print(f"  a is b : {a is b}")       # True (Python caches -5 to 256)
print(f"  id(a) = {id(a)}, id(b) = {id(b)}")

x = 1000
y = 1000
print(f"\n  x = {x}, y = {y}")
print(f"  x == y : {x == y}")       # True (same value)
print(f"  x is y : {x is y}")       # May be True or False depending on context
print(f"  id(x) = {id(x)}, id(y) = {id(y)}")

# Explanation: Python interns small integers (-5 to 256) for performance.
# For these, `is` returns True because both variables point to the same
# cached object. For larger integers, Python *may* create separate objects,
# so `is` can return False even though `==` returns True.
# Key rule: Use `==` for value comparison, `is` for identity comparison.


# ============================================================
# Q3: Demonstrate that Python integers have unlimited precision
# ============================================================
# Question: Compute 2**1000 and print its value and number of digits.
# Show that Python doesn't overflow like C or Java.

print("\n=== Q3: Unlimited Integer Precision ===")
big_number = 2 ** 1000
digits = len(str(big_number))
print(f"  2 ** 1000 has {digits} digits")
print(f"  First 50 chars: {str(big_number)[:50]}...")
print(f"  Last  50 chars: ...{str(big_number)[-50:]}")

# Explanation: Python's int type supports arbitrary precision arithmetic.
# Unlike C (where int overflows at ~2 billion) or Java (long at ~9.2e18),
# Python can handle numbers with thousands of digits seamlessly.
# Output: 2 ** 1000 has 302 digits


# ============================================================
# Q4: Explore boolean values as integers
# ============================================================
# Question: Show that True == 1 and False == 0 in Python.
# Demonstrate boolean arithmetic and a practical use case.

print("\n=== Q4: Booleans as Integers ===")
print(f"  True  + True  = {True + True}")     # 2
print(f"  True  * 10    = {True * 10}")        # 10
print(f"  False + 42    = {False + 42}")       # 42
print(f"  True  == 1    : {True == 1}")        # True
print(f"  False == 0    : {False == 0}")       # True
print(f"  isinstance(True, int): {isinstance(True, int)}")  # True

# Practical: Count how many numbers in a list are even
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_count = sum(n % 2 == 0 for n in numbers)
print(f"  Even numbers in {numbers}: {even_count}")

# Explanation: bool is a subclass of int in Python. True is literally 1
# and False is literally 0. This allows using booleans in arithmetic,
# which is useful in patterns like sum(condition for item in iterable).


# ============================================================
# Q5: Demonstrate string immutability
# ============================================================
# Question: Show that strings cannot be modified in place.
# Attempt to change a character and handle the resulting error.

print("\n=== Q5: String Immutability ===")
greeting = "Hello"
print(f"  Original: {greeting!r}")

try:
    greeting[0] = "J"  # This will raise TypeError
except TypeError as e:
    print(f"  Error: {e}")
    print("  Strings are immutable -- you cannot change individual characters.")

# The correct approach: create a new string
new_greeting = "J" + greeting[1:]
print(f"  New string: {new_greeting!r}")

# Explanation: Python strings are immutable sequences. Any "modification"
# actually creates a new string object. This design enables string
# interning and makes strings hashable (usable as dict keys / set elements).


# ============================================================
# Q6: Understand None — Python's null value
# ============================================================
# Question: Demonstrate proper None usage, comparison, and common pitfalls.

print("\n=== Q6: None -- Python's Null ===")
result = None

# Always use `is` to compare with None, never `==`
print(f"  result is None     : {result is None}")        # True (correct)
print(f"  result is not None : {result is not None}")    # False
print(f"  result == None     : {result == None}")        # True but BAD practice

# None is falsy
if not result:
    print("  None is falsy in a boolean context")

# None is a singleton — there's only one None object
print(f"  id(None) = {id(None)}")
a_none = None
print(f"  id(a_none) = {id(a_none)}")
print(f"  a_none is None: {a_none is None}")  # Always True

# Edge case: distinguish None from other falsy values
falsy_values = [None, 0, "", [], False, {}, set()]
for val in falsy_values:
    is_none = "IS None" if val is None else "not None"
    print(f"  {str(type(val).__name__):>5} {str(val)!r:<8} -> falsy, but {is_none}")

# Explanation: None is Python's singleton null object. Always compare with
# `is None` (not `==`) because a class can override __eq__ to return True
# for None comparison. None is falsy, but so are 0, "", [], etc.


# ============================================================
# Q7: Dynamic typing — reassigning a variable to different types
# ============================================================
# Question: Assign a variable to an int, then reassign it to a str,
# then a list. Show the type changes at each step.

print("\n=== Q7: Dynamic Typing ===")
data = 42
print(f"  data = {data!r:<20} type = {type(data).__name__}")

data = "now a string"
print(f"  data = {data!r:<20} type = {type(data).__name__}")

data = [1, 2, 3]
print(f"  data = {data!r:<20} type = {type(data).__name__}")

data = {"key": "value"}
print(f"  data = {data!r:<20} type = {type(data).__name__}")

# Explanation: Python variables are just names (labels) bound to objects.
# Reassigning a variable doesn't change the old object — it rebinds the
# name to a new object. The old object may be garbage-collected if no
# other references exist.


# ============================================================
# Q8: Use isinstance() for safe type checking
# ============================================================
# Question: Write a function that accepts any value and returns a
# description of its type category (numeric, text, collection, other).

print("\n=== Q8: isinstance() for Type Checking ===")

def categorize(value):
    """Categorize a value into a type family."""
    if isinstance(value, bool):
        # Check bool BEFORE int because bool is a subclass of int
        return "boolean"
    elif isinstance(value, (int, float, complex)):
        return "numeric"
    elif isinstance(value, str):
        return "text"
    elif isinstance(value, (list, tuple, set, frozenset, dict)):
        return "collection"
    elif value is None:
        return "null"
    else:
        return "other"

test_values = [42, 3.14, "hello", True, None, [1, 2], (1,), {1}, {"a": 1}, 2+3j]
for val in test_values:
    print(f"  {val!r:<16} -> {categorize(val)}")

# Explanation: isinstance() is preferred over type() == because it
# respects inheritance. Crucially, check bool before int because
# isinstance(True, int) returns True (bool is a subclass of int).
# Output:
#   42               -> numeric
#   3.14             -> numeric
#   'hello'          -> text
#   True             -> boolean
#   None             -> null
#   [1, 2]           -> collection


# ============================================================
# Q9: Explore the sys.getsizeof() for memory footprint
# ============================================================
# Question: Compare the memory footprint of different data types
# and demonstrate how Python's integer size grows with magnitude.

import sys

print("\n=== Q9: Memory Footprint of Types ===")
samples = {
    "int (0)": 0,
    "int (1)": 1,
    "int (2**30)": 2**30,
    "int (2**100)": 2**100,
    "float": 3.14,
    "str (empty)": "",
    "str ('hi')": "hi",
    "bool": True,
    "None": None,
    "list (empty)": [],
    "list [1,2,3]": [1, 2, 3],
    "dict (empty)": {},
    "tuple (empty)": (),
}

print(f"  {'Type':<18} {'Value':<22} {'Bytes':>6}")
print(f"  {'-'*18} {'-'*22} {'-'*6}")
for label, val in samples.items():
    val_str = repr(val) if len(repr(val)) <= 20 else repr(val)[:17] + "..."
    print(f"  {label:<18} {val_str:<22} {sys.getsizeof(val):>6}")

# Explanation: sys.getsizeof() returns the memory consumed by an object
# in bytes. Key observations:
# - Python int grows in memory as magnitude increases (arbitrary precision).
# - float is always the same size (C double under the hood).
# - Empty collections have a base overhead for the container itself.
# - Containers report *shallow* size (not including contained objects).


# ============================================================
# Q10: Multiple assignment, unpacking, and swap idiom
# ============================================================
# Question: Demonstrate simultaneous assignment, sequence unpacking,
# extended unpacking (*), and the Pythonic swap idiom.

print("\n=== Q10: Multiple Assignment & Unpacking ===")

# Simultaneous assignment
x, y, z = 1, 2, 3
print(f"  x={x}, y={y}, z={z}")

# Swap without a temporary variable
x, y = y, x
print(f"  After swap: x={x}, y={y}")

# Extended unpacking with *
first, *middle, last = [10, 20, 30, 40, 50]
print(f"  first={first}, middle={middle}, last={last}")

# Unpacking a nested structure
person = ("Divya", (2005, 3, 15))
name, (year, month, day) = person
print(f"  Name: {name}, Born: {year}-{month:02d}-{day:02d}")

# Edge case: single-element unpacking
(solo,) = [99]
print(f"  Single unpack: {solo}")

# Using _ as throwaway variable
_, important, _ = ("ignore", "keep this", "ignore")
print(f"  Kept: {important!r}")

# Explanation: Python supports parallel assignment via tuple packing/unpacking.
# The swap idiom (a, b = b, a) works because the right side is evaluated
# first as a tuple, then unpacked to the left. The * operator in unpacking
# captures "the rest" as a list — very useful for head/tail patterns.
# Output:
#   x=1, y=2, z=3
#   After swap: x=2, y=1
#   first=10, middle=[20, 30, 40], last=50
#   Name: Divya, Born: 2005-03-15
#   Single unpack: 99
#   Kept: 'keep this'
