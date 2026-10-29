"""
Question 7: Separate Chaining Hash Map from First Principles
Topic: Data Structures & Algorithms (DSA)

Key Concepts Tested:
- Custom Hash Map implementation without built-in dict or set
- Collision resolution via Separate Chaining (singly linked bucket chains)
- Modulo hashing with abs(hash(key)) % capacity
- Dynamic rehashing & table doubling when load factor exceeds threshold
- Introspection: load factor and collision metrics
"""

from typing import TypeVar, Generic, Optional, List, Any

K = TypeVar("K")
V = TypeVar("V")


class HashNode(Generic[K, V]):
    """Linked node within a hash table bucket chain."""

    def __init__(self, key: K, value: V, next_node: Optional["HashNode[K, V]"] = None) -> None:
        self.key = key
        self.value = value
        self.next = next_node

    def __repr__(self) -> str:
        return f"HashNode({self.key}: {self.value})"


class SeparateChainingHashMap(Generic[K, V]):
    """
    Complete Hash Map built from first principles using separate chaining
    and dynamic table resizing.
    """

    def __init__(self, initial_capacity: int = 8, max_load_factor: float = 0.75) -> None:
        if initial_capacity <= 0:
            raise ValueError("Initial capacity must be positive")
        self._capacity = initial_capacity
        self._max_load_factor = max_load_factor
        self._size = 0
        self._buckets: List[Optional[HashNode[K, V]]] = [None] * self._capacity

    @property
    def capacity(self) -> int:
        return self._capacity

    def load_factor(self) -> float:
        return round(self._size / self._capacity, 4)

    def _hash(self, key: K) -> int:
        return abs(hash(key)) % self._capacity

    def put(self, key: K, value: V) -> None:
        """
        Inserts or updates a key-value pair.
        Rehashes if load factor exceeds max_load_factor.
        """
        index = self._hash(key)
        curr = self._buckets[index]

        # 1. Update existing key in chain
        while curr:
            if curr.key == key:
                curr.value = value
                return
            curr = curr.next

        # 2. Insert new key at the head of the bucket chain
        new_node = HashNode(key, value, next_node=self._buckets[index])
        self._buckets[index] = new_node
        self._size += 1

        # 3. Dynamic resizing check
        if (self._size / self._capacity) > self._max_load_factor:
            self._resize(self._capacity * 2)

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """
        Retrieves the value for key, or default if absent.
        """
        index = self._hash(key)
        curr = self._buckets[index]
        while curr:
            if curr.key == key:
                return curr.value
            curr = curr.next
        return default

    def remove(self, key: K) -> V:
        """
        Deletes key-value pair and returns value.
        Raises KeyError if key is not found.
        """
        index = self._hash(key)
        curr = self._buckets[index]
        prev: Optional[HashNode[K, V]] = None

        while curr:
            if curr.key == key:
                if prev is None:
                    self._buckets[index] = curr.next
                else:
                    prev.next = curr.next
                self._size -= 1
                return curr.value
            prev = curr
            curr = curr.next

        raise KeyError(f"Key '{key}' not found in hash map")

    def __contains__(self, key: K) -> bool:
        index = self._hash(key)
        curr = self._buckets[index]
        while curr:
            if curr.key == key:
                return True
            curr = curr.next
        return False

    def __len__(self) -> int:
        return self._size

    def collision_count(self) -> int:
        """Counts nodes stored beyond the primary head node across all buckets."""
        collisions = 0
        for head in self._buckets:
            if head and head.next:
                curr = head.next
                while curr:
                    collisions += 1
                    curr = curr.next
        return collisions

    def _resize(self, new_capacity: int) -> None:
        """Doubles capacity and rehashes all active entries."""
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [None] * new_capacity
        self._size = 0  # Re-populated via put()

        for head in old_buckets:
            curr = head
            while curr:
                self.put(curr.key, curr.value)
                curr = curr.next


if __name__ == "__main__":
    hash_map = SeparateChainingHashMap[str, int](initial_capacity=4, max_load_factor=0.75)

    print("=== 1. Insertion & Load Factor Tracking ===")
    hash_map.put("apple", 100)
    hash_map.put("banana", 200)
    hash_map.put("cherry", 300)  # size = 3, load factor = 3/4 = 0.75 (at threshold)

    lf_before = hash_map.load_factor()
    cap_before = hash_map.capacity
    print(f"Load Factor Before Resizing: {lf_before} (Capacity: {cap_before})")

    # Adding 4th item triggers resizing (4/4 = 1.0 > 0.75)
    hash_map.put("date", 400)
    lf_after = hash_map.load_factor()
    cap_after = hash_map.capacity
    print(f"Load Factor After Resizing: {lf_after} (Capacity: {cap_after})")

    print("\n=== 2. Retrieval & In-Place Update ===")
    val_banana = hash_map.get("banana")
    print(f"Retrieved Banana Value: {val_banana}")

    hash_map.put("banana", 250)  # Update existing key
    updated_banana = hash_map.get("banana")
    print(f"Updated Banana Value: {updated_banana}")
    print(f"Total size after update: {len(hash_map)} (size unchanged)")

    print("\n=== 3. Removal & Membership Verification ===")
    removed_val = hash_map.remove("apple")
    has_apple = "apple" in hash_map
    print(f"Removed Apple Value: {removed_val}")
    print(f"Contains Apple After Removal: {has_apple}")

    print("\n=== 4. Key Absence & Introspection ===")
    print(f"Non-existent key default: {hash_map.get('non_existent', default=-1)}")
    print(f"Current Collision Count: {hash_map.collision_count()}")

    try:
        hash_map.remove("ghost_key")
    except KeyError as err:
        print(f"Caught expected KeyError: {err}")
