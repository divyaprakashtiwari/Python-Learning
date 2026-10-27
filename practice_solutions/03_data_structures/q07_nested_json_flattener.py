"""
Topic 03 - Data Structures: Question 7
Problem: Arbitrarily Nested JSON-like Hierarchy Flattener, Path Getter, and Depth Calculator.
"""

from typing import Any, Dict


def flatten_dict(nested_data: Any, parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """Recursively flattens nested dicts and lists into dot-delimited key-value pairs."""
    items = {}
    if isinstance(nested_data, dict):
        if not nested_data and parent_key:
            items[parent_key] = {}
        for k, v in nested_data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
            items.update(flatten_dict(v, new_key, sep=sep))
    elif isinstance(nested_data, list):
        if not nested_data and parent_key:
            items[parent_key] = []
        for idx, item in enumerate(nested_data):
            new_key = f"{parent_key}{sep}{idx}" if parent_key else str(idx)
            items.update(flatten_dict(item, new_key, sep=sep))
    else:
        items[parent_key] = nested_data
    return items


def get_by_path(nested_data: Any, key_path: str, default: Any = None, sep: str = ".") -> Any:
    """Traverses nested dicts/lists along a dot-separated path safely."""
    tokens = key_path.split(sep)
    current = nested_data
    for token in tokens:
        if isinstance(current, dict):
            if token in current:
                current = current[token]
            else:
                return default
        elif isinstance(current, list):
            if token.isdigit() and 0 <= int(token) < len(current):
                current = current[int(token)]
            else:
                return default
        else:
            return default
    return current


def calculate_max_depth(node: Any) -> int:
    """Calculates the maximum depth of nested dictionaries and lists."""
    if isinstance(node, dict) and node:
        return 1 + max(calculate_max_depth(v) for v in node.values())
    elif isinstance(node, list) and node:
        return 1 + max(calculate_max_depth(v) for v in node)
    return 0


config = {
    "app": "DataPipeline",
    "services": {
        "database": {
            "primary": {"host": "db-1.internal", "port": 5432},
            "replicas": [{"host": "db-2.internal"}, {"host": "db-3.internal"}]
        },
        "cache": {"enabled": True, "ttl": 3600}
    }
}

# 1. Recursive Flattening
flattened = flatten_dict(config)
print("Flattened Configuration:")
print("{")
for k, v in flattened.items():
    print(f"    '{k}': {repr(v)},")
print("}")

# 2. Safe Path-Based Getter
p1 = "services.database.primary.port"
print(f"Path Lookup ('{p1}'): {get_by_path(config, p1)}")

p2 = "services.database.replicas.1.host"
print(f"Path Lookup ('{p2}'): '{get_by_path(config, p2)}'")

p3 = "services.metrics.endpoint"
print(f"Path Lookup with Fallback ('{p3}'): '{get_by_path(config, p3, default='NOT_FOUND')}'")

# 3. Maximum Depth Calculator
depth = calculate_max_depth(config)
print(f"Maximum Tree Depth: {depth}")
