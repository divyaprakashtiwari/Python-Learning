"""
Phase 6 - Section G.03: Hash Sets
Example 03: Set Operations, Happy Number, and Custom HashSet Implementation

Demonstrating:
1. Cycle detection in sequences using a HashSet (Happy Number problem).
2. Fundamental mathematical set operations (union, intersection, difference, symmetric difference).
3. Custom HashSet implementation using separate chaining buckets.
"""


def is_happy(n):
    """
    Determine if a number is happy (sum of squares of digits reaches 1).
    Uses a HashSet to detect infinite cycles.
    """
    def get_next(num):
        total = 0
        while num > 0:
            num, digit = divmod(num, 10)
            total += digit * digit
        return total

    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = get_next(n)

    return n == 1


class SimpleHashSet:
    """
    Custom HashSet implementation using separate chaining.
    """
    def __init__(self, capacity=1000):
        self._capacity = capacity
        self._buckets = [[] for _ in range(capacity)]

    def _hash(self, key):
        return hash(key) % self._capacity

    def add(self, key):
        idx = self._hash(key)
        if key not in self._buckets[idx]:
            self._buckets[idx].append(key)

    def remove(self, key):
        idx = self._hash(key)
        if key in self._buckets[idx]:
            self._buckets[idx].remove(key)

    def contains(self, key):
        idx = self._hash(key)
        return key in self._buckets[idx]


def main():
    print("=" * 60)
    print("1. Happy Number Problem (Cycle Detection with HashSet)")
    print("=" * 60)
    numbers = [19, 2, 7, 4]
    for num in numbers:
        print(f"Number {num} is happy? {is_happy(num)}")

    print("\n" + "=" * 60)
    print("2. Built-in Set Operations")
    print("=" * 60)
    a = {1, 2, 3, 4, 5}
    b = {4, 5, 6, 7, 8}
    print("Set A:", a)
    print("Set B:", b)
    print("Union (A | B)               :", a | b)
    print("Intersection (A & B)        :", a & b)
    print("Difference (A - B)          :", a - b)
    print("Symmetric Difference (A ^ B):", a ^ b)

    print("\n" + "=" * 60)
    print("3. Custom SimpleHashSet Verification")
    print("=" * 60)
    custom_set = SimpleHashSet(capacity=16)
    for x in [10, 26, 42, 10]:  # 10, 26, 42 collide modulo 16
        custom_set.add(x)

    print("Contains 10:", custom_set.contains(10))
    print("Contains 26:", custom_set.contains(26))
    print("Contains 99:", custom_set.contains(99))
    custom_set.remove(10)
    print("After remove(10), contains 10:", custom_set.contains(10))
    print("Contains 26 still:", custom_set.contains(26))


if __name__ == "__main__":
    main()
