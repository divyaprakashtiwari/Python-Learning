# Phase 5 — Topic 09: Regular Expressions

## 1. Introduction

**Regular Expressions (Regex)** are a mini-language for matching, validating, extracting, and transforming patterns inside text. Python's built-in `re` module compiles regex patterns into fast bytecode state machines capable of parsing complex log formats, redacting sensitive PII (emails, phone numbers, credit cards), and tokenizing text in a few lines of code.

---

## 2. Why is it used?

1. **Structured Data Extraction:** Named capture groups (`(?P<name>...)`) turn unstructured server log lines into clean Python dictionaries via `.groupdict()`.
2. **Input Validation (`re.fullmatch`):** Validates whether an entire string conforms to an identifier format (e.g., ISO date `YYYY-MM-DD`, semantic version `1.2.3`, or SKU code).
3. **Context-Aware Search & Replace (`re.sub`):** Supports both backreferences and dynamic Python callback functions `re.sub(pattern, callback, text)` for custom masking and formatting.
4. **Performance via Pre-Compilation (`re.compile`):** Compiling frequently used regexes once at module import time avoids re-parsing the pattern inside tight loops.

---

## 3. Syntax

```python
import re

# Always use RAW STRINGS (r"...") so Python doesn't interpret \b, \d, \s as string escapes!
DATE_RE = re.compile(r"\b(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\b")

# 1. Core Matching Functions
m1 = re.match(r"\d+", "123abc")       # Anchored at index 0 -> Match('123')
m2 = re.search(r"\d+", "id=123")      # Searches anywhere   -> Match('123')
m3 = re.fullmatch(r"\d+", "123")      # Entire string matches -> Match('123')

# 2. Finding All Occurrences
all_strings: list[str] = re.findall(r"\d+", "a1 b22 c333")  # ['1', '22', '333']
for match in re.finditer(r"\d+", "a1 b22 c333"):            # Lazy Match iterator
    print(match.group(0), match.span())

# 3. Substitution
cleaned = re.sub(r"\s+", " ", "too    many   spaces")
```

---

## 4. Explanation (Step-by-Step)

1. **Why Raw Strings (`r"..."`) Are Mandatory:**
   - In a normal Python string literal `"..."`, `\b` is the ASCII backspace character (`\x08`). In regex, `\b` means **word boundary**. Using `r"\bword\b"` passes the literal backslash and `b` directly to the regex engine (and prevents Python 3.12+ `SyntaxWarning: invalid escape sequence '\d'`).
2. **`re.match()` vs `re.search()` vs `re.fullmatch()`:**
   - `re.match(pattern, text)`: Checks **only at the very beginning** of `text` (index 0).
   - `re.search(pattern, text)`: Scans through `text` and returns the **first** match anywhere.
   - `re.fullmatch(pattern, text)`: Succeeds only if the **entire** string from start to end matches `pattern` (ideal for validation!).
3. **Capture Groups vs Non-Capturing Groups:**
   - `(pattern)` is a numbered capture group (`match.group(1)`). Note: if you pass a pattern containing capture groups to `re.findall()`, `findall()` returns **only the captured groups** (or tuples of groups), not the full match!
   - `(?:pattern)` groups sub-patterns for `|` or `+` **without capturing**.
   - `(?P<name>pattern)` assigns a symbolic name accessible via `match.group("name")` and `match.groupdict()`.
4. **Greedy vs Non-Greedy (Lazy) Quantifiers:**
   - `*`, `+`, and `?` are **greedy** by default—they match as much text as possible (`r"<b>.*</b>"` on `"<b>A</b> and <b>B</b>"` matches the entire string).
   - Adding `?` (`*?`, `+?`, `??`) makes them **non-greedy (lazy)**—matching the shortest possible substring (`['<b>A</b>', '<b>B</b>']`).

---

## 5. Minimum 3 Examples

### Example 01: `re.search()`, `re.match()`, `re.fullmatch()`, `re.findall()`, & Raw Strings (`r"..."`)
File: [`example_01_search_match_findall_and_raw_strings.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/09_Regular_Expressions/example_01_search_match_findall_and_raw_strings.py)

```python
r"""
Phase 5 - Topic 09: Regular Expressions
Example 01: `re.search()`, `re.match()`, `re.fullmatch()`, `re.findall()`, & Raw Strings (`r"..."`)

Demonstrates:
  - Why raw strings (`r"..."`) are essential for regex patterns (`\b`, `\d`, `\s`)
  - The difference between `re.match()` (anchored at start), `re.search()` (anywhere),
    and `re.fullmatch()` (entire string must match)
  - Extracting all occurrences with `re.findall()` and `re.finditer()`
"""

import re


def main() -> None:
    text = "Order #4091 placed on 2026-11-04; Order #5102 placed on 2026-11-05."

    print("=== 1. `re.match` vs `re.search` vs `re.fullmatch` ===")
    print(f"  re.match(r'#\\d+', text)     : {re.match(r'#\d+', text)} (None: '#' is not at index 0)")
    first_hit = re.search(r"#\d+", text)
    print(f"  re.search(r'#\\d+', text)    : {first_hit.group(0) if first_hit else None} at span {first_hit.span() if first_hit else None}")
    print(f"  re.fullmatch(r'\\d{{4}}', '4091'): {bool(re.fullmatch(r'\d{4}', '4091'))}")

    print("\n=== 2. Extracting All Matches with `re.findall` & `re.finditer` ===")
    order_ids = re.findall(r"#(\d+)", text)
    print(f"  re.findall(r'#(\\d+)', text) : {order_ids} (returns captured group strings)")

    for match in re.finditer(r"\b(\d{4})-(\d{2})-(\d{2})\b", text):
        year, month, day = match.groups()
        print(f"  re.finditer date at {match.span()}: year={year}, month={month}, day={day}")


if __name__ == "__main__":
    main()
```

### Example 02: Named Capture Groups (`(?P<name>...)`), `.groupdict()`, & Lookarounds
File: [`example_02_named_capture_groups_and_lookarounds.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/09_Regular_Expressions/example_02_named_capture_groups_and_lookarounds.py)

```python
"""
Phase 5 - Topic 09: Regular Expressions
Example 02: Named Capture Groups (`(?P<name>...)`), `.groupdict()`, & Lookarounds

Demonstrates:
  - Parsing structured log lines into dictionaries using named groups `(?P<name>...)` and `.groupdict()`
  - Using positive lookahead `(?=...)` and positive lookbehind `(?<=...)` for zero-width assertions
"""

import re


LOG_PATTERN = re.compile(
    r"^\[(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] "
    r"(?P<level>INFO|WARN|ERROR) "
    r"service=(?P<service>[a-z0-9_-]+) "
    r"latency_ms=(?P<latency>\d+)$"
)


def main() -> None:
    print("=== 1. Parsing Structured Logs with Named Capture Groups (`.groupdict()`) ===")
    raw_line = "[2026-11-04 14:22:09] ERROR service=auth-api latency_ms=342"
    match = LOG_PATTERN.match(raw_line)
    if match:
        print(f"  Parsed groupdict: {match.groupdict()}")
        print(f"  Direct group('service'): {match.group('service')!r}")

    print("\n=== 2. Lookaround Assertions (Extract USD Prices Only, Ignoring INR) ===")
    invoice = "Items: $45, Rs.900, $120, Rs.250"
    # (?<=\$)\d+ matches digits ONLY if immediately preceded by literal '$'
    usd_amounts = re.findall(r"(?<=\$)\d+", invoice)
    print(f"  USD amounts via positive lookbehind `(?<=\\$)\\d+`: {usd_amounts}")


if __name__ == "__main__":
    main()
```

### Example 03: Dynamic Redaction & Replacement with `re.sub()` Callbacks & Greedy vs Non-Greedy
File: [`example_03_re_sub_callbacks_and_compiled_regex.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/09_Regular_Expressions/example_03_re_sub_callbacks_and_compiled_regex.py)

```python
"""
Phase 5 - Topic 09: Regular Expressions
Example 03: Dynamic Redaction & Replacement with `re.sub()` Callbacks & Greedy vs Non-Greedy

Demonstrates:
  - Passing a callable function to `re.sub(pattern, repl_func, text)` for dynamic PII masking
  - Backreferences in replacement strings (`r"\\g<1>"`)
  - Greedy (`.*`) vs Non-Greedy/Lazy (`.*?`) quantifiers on HTML/tag extraction
"""

import re


def mask_email(match: re.Match[str]) -> str:
    """Mask email local-part keeping only first and last character: `a***v@domain.com`."""
    user = match.group("user")
    domain = match.group("domain")
    masked_user = user[0] + ("*" * max(1, len(user) - 2)) + user[-1] if len(user) > 2 else "***"
    return f"{masked_user}@{domain}"


def main() -> None:
    print("=== 1. Dynamic PII Masking with `re.sub(pattern, callable, text)` ===")
    support_ticket = "Contact aarav.sharma@example.com or diya@company.org for escalation."
    email_re = re.compile(r"(?P<user>[a-zA-Z0-9._%+-]+)@(?P<domain>[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})")
    redacted = email_re.sub(mask_email, support_ticket)
    print(f"  Original : {support_ticket}")
    print(f"  Redacted : {redacted}")

    print("\n=== 2. Greedy (`.*`) vs Non-Greedy (`.*?`) Quantifiers ===")
    snippet = "<b>First</b> and <b>Second</b>"
    print(f"  Greedy     `r'<b>.*</b>'`  -> {re.findall(r'<b>.*</b>', snippet)}")
    print(f"  Non-Greedy `r'<b>.*?</b>'` -> {re.findall(r'<b>.*?</b>', snippet)}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== 1. `re.match` vs `re.search` vs `re.fullmatch` ===
  re.match(r'#\d+', text)     : None (None: '#' is not at index 0)
  re.search(r'#\d+', text)    : #4091 at span (6, 11)
  re.fullmatch(r'\d{4}', '4091'): True

=== 2. Extracting All Matches with `re.findall` & `re.finditer` ===
  re.findall(r'#(\d+)', text) : ['4091', '5102'] (returns captured group strings)
  re.finditer date at (22, 32): year=2026, month=11, day=04
  re.finditer date at (56, 66): year=2026, month=11, day=05
```

### Output — Example 02
```text
=== 1. Parsing Structured Logs with Named Capture Groups (`.groupdict()`) ===
  Parsed groupdict: {'timestamp': '2026-11-04 14:22:09', 'level': 'ERROR', 'service': 'auth-api', 'latency': '342'}
  Direct group('service'): 'auth-api'

=== 2. Lookaround Assertions (Extract USD Prices Only, Ignoring INR) ===
  USD amounts via positive lookbehind `(?<=\$)\d+`: ['45', '120']
```

### Output — Example 03
```text
=== 1. Dynamic PII Masking with `re.sub(pattern, callable, text)` ===
  Original : Contact aarav.sharma@example.com or diya@company.org for escalation.
  Redacted : Contact a**********a@example.com or d**a@company.org for escalation.

=== 2. Greedy (`.*`) vs Non-Greedy (`.*?`) Quantifiers ===
  Greedy     `r'<b>.*</b>'`  -> ['<b>First</b> and <b>Second</b>']
  Non-Greedy `r'<b>.*?</b>'` -> ['<b>First</b>', '<b>Second</b>']
```

---

## 7. Code Explanation

1. **`re.finditer` vs `re.findall` (Example 01):** `re.findall()` materializes a list of strings (or tuples if multiple groups exist) and discards match offsets. `re.finditer()` lazily yields full `re.Match` objects with `.span()`, `.group(0)`, and `.groups()`.
2. **`(?<=\$)\d+` Positive Lookbehind (Example 02):** `(?<=\$)` verifies that a `$` precedes the digits **without consuming `$` as part of the match**, so `re.findall()` returns `['45', '120']` directly without needing a capture group.
3. **`email_re.sub(mask_email, support_ticket)` (Example 03):** For every match found, `re.sub()` passes the `re.Match` object to `mask_email(match)` and replaces the matched span with the returned string.

---

## 8. Common Mistakes

1. **Using `re.match(r"^\d+", s)` Expecting `$` to Be Enforced:**
   - `re.match(r"\d+", "123abc")` succeeds because `re.match` only anchors the **start** of the string! Always use `re.fullmatch(r"\d+", s)` when validating that an entire string matches.
2. **Grouping With `(...)` Inside `re.findall()` When You Wanted Full Matches:**
   - `re.findall(r"(http|https)://\S+", text)` returns `['http', 'https']` instead of the full URLs because `findall` returns capture groups when present! Use a non-capturing group `(?:http|https)://\S+` or `[m.group(0) for m in re.finditer(...)]`.
3. **Forgetting `re.escape(user_input)` When Interpolating Literal Strings Into Regexes:**
   - If `query = "c++ (v2.0)"`, interpolating `rf"\b{query}\b"` crashes or misbehaves because `+`, `(`, `.`, `)` are regex metacharacters. Always wrap dynamic literal substrings in `re.escape(query)`.

---

## 9. Practice Questions

1. **Easy:** Write a function `is_valid_indian_mobile(phone: str) -> bool` using `re.fullmatch` that accepts an optional `+91-` or `+91 ` prefix followed by a 10-digit number starting with `6`, `7`, `8`, or `9`.
2. **Medium:** Write a function `snake_to_camel(identifier: str) -> str` using `re.sub` with a callback function that converts `"user_profile_id"` into `"userProfileId"`.
3. **Hard:** Write a compiled `re.VERBOSE` (`re.X`) regex that parses semantic version strings (`1.2.3-alpha.1+build.45`) into named groups `major`, `minor`, `patch`, `prerelease`, and `buildmetadata`.

---

## 10. Interview Questions

### Q1: What is Catastrophic Backtracking (ReDoS), and how do you prevent it in Python?
**Answer:** Nested quantifiers like `r"(a+)+b"` on an input of `"aaaaaaaaaaaaaaaaaaaaaaaa!"` cause NFA regex engines to explore $O(2^n)$ backtracking paths, freezing the CPU. Prevention:
1. Flatten nested quantifiers (`r"a+b"`).
2. Use **atomic groups** `(?>...)` or **possessive quantifiers** `*+`, `++`, `?+` (supported natively in Python 3.11+ `re`!), which forbid backtracking once matched.

### Q2: Does `re.compile()` make every regex faster?
**Answer:** Top-level functions like `re.search(pattern, text)` internally cache the most recently compiled patterns (up to `_MAXCACHE = 512`). However, calling `re.compile()` once at module level avoids dictionary cache lookup overhead inside hot loops and lets you invoke `.search(text, pos, endpos)` with slice bounds without slicing the string.

### Q3: What do the regex flags `re.IGNORECASE` (`re.I`), `re.MULTILINE` (`re.M`), and `re.DOTALL` (`re.S`) do?
**Answer:**
- `re.I`: Case-insensitive matching.
- `re.M`: Makes `^` and `$` match the start and end of **each line** (around `\n`) instead of only the start and end of the entire string.
- `re.S`: Makes the dot `.` match **any character including `\n`** (normally `.` matches everything except `\n`).
