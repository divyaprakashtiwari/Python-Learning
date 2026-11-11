# Section D: Arrays and Strings — Topic 06: String Problems

## 1. Introduction

**String Algorithms** are among the most frequently tested topics in software engineering interviews because text processing, log parsing, DNA sequence alignment, compiler lexing, and network protocol framing all operate on strings.

In Python, `str` objects are **immutable contiguous arrays of Unicode characters**. This immutability means:
- Concatenating inside a loop (`res += ch`) reallocates and copies the string on every step ($O(N^2)$ time), whereas accumulating into a `list[str]` and calling `"".join(parts)` runs in **$O(N)$ linear time**.
- Advanced string problems rely on three foundational patterns:
  1. **Expand-Around-Center ($2N - 1$ Centers):** Solves Palindromic Substring problems in $O(N^2)$ time and **$O(1)$ space** (vs $O(N^2)$ DP table memory).
  2. **KMP (Knuth-Morris-Pratt) LPS Table:** Solves exact substring matching in guaranteed **$O(N + M)$ worst-case linear time** (never backing up the text pointer `i`).
  3. **Canonical Frequency Signatures & Length-Prefixed Framing:** Groups anagrams in $O(N \cdot L)$ time without sorting, and encodes/decodes arbitrary string lists safely.

---

## 2. Why is it used?

1. **Eliminating $O(N \cdot M)$ Backtracking in Pattern Matching:**
   Naive substring search (`text.find(pattern)` in the worst case on repetitive strings like `"AAA...AAAB"`) backs up the text pointer `i` on every mismatch, taking $O(N \cdot M)$ time. The **KMP Algorithm** precomputes the **Longest Proper Prefix which is also a Suffix (LPS)** table in $O(M)$ time so `i` **never moves backward** — guaranteeing $O(N + M)$ time against algorithmic complexity DoS attacks!
2. **$O(1)$-Space Palindrome Detection:**
   A 2D Dynamic Programming table `dp[i][j]` for Longest Palindromic Substring on a $10,000$-character string allocates $10^8$ booleans ($\sim 100\text{ MB}$). Expanding outward from each of the $2N - 1$ centers uses **$O(1)$ auxiliary memory** and stops early on the very first mismatch!

---

## 3. Syntax & Core Blueprints

### Blueprint 1: Expand Around All $2N - 1$ Palindrome Centers ($O(N^2)$ Time, $O(1)$ Space)
```python
def expand(s: str, left: int, right: int) -> tuple[int, int]:
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    return left + 1, right  # Valid slice s[left+1 : right]

for i in range(len(s)):
    odd_start, odd_end = expand(s, i, i)          # Odd length ("aba")
    even_start, even_end = expand(s, i, i + 1)    # Even length ("abba")
```

### Blueprint 2: KMP LPS (Failure Function) Table ($O(M)$ Time)
```python
def build_lps(pattern: str) -> list[int]:
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps
```

---

## 4. Step-by-Step Explanation & Complexity Analysis

### 1. Why There Are Exactly $2N - 1$ Palindrome Centers
A palindrome of **odd** length (e.g., `"racecar"`, length 7) is centered on a **single character** (`'e'` at index `i`) — there are $N$ such centers.
A palindrome of **even** length (e.g., `"abba"`, length 4) is centered **between two adjacent characters** (`(i, i + 1)`) — there are $N - 1$ such centers.
Total centers $= N + (N - 1) = 2N - 1$. Expanding from each takes $O(N)$ worst-case time $\rightarrow$ $O(N^2)$ time and $O(1)$ space!

### 2. How KMP Uses the LPS Table to Avoid Backing Up `i`
Suppose `pattern = "ABABCABAB"`. Its LPS array is `[0, 0, 1, 2, 0, 1, 2, 3, 4]`.
- `lps[8] = 4` means the 4-character prefix `"ABAB"` is also a suffix of `"ABABCABAB"`.
- If a mismatch occurs right after matching index `8` (or after a full match), we already know the last 4 characters of `text` matched `"ABAB"`, so we simply set `j = lps[j - 1] = 4` and keep `i` moving forward!

| Algorithm / Problem | Brute Force | Optimal Time | Auxiliary Space |
| :--- | :--- | :--- | :--- |
| **Longest Palindromic Substring** | $O(N^3)$ | $O(N^2)$ (Expand) / $O(N)$ (Manacher) | $O(1)$ |
| **Substring Pattern Search (KMP)** | $O(N \cdot M)$ | $O(N + M)$ | $O(M)$ LPS table |
| **Group $N$ Words of Length $L$** | $O(N \cdot L \log L)$ | $O(N \cdot L)$ (26-tuple key) | $O(N \cdot L)$ |
| **Length-Prefixed Encode/Decode** | Escaping $O(N^2)$ | $O(N)$ | $O(N)$ |

---

## 5. Practical Examples (3 Complete Programs)

### Example 1: Expand-Around-Center Palindromes (`example_01_expand_around_center_palindromes.py`)
```python
def expand_around_center(s: str, left: int, right: int) -> tuple[int, int, int]:
    n = len(s)
    count = 0
    while left >= 0 and right < n and s[left] == s[right]:
        count += 1
        left -= 1
        right += 1
    return left + 1, right, count
```

### Example 2: KMP Pattern Matching & LPS Table (`example_02_kmp_pattern_matching_and_lps_table.py`)
```python
def kmp_search_all(text: str, pattern: str) -> tuple[list[int], list[int]]:
    if not pattern:
        return [0], []

    lps = build_kmp_lps_table(pattern)
    matches: list[int] = []
    i = 0
    j = 0
    n, m = len(text), len(pattern)

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                matches.append(i - m)
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches, lps
```

### Example 3: Group Anagrams ($O(N \cdot L)$) & Length-Prefixed Codec (`example_03_group_anagrams_and_length_prefixed_codec.py`)
```python
def group_anagrams_linear(words: list[str]) -> list[list[str]]:
    groups: dict[tuple[int, ...], list[str]] = defaultdict(list)

    for word in words:
        counts = [0] * 26
        for ch in word:
            counts[ord(ch) - ord("a")] += 1
        groups[tuple(counts)].append(word)

    return list(groups.values())
```

---

## 6. Verified Console Output

### Output of `example_01_expand_around_center_palindromes.py`
```text
========================================================================
1. EXPAND-AROUND-CENTER: LONGEST PALINDROME & TOTAL COUNT
========================================================================
  String: 'babad         ' -> Longest Palindrome: 'bab    ' | Total Palindromic Substrings: 7
  String: 'cbbd          ' -> Longest Palindrome: 'bb     ' | Total Palindromic Substrings: 5
  String: 'racecar       ' -> Longest Palindrome: 'racecar' | Total Palindromic Substrings: 10
  String: 'aaa           ' -> Longest Palindrome: 'aaa    ' | Total Palindromic Substrings: 6
  String: 'abacdfgdcaba  ' -> Longest Palindrome: 'aba    ' | Total Palindromic Substrings: 14
```

### Output of `example_02_kmp_pattern_matching_and_lps_table.py`
```text
========================================================================
1. KNUTH-MORRIS-PRATT (KMP) O(N + M) STRING MATCHING & LPS TABLE
========================================================================
Text    : 'ABABDABACDABABCABABABABCABAB'
Pattern : 'ABABCABAB'
LPS     : [0, 0, 1, 2, 0, 1, 2, 3, 4]
Matches : [10, 19] (Overlapping matches found in a single pass!)
```

### Output of `example_03_group_anagrams_and_length_prefixed_codec.py`
```text
========================================================================
1. GROUP ANAGRAMS IN O(N * L) TIME VIA 26-TUPLE SIGNATURE
========================================================================
Input Words    : ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']
Anagram Groups : [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]

========================================================================
2. LENGTH-PREFIXED STRING ENCODE & DECODE (LEETCODE 271)
========================================================================
Original List  : ['hello#world', '12#34', '', 'antigravity:python']
Wire Payload   : '11#hello#world5#12#340#18#antigravity:python'
Decoded List   : ['hello#world', '12#34', '', 'antigravity:python']
```

---

## 7. Code Explanation

1. **Why `"abacdfgdcaba"` Proves Longest Palindromic Substring Is NOT Just Longest Common Substring with `s[::-1]`:**
   Beginners often propose: *"Reverse `s` and find the Longest Common Substring between `s` and `s[::-1]`!"* On `s = "abacdfgdcaba"`, `s[::-1]` is `"abacdgfdcaba"`. Their longest common substring is `"abacd"` (length 5), which is **not a palindrome** (it matched `"abacd"` at the front with the reversed `"dcaba"` at the back!). Expand-Around-Center correctly returns `"aba"`.
2. **Why `<len>#<payload>` Framing Is Immune to Delimiter Injection:**
   If you join strings with a delimiter like `","` or `"#"`, any string that naturally contains `"#"` (like `"hello#world"` or `"12#34"`) breaks `.split("#")`! By reading the integer `length` up to the first `"#"` and then slicing **exact byte/character offsets** `encoded[sep_idx + 1 : sep_idx + 1 + length]`, any `"#"` or digits inside the payload are skipped over blindly — the exact same framing used in HTTP `Content-Length` and Redis RESP!

---

## 8. Common Mistakes

1. **Forgetting Even-Length Centers `(i, i + 1)` in Palindrome Expansion:**
   If you only expand around `(i, i)`, your code will completely miss even-length palindromes like `"cbbd"` $\rightarrow$ `"bb"`! Always call `expand` twice per index: `(i, i)` and `(i, i + 1)`.
2. **Using a `list` Instead of a `tuple` as a Dictionary Key (`groups[counts]`):**
   In Python, `list` is mutable and unhashable (`TypeError: unhashable type: 'list'`). Always convert `counts` to `tuple(counts)` before indexing `groups[tuple(counts)]`.

---

## 9. Practice Questions

1. **Easy — Reverse Words in a String (LeetCode 151):** Given an input string `s`, reverse the order of the words while collapsing multiple spaces into a single space (`" ".join(reversed(s.split()))`), and also implement the in-place `list[str]` two-pointer reversal version (reverse whole char array, then reverse each individual word).
2. **Medium — Longest Common Prefix & String Compression (LeetCode 14 / 443):** Compress a character array `["a","a","b","b","c","c","c"]` in-place to `["a","2","b","2","c","3"]` using Reader/Writer two pointers in $O(N)$ time and $O(1)$ space.
3. **Hard — Shortest Palindrome by Prepending Characters (LeetCode 214):** Given a string `s`, find the shortest palindrome you can form by adding characters in front of `s` in **$O(N)$ linear time** by computing the KMP LPS table of `s + "#" + s[::-1]`!

---

## 10. Interview Questions

### Q1: How does Rabin-Karp (Rolling Hash) compare to KMP for substring matching?
**Answer:**
- **KMP** runs in deterministic **$O(N + M)$ worst-case time** using an $O(M)$ LPS table and is ideal for searching a **single pattern**.
- **Rabin-Karp** computes a polynomial rolling hash $\sum s[i] \cdot B^{k} \pmod P$ in $O(1)$ per slide ($O(N + M)$ average time, $O(N \cdot M)$ worst-case on hash collisions). Its killer advantage is **multi-pattern search** (finding any of $K$ patterns of length $M$ in $O(N + K \cdot M)$ time using a hash set of pattern hashes) and **Longest Duplicate Substring** (Binary Search on length + Rolling Hash).

### Q2: Why does `s + "#" + s[::-1]` with KMP's LPS table find the longest palindromic prefix of `s` in $O(N)$ time?
**Answer:**
A prefix of `s` is a palindrome if and only if it equals its own reversal (which sits at the **suffix** of `s[::-1]`). By concatenating `combined = s + "#" + s[::-1]` (where `"#"` prevents matches from crossing the middle boundary), `lps[-1]` gives the exact length of the longest prefix of `s` that is also a suffix of `s[::-1]` — i.e., the **longest palindromic prefix of `s`** in $O(N)$ time!
