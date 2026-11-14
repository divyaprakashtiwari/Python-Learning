"""
Phase 6 - Section G.05: Hashing Problems
Example 03: LRU Cache Implementation

Demonstrating:
1. LRU (Least Recently Used) Cache using Doubly Linked List + Hash Map (O(1) get & put).
2. Pythonic LRU Cache using collections.OrderedDict.
"""

from collections import OrderedDict


class DLinkedNode:
    """Doubly linked list node storing key and value."""
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """
    LRU Cache using Hash Map + Doubly Linked List.
    get(key) -> O(1)
    put(key, value) -> O(1)
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> DLinkedNode
        # Sentinel dummy head and tail
        self.head = DLinkedNode()
        self.tail = DLinkedNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node_to_head(self, node: DLinkedNode):
        """Insert node immediately after dummy head."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: DLinkedNode):
        """Unlink an existing node from the list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _move_to_head(self, node: DLinkedNode):
        """Move an accessed node to the most recently used (head) position."""
        self._remove_node(node)
        self._add_node_to_head(node)

    def _pop_tail(self) -> DLinkedNode:
        """Evict the least recently used node (before dummy tail)."""
        res = self.tail.prev
        self._remove_node(res)
        return res

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._move_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            new_node = DLinkedNode(key, value)
            self.cache[key] = new_node
            self._add_node_to_head(new_node)
            if len(self.cache) > self.capacity:
                tail = self._pop_tail()
                del self.cache[tail.key]


class LRUCacheOrderedDict:
    """Pythonic LRU Cache using collections.OrderedDict."""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Pop oldest (FIFO end)


def main():
    print("=" * 60)
    print("1. Custom LRU Cache (Hash Map + Doubly Linked List)")
    print("=" * 60)
    lru = LRUCache(2)
    lru.put(1, 100)
    lru.put(2, 200)
    print("get(1)    :", lru.get(1))    # returns 100, marks 1 as most recent
    lru.put(3, 300)                    # evicts key 2 (least recently used)
    print("get(2)    :", lru.get(2))    # returns -1 (evicted)
    lru.put(4, 400)                    # evicts key 1
    print("get(1)    :", lru.get(1))    # returns -1 (evicted)
    print("get(3)    :", lru.get(3))    # returns 300
    print("get(4)    :", lru.get(4))    # returns 400

    print("\n" + "=" * 60)
    print("2. Pythonic OrderedDict LRU Cache Verification")
    print("=" * 60)
    py_lru = LRUCacheOrderedDict(2)
    py_lru.put(1, 100)
    py_lru.put(2, 200)
    print("py_lru.get(1):", py_lru.get(1))
    py_lru.put(3, 300)
    print("py_lru.get(2):", py_lru.get(2))
    py_lru.put(4, 400)
    print("py_lru.get(1):", py_lru.get(1))
    print("py_lru.get(3):", py_lru.get(3))
    print("py_lru.get(4):", py_lru.get(4))


if __name__ == "__main__":
    main()
