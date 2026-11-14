"""
Phase 6 - Data Structures and Algorithms
Section G: Hashing
Topic 01: Hash Tables
Example 01: Separate Chaining Hash Table with Dynamic Rehashing (Load Factor alpha <= 0.75)

How does a Hash Table achieve O(1) average-case `put`, `get`, and `remove`?
  1. **Hash Function (`_bucket_index(key)`):** Maps an arbitrary hashable `key` to an
     integer bucket index in `0 .. capacity - 1` via `hash(key) % capacity`.
  2. **Collision Resolution via Separate Chaining:** When two distinct keys map to the
     same bucket index, that bucket stores a short chain (list/linked-list) of
     `(key, value)` pairs.
  3. **Dynamic Rehashing (`load_factor = size / capacity > 0.75`):** To guarantee that
     the average chain length stays O(1), whenever `alpha > 0.75`, we double the
     bucket array capacity and re-hash every existing `(key, value)` pair into its
     new bucket!
"""

from typing import Any, Generic, List, Optional, Tuple, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class SeparateChainingHashTable(Generic[K, V]):
    """Hash Table with Separate Chaining collision resolution and dynamic 2x rehashing."""

    MAX_LOAD_FACTOR = 0.75

    def __init__(self, initial_capacity: int = 4) -> None:
        self._capacity: int = max(4, initial_capacity)
        self._buckets: List[List[Tuple[K, V]]] = [[] for _ in range(self._capacity)]
        self._size: int = 0
        self.rehash_count: int = 0

    @property
    def load_factor(self) -> float:
        return self._size / self._capacity

    def _bucket_index(self, key: K, cap: Optional[int] = None) -> int:
        target_cap = self._capacity if cap is None else cap
        # Mask with 0x7FFFFFFF for deterministic positive index
        return (hash(key) & 0x7FFFFFFF) % target_cap

    def _rehash(self, new_capacity: int) -> None:
        new_buckets: List[List[Tuple[K, V]]] = [[] for _ in range(new_capacity)]
        for chain in self._buckets:
            for k, v in chain:
                idx = self._bucket_index(k, new_capacity)
                new_buckets[idx].append((k, v))
        self._capacity = new_capacity
        self._buckets = new_buckets
        self.rehash_count += 1

    def put(self, key: K, value: V) -> None:
        """Inserts or updates `(key, value)` in average O(1) time."""
        idx = self._bucket_index(key)
        chain = self._buckets[idx]
        for i, (k, _) in enumerate(chain):
            if k == key:
                chain[i] = (key, value)
                return

        chain.append((key, value))
        self._size += 1
        if self.load_factor > self.MAX_LOAD_FACTOR:
            self._rehash(self._capacity * 2)

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """Retrieves the value for `key` in average O(1) time, or `default` if absent."""
        idx = self._bucket_index(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        return default

    def remove(self, key: K) -> bool:
        """Removes `key` if present in average O(1) time."""
        idx = self._bucket_index(key)
        chain = self._buckets[idx]
        for i, (k, _) in enumerate(chain):
            if k == key:
                # Swap-with-last removal inside chain in O(1)
                chain[i] = chain[-1]
                chain.pop()
                self._size -= 1
                return True
        return False

    def __len__(self) -> int:
        return self._size


if __name__ == "__main__":
    print("=" * 72)
    print("Separate Chaining Hash Table with Automatic 2x Rehashing (alpha <= 0.75)")
    print("=" * 72)

    ht: SeparateChainingHashTable[str, int] = SeparateChainingHashTable(initial_capacity=4)
    entries = [
        ("alice", 92),
        ("bob", 85),
        ("charlie", 78),
        ("diana", 96),
        ("evan", 88),
        ("fiona", 91),
        ("george", 84),
    ]

    for name, score in entries:
        ht.put(name, score)
        print(
            f"  put('{name:<7}', {score}) -> size={len(ht)}/{ht._capacity}, "
            f"alpha={ht.load_factor:.2f}, rehashes={ht.rehash_count}"
        )

    ht.put("bob", 99)  # Update existing key
    print(f"\nUpdated 'bob' -> get('bob') = {ht.get('bob')}, get('unknown', -1) = {ht.get('unknown', -1)}")
    print(f"remove('charlie') -> {ht.remove('charlie')}, new size = {len(ht)}")
    non_empty_chains = [len(b) for b in ht._buckets if b]
    print(f"Max chain length across {ht._capacity} buckets: {max(non_empty_chains)}")

