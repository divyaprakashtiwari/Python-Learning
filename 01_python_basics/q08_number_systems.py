"""
Topic 01: Python Basics
Question 08: Number Systems and Conversions

Master binary, octal, hexadecimal systems, bitwise manipulation,
IEEE 754 floats, and practical encoding/decoding patterns.
"""

# ============================================================
# Q1: Number system fundamentals
# ============================================================
# Question: Create numbers in different bases and convert between them.
# Show the relationship between positional notation and value.

print("=== Q1: Number System Fundamentals ===")

# Literal notations in Python
decimal = 255
binary = 0b11111111
octal = 0o377
hexadecimal = 0xFF

print(f"  Decimal:     {decimal}")
print(f"  Binary:      {binary}  (0b11111111)")
print(f"  Octal:       {octal}  (0o377)")
print(f"  Hex:         {hexadecimal}  (0xFF)")
print(f"  All equal:   {decimal == binary == octal == hexadecimal}")

# Positional value breakdown
print(f"\n  Binary 11111111 breakdown:")
for i in range(7, -1, -1):
    bit = 1
    value = bit * (2 ** i)
    print(f"    Bit {i}: {bit} x 2^{i} = {value}")
print(f"    Total: {sum(2**i for i in range(8))}")

# Explanation: Python supports four number base literals:
# decimal (no prefix), binary (0b), octal (0o), hex (0x/0X).
# All are stored internally as the same integer type.
# Positional notation: each digit's value = digit * base^position.


# ============================================================
# Q2: Custom base converter
# ============================================================
# Question: Build a function that converts any integer to any
# base (2-36) and back.

print("\n=== Q2: Universal Base Converter ===")

def to_base(number, base):
    """Convert a non-negative integer to any base (2-36)."""
    if base < 2 or base > 36:
        raise ValueError(f"Base must be 2-36, got {base}")
    if number == 0:
        return "0"

    negative = number < 0
    number = abs(number)
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = []

    while number > 0:
        number, remainder = divmod(number, base)
        result.append(digits[remainder])

    if negative:
        result.append('-')
    return ''.join(reversed(result))

def from_base(string, base):
    """Convert a string representation in given base to integer."""
    return int(string, base)

# Test conversions
test_values = [0, 1, 10, 42, 255, 1000, 65535]
bases = [2, 8, 10, 16, 36]

print(f"  {'Dec':>6}", end="")
for b in bases:
    print(f"  {'Base'+str(b):>12}", end="")
print()

for val in test_values:
    print(f"  {val:>6}", end="")
    for b in bases:
        print(f"  {to_base(val, b):>12}", end="")
    print()

# Verify round-trip
print(f"\n  Round-trip verification:")
for val in [42, 255, 1000]:
    for b in [2, 8, 16, 36]:
        converted = to_base(val, b)
        restored = from_base(converted, b)
        status = "OK" if restored == val else "FAIL"
        print(f"    {val} -> base {b}: {converted} -> {restored} [{status}]")

# Explanation: divmod(number, base) repeatedly extracts digits from right
# to left. Base 36 uses digits 0-9 and letters A-Z (0-35).
# int(string, base) is the built-in way to parse any base.


# ============================================================
# Q3: Bit manipulation patterns
# ============================================================
# Question: Demonstrate common bit manipulation techniques:
# set, clear, toggle, check bits.

print("\n=== Q3: Bit Manipulation Patterns ===")

def show_bits(n, width=8):
    """Show a number's binary representation."""
    if n < 0:
        n = n & ((1 << width) - 1)
    return f"{n:0{width}b}"

# Set a bit (make it 1)
def set_bit(n, pos):
    return n | (1 << pos)

# Clear a bit (make it 0)
def clear_bit(n, pos):
    return n & ~(1 << pos)

# Toggle a bit (flip it)
def toggle_bit(n, pos):
    return n ^ (1 << pos)

# Check a bit (is it 1?)
def check_bit(n, pos):
    return bool(n & (1 << pos))

n = 0b10101010  # 170
print(f"  Original:       {show_bits(n)} ({n})")
print(f"  Set bit 0:      {show_bits(set_bit(n, 0))} ({set_bit(n, 0)})")
print(f"  Clear bit 7:    {show_bits(clear_bit(n, 7))} ({clear_bit(n, 7)})")
print(f"  Toggle bit 4:   {show_bits(toggle_bit(n, 4))} ({toggle_bit(n, 4)})")
print(f"  Bit 7 is set:   {check_bit(n, 7)}")
print(f"  Bit 0 is set:   {check_bit(n, 0)}")

# Count set bits (population count)
def count_bits(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

# Using bin().count('1')
for val in [0, 1, 7, 255, 1024]:
    print(f"  Bits in {val:>5}: {count_bits(val)} (verify: {bin(val).count('1')})")

# Explanation: Bit operations:
# Set:    n | (1 << pos)   -- OR with mask
# Clear:  n & ~(1 << pos)  -- AND with inverted mask
# Toggle: n ^ (1 << pos)   -- XOR with mask
# Check:  n & (1 << pos)   -- AND with mask


# ============================================================
# Q4: Practical bitwise applications
# ============================================================
# Question: Use bit flags for permissions, colors, and feature toggles.

print("\n=== Q4: Bit Flags for Permissions ===")

# Unix-style file permissions
READ = 0b100    # 4
WRITE = 0b010   # 2
EXEC = 0b001    # 1

def permission_string(perm):
    """Convert permission bits to rwx string."""
    r = 'r' if perm & READ else '-'
    w = 'w' if perm & WRITE else '-'
    x = 'x' if perm & EXEC else '-'
    return f"{r}{w}{x}"

# Create permissions
owner = READ | WRITE | EXEC   # 7 (rwx)
group = READ | EXEC           # 5 (r-x)
other = READ                  # 4 (r--)

print(f"  Owner:  {show_bits(owner, 3)} -> {permission_string(owner)} ({owner})")
print(f"  Group:  {show_bits(group, 3)} -> {permission_string(group)} ({group})")
print(f"  Other:  {show_bits(other, 3)} -> {permission_string(other)} ({other})")
print(f"  chmod:  {owner}{group}{other}")

# Feature flags
FEATURE_DARK_MODE = 1 << 0    # 1
FEATURE_BETA = 1 << 1         # 2
FEATURE_ANALYTICS = 1 << 2    # 4
FEATURE_AI = 1 << 3           # 8

user_flags = FEATURE_DARK_MODE | FEATURE_AI
print(f"\n  User features: {show_bits(user_flags, 4)}")
print(f"  Dark mode: {bool(user_flags & FEATURE_DARK_MODE)}")
print(f"  Beta:      {bool(user_flags & FEATURE_BETA)}")
print(f"  Analytics: {bool(user_flags & FEATURE_ANALYTICS)}")
print(f"  AI:        {bool(user_flags & FEATURE_AI)}")

# Explanation: Bit flags compactly store multiple boolean values in one int.
# Unix permissions use 3 bits per group (rwx). Feature flags are common in
# software for toggling features without code changes. Each flag is a power
# of 2 so they don't overlap.


# ============================================================
# Q5: IEEE 754 floating-point representation
# ============================================================
# Question: Explore how floats are stored in binary and why
# precision issues occur.

import struct

print("\n=== Q5: IEEE 754 Float Internals ===")

def float_to_binary(f):
    """Show the IEEE 754 binary representation of a float."""
    packed = struct.pack('>d', f)  # Big-endian double
    bits = ''.join(f'{byte:08b}' for byte in packed)
    sign = bits[0]
    exponent = bits[1:12]
    mantissa = bits[12:]
    return sign, exponent, mantissa

values = [1.0, -1.0, 0.5, 0.1, 3.14, float('inf'), 0.0]
for val in values:
    sign, exp, mant = float_to_binary(val)
    print(f"  {val:>8} -> sign:{sign} exp:{exp} mantissa:{mant[:20]}...")

# Why 0.1 + 0.2 != 0.3
print(f"\n  Precision demonstration:")
print(f"  0.1 in binary:     {0.1:.55f}")
print(f"  0.2 in binary:     {0.2:.55f}")
print(f"  0.1 + 0.2:         {0.1 + 0.2:.55f}")
print(f"  0.3 exact:         {0.3:.55f}")
print(f"  Difference:        {abs((0.1 + 0.2) - 0.3):.2e}")

# Explanation: IEEE 754 double uses 64 bits: 1 sign, 11 exponent, 52 mantissa.
# Most decimal fractions (like 0.1) can't be exactly represented in binary,
# similar to how 1/3 can't be exact in decimal. This is why floating-point
# arithmetic has precision issues.


# ============================================================
# Q6: Hexadecimal in real-world usage
# ============================================================
# Question: Show practical hex usage: colors, memory addresses,
# hash values, MAC addresses.

print("\n=== Q6: Hex in the Real World ===")

# RGB Colors
def hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    """Convert RGB tuple to hex color string."""
    return f"#{r:02x}{g:02x}{b:02x}"

colors = {
    "Red": "#FF0000", "Green": "#00FF00", "Blue": "#0000FF",
    "White": "#FFFFFF", "Coral": "#FF7F50", "Gold": "#FFD700",
}

print(f"  {'Color':<10} {'Hex':>10} {'RGB':>18}")
for name, hex_val in colors.items():
    rgb = hex_to_rgb(hex_val)
    print(f"  {name:<10} {hex_val:>10} {str(rgb):>18}")

# Verify round-trip
test_rgb = (255, 127, 80)
hex_val = rgb_to_hex(*test_rgb)
back_rgb = hex_to_rgb(hex_val)
print(f"\n  Round-trip: {test_rgb} -> {hex_val} -> {back_rgb}")

# Hash values
import hashlib
text = "Hello, Python!"
md5 = hashlib.md5(text.encode()).hexdigest()
print(f"\n  MD5 of '{text}': {md5}")
print(f"  That's {len(md5) * 4} bits ({len(md5)} hex digits)")

# Memory addresses
x = 42
print(f"\n  id(42) = {id(x)} = {hex(id(x))}")

# Explanation: Hexadecimal is compact (4 bits per digit vs 1 bit for binary).
# Colors use hex because each channel (R,G,B) is 1 byte (0-255 = 00-FF).
# Cryptographic hashes output hex strings. Memory addresses are hex.


# ============================================================
# Q7: Binary data and bytes
# ============================================================
# Question: Work with binary data: bytes, bytearray, memoryview.

print("\n=== Q7: Binary Data Types ===")

# Creating bytes
b1 = b"Hello"                         # bytes literal
b2 = bytes([72, 101, 108, 108, 111])  # from integer list
b3 = bytes.fromhex("48656c6c6f")     # from hex string

print(f"  b'Hello':          {b1}")
print(f"  bytes([72,...]):    {b2}")
print(f"  bytes.fromhex():   {b3}")
print(f"  All equal:         {b1 == b2 == b3}")
print(f"  To hex:            {b1.hex()}")

# bytearray is mutable bytes
ba = bytearray(b"Hello")
ba[0] = ord('J')
print(f"\n  bytearray mutation: {ba}")

# Packing/unpacking structured data
import struct
# Pack: int(4 bytes) + float(4 bytes) + char(1 byte)
packed = struct.pack('>if1s', 42, 3.14, b'A')
print(f"\n  Packed struct:    {packed.hex()}")
print(f"  Size:             {len(packed)} bytes")

unpacked = struct.unpack('>if1s', packed)
print(f"  Unpacked:         {unpacked}")

# Practical: Read/write binary integers
def int_to_bytes(n, length=4, byteorder='big'):
    """Convert integer to bytes."""
    return n.to_bytes(length, byteorder=byteorder)

def bytes_to_int(b, byteorder='big'):
    """Convert bytes to integer."""
    return int.from_bytes(b, byteorder=byteorder)

for val in [0, 1, 255, 1000, 65535]:
    b = int_to_bytes(val, 4)
    restored = bytes_to_int(b)
    print(f"  {val:>6} -> {b.hex()} -> {restored}")

# Explanation: bytes is immutable binary data, bytearray is mutable.
# struct.pack/unpack converts between Python values and C structs.
# int.to_bytes/from_bytes converts integers to/from byte sequences.
# These are essential for binary file formats and network protocols.


# ============================================================
# Q8: Encoding schemes (ASCII, UTF-8, UTF-16)
# ============================================================
# Question: Compare different text encoding schemes and show
# how characters are represented in each.

print("\n=== Q8: Text Encoding Comparison ===")

test_chars = ['A', 'Z', '0', '9', ' ']

print(f"  {'Char':<6} {'Dec':>5} {'Hex':>5} {'Bin':>10} {'UTF-8':>8} {'UTF-16':>12}")
print(f"  {'-'*6} {'-'*5} {'-'*5} {'-'*10} {'-'*8} {'-'*12}")

for char in test_chars:
    code = ord(char)
    utf8 = char.encode('utf-8').hex()
    utf16 = char.encode('utf-16-be').hex()
    print(f"  {char!r:<6} {code:>5} {code:>5x} {code:>10b} {utf8:>8} {utf16:>12}")

# Show UTF-8 variable-length encoding
print(f"\n  UTF-8 variable length demonstration:")
test_strings = [
    ("ASCII 'A'", "A"),
    ("Digits '123'", "123"),
    ("Mixed 'Hi!'", "Hi!"),
]

for label, text in test_strings:
    utf8_bytes = text.encode('utf-8')
    print(f"  {label:<20} chars:{len(text):>2} bytes:{len(utf8_bytes):>2} hex:{utf8_bytes.hex()}")

# Explanation: ASCII uses 7 bits (0-127) for English characters.
# UTF-8 uses 1-4 bytes: ASCII chars = 1 byte, most others = 2-3 bytes.
# UTF-16 uses 2 or 4 bytes. UTF-8 is dominant on the web because it's
# backward-compatible with ASCII and space-efficient for English text.


# ============================================================
# Q9: Number theory: GCD, LCM, primes, and modular arithmetic
# ============================================================
# Question: Implement fundamental number theory algorithms.

import math

print("\n=== Q9: Number Theory Fundamentals ===")

# Euclidean algorithm for GCD
def gcd_euclidean(a, b):
    """Find GCD using Euclidean algorithm."""
    steps = []
    while b:
        steps.append(f"{a} = {a//b} x {b} + {a%b}")
        a, b = b, a % b
    return a, steps

result, steps = gcd_euclidean(48, 18)
print(f"  GCD(48, 18) = {result}")
for step in steps:
    print(f"    {step}")
print(f"  Verify: math.gcd(48, 18) = {math.gcd(48, 18)}")

# LCM
def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)
print(f"\n  LCM(12, 18) = {lcm(12, 18)}")

# Primality test
def is_prime(n):
    """Efficient primality test."""
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

primes = [n for n in range(2, 50) if is_prime(n)]
print(f"  Primes < 50: {primes}")

# Modular exponentiation
print(f"\n  Modular arithmetic:")
print(f"  pow(2, 10, 1000)  = {pow(2, 10, 1000)}")   # 1024 % 1000 = 24
print(f"  pow(3, 100, 97)   = {pow(3, 100, 97)}")     # Fermat's little theorem

# Explanation: The Euclidean algorithm finds GCD in O(log min(a,b)) steps.
# The primality test checks divisibility by 2, 3, then 6k+-1 up to sqrt(n).
# pow(base, exp, mod) uses fast modular exponentiation (O(log exp)),
# essential for cryptography (RSA relies on modular exponentiation).


# ============================================================
# Q10: Build a number system exploration tool
# ============================================================
# Question: Create an interactive tool that displays comprehensive
# information about any number.

print("\n=== Q10: Number Explorer ===")

def explore_number(n):
    """Display comprehensive information about a number."""
    print(f"\n  --- Exploring: {n} ---")

    # Base representations
    print(f"  Decimal:      {n}")
    print(f"  Binary:       {bin(n)}")
    print(f"  Octal:        {oct(n)}")
    print(f"  Hexadecimal:  {hex(n)}")

    # Properties
    print(f"\n  Properties:")
    print(f"    Even:         {n % 2 == 0}")
    print(f"    Positive:     {n > 0}")
    print(f"    Power of 2:   {n > 0 and (n & (n-1)) == 0}")
    print(f"    Prime:        {is_prime(n)}")
    print(f"    Perfect sq:   {int(math.isqrt(abs(n)))**2 == abs(n)}")

    # Bit information
    if n > 0:
        print(f"\n  Bit analysis:")
        print(f"    Bit length:   {n.bit_length()}")
        print(f"    Set bits:     {bin(n).count('1')}")
        print(f"    Highest bit:  2^{n.bit_length()-1} = {2**(n.bit_length()-1)}")

    # Factors (for small numbers)
    if 1 < abs(n) <= 10000:
        factors = [i for i in range(1, abs(n)+1) if abs(n) % i == 0]
        if len(factors) <= 20:
            print(f"    Factors:      {factors}")
        print(f"    Num factors:  {len(factors)}")

    # As bytes
    if 0 <= n <= 0xFFFFFFFF:
        byte_len = max(1, (n.bit_length() + 7) // 8)
        print(f"    As bytes:     {n.to_bytes(byte_len, 'big').hex()}")

for test_num in [42, 255, 1024, 97]:
    explore_number(test_num)

# Explanation: This tool combines everything from this file:
# base conversion, bit analysis, number theory (primality, factors),
# byte representation. It's a practical reference tool for understanding
# how numbers work at different levels of abstraction.
