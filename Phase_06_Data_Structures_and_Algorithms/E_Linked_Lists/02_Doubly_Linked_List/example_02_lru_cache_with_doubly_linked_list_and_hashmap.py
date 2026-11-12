"""
Phase 6 - Data Structures and Algorithms
Section E: Linked Lists - Topic 02: Doubly Linked List
Example 02: O(1) LRU (Least Recently Used) Cache Powered by Doubly Linked List + Hash Map

Demonstrates:
1. The most famous real-world system-design & coding-interview application of a
   Doubly Linked List: **LRU Cache (LeetCode 146)**!
2. Why BOTH data structures are required for O(1) `get(key)` and O(1) `put(key, val)`:
   - Hash Map (`dict[key, DNode]`): jumps directly to the node in O(1) time.
   - Doubly Linked List: moves an accessed node to the Most-Recently-Used (MRU) front
     AND evicts the Least-Recently-Used (LRU) tail node in strictly O(1) time!
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class CacheNode:
    key: str
    value: int
    prev: CacheNode | None = None
    next: CacheNode | None = None


class LRUCache:
    """
    O(1) get and O(1) put Least-Recently-Used Cache using a Hash Map + Sentinel Doubly Linked List.
    - Front (right after `head_mru`) = Most Recently Used (MRU)
    - Back  (right before `tail_lru`) = Least Recently Used (LRU -> evicted first when full)
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be >= 1")
        self.capacity = capacity
        self.map: dict[str, CacheNode] = {}

        self.head_mru = CacheNode("", 0)
        self.tail_lru = CacheNode("", 0)
        self.head_mru.next = self.tail_lru
        self.tail_lru.prev = self.head_mru

    def _unlink(self, node: CacheNode) -> None:
        left, right = node.prev, node.next
        assert left is not None and right is not None
        left.next = right
        right.prev = left

    def _insert_at_mru_front(self, node: CacheNode) -> None:
        first = self.head_mru.next
        assert first is not None
        node.prev = self.head_mru
        node.next = first
        self.head_mru.next = node
        first.prev = node

    def get(self, key: str) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        # Move accessed node to MRU front in O(1)!
        self._unlink(node)
        self._insert_at_mru_front(node)
        return node.value

    def put(self, key: str, value: int) -> str | None:
        """Insert or update `(key, value)`. Returns evicted key if capacity was exceeded."""
        evicted_key: str | None = None
        if key in self.map:
            node = self.map[key]
            node.value = value
            self._unlink(node)
            self._insert_at_mru_front(node)
            return None

        if len(self.map) >= self.capacity:
            # Evict the Least Recently Used node sitting at `tail_lru.prev` in O(1)!
            lru_node = self.tail_lru.prev
            assert lru_node is not None and lru_node is not self.head_mru
            self._unlink(lru_node)
            del self.map[lru_node.key]
            evicted_key = lru_node.key

        new_node = CacheNode(key, value)
        self.map[key] = new_node
        self._insert_at_mru_front(new_node)
        return evicted_key

    def mru_to_lru_snapshot(self) -> list[tuple[str, int]]:
        items: list[tuple[str, int]] = []
        curr = self.head_mru.next
        while curr is not None and curr is not self.tail_lru:
            items.append((curr.key, curr.value))
            curr = curr.next
        return items


if __name__ == "__main__":
    print("=" * 72)
    print("1. O(1) LRU CACHE (DOUBLY LINKED LIST + HASH MAP, CAPACITY = 3)")
    print("=" * 72)

    cache = LRUCache(capacity=3)
    for k, v in [("user:1", 101), ("user:2", 202), ("user:3", 303)]:
        cache.put(k, v)
    print(f"After 3 puts (MRU -> LRU)   : {cache.mru_to_lru_snapshot()}")

    print(f"get('user:1') -> {cache.get('user:1')}         : {cache.mru_to_lru_snapshot()}")
    evicted = cache.put("user:4", 404)
    print(f"put('user:4', 404) [evicts {evicted}] : {cache.mru_to_lru_snapshot()}")

