"""
Phase 6 - Section A (Complexity Analysis) - Topic 01: Time Complexity
Example 03: Python Built-in Container Lookup Complexity — `list` O(n) vs `set` O(1)

Demonstrates:
  - Why `x in my_list` scans sequentially in O(n) comparisons, whereas `x in my_set`
    computes `hash(x)` and probes the hash table in O(1) average comparisons
  - Reducing an O(n * m) duplicate intersection problem to O(n + m) using a `set`
"""


class TrackedInt(int):
    """Subclass of `int` that counts how many `==` equality comparisons are performed."""

    comparisons = 0

    def __eq__(self, other: object) -> bool:
        TrackedInt.comparisons += 1
        return super().__eq__(other)

    def __hash__(self) -> int:
        return super().__hash__()


def main() -> None:
    items_list = [TrackedInt(i) for i in range(500)]
    items_set = set(items_list)
    target = TrackedInt(499)  # Worst-case position at the very end of the list

    print("=== Comparing Equality Comparisons for Lookup of Last Element (N=500) ===")
    TrackedInt.comparisons = 0
    found_in_list = target in items_list
    list_comps = TrackedInt.comparisons

    TrackedInt.comparisons = 0
    found_in_set = target in items_set
    set_comps = TrackedInt.comparisons

    print(f"  target in list (O(n)) : found={found_in_list} | equality comparisons = {list_comps}")
    print(f"  target in set  (O(1)) : found={found_in_set} | equality comparisons = {set_comps}")


if __name__ == "__main__":
    main()
