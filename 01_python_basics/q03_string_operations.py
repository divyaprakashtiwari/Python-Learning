"""
Topic 01: Python Basics
Question 03: String Operations

Master Python string methods, slicing, searching, and manipulation.
"""

# ============================================================
# Q1: String slicing and indexing
# ============================================================
# Question: Given a string, demonstrate positive/negative indexing,
# slicing with step, and reversing a string.

print("=== Q1: String Slicing and Indexing ===")
text = "Hello, Python!"

# Positive indexing (0-based)
print(f"  text[0]  = {text[0]!r}")    # 'H'
print(f"  text[7]  = {text[7]!r}")    # 'P'
print(f"  text[-1] = {text[-1]!r}")   # '!'

# Slicing: [start:stop:step]
print(f"  text[0:5]   = {text[0:5]!r}")     # 'Hello'
print(f"  text[7:]    = {text[7:]!r}")       # 'Python!'
print(f"  text[:5]    = {text[:5]!r}")       # 'Hello'
print(f"  text[::2]   = {text[::2]!r}")      # Every 2nd char
print(f"  text[::-1]  = {text[::-1]!r}")     # Reversed

# Edge case: slicing beyond bounds doesn't error
print(f"  text[100:]  = {text[100:]!r}")     # '' (empty, no error)
print(f"  text[-100:5]= {text[-100:5]!r}")   # 'Hello' (clamped)

# Explanation: text[start:stop:step] extracts a substring. Negative indices
# count from the end. Slicing never raises IndexError even with out-of-range
# values -- it just clamps to the string boundaries. [::-1] is the classic
# Python idiom for string reversal.


# ============================================================
# Q2: Essential string methods
# ============================================================
# Question: Demonstrate the most commonly used string methods:
# upper, lower, title, strip, replace, split, join.

print("\n=== Q2: Essential String Methods ===")
messy = "  Hello, WORLD!  "

print(f"  Original:   {messy!r}")
print(f"  .strip():   {messy.strip()!r}")
print(f"  .lstrip():  {messy.lstrip()!r}")
print(f"  .rstrip():  {messy.rstrip()!r}")
print(f"  .lower():   {messy.lower()!r}")
print(f"  .upper():   {messy.upper()!r}")
print(f"  .title():   {messy.strip().title()!r}")
print(f"  .swapcase():{messy.strip().swapcase()!r}")
print(f"  .capitalize():{messy.strip().capitalize()!r}")

# replace
original = "I love Java"
fixed = original.replace("Java", "Python")
print(f"  '{original}'.replace('Java','Python') = {fixed!r}")

# count
text = "banana"
print(f"  'banana'.count('an') = {text.count('an')}")  # 2
print(f"  'banana'.count('a')  = {text.count('a')}")   # 3

# Explanation: All string methods return NEW strings (strings are immutable).
# strip() is essential for cleaning user input. replace() replaces ALL
# occurrences by default; use replace(old, new, count) to limit.


# ============================================================
# Q3: String searching methods
# ============================================================
# Question: Use find(), index(), startswith(), endswith(), and `in`
# to search within strings. Handle the differences between find/index.

print("\n=== Q3: String Searching ===")
text = "The quick brown fox jumps over the lazy dog"

# find() returns -1 if not found
print(f"  text.find('fox')    = {text.find('fox')}")     # 16
print(f"  text.find('cat')    = {text.find('cat')}")     # -1

# index() raises ValueError if not found
try:
    pos = text.index('cat')
except ValueError as e:
    print(f"  text.index('cat')   -> ValueError: {e}")

# rfind() / rindex() search from the right
print(f"  text.find('the')    = {text.find('the')}")     # 31 (case-sensitive!)
print(f"  text.find('The')    = {text.find('The')}")     # 0

# startswith() and endswith()
print(f"  text.startswith('The')     = {text.startswith('The')}")     # True
print(f"  text.endswith('dog')       = {text.endswith('dog')}")       # True
print(f"  text.endswith(('dog','cat'))= {text.endswith(('dog','cat'))}")  # tuple!

# `in` operator
print(f"  'fox' in text = {'fox' in text}")   # True
print(f"  'cat' in text = {'cat' in text}")   # False

# Explanation: find() is safer than index() because it returns -1 instead
# of raising an exception. startswith/endswith accept tuples to check
# multiple prefixes/suffixes at once. All searches are case-sensitive.


# ============================================================
# Q4: String validation methods (isdigit, isalpha, etc.)
# ============================================================
# Question: Use is*() methods to validate string content.

print("\n=== Q4: String Validation Methods ===")

test_strings = ["Hello", "hello123", "123", "12.5", "", "   ", "Hello World",
                "HELLO", "hello"]

print(f"  {'String':<14} {'alpha':>5} {'digit':>5} {'alnum':>5} "
      f"{'space':>5} {'upper':>5} {'lower':>5}")
print(f"  {'-'*14} {'-'*5} {'-'*5} {'-'*5} {'-'*5} {'-'*5} {'-'*5}")

for s in test_strings:
    if s == "":
        label = "(empty)"
    elif s == "   ":
        label = "(spaces)"
    else:
        label = s
    print(f"  {label:<14} {str(s.isalpha()):>5} {str(s.isdigit()):>5} "
          f"{str(s.isalnum()):>5} {str(s.isspace()):>5} "
          f"{str(s.isupper()):>5} {str(s.islower()):>5}")

# Practical: Validate a username
def is_valid_username(username):
    """Username must be 3-20 chars, alphanumeric + underscore, start with letter."""
    if not 3 <= len(username) <= 20:
        return False
    if not username[0].isalpha():
        return False
    return all(c.isalnum() or c == '_' for c in username)

for name in ["divya", "user_123", "3bad", "ab", "valid_user_name_here_ok", "no spaces"]:
    print(f"  is_valid_username({name!r:>25}) = {is_valid_username(name)}")

# Explanation: All is*() methods return False for empty strings.
# isdigit() only handles ASCII digits; for Unicode digits use isnumeric().
# These methods are great for input validation without regex.


# ============================================================
# Q5: String formatting (f-strings, format(), %)
# ============================================================
# Question: Compare all three string formatting methods and show
# advanced f-string features (alignment, fill, precision).

print("\n=== Q5: String Formatting Methods ===")
name = "Divya"
age = 21
gpa = 3.857

# Method 1: f-strings (Python 3.6+) -- PREFERRED
print(f"  f-string:  {name} is {age} years old with GPA {gpa:.2f}")

# Method 2: .format()
print("  .format(): {} is {} years old with GPA {:.2f}".format(name, age, gpa))

# Method 3: % operator (old-style)
print("  %% format: %s is %d years old with GPA %.2f" % (name, age, gpa))

# Advanced f-string formatting
print(f"\n  Alignment and fill:")
print(f"  {'Left':<20}|")
print(f"  {'Center':^20}|")
print(f"  {'Right':>20}|")
print(f"  {'Filled':*^20}|")

print(f"\n  Number formatting:")
big_num = 1234567890
print(f"  Comma separator: {big_num:,}")
print(f"  Underscore sep:  {big_num:_}")
print(f"  Percentage:      {0.856:.1%}")
print(f"  Scientific:      {big_num:.2e}")
print(f"  Binary:          {42:08b}")
print(f"  Hex:             {255:#06x}")

# f-string with expressions
print(f"\n  Expression in f-string: {2**10 = }")  # Python 3.8+
print(f"  Conditional: {'adult' if age >= 18 else 'minor'}")

# Explanation: f-strings are the modern, preferred way to format strings.
# They're faster than .format() and % because they're evaluated at compile time.
# The `=` specifier (Python 3.8+) shows both the expression and its value.
# Format spec: [[fill]align][sign][#][0][width][grouping][.precision][type]


# ============================================================
# Q6: Multi-line strings and escape characters
# ============================================================
# Question: Demonstrate triple-quoted strings, raw strings,
# and all common escape characters.

print("\n=== Q6: Multi-line Strings and Escapes ===")

# Triple-quoted strings preserve newlines
multiline = """Line 1
Line 2
Line 3"""
print(f"  Triple-quoted:\n{multiline}")

# Common escape characters
print(f"\n  Escapes:")
print(f"  \\n = newline (already used)")
print(f"  \\t = tab:\tHere")
print(f"  \\\\ = backslash: \\")
print(f"  \\' = single quote: '")
print(f"  \\\" = double quote: \"")
print(f"  \\0 = null character (length = {len(chr(0))})")

# Raw strings -- backslashes are literal
raw = r"C:\Users\new_folder\test"
print(f"\n  Raw string: {raw}")  # No interpretation of \n, \t

# Edge case: raw string can't end with odd number of backslashes
# r"test\" is a syntax error -- use "test\\" or r"test" + "\\"

# Explanation: Triple-quoted strings (''' or """) are ideal for
# multi-line text and docstrings. Raw strings (r"...") treat backslashes
# as literal characters, making them perfect for Windows paths and regex.


# ============================================================
# Q7: String repetition, concatenation, and membership
# ============================================================
# Question: Show efficient string building patterns and explain
# why += in a loop is problematic.

print("\n=== Q7: String Building Patterns ===")

# Basic operations
print(f"  'Ha' * 3        = {'Ha' * 3}")
print(f"  'Hello' + ' ' + 'World' = {'Hello' + ' ' + 'World'}")

# INEFFICIENT: += in a loop (creates new string each time)
import time

def build_with_concat(n):
    result = ""
    for i in range(n):
        result += str(i)
    return result

# EFFICIENT: join with list
def build_with_join(n):
    parts = []
    for i in range(n):
        parts.append(str(i))
    return "".join(parts)

# Time comparison
n = 50000
start = time.perf_counter()
s1 = build_with_concat(n)
time1 = time.perf_counter() - start

start = time.perf_counter()
s2 = build_with_join(n)
time2 = time.perf_counter() - start

print(f"\n  Building string of {n} numbers:")
print(f"    += concat: {time1:.4f} sec")
print(f"    join():    {time2:.4f} sec")
print(f"    Same result: {s1 == s2}")

# Explanation: String concatenation with += creates a new string object
# each iteration (O(n^2) total). list.append() + join() is O(n).
# For small strings += is fine, but for building large strings always use join().


# ============================================================
# Q8: Partition, expandtabs, center, zfill, and translate
# ============================================================
# Question: Demonstrate lesser-known but useful string methods.

print("\n=== Q8: Lesser-Known String Methods ===")

# partition() -- splits into 3 parts at first occurrence
email = "user@example.com"
local, at, domain = email.partition("@")
print(f"  '{email}'.partition('@') = ({local!r}, {at!r}, {domain!r})")

# rpartition() -- splits from the right
path = "C:/Users/docs/file.txt"
head, sep, tail = path.rpartition("/")
print(f"  '{path}'.rpartition('/') = ({head!r}, {sep!r}, {tail!r})")

# zfill() -- zero-pad numbers
for num in [1, 42, 100, 5]:
    print(f"  str({num}).zfill(5) = {str(num).zfill(5)}")

# center()
title = "PYTHON"
print(f"  '{title}'.center(30, '-') = {title.center(30, '-')!r}")

# expandtabs()
tabbed = "Name\tAge\tCity"
print(f"  expandtabs(12): {tabbed.expandtabs(12)}")

# maketrans() and translate() -- character-level replacement
table = str.maketrans("aeiou", "12345")
original = "hello world"
translated = original.translate(table)
print(f"  Translate vowels: '{original}' -> '{translated}'")

# Remove characters with translate
remove_table = str.maketrans("", "", "aeiou")
print(f"  Remove vowels:    '{original}' -> '{original.translate(remove_table)}'")

# Explanation: partition() is cleaner than split() when you need exactly
# 3 parts. translate() is extremely fast for character-level operations
# because it uses a C-level lookup table. zfill() is perfect for
# fixed-width numeric strings like IDs and timestamps.


# ============================================================
# Q9: String encoding awareness and Unicode basics
# ============================================================
# Question: Show how Python handles Unicode strings, character
# counting vs byte counting, and normalization basics.

print("\n=== Q9: Unicode and String Length ===")

# Length counts characters, not bytes
ascii_text = "Hello"
print(f"  '{ascii_text}': len={len(ascii_text)}, bytes={len(ascii_text.encode('utf-8'))}")

# ASCII-safe demonstration
emoji_text = "Hi!"
print(f"  '{emoji_text}': len={len(emoji_text)}, bytes={len(emoji_text.encode('utf-8'))}")

# Working with Unicode categories
import unicodedata

chars = ['A', '1', '+', ' ']
for c in chars:
    try:
        name = unicodedata.name(c)
    except ValueError:
        name = "(no name)"
    cat = unicodedata.category(c)
    print(f"  {c!r:>4}: category={cat}, name={name}")

# Practical: Remove accents from characters
def remove_accents(text):
    """Remove accent marks from characters (ASCII-safe)."""
    import unicodedata
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join(c for c in nfkd if unicodedata.category(c) != 'Mn')

accented = "cafe"
cleaned = remove_accents(accented)
print(f"\n  remove_accents('{accented}') = '{cleaned}'")

# Explanation: Python 3 strings are Unicode by default. len() counts
# characters (code points), but the byte representation varies by encoding.
# UTF-8 uses 1-4 bytes per character. unicodedata provides character
# metadata -- useful for text normalization and cleaning.


# ============================================================
# Q10: Build a text processing toolkit
# ============================================================
# Question: Create utility functions for common text operations:
# word count, sentence extraction, text wrapping, slug generation.

print("\n=== Q10: Text Processing Toolkit ===")

def word_count(text):
    """Count words in text, handling multiple whitespace."""
    return len(text.split())

def char_frequency(text):
    """Count character frequencies (case-insensitive, letters only)."""
    freq = {}
    for c in text.lower():
        if c.isalpha():
            freq[c] = freq.get(c, 0) + 1
    return dict(sorted(freq.items(), key=lambda x: -x[1]))

def to_slug(text):
    """Convert text to URL-friendly slug."""
    slug = text.lower().strip()
    # Replace non-alphanumeric with hyphens
    result = []
    for c in slug:
        if c.isalnum():
            result.append(c)
        elif result and result[-1] != '-':
            result.append('-')
    return ''.join(result).strip('-')

def truncate(text, max_len=50, suffix="..."):
    """Truncate text at word boundary."""
    if len(text) <= max_len:
        return text
    truncated = text[:max_len - len(suffix)]
    # Find last space to avoid cutting words
    last_space = truncated.rfind(' ')
    if last_space > 0:
        truncated = truncated[:last_space]
    return truncated + suffix

def title_case(text):
    """Smart title case (don't capitalize small words)."""
    small_words = {'a', 'an', 'the', 'and', 'but', 'or', 'for',
                   'nor', 'on', 'at', 'to', 'by', 'in', 'of'}
    words = text.lower().split()
    result = []
    for i, word in enumerate(words):
        if i == 0 or word not in small_words:
            result.append(word.capitalize())
        else:
            result.append(word)
    return ' '.join(result)

# Test each function
sample = "The quick brown fox jumps over the lazy dog near the river bank"

print(f"  Word count:      {word_count(sample)}")
print(f"  Top 5 chars:     {dict(list(char_frequency(sample).items())[:5])}")
print(f"  Slug:            {to_slug('Hello World! This is Python 3')!r}")
print(f"  Truncated:       {truncate(sample, 30)!r}")
print(f"  Title case:      {title_case('the lord of the rings')!r}")

# Edge cases
print(f"\n  Edge cases:")
print(f"  word_count(''):          {word_count('')}")
print(f"  to_slug('---hello---'):  {to_slug('---hello---')!r}")
print(f"  truncate('short', 50):   {truncate('short', 50)!r}")
print(f"  title_case(''):          {title_case('')!r}")

# Explanation: These are common text processing utilities. to_slug() creates
# URL-friendly strings. truncate() cuts at word boundaries to avoid breaking
# words. title_case() skips small words (articles, prepositions) following
# standard English title case rules. char_frequency() uses dict.get() for
# concise counting (collections.Counter is even better).
