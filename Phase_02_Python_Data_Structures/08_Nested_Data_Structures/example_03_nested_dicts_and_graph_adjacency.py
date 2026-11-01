"""
Topic 08: Nested Data Structures
Example 03: Safe Deep Dict Lookup & Weighted Graph Adjacency List

Demonstrates:
1. A safe `deep_get()` helper to traverse deeply nested dictionaries without `KeyError`.
2. Representing a weighted graph as `dict[str, list[tuple[str, int]]]`.
"""

from typing import Any


def deep_get(data: dict, path: list[str], default: Any = None) -> Any:
    """Safely navigate a nested dictionary along `path` keys."""
    current: Any = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def main() -> None:
    app_config = {
        "server": {
            "database": {
                "host": "db.internal.local",
                "port": 5432,
            }
        }
    }

    print("=== 1. Safe Deep Dictionary Navigation ===")
    db_host = deep_get(app_config, ["server", "database", "host"], default="localhost")
    redis_host = deep_get(app_config, ["server", "cache", "host"], default="127.0.0.1")
    print(f"Resolved DB Host    : {db_host}")
    print(f"Resolved Cache Host : {redis_host} (Fallback default)")

    print("\n=== 2. Weighted Graph Adjacency List (dict of list of tuples) ===")
    flight_graph: dict[str, list[tuple[str, int]]] = {
        "DEL": [("BOM", 1150), ("BLR", 1740)],
        "BOM": [("BLR", 840), ("HYD", 620)],
        "BLR": [("HYD", 500)],
    }
    for origin, edges in flight_graph.items():
        formatted_edges = ", ".join(f"{dest} ({km} km)" for dest, km in edges)
        print(f"  {origin} -> {formatted_edges}")


if __name__ == "__main__":
    main()
