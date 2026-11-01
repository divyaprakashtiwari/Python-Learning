# Topic 10: String Manipulation

---

## 1. Introduction

**String Manipulation** encompasses advanced techniques and algorithmic patterns for parsing, sanitizing, transforming, and analyzing strings efficiently in `O(n)` time.

While Topic 01 introduced string basics (indexing, slicing, and elementary methods), this topic focuses on **production text-processing idioms** (`removeprefix`, `removesuffix`, `partition`, `str.maketrans` + `translate`) and **core DSA string algorithms** (word reversal, 26-bucket frequency arrays for anagrams, and variable-size Sliding Windows).

---

## 2. Why is it used?

1. **Bug-Free Prefix & Path Parsing:** `.removeprefix()` and `.removesuffix()` prevent the notorious `.lstrip()` / `.rstrip()` character-set stripping bugs in file paths and URLs.
2. **High-Throughput Text Cleaning (`translate`):** Removing punctuation or remapping characters across millions of tokens in a single C-level pass via `str.maketrans()` + `.translate()`.
3. **Coding Interview Mastery:** Over 30% of array/string interview questions rely on character frequency arrays (`[0] * 26`), two pointers, or sliding windows over strings.

---

## 3. Syntax

```python
import string

# 1. Exact Prefix / Suffix Removal (Python 3.9+)
stem = "test_auth.py".removeprefix("test_").removesuffix(".py")  # 'auth'

# 2. Safe 3-Way Partitioning (Never raises ValueError when separator is missing!)
head, sep, tail = "key=value=1".partition("=")  # ('key', '=', 'value=1')

# 3. Single-Pass Character Translation & Deletion
table = str.maketrans("", "", string.punctuation)
clean_text = "Hello, World!".translate(table)   # 'Hello World'

# 4. Collapsing Whitespace & Reversing Words
reversed_words = " ".join("  hello   world  ".split()[::-1])  # 'world hello'
```

---

## 4. Explanation (Key String Manipulation Patterns)

1. **Why `.partition(sep)` Beats `.split(sep, 1)`:**
   - If `"=" ` is missing from `line`, `k, v = line.split("=", 1)` crashes with `ValueError: not enough values to unpack`.
   - `key, sep, val = line.partition("=")` **always** returns a 3-tuple: if `"="` is missing, it returns `(line, "", "")` without ever raising an error!
2. **26-Bucket Frequency Array (`[0] * 26`) for Lowercase ASCII Strings:**
   - For any lowercase letter `ch`, `ord(ch) - ord('a')` maps `'a'..'z'` to index `0..25`.
   - This lets you compare character frequencies of two strings in **`O(n)` time and `O(1)` (`26` ints) space**—faster than sorting (`O(n log n)`) and with lower overhead than a hash map.
3. **Variable-Size Sliding Window for Substring Problems:**
   - Maintain a window `[left .. right]` and a dictionary `last_seen[ch] = index`.
   - Whenever `ch` repeats inside the active window (`last_seen[ch] >= left`), jump `left` directly to `last_seen[ch] + 1` in `O(1)` time.

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_partition_prefixes_and_translation.py`](example_01_partition_prefixes_and_translation.py)
- [`example_02_slug_generator_and_word_reversal.py`](example_02_slug_generator_and_word_reversal.py)
- [`example_03_anagram_and_sliding_window_strings.py`](example_03_anagram_and_sliding_window_strings.py)

### Example 1: `removeprefix`/`removesuffix`, `partition`, and `str.translate` (`example_01_partition_prefixes_and_translation.py`)

```python
import string


def main() -> None:
    filename = "test_user_controller.py"
    clean_stem = filename.removeprefix("test_").removesuffix(".py")
    print("=== 1. Exact Prefix & Suffix Removal ===")
    print(f"Original Filename : {filename!r}")
    print(f"Cleaned Stem      : {clean_stem!r}")

    email = "divya.tiwari@university.edu.in"
    username, _, domain = email.partition("@")
    subdomain, _, top_level = domain.rpartition(".")
    print("\n=== 2. Safe Splitting with partition() & rpartition() ===")
    print(f"Username          : {username!r}")
    print(f"Full Domain       : {domain!r} (Sub: {subdomain!r}, TLD: {top_level!r})")

    messy_sentence = "Hello, World! Python-3.13 is #1 for DSA!!!"
    delete_chars = string.punctuation.replace("-", "").replace(".", "")
    trans_table = str.maketrans("-", " ", delete_chars)
    cleaned_sentence = messy_sentence.translate(trans_table)
    print("\n=== 3. Single-Pass Translation & Punctuation Removal ===")
    print(f"Before translate  : {messy_sentence}")
    print(f"After translate   : {cleaned_sentence}")


if __name__ == "__main__":
    main()
```

### Example 2: URL Slug Generator and Reverse Words (`example_02_slug_generator_and_word_reversal.py`)

```python
def generate_url_slug(title: str) -> str:
    """Convert an article title into a clean, lowercase, hyphen-separated URL slug."""
    cleaned_chars = [
        ch.lower() if ch.isalnum() else " "
        for ch in title
    ]
    words = "".join(cleaned_chars).split()
    return "-".join(words)


def reverse_words_in_string(s: str) -> str:
    """Reverse the order of words while collapsing multiple spaces to a single space."""
    return " ".join(s.split()[::-1])


def main() -> None:
    print("=== 1. Blog / E-Commerce URL Slug Generator ===")
    titles = [
        "  Phase 02: Python Data Structures & Algorithms! ",
        "Top 10 Interview Questions (2026 Edition)",
    ]
    for title in titles:
        print(f"  Title : {title!r}")
        print(f"  Slug  : {generate_url_slug(title)!r}")

    print("\n=== 2. Reverse Words in a String (Multiple Spaces Handled) ===")
    raw_input = "   the   sky   is   blue  "
    print(f"  Input  : {raw_input!r}")
    print(f"  Output : {reverse_words_in_string(raw_input)!r}")


if __name__ == "__main__":
    main()
```

### Example 3: `O(n)` Anagram Check & Longest Unique Substring (`example_03_anagram_and_sliding_window_strings.py`)

```python
def are_anagrams_ascii(s: str, t: str) -> bool:
    """Check if two lowercase English strings are anagrams in O(n) time and O(1) space."""
    if len(s) != len(t):
        return False
    counts = [0] * 26
    base = ord("a")
    for ch_s, ch_t in zip(s, t):
        counts[ord(ch_s) - base] += 1
        counts[ord(ch_t) - base] -= 1
    return all(c == 0 for c in counts)


def longest_unique_substring(s: str) -> tuple[int, str]:
    """Return (max_length, substring) of the longest substring with all unique chars."""
    last_seen: dict[str, int] = {}
    left = 0
    best_len = 0
    best_start = 0

    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        window_len = right - left + 1
        if window_len > best_len:
            best_len = window_len
            best_start = left

    return (best_len, s[best_start : best_start + best_len])


def main() -> None:
    print("=== 1. O(n) Anagram Check (26-Bucket Frequency Array) ===")
    for s1, s2 in [("listen", "silent"), ("rat", "car"), ("anagram", "nagaram")]:
        print(f"  are_anagrams({s1!r}, {s2!r}) -> {are_anagrams_ascii(s1, s2)}")

    print("\n=== 2. Longest Substring Without Repeating Characters ===")
    for sample in ["abcabcbb", "pwwkew", "dvdf"]:
        length, sub = longest_unique_substring(sample)
        print(f"  Input: {sample!r:<10} -> Max Length: {length} (Substring: {sub!r})")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== 1. Exact Prefix & Suffix Removal ===
Original Filename : 'test_user_controller.py'
Cleaned Stem      : 'user_controller'

=== 2. Safe Splitting with partition() & rpartition() ===
Username          : 'divya.tiwari'
Full Domain       : 'university.edu.in' (Sub: 'university.edu', TLD: 'in')

=== 3. Single-Pass Translation & Punctuation Removal ===
Before translate  : Hello, World! Python-3.13 is #1 for DSA!!!
After translate   : Hello World Python 3.13 is 1 for DSA
```

### Output for Example 2:
```text
=== 1. Blog / E-Commerce URL Slug Generator ===
  Title : '  Phase 02: Python Data Structures & Algorithms! '
  Slug  : 'phase-02-python-data-structures-algorithms'
  Title : 'Top 10 Interview Questions (2026 Edition)'
  Slug  : 'top-10-interview-questions-2026-edition'

=== 2. Reverse Words in a String (Multiple Spaces Handled) ===
  Input  : '   the   sky   is   blue  '
  Output : 'blue is sky the'
```

### Output for Example 3:
```text
=== 1. O(n) Anagram Check (26-Bucket Frequency Array) ===
  are_anagrams('listen', 'silent') -> True
  are_anagrams('rat', 'car') -> False
  are_anagrams('anagram', 'nagaram') -> True

=== 2. Longest Substring Without Repeating Characters ===
  Input: 'abcabcbb' -> Max Length: 3 (Substring: 'abc')
  Input: 'pwwkew'   -> Max Length: 3 (Substring: 'wke')
  Input: 'dvdf'     -> Max Length: 3 (Substring: 'vdf')
```

---

## 7. Code Explanation

- **`filename.removeprefix("test_")` vs `filename.lstrip("test_")`:** Had we used `.lstrip("test_")` on `"test_status.py"`, it would have stripped `'s'` and `'t'` from `"status"` too, corrupting it into `"atus.py"`! `.removeprefix("test_")` strips only the exact prefix `"test_"`.
- **`str.maketrans(from_str, to_str, delete_str)`:** Builds a Unicode code-point lookup table used by `.translate()` to map and delete characters in one fast `O(n)` pass.
- **`if ch in last_seen and last_seen[ch] >= left:`:** In the sliding window, checking `last_seen[ch] >= left` ensures we ignore stale occurrences of `ch` that fell outside the left boundary of our current window.

---

## 8. Common Mistakes

1. **Using `.lstrip("prefix")` or `.rstrip(".ext")` for Prefixes/Extensions:**
   `"script_test.py".rstrip(".py")` strips `'y'` and `'p'`, turning `"script_party.py"` into `"script_part"`! Always use `.removesuffix(".py")` and `.removeprefix("prefix")`.
2. **Passing Both a Dictionary and a Second Argument to `str.maketrans()`:**
   `str.maketrans()` accepts **either** 1 argument (a `dict` mapping characters/code-points to replacements or `None`) **or** 2–3 string arguments (`from_str, to_str[, delete_str]`).
3. **Forgetting `last_seen[ch] >= left` in Sliding Window:**
   On input `"abba"`, when `right` reaches the second `'a'` (index `3`) and `left` is at index `2` (the second `'b'`), `last_seen['a']` is `0` (`< left`). Without the `>= left` check, `left` would move **backward** to `0 + 1 = 1`!

---

## 9. Practice Questions

1. **Easy:** Write a function `is_isomorphic(s: str, t: str) -> bool` (LeetCode 205) that checks if characters in `s` can be replaced one-to-one to get `t` (e.g., `"egg"` and `"add"` -> `True`, `"foo"` and `"bar"` -> `False`).
2. **Medium:** Write a function `longest_palindromic_substring(s: str) -> str` (LeetCode 5) using the **Expand Around Center** technique (`O(n^2)` time, `O(1)` space) handling both odd-length (`i, i`) and even-length (`i, i + 1`) centers.
3. **Hard:** Write a function `min_window_substring(s: str, t: str) -> str` (LeetCode 76) that finds the minimum contiguous substring of `s` containing every character of `t` (including duplicates) in `O(|s| + |t|)` time using a variable-size sliding window.

---

## 10. Interview Questions

### Q1: Why is checking `sorted(s) == sorted(t)` suboptimal for large anagram checks compared to a frequency count?
**Answer:** `sorted(s) == sorted(t)` takes **`O(n log n)`** time and **`O(n)`** extra space to build two sorted character lists. A frequency counter (`collections.Counter(s) == collections.Counter(t)` or a 26-element array `[0] * 26` for lowercase English letters) runs in **`O(n)`** linear time and **`O(1)`** space (at most 26 buckets).

### Q2: How does `.casefold()` differ from `.lower()` in Python?
**Answer:** `.lower()` performs standard ASCII/basic Unicode lowercase conversion, whereas `.casefold()` performs aggressive Unicode case-folding designed for **case-insensitive string matching** across international alphabets (for example, converting the German character `'ß'` into `"ss"`).

### Q3: What is the time complexity of `s.replace(old, new)` when called in a loop of `k` different replacements on a string of length `n`?
**Answer:** Each `.replace()` call scans the entire string and allocates a new string in `O(n)` time, so `k` sequential `.replace()` calls take `O(k * n)` time. For single-character replacements or deletions, `s.translate(str.maketrans(...))` performs all `k` replacements in a single **`O(n)`** pass.
