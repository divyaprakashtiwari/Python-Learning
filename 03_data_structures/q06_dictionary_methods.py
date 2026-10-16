"""
Topic 03: Data Structures
Question 06: Dictionary Methods (Deep Dive)

Master Python dictionary methods: .get() nuances, .setdefault(), .pop() vs .popitem(),
.update() signatures, collections.defaultdict, OrderedDict (with .move_to_end),
ChainMap for multi-layer config, recursive deep dict merge, schema diff comparator,
and an LRU cache implementation.
"""

import copy
from collections import defaultdict, OrderedDict, ChainMap
from typing import Any

# ============================================================
# Q1: .get() Nuance: Missing Key vs None Value
# ============================================================
# Question: Demonstrate the difference between a key that does not exist versus
# a key that explicitly holds the value None. Show how `.get()` can mislead if not careful.

print("=== Q1: .get() with Defaults vs None Values ===")

user_settings = {
    "theme": "dark",
    "nickname": None,      # Explicitly set to None
    "notifications": False
}

# Looking up a missing key with default fallback
missing_font = user_settings.get("font_family", "Consolas")
print(f"  Missing key 'font_family' -> .get() returned fallback: '{missing_font}'")

# THE PITFALL: 'nickname' exists, but its value is None!
nickname_val = user_settings.get("nickname", "Anonymous")
print(f"  Existing key with None 'nickname' -> .get() returned: {nickname_val} (Fallback was IGNORED!)")

# Correct disambiguation pattern: check membership first or use sentinel
SENTINEL = object()
def get_explicit(d: dict, key: str, default: Any = None) -> Any:
    val = d.get(key, SENTINEL)
    if val is SENTINEL or val is None:
        return default
    return val

print(f"  Disambiguated helper on 'nickname': '{get_explicit(user_settings, 'nickname', 'Anonymous')}'")

# Explanation: `dict.get(key, default)` returns `default` ONLY when `key not in dict`.
# If `key in dict` and `dict[key]` is `None`, `.get()` returns `None`, NOT the default.


# ============================================================
# Q2: Grouping Elements with .setdefault()
# ============================================================
# Question: Use `.setdefault()` to group transactions by category without
# raising KeyError or checking membership manually.

print("\n=== Q2: Grouping with .setdefault() ===")

transactions = [
    {"category": "Food",    "amount": 25.50},
    {"category": "Utility", "amount": 120.00},
    {"category": "Food",    "amount": 15.00},
    {"category": "Travel",  "amount": 45.00},
    {"category": "Food",    "amount": 60.00},
]

grouped_spend = {}

for tx in transactions:
    cat = tx["category"]
    # .setdefault(k, []) retrieves existing list or initializes with [] and returns it
    grouped_spend.setdefault(cat, []).append(tx["amount"])

print(f"  Grouped spending lists:")
for cat, amounts in grouped_spend.items():
    print(f"    {cat:<10}: {amounts} (Total: ${sum(amounts):.2f})")

# Explanation: `d.setdefault(key, default)` checks if `key in d`. If not, sets `d[key] = default`.
# It always returns `d[key]`, enabling immediate in-place mutation like `.append()`.


# ============================================================
# Q3: .pop() vs .popitem() (LIFO Removal)
# ============================================================
# Question: Demonstrate removing items by key using `.pop()`, and removing
# the most recently inserted item using `.popitem()` (LIFO order).

print("\n=== Q3: .pop() vs .popitem() ===")

cache = {"req_1": "data_1", "req_2": "data_2", "req_3": "data_3", "req_4": "data_4"}

# .pop(key, default) removes by key
val = cache.pop("req_2", None)
print(f"  .pop('req_2') returned: '{val}', remaining: {cache}")

# .pop() with safe fallback when key is absent
missing_val = cache.pop("req_999", "NOT_FOUND")
print(f"  .pop('req_999', 'NOT_FOUND') returned: '{missing_val}'")

# .popitem() removes the LAST (LIFO) inserted key-value pair as a tuple
last_pair = cache.popitem()
print(f"  .popitem() removed LIFO pair: {last_pair}")
print(f"  Remaining cache: {cache}")

# Explanation: In Python 3.7+, dictionaries are insertion-ordered. `.popitem()` removes
# and returns the most recently inserted `(key, value)` pair in $O(1)$ time.


# ============================================================
# Q4: Flexible .update() Signatures
# ============================================================
# Question: Demonstrate the multiple input formats accepted by `.update()`:
# another dictionary, a list of (key, value) pairs, and keyword arguments simultaneously.

print("\n=== Q4: Flexible .update() Signatures ===")

profile = {"username": "coder", "level": 1}

# 1. Update from another dictionary
profile.update({"level": 2, "xp": 1500})
print(f"  After dict update:        {profile}")

# 2. Update from iterable of key-value tuples
profile.update([("badge", "gold"), ("rank", 42)])
print(f"  After tuple list update:  {profile}")

# 3. Update using keyword arguments
profile.update(status="ONLINE", rank=40)
print(f"  After kwargs update:      {profile}")

# 4. Simultaneous combination: pair list + kwargs
profile.update([("xp", 2000)], status="ACTIVE_IN_GAME", title="Master")
print(f"  After combined update:    {profile}")

# Explanation: `dict.update([other], **kwargs)` allows chaining multiple input streams
# directly into the dictionary in-place.


# ============================================================
# Q5: collections.defaultdict (Single and Nested)
# ============================================================
# Question: Implement auto-initializing counters, list accumulators, and a 2D
# nested dictionary using `collections.defaultdict`.

print("\n=== Q5: collections.defaultdict Deep Dive ===")

# 1. Counter factory: defaultdict(int) initializes missing keys with 0
hit_counter = defaultdict(int)
for page in ["/home", "/about", "/home", "/contact", "/home", "/about"]:
    hit_counter[page] += 1  # No KeyError! Missing keys start at 0
print(f"  Hit counter: {dict(hit_counter)}")

# 2. Set accumulator: defaultdict(set)
user_permissions = defaultdict(set)
user_permissions["alice"].add("read")
user_permissions["alice"].add("write")
user_permissions["bob"].add("read")
print(f"  User permissions: {dict(user_permissions)}")

# 3. 2D Nested defaultdict: matrix[row][col] auto-vivification
def nested_dict_factory():
    return defaultdict(int)

grid = defaultdict(nested_dict_factory)
grid["Server_A"]["CPU"] = 85
grid["Server_A"]["RAM"] = 62
grid["Server_B"]["CPU"] = 40
print(f"  Server A CPU: {grid['Server_A']['CPU']}%")
print(f"  Server B RAM: {grid['Server_B']['RAM']}% (Auto-initialized to 0)")

# Explanation: `defaultdict(factory)` calls `factory()` with zero arguments when a
# missing key is accessed, automatically populating the entry without manual boilerplates.


# ============================================================
# Q6: collections.OrderedDict and .move_to_end()
# ============================================================
# Question: Contrast standard dict with `collections.OrderedDict`.
# Demonstrate `.move_to_end(key, last=True/False)` and order-sensitive equality.

print("\n=== Q6: collections.OrderedDict Features ===")

# Standard dict is insertion-ordered, but OrderedDict provides explicit ordering controls
od = OrderedDict([("a", 1), ("b", 2), ("c", 3), ("d", 4)])
print(f"  Initial OrderedDict:       {list(od.keys())}")

# Move key 'b' to the very END (last=True is default)
od.move_to_end("b", last=True)
print(f"  After move_to_end('b'):    {list(od.keys())}")

# Move key 'c' to the FRONT (last=False)
od.move_to_end("c", last=False)
print(f"  After move_to_end('c', F): {list(od.keys())}")

# Order-sensitive equality check:
od1 = OrderedDict([("x", 1), ("y", 2)])
od2 = OrderedDict([("y", 2), ("x", 1)])
print(f"  OrderedDict equality check: {od1 == od2} (Different insertion orders -> False!)")

std1 = {"x": 1, "y": 2}
std2 = {"y": 2, "x": 1}
print(f"  Standard dict equality:    {std1 == std2} (Order is ignored for dict equality -> True)")

# Explanation: `OrderedDict` is essential when element order matters for equality,
# or when items must be rearranged in $O(1)$ time (e.g. priority queues, LRU caches).


# ============================================================
# Q7: collections.ChainMap for Hierarchical Scoped Configurations
# ============================================================
# Question: Implement a multi-layer configuration resolution system using `ChainMap`:
# CLI Arguments -> Environment Variables -> Config File -> System Defaults.

print("\n=== Q7: Scoped Configuration with ChainMap ===")

# 4 layers of configuration
system_defaults = {"host": "0.0.0.0", "port": 8080, "debug": False, "workers": 4}
config_file     = {"port": 5000, "workers": 8, "log_level": "INFO"}
env_variables   = {"port": 3000, "debug": True}
cli_arguments   = {"workers": 16}  # Top priority override

# ChainMap searches maps from left to right!
app_config = ChainMap(cli_arguments, env_variables, config_file, system_defaults)

print("  Resolved Configuration Hierarchy:")
print(f"    workers:   {app_config['workers']}   (From CLI override: 16)")
print(f"    port:      {app_config['port']}      (From Env variable: 3000)")
print(f"    debug:     {app_config['debug']}     (From Env variable: True)")
print(f"    log_level: {app_config['log_level']} (From Config file: INFO)")
print(f"    host:      {app_config['host']}   (From System defaults: 0.0.0.0)")

# Mutations on ChainMap affect ONLY the first mapping (cli_arguments)
app_config["new_param"] = "test_val"
print(f"  First layer (CLI) received mutation: {cli_arguments}")

# Explanation: `ChainMap` groups multiple dicts into a single updateable view without
# physically merging them. Search looks up the first dictionary containing the key.


# ============================================================
# Q8: Recursive Deep Dictionary Merge (Deep Update)
# ============================================================
# Question: Implement a recursive deep merge function: when both dictionaries share
# a nested dictionary key, merge the inner dictionaries rather than overwriting.

print("\n=== Q8: Recursive Deep Dictionary Merge ===")

def deep_merge_dicts(base: dict, overlay: dict) -> dict:
    """Recursively merges overlay into base without destructive overwrites."""
    result = copy.deepcopy(base)
    
    for k, v in overlay.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            # Recursively merge inner dictionaries
            result[k] = deep_merge_dicts(result[k], v)
        else:
            # Overwrite or insert non-dict values
            result[k] = copy.deepcopy(v)
            
    return result

base_schema = {
    "server": {"host": "localhost", "port": 8080, "ssl": {"enabled": False}},
    "logging": {"level": "DEBUG", "dest": "stdout"}
}

overlay_schema = {
    "server": {"port": 443, "ssl": {"enabled": True, "cert": "/etc/ssl/cert.pem"}},
    "logging": {"dest": "/var/log/app.log"}
}

merged_config = deep_merge_dicts(base_schema, overlay_schema)
print("  Deeply Merged Schema:")
import pprint
for k, v in merged_config.items():
    print(f"    {k}: {v}")

# Verify that base['server']['host'] was preserved!
print(f"  Preserved nested base value server.host: '{merged_config['server']['host']}'")

# Explanation: Standard `.update()` or `|` replaces the entire nested dictionary.
# A recursive deep merge preserves unmentioned sibling keys in nested structures.


# ============================================================
# Q9: Dictionary Difference and Schema Diff Comparator
# ============================================================
# Question: Build a schema diff tool that compares two dictionaries and reports:
# added keys, removed keys, modified keys (with old/new values), and identical keys.

print("\n=== Q9: Dictionary Diff Comparator ===")

def diff_dictionaries(dict_old: dict, dict_new: dict) -> dict:
    """Compares two flat dictionaries and categorizes differences."""
    keys_old = set(dict_old.keys())
    keys_new = set(dict_new.keys())
    
    added_keys = keys_new - keys_old
    removed_keys = keys_old - keys_new
    common_keys = keys_old & keys_new
    
    modified = {}
    identical = set()
    
    for k in common_keys:
        if dict_old[k] != dict_new[k]:
            modified[k] = {"old": dict_old[k], "new": dict_new[k]}
        else:
            identical.add(k)
            
    return {
        "added": sorted(list(added_keys)),
        "removed": sorted(list(removed_keys)),
        "modified": modified,
        "identical": sorted(list(identical))
    }

version_1 = {"id": 101, "name": "Widget", "price": 19.99, "status": "DRAFT", "tag": "sale"}
version_2 = {"id": 101, "name": "Widget Pro", "price": 24.99, "status": "DRAFT", "sku": "WID-99"}

diff_report = diff_dictionaries(version_1, version_2)
print("  Diff Report:")
print(f"    Added keys:     {diff_report['added']}")
print(f"    Removed keys:   {diff_report['removed']}")
print(f"    Identical keys: {diff_report['identical']}")
print("    Modified keys:")
for k, change in diff_report["modified"].items():
    print(f"      {k}: {change['old']} -> {change['new']}")

# Explanation: Set operations on `dict.keys()` (`&`, `-`) provide efficient $O(N)$
# audit comparison between database records, API payloads, or config versions.


# ============================================================
# Q10: LRU (Least Recently Used) Cache via OrderedDict
# ============================================================
# Question: Implement an LRU cache of fixed capacity K using `collections.OrderedDict`.
# Both `get(key)` and `put(key, val)` run in O(1) time. When capacity is exceeded,
# evict the least recently accessed item.

print("\n=== Q10: LRU Cache Implementation ===")

class LRUCache:
    """Least Recently Used cache backed by OrderedDict."""
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self._cache = OrderedDict()

    def get(self, key: str) -> Any:
        if key not in self._cache:
            return None
        # Move accessed key to end (marking it as most recently used)
        self._cache.move_to_end(key, last=True)
        return self._cache[key]

    def put(self, key: str, value: Any):
        if key in self._cache:
            # Update existing key and mark most recently used
            self._cache.move_to_end(key, last=True)
        self._cache[key] = value
        
        # Check if capacity breached
        if len(self._cache) > self.capacity:
            # Pop least recently used item (the first item at front)
            evicted_key, evicted_val = self._cache.popitem(last=False)
            print(f"    [EVICT] Evicted LRU item: '{evicted_key}' (Value: {evicted_val})")

    def current_items(self) -> list:
        return list(self._cache.keys())

# Test LRU Cache with capacity 3
lru = LRUCache(capacity=3)
print("  Putting K1, K2, K3:")
lru.put("K1", "Data 1")
lru.put("K2", "Data 2")
lru.put("K3", "Data 3")
print(f"    State (Front=Oldest, Back=Newest): {lru.current_items()}")

print("\n  Accessing K1 (Moves K1 to most recent):")
_ = lru.get("K1")
print(f"    State: {lru.current_items()} (K2 is now the oldest!)")

print("\n  Putting K4 (Triggers eviction of oldest: K2):")
lru.put("K4", "Data 4")
print(f"    Final State: {lru.current_items()}")

# Summary Output
print("\n" + "=" * 55)
print("  All 10 Questions for Topic 03 - Q06 executed successfully!")
print("=" * 55)
