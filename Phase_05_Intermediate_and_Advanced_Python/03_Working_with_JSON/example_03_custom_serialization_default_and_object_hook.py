"""
Phase 5 - Topic 03: Working with JSON
Example 03: Custom Serialization (`default=`) & Deserialization (`object_hook=`)

Demonstrates:
  - Teaching `json.dumps()` how to serialize `datetime.date`, `set`, and custom classes
    using a custom `default=` serializer function
  - Reconstructing typed domain objects during `json.loads()` using `object_hook=`
"""

from dataclasses import dataclass
from datetime import date
import json


@dataclass(frozen=True)
class ReleaseBuild:
    version: str
    released_on: date
    tags: set[str]


def custom_json_default(obj: object) -> object:
    """Convert non-JSON-native Python types into tagged dictionaries."""
    if isinstance(obj, ReleaseBuild):
        return {
            "__type__": "ReleaseBuild",
            "version": obj.version,
            "released_on": obj.released_on.isoformat(),
            "tags": sorted(obj.tags),
        }
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def custom_json_object_hook(dct: dict[str, object]) -> object:
    """Reconstruct `ReleaseBuild` instances when `__type__ == 'ReleaseBuild'` is encountered."""
    if dct.get("__type__") == "ReleaseBuild":
        return ReleaseBuild(
            version=str(dct["version"]),
            released_on=date.fromisoformat(str(dct["released_on"])),
            tags=set(dct["tags"]),  # type: ignore[arg-type]
        )
    return dct


def main() -> None:
    build = ReleaseBuild(version="2.4.0", released_on=date(2026, 11, 4), tags={"stable", "lts"})

    print("=== 1. Serializing Custom Object with `default=custom_json_default` ===")
    encoded = json.dumps(build, default=custom_json_default, indent=2)
    print(encoded)

    print("\n=== 2. Deserializing Back to Domain Object with `object_hook=` ===")
    decoded = json.loads(encoded, object_hook=custom_json_object_hook)
    print(f"  Decoded object : {decoded!r}")
    print(f"  Equality check : {decoded == build} (type={type(decoded).__name__})")


if __name__ == "__main__":
    main()
