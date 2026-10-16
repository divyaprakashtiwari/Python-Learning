"""
Topic 02: Control Flow
Question 03: for Loop Fundamentals

Master iteration in Python: range mechanics, enumerate, zip, dictionary traversal,
accumulation patterns, reversed sequences, matrix iteration, and batch processing.
"""

from itertools import zip_longest

# ============================================================
# Q1: Range Object Mechanics and Lazy Evaluation
# ============================================================
# Question: Demonstrate all variations of the `range()` function (start, stop, step),
# negative steps, and show that `range` is an immutable, lazy sequence object.

print("=== Q1: range() Object Mechanics ===")

# 1. Single argument: stop (0 to stop - 1)
stop_range = list(range(5))
print(f"  range(5):               {stop_range}")

# 2. Two arguments: start, stop [start, stop)
start_stop_range = list(range(10, 15))
print(f"  range(10, 15):          {start_stop_range}")

# 3. Three arguments: positive step
step_range = list(range(0, 20, 3))
print(f"  range(0, 20, 3):        {step_range}")

# 4. Negative step: countdown
countdown = list(range(10, 0, -2))
print(f"  range(10, 0, -2):       {countdown}")

# 5. Memory efficiency: range does not allocate all numbers in memory!
huge_range = range(0, 1_000_000_000, 7)
import sys
print(f"  Memory of range(1 Billion): {sys.getsizeof(huge_range)} bytes")
print(f"  Index access huge_range[100]: {huge_range[100]}")
print(f"  Length of huge_range: {len(huge_range):,}")

# Explanation: `range()` creates a lazy sequence object that computes elements on demand.
# It uses $O(1)$ memory regardless of how large the interval is.


# ============================================================
# Q2: Pythonic Index Tracking with `enumerate()`
# ============================================================
# Question: Demonstrate why `for i in range(len(lst))` is an anti-pattern in Python,
# and use `enumerate()` with custom start indices to format ranked lists.

print("\n=== Q2: Index Tracking with enumerate() ===")

top_languages = ["Python", "Rust", "Go", "TypeScript", "Kotlin"]

# Anti-pattern:
# for i in range(len(top_languages)):
#     print(f"{i}: {top_languages[i]}")

# Pythonic Pattern: enumerate() gives (index, value) tuples directly
print("  Ranked Leaderboard (1-based index):")
for rank, lang in enumerate(top_languages, start=1):
    medal = "[#1]" if rank == 1 else "[#2]" if rank == 2 else "[#3]" if rank == 3 else f"[#{rank}]"
    print(f"    {medal:<6} {lang}")

# Unpacking in enumerate
tasks = [("Fix auth bug", "HIGH"), ("Refactor CSS", "LOW"), ("Write tests", "CRITICAL")]
print("\n  Task Priority Matrix:")
for idx, (task_title, priority) in enumerate(tasks, start=101):
    print(f"    [ID: {idx}] [{priority:<8}] {task_title}")

# Explanation: `enumerate()` is cleaner, faster, and avoids clumsy index subscripting (`arr[i]`),
# eliminating off-by-one errors and out-of-bounds exceptions.


# ============================================================
# Q3: Parallel Iteration with `zip()` and `zip_longest()`
# ============================================================
# Question: Iterate multiple lists in lockstep using `zip()`, enforce length matching
# using `strict=True`, and handle uneven lengths with `itertools.zip_longest()`.

print("\n=== Q3: Parallel Iteration with zip() ===")

names = ["Alice", "Bob", "Charlie"]
scores = [95, 88, 92]
roles = ["Architect", "Developer", "Designer"]

print("  Zipping 3 lists in parallel:")
for name, score, role in zip(names, scores, roles):
    print(f"    {name:<8} ({role:<10}) -> Score: {score}")

# Handling uneven lengths:
cities = ["New York", "London", "Tokyo", "Berlin", "Paris"]
temps_c = [22, 18, 26]  # Missing temperatures for Berlin and Paris

# Standard zip truncates to the shortest list
standard_zip = list(zip(cities, temps_c))
print(f"\n  Standard zip (truncated to shortest): {len(standard_zip)} pairs")

# zip_longest fills missing values with fillvalue
print("  zip_longest with default fallback value:")
for city, temp in zip_longest(cities, temps_c, fillvalue="N/A"):
    formatted_temp = f"{temp} deg C" if isinstance(temp, (int, float)) else temp
    print(f"    {city:<10}: {formatted_temp}")

# Python 3.10+ strict=True raises ValueError on length mismatch
try:
    for c, t in zip(cities, temps_c, strict=True):
        pass
except ValueError as e:
    print(f"\n  zip(strict=True) caught uneven length: {e}")

# Explanation: `zip()` stops at the shortest iterator by default. Use `strict=True`
# when unequal lengths represent data corruption, and `zip_longest` when missing data is expected.


# ============================================================
# Q4: Traversing Dictionaries (.keys, .values, .items)
# ============================================================
# Question: Traverse dictionary keys, values, and item pairs.
# Group and aggregate item costs by department.

print("\n=== Q4: Traversing Dictionaries ===")

department_expenses = {
    "Engineering": [12_000, 4_500, 8_200],
    "Marketing":   [5_000, 3_200],
    "Sales":       [7_500, 9_100, 2_400, 1_800],
    "Operations":  [3_400, 1_200]
}

total_company_spend = 0
print(f"  {'Department':<15} {'Entries':<10} {'Total Cost':<15} {'Average Spend'}")
print("  " + "-" * 55)

# Iterating with .items() gives (key, value) pairs
for dept, expenses in department_expenses.items():
    dept_sum = sum(expenses)
    dept_avg = dept_sum / len(expenses) if expenses else 0.0
    total_company_spend += dept_sum
    print(f"  {dept:<15} {len(expenses):<10} ${dept_sum:>9,d}    ${dept_avg:>8,.2f}")

print("  " + "-" * 55)
print(f"  Total Company Expenditure: ${total_company_spend:,.2f}")

# Explanation: Using `.items()` avoids repeated dictionary lookups (`d[k]`)
# inside the loop body, delivering cleaner syntax and $O(1)$ per-item retrieval.


# ============================================================
# Q5: Manual Accumulation Patterns (Running Stats)
# ============================================================
# Question: Write a loop that processes a numeric stream without built-ins (sum, max, min)
# to compute count, total, running average, minimum, maximum, and product.

print("\n=== Q5: Manual Accumulation Patterns ===")

numbers = [14, 28, 7, 45, 92, 33, 19, 58]

# Initialize accumulators
count = 0
total = 0
product = 1
minimum = float('inf')
maximum = float('-inf')

for num in numbers:
    count += 1
    total += num
    product *= num
    if num < minimum:
        minimum = num
    if num > maximum:
        maximum = num

average = total / count if count > 0 else 0.0

print(f"  Dataset: {numbers}")
print(f"  Count:   {count}")
print(f"  Total:   {total}")
print(f"  Average: {average:.2f}")
print(f"  Minimum: {minimum}")
print(f"  Maximum: {maximum}")

# Factorial via for loop accumulation
def compute_factorial(n: int) -> int:
    """Computes n! iteratively."""
    if n < 0:
        raise ValueError("Factorial undefined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

print(f"  Factorial 6! = {compute_factorial(6)} (720)")
print(f"  Factorial 10! = {compute_factorial(10):,}")

# Explanation: Initializing `minimum = float('inf')` and `maximum = float('-inf')`
# guarantees that the first element in any non-empty sequence correctly updates both bounds.


# ============================================================
# Q6: Reverse Iteration (`reversed()` vs Slicing)
# ============================================================
# Question: Demonstrate memory-efficient reverse traversal using `reversed()`
# versus slice copies (`[::-1]`), and verify a palindrome using two-pointer for loops.

print("\n=== Q6: Reverse Iteration and Palindromes ===")

items = ["alpha", "beta", "gamma", "delta", "epsilon"]

# Method 1: Slicing creates an entirely NEW list in memory
slice_copy = items[::-1]
print(f"  Reversed via slice [::-1]: {slice_copy}")

# Method 2: reversed() returns an iterator without creating a new list
print("  Reversed via reversed() iterator:")
for item in reversed(items):
    print(f"    <- {item}")

# Palindrome verification using loop with symmetric indexing
def is_palindrome_loop(text: str) -> bool:
    """Checks if cleaned string is identical forwards and backwards."""
    clean = "".join(c.lower() for c in text if c.isalnum())
    n = len(clean)
    for i in range(n // 2):
        if clean[i] != clean[n - 1 - i]:
            return False
    return True

phrases = ["Racecar", "A man, a plan, a canal: Panama", "Hello Python", "No lemon, no melon"]
for p in phrases:
    pal = is_palindrome_loop(p)
    print(f"  '{p[:30]:<32}' -> {'PALINDROME' if pal else 'NOT PALINDROME'}")

# Explanation: `reversed()` requires $O(1)$ auxiliary memory because it yields
# elements from the end of reversible sequences without duplicating the underlying buffer.


# ============================================================
# Q7: Character Classification and Frequency Counter
# ============================================================
# Question: Iterate through a text string and categorize each character:
# vowels, consonants, digits, whitespace, and punctuation symbols.

print("\n=== Q7: Character Analysis and Frequency ===")

sample_text = "Python 3.13 is blazingly FAST & clean!"

vowels = "aeiou"
categories = {
    "vowels": 0,
    "consonants": 0,
    "digits": 0,
    "whitespace": 0,
    "punctuation": 0
}

char_frequencies = {}

for ch in sample_text:
    # Character frequency
    lower_ch = ch.lower()
    char_frequencies[lower_ch] = char_frequencies.get(lower_ch, 0) + 1
    
    # Categorization
    if ch.isalpha():
        if lower_ch in vowels:
            categories["vowels"] += 1
        else:
            categories["consonants"] += 1
    elif ch.isdigit():
        categories["digits"] += 1
    elif ch.isspace():
        categories["whitespace"] += 1
    else:
        categories["punctuation"] += 1

print(f"  Input text: \"{sample_text}\"")
print(f"  Character Breakdown:")
for cat, cnt in categories.items():
    print(f"    {cat.capitalize():<14}: {cnt}")

top_3_chars = sorted(char_frequencies.items(), key=lambda pair: pair[1], reverse=True)[:3]
print(f"  Most frequent chars: {top_3_chars}")

# Explanation: Strings in Python are iterable sequence types yielding individual 1-character
# strings on each iteration step.


# ============================================================
# Q8: The Mutation Pitfall: Modifying a List During Iteration
# ============================================================
# Question: Demonstrate the dangerous bug caused by mutating (removing elements from)
# a list while iterating over it, and show the two correct patterns to solve it.

print("\n=== Q8: List Mutation During Iteration Pitfall ===")

# THE BUG: Deleting even numbers while iterating
buggy_list = [1, 2, 4, 5, 6, 8, 9, 10]
# Expected: [1, 5, 9]

# Anti-pattern:
# When index 1 ('2') is removed, '4' shifts into index 1, but loop moves to index 2!
# Element '4' is skipped completely!
for x in buggy_list[:]:  # Safe slice copy demo
    pass

# Demonstrate the bug on a dummy copy
demo_bad = [1, 2, 4, 5, 6, 8, 9, 10]
for val in demo_bad:
    if val % 2 == 0:
        demo_bad.remove(val)
print(f"  Buggy removal result (elements skipped!): {demo_bad}")

# SOLUTION 1: Iterate over a shallow copy with [:]
safe_list_1 = [1, 2, 4, 5, 6, 8, 9, 10]
for val in safe_list_1[:]:  # Slicing creates a snapshot copy
    if val % 2 == 0:
        safe_list_1.remove(val)
print(f"  Solution 1 (iterate over snapshot copy):   {safe_list_1}")

# SOLUTION 2: Filter into a new list (most Pythonic & fastest: O(N) vs O(N^2))
original = [1, 2, 4, 5, 6, 8, 9, 10]
filtered = [x for x in original if x % 2 != 0]
print(f"  Solution 2 (list comprehension / filter): {filtered}")

# Explanation: Mutating a sequence changes its internal indices. The iterator's
# cursor advances unconditionally, causing subsequent elements to be skipped.


# ============================================================
# Q9: Multi-Dimensional Grid and Matrix Traversal
# ============================================================
# Question: Given an N x N matrix, use nested `for` loops to:
# 1. Print the formatted grid.
# 2. Compute the sum of each row and column.
# 3. Compute primary and secondary diagonal sums.

print("\n=== Q9: Matrix Traversal and Diagonals ===")

matrix = [
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
]

n = len(matrix)

print("  Grid Display:")
for row in matrix:
    row_str = "  ".join(f"{val:>4}" for val in row)
    print(f"    [ {row_str} ]")

# Row sums
row_sums = []
for r in range(n):
    r_sum = 0
    for c in range(n):
        r_sum += matrix[r][c]
    row_sums.append(r_sum)
print(f"\n  Row sums:    {row_sums}")

# Column sums
col_sums = []
for c in range(n):
    c_sum = 0
    for r in range(n):
        c_sum += matrix[r][c]
    col_sums.append(c_sum)
print(f"  Column sums: {col_sums}")

# Diagonals
primary_diagonal = 0
secondary_diagonal = 0
for i in range(n):
    primary_diagonal += matrix[i][i]              # Top-left to bottom-right
    secondary_diagonal += matrix[i][n - 1 - i]    # Top-right to bottom-left

print(f"  Primary Diagonal (10+50+90):   {primary_diagonal}")
print(f"  Secondary Diagonal (30+50+70): {secondary_diagonal}")

# Explanation: For an $N \times N$ matrix, the primary diagonal has coordinates $(i, i)$
# and the secondary diagonal has coordinates $(i, n - 1 - i)$.


# ============================================================
# Q10: Batch Stream / Chunk Processing Engine
# ============================================================
# Question: Build a batch processor that chunks a dataset of arbitrary size into
# batches of fixed size `k`, processing each chunk and reporting remaining tails.

print("\n=== Q10: Batch Stream Processing ===")

def process_in_batches(dataset: list, batch_size: int) -> list[dict]:
    """Slices a dataset into sequential batches for processing."""
    if batch_size <= 0:
        raise ValueError("Batch size must be >= 1")
        
    batch_reports = []
    total_items = len(dataset)
    
    # Range with step size = batch_size
    for batch_num, start_idx in enumerate(range(0, total_items, batch_size), start=1):
        end_idx = min(start_idx + batch_size, total_items)
        chunk = dataset[start_idx:end_idx]
        
        # Simulate processing work
        batch_sum = sum(chunk)
        batch_reports.append({
            "batch_number": batch_num,
            "range": f"[{start_idx}:{end_idx}]",
            "size": len(chunk),
            "items": chunk,
            "sum": batch_sum
        })
        
    return batch_reports

records = [15, 23, 8, 42, 67, 91, 12, 34, 55, 78, 99]  # 11 items
batch_k = 3

reports = process_in_batches(records, batch_k)
for b in reports:
    print(f"  Batch #{b['batch_number']} (Items {b['size']}): {str(b['items']):<18} | Sum: {b['sum']}")

# Summary Output
print("\n" + "=" * 55)
print("  All 10 Questions for Topic 02 - Q03 executed successfully!")
print("=" * 55)
