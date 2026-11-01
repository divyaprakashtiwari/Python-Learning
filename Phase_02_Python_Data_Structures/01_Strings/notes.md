# Topic 01: Strings

---

## 1. Introduction

A **String (`str`)** in Python is an ordered, **immutable** sequence of Unicode characters enclosed in single quotes (`'...'`), double quotes (`"..."`), or triple quotes (`"""..."""` for multi-line strings).

Because strings are **sequences**, you can access individual characters in `O(1)` time by index (`s[0]`, `s[-1]`), slice substrings (`s[start:stop:step]`), iterate over characters with a `for` loop, and query their length with `len(s)`.

---

## 2. Why is it used?

Strings are the most ubiquitous data structure in software development and coding interviews:
1. **Text & Log Processing:** Parsing URLs, log files, CSV records, and configuration files.
2. **Web & API Payloads:** Every HTTP header, JSON key, HTML page, and SQL query is constructed from strings.
3. **Coding Interview Classics:** Anagrams, palindromes, longest substring without repeating characters, and string compression are among the top 5 most frequently asked interview problem categories.

---

## 3. Syntax

```python
# 1. String Literals
single_quoted = 'Hello'
double_quoted = "Python's Strings"
raw_regex_path = r"C:\Users\ACER\notes"  # Raw string: ignores backslash escapes
multiline = """Line 1
Line 2"""

# 2. Indexing & Slicing: s[start : stop : step]
word = "PYTHON"
first_char = word[0]       # 'P'
last_char = word[-1]       # 'N'
prefix = word[:3]          # 'PYT' (stop index 3 is exclusive)
reversed_word = word[::-1] # 'NOHTYP'

# 3. Core Methods
cleaned = "  hello world  ".strip().title()   # 'Hello World'
parts = "a,b,c".split(",")                    # ['a', 'b', 'c']
joined = "-".join(parts)                      # 'a-b-c'
```

---

## 4. Explanation (Dual Indexing & Memory Model)

Every character in a Python string of length $n$ has **two valid indices**:
- A **positive index** from `0` (leftmost) to `n - 1` (rightmost).
- A **negative index** from `-n` (leftmost) to `-1` (rightmost).

```
 Character :    'P'    'Y'    'T'    'H'    'O'    'N'
 Pos Index :     0      1      2      3      4      5
 Neg Index :    -6     -5     -4     -3     -2     -1
```

### Why Are Strings Immutable?
Once `'PYTHON'` is created in memory, you **cannot** mutate a character in-place (`word[0] = 'J'` raises `TypeError`). Every string method (`.upper()`, `.replace()`, `.strip()`) returns a **brand-new string object** and leaves the original string untouched.

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_indexing_and_slicing.py`](example_01_indexing_and_slicing.py)
- [`example_02_core_string_methods.py`](example_02_core_string_methods.py)
- [`example_03_unicode_ord_chr_and_caesar_cipher.py`](example_03_unicode_ord_chr_and_caesar_cipher.py)

### Example 1: String Indexing, Slicing, and Immutability (`example_01_indexing_and_slicing.py`)

```python
def main() -> None:
    course_code = "PYTHON-DSA-2026"

    print("=== 1. Positive and Negative Indexing ===")
    print(f"Full String       : {course_code!r} (Length: {len(course_code)})")
    print(f"First char [0]    : {course_code[0]!r}")
    print(f"Last char [-1]    : {course_code[-1]!r}")
    print(f"4th from end [-4] : {course_code[-4]!r}")

    print("\n=== 2. Slicing: s[start:stop:step] ===")
    print(f"Language [0:6]    : {course_code[:6]!r}")
    print(f"Topic [7:10]      : {course_code[7:10]!r}")
    print(f"Year [-4:]        : {course_code[-4:]!r}")
    print(f"Every 2nd char    : {course_code[::2]!r}")
    print(f"Reversed [::-1]   : {course_code[::-1]!r}")

    print("\n=== 3. String Immutability Proof ===")
    word = "cat"
    modified_word = "b" + word[1:]
    print(f"Original word     : {word!r}")
    print(f"New sliced string : {modified_word!r}")


if __name__ == "__main__":
    main()
```

### Example 2: Essential String Methods (`example_02_core_string_methods.py`)

```python
def main() -> None:
    raw_log = "   [WARN] 2026-11-01 | user=divya_tiwari | action=login_retry   "

    print("=== 1. Whitespace Stripping & Case Normalization ===")
    cleaned = raw_log.strip()
    print(f"Cleaned Log       : {cleaned!r}")
    print(f"Starts with [WARN]: {cleaned.startswith('[WARN]')}")
    print(f"Ends with retry   : {cleaned.endswith('login_retry')}")

    print("\n=== 2. Searching & Replacing ===")
    pos = cleaned.find("user=")
    print(f"Index of 'user='  : {pos}")
    print(f"Count of '|'      : {cleaned.count('|')}")
    promoted_log = cleaned.replace("[WARN]", "[INFO]", 1)
    print(f"Replaced Log      : {promoted_log}")

    print("\n=== 3. Splitting and Joining (`split` & `join`) ===")
    fields = [part.strip() for part in cleaned.split("|")]
    print(f"Parsed Fields     : {fields}")
    csv_line = ",".join(fields)
    print(f"Joined as CSV     : {csv_line}")


if __name__ == "__main__":
    main()
```

### Example 3: Unicode (`ord`, `chr`) and Caesar Cipher (`example_03_unicode_ord_chr_and_caesar_cipher.py`)

```python
def caesar_cipher(text: str, shift: int) -> str:
    """Shift alphabetic characters by `shift` positions while preserving case."""
    result_chars: list[str] = []

    for ch in text:
        if ch.isupper():
            base = ord("A")
            shifted = (ord(ch) - base + shift) % 26 + base
            result_chars.append(chr(shifted))
        elif ch.islower():
            base = ord("a")
            shifted = (ord(ch) - base + shift) % 26 + base
            result_chars.append(chr(shifted))
        else:
            result_chars.append(ch)

    return "".join(result_chars)


def main() -> None:
    print("=== 1. Unicode Code Points (ord & chr) ===")
    for ch in ["A", "Z", "a", "0"]:
        print(f"  Character {ch!r} -> ord({ch!r}) = {ord(ch):>3} -> chr({ord(ch)}) = {chr(ord(ch))!r}")

    print("\n=== 2. Caesar Cipher Encryption & Decryption ===")
    secret_message = "Meet at Gate 04 at 18:30!"
    shift_key = 5
    encrypted = caesar_cipher(secret_message, shift=shift_key)
    decrypted = caesar_cipher(encrypted, shift=-shift_key)

    print(f"Original Message  : {secret_message}")
    print(f"Encrypted (+{shift_key})    : {encrypted}")
    print(f"Decrypted (-{shift_key})    : {decrypted}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== 1. Positive and Negative Indexing ===
Full String       : 'PYTHON-DSA-2026' (Length: 15)
First char [0]    : 'P'
Last char [-1]    : '6'
4th from end [-4] : '2'

=== 2. Slicing: s[start:stop:step] ===
Language [0:6]    : 'PYTHON'
Topic [7:10]      : 'DSA'
Year [-4:]        : '2026'
Every 2nd char    : 'PTO-S-06'
Reversed [::-1]   : '6202-ASD-NOHTYP'

=== 3. String Immutability Proof ===
Original word     : 'cat'
New sliced string : 'bat'
```

### Output for Example 2:
```text
=== 1. Whitespace Stripping & Case Normalization ===
Cleaned Log       : '[WARN] 2026-11-01 | user=divya_tiwari | action=login_retry'
Starts with [WARN]: True
Ends with retry   : True

=== 2. Searching & Replacing ===
Index of 'user='  : 20
Count of '|'      : 2
Replaced Log      : [INFO] 2026-11-01 | user=divya_tiwari | action=login_retry

=== 3. Splitting and Joining (`split` & `join`) ===
Parsed Fields     : ['[WARN] 2026-11-01', 'user=divya_tiwari', 'action=login_retry']
Joined as CSV     : [WARN] 2026-11-01,user=divya_tiwari,action=login_retry
```

### Output for Example 3:
```text
=== 1. Unicode Code Points (ord & chr) ===
  Character 'A' -> ord('A') =  65 -> chr(65) = 'A'
  Character 'Z' -> ord('Z') =  90 -> chr(90) = 'Z'
  Character 'a' -> ord('a') =  97 -> chr(97) = 'a'
  Character '0' -> ord('0') =  48 -> chr(48) = '0'

=== 2. Caesar Cipher Encryption & Decryption ===
Original Message  : Meet at Gate 04 at 18:30!
Encrypted (+5)    : Rjjy fy Lfyj 04 fy 18:30!
Decrypted (-5)    : Meet at Gate 04 at 18:30!
```

---

## 7. Code Explanation

- **`s[::-1]`** — Omitting `start` and `stop` with `step = -1` slices the entire string from right to left, returning a reversed copy in `O(n)` time.
- **`(ord(ch) - base + shift) % 26 + base`** — Maps `'A'..'Z'` to `0..25`, shifts by `shift` with modulo-26 wrap-around, and converts back to a character via `chr()`.
- **`"".join(result_chars)`** — Accumulating characters into a `list` and calling `"".join(...)` at the end runs in **`O(n)` linear time**, whereas repeatedly concatenating `res += ch` in a loop can degrade to `O(n^2)` because strings are immutable.

---

## 8. Common Mistakes

1. **Forgetting to Capture the Return Value of String Methods:**
   ```python
   # WRONG: Strings are immutable; s.upper() does NOT modify `s` in-place!
   s = "hello"
   s.upper()
   print(s)        # Still prints 'hello'!
   # CORRECT:
   s = s.upper()   # Prints 'HELLO'
   ```
2. **Confusing `s.find(sub)` with `s.index(sub)`:**
   `s.find("xyz")` safely returns `-1` when the substring is not found, whereas `s.index("xyz")` raises `ValueError: substring not found`.
3. **Out-of-Bounds Indexing vs Out-of-Bounds Slicing:**
   `s[100]` raises an `IndexError`, whereas slicing `s[0:100]` never raises an `IndexError`—it gracefully clamps to the end of the string!

---

## 9. Practice Questions

1. **Easy:** Write a function `count_vowels_and_consonants(text: str) -> tuple[int, int]` that returns `(vowel_count, consonant_count)` for any input string, ignoring digits, spaces, and punctuation.
2. **Medium:** Write a function `is_clean_palindrome(s: str) -> bool` that checks if a sentence (like `"A man, a plan, a canal: Panama"`) is a palindrome after filtering only `.isalnum()` characters and lowercasing them.
3. **Hard:** Write a function `compress_string(s: str) -> str` that performs Run-Length Encoding (e.g., `"aaabbcdddd" -> "a3b2c1d4"`), and returns the original string if the compressed version is not strictly shorter.

---

## 10. Interview Questions

### Q1: Why is `"".join(list_of_strings)` preferred over concatenating strings with `+=` inside a loop?
**Answer:** Because `str` is immutable, `s = s + piece` allocates a new string and copies all existing characters on each iteration, leading to $1 + 2 + \dots + N = O(N^2)$ worst-case work. `"".join(pieces)` pre-calculates the exact total length in a single pass and allocates memory only once in **`O(N)`** time.

### Q2: What is the difference between `str.strip("abc")` and `str.removeprefix("abc")`?
**Answer:** `str.strip("abc")` treats `"abc"` as a **set of characters** (`{'a', 'b', 'c'}`) and strips any combination of those characters from both ends (`"cbaxxxabc".strip("abc") == "xxx"`). `str.removeprefix("abc")` (added in Python 3.9) removes the **exact substring** `"abc"` from the start of the string.

### Q3: What is String Interning in Python?
**Answer:** String interning is an optimization where CPython caches and reuses a single copy of certain immutable strings (especially valid identifier-like strings such as `"user_id"` or compile-time literals) in memory so that multiple variables reference the same memory address (`sys.intern()`).
