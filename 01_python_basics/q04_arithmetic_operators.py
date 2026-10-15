"""
Topic 01: Python Basics
Question 04: Arithmetic Operators

Master all arithmetic operators, operator precedence,
division quirks, and practical math operations.
"""

# ============================================================
# Q1: All arithmetic operators demonstration
# ============================================================
# Question: Demonstrate +, -, *, /, //, %, ** with examples
# and show the difference between / and //.

print("=== Q1: Arithmetic Operators ===")
a, b = 17, 5

print(f"  a = {a}, b = {b}")
print(f"  a + b  = {a + b}")      # 22 (addition)
print(f"  a - b  = {a - b}")      # 12 (subtraction)
print(f"  a * b  = {a * b}")      # 85 (multiplication)
print(f"  a / b  = {a / b}")      # 3.4 (true division - always float)
print(f"  a // b = {a // b}")     # 3 (floor division - rounds DOWN)
print(f"  a % b  = {a % b}")      # 2 (modulo - remainder)
print(f"  a ** b = {a ** b}")     # 1419857 (exponentiation)

# Key difference: / vs //
print(f"\n  Division details:")
print(f"  10 / 3  = {10 / 3}")    # 3.3333...
print(f"  10 // 3 = {10 // 3}")   # 3 (floor, not truncate)
print(f"  10 / 2  = {10 / 2}")    # 5.0 (still float!)
print(f"  10 // 2 = {10 // 2}")   # 5 (int when both operands are int)

# Explanation: True division (/) ALWAYS returns float, even for 10/2.
# Floor division (//) rounds toward negative infinity (not toward zero).
# This distinction matters for negative numbers (see Q2).


# ============================================================
# Q2: Negative number division and modulo
# ============================================================
# Question: Show how // and % behave with negative numbers.
# Compare Python's behavior with other languages.

print("\n=== Q2: Negative Division and Modulo ===")

test_cases = [(7, 3), (-7, 3), (7, -3), (-7, -3)]

print(f"  {'a':>4} {'b':>4} {'a/b':>8} {'a//b':>6} {'a%b':>5} {'verify':>10}")
print(f"  {'-'*4} {'-'*4} {'-'*8} {'-'*6} {'-'*5} {'-'*10}")

for a, b in test_cases:
    div = a / b
    floor_div = a // b
    mod = a % b
    # The invariant: a == (a // b) * b + (a % b)
    verify = floor_div * b + mod
    print(f"  {a:>4} {b:>4} {div:>8.4f} {floor_div:>6} {mod:>5} {verify:>10}")

print(f"\n  Invariant: a == (a // b) * b + (a % b)")
print(f"  Python's // rounds toward -infinity (floor)")
print(f"  C/Java's // truncates toward 0")
print(f"\n  Example: -7 // 3 = {-7 // 3} (floor), C would give {int(-7/3)} (truncate)")

# Explanation: Python's // is true floor division (toward -inf).
# The modulo result always has the same sign as the divisor.
# This is mathematically cleaner than C's truncation behavior.
# The invariant a == (a//b)*b + (a%b) always holds in Python.


# ============================================================
# Q3: Operator precedence
# ============================================================
# Question: Demonstrate PEMDAS/operator precedence rules.
# Show cases where precedence causes unexpected results.

print("\n=== Q3: Operator Precedence ===")

# Without parentheses
expr1 = 2 + 3 * 4
print(f"  2 + 3 * 4     = {expr1} (not 20, * before +)")

expr2 = 2 ** 3 ** 2
print(f"  2 ** 3 ** 2   = {expr2} (right-associative: 2**(3**2) = 2**9 = 512)")

expr3 = -2 ** 2
print(f"  -2 ** 2       = {expr3} (** binds tighter than unary -, so -(2**2))")

expr4 = (-2) ** 2
print(f"  (-2) ** 2     = {expr4} (parentheses fix it)")

# Mixed operations
expr5 = 10 + 20 * 30 / 10 - 5
print(f"  10 + 20*30/10 - 5 = {expr5}")

# Precedence table (high to low):
# ** (exponentiation, right-associative)
# +x, -x, ~x (unary)
# *, /, //, % (multiplication/division)
# +, - (addition/subtraction)

# Practical: Calculate compound interest
principal = 10000
rate = 0.08
years = 5
amount = principal * (1 + rate) ** years
print(f"\n  Compound interest:")
print(f"  Principal: {principal}, Rate: {rate}, Years: {years}")
print(f"  Amount = P * (1 + r)^n = {amount:.2f}")

# Explanation: Python follows standard math precedence (PEMDAS).
# ** is right-associative: 2**3**2 = 2**(3**2) = 512, not (2**3)**2 = 64.
# Unary minus has LOWER precedence than **: -2**2 = -(4) = -4.
# When in doubt, use parentheses for clarity.


# ============================================================
# Q4: divmod() and practical remainder applications
# ============================================================
# Question: Use divmod() for efficient quotient+remainder.
# Build practical converters (time, currency, etc.)

print("\n=== Q4: divmod() and Practical Uses ===")

# Basic divmod
q, r = divmod(17, 5)
print(f"  divmod(17, 5) = ({q}, {r})")

# Time conversion
total_seconds = 3661
hours, remainder = divmod(total_seconds, 3600)
minutes, seconds = divmod(remainder, 60)
print(f"  {total_seconds} seconds = {hours}h {minutes}m {seconds}s")

# Money: convert cents to dollars and cents
total_cents = 1599
dollars, cents = divmod(total_cents, 100)
print(f"  {total_cents} cents = ${dollars}.{cents:02d}")

# Convert decimal to any base
def to_base(number, base):
    """Convert a positive integer to any base (2-36)."""
    if number == 0:
        return "0"
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = []
    while number > 0:
        number, remainder = divmod(number, base)
        result.append(digits[remainder])
    return ''.join(reversed(result))

print(f"\n  Custom base conversion:")
print(f"  255 in base 2:  {to_base(255, 2)}")
print(f"  255 in base 8:  {to_base(255, 8)}")
print(f"  255 in base 16: {to_base(255, 16)}")
print(f"  100 in base 3:  {to_base(100, 3)}")

# Explanation: divmod(a, b) returns (a // b, a % b) in one operation.
# It's both cleaner and slightly faster than computing // and % separately.
# Perfect for unit conversions (time, currency, bases).


# ============================================================
# Q5: Augmented assignment operators
# ============================================================
# Question: Demonstrate +=, -=, *=, /=, //=, %=, **=
# and show they modify in place for mutable types.

print("\n=== Q5: Augmented Assignment Operators ===")

x = 10
print(f"  Start: x = {x}")

x += 5    # x = x + 5
print(f"  x += 5  -> x = {x}")

x -= 3    # x = x - 3
print(f"  x -= 3  -> x = {x}")

x *= 2    # x = x * 2
print(f"  x *= 2  -> x = {x}")

x //= 3   # x = x // 3
print(f"  x //= 3 -> x = {x}")

x **= 2   # x = x ** 2
print(f"  x **= 2 -> x = {x}")

x %= 5    # x = x % 5
print(f"  x %%= 5  -> x = {x}")

# Important: for immutable types, += creates a new object
a = "hello"
id_before = id(a)
a += " world"
id_after = id(a)
print(f"\n  String += creates new object: {id_before != id_after}")

# For mutable types, += modifies in place
b = [1, 2, 3]
id_before = id(b)
b += [4, 5]
id_after = id(b)
print(f"  List += modifies in place: {id_before == id_after}")

# Explanation: For immutable types (int, str, tuple), augmented assignment
# creates a new object and rebinds the variable. For mutable types (list),
# it calls __iadd__ which modifies the object in place. This difference
# matters when objects are shared (aliased) by multiple variables.


# ============================================================
# Q6: Integer division edge cases
# ============================================================
# Question: Explore division by zero, large numbers,
# floating-point division precision issues.

print("\n=== Q6: Division Edge Cases ===")

# Division by zero
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"  10 / 0:  ZeroDivisionError: {e}")

try:
    result = 10 // 0
except ZeroDivisionError as e:
    print(f"  10 // 0: ZeroDivisionError: {e}")

try:
    result = 10 % 0
except ZeroDivisionError as e:
    print(f"  10 %% 0:  ZeroDivisionError: {e}")

# Float division oddities
print(f"\n  Float precision issues:")
print(f"  0.1 + 0.2 = {0.1 + 0.2}")            # Not exactly 0.3!
print(f"  0.1 + 0.2 == 0.3: {0.1 + 0.2 == 0.3}")  # False!

# Proper float comparison
import math
print(f"  math.isclose(0.1 + 0.2, 0.3): {math.isclose(0.1 + 0.2, 0.3)}")

# Using Decimal for exact arithmetic
from decimal import Decimal
d1 = Decimal('0.1') + Decimal('0.2')
print(f"  Decimal('0.1') + Decimal('0.2') = {d1}")
print(f"  == Decimal('0.3'): {d1 == Decimal('0.3')}")

# Large number division
big = 10 ** 50
print(f"\n  10^50 / 7 = {big / 7:.2f}")
print(f"  10^50 // 7 = {big // 7}")

# Explanation: Floating-point numbers use IEEE 754 binary representation.
# 0.1 can't be exactly represented in binary, causing precision issues.
# Use math.isclose() for float comparison, or decimal.Decimal for exact
# decimal arithmetic (financial calculations, etc.).


# ============================================================
# Q7: The math module essentials
# ============================================================
# Question: Demonstrate the most useful functions from the math module.

import math

print("\n=== Q7: Math Module Essentials ===")

# Rounding functions
print(f"  math.floor(3.7)  = {math.floor(3.7)}")
print(f"  math.ceil(3.2)   = {math.ceil(3.2)}")
print(f"  math.trunc(-3.7) = {math.trunc(-3.7)}")
print(f"  round(3.5)       = {round(3.5)} (banker's rounding)")

# Powers and roots
print(f"\n  math.sqrt(144)   = {math.sqrt(144)}")
print(f"  math.pow(2, 10)  = {math.pow(2, 10)}")
print(f"  math.log(100, 10)= {math.log(100, 10)}")
print(f"  math.log2(1024)  = {math.log2(1024)}")

# Constants
print(f"\n  math.pi  = {math.pi}")
print(f"  math.e   = {math.e}")
print(f"  math.inf = {math.inf}")
print(f"  math.nan = {math.nan}")

# Useful checks
print(f"\n  math.isinf(math.inf)  = {math.isinf(math.inf)}")
print(f"  math.isnan(math.nan)  = {math.isnan(math.nan)}")
print(f"  math.isfinite(3.14)   = {math.isfinite(3.14)}")

# GCD and LCM
print(f"\n  math.gcd(48, 18)  = {math.gcd(48, 18)}")
print(f"  math.lcm(4, 6)    = {math.lcm(4, 6)}")  # Python 3.9+

# Factorial and combinatorics
print(f"  math.factorial(10) = {math.factorial(10)}")
print(f"  math.comb(10, 3)   = {math.comb(10, 3)}")   # C(10,3)
print(f"  math.perm(10, 3)   = {math.perm(10, 3)}")   # P(10,3)

# Explanation: The math module provides C-level fast implementations of
# mathematical functions. Use math.isclose() for float comparison.
# math.gcd/lcm are essential for number theory problems.
# math.comb/perm (Python 3.8+) are useful for combinatorics.


# ============================================================
# Q8: Bitwise operators
# ============================================================
# Question: Demonstrate &, |, ^, ~, <<, >> with practical examples.

print("\n=== Q8: Bitwise Operators ===")

a, b = 12, 10  # 1100, 1010 in binary
print(f"  a = {a} ({a:04b}), b = {b} ({b:04b})")
print(f"  a & b  = {a & b:>2} ({a & b:04b})  AND")
print(f"  a | b  = {a | b:>2} ({a | b:04b})  OR")
print(f"  a ^ b  = {a ^ b:>2} ({a ^ b:04b})  XOR")
print(f"  ~a     = {~a:>2} (NOT, flips all bits)")
print(f"  a << 2 = {a << 2:>2} ({a << 2:08b})  Left shift (multiply by 4)")
print(f"  a >> 1 = {a >> 1:>2} ({a >> 1:04b})  Right shift (divide by 2)")

# Practical: Check if a number is even/odd with bitwise AND
for n in range(6):
    parity = "odd" if n & 1 else "even"
    print(f"  {n} & 1 = {n & 1} -> {parity}")

# Practical: Swap without temp using XOR
x, y = 5, 3
x ^= y
y ^= x
x ^= y
print(f"\n  XOR swap: x=5, y=3 -> x={x}, y={y}")

# Practical: Power of 2 check
def is_power_of_2(n):
    return n > 0 and (n & (n - 1)) == 0

for n in [1, 2, 3, 4, 8, 16, 15, 0]:
    print(f"  is_power_of_2({n:>2}) = {is_power_of_2(n)}")

# Explanation: Bitwise operations work on the binary representation.
# n & 1 is the fastest way to check even/odd.
# n & (n-1) == 0 checks if n is a power of 2 (only one bit set).
# Left shift by k multiplies by 2^k; right shift divides by 2^k.


# ============================================================
# Q9: The abs(), pow(), and round() built-in functions
# ============================================================
# Question: Explore built-in numeric functions and their edge cases.

print("\n=== Q9: Built-in Numeric Functions ===")

# abs() -- absolute value
print(f"  abs(-5)    = {abs(-5)}")
print(f"  abs(5)     = {abs(5)}")
print(f"  abs(-3.14) = {abs(-3.14)}")
print(f"  abs(3+4j)  = {abs(3+4j)}")  # Magnitude of complex number

# pow() -- power with optional modulo
print(f"\n  pow(2, 10)     = {pow(2, 10)}")
print(f"  pow(2, 10, 100)= {pow(2, 10, 100)}")  # (2**10) % 100, faster
print(f"  2 ** 10 % 100  = {2 ** 10 % 100}")     # Same result, slower

# Modular exponentiation is crucial for cryptography
# pow(base, exp, mod) is O(log exp), much faster than (base**exp) % mod
import time
base, exp, mod = 2, 100000, 1000000007
start = time.perf_counter()
result = pow(base, exp, mod)
elapsed = time.perf_counter() - start
print(f"  pow(2, 100000, 10^9+7) = {result} ({elapsed:.6f}s)")

# round() with precision
print(f"\n  round(3.14159, 2) = {round(3.14159, 2)}")
print(f"  round(3.14159, 4) = {round(3.14159, 4)}")
print(f"  round(1234, -2)   = {round(1234, -2)}")   # Round to hundreds
print(f"  round(1250, -2)   = {round(1250, -2)}")   # Banker's rounding

# Explanation: pow(base, exp, mod) computes modular exponentiation
# efficiently using fast exponentiation (O(log n)). This is crucial
# in cryptography (RSA, Diffie-Hellman). round() with negative ndigits
# rounds to tens, hundreds, etc.


# ============================================================
# Q10: Build a calculator with proper error handling
# ============================================================
# Question: Create a command-line calculator that handles all
# arithmetic operations with edge cases.

print("\n=== Q10: Calculator with Edge Cases ===")

def calculate(a, operator, b):
    """Perform arithmetic with comprehensive error handling."""
    operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y if y != 0 else "Error: Division by zero",
        '//': lambda x, y: x // y if y != 0 else "Error: Division by zero",
        '%': lambda x, y: x % y if y != 0 else "Error: Division by zero",
        '**': lambda x, y: x ** y,
    }

    if operator not in operations:
        return f"Error: Unknown operator '{operator}'"

    try:
        result = operations[operator](a, b)
        # Check for overflow/infinity
        if isinstance(result, float) and (math.isinf(result) or math.isnan(result)):
            return f"Error: Result is {result}"
        return result
    except OverflowError:
        return "Error: Result too large"
    except Exception as e:
        return f"Error: {e}"

# Test the calculator
test_cases = [
    (10, '+', 5),
    (10, '-', 20),
    (3, '*', 7),
    (10, '/', 3),
    (10, '/', 0),
    (10, '//', 3),
    (-7, '//', 2),
    (17, '%', 5),
    (2, '**', 100),
    (2, '**', -1),
    (0, '**', 0),
    (10, '&', 5),  # Invalid operator
]

for a, op, b in test_cases:
    result = calculate(a, op, b)
    print(f"  {a} {op:>2} {b} = {result}")

# Explanation: This calculator uses a dictionary of lambda functions
# for operator dispatch (cleaner than if/elif chains). It pre-checks
# for division by zero and post-checks for infinity/NaN. The dictionary
# approach is extensible -- adding new operations is trivial.
