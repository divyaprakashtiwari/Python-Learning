"""
Phase 4 - Topic 01: Classes and Objects
Example 02: Object Identity (`is` vs `==`), Type Inspection (`isinstance`), and `__dict__`

Demonstrates:
  - Why two distinct instances with identical attributes have `a is b -> False`
  - Inspecting an object's runtime class (`type(obj)`, `isinstance(obj, Class)`)
  - Inspecting the underlying attribute dictionary `obj.__dict__`
  - Dynamic attribute assignment vs using `__slots__` for fixed-attribute memory efficiency
"""


class ServerNode:
    """Standard class backed by a per-instance `__dict__` namespace."""

    def __init__(self, hostname: str, ip_address: str) -> None:
        self.hostname = hostname
        self.ip_address = ip_address


class CompactMetricPoint:
    """Memory-efficient class using `__slots__` (no per-instance `__dict__`)."""

    __slots__ = ("timestamp", "cpu_load")

    def __init__(self, timestamp: int, cpu_load: float) -> None:
        self.timestamp = timestamp
        self.cpu_load = cpu_load


def main() -> None:
    print("=== 1. Object Identity (`is`) vs Attribute Values ===")
    node_a = ServerNode("api-prod-01", "10.0.1.15")
    node_b = ServerNode("api-prod-01", "10.0.1.15")
    node_alias = node_a

    print(f"  node_a is node_b        : {node_a is node_b} (two separate objects in memory)")
    print(f"  node_a is node_alias    : {node_a is node_alias} (alias to same object)")
    print(f"  isinstance(node_a, ServerNode) : {isinstance(node_a, ServerNode)}")
    print(f"  isinstance(node_a, object)     : {isinstance(node_a, object)} (all classes inherit from object)")

    print("\n=== 2. Inspecting the Instance Namespace (`obj.__dict__`) ===")
    print(f"  Initial node_a.__dict__ : {node_a.__dict__}")
    # Dynamically adding a new attribute at runtime updates `node_a.__dict__`
    node_a.region = "ap-south-1"  # type: ignore[attr-defined]
    print(f"  After adding `.region`  : {node_a.__dict__}")
    print(f"  node_b.__dict__         : {node_b.__dict__} (unaffected!)")

    print("\n=== 3. Preventing Accidental Dynamic Attributes with `__slots__` ===")
    metric = CompactMetricPoint(1730716800, 0.74)
    print(f"  metric.timestamp={metric.timestamp}, metric.cpu_load={metric.cpu_load}")
    print(f"  Has `__dict__`?         : {hasattr(metric, '__dict__')}")
    try:
        metric.typo_attribute = 99.9  # type: ignore[attr-defined]
    except AttributeError as err:
        print(f"  Caught expected AttributeError: {err}")


if __name__ == "__main__":
    main()
