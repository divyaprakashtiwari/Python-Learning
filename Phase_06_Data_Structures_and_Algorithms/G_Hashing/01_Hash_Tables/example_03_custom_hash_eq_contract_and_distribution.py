"""
Phase 6 - Data Structures and Algorithms
Section G: Hashing
Topic 01: Hash Tables
Example 03: Custom Hashable Classes (`__hash__` and `__eq__` Contract) &
            Polynomial Rolling Hash Distribution Benchmark

In Python, an object can be used as a `dict` key or `set` member if and only if it is
**hashable** — meaning it implements `__hash__(self) -> int` and `__eq__(self, other) -> bool`
obeying the **Fundamental Hash Invariant**:
  1. If `a == b`, then `hash(a) == hash(b)` MUST hold!
  2. `hash(a)` MUST NEVER CHANGE during `a`'s lifetime inside a hash table (which is
     why mutable containers like `list`, `dict`, and `set` set `__hash__ = None`).

We demonstrate:
  - What breaks when a mutable attribute used in `__hash__` is mutated after insertion.
  - Implementing a rock-solid immutable custom key class (`GridCoord` / `EmployeeKey`).
  - Comparing a bad additive hash (`sum(ord(c))`) against a Polynomial Rolling Hash
    (`sum(c * 31^i)`) on anagrams and English words.
"""

from typing import Dict, List


class ImmutableEmployeeKey:
    """
    Properly hashable custom key class enforcing immutability of key fields and
    satisfying `a == b => hash(a) == hash(b)`.
    """

    __slots__ = ("_emp_id", "_dept")

    def __init__(self, emp_id: int, dept: str) -> None:
        self._emp_id = emp_id
        self._dept = dept.strip().upper()  # Normalize before hashing & comparing!

    @property
    def emp_id(self) -> int:
        return self._emp_id

    @property
    def dept(self) -> str:
        return self._dept

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ImmutableEmployeeKey):
            return NotImplemented
        return (self._emp_id, self._dept) == (other._emp_id, other._dept)

    def __hash__(self) -> int:
        # Delegate to tuple hash of the exact same fields checked in `__eq__`
        return hash((self._emp_id, self._dept))

    def __repr__(self) -> str:
        return f"Emp({self._emp_id}, '{self._dept}')"


def bad_additive_hash(word: str, num_buckets: int) -> int:
    """Bad hash function: sums character codes (all anagrams collide!)."""
    return sum(ord(ch) for ch in word) % num_buckets


def polynomial_rolling_hash(word: str, num_buckets: int, base: int = 31) -> int:
    """Good hash function: position-sensitive polynomial rolling hash."""
    h = 0
    for ch in word:
        h = (h * base + ord(ch)) & 0x7FFFFFFF
    return h % num_buckets


if __name__ == "__main__":
    print("=" * 72)
    print("1. Custom `__hash__` and `__eq__` Contract Verification")
    print("=" * 72)

    k1 = ImmutableEmployeeKey(101, "engineering")
    k2 = ImmutableEmployeeKey(101, "  ENGINEERING ")
    print(f"k1 = {k1}, k2 = {k2}")
    print(f"k1 == k2          : {k1 == k2}")
    print(f"hash(k1)==hash(k2): {hash(k1) == hash(k2)}")

    payroll: Dict[ImmutableEmployeeKey, int] = {k1: 145_000}
    print(f"Lookup payroll[k2]: Rs. {payroll[k2]:,}")

    print("\n" + "=" * 72)
    print("2. Additive Hash vs Polynomial Rolling Hash on Anagrams (16 Buckets)")
    print("=" * 72)
    anagrams: List[str] = ["listen", "silent", "enlist", "inlets", "tinsel"]
    for w in anagrams:
        b_bad = bad_additive_hash(w, 16)
        b_good = polynomial_rolling_hash(w, 16)
        print(f"  word = '{w}' -> Bad Additive Bucket = {b_bad:>2} | Polynomial Bucket = {b_good:>2}")

