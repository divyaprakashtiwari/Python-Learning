# Hash Tables

## 1. Introduction

A **hash table** (also called a hash map) is a data structure that maps keys to values using a **hash function**. It provides average-case O(1) time complexity for insert, delete, and lookup operations, making it one of the most powerful and commonly used data structures in computer science.

The core idea: transform a key into an integer **index** (via hashing) and store the value at that index in an underlying array. Because multiple keys can hash to the same index (a **collision**), hash tables must include a collision-resolution strategy.

---

## 2. Why Use Hash Tables?

| Scenario | Why Hash Table Wins |
|---|---|
| Fast key-value lookup | O(1) average vs O(log n) for BST |
| Counting frequencies | Accumulate counts in one pass |
| Deduplication / membership | O(1) contains check |
| Caching / memoization | Store computed results by key |
| Graph adjacency lists | Nodes mapped to neighbour lists |
| Index building (databases) | Record lookup without full scan |

Python's built-in `dict` and `set` are hash tables under the hood.

---

## 3. Syntax / API

### Python Built-in dict (Hash Map)

```python
# Create
table = {}
table = dict()

# Insert / Update
table[key] = value

# Lookup
value = table[key]          # raises KeyError if missing
value = table.get(key, default)

# Delete
del table[key]

# Membership
key in table                # O(1) average

# Iterate
for k, v in table.items():
    pass
```

### Custom Hash Table (class skeleton)

```python
class HashTable:
    def __init__(self, capacity=16):
        self._capacity = capacity
        self._buckets  = [[] for _ in range(capacity)]
        self._size     = 0

    def _hash(self, key):
        return hash(key) % self._capacity

    def put(self, key, value): ...
    def get(self, key): ...
    def remove(self, key): ...
```

---

## 4. How Hash Tables Work

### Step-by-Step

1. **Hash function**: `index = hash(key) % capacity`
2. **Store**: place `(key, value)` at `buckets[index]`
3. **Retrieve**: recompute index, scan bucket for matching key
4. **Collision**: two keys map to same index — resolved by one of:

### Collision Resolution Strategies

#### Separate Chaining
Each bucket holds a **linked list** (or Python list) of `(key, value)` pairs.

```
bucket[3] -> [(key_a, val_a), (key_b, val_b)]
```

- **Pros**: Simple, handles high load factors gracefully
- **Cons**: Extra memory for pointers; cache-unfriendly

#### Open Addressing (Linear Probing)
If `bucket[i]` is taken, try `bucket[(i+1) % cap]`, `(i+2) % cap`, ...

- **Pros**: Cache-friendly (contiguous array)
- **Cons**: Clustering; requires tombstones for deletion

#### Quadratic Probing / Double Hashing
Variants of open addressing that reduce clustering.

### Load Factor and Rehashing

```
load_factor = size / capacity
```

When `load_factor > threshold` (commonly 0.75), **rehash**: allocate a new array of double capacity and re-insert all entries.

- Rehashing is O(n) but amortised over n insertions → O(1) amortised per insert

---

## 5. Examples

### Example 1: Separate Chaining Hash Table

```python
class HashTable:
    def __init__(self, capacity=8, load_limit=0.75):
        self._cap    = capacity
        self._limit  = load_limit
        self._data   = [[] for _ in range(capacity)]
        self._size   = 0

    def _hash(self, key):
        return hash(key) % self._cap

    def put(self, key, value):
        idx = self._hash(key)
        for i, (k, _) in enumerate(self._data[idx]):
            if k == key:
                self._data[idx][i] = (key, value)
                return
        self._data[idx].append((key, value))
        self._size += 1
        if self._size / self._cap > self._limit:
            self._rehash()

    def get(self, key, default=None):
        for k, v in self._data[self._hash(key)]:
            if k == key:
                return v
        return default

    def _rehash(self):
        old = self._data
        self._cap *= 2
        self._data = [[] for _ in range(self._cap)]
        self._size = 0
        for bucket in old:
            for k, v in bucket:
                self.put(k, v)
```

### Example 2: Open Addressing with Tombstones

```python
_DELETED = object()   # sentinel for tombstones

class OpenHashTable:
    def __init__(self, capacity=8):
        self._cap   = capacity
        self._slots = [None] * capacity
        self._size  = 0

    def _hash(self, key):
        return hash(key) % self._cap

    def put(self, key, value):
        i = self._hash(key)
        while self._slots[i] not in (None, _DELETED):
            if self._slots[i][0] == key:
                self._slots[i] = (key, value)
                return
            i = (i + 1) % self._cap
        self._slots[i] = (key, value)
        self._size += 1

    def get(self, key, default=None):
        i = self._hash(key)
        while self._slots[i] is not None:
            if self._slots[i] is not _DELETED and self._slots[i][0] == key:
                return self._slots[i][1]
            i = (i + 1) % self._cap
        return default

    def remove(self, key):
        i = self._hash(key)
        while self._slots[i] is not None:
            if self._slots[i] is not _DELETED and self._slots[i][0] == key:
                self._slots[i] = _DELETED
                self._size -= 1
                return True
            i = (i + 1) % self._cap
        return False
```

### Example 3: Hash and Equality Contract

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))   # consistent with __eq__

p1 = Point(1, 2)
p2 = Point(1, 2)
d = {p1: "origin-offset"}
print(d[p2])    # "origin-offset" -- works because hash and eq agree
```

---

## 6. Output

```
# Separate Chaining
ht.put("apple", 5)
ht.put("banana", 3)
print(ht.get("apple"))   # 5
print(ht.get("cherry"))  # None

# Open Addressing
oht.put("x", 10)
oht.remove("x")
print(oht.get("x"))      # None

# Custom __hash__
print(d[Point(1, 2)])    # origin-offset
```

---

## 7. Code Explanation

| Concept | Detail |
|---|---|
| `hash(key) % cap` | Maps key to bucket index; built-in `hash()` returns a machine-sized int |
| Separate chaining | Bucket = list of (k, v) pairs; scan linearly within bucket |
| Open addressing | Probe sequence fills empty slots; tombstones mark deleted entries |
| Load factor 0.75 | Empirical sweet spot between space and performance |
| Rehashing | Doubles capacity, re-hashes all keys; keeps load factor low |
| `__hash__` / `__eq__` | Must be consistent: if `a == b` then `hash(a) == hash(b)` |
| Tombstone | Placeholder for deleted slot so probe chains are not broken |

---

## 8. Common Mistakes

1. **Mutable keys**: lists, dicts, sets are unhashable — use tuples or frozensets.
2. **Missing tombstones**: removing a slot in open addressing can break lookup chains.
3. **Wrong `__hash__`/`__eq__` contract**: if two equal objects have different hashes, dict lookups fail silently.
4. **Never rehashing**: letting load factor exceed 1.0 causes O(n) operations or infinite loops.
5. **Modifying a dict while iterating**: raises `RuntimeError`; iterate over a copy instead.
6. **Assuming insertion order before Python 3.7**: dicts are ordered since 3.7, but do not rely on it for logic.

---

## 9. Practice Questions

1. Implement a hash table from scratch using separate chaining with dynamic resizing at load factor 0.75.
2. Implement the same using open addressing with linear probing and tombstones.
3. Write a `MinHashTable` that also supports `get_min()` in O(1) time.
4. Given a list of words, use a hash table to count frequency of each word.
5. Design a hash table that supports `put`, `get`, `remove`, and `get_random_key` all in O(1) average.

---

## 10. Interview Questions

**Q1: What is the average and worst-case time complexity of hash table operations?**
Average O(1) for insert/delete/lookup; worst case O(n) when all keys collide into one bucket (poor hash function or adversarial input).

**Q2: What is a hash collision and how is it handled?**
Two keys produce the same index. Common strategies: separate chaining (each bucket holds a list) and open addressing (probe for the next empty slot).

**Q3: Why do we need tombstones in open addressing?**
Deletion cannot simply clear a slot because that would break probe chains and cause lookups for later-inserted keys to terminate prematurely, returning incorrect "not found" results.

**Q4: What are the properties of a good hash function?**
Deterministic, uniform distribution, fast to compute, avalanche effect (small change in key causes large change in hash), and minimal collisions.

**Q5: How does Python's dict differ from a standard hash map?**
Python dicts maintain insertion order (since 3.7), use an optimised open-addressing scheme (compact tables with indices array), and are optimised for the common case of string keys.

**Q6: When would you prefer a BST-based map over a hash map?**
When you need ordered iteration, range queries, or guaranteed O(log n) worst case (hash tables degrade to O(n) under hash collision attacks).
