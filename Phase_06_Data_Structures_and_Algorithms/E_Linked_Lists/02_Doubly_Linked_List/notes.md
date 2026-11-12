# Section E: Linked Lists — Topic 02: Doubly Linked List

## 1. Introduction

A **Doubly Linked List (DLL)** upgrades every node in a linked list to store **two directional pointers** alongside its data payload `val`:
1. **`next`:** Points to the successor node (toward the back/tail).
2. **`prev`:** Points to the predecessor node (toward the front/head).

```
[head_sentinel] <-> [ 10 ] <-> [ 20 ] <-> [ 30 ] <-> [tail_sentinel]
```

Adding that single `.prev` pointer unlocks two transformative capabilities that a Singly Linked List cannot perform in $O(1)$ time:
1. **$O(1)$ Tail Deletion (`pop_right` / `pop_back`):** Because the tail node knows its own `.prev` node, we never have to walk from `head` to find the second-to-last node!
2. **$O(1)$ Arbitrary Node Unlinking (`unlink_node(node)`):** Given a direct memory reference to **any** node in the list (even in the middle or at the tail!), we can splice it out in **strictly $O(1)$ time** (`node.prev.next = node.next; node.next.prev = node.prev`).

---

## 2. Why is it used?

1. **The Core Engine of $O(1)$ LRU & LFU Caches (Redis, OS Page Tables, Browser Caches):**
   In an **LRU (Least Recently Used) Cache**, every `get(key)` must promote the accessed item to the Most-Recently-Used (MRU) front in $O(1)$ time, and every cache-full `put(key, val)` must evict the Least-Recently-Used (LRU) tail item in $O(1)$ time. Combining a **Hash Map** (`key -> CacheNode`) with a **Sentinel-Bounded Doubly Linked List** is the universal industry standard for $O(1)$ caching!
2. **Python's `collections.OrderedDict` & Linux Kernel `struct list_head`:**
   Python's `OrderedDict.move_to_end(key)` and Linux kernel process/timer queues use Doubly Linked Lists for $O(1)$ insertion, reordering, and removal.
3. **Bidirectional Navigation (Undo/Redo Stacks & Browser History):**
   Stepping backward (`curr = curr.prev`) and forward (`curr = curr.next`) takes $O(1)$ per step, and visiting a new URL truncates the entire forward history in $O(1)$ by overwriting `curr.next = new_page`.

---

## 3. Syntax & Core Blueprints

### Blueprint 1: Sentinel-Bounded Doubly Linked List (Zero `None`-Check Branches!)
```python
class DListNode:
    def __init__(self, val: int = 0) -> None:
        self.val = val
        self.prev: "DListNode | None" = None
        self.next: "DListNode | None" = None

class DoublyLinkedList:
    def __init__(self) -> None:
        self.head_sentinel = DListNode(0)
        self.tail_sentinel = DListNode(0)
        self.head_sentinel.next = self.tail_sentinel
        self.tail_sentinel.prev = self.head_sentinel

    def _insert_between(self, node: DListNode, left: DListNode, right: DListNode) -> None:
        node.prev = left
        node.next = right
        left.next = node
        right.prev = node

    def unlink(self, node: DListNode) -> None:
        left, right = node.prev, node.next
        left.next = right
        right.prev = left
```

---

## 4. Step-by-Step Explanation & Complexity Analysis

### Why Two Dummy Sentinels (`head_sentinel` and `tail_sentinel`) Are Best Practice
In a naive Doubly Linked List where `head` and `tail` can be `None`, every insertion and deletion has to check 4 edge cases:
- Is the list empty (`head is None`)?
- Are we deleting the `head` (`node.prev is None`)?
- Are we deleting the `tail` (`node.next is None`)?
- Is there only 1 element (`head is tail`)?

By allocating two permanent guard nodes `head_sentinel <-> tail_sentinel` at initialization:
- Every real data node is **guaranteed** to sit strictly between two non-`None` neighbors (`left` and `right`).
- `append_left(x)` is simply `_insert_between(x, head_sentinel, head_sentinel.next)`.
- `append_right(x)` is simply `_insert_between(x, tail_sentinel.prev, tail_sentinel)`.
- `unlink(node)` is **always** two lines (`node.prev.next = node.next; node.next.prev = node.prev`) with zero `if` branches!

### Complexity Comparison

| Operation | Singly Linked List | Doubly Linked List | Trade-off |
| :--- | :--- | :--- | :--- |
| **`append_left` / `pop_left`** | $O(1)$ | $O(1)$ | Tie |
| **`append_right` (at Tail)** | $O(1)$ | $O(1)$ | Tie |
| **`pop_right` (Delete Tail)** | $O(N)$ | **$O(1)$** | DLL wins ($O(1)$ via `tail.prev`) |
| **Unlink Arbitrary `node` by Reference** | $O(N)$ (need `prev`) | **$O(1)$** | DLL wins (enables $O(1)$ LRU Cache!) |
| **Memory per Node** | 1 pointer (`next`) | 2 pointers (`prev`, `next`) | DLL uses 8 extra bytes/node on 64-bit |

---

## 5. Practical Examples (3 Complete Programs)

### Example 1: Sentinel-Bounded Doubly Linked List Operations (`example_01_sentinel_doubly_linked_list_operations.py`)
```python
    def _insert_between(
        self, val: int, left_node: DListNode, right_node: DListNode
    ) -> DListNode:
        node = DListNode(val, prev=left_node, next=right_node)
        left_node.next = node
        right_node.prev = node
        self._size += 1
        return node

    def unlink_node(self, node: DListNode) -> int:
        left_node = node.prev
        right_node = node.next
        assert left_node is not None and right_node is not None
        left_node.next = right_node
        right_node.prev = left_node
        node.prev = node.next = None
        self._size -= 1
        return node.val
```

### Example 2: $O(1)$ LRU Cache (`example_02_lru_cache_with_doubly_linked_list_and_hashmap.py`)
```python
    def get(self, key: str) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._unlink(node)
        self._insert_at_mru_front(node)
        return node.value

    def put(self, key: str, value: int) -> str | None:
        if key in self.map:
            node = self.map[key]
            node.value = value
            self._unlink(node)
            self._insert_at_mru_front(node)
            return None

        if len(self.map) >= self.capacity:
            lru_node = self.tail_lru.prev
            assert lru_node is not None and lru_node is not self.head_mru
            self._unlink(lru_node)
            del self.map[lru_node.key]
```

### Example 3: Browser History & Flattening a Multilevel Doubly Linked List (`example_03_browser_history_and_flatten_multilevel_dll.py`)
```python
def flatten_multilevel_dll(head: MultiLevelDNode | None) -> list[int]:
    curr = head
    while curr is not None:
        if curr.child is not None:
            child_head = curr.child
            child_tail = child_head
            while child_tail.next is not None:
                child_tail = child_tail.next

            orig_next = curr.next
            curr.next = child_head
            child_head.prev = curr
            curr.child = None

            if orig_next is not None:
                child_tail.next = orig_next
                orig_next.prev = child_tail

        curr = curr.next
```

---

## 6. Verified Console Output

### Output of `example_01_sentinel_doubly_linked_list_operations.py`
```text
========================================================================
1. SENTINEL-BOUNDED DOUBLY LINKED LIST O(1) OPERATIONS
========================================================================
Forward Traversal      : [10, 20, 30, 40] (len=4)
Backward Traversal     : [40, 30, 20, 10]
After O(1) unlink(n30) : [10, 20, 40]
After O(1) pop_right() -> 40: [10, 20]
```

### Output of `example_02_lru_cache_with_doubly_linked_list_and_hashmap.py`
```text
========================================================================
1. O(1) LRU CACHE (DOUBLY LINKED LIST + HASH MAP, CAPACITY = 3)
========================================================================
After 3 puts (MRU -> LRU)   : [('user:3', 303), ('user:2', 202), ('user:1', 101)]
get('user:1') -> 101         : [('user:1', 101), ('user:3', 303), ('user:2', 202)]
put('user:4', 404) [evicts user:2] : [('user:4', 404), ('user:1', 101), ('user:3', 303)]
```

### Output of `example_03_browser_history_and_flatten_multilevel_dll.py`
```text
========================================================================
1. BROWSER HISTORY NAVIGATION (LEETCODE 1472)
========================================================================
back(2)                -> github.com
forward(1)             -> leetcode.com
visit('peps...'), forward(2) -> peps.python.org (Forward history cleared!)
back(2)                -> github.com

========================================================================
2. FLATTEN A MULTILEVEL DOUBLY LINKED LIST IN O(1) SPACE (LC 430)
========================================================================
Flattened Multilevel Chain: [1, 2, 4, 5, 3]
```

---

## 7. Code Explanation

1. **Why `CacheNode` in LRU Cache Must Store BOTH `key` AND `value`:**
   Interviewers always check whether you include `key` inside `CacheNode`! Why? When the cache is full and you evict `lru_node = self.tail_lru.prev` in $O(1)$ time, you must also delete its entry from the dictionary (`del self.map[lru_node.key]`). If `CacheNode` only stored `value`, you wouldn't know which dictionary key to delete without an $O(N)$ scan of `self.map`!
2. **Why `flatten_multilevel_dll` Handles Nested Children of Children Iteratively in $O(1)$ Space:**
   When we splice `curr`'s immediate `.child` list right between `curr` and `curr.next`, the main loop's next step is `curr = curr.next` — which steps **directly into the newly spliced child list**! If any node inside that child list has its own `.child` (grandchild), the exact same loop will encounter and splice it in on the way!

---

## 8. Common Mistakes

1. **Updating Only 2 Pointers Instead of 4 During Insertion:**
   Inserting `node` between `left` and `right` in a Doubly Linked List requires wiring **4 pointers**: `node.prev = left`, `node.next = right`, `left.next = node`, and `right.prev = node`. Forgetting `right.prev = node` leaves forward traversal looking fine while corrupting backward traversal and future `unlink` calls!
2. **Forgetting to Clear `curr.child = None` When Flattening a Multilevel DLL:**
   LeetCode 430's judge verifies that all `.child` pointers in the returned flattened list are `None`. Always set `curr.child = None` after splicing.

---

## 9. Practice Questions

1. **Easy — Reverse a Doubly Linked List In-Place:** Given the `head` of a Doubly Linked List, reverse it in-place in $O(N)$ time and $O(1)$ space by swapping `curr.prev, curr.next = curr.next, curr.prev` on every node.
2. **Medium — Design a Text Editor with a Cursor (LeetCode 2296):** Implement `addText(text)`, `deleteText(k)`, `cursorLeft(k)`, and `cursorRight(k)` using a Doubly Linked List (or two stacks `left_chars` and `right_chars`) where all cursor operations take $O(k)$ time independent of total document length $N$.
3. **Hard — LFU (Least Frequently Used) Cache in $O(1)$ Time (LeetCode 460):** Combine `key_to_node` Hash Map, `freq_to_dll` Hash Map of Doubly Linked Lists (one DLL per frequency count), and `min_freq` integer tracker to achieve strictly $O(1)$ `get` and `put` with LFU + LRU tie-breaking!

---

## 10. Interview Questions

### Q1: In Python, how does `collections.OrderedDict` allow you to implement an LRU Cache in 10 lines, and Why do interviewers still ask you to build `DListNode` + `dict` from scratch?
**Answer:**
Under the hood, CPython's `OrderedDict` **is** a Hash Table combined with a circular Doubly Linked List in C! Its methods `move_to_end(key, last=True)` and `popitem(last=False)` execute the exact same $O(1)$ pointer unlinking and relinking. Interviewers ask you to implement `CacheNode` + sentinel DLL from scratch to test whether you understand pointer invariants and why a plain array + dict cannot achieve $O(1)$ middle promotion.

### Q2: How does an XOR Linked List store a Doubly Linked List using only ONE pointer field per node in C/C++?
**Answer:**
Instead of storing two 8-byte pointers (`prev` and `next`), each node stores a single bitwise XOR of the two memory addresses: `link = address(prev) ^ address(next)`. When traversing forward from `prev` to `curr`, you compute `address(next) = address(prev) ^ curr.link`! (This is not used in garbage-collected languages like Python or Java because GC requires real object references to trace reachability.)

