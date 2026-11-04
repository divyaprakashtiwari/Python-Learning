"""
Phase 5 - Topic 03: Working with JSON
Example 01: `json.dumps()` and `json.loads()` — Pretty-Printing, Key Sorting, & Type Mapping

Demonstrates:
  - Converting Python objects (`dict`, `list`, `tuple`, `bool`, `None`) to JSON strings with `json.dumps()`
  - Controlling formatting (`indent=2`, `sort_keys=True`, `separators=(',', ':')`)
  - Parsing JSON strings back into Python objects with `json.loads()` (notice `tuple` becomes `list`)
"""

import json


def main() -> None:
    course_payload = {
        "title": "Python Complete Notes - Free Open Source",
        "phase": 5,
        "published": True,
        "prerequisites": ("Phase 1", "Phase 2", "Phase 3", "Phase 4"),
        "certificate_url": None,
        "metrics": {"topics": 142, "rating": 4.95},
    }

    print("=== 1. Pretty-Printed & Key-Sorted JSON String (`json.dumps`) ===")
    json_str = json.dumps(course_payload, indent=2, sort_keys=True)
    print(json_str)

    print("\n=== 2. Compact Wire Format (`separators=(',', ':')`) ===")
    compact_str = json.dumps(course_payload, separators=(",", ":"))
    print(f"  Length comparison: pretty={len(json_str)} chars vs compact={len(compact_str)} chars")

    print("\n=== 3. Round-Trip Parsing (`json.loads`) & Tuple->List Coercion ===")
    restored = json.loads(json_str)
    print(f"  Restored type: {type(restored).__name__} | published={restored['published']!r}")
    print(f"  Original prerequisites type: {type(course_payload['prerequisites']).__name__}")
    print(f"  Restored prerequisites type: {type(restored['prerequisites']).__name__} -> {restored['prerequisites']}")


if __name__ == "__main__":
    main()
