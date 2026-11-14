# Hashing Problems

## 1. Introduction

Advanced **Hashing Problems** encompass complex design patterns, system cache architectures, graph and linked data structure cloners, and algorithmic search space reductions.

These problems represent classic engineering interview scenarios where hash maps serve not merely as simple lookup structures, but as components in composite data structures (such as **LRU Cache** using Hash Maps paired with Doubly Linked Lists) or strategic algorithmic pivots (such as **Meet-in-the-Middle** in 4Sum II, and object-graph cloning in Copy List with Random Pointer).

---

## 2. Why Use Hashing for Advanced Problems?

| Problem | Naive Complexity | Hash-Optimized Complexity | Architectural Role of Hash Map |
|---|---|---|---|
| **LRU Cache** | $O(n)$ search / update | $O(1)$ `get` & `put` | Maps key directly to Doubly Linked List node |
| **4Sum II** | $O(n^4)$ brute force | $O(n^2)$ time & space | Meet-in-the-Middle frequency table of pairwise sums |
| **Copy List with Random Pointer** | $O(n^2)$ searching random | $O(n)$ time & space | Maps original `Node` instance $\to$ clone `Node` instance |
| **Minimum Window Substring** | $O(n^2)$ substring validation | $O(n)$ sliding window | Character requirement vs window frequency balance |
| **LFU Cache** | $O(n)$ eviction | $O(1)$ operations | Frequency hash map + doubly linked buckets |

---

## 3. Syntax / Architectural Skeletons

### LRU Cache Architecture (Hash Map + Doubly Linked List)

```python
class DLinkedNode:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> DLinkedNode
        self.head = DLinkedNode()  # Dummy MRU
        self.tail = DLinkedNode()  # Dummy LRU
        self.head.next = self.tail
        self.tail.prev = self.head
```

### Meet-in-the-Middle Hashing

```python
# Split 4-way search space into two pairwise 2-way tables
sum_ab = Counter(a + b for a in A for b in B)
total = sum(sum_ab[- (c + d)] for c in C for d in D if -(c + d) in sum_ab)
```

---

## 4. Key Algorithmic Patterns

### 1. Composite Data Structure: Hash Map + Doubly Linked List
- **Hash Map** provides $O(1)$ key lookup returning the linked list node reference.
- **Doubly Linked List** allows $O(1)$ removal and head-insertion without array shifting.
- Together, they achieve $O(1)$ time for both cache hits (`get`) and cache evictions (`put`).

### 2. Meet in the Middle
When evaluating 4 arrays of size $n$, computing all combinations requires $O(n^4)$. By computing all pairwise sums of the first two arrays into a hash table ($O(n^2)$), we can iterate over the second pair ($O(n^2)$) and check for the negated complement in $O(1)$, cutting complexity from quartic to quadratic.

### 3. Object-Graph Cloning via Identity Hashing
To clone complex structures with cycles or arbitrary pointer graphs (like linked lists with random pointers or general directed graphs), maintain a `visited` or `clone_map` dictionary:
```python
clone_map = {old_node: Node(old_node.val)}
clone_map[old_node].next = clone_map.get(old_node.next)
clone_map[old_node].random = clone_map.get(old_node.random)
```

---

## 5. Examples

### Example 1: 4Sum II (Meet in the Middle) & Minimum Window Substring
```python
def four_sum_count(nums1, nums2, nums3, nums4):
    sum_ab = defaultdict(int)
    for a in nums1:
        for b in nums2:
            sum_ab[a + b] += 1

    count = 0
    for c in nums3:
        for d in nums4:
            count += sum_ab.get(-(c + d), 0)
    return count
```

### Example 2: Copy List with Random Pointer
```python
def copy_random_list(head):
    if not head:
        return None
    clone_map = {}
    curr = head
    while curr:
        clone_map[curr] = Node(curr.val)
        curr = curr.next

    curr = head
    while curr:
        if curr.next:
            clone_map[curr].next = clone_map[curr.next]
        if curr.random:
            clone_map[curr].random = clone_map[curr.random]
        curr = curr.next
    return clone_map[head]
```

### Example 3: LRU Cache Implementation
```python
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head, self.tail = DLinkedNode(), DLinkedNode()
        self.head.next = self.tail
        self.tail.prev = self.head

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
            node = DLinkedNode(key, value)
            self.cache[key] = node
            self._add_to_head(node)
            if len(self.cache) > self.capacity:
                tail = self._pop_tail()
                del self.cache[tail.key]
```

---

## 6. Output

```
1. 4Sum II:
   Tuples summing to 0: 2

2. Minimum Window Substring:
   s = 'ADOBECODEBANC', t = 'ABC' -> 'BANC'

3. Copy List with Random Pointer:
   Original and Cloned structures match identically.
   Distinct objects in memory: True

4. LRU Cache:
   put(1, 100), put(2, 200)
   get(1) -> 100
   put(3, 300) -> evicts key 2
   get(2) -> -1
```

---

## 7. Code Explanation

| Mechanism | Purpose |
|---|---|
| `DLinkedNode` sentinels | `head` and `tail` dummy nodes eliminate boundary null-checks during insertions/deletions |
| `cache[key] = node` | Direct pointer mapping allows $O(1)$ lookup before unlinking node from doubly linked list |
| `sum_ab[a + b] += 1` | Compresses first half of combinatorial space into frequency map |
| `clone_map[curr]` | Python uses object `id()` as default hash for class instances, enabling identity-based cloning |
| Interleaved list clone | Alternative $O(1)$ space method placing clone $A'$ immediately after original $A$ |

---

## 8. Common Mistakes

1. **Forgetting to Update LRU on Cache Hit (`get`)**:
   A `get` operation counts as an access! The accessed node must be moved to the head (most recently used).
2. **Deleting Wrong Node from Cache Map on Eviction**:
   When evicting the LRU tail, you must delete `tail.key` from `self.cache`, not an arbitrary key.
3. **Circular Graph Deep Copy Traps**:
   Not using a memoization hash map when cloning graphs causes infinite recursion on cyclic references.
4. **Incorrect Target Window Contraction**:
   Shrinking the sliding window in Minimum Window Substring without decrementing `formed` count when a critical character count falls below requirement.
5. **Memory Leaks from Unlinked Nodes**:
   In languages without garbage collection (or cyclic references), failing to properly sever `prev` and `next` pointers leaves dangling nodes.

---

## 9. Practice Questions

1. Implement an **LFU Cache (Least Frequently Used)** with $O(1)$ get and put using frequency hash maps and doubly linked bucket chains.
2. Clone an arbitrary Undirected Graph using BFS/DFS with an identity hash map.
3. Solve **Insert Delete GetRandom O(1) - Duplicates allowed** using an array and a hash map of index sets.
4. Design an In-Memory File System supporting `ls`, `mkdir`, `addContentToFile`, and `readContentFromFile` using trie/hash maps.
5. Implement **Max Points on a Line** in $O(n^2)$ using fractional slope hashing with greatest common divisors (GCD).

---

## 10. Interview Questions

**Q1: Why does an LRU Cache require a Doubly Linked List instead of a Singly Linked List?**
To remove a node in $O(1)$ time when moving it to the head, we must update its predecessor's pointer (`prev.next = next`). A singly linked list would require an $O(n)$ traversal from the head to locate the preceding node.

**Q2: How does `collections.OrderedDict` implement LRU eviction in Python?**
`OrderedDict` internally maintains a doubly linked list over its hash table keys. Calling `move_to_end(key)` adjusts node pointers in $O(1)$, and `popitem(last=False)` pops the oldest item in $O(1)$.

**Q3: Can `copy_random_list` be done in $O(1)$ auxiliary space?**
Yes, by interleaving cloned nodes into the original list (`A -> A' -> B -> B'`), copying random pointers via `curr.next.random = curr.random.next`, and then separating the interleaved lists.

**Q4: How does slope hashing work in Max Points on a Line without floating-point precision errors?**
Instead of storing floating-point division `dy / dx`, divide both by their greatest common divisor $\text{gcd}(\Delta y, \Delta x)$ and store the normalized reduced integer tuple `(dy // g, dx // g)` as the hash map key.

**Q5: What is the space-time trade-off in 4Sum II?**
Brute force takes $O(n^4)$ time and $O(1)$ space. Splitting $2 + 2$ takes $O(n^2)$ time and $O(n^2)$ auxiliary space. Splitting $3 + 1$ would take $O(n^3)$ time and $O(n)$ space.
