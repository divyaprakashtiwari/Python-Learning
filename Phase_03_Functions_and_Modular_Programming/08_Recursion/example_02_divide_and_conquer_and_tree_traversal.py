"""
Phase 3 - Topic 08: Recursion
Example 02: Divide-and-Conquer Recursion & Nested Tree/JSON Flattening

Demonstrates:
  - Recursive Binary Search on a sorted list in O(log n) time
  - Traversing arbitrary-depth nested dictionaries/lists (where iteration is awkward
    and recursion is natural)
"""

from typing import Any


def binary_search_recursive(
    arr: list[int],
    target: int,
    low: int,
    high: int,
) -> int:
    """Return index of `target` in sorted `arr[low..high]`, or -1 if absent."""
    if low > high:
        return -1  # Base case: search space exhausted

    mid = (low + high) // 2
    if arr[mid] == target:
        return mid  # Base case: target found
    if target < arr[mid]:
        return binary_search_recursive(arr, target, low, mid - 1)
    return binary_search_recursive(arr, target, mid + 1, high)


def flatten_nested_json(
    data: dict[str, Any],
    parent_key: str = "",
    sep: str = ".",
) -> dict[str, Any]:
    """Recursively flatten an arbitrarily nested dictionary into dot-separated keys."""
    flat: dict[str, Any] = {}
    for key, value in data.items():
        full_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict) and value:
            # Recursive step: merge flattened sub-dictionary
            flat.update(flatten_nested_json(value, full_key, sep=sep))
        else:
            # Base case: leaf value
            flat[full_key] = value
    return flat


def main() -> None:
    print("=== 1. Recursive Binary Search ===")
    sorted_ids = [102, 115, 128, 144, 159, 173, 188, 205]
    for target in (144, 205, 130):
        idx = binary_search_recursive(sorted_ids, target, 0, len(sorted_ids) - 1)
        print(f"  Search target={target:<3} -> index={idx}")

    print("\n=== 2. Flattening Arbitrary-Depth Nested Config via Recursion ===")
    nested_config = {
        "service": "payment-api",
        "database": {
            "primary": {"host": "db-01.internal", "port": 5432},
            "pool": {"max_size": 20},
        },
        "feature_flags": {"enable_upi": True},
    }
    flattened = flatten_nested_json(nested_config)
    for k, v in flattened.items():
        print(f"  {k:<28} = {v!r}")


if __name__ == "__main__":
    main()
