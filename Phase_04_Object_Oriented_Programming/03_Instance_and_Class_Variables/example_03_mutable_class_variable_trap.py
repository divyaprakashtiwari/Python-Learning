"""
Phase 4 - Topic 03: Instance and Class Variables
Example 03: The Mutable Class Variable Trap (`permissions = []` on Class vs `self`)

Demonstrates:
  - Why defining a mutable list/dict/set as a class variable causes all instances
    to accidentally share and mutate the exact same container!
  - How to fix it by initializing mutable containers inside `__init__` on `self`
"""


class BuggyUserProfile:
    """BUGGY: `roles` is a mutable class variable shared by EVERY user instance!"""

    roles: list[str] = []

    def __init__(self, username: str) -> None:
        self.username = username


class SafeUserProfile:
    """SAFE: Each instance gets its own independent `self.roles` list in `__init__`."""

    def __init__(self, username: str) -> None:
        self.username = username
        self.roles: list[str] = []


def main() -> None:
    print("=== 1. The Mutable Class Variable Trap (`BuggyUserProfile`) ===")
    u1 = BuggyUserProfile("alice")
    u2 = BuggyUserProfile("bob")
    u1.roles.append("admin")
    print(f"  u1 ('alice') roles : {u1.roles}")
    print(f"  u2 ('bob')   roles : {u2.roles}  <-- Bob accidentally became admin!")
    print(f"  u1.roles is u2.roles: {u1.roles is u2.roles}")

    print("\n=== 2. The Fix: Initialize Mutable Attributes Inside `__init__` ===")
    s1 = SafeUserProfile("alice")
    s2 = SafeUserProfile("bob")
    s1.roles.append("admin")
    print(f"  s1 ('alice') roles : {s1.roles}")
    print(f"  s2 ('bob')   roles : {s2.roles}  <-- Clean and isolated!")
    print(f"  s1.roles is s2.roles: {s1.roles is s2.roles}")


if __name__ == "__main__":
    main()
