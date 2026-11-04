"""
Phase 3 - Topic 04: Default Arguments
Example 02: The Mutable Default Argument Trap (`items=[]` vs `items=None`)

Demonstrates:
  - Why default argument values are evaluated ONCE at `def` definition time,
    NOT re-created on every function call
  - How a mutable default (`list`, `dict`, `set`) leaks state across separate calls
  - The canonical Python fix using `None` as a sentinel (`if items is None: items = []`)
  - Inspecting `func.__defaults__` to see the live mutated default tuple in memory
"""


def append_tag_buggy(tag: str, tags: list[str] = []) -> list[str]:
    """BUGGY: Default list `[]` is created once at `def` time and shared across calls!"""
    tags.append(tag)
    return tags


def append_tag_safe(tag: str, tags: list[str] | None = None) -> list[str]:
    """SAFE: Uses immutable `None` sentinel and creates a fresh list per call."""
    if tags is None:
        tags = []
    tags.append(tag)
    return tags


def main() -> None:
    print("=== 1. The Mutable Default Argument Trap (`tags=[]`) ===")
    print(f"  Before any call, __defaults__ = {append_tag_buggy.__defaults__}")
    call_1 = append_tag_buggy("python")
    print(f"  Call 1 (`append_tag_buggy('python')`)  -> {call_1}")
    call_2 = append_tag_buggy("backend")
    print(f"  Call 2 (`append_tag_buggy('backend')`) -> {call_2}  (LEAKED from Call 1!)")
    print(f"  After 2 calls,  __defaults__ = {append_tag_buggy.__defaults__}")
    print(f"  Are `call_1` and `call_2` the exact same list? {call_1 is call_2}")

    print("\n=== 2. The Canonical Fix (`tags: list[str] | None = None`) ===")
    safe_1 = append_tag_safe("python")
    print(f"  Call 1 (`append_tag_safe('python')`)   -> {safe_1}")
    safe_2 = append_tag_safe("backend")
    print(f"  Call 2 (`append_tag_safe('backend')`)  -> {safe_2}  (Clean fresh list!)")
    print(f"  Are `safe_1` and `safe_2` the exact same list? {safe_1 is safe_2}")

    # Passing an explicit list still works as expected
    existing = ["urgent"]
    safe_3 = append_tag_safe("hotfix", existing)
    print(f"  Call 3 (with existing list)            -> {safe_3}")


if __name__ == "__main__":
    main()
