"""
Phase 5 - Topic 16: Dataclasses
Example 02: `field(default_factory=...)`, `__post_init__` Validation, & `InitVar`

Demonstrates:
  - Why `@dataclass` forbids mutable defaults (`tags: list[str] = []` raises `ValueError`)
    and how `field(default_factory=list)` gives each instance its own fresh list
  - Hiding sensitive fields from `__repr__` using `field(repr=False)`
  - Derived fields and validation in `__post_init__()`
"""

from dataclasses import dataclass, field


@dataclass
class APIClientConfig:
    base_url: str
    api_key: str = field(repr=False)
    timeout_sec: float = 10.0
    default_headers: list[str] = field(default_factory=list)
    normalized_url: str = field(init=False)

    def __post_init__(self) -> None:
        if self.timeout_sec <= 0:
            raise ValueError("timeout_sec must be positive")
        self.normalized_url = self.base_url.rstrip("/")


def main() -> None:
    print("=== 1. Safe Mutable Defaults (`default_factory=list`) & Hidden `repr=False` ===")
    c1 = APIClientConfig("https://api.example.com/", api_key="secret-token-123")
    c2 = APIClientConfig("https://auth.example.com/", api_key="secret-token-456")
    c1.default_headers.append("X-Request-ID")

    print(f"  c1 repr (api_key hidden!): {c1!r}")
    print(f"  c2 default_headers       : {c2.default_headers} (isolated from c1!)")

    print("\n=== 2. `__post_init__` Validation Guard ===")
    try:
        APIClientConfig("https://api.example.com", api_key="k", timeout_sec=-5.0)
    except ValueError as err:
        print(f"  Caught expected validation error: {err}")


if __name__ == "__main__":
    main()
