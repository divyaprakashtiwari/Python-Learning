"""
Topic 03: Data Structures
Question 08: List Comprehensions (and Set/Dict Comprehensions Deep Dive)

Master Python comprehensions from fundamentals to advanced patterns:
- Syntax mechanics and performance vs map/filter/loops
- Filtering (trailing if) vs Ternary transformation (leading if-else)
- Nested comprehensions for 2D matrix flattening
- Matrix transposition and coordinate grids
- Multi-clause loops (Cartesian product vs zip)
- Set and dictionary comprehensions
- Walrus operator (:=) inside comprehensions to eliminate redundant calls
- Inverting, grouping, and restructuring data payloads
- Memory efficiency: List comprehension vs Generator expression
- Real-world log processing pipeline using composable comprehensions
"""

import sys
from typing import Any, Dict, List, Set, Tuple


# ============================================================
# Q1: Basic Comprehension vs map/filter Syntax & Readability
# ============================================================
# Question: Convert a traditional for-loop and a map/filter combination into idiomatic
# list comprehensions. Square only the even numbers from 0 to 9.

print("=== Q1: Comprehension vs map/filter ===")

raw_nums = list(range(10))

# 1. Imperative loop
loop_result = []
for n in raw_nums:
    if n % 2 == 0:
        loop_result.append(n ** 2)

# 2. Functional map + filter
map_filter_result = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, raw_nums)))

# 3. Pythonic list comprehension
comp_result = [n ** 2 for n in raw_nums if n % 2 == 0]

print(f"  Loop result:          {loop_result}")
print(f"  Map/Filter result:    {map_filter_result}")
print(f"  Comprehension result: {comp_result}")

assert loop_result == map_filter_result == comp_result == [0, 4, 16, 36, 64]

# Explanation: List comprehensions run at C-speed in CPython (bytecode instruction
# LIST_APPEND) without the overhead of lambda function call frames required by map/filter.


# ============================================================
# Q2: Trailing Filter `if` vs Leading Ternary `if-else`
# ============================================================
# Question: Demonstrate the crucial syntactic difference between:
# 1) Filtering items (trailing `if`)
# 2) Transforming items conditionally (leading `x if cond else y`)
# Categorize numbers as "EVEN" or "ODD", but only for numbers divisible by 3.

print("\n=== Q2: Trailing Filter `if` vs Leading Ternary `if-else` ===")

numbers = list(range(1, 13))

# Trailing 'if' acts as a FILTER (omits elements)
divisible_by_3 = [x for x in numbers if x % 3 == 0]
print(f"  Only divisible by 3 (Filter): {divisible_by_3}")
assert divisible_by_3 == [3, 6, 9, 12]

# Leading 'if-else' acts as a TRANSFORMATION (preserves length, changes value)
parity_labels = ["EVEN" if x % 2 == 0 else "ODD" for x in numbers]
print(f"  Parity transformation (first 6): {parity_labels[:6]}")
assert parity_labels[:4] == ["ODD", "EVEN", "ODD", "EVEN"]

# Combining BOTH: Transform only the filtered elements
combined = [f"{x}:EVEN" if x % 2 == 0 else f"{x}:ODD" for x in numbers if x % 3 == 0]
print(f"  Combined (Div by 3 with parity label): {combined}")
assert combined == ["3:ODD", "6:EVEN", "9:ODD", "12:EVEN"]

# Explanation:
# [ <expr> for <var> in <iterable> if <filter_condition> ]
# [ <val_if_true> if <cond> else <val_if_false> for <var> in <iterable> ]


# ============================================================
# Q3: Nested Comprehensions & 2D Matrix Flattening
# ============================================================
# Question: Flatten a 2D matrix into a 1D list using a list comprehension.
# Explain loop ordering in multi-for comprehensions.

print("\n=== Q3: Matrix Flattening & Loop Order ===")

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Note: The order of `for` clauses matches the order of nested imperative loops:
# for row in matrix:
#     for item in row:
#         flattened.append(item)
flattened = [item for row in matrix for item in row]

print(f"  Original 3x3 matrix: {matrix}")
print(f"  Flattened 1D list:   {flattened}")

assert flattened == [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Flatten with filter: only even elements from rows whose index is >= 1
filtered_flat = [item for row_idx, row in enumerate(matrix) if row_idx >= 1 for item in row if item % 2 == 0]
print(f"  Filtered flat (row >= 1, even items): {filtered_flat}")
assert filtered_flat == [4, 6, 8]

# Explanation: Clauses in a list comprehension read from left to right, exactly
# matching the nesting order of nested `for` statements.


# ============================================================
# Q4: Matrix Transposition & Grid Transformations
# ============================================================
# Question: Transpose an N x M rectangular matrix (swap rows and columns)
# using a nested list comprehension without importing any external libraries.

print("\n=== Q4: Matrix Transposition ===")

rect_matrix = [
    ["A1", "B1", "C1", "D1"],
    ["A2", "B2", "C2", "D2"],
    ["A3", "B3", "C3", "D3"]
]  # 3 rows x 4 columns

# Transposition: outer comprehension iterates over columns (0..3),
# inner comprehension extracts row[col_idx] for each row in matrix
transposed = [[row[col_idx] for row in rect_matrix] for col_idx in range(len(rect_matrix[0]))]

print(f"  Original shape: {len(rect_matrix)} rows x {len(rect_matrix[0])} cols")
print(f"  Transposed shape: {len(transposed)} rows x {len(transposed[0])} cols")
for r in transposed:
    print(f"    {r}")

assert len(transposed) == 4
assert len(transposed[0]) == 3
assert transposed[0] == ["A1", "A2", "A3"]
assert transposed[3] == ["D1", "D2", "D3"]

# Alternative built-in idiom: [list(c) for c in zip(*rect_matrix)]
assert transposed == [list(c) for c in zip(*rect_matrix)]

# Explanation: A nested comprehension `[ [expr for inner in ...] for outer in ... ]`
# builds a list of lists, where the outer loop determines rows of the result.


# ============================================================
# Q5: Cartesian Product with Custom Constraints
# ============================================================
# Question: Generate all valid playing card deck combinations (Rank x Suit)
# and filter pairs of dice rolls that sum to an exact target (e.g., 7).

print("\n=== Q5: Cartesian Products & Constraint Filtering ===")

suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

deck = [(rank, suit) for suit in suits for rank in ranks]
print(f"  Total standard deck cards: {len(deck)}")
print(f"  First 3 cards: {deck[:3]}")
assert len(deck) == 52

# Dice rolls summing to 7: two 6-sided dice (1..6)
dice_rolls = [(d1, d2) for d1 in range(1, 7) for d2 in range(1, 7) if d1 + d2 == 7]
print(f"  Dice combinations summing to 7: {dice_rolls}")
assert len(dice_rolls) == 6
assert dice_rolls == [(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)]

# Explanation: Multi-clause comprehensions cleanly compute Cartesian products
# with inline relational constraints without requiring `itertools.product`.


# ============================================================
# Q6: Set Comprehensions (Deduplication & Canonical Normalization)
# ============================================================
# Question: Normalize a list of raw email strings (mixed case, whitespace, duplicates, invalid)
# into a clean set of domain names using a set comprehension.

print("\n=== Q6: Set Comprehensions ===")

raw_emails = [
    "  Alice@EXAMPLE.com  ",
    "bob@work.net",
    "ALICE@example.COM",    # Duplicate domain and user
    "charlie@Example.Com",  # Duplicate domain
    "invalid-email-address",
    "diana@WORK.NET",       # Duplicate domain
    "evan@sub.domain.org"
]

# Set comprehension automatically enforces uniqueness and unordered set semantics
unique_domains: Set[str] = {
    email.strip().lower().split("@")[1]
    for email in raw_emails
    if "@" in email and "." in email.split("@")[1]
}

print(f"  Extracted canonical unique domains: {sorted(list(unique_domains))}")
assert unique_domains == {"example.com", "work.net", "sub.domain.org"}

# Word lengths set
sentence = "the quick brown fox jumps over the lazy dog"
unique_word_lengths = {len(w) for w in sentence.split()}
print(f"  Unique word lengths: {sorted(list(unique_word_lengths))}")
assert unique_word_lengths == {3, 4, 5}

# Explanation: Set comprehensions `{expr for x in iterable}` use curly braces
# with a single expression, providing automatic O(1) deduplication.


# ============================================================
# Q7: Dictionary Comprehensions (Inversion, Filtering, Grouping)
# ============================================================
# Question: Demonstrate dictionary comprehensions for:
# 1) Key-value inversion
# 2) Filtering dict by values
# 3) Transforming keys and values simultaneously

print("\n=== Q7: Dictionary Comprehensions ===")

stock_prices = {
    "AAPL": 178.50,
    "GOOGL": 142.20,
    "MSFT": 420.00,
    "AMZN": 180.10,
    "TSLA": 165.00
}

# 1. Filtering stocks over $175 with 10% price markup
premium_stocks = {
    ticker: round(price * 1.10, 2)
    for ticker, price in stock_prices.items()
    if price >= 175.00
}
print(f"  Premium stocks (+10%): {premium_stocks}")
assert set(premium_stocks.keys()) == {"AAPL", "MSFT", "AMZN"}
assert premium_stocks["AAPL"] == round(178.50 * 1.10, 2)

# 2. Inverting unique mapping: role -> user
user_roles = {"alice": "Admin", "bob": "Editor", "charlie": "Viewer"}
role_to_user = {role.lower(): user.capitalize() for user, role in user_roles.items()}
print(f"  Inverted roles: {role_to_user}")
assert role_to_user["admin"] == "Alice"
assert role_to_user["editor"] == "Bob"

# Explanation: Dict comprehensions `{k_expr: v_expr for item in iterable}` offer
# declarative dictionary generation, filtering, and key/value transformation.


# ============================================================
# Q8: Walrus Operator (:=) inside Comprehensions
# ============================================================
# Question: Use the assignment expression (walrus operator `:=`) inside a comprehension
# to avoid executing an expensive or repetitive computation twice (e.g. in filter and output).

print("\n=== Q8: Walrus Operator in Comprehensions ===")

expensive_calls = 0

def simulate_heavy_compute(val: int) -> int:
    """Simulates an expensive calculation or database query."""
    global expensive_calls
    expensive_calls += 1
    return (val ** 3) - (val * 2)

raw_inputs = [1, 2, 3, 4, 5, 6, 7, 8]

# WITHOUT walrus: simulate_heavy_compute is evaluated TWICE per item (once in `if`, once in output)!
expensive_calls = 0
naive_results = [
    simulate_heavy_compute(x)
    for x in raw_inputs
    if simulate_heavy_compute(x) > 50
]
naive_count = expensive_calls

# WITH walrus operator: store result in `res` during filter check, reuse in expression!
expensive_calls = 0
walrus_results = [
    res
    for x in raw_inputs
    if (res := simulate_heavy_compute(x)) > 50
]
walrus_count = expensive_calls

print(f"  Filtered results: {walrus_results}")
print(f"  Function calls WITHOUT walrus: {naive_count}")
print(f"  Function calls WITH walrus:    {walrus_count}")

assert naive_results == walrus_results
assert walrus_count == len(raw_inputs)  # Evaluated exactly once per input element!
assert naive_count > walrus_count       # Naive ran extra evaluations on passing elements

# Explanation: Introduced in Python 3.8, `(target := expr)` binds the expression
# value to a variable in the local scope, preventing redundant function invocations.


# ============================================================
# Q9: Generator Expressions vs List Comprehensions (Memory Benchmark)
# ============================================================
# Question: Compare memory footprint and lazy evaluation between a list comprehension
# `[x for x in ...]` and a generator expression `(x for x in ...)`.

print("\n=== Q9: Generator Expression vs List Comprehension ===")

N = 100_000

# List comprehension: Eagerly creates and stores 100,000 items in memory
list_comp = [x * 2 for x in range(N)]
list_mem = sys.getsizeof(list_comp)

# Generator expression: Evaluates lazily on demand, constant memory overhead
gen_expr = (x * 2 for x in range(N))
gen_mem = sys.getsizeof(gen_expr)

print(f"  List comprehension size for {N:,} elements: {list_mem:,} bytes")
print(f"  Generator expression size for {N:,} elements: {gen_mem:,} bytes")
print(f"  Memory reduction ratio: {list_mem / gen_mem:.1f}x smaller")

# Generator yields correct values on demand
first_five = [next(gen_expr) for _ in range(5)]
print(f"  First 5 items yielded from generator: {first_five}")

assert list_comp[:5] == first_five == [0, 2, 4, 6, 8]
assert gen_mem < 250  # Generator object is typically ~100-200 bytes regardless of N
assert list_mem > 800_000

# Explanation: Use list comprehensions when you need indexing, length, multiple
# iterations, or full persistence. Use generator expressions for streaming, large data,
# or when passing directly into reducers like sum(), min(), max(), any(), all().


# ============================================================
# Q10: Real-World Log Parsing & Metric Pipeline
# ============================================================
# Question: Build an analytical log processing pipeline using composable comprehensions.
# Parse raw web server log lines, extract HTTP status codes and response times,
# filter 4xx/5xx errors, and compute latency statistics.

print("\n=== Q10: Real-World Log Processing Pipeline ===")

raw_log_stream = [
    '2026-10-17 10:00:01 INFO [GET /api/v1/users] status=200 duration=45ms',
    '2026-10-17 10:00:02 WARN [POST /api/v1/auth] status=401 duration=120ms',
    '2026-10-17 10:00:03 INFO [GET /api/v1/products] status=200 duration=35ms',
    '2026-10-17 10:00:04 ERROR [POST /api/v1/checkout] status=500 duration=850ms',
    '2026-10-17 10:00:05 INFO [GET /api/v1/orders] status=200 duration=60ms',
    '2026-10-17 10:00:06 ERROR [GET /api/v1/orders/999] status=404 duration=18ms',
    'INVALID_GARBAGE_LOG_LINE_IGNORED'
]

# Step 1: Structured parse via dict comprehension & filtering
parsed_logs = [
    {
        "timestamp": f"{parts[0]} {parts[1]}",
        "level": parts[2],
        "method": parts[3].strip("[]"),
        "endpoint": parts[4].strip("[]"),
        "status": int(parts[5].split("=")[1]),
        "latency_ms": int(parts[6].split("=")[1].replace("ms", ""))
    }
    for line in raw_log_stream
    if len(parts := line.split()) >= 7 and parts[5].startswith("status=")
]

# Step 2: Extract error logs (status >= 400)
error_logs = [entry for entry in parsed_logs if entry["status"] >= 400]

# Step 3: Fast status code frequency map via dict comprehension
all_statuses = [entry["status"] for entry in parsed_logs]
status_counts = {code: all_statuses.count(code) for code in set(all_statuses)}

# Step 4: Compute latency statistics using generator expressions inside aggregators
durations = [entry["latency_ms"] for entry in parsed_logs]
avg_latency = sum(durations) / len(durations)
max_latency = max(durations)

print(f"  Parsed records count: {len(parsed_logs)}")
print(f"  Error incidents detected: {len(error_logs)}")
print(f"  Status code distribution: {status_counts}")
print(f"  Average latency: {avg_latency:.2f} ms (Max: {max_latency} ms)")

assert len(parsed_logs) == 6
assert len(error_logs) == 3  # 401, 500, 404
assert status_counts[200] == 3
assert status_counts[500] == 1
assert max_latency == 850

print("\nAll 10 list comprehension questions executed and asserted successfully!")
