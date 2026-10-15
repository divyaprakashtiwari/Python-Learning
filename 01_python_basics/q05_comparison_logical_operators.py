"""
Topic 01: Python Basics
Question 05: Comparison and Logical Operators

Master comparison operators, logical operators (and/or/not),
short-circuit evaluation, chained comparisons, and operator precedence.
"""

# ============================================================
# Q1: All comparison operators
# ============================================================
# Question: Demonstrate ==, !=, <, >, <=, >= with various types.

print("=== Q1: Comparison Operators ===")
a, b = 10, 20

print(f"  a={a}, b={b}")
print(f"  a == b: {a == b}")   # False
print(f"  a != b: {a != b}")   # True
print(f"  a < b:  {a < b}")    # True
print(f"  a > b:  {a > b}")    # False
print(f"  a <= b: {a <= b}")   # True
print(f"  a >= b: {a >= b}")   # False

# String comparison (lexicographic)
print(f"\n  'apple' < 'banana': {'apple' < 'banana'}")  # True
print(f"  'abc' < 'abd':      {'abc' < 'abd'}")          # True
print(f"  'A' < 'a':          {'A' < 'a'}")              # True (65 < 97)

# Comparing different types
print(f"\n  1 == 1.0:   {1 == 1.0}")     # True (cross-type)
print(f"  True == 1:  {True == 1}")      # True (bool is int)
print(f"  0 == False: {0 == False}")     # True

# Explanation: Comparison operators return boolean values. Strings are
# compared lexicographically (character by character using Unicode values).
# Cross-type comparison works for numeric types. Comparing unrelated types
# (like str and int) with < or > raises TypeError in Python 3.


# ============================================================
# Q2: Chained comparisons
# ============================================================
# Question: Demonstrate Python's unique chained comparison feature.

print("\n=== Q2: Chained Comparisons ===")

x = 15
print(f"  x = {x}")
print(f"  1 < x < 20:     {1 < x < 20}")       # True
print(f"  10 <= x <= 20:   {10 <= x <= 20}")     # True
print(f"  0 < x < 10:      {0 < x < 10}")        # False

# Equivalent to: (1 < x) and (x < 20)
# BUT x is only evaluated once in the chained version

# Multiple chains
a, b, c = 1, 2, 3
print(f"\n  a={a}, b={b}, c={c}")
print(f"  a < b < c:   {a < b < c}")             # True
print(f"  a < b > c:   {a < b > c}")             # False
print(f"  a == a == a:  {a == a == a}")           # True
print(f"  a != b != c:  {a != b != c}")           # True (a!=b and b!=c)

# Practical: Range checking
def classify_temperature(temp):
    """Classify temperature using chained comparisons."""
    if temp < 0:
        return "freezing"
    elif 0 <= temp < 15:
        return "cold"
    elif 15 <= temp < 25:
        return "comfortable"
    elif 25 <= temp < 35:
        return "warm"
    else:
        return "hot"

for t in [-10, 0, 10, 20, 30, 40]:
    print(f"  {t:>3} C -> {classify_temperature(t)}")

# Explanation: Chained comparisons are syntactic sugar unique to Python.
# a < b < c is equivalent to (a < b) and (b < c), but b is evaluated
# only once. This makes range checks very readable.


# ============================================================
# Q3: Logical operators (and, or, not)
# ============================================================
# Question: Show how and/or/not work, including their return values
# (they don't always return True/False!)

print("\n=== Q3: Logical Operators ===")

# Basic logic
print(f"  True and True:   {True and True}")
print(f"  True and False:  {True and False}")
print(f"  True or False:   {True or False}")
print(f"  not True:        {not True}")

# KEY INSIGHT: and/or return VALUES, not just True/False
print(f"\n  Return values (not just booleans):")
print(f"  'hello' and 'world': {'hello' and 'world'!r}")  # 'world'
print(f"  '' and 'world':      {'' and 'world'!r}")        # ''
print(f"  'hello' or 'world':  {'hello' or 'world'!r}")   # 'hello'
print(f"  '' or 'world':       {'' or 'world'!r}")         # 'world'
print(f"  0 or [] or 'found':  {0 or [] or 'found'!r}")   # 'found'
print(f"  None and 'hello':    {None and 'hello'!r}")      # None

# Explanation: `and` returns the first falsy value, or the last value.
#              `or` returns the first truthy value, or the last value.
# This is NOT a bug -- it's by design and enables useful patterns.


# ============================================================
# Q4: Short-circuit evaluation
# ============================================================
# Question: Demonstrate that `and` and `or` stop evaluating as
# soon as the result is determined.

print("\n=== Q4: Short-Circuit Evaluation ===")

def loud_true():
    print("    (loud_true called)")
    return True

def loud_false():
    print("    (loud_false called)")
    return False

# `and` stops at first False
print("  False and loud_true():")
result = False and loud_true()    # loud_true NOT called
print(f"  Result: {result}")

print("\n  True and loud_false():")
result = True and loud_false()    # loud_false IS called
print(f"  Result: {result}")

# `or` stops at first True
print("\n  True or loud_false():")
result = True or loud_false()     # loud_false NOT called
print(f"  Result: {result}")

# Practical: Safe attribute access
data = None
# Without short-circuit, this would crash:
name = data and data.get("name", "Unknown")
print(f"\n  data=None, data and data.get('name'): {name!r}")

data = {"name": "Divya"}
name = data and data.get("name", "Unknown")
print(f"  data=dict, data and data.get('name'): {name!r}")

# Explanation: Short-circuit evaluation means Python stops evaluating
# as soon as the outcome is determined. This is used for safe access
# patterns (check None before accessing attributes) and performance
# optimization (put cheap checks before expensive ones).


# ============================================================
# Q5: Logical operator precedence
# ============================================================
# Question: Show the precedence: not > and > or.
# Demonstrate how this can cause unexpected results.

print("\n=== Q5: Logical Operator Precedence ===")

# not > and > or
result1 = True or False and False
print(f"  True or False and False = {result1}")
# Evaluated as: True or (False and False) = True or False = True

result2 = (True or False) and False
print(f"  (True or False) and False = {result2}")
# With parens: True and False = False

# not has highest precedence
result3 = not True or True
print(f"  not True or True = {result3}")
# Evaluated as: (not True) or True = False or True = True

result4 = not (True or True)
print(f"  not (True or True) = {result4}")
# With parens: not True = False

# Practical pitfall
x = 5
# This is WRONG for checking if x is 1 or 2 or 3
wrong = x == 1 or 2 or 3    # Always truthy! (x==1) or 2 or 3
right = x in (1, 2, 3)      # Correct way
print(f"\n  x = {x}")
print(f"  x == 1 or 2 or 3:  {wrong!r} (WRONG! Always truthy)")
print(f"  x in (1, 2, 3):    {right} (Correct)")

# Explanation: The precedence is: not > and > or.
# This means `True or False and False` is `True or (False and False)`.
# Common pitfall: `x == 1 or 2` is `(x == 1) or 2`, not `x == (1 or 2)`.
# Use `x in (1, 2, 3)` or `x == 1 or x == 2 or x == 3`.


# ============================================================
# Q6: Identity operators (is, is not)
# ============================================================
# Question: Explain when to use `is` vs `==` and common gotchas.

print("\n=== Q6: Identity vs Equality ===")

# is checks identity (same object), == checks equality (same value)
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(f"  a = {a}, b = {b}")
print(f"  a == b: {a == b}")   # True (same value)
print(f"  a is b: {a is b}")   # False (different objects)
print(f"  a is c: {a is c}")   # True (same object)

# When to use `is`:
# 1. Comparing with None
value = None
print(f"\n  value is None:     {value is None}")      # CORRECT
print(f"  value == None:     {value == None}")         # Works but BAD

# 2. Comparing with True/False (rare, usually unnecessary)
# 3. Checking if two variables reference the same object

# Integer caching gotcha
x = 256
y = 256
print(f"\n  256 is 256: {x is y}")   # True (cached)

x = 257
y = 257
# In script mode, Python may optimize this differently than REPL
print(f"  257 is 257: {x is y}")     # May be True in scripts

# Explanation: `is` checks if two references point to the same object
# (same id()). `==` checks if two objects have equal values. ALWAYS use
# `is` for None, `is` for singleton checks. Use `==` for everything else.


# ============================================================
# Q7: Membership operators (in, not in)
# ============================================================
# Question: Use `in` and `not in` with strings, lists, dicts, and sets.
# Show performance differences.

print("\n=== Q7: Membership Operators ===")

# In strings
text = "Hello, Python World"
print(f"  'Python' in text:  {'Python' in text}")
print(f"  'java' in text:    {'java' in text}")
print(f"  'H' in text:       {'H' in text}")

# In lists
fruits = ["apple", "banana", "cherry"]
print(f"\n  'banana' in fruits:  {'banana' in fruits}")
print(f"  'grape' not in fruits: {'grape' not in fruits}")

# In dictionaries (checks KEYS, not values)
person = {"name": "Divya", "age": 21}
print(f"\n  'name' in person:  {'name' in person}")      # True
print(f"  'Divya' in person: {'Divya' in person}")       # False (not a key)
print(f"  'Divya' in person.values(): {'Divya' in person.values()}")  # True

# Performance: set vs list for membership testing
import time

data_list = list(range(100000))
data_set = set(data_list)

# Search for a value near the end
target = 99999

start = time.perf_counter()
for _ in range(1000):
    _ = target in data_list
list_time = time.perf_counter() - start

start = time.perf_counter()
for _ in range(1000):
    _ = target in data_set
set_time = time.perf_counter() - start

print(f"\n  Membership test (1000x on 100K items):")
print(f"  List: {list_time:.4f}s")
print(f"  Set:  {set_time:.6f}s")
print(f"  Set is ~{list_time/set_time:.0f}x faster")

# Explanation: `in` for lists is O(n) -- it scans linearly.
# `in` for sets/dicts is O(1) -- it uses hash lookup.
# For dictionaries, `in` checks keys by default.
# Convert to a set when doing repeated membership tests on large data.


# ============================================================
# Q8: Ternary (conditional) expression
# ============================================================
# Question: Use Python's ternary operator for concise conditionals.
# Show nested ternary and alternatives.

print("\n=== Q8: Ternary Expressions ===")

age = 21
status = "adult" if age >= 18 else "minor"
print(f"  age={age}: {status}")

# Ternary with function calls
x = -5
result = abs(x) if x < 0 else x
print(f"  x={x}: abs if negative -> {result}")

# Common pattern: default value
name = ""
display_name = name if name else "Anonymous"
print(f"  name={name!r}: display as {display_name!r}")

# Nested ternary (use sparingly!)
score = 85
grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "F"
print(f"  score={score}: grade={grade}")

# Better alternative for complex conditions
def get_grade(score):
    """Cleaner than nested ternary."""
    thresholds = [(90, "A"), (80, "B"), (70, "C"), (60, "D")]
    for threshold, grade in thresholds:
        if score >= threshold:
            return grade
    return "F"

for s in [95, 85, 75, 65, 50]:
    print(f"  score={s}: grade={get_grade(s)}")

# Explanation: Python's ternary is `value_if_true if condition else value_if_false`.
# Unlike C's `? :`, it reads left to right: result first, then condition.
# Nested ternaries work but hurt readability -- prefer functions or
# dict lookups for complex mappings.


# ============================================================
# Q9: Operator overloading preview
# ============================================================
# Question: Show that comparison operators can be customized
# in classes via magic methods.

print("\n=== Q9: Custom Comparison (Operator Overloading) ===")

class Temperature:
    """Temperature class that supports comparison operators."""

    def __init__(self, celsius):
        self.celsius = celsius

    def __repr__(self):
        return f"Temperature({self.celsius}C)"

    def __eq__(self, other):
        if isinstance(other, Temperature):
            return self.celsius == other.celsius
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Temperature):
            return self.celsius < other.celsius
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Temperature):
            return self.celsius <= other.celsius
        return NotImplemented

    # Python can derive __gt__, __ge__ from __lt__, __le__
    # using functools.total_ordering (covered in OOP)

t1 = Temperature(20)
t2 = Temperature(30)
t3 = Temperature(20)

print(f"  t1={t1}, t2={t2}, t3={t3}")
print(f"  t1 == t3: {t1 == t3}")    # True
print(f"  t1 < t2:  {t1 < t2}")     # True
print(f"  t1 == t2: {t1 == t2}")    # False

# Sorting works because __lt__ is defined
temps = [Temperature(30), Temperature(10), Temperature(20)]
sorted_temps = sorted(temps)
print(f"  sorted: {sorted_temps}")

# Explanation: Python comparison operators call magic methods:
# ==: __eq__,  !=: __ne__,  <: __lt__,  >: __gt__
# <=: __le__,  >=: __ge__
# Returning NotImplemented lets Python try the other operand's method.


# ============================================================
# Q10: Build a flexible condition evaluator
# ============================================================
# Question: Create a system that evaluates complex conditions
# from data, demonstrating all operators together.

print("\n=== Q10: Condition Evaluator ===")

def evaluate_eligibility(person):
    """Check eligibility based on multiple criteria."""
    name = person.get("name", "Unknown")
    age = person.get("age", 0)
    gpa = person.get("gpa", 0.0)
    citizen = person.get("citizen", False)
    experience = person.get("experience_years", 0)

    results = {}

    # Chained comparison
    results["age_valid"] = 18 <= age <= 65

    # Logical operators
    results["academic"] = gpa >= 3.5 and age < 30

    # Complex condition with short-circuit
    results["eligible"] = (
        citizen
        and 18 <= age <= 65
        and (gpa >= 3.0 or experience >= 5)
    )

    # Ternary
    results["category"] = "senior" if experience >= 10 else "mid" if experience >= 5 else "junior"

    return name, results

# Test with different profiles
profiles = [
    {"name": "Alice", "age": 25, "gpa": 3.8, "citizen": True, "experience_years": 3},
    {"name": "Bob", "age": 17, "gpa": 3.9, "citizen": True, "experience_years": 0},
    {"name": "Carol", "age": 45, "gpa": 2.5, "citizen": True, "experience_years": 20},
    {"name": "Dave", "age": 30, "gpa": 3.5, "citizen": False, "experience_years": 8},
]

for profile in profiles:
    name, results = evaluate_eligibility(profile)
    print(f"\n  {name}:")
    for key, value in results.items():
        print(f"    {key:<12}: {value}")

# Explanation: This combines all operators covered in this file:
# comparison (>=, <=), chained (18 <= age <= 65), logical (and, or),
# short-circuit (citizen checked first), ternary (category assignment),
# and membership (dict.get for safe access). Real-world code often
# combines these operators in eligibility checks, filters, and rules.
