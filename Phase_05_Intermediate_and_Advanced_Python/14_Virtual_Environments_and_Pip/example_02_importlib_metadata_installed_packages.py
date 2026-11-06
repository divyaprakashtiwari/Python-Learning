"""
Phase 5 - Topic 14: Virtual Environments and pip
Example 02: Querying Installed Packages Programmatically with `importlib.metadata`

Demonstrates:
  - Inspecting installed distributions (`pip` itself) using Python's built-in `importlib.metadata`
  - Listing package metadata (`Name`, `Version`, `Summary`) without spawning a subprocess
"""

from importlib import metadata


def inspect_distribution(pkg_name: str) -> dict[str, str]:
    """Fetch standard metadata for an installed distribution (`pip`)."""
    meta = metadata.metadata(pkg_name)
    return {
        "name": meta["Name"],
        "summary": meta["Summary"],
        "has_version": str(bool(metadata.version(pkg_name))),
    }


def main() -> None:
    print("=== Querying Installed `pip` Distribution via `importlib.metadata` ===")
    info = inspect_distribution("pip")
    print(f"  Package Name    : {info['name']}")
    print(f"  Version Present : {info['has_version']}")
    print(f"  Summary         : {info['summary']}")


if __name__ == "__main__":
    main()
