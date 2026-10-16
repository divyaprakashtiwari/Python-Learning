"""
Topic 03: Data Structures
Question 05: Dictionary Basics (Deep Dive)

Master Python dictionaries: key-value mechanics, valid hashable keys,
KeyError avoidance, view objects (.keys, .values, .items), dictionary merge
operators (| and |=), O(1) membership speed, key-value inversion,
frequency counting, copy semantics, and an in-memory session cache.
"""

import copy
import time
from typing import Any

# ============================================================
# Q1: Dictionary Creation and Valid Key Types
# ============================================================
# Question: Demonstrate multiple ways to construct dictionaries: literals, dict(),
# from pairs, and dict.fromkeys(). Show which data types can serve as keys.

print("=== Q1: Dictionary Construction & Key Types ===")

# Construction methods
dict_literal = {"name": "Alice", "role": "Architect"}
dict_constructor = dict(name="Bob", role="Developer")
dict_from_pairs = dict([("name", "Charlie"), ("role", "Designer")])
dict_fromkeys = dict.fromkeys(["id", "created_at", "updated_at"], None)

print(f"  1. Literal:         {dict_literal}")
print(f"  2. dict(kwarg=val): {dict_constructor}")
print(f"  3. From pairs:      {dict_from_pairs}")
print(f"  4. dict.fromkeys(): {dict_fromkeys}")

# Valid key types (must be immutable and hashable)
complex_keys = {
    "string_key": 1,
    42: "integer_key",
    3.1415: "float_key",
    (10, 20): "tuple_coordinate_key",
    frozenset([1, 2]): "frozenset_key",
    True: "boolean_key (Note: True == 1 hash collision!)"
}
print(f"  Diverse hashable keys count: {len(complex_keys)}")

# Invalid key type: list or dict
try:
    bad_dict = {[1, 2]: "Invalid list key"}  # type: ignore
except TypeError as e:
    print(f"  Caught expected unhashable key error: {e}")

# Explanation: Dictionary keys must be hashable. Numeric keys 1 and True collide
# because `hash(1) == hash(True) == 1` and `1 == True`.


# ============================================================
# Q2: Key Access, KeyError Handling, and Safe Retrieval
# ============================================================
# Question: Demonstrate accessing keys via subscripting `d[k]`, catching `KeyError`,
# checking membership with `in`, and using safe default retrieval.

print("\n=== Q2: Key Access and KeyError Handling ===")

config = {"host": "localhost", "port": 8080, "debug": True}

# Direct subscript access
print(f"  config['host']: {config['host']}")

# Missing key causes KeyError
try:
    print(config["timeout"])
except KeyError as e:
    print(f"  Accessing missing key raised KeyError: {e}")

# Pattern 1: Membership check with 'in'
if "timeout" in config:
    timeout_val = config["timeout"]
else:
    timeout_val = 30  # Default fallback
print(f"  Pattern 1 ('in' check): timeout = {timeout_val}")

# Adding new key-value pair and modifying existing
config["timeout"] = 45   # Added
config["debug"] = False  # Modified
print(f"  Updated config: {config}")

# Explanation: Subscript access `d[k]` is $O(1)$ average time complexity.
# Testing `k in d` also takes $O(1)$ and never raises an exception.


# ============================================================
# Q3: Dynamic Dictionary Views (.keys(), .values(), .items())
# ============================================================
# Question: Demonstrate dictionary view objects. Prove that views are dynamic
# and automatically reflect subsequent mutations of the underlying dictionary.

print("\n=== Q3: Dynamic Dictionary Views ===")

inventory = {"laptop": 15, "monitor": 25, "keyboard": 40}

# Capture view objects
keys_view = inventory.keys()
values_view = inventory.values()
items_view = inventory.items()

print(f"  Initial keys view:   {list(keys_view)}")
print(f"  Initial values view: {list(values_view)}")

# Mutate inventory: add new item and modify existing
inventory["mouse"] = 50
inventory["laptop"] = 12

# The previously captured view objects reflect these mutations AUTOMATICALLY!
print("\n  After mutating dictionary:")
print(f"    keys_view automatically updated:   {list(keys_view)}")
print(f"    values_view automatically updated: {list(values_view)}")
print(f"    items_view count:                  {len(items_view)}")

# Dictionary views support set operations (keys and items)
other_catalog = {"monitor": 30, "desk": 10}
shared_keys = keys_view & other_catalog.keys()  # Set intersection on dict views!
print(f"    Shared keys between catalogs:      {shared_keys}")

# Explanation: In Python 3, `.keys()`, `.values()`, and `.items()` return view objects
# that maintain a live window to the underlying table without copying data.


# ============================================================
# Q4: Dictionary Merging (PEP 448 Unpacking & PEP 584 Operators)
# ============================================================
# Question: Merge dictionaries using three modern techniques:
# 1. Double splat `**d1, **d2`
# 2. Merge operator `d1 | d2` (Python 3.9+)
# 3. In-place merge operator `d1 |= d2`
# Show that rightmost values win on key collisions.

print("\n=== Q4: Dictionary Merging and Precedence ===")

default_settings = {"theme": "light", "font_size": 14, "auto_save": True, "timeout": 30}
user_preferences = {"theme": "dark", "font_size": 16, "show_line_numbers": True}

# Method 1: Double-splat unpacking {**d1, **d2}
merged_splat = {**default_settings, **user_preferences}
print(f"  Method 1 (**):   {merged_splat}")

# Method 2: Python 3.9+ Merge operator |
merged_pipe = default_settings | user_preferences
print(f"  Method 2 (|):    {merged_pipe}")

# Verify collision resolution: right operand overrides left operand
print(f"  theme resolved to: '{merged_pipe['theme']}' (user preference won over default)")

# Method 3: In-place update operator |=
working_copy = default_settings.copy()
working_copy |= user_preferences
print(f"  Method 3 (|=):   {working_copy}")

# Explanation: The union operator `|` creates a new dictionary combining both operands.
# When duplicate keys exist, the value from the right-hand operand takes precedence.


# ============================================================
# Q5: O(1) Membership Testing vs O(N) List Lookups
# ============================================================
# Question: Demonstrate the dramatic speed advantage of dictionary key lookups (O(1))
# versus list scans (O(N)) using a large collection.

print("\n=== Q5: O(1) vs O(N) Lookup Benchmark ===")

DATA_SIZE = 100_000
test_keys_list = [f"key_{i}" for i in range(DATA_SIZE)]
test_dict = {k: i for i, k in enumerate(test_keys_list)}

target_needle = f"key_{DATA_SIZE - 1}"  # Last item (worst case for linear scan)

# Time list lookup O(N)
t0 = time.perf_counter()
found_in_list = target_needle in test_keys_list
t_list = time.perf_counter() - t0

# Time dict lookup O(1)
t0 = time.perf_counter()
found_in_dict = target_needle in test_dict
t_dict = time.perf_counter() - t0

print(f"  Target: '{target_needle}' in {DATA_SIZE:,} elements")
print(f"  List lookup (O(N)): {t_list * 1000:>8.4f} ms")
print(f"  Dict lookup (O(1)): {t_dict * 1000:>8.4f} ms")
speedup = t_list / t_dict if t_dict > 0 else float('inf')
print(f"  Speedup factor:     ~{speedup:,.0f}x faster with dict")

# Explanation: Lists require iterating up to $N$ elements sequentially ($O(N)$).
# Dictionaries use hash tables to locate the slot in average $O(1)$ constant time.


# ============================================================
# Q6: Inverting / Swapping Keys and Values
# ============================================================
# Question: Invert a dictionary (swap keys and values):
# 1. For one-to-one mapping.
# 2. For one-to-many mapping where duplicate values collect keys into a list.

print("\n=== Q6: Inverting Keys and Values ===")

# One-to-one inversion
country_capitals = {"France": "Paris", "Japan": "Tokyo", "Italy": "Rome"}
capital_to_country = {v: k for k, v in country_capitals.items()}
print(f"  Original: {country_capitals}")
print(f"  Inverted: {capital_to_country}")

# One-to-many inversion (grouping keys by value)
department_roster = {
    "Alice": "Engineering",
    "Bob": "Design",
    "Charlie": "Engineering",
    "David": "Marketing",
    "Eve": "Engineering",
}

dept_to_employees = {}
for emp, dept in department_roster.items():
    if dept not in dept_to_employees:
        dept_to_employees[dept] = []
    dept_to_employees[dept].append(emp)

print("\n  Grouped Employees by Department:")
for dept, emps in dept_to_employees.items():
    print(f"    {dept:<12}: {emps}")

# Explanation: When inverting dictionaries with non-unique values, values must be mapped
# to lists or sets of keys to avoid silently overwriting previous associations.


# ============================================================
# Q7: Frequency Counter Algorithm
# ============================================================
# Question: Build a frequency counting function using standard dictionary accumulation
# (without importing collections.Counter) to analyze word occurrences in a text string.

print("\n=== Q7: Word Frequency Accumulation ===")

def count_word_frequencies(text: str) -> dict[str, int]:
    """Tallies word occurrences using dictionary accumulation."""
    clean_words = "".join(c.lower() if c.isalnum() or c.isspace() else " " for c in text).split()
    counts = {}
    
    for word in clean_words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
            
    return counts

passage = "To be or not to be that is the question whether tis nobler in the mind to suffer"
freq_map = count_word_frequencies(passage)

# Sort words by frequency descending
sorted_by_freq = sorted(freq_map.items(), key=lambda pair: pair[1], reverse=True)
print(f"  Top 5 most frequent words:")
for word, cnt in sorted_by_freq[:5]:
    print(f"    '{word}': {cnt} times")

# Explanation: Dictionary frequency accumulation `if word in counts: counts[word] += 1`
# runs in $O(N)$ time and forms the basis of NLP tokenization and analytics.


# ============================================================
# Q8: Shallow vs Deep Copy in Nested Dictionaries
# ============================================================
# Question: Prove why `d.copy()` is insufficient for nested dictionaries
# and demonstrate when `copy.deepcopy()` is mandatory.

print("\n=== Q8: Shallow vs Deep Copy in Dictionaries ===")

app_config = {
    "app_name": "Portal",
    "database": {"host": "10.0.0.1", "port": 5432},
    "features": ["auth", "billing"]
}

# Shallow copy via .copy()
shallow_cfg = app_config.copy()
# Deep copy via copy.deepcopy()
deep_cfg = copy.deepcopy(app_config)

# Mutate top-level field (safe in shallow copy)
app_config["app_name"] = "Portal-V2"

# Mutate nested dictionary and nested list (corrupts shallow copy!)
app_config["database"]["port"] = 9999
app_config["features"].append("analytics")

print("  After mutating original's nested configuration:")
print(f"    Original:     {app_config}")
print(f"    Shallow copy: {shallow_cfg}  <- NESTED VALUES MUTATED!")
print(f"    Deep copy:    {deep_cfg}  <- UNTOUCHED & SAFE")

# Explanation: `dict.copy()` creates a new outer dictionary, but nested inner dicts
# and lists are shared by reference. Use `copy.deepcopy()` for nested structures.


# ============================================================
# Q9: Dictionary Filtering and Value Transformations
# ============================================================
# Question: Filter a product catalog dictionary to keep only items currently in stock,
# and apply a 15% discount to all remaining prices.

print("\n=== Q9: Dictionary Filtering & Transformations ===")

catalog = {
    "Laptop":      {"price": 1200.0, "stock": 5},
    "Monitor":     {"price": 300.0,  "stock": 0},  # Out of stock
    "Mechanical KB": {"price": 150.0,  "stock": 12},
    "Mousepad":    {"price": 20.0,   "stock": 0},  # Out of stock
    "USB-C Hub":   {"price": 45.0,   "stock": 8},
}

# Filter out-of-stock items and apply 15% discount in a dictionary comprehension
discounted_in_stock = {
    item: {
        "original_price": data["price"],
        "sale_price": round(data["price"] * 0.85, 2),
        "stock": data["stock"]
    }
    for item, data in catalog.items()
    if data["stock"] > 0
}

print(f"  Filtered & Discounted Catalog ({len(discounted_in_stock)} items in stock):")
for item, info in discounted_in_stock.items():
    print(f"    {item:<14} -> Orig: ${info['original_price']:<7.2f} | Sale: ${info['sale_price']:<7.2f} (Stock: {info['stock']})")

# Explanation: Dictionary comprehensions `{k: transform(v) for k, v in d.items() if condition}`
# provide declarative, expressive filtering and mapping in a single statement.


# ============================================================
# Q10: In-Memory Session Cache with TTL Expiry
# ============================================================
# Question: Build an in-memory session management store using dictionaries:
# create session, validate token, touch/extend last active time, check expiration (TTL),
# and purge expired sessions.

print("\n=== Q10: In-Memory Session Cache with TTL ===")

class SessionStore:
    def __init__(self, default_ttl_seconds: int = 1800):
        self._sessions: dict[str, dict] = {}
        self.default_ttl = default_ttl_seconds

    def create_session(self, token: str, user_id: str, role: str) -> dict:
        """Stores a new session record."""
        now = time.time()
        record = {
            "token": token,
            "user_id": user_id,
            "role": role,
            "created_at": now,
            "last_active": now,
            "ttl": self.default_ttl
        }
        self._sessions[token] = record
        return record

    def get_session(self, token: str) -> dict | None:
        """Retrieves session if valid and not expired; touches last_active."""
        if token not in self._sessions:
            return None
            
        record = self._sessions[token]
        now = time.time()
        # Check expiry
        if now - record["last_active"] > record["ttl"]:
            del self._sessions[token]  # Invalidate expired session
            return None
            
        # Extend activity timestamp
        record["last_active"] = now
        return record

    def purge_expired(self) -> int:
        """Purges all expired sessions from cache."""
        now = time.time()
        expired_tokens = [
            t for t, rec in self._sessions.items()
            if now - rec["last_active"] > rec["ttl"]
        ]
        for t in expired_tokens:
            del self._sessions[t]
        return len(expired_tokens)

    def active_count(self) -> int:
        return len(self._sessions)

# Test session store
store = SessionStore(default_ttl_seconds=10)
store.create_session("tok_101", "user_alice", "admin")
store.create_session("tok_102", "user_bob", "member")

print(f"  Active sessions created: {store.active_count()}")
sess = store.get_session("tok_101")
print(f"  Retrieved session 'tok_101': User={sess['user_id']}, Role={sess['role']}")

# Simulate immediate expiration on a dummy session
store._sessions["tok_102"]["last_active"] -= 20  # Fast-forward 20 seconds into past
expired_sess = store.get_session("tok_102")
print(f"  Retrieved expired session 'tok_102': {expired_sess} (Auto-invalidated!)")
print(f"  Remaining active sessions: {store.active_count()}")

# Summary Output
print("\n" + "=" * 55)
print("  All 10 Questions for Topic 03 - Q05 executed successfully!")
print("=" * 55)
