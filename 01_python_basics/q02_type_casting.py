"""
Topic 01: Python Basics
Question 02: Type Casting and Conversion

Learn how to convert between Python's built-in types safely,
handle edge cases, and understand implicit vs explicit conversion.
"""

# ============================================================
# Q1: Basic int/float/str conversions
# ============================================================
# Question: Convert between int, float, and str. Show what
# happens with truncation (float -> int) and precision.

print("=== Q1: Basic Type Conversions ===")
# String to int
age_str = "25"
age_int = int(age_str)
print(f"  int('25')     = {age_int} (type: {type(age_int).__name__})")

# String to float
price_str = "19.99"
price_float = float(price_str)
print(f"  float('19.99')= {price_float} (type: {type(price_float).__name__})")

# Float to int (truncates, does NOT round)
pi = 3.99
pi_int = int(pi)
print(f"  int(3.99)     = {pi_int}  (truncates toward zero, NOT rounds)")

# Negative float to int
neg = -3.7
neg_int = int(neg)
print(f"  int(-3.7)     = {neg_int} (truncates toward zero)")

# Int to float
num = 42
num_float = float(num)
print(f"  float(42)     = {num_float}")

# Number to string
print(f"  str(42)       = {str(42)!r}")
print(f"  str(3.14)     = {str(3.14)!r}")

# Explanation: int() truncates toward zero (not floor!). For -3.7,
# int() gives -3 (toward zero), while math.floor() would give -4.
# Output:
#   int('25')     = 25 (type: int)
#   float('19.99')= 19.99 (type: float)
#   int(3.99)     = 3  (truncates toward zero, NOT rounds)


# ============================================================
# Q2: Handle invalid conversions gracefully
# ============================================================
# Question: Try to convert invalid strings to numbers and handle
# the ValueError. Write a safe conversion function.

print("\n=== Q2: Safe Conversion with Error Handling ===")

def safe_int(value, default=0):
    """Convert value to int safely, returning default on failure."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    """Convert value to float safely, returning default on failure."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

test_cases = ["42", "3.14", "hello", "", None, "  100  ", True, [1, 2]]
for val in test_cases:
    print(f"  safe_int({val!r:>12}) = {safe_int(val):<6}  "
          f"safe_float({val!r:>12}) = {safe_float(val)}")

# Explanation: ValueError occurs when the string format is wrong.
# TypeError occurs when the type itself can't be converted (like None).
# Note: int("3.14") raises ValueError -- you need int(float("3.14")).
# "  100  " works with int() because it strips whitespace automatically.


# ============================================================
# Q3: Boolean conversion rules
# ============================================================
# Question: Show exactly which values are truthy and falsy in Python.
# Demonstrate bool() on various types.

print("\n=== Q3: Boolean Conversion (Truthy/Falsy) ===")

falsy_values = [0, 0.0, 0j, "", [], (), {}, set(), None, False, range(0)]
truthy_values = [1, -1, 0.1, "hello", [0], (0,), {"": ""}, {0}, True, range(1)]

print("  Falsy values:")
for val in falsy_values:
    print(f"    bool({str(val):<12}) = {bool(val)}")

print("  Truthy values:")
for val in truthy_values:
    print(f"    bool({str(val):<12}) = {bool(val)}")

# Edge case: Custom objects are truthy unless __bool__ or __len__ says otherwise
class AlwaysFalse:
    def __bool__(self):
        return False

obj = AlwaysFalse()
print(f"  bool(AlwaysFalse()) = {bool(obj)}")

# Explanation: Python's truthiness rules:
# Falsy: 0, 0.0, empty sequences/mappings, None, False
# Truthy: Everything else, including negative numbers and [0]
# Custom classes can define __bool__() or __len__() to control this.


# ============================================================
# Q4: ord() and chr() -- character/integer conversion
# ============================================================
# Question: Convert between characters and their Unicode code points.
# Build a simple Caesar-like shift using ord/chr.

print("\n=== Q4: Character <-> Integer (ord/chr) ===")

# Basic conversions
print(f"  ord('A') = {ord('A')}")   # 65
print(f"  ord('a') = {ord('a')}")   # 97
print(f"  ord('0') = {ord('0')}")   # 48
print(f"  chr(65)  = {chr(65)!r}")  # 'A'
print(f"  chr(8364)= {chr(8364)!r}")  # Euro sign

# Shift each letter by 1
word = "Hello"
shifted = "".join(chr(ord(c) + 1) for c in word)
print(f"  Shifting '{word}' by +1: '{shifted}'")

# Get ASCII values of a string
text = "Python"
ascii_vals = [ord(c) for c in text]
print(f"  ASCII values of '{text}': {ascii_vals}")

# Explanation: ord() returns the Unicode code point of a single character.
# chr() does the reverse. ASCII letters A-Z are 65-90, a-z are 97-122,
# digits 0-9 are 48-57. This is fundamental for encryption and text processing.


# ============================================================
# Q5: Number base conversions (bin, oct, hex, int with base)
# ============================================================
# Question: Convert numbers between decimal, binary, octal, and hex.
# Show both directions of conversion.

print("\n=== Q5: Number Base Conversions ===")

num = 255
print(f"  Decimal {num}:")
print(f"    Binary : {bin(num)}")      # '0b11111111'
print(f"    Octal  : {oct(num)}")      # '0o377'
print(f"    Hex    : {hex(num)}")      # '0xff'

# Convert back to decimal using int() with base
print(f"\n  Back to decimal:")
print(f"    int('11111111', 2) = {int('11111111', 2)}")
print(f"    int('377', 8)      = {int('377', 8)}")
print(f"    int('ff', 16)      = {int('ff', 16)}")
print(f"    int('0xff', 16)    = {int('0xff', 16)}")  # prefix OK too

# Formatting without the 0b/0o/0x prefix
print(f"\n  Formatted (no prefix):")
print(f"    Binary : {num:08b}")
print(f"    Octal  : {num:o}")
print(f"    Hex    : {num:02x} (lowercase), {num:02X} (uppercase)")

# Explanation: bin(), oct(), hex() return string representations with
# prefixes. int(string, base) parses any base from 2 to 36.
# Format specs like :b, :o, :x give the digits without prefixes.


# ============================================================
# Q6: Implicit type coercion in arithmetic
# ============================================================
# Question: Show how Python automatically promotes types in
# mixed-type arithmetic (int + float, bool + int, etc.)

print("\n=== Q6: Implicit Type Coercion ===")

# int + float -> float
result1 = 5 + 3.0
print(f"  5 + 3.0     = {result1} (type: {type(result1).__name__})")

# int + bool -> int
result2 = 10 + True
print(f"  10 + True   = {result2} (type: {type(result2).__name__})")

# float + bool -> float
result3 = 1.5 + False
print(f"  1.5 + False = {result3} (type: {type(result3).__name__})")

# int + complex -> complex
result4 = 3 + 2j
print(f"  3 + 2j      = {result4} (type: {type(result4).__name__})")

# int / int -> float (true division)
result5 = 10 / 3
print(f"  10 / 3      = {result5} (type: {type(result5).__name__})")

# int // int -> int (floor division)
result6 = 10 // 3
print(f"  10 // 3     = {result6} (type: {type(result6).__name__})")

# Explanation: Python's numeric tower: bool < int < float < complex.
# In mixed operations, the "wider" type wins. True division (/)
# ALWAYS returns float, even for 10/2. Floor division (//) returns
# int only if both operands are int.


# ============================================================
# Q7: String to list and list to string
# ============================================================
# Question: Convert between strings and lists using split(), join(),
# and list(). Show common real-world patterns.

print("\n=== Q7: String <-> List Conversions ===")

# String to list of characters
text = "Python"
chars = list(text)
print(f"  list('Python')        = {chars}")

# String to list of words
sentence = "Hello World from Python"
words = sentence.split()
print(f"  'Hello World...'.split()  = {words}")

# CSV-like splitting
csv_line = "Alice,30,Engineer"
fields = csv_line.split(",")
print(f"  CSV split: {fields}")

# List to string
joined = " ".join(words)
print(f"  ' '.join(words)      = {joined!r}")

# List of numbers to string (must convert elements first)
numbers = [1, 2, 3, 4, 5]
num_str = ", ".join(str(n) for n in numbers)
print(f"  Join numbers: {num_str!r}")

# Edge cases
print(f"  ''.split()           = {''.split()}")           # []
print(f"  '  '.split()         = {'  '.split()}")         # []
print(f"  'a,,b'.split(',')    = {'a,,b'.split(',')}")    # ['a', '', 'b']

# Explanation: split() without args splits on whitespace and removes empties.
# split(',') splits on exact delimiter (keeps empties between delimiters).
# join() requires all elements to be strings -- use a generator expression
# to convert non-strings first.


# ============================================================
# Q8: round(), int(), math.floor(), math.ceil() comparison
# ============================================================
# Question: Compare all four ways to convert float to int.
# Show banker's rounding and its implications.

import math

print("\n=== Q8: Float-to-Int Conversion Methods ===")

test_values = [2.3, 2.5, 2.7, 3.5, -2.3, -2.5, -2.7, 0.5, 1.5]

print(f"  {'Value':>6} {'int()':>6} {'round()':>8} {'floor()':>8} {'ceil()':>7}")
print(f"  {'-'*6} {'-'*6} {'-'*8} {'-'*8} {'-'*7}")
for v in test_values:
    print(f"  {v:>6.1f} {int(v):>6} {round(v):>8} "
          f"{math.floor(v):>8} {math.ceil(v):>7}")

# Banker's rounding: round() rounds to EVEN on .5
print(f"\n  Banker's rounding (rounds to even):")
print(f"  round(0.5) = {round(0.5)}  (rounds to 0, not 1)")
print(f"  round(1.5) = {round(1.5)}  (rounds to 2)")
print(f"  round(2.5) = {round(2.5)}  (rounds to 2, not 3)")
print(f"  round(3.5) = {round(3.5)}  (rounds to 4)")

# Explanation:
# int()        -> truncates toward zero
# round()      -> banker's rounding (round half to even)
# math.floor() -> always rounds DOWN (toward negative infinity)
# math.ceil()  -> always rounds UP (toward positive infinity)
# Banker's rounding reduces bias in statistical calculations.


# ============================================================
# Q9: bytes and string encoding/decoding
# ============================================================
# Question: Convert between str and bytes using encode/decode.
# Handle encoding errors gracefully.

print("\n=== Q9: String <-> Bytes Encoding ===")

# Basic encode/decode
text = "Hello, Python!"
encoded = text.encode("utf-8")
print(f"  Original:  {text!r}")
print(f"  Encoded:   {encoded}")
print(f"  Type:      {type(encoded).__name__}")
print(f"  Decoded:   {encoded.decode('utf-8')!r}")

# Different encodings produce different bytes
word = "cafe"
for encoding in ["utf-8", "ascii", "utf-16"]:
    try:
        b = word.encode(encoding)
        print(f"  '{word}'.encode('{encoding}'): {b} ({len(b)} bytes)")
    except UnicodeEncodeError as e:
        print(f"  '{word}'.encode('{encoding}'): ERROR - {e}")

# Handling errors
problematic = "Hello \x80 World"  # Contains a problematic character
for errors in ["strict", "ignore", "replace"]:
    try:
        result = problematic.encode("ascii", errors=errors)
        print(f"  encode(ascii, {errors:>8}): {result}")
    except UnicodeEncodeError:
        print(f"  encode(ascii, {errors:>8}): UnicodeEncodeError raised")

# Explanation: Strings in Python 3 are Unicode. bytes are raw byte sequences.
# encode() converts str -> bytes, decode() converts bytes -> str.
# UTF-8 is the most common encoding. The 'errors' parameter controls
# behavior for unencodable characters: 'strict' raises, 'ignore' skips,
# 'replace' substitutes with '?'.


# ============================================================
# Q10: Complex type chain conversions and practical patterns
# ============================================================
# Question: Demonstrate multi-step conversions and practical
# type-casting patterns used in real programs.

print("\n=== Q10: Practical Type Conversion Patterns ===")

# Pattern 1: Parsing "yes/no" to boolean
def parse_bool(value):
    """Convert various representations to boolean."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower().strip() in ("yes", "true", "1", "on", "y")
    return bool(value)

for val in ["yes", "YES", "no", "True", "1", "0", "on", "", True, False]:
    print(f"  parse_bool({val!r:>8}) = {parse_bool(val)}")

# Pattern 2: Safe numeric parsing with units
def parse_measurement(text):
    """Parse strings like '5.2kg', '100cm' into (value, unit)."""
    text = text.strip()
    i = 0
    while i < len(text) and (text[i].isdigit() or text[i] == '.'):
        i += 1
    if i == 0:
        return None, text
    return float(text[:i]), text[i:].strip()

measurements = ["5.2kg", "100cm", "3.14m", "no_number", "42"]
for m in measurements:
    value, unit = parse_measurement(m)
    print(f"  parse_measurement({m!r:>14}) = ({value}, {unit!r})")

# Pattern 3: Convert list of mixed types to uniform type
mixed = [1, "2", 3.0, True, "4.5"]
as_floats = [float(x) for x in mixed]
print(f"\n  Mixed: {mixed}")
print(f"  As floats: {as_floats}")

# Pattern 4: Two's complement understanding
# Converting negative numbers to their binary representation
for n in [5, -5, 127, -128]:
    if n >= 0:
        print(f"  {n:>4} in 8-bit binary: {n:08b}")
    else:
        # Show two's complement for negative
        twos = n & 0xFF  # Mask to 8 bits
        print(f"  {n:>4} in 8-bit binary: {twos:08b} (two's complement)")

# Explanation: Real-world type casting goes beyond simple int()/str().
# Pattern 1 handles user input normalization.
# Pattern 2 extracts numbers from strings with units.
# Pattern 3 normalizes heterogeneous data.
# Pattern 4 shows how negative numbers work at the binary level.
