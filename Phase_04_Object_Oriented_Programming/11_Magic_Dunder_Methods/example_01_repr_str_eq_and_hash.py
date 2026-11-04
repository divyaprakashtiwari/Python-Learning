"""
Phase 4 - Topic 11: Magic/Dunder Methods
Example 01: String Representation (`__repr__` vs `__str__`) & Equality/Hashing (`__eq__`, `__hash__`)

Demonstrates:
  - `__repr__`: unambiguous developer/debugger representation (ideally valid Python code)
  - `__str__`: readable end-user representation (used by `print()` and `f"{obj}"`)
  - `__eq__` and `__hash__`: allowing custom immutable objects to be compared by value
    AND used as `dict` keys or `set` members!
"""


class SemanticVersion:
    """Immutable semantic version `(major, minor, patch)` supporting `==`, `<`, `set`, and `dict`."""

    def __init__(self, major: int, minor: int, patch: int) -> None:
        self._major = major
        self._minor = minor
        self._patch = patch

    def _as_tuple(self) -> tuple[int, int, int]:
        return (self._major, self._minor, self._patch)

    def __repr__(self) -> str:
        """Developer representation (used in lists, dicts, REPL, and tracebacks)."""
        return f"SemanticVersion({self._major}, {self._minor}, {self._patch})"

    def __str__(self) -> str:
        """User-facing display string (used by `print(v)` and `f'{v}'`)."""
        return f"v{self._major}.{self._minor}.{self._patch}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        return self._as_tuple() == other._as_tuple()

    def __lt__(self, other: "SemanticVersion") -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        return self._as_tuple() < other._as_tuple()

    def __hash__(self) -> int:
        """Required when `__eq__` is defined so instances remain hashable in sets/dicts."""
        return hash(self._as_tuple())


def main() -> None:
    v1 = SemanticVersion(3, 12, 0)
    v2 = SemanticVersion(3, 12, 0)
    v3 = SemanticVersion(3, 13, 7)

    print("=== 1. `__str__` vs `__repr__` ===")
    print(f"  str(v1)   / f'{{v1}}'   : {v1}")
    print(f"  repr(v1)  / f'{{v1!r}}' : {v1!r}")
    print(f"  Inside a list [v1, v3]  : {[v1, v3]} (containers always use __repr__!)")

    print("\n=== 2. Value Equality (`__eq__`), Sorting (`__lt__`), and Hashing (`__hash__`) ===")
    print(f"  v1 == v2 : {v1 == v2} | v1 is v2 : {v1 is v2}")
    print(f"  Sorted   : {sorted([v3, v1])}")
    unique_versions = {v1, v2, v3}
    print(f"  Set deduplication len({{v1, v2, v3}}) : {len(unique_versions)} -> {unique_versions}")


if __name__ == "__main__":
    main()
