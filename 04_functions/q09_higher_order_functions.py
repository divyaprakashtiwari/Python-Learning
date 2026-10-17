"""
Topic 04: Functions
Question 09: Higher-Order Functions: map, filter, reduce (Deep Dive)

Master functional programming primitives in Python:
- Multi-iterable parallel processing with map(fn, iter1, iter2)
- filter() mechanics and the filter(None, iterable) truthiness idiom
- functools.reduce() folding semantics, accumulators, and initializers
- Performance benchmark: map() with C-functions vs list comprehensions
- Advanced reductions: deep dictionary merging and group-by aggregations
- Function currying with higher-order functions (curry(f)(a)(b)(c))
- Fluent pipeline composition (pipe(*functions))
- Predicate combinators (all_of, any_of, complement)
- Higher-order memoization decorator with custom key serialization
- Real-world streaming ETL pipeline using composable higher-order transforms
"""

import functools
import operator
import time
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple


# ============================================================
# Q1: Multi-Iterable Parallel Mapping with map()
# ============================================================
# Question: Demonstrate that `map(fn, iter1, iter2, ...)` can accept multiple iterables
# simultaneously. Implement parallel vector arithmetic, and verify it terminates when
# the shortest iterable is exhausted.

print("=== Q1: Multi-Iterable Parallel map() ===")

vec_x = [1.0, 2.5, 4.0, 10.0]
vec_y = [3.0, 1.5, 2.0]  # Length 3 (shorter)
weights = [0.5, 0.5, 1.0, 2.0]

# Compute weighted combination: x * weight + y
def weighted_add(x: float, y: float, w: float) -> float:
    return round((x * w) + y, 2)

# map() lazily consumes all three iterables in lockstep!
mapped_iter = map(weighted_add, vec_x, vec_y, weights)

# Verify lazy evaluation (it's a map iterator, not a list)
assert iter(mapped_iter) is mapped_iter
mapped_results = list(mapped_iter)

print(f"  Vector X:       {vec_x}")
print(f"  Vector Y:       {vec_y} (length 3)")
print(f"  Mapped Results: {mapped_results}")

# Stops at length 3 because vec_y has only 3 elements
assert len(mapped_results) == 3
# Calculation checks: (1.0*0.5)+3.0=3.5, (2.5*0.5)+1.5=2.75, (4.0*1.0)+2.0=6.0
assert mapped_results == [3.5, 2.75, 6.0]

# Explanation: `map()` passes items at index `i` from each iterable to `fn(*args)`.
# Execution stops as soon as the shortest input iterable is exhausted.


# ============================================================
# Q2: filter() Mechanics & The Truthiness Idiom (filter(None, seq))
# ============================================================
# Question: Demonstrate filtering with custom predicates, and showcase the `filter(None, sequence)`
# idiom that removes all falsy values (0, False, empty strings, None) in C-speed.

print("\n=== Q2: filter() and filter(None, seq) Truthiness Idiom ===")

dirty_data = ["Alice", "", None, "Bob", 0, "Charlie", False, [], "Diana", {}]

# 1. filter(None, iterable) strips all falsy elements without writing a lambda!
cleaned_truthy = list(filter(None, dirty_data))
print(f"  filter(None, data) truthy extraction: {cleaned_truthy}")
assert cleaned_truthy == ["Alice", "Bob", "Charlie", "Diana"]

# 2. Custom predicate filter
def is_long_name(name: str) -> bool:
    return len(name) > 4

long_names = list(filter(is_long_name, cleaned_truthy))
print(f"  Names longer than 4 chars:            {long_names}")
assert long_names == ["Alice", "Charlie", "Diana"]

# Explanation: Passing `None` as the first argument to `filter()` tests each element
# for boolean truthiness (`bool(x)`), efficiently purging blanks, zeroes, and empty collections.


# ============================================================
# Q3: functools.reduce() Folding Semantics & Initializers
# ============================================================
# Question: Demonstrate `functools.reduce()`. Explain how the accumulator progresses
# through a sequence, why an explicit initializer is vital for empty collections,
# and what error occurs if an empty collection has no initializer.

print("\n=== Q3: functools.reduce() Folding Semantics ===")

numbers = [1, 2, 3, 4, 5]

# Step trace accumulator
def traced_multiply(acc: int, x: int) -> int:
    return acc * x

# Product without initializer: acc starts with numbers[0], x starts with numbers[1]
factorial_5 = functools.reduce(traced_multiply, numbers)
print(f"  Product of 1..5: {factorial_5}")
assert factorial_5 == 120

# With explicit initializer: acc starts with 100
total_with_base = functools.reduce(operator.add, numbers, 100)
print(f"  Sum with base initializer 100: {total_with_base}")
assert total_with_base == 115

# Empty sequence with initializer returns initializer safely
empty_safe = functools.reduce(operator.add, [], 0)
assert empty_safe == 0

# Empty sequence WITHOUT initializer raises TypeError!
caught_empty_error = False
try:
    functools.reduce(operator.add, [])
except TypeError as err:
    caught_empty_error = True
    print(f"  Caught expected empty reduce error: {err}")
assert caught_empty_error

# Explanation: `reduce(fn, iterable, [initial])` folds items from left to right.
# Providing an initializer guarantees a well-defined return value even if the iterable is empty.


# ============================================================
# Q4: Benchmark: map() with Built-in C-Func vs Comprehensions
# ============================================================
# Question: Empirically compare execution speed between `map(str.upper, words)`
# and `[w.upper() for w in words]` for a large dataset.

print("\n=== Q4: Performance Benchmark: map() vs Comprehension ===")

WORD_COUNT = 100_000
raw_words = ["python_learning_repo_test_string"] * WORD_COUNT

# 1. Using map() with bound C-level method str.upper
t0 = time.perf_counter()
mapped_list = list(map(str.upper, raw_words))
t_map = time.perf_counter() - t0

# 2. Using list comprehension
t0 = time.perf_counter()
comp_list = [w.upper() for w in raw_words]
t_comp = time.perf_counter() - t0

print(f"  map(str.upper, words) time:    {t_map * 1000:.3f} ms")
print(f"  [w.upper() for w in words]:    {t_comp * 1000:.3f} ms")

assert mapped_list == comp_list

# Explanation: When applying an existing C-level built-in function (e.g. str.upper, int, abs),
# `map()` is often faster because loop iteration occurs in C without bytecode evaluation.
# When a lambda is needed, comprehensions are usually faster.


# ============================================================
# Q5: Advanced Reductions: Deep Dictionary Merging & Aggregation
# ============================================================
# Question: Use `functools.reduce()` to combine a stream of partial metric updates
# into a single aggregated report without mutation.

print("\n=== Q5: Advanced Reduction (Consolidated Metrics) ===")

daily_metrics = [
    {"views": 1200, "clicks": 80,  "conversions": 12},
    {"views": 1500, "clicks": 110, "conversions": 15},
    {"views": 900,  "clicks": 65,  "conversions": 8},
    {"views": 2100, "clicks": 140, "conversions": 25},
]

def merge_metrics(acc: Dict[str, int], current: Dict[str, int]) -> Dict[str, int]:
    return {
        key: acc.get(key, 0) + current.get(key, 0)
        for key in set(acc.keys()) | set(current.keys())
    }

total_report = functools.reduce(merge_metrics, daily_metrics, {})
print(f"  Aggregated report via reduce: {total_report}")

assert total_report["views"] == 5700
assert total_report["clicks"] == 395
assert total_report["conversions"] == 60

# Explanation: `reduce()` models folding sequences of objects into a single cumulative summary,
# the foundation of MapReduce distributed computing paradigms.


# ============================================================
# Q6: Function Currying with Higher-Order Functions
# ============================================================
# Question: Implement a generic `curry()` higher-order function that converts an N-argument
# function into a chain of single-argument functions: `curry(f)(a)(b)(c)`.

print("\n=== Q6: Function Currying ===")

import inspect

def curry(func: Callable[..., Any]) -> Callable[..., Any]:
    """Recursively curries a function until all required parameters are supplied."""
    sig = inspect.signature(func)
    total_args = len(sig.parameters)

    def _curried(*args: Any) -> Any:
        if len(args) >= total_args:
            return func(*args)
        return lambda *more_args: _curried(*(args + more_args))

    return _curried

def volume(length: float, width: float, height: float) -> float:
    return length * width * height

curried_volume = curry(volume)

# Call one argument at a time
v1 = curried_volume(2.0)(3.0)(4.0)
# Call partially
box_with_fixed_base = curried_volume(5.0, 4.0)  # Waiting for height
v2 = box_with_fixed_base(2.0)
v3 = box_with_fixed_base(10.0)

print(f"  curried_volume(2)(3)(4) = {v1}")
print(f"  box_with_fixed_base(2)  = {v2}")
print(f"  box_with_fixed_base(10) = {v3}")

assert v1 == 24.0
assert v2 == 40.0
assert v3 == 200.0

# Explanation: Currying breaks down multi-argument functions into unary pipelines,
# enabling partial specialization and composition in functional code.


# ============================================================
# Q7: Fluent Pipeline Composition with pipe()
# ============================================================
# Question: Implement a `pipe(*functions)` higher-order function using `reduce()`
# that feeds data through an arbitrary series of transforming functions.

print("\n=== Q7: Pipeline Composition with pipe() ===")

def pipe(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Composes functions left-to-right: pipe(f, g, h)(x) == h(g(f(x)))."""
    def _pipeline(initial_value: Any) -> Any:
        return functools.reduce(lambda val, fn: fn(val), functions, initial_value)
    return _pipeline

# Build pipeline stages
sanitize_text = lambda s: s.strip()
remove_dashes = lambda s: s.replace("-", " ")
capitalize_words = lambda s: s.title()
prefix_ticket = lambda s: f"[TICKET] {s}"

ticket_pipeline = pipe(sanitize_text, remove_dashes, capitalize_words, prefix_ticket)

raw_input_str = "   database-connection-timeout-error   "
formatted_ticket = ticket_pipeline(raw_input_str)

print(f"  Raw:       '{raw_input_str}'")
print(f"  Formatted: '{formatted_ticket}'")

assert formatted_ticket == "[TICKET] Database Connection Timeout Error"

# Explanation: `pipe()` chains transformations cleanly from left-to-right,
# replacing hard-to-read nested calls `f(g(h(x)))` with linear data flow.


# ============================================================
# Q8: Predicate Combinators (all_of, any_of, complement)
# ============================================================
# Question: Implement higher-order predicate combinators `all_of(*predicates)` and
# `any_of(*predicates)` that combine multiple validation rules into a single test function.

print("\n=== Q8: Predicate Combinators ===")

def all_of(*predicates: Callable[[Any], bool]) -> Callable[[Any], bool]:
    """Returns True if and only if ALL predicates return True."""
    return lambda item: all(p(item) for p in predicates)

def any_of(*predicates: Callable[[Any], bool]) -> Callable[[Any], bool]:
    """Returns True if AT LEAST ONE predicate returns True."""
    return lambda item: any(p(item) for p in predicates)

def complement(predicate: Callable[[Any], bool]) -> Callable[[Any], bool]:
    """Negates a predicate."""
    return lambda item: not predicate(item)

# Predicates for password validation
has_min_len = lambda pwd: len(pwd) >= 8
has_uppercase = lambda pwd: any(c.isupper() for c in pwd)
has_digit = lambda pwd: any(c.isdigit() for c in pwd)
has_symbol = lambda pwd: any(c in "!@#$%^&*" for c in pwd)

is_strong_password = all_of(has_min_len, has_uppercase, has_digit, has_symbol)

p1 = is_strong_password("Pass123!")  # Valid: len >= 8, upper, digit, symbol
p2 = is_strong_password("weak")      # Invalid: too short, no upper, no digit, no symbol
p3 = is_strong_password("Password!") # Invalid: no digit

print(f"  'Pass123!' is strong:  {p1}")
print(f"  'weak' is strong:      {p2}")
print(f"  'Password!' is strong: {p3}")

assert p1 is True
assert p2 is False
assert p3 is False

# Explanation: Combinator functions combine atomic validation predicates into
# complex rule engines without nested conditional boilerplate.


# ============================================================
# Q9: Higher-Order Memoizer with Custom Key Serializer
# ============================================================
# Question: Implement a memoization decorator that accepts unhashable arguments (e.g. dicts, lists)
# by using a customizable key serialization function (e.g. converting dicts to sorted tuples).

print("\n=== Q9: Higher-Order Memoizer for Unhashable Types ===")

def smart_cache(key_builder: Callable[..., Any]):
    """Decorator factory creating a cache parameterized by a custom key serializer."""
    def decorator(func: Callable[..., Any]):
        cache: Dict[Any, Any] = {}

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            cache_key = key_builder(*args, **kwargs)
            if cache_key in cache:
                return cache[cache_key]
            result = func(*args, **kwargs)
            cache[cache_key] = result
            return result
        return wrapper
    return decorator

# Custom key serializer converting unhashable dict into frozen sorted tuple
def freeze_value(val: Any) -> Any:
    if isinstance(val, dict):
        return tuple(sorted((k, freeze_value(v)) for k, v in val.items()))
    elif isinstance(val, (list, tuple)):
        return tuple(freeze_value(x) for x in val)
    return val

def dict_payload_serializer(payload: Dict[str, Any]) -> Tuple[Tuple[str, Any], ...]:
    return tuple(sorted((k, freeze_value(v)) for k, v in payload.items()))

eval_count = 0

@smart_cache(dict_payload_serializer)
def analyze_payload(data: Dict[str, Any]) -> str:
    global eval_count
    eval_count += 1
    return f"ANALYSIS_FOR_{data.get('category', 'UNKNOWN')}_HASH_{sum(data.get('values', []))}"

# Test calls with identical dict content (unhashable by standard hash())
dict1 = {"category": "FINANCE", "values": [10, 20]}
dict2 = {"values": [10, 20], "category": "FINANCE"}  # Different key order, identical content

res_a = analyze_payload(dict1)
res_b = analyze_payload(dict2)

print(f"  Result A: {res_a}")
print(f"  Total function evaluations: {eval_count} (Second call hit cache!)")

assert res_a == res_b
assert eval_count == 1

# Explanation: By abstracting cache key generation into a higher-order function,
# we can cache complex domain structures like queries, lists, and JSON payloads.


# ============================================================
# Q10: Production-Grade Composable ETL Stream Pipeline
# ============================================================
# Question: Implement a complete data processing pipeline using map, filter, and reduce
# that cleans raw transaction events, enriches them with sales tax, filters invalid transactions,
# and computes the final fiscal revenue breakdown.

print("\n=== Q10: Composable ETL Stream Pipeline ===")

raw_transactions = [
    {"id": "T1", "amount": 100.0, "status": "COMPLETED", "region": "US-CA"},
    {"id": "T2", "amount": -50.0, "status": "COMPLETED", "region": "US-NY"},  # Invalid amount
    {"id": "T3", "amount": 250.0, "status": "PENDING",   "region": "US-CA"},  # Not completed
    {"id": "T4", "amount": 400.0, "status": "COMPLETED", "region": "US-NY"},
    {"id": "T5", "amount": 150.0, "status": "COMPLETED", "region": "US-TX"},
]

REGIONAL_TAX_RATES = {"US-CA": 0.08, "US-NY": 0.085, "US-TX": 0.0625}

# Step 1: Filter only valid completed transactions
is_valid_completed = lambda t: t.get("status") == "COMPLETED" and t.get("amount", 0) > 0
valid_stream = filter(is_valid_completed, raw_transactions)

# Step 2: Map enrichment: compute tax and gross total
def enrich_transaction(tx: Dict[str, Any]) -> Dict[str, Any]:
    rate = REGIONAL_TAX_RATES.get(tx["region"], 0.05)
    tax = round(tx["amount"] * rate, 2)
    return {
        "id": tx["id"],
        "region": tx["region"],
        "net": tx["amount"],
        "tax": tax,
        "gross": round(tx["amount"] + tax, 2)
    }

enriched_stream = map(enrich_transaction, valid_stream)

# Step 3: Reduce aggregation: fold stream into final fiscal summary
def revenue_reducer(acc: Dict[str, float], tx: Dict[str, Any]) -> Dict[str, float]:
    acc["total_net"] = round(acc["total_net"] + tx["net"], 2)
    acc["total_tax"] = round(acc["total_tax"] + tx["tax"], 2)
    acc["total_gross"] = round(acc["total_gross"] + tx["gross"], 2)
    acc["transaction_count"] = acc["transaction_count"] + 1
    return acc

initial_ledger = {"total_net": 0.0, "total_tax": 0.0, "total_gross": 0.0, "transaction_count": 0}
final_ledger = functools.reduce(revenue_reducer, enriched_stream, initial_ledger)

print(f"  Processed Transactions: {int(final_ledger['transaction_count'])}")
print(f"  Total Net Revenue:     ${final_ledger['total_net']:.2f}")
print(f"  Total Tax Collected:   ${final_ledger['total_tax']:.2f}")
print(f"  Total Gross Inflow:    ${final_ledger['total_gross']:.2f}")

# Valid txs: T1 ($100), T4 ($400), T5 ($150) -> Total net = $650.00
# Tax: T1 (100*0.08=8), T4 (400*0.085=34), T5 (150*0.0625=9.38) -> Total tax = $51.38
# Gross: $701.38
assert final_ledger["transaction_count"] == 3
assert final_ledger["total_net"] == 650.0
assert final_ledger["total_tax"] == 51.38
assert final_ledger["total_gross"] == 701.38

print("\nAll 10 higher-order functions questions executed and asserted successfully!")
