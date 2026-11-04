"""
Phase 5 - Topic 10: Python Collections Module
Example 03: `collections.namedtuple` & `ChainMap` Layered Configs

Demonstrates:
  - Lightweight immutable tuple subclasses with named fields (`_replace`, `_asdict`)
  - Layered configuration lookup (`CLI args -> Env Vars -> Defaults`) without copying dicts using `ChainMap`
"""

from collections import ChainMap, namedtuple


Point2D = namedtuple("Point2D", ["x", "y"], defaults=[0, 0])


def main() -> None:
    print("=== 1. `namedtuple` -- Memory-Efficient Tuple with Named Attributes ===")
    p1 = Point2D(10, 25)
    p2 = p1._replace(x=50)
    print(f"  p1: {p1} | p1.x={p1.x}, p1[1]={p1[1]}")
    print(f"  p2 (`p1._replace(x=50)`): {p2} | _asdict()={p2._asdict()}")

    print("\n=== 2. `ChainMap` -- Layered Config Hierarchy (CLI -> Env -> Defaults) ===")
    defaults = {"host": "localhost", "port": 8080, "timeout": 30}
    env_vars = {"port": 9000}
    cli_args = {"timeout": 5}

    # Searches `cli_args` first, then `env_vars`, then `defaults`
    config = ChainMap(cli_args, env_vars, defaults)
    print(f"  Effective host    : {config['host']} (from defaults)")
    print(f"  Effective port    : {config['port']} (overridden by env_vars)")
    print(f"  Effective timeout : {config['timeout']} (overridden by cli_args)")


if __name__ == "__main__":
    main()
