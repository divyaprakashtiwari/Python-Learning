"""
Phase 5 - Topic 16: Dataclasses
Example 01: `@dataclass` Fundamentals — Auto-Generated `__init__`, `__repr__`, and `__eq__`

Demonstrates:
  - Eliminating boilerplate `__init__`, `__repr__`, and `__eq__` methods using `@dataclass`
  - Default field values and `dataclasses.asdict()` / `dataclasses.astuple()` conversion helpers
"""

from dataclasses import asdict, astuple, dataclass


@dataclass
class CourseModule:
    code: str
    title: str
    duration_hours: float = 2.5
    is_published: bool = True


def main() -> None:
    print("=== 1. Auto-Generated `__init__`, `__repr__`, and `__eq__` ===")
    m1 = CourseModule("PY-501", "Intermediate & Advanced Python", duration_hours=6.0)
    m2 = CourseModule("PY-501", "Intermediate & Advanced Python", duration_hours=6.0)
    print(f"  m1 repr        : {m1!r}")
    print(f"  m1 == m2       : {m1 == m2} (structural value equality, even though m1 is not m2!)")

    print("\n=== 2. Converting to `dict` and `tuple` (`asdict` / `astuple`) ===")
    print(f"  asdict(m1)     : {asdict(m1)}")
    print(f"  astuple(m1)    : {astuple(m1)}")


if __name__ == "__main__":
    main()
