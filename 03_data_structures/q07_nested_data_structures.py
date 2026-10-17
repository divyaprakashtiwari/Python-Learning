"""
Topic 03: Data Structures
Question 07: Nested Data Structures (Deep Dive)

Master complex nested collections in Python:
- Multi-dimensional indexing and matrix coordinates
- Shallow vs deep copy pitfalls in nested structures
- Safe deep path lookup (dot-notation / JSON pointers)
- Recursive dictionary flattening and unflattening
- Multi-level grouping and relational pivot tables
- Recursive data sanitization (sensitive key masking)
- Tree hierarchies and recursive traversal
- Structural deep diff comparison
- In-memory document store with nested path queries
"""

import copy
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple, Union


# ============================================================
# Q1: Multi-Dimensional Coordinate Indexing & Grid Traversal
# ============================================================
# Question: Implement coordinate-based access for 2D and 3D nested grids.
# Handle negative indexing, boundary validation, and row/column extraction.

print("=== Q1: Multi-Dimensional Coordinate Indexing ===")

grid_3x3: List[List[int]] = [
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
]

def safe_grid_get(matrix: List[List[Any]], row: int, col: int, default: Any = None) -> Any:
    """Safely retrieves a value from a 2D matrix with boundary checking."""
    if 0 <= row < len(matrix) and 0 <= col < len(matrix[row]):
        return matrix[row][col]
    return default

def get_column(matrix: List[List[Any]], col_index: int) -> List[Any]:
    """Extracts an entire column across all rows."""
    return [row[col_index] for row in matrix if 0 <= col_index < len(row)]

center_val = safe_grid_get(grid_3x3, 1, 1)
oob_val = safe_grid_get(grid_3x3, 5, 2, default=-1)
col_1 = get_column(grid_3x3, 1)

print(f"  Center value (1, 1): {center_val}")
print(f"  Out of bounds (5, 2): {oob_val}")
print(f"  Column 1 extraction: {col_1}")

assert center_val == 50
assert oob_val == -1
assert col_1 == [20, 50, 80]

# Explanation: In 2D lists `matrix[r][c]`, row is selected first, then column.
# Column slices do not exist natively for built-in lists (unlike NumPy),
# requiring list comprehensions or zip(*matrix).


# ============================================================
# Q2: Shallow vs Deep Copy Pitfalls in Nested Structures
# ============================================================
# Question: Demonstrate the multiplication multiplication pitfall (`[[0]*3]*3`),
# shallow copy mutation bleed, and how `copy.deepcopy` isolates nested references.

print("\n=== Q2: Shallow vs Deep Copy Pitfalls ===")

# The classic multiplication trap: 3 rows pointing to the EXACT SAME list object in memory!
buggy_board = [[0] * 3] * 3
buggy_board[0][0] = 99
print(f"  Buggy grid after modifying [0][0]: {buggy_board}")
# Note how ALL rows reflect 99 because row references are identical
assert buggy_board[1][0] == 99 and buggy_board[2][0] == 99

# Correct creation with list comprehension
clean_board = [[0] * 3 for _ in range(3)]
clean_board[0][0] = 99
print(f"  Clean grid after modifying [0][0]: {clean_board}")
assert clean_board[1][0] == 0 and clean_board[2][0] == 0

# Shallow copy of a nested structure vs deepcopy
original_profile = {
    "user": "alice",
    "roles": ["editor", "viewer"],
    "prefs": {"theme": "light"}
}

shallow_copy = original_profile.copy()
deep_copy = copy.deepcopy(original_profile)

# Mutating nested structures
shallow_copy["roles"].append("admin")
shallow_copy["prefs"]["theme"] = "dark"

print(f"  Original after shallow mutation -> roles: {original_profile['roles']}, theme: {original_profile['prefs']['theme']}")
print(f"  Deep copy remains isolated      -> roles: {deep_copy['roles']}, theme: {deep_copy['prefs']['theme']}")

assert "admin" in original_profile["roles"], "Shallow copy shares nested references!"
assert deep_copy["roles"] == ["editor", "viewer"], "Deep copy must remain isolated!"
assert deep_copy["prefs"]["theme"] == "light"

# Explanation: A shallow copy creates a new top-level container, but retains
# references to child mutable objects. `copy.deepcopy()` recursively duplicates
# all nested containers and values.


# ============================================================
# Q3: Safe Deep Path Lookup (Dot / Slash Notation)
# ============================================================
# Question: Write a resilient deep lookup function `get_path(data, "a.b.0.c", default=None)`
# that supports dictionary keys and list index integers without raising exceptions.

print("\n=== Q3: Safe Deep Path Lookup ===")

nested_payload = {
    "server": {
        "clusters": [
            {"id": "us-east-1", "nodes": [{"ip": "10.0.0.1", "status": "UP"}]},
            {"id": "eu-central-1", "nodes": []}
        ]
    }
}

def get_path(data: Any, path: str, default: Any = None, delimiter: str = ".") -> Any:
    """Traverse nested dicts and lists using dot notation with integer indices."""
    tokens = path.split(delimiter)
    curr = data
    for token in tokens:
        if isinstance(curr, dict) and token in curr:
            curr = curr[token]
        elif isinstance(curr, list) and token.isdigit():
            idx = int(token)
            if 0 <= idx < len(curr):
                curr = curr[idx]
            else:
                return default
        else:
            return default
    return curr

node_ip = get_path(nested_payload, "server.clusters.0.nodes.0.ip")
missing_node = get_path(nested_payload, "server.clusters.1.nodes.0.ip", default="N/A")
bad_path = get_path(nested_payload, "server.non_existent.key", default="UNKNOWN")

print(f"  Lookup 'server.clusters.0.nodes.0.ip' -> {node_ip}")
print(f"  Lookup 'server.clusters.1.nodes.0.ip' -> {missing_node}")
print(f"  Lookup 'server.non_existent.key'      -> {bad_path}")

assert node_ip == "10.0.0.1"
assert missing_node == "N/A"
assert bad_path == "UNKNOWN"

# Explanation: Parsing path tokens allows safely navigating arbitrary JSON structures
# without chain-nesting `.get()` calls or catching multiple KeyError/IndexError exceptions.


# ============================================================
# Q4: Recursive Dictionary Flattener
# ============================================================
# Question: Recursively flatten an arbitrarily nested dictionary into a single-level
# dictionary where keys are concatenated with dots (e.g., {"a": {"b": 1}} -> {"a.b": 1}).
# Also support nested lists with indexed keys.

print("\n=== Q4: Recursive Dictionary Flattener ===")

complex_config = {
    "app": {
        "name": "DataPipeline",
        "version": "2.4.1",
        "settings": {
            "retries": 3,
            "timeout_seconds": 30
        }
    },
    "endpoints": [
        {"url": "https://api.v1.org", "auth": True},
        {"url": "https://backup.v1.org", "auth": False}
    ]
}

def flatten_dict(d: Any, parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """Recursively flattens nested dictionaries and lists into dot-delimited keys."""
    items: List[Tuple[str, Any]] = []
    
    if isinstance(d, dict):
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
            items.extend(flatten_dict(v, new_key, sep=sep).items())
    elif isinstance(d, list):
        for i, v in enumerate(d):
            new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
            items.extend(flatten_dict(v, new_key, sep=sep).items())
    else:
        items.append((parent_key, d))
        
    return dict(items)

flattened = flatten_dict(complex_config)
print("  Flattened structure:")
for key, val in list(flattened.items())[:5]:
    print(f"    {key}: {val}")

assert flattened["app.name"] == "DataPipeline"
assert flattened["app.settings.retries"] == 3
assert flattened["endpoints.0.url"] == "https://api.v1.org"
assert flattened["endpoints.1.auth"] is False

# Explanation: Recursion inspects container types (dict/list) at each layer,
# accumulating the prefix key path until terminal scalar values are reached.


# ============================================================
# Q5: Unflattening Dotted Keys into Deeply Nested Dictionaries
# ============================================================
# Question: Implement the inverse operation: reconstruct a deeply nested dictionary
# from a flat dictionary of dotted keys.

print("\n=== Q5: Unflattening Dotted Keys ===")

flat_data = {
    "database.primary.host": "db.internal",
    "database.primary.port": 5432,
    "database.replica.host": "db-rep.internal",
    "database.replica.port": 5433,
    "logging.level": "INFO"
}

def unflatten_dict(flat: Dict[str, Any], sep: str = ".") -> Dict[str, Any]:
    """Reconstructs nested dictionaries from dot-delimited key-value pairs."""
    result: Dict[str, Any] = {}
    for compound_key, value in flat.items():
        parts = compound_key.split(sep)
        curr = result
        for part in parts[:-1]:
            if part not in curr or not isinstance(curr[part], dict):
                curr[part] = {}
            curr = curr[part]
        curr[parts[-1]] = value
    return result

unflattened = unflatten_dict(flat_data)
print(f"  Unflattened primary host: {unflattened['database']['primary']['host']}")
print(f"  Unflattened replica port: {unflattened['database']['replica']['port']}")
print(f"  Logging level:            {unflattened['logging']['level']}")

assert unflattened["database"]["primary"]["host"] == "db.internal"
assert unflattened["database"]["primary"]["port"] == 5432
assert unflattened["logging"]["level"] == "INFO"

# Explanation: Unflattening splits each key by separator and traverses down the
# structure, instantiating intermediate empty dictionaries whenever a path segment is missing.


# ============================================================
# Q6: Relational Pivot & Multi-Level Aggregation
# ============================================================
# Question: Given a flat list of employee dictionaries (records), aggregate and group
# them into a multi-tier hierarchy: {department -> {role -> [employee names]}}.
# Also compute total salary per department.

print("\n=== Q6: Multi-Level Grouping & Aggregation ===")

employees = [
    {"name": "Alice",   "dept": "Engineering", "role": "Senior Dev", "salary": 120000},
    {"name": "Bob",     "dept": "Engineering", "role": "Junior Dev", "salary": 80000},
    {"name": "Charlie", "dept": "Engineering", "role": "Senior Dev", "salary": 130000},
    {"name": "Diana",   "dept": "Marketing",   "role": "Content Lead", "salary": 95000},
    {"name": "Evan",    "dept": "Marketing",   "role": "Designer",     "salary": 90000},
    {"name": "Fiona",   "dept": "Sales",       "role": "Account Exec", "salary": 105000},
]

# Nested defaultdict: dept -> role -> list of names
nested_dept_roster: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
dept_salary_totals: Dict[str, int] = defaultdict(int)

for emp in employees:
    dept = emp["dept"]
    role = emp["role"]
    name = emp["name"]
    nested_dept_roster[dept][role].append(name)
    dept_salary_totals[dept] += emp["salary"]

print("  Engineering Senior Devs:", nested_dept_roster["Engineering"]["Senior Dev"])
print("  Marketing Designers:    ", nested_dept_roster["Marketing"]["Designer"])
print("  Total Engineering Salary:", f"${dept_salary_totals['Engineering']:,}")

assert nested_dept_roster["Engineering"]["Senior Dev"] == ["Alice", "Charlie"]
assert dept_salary_totals["Engineering"] == 330000
assert dept_salary_totals["Marketing"] == 185000

# Explanation: `defaultdict(lambda: defaultdict(list))` automatically instantiates
# nested layers on first access, eliminating verbose membership checks and `setdefault`.


# ============================================================
# Q7: Recursive Data Sanitization (Sensitive Key Masking)
# ============================================================
# Question: Write a recursive sanitizer that masks sensitive values (e.g., "password",
# "token", "ssn", "secret") with "***REDACTED***" across arbitrary nested dicts and lists.

print("\n=== Q7: Recursive Data Sanitization ===")

audit_log = {
    "event_id": 98412,
    "credentials": {
        "username": "superadmin",
        "password": "CleartextPassword123!",
        "api_tokens": ["token_live_abc123", "token_test_xyz789"]
    },
    "metadata": {
        "ip": "192.168.1.50",
        "headers": {
            "Authorization": "Bearer eyJhbGciOi...",
            "User-Agent": "Mozilla/5.0"
        }
    }
}

SENSITIVE_KEYS = {"password", "api_tokens", "authorization", "secret", "token"}

def sanitize_nested(obj: Any, mask: str = "***REDACTED***") -> Any:
    """Recursively duplicates and redacts sensitive keys in dictionaries and lists."""
    if isinstance(obj, dict):
        sanitized = {}
        for k, v in obj.items():
            if str(k).lower() in SENSITIVE_KEYS:
                sanitized[k] = mask
            else:
                sanitized[k] = sanitize_nested(v, mask)
        return sanitized
    elif isinstance(obj, list):
        return [sanitize_nested(elem, mask) for elem in obj]
    else:
        return obj

sanitized_log = sanitize_nested(audit_log)
print(f"  Sanitized password:      {sanitized_log['credentials']['password']}")
print(f"  Sanitized api_tokens:    {sanitized_log['credentials']['api_tokens']}")
print(f"  Preserved username:      {sanitized_log['credentials']['username']}")
print(f"  Sanitized Authorization: {sanitized_log['metadata']['headers']['Authorization']}")

assert sanitized_log["credentials"]["password"] == "***REDACTED***"
assert sanitized_log["credentials"]["api_tokens"] == "***REDACTED***"
assert sanitized_log["credentials"]["username"] == "superadmin"
assert sanitized_log["metadata"]["headers"]["Authorization"] == "***REDACTED***"
# Verify original is unmutated
assert audit_log["credentials"]["password"] == "CleartextPassword123!"

# Explanation: By creating a new structure during recursive traversal, the original
# data remains unmodified (pure functional transformation) while redacting sensitive fields.


# ============================================================
# Q8: Tree Representation & Recursive Depth Traversal
# ============================================================
# Question: Model a corporate organization tree using nested dictionaries.
# Calculate total headcount under a manager and find the reporting path to an employee.

print("\n=== Q8: Org Tree & Recursive Depth Traversal ===")

org_tree = {
    "name": "Sarah (CEO)",
    "reports": [
        {
            "name": "Mark (VP Eng)",
            "reports": [
                {"name": "Leo (Lead Arch)", "reports": []},
                {"name": "Maya (Dev)", "reports": []}
            ]
        },
        {
            "name": "Chloe (VP Sales)",
            "reports": [
                {"name": "Zack (Rep)", "reports": []}
            ]
        }
    ]
}

def count_headcount(node: Dict[str, Any]) -> int:
    """Recursively counts total employees including the node itself."""
    count = 1  # Self
    for sub in node.get("reports", []):
        count += count_headcount(sub)
    return count

def find_path_to_employee(node: Dict[str, Any], target_name: str, path: Optional[List[str]] = None) -> Optional[List[str]]:
    """Returns the chain of command from root to target employee."""
    if path is None:
        path = []
    
    current_path = path + [node["name"]]
    if node["name"] == target_name:
        return current_path
    
    for report in node.get("reports", []):
        found = find_path_to_employee(report, target_name, current_path)
        if found:
            return found
    return None

total_company_size = count_headcount(org_tree)
maya_chain = find_path_to_employee(org_tree, "Maya (Dev)")

print(f"  Total company headcount: {total_company_size}")
print(f"  Chain of command to Maya: {' -> '.join(maya_chain if maya_chain else [])}")

assert total_company_size == 6
assert maya_chain == ["Sarah (CEO)", "Mark (VP Eng)", "Maya (Dev)"]

# Explanation: Trees in Python are naturally represented via recursive dict structures
# with child lists. Traversal follows standard Depth-First Search (DFS) patterns.


# ============================================================
# Q9: Structural Deep Difference Comparator
# ============================================================
# Question: Compare two nested dictionary structures and report differences:
# added keys, removed keys, and modified values with their full dot paths.

print("\n=== Q9: Structural Deep Difference Comparator ===")

v1_config = {
    "database": {"host": "localhost", "port": 5432, "pool_size": 10},
    "cache": {"enabled": True, "ttl": 300},
    "tags": ["prod", "us-east"]
}

v2_config = {
    "database": {"host": "db.prod.internal", "port": 5432, "ssl": True},
    "cache": {"enabled": True, "ttl": 600},
    "tags": ["prod", "us-east"]
}

def deep_diff(d1: Any, d2: Any, path: str = "") -> Dict[str, List[str]]:
    """Compares two nested dictionaries and returns added, removed, and modified paths."""
    diffs = {"added": [], "removed": [], "modified": []}

    def _compare(o1: Any, o2: Any, curr_path: str):
        if isinstance(o1, dict) and isinstance(o2, dict):
            keys1, keys2 = set(o1.keys()), set(o2.keys())
            for k in keys2 - keys1:
                diffs["added"].append(f"{curr_path}.{k}" if curr_path else k)
            for k in keys1 - keys2:
                diffs["removed"].append(f"{curr_path}.{k}" if curr_path else k)
            for k in keys1 & keys2:
                sub_path = f"{curr_path}.{k}" if curr_path else k
                _compare(o1[k], o2[k], sub_path)
        elif o1 != o2:
            diffs["modified"].append(f"{curr_path} (from {repr(o1)} to {repr(o2)})")

    _compare(d1, d2, path)
    return diffs

diff_result = deep_diff(v1_config, v2_config)
print(f"  Added paths:    {diff_result['added']}")
print(f"  Removed paths:  {diff_result['removed']}")
print(f"  Modified paths: {diff_result['modified']}")

assert "database.ssl" in diff_result["added"]
assert "database.pool_size" in diff_result["removed"]
assert any("database.host" in item for item in diff_result["modified"])
assert any("cache.ttl" in item for item in diff_result["modified"])

# Explanation: Deep diffing walks matching keys in both dictionaries, detecting added
# or removed keys via set symmetric differences, and recursing on matching keys.


# ============================================================
# Q10: Real-World In-Memory Document Store with Nested Queries
# ============================================================
# Question: Implement a miniature document store that queries collections of nested
# dicts using path expressions with operators ($gt, $eq, $in, $contains).

print("\n=== Q10: In-Memory Document Store Query Engine ===")

class MiniDocStore:
    def __init__(self):
        self._docs: List[Dict[str, Any]] = []

    def insert(self, doc: Dict[str, Any]) -> None:
        self._docs.append(copy.deepcopy(doc))

    def _resolve_path(self, doc: Dict[str, Any], path: str) -> Any:
        tokens = path.split(".")
        curr = doc
        for t in tokens:
            if isinstance(curr, dict) and t in curr:
                curr = curr[t]
            else:
                return None
        return curr

    def _eval_clause(self, doc_val: Any, condition: Any) -> bool:
        if isinstance(condition, dict):
            for op, expected in condition.items():
                if op == "$gt" and not (doc_val is not None and doc_val > expected):
                    return False
                elif op == "$lt" and not (doc_val is not None and doc_val < expected):
                    return False
                elif op == "$in" and not (doc_val in expected):
                    return False
                elif op == "$contains" and not (isinstance(doc_val, (list, str)) and expected in doc_val):
                    return False
            return True
        return doc_val == condition

    def find(self, filter_spec: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        for doc in self._docs:
            matched = True
            for path, condition in filter_spec.items():
                val = self._resolve_path(doc, path)
                if not self._eval_clause(val, condition):
                    matched = False
                    break
            if matched:
                results.append(doc)
        return results

store = MiniDocStore()
store.insert({
    "id": 101,
    "title": "Clean Code",
    "meta": {"pricing": {"usd": 38.50, "in_stock": True}, "tags": ["programming", "craftsmanship"]}
})
store.insert({
    "id": 102,
    "title": "Design Patterns",
    "meta": {"pricing": {"usd": 54.00, "in_stock": False}, "tags": ["architecture", "gof"]}
})
store.insert({
    "id": 103,
    "title": "Refactoring",
    "meta": {"pricing": {"usd": 45.00, "in_stock": True}, "tags": ["programming", "refactoring"]}
})

# Query: pricing > 40 USD and in_stock == True
price_query = store.find({
    "meta.pricing.usd": {"$gt": 40.00},
    "meta.pricing.in_stock": True
})

# Query: tags containing "programming"
tag_query = store.find({
    "meta.tags": {"$contains": "programming"}
})

print(f"  Books > $40 in stock: {[b['title'] for b in price_query]}")
print(f"  Books with 'programming' tag: {[b['title'] for b in tag_query]}")

assert len(price_query) == 1 and price_query[0]["id"] == 103
assert len(tag_query) == 2 and {b["id"] for b in tag_query} == {101, 103}

print("\nAll 10 nested data structure questions executed and asserted successfully!")
