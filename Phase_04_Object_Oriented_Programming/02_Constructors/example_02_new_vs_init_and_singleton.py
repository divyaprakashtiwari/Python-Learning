"""
Phase 4 - Topic 02: Constructors
Example 02: Two-Step Object Creation (`__new__` Allocator vs `__init__` Initializer)

Demonstrates:
  - The real difference between `__new__` (allocates and returns the instance)
    and `__init__` (initializes attributes on the already-allocated instance)
  - Using `__new__` to implement the classic Singleton Pattern and to subclass
    an immutable built-in type (`str` / `tuple`)
"""


class DatabaseConnectionPool:
    """Singleton class: `__new__` ensures only one pool instance is ever allocated."""

    _instance: "DatabaseConnectionPool | None" = None
    _initialized: bool = False

    def __new__(cls, *args: object, **kwargs: object) -> "DatabaseConnectionPool":
        print(f"    [1. __new__] Checking if {cls.__name__} singleton exists...")
        if cls._instance is None:
            print("    [1. __new__] Allocating brand-new instance via super().__new__(cls)")
            cls._instance = super().__new__(cls)
        else:
            print("    [1. __new__] Returning existing singleton instance!")
        return cls._instance

    def __init__(self, max_connections: int = 10) -> None:
        print(f"    [2. __init__] Running initializer (already initialized={self._initialized})")
        if not self._initialized:
            self.max_connections = max_connections
            self._initialized = True


class UpperSlug(str):
    """Subclassing immutable `str`: value must be transformed inside `__new__`, not `__init__`!"""

    def __new__(cls, raw_text: str) -> "UpperSlug":
        normalized = raw_text.strip().upper().replace(" ", "-")
        return super().__new__(cls, normalized)


def main() -> None:
    print("=== 1. Tracing `__new__` Followed by `__init__` (Singleton Pool) ===")
    pool_a = DatabaseConnectionPool(max_connections=20)
    pool_b = DatabaseConnectionPool(max_connections=99)
    print(f"  pool_a is pool_b        : {pool_a is pool_b}")
    print(f"  pool_b.max_connections  : {pool_b.max_connections} (preserved from first init!)")

    print("\n=== 2. Customizing Immutable Type Creation in `__new__` ===")
    slug = UpperSlug("  python oop constructors  ")
    print(f"  UpperSlug value         : {slug!r} | isinstance(slug, str)={isinstance(slug, str)}")


if __name__ == "__main__":
    main()
