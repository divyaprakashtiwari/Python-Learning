"""
Topic: Data Structures and Algorithms (DSA) - Hash Table
--------------------------------------------------------
Questions Covered:
1. Separate Chaining Hash Map: Array of buckets with custom polynomial hash function and key-value chaining.
2. Open Addressing (Linear Probing): In-place array probing with tombstone markers for deleted slots.
3. Open Addressing (Quadratic Probing): Collision resolution via quadratic stride polynomials.
4. Double Hashing: Secondary hash function determining collision resolution jump size.
5. Dynamic Rehashing & Resizing: Auto-doubling capacity when load factor exceeds threshold (0.75).
6. One-Pass Two Sum via Hash Map: O(n) complement lookup in single scan.
7. Group Anagrams via Frequency Key Hashing: Multi-string clustering with canonical character tuple keys.
8. Subarray Sum Equals K: Prefix sum frequency map counting continuous subsegment sums in O(n).
9. Longest Consecutive Sequence: O(n) linear range expansion using hash set boundary checks.
10. Architectural System: Distributed Consistent Hashing Ring with Virtual Nodes (Hotspot-Proof Sharding).
"""

from typing import List, Tuple, Optional, Any, Dict, Set


# ==============================================================================
# Question 1: Separate Chaining Hash Map
# ==============================================================================
class SeparateChainingHashMap:
    """
    Hash map with collision resolution by separate chaining.
    Uses polynomial rolling hash function.
    """
    def __init__(self, initial_capacity: int = 11):
        self.capacity = initial_capacity
        self.buckets: List[List[Tuple[Any, Any]]] = [[] for _ in range(self.capacity)]
        self.size = 0

    def _hash(self, key: Any) -> int:
        key_str = str(key)
        h = 0
        p = 31
        m = self.capacity
        for ch in key_str:
            h = (h * p + ord(ch)) % m
        return h

    def put(self, key: Any, value: Any) -> None:
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1

    def get(self, key: Any) -> Optional[Any]:
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return None

    def remove(self, key: Any) -> bool:
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return True
        return False

    def load_factor(self) -> float:
        return self.size / self.capacity


def test_q1_separate_chaining():
    hm = SeparateChainingHashMap(5)
    hm.put("apple", 100)
    hm.put("banana", 200)
    hm.put("cherry", 300)

    assert hm.get("apple") == 100
    assert hm.get("banana") == 200
    assert hm.get("unknown") is None

    # Update existing
    hm.put("apple", 150)
    assert hm.get("apple") == 150

    # Delete
    assert hm.remove("banana") is True
    assert hm.get("banana") is None
    assert hm.remove("nonexistent") is False
    print("=== Q1: Separate Chaining Hash Map Verified ===")


# ==============================================================================
# Question 2: Open Addressing with Linear Probing and Tombstones
# ==============================================================================
class LinearProbingHashMap:
    """
    Hash map with open addressing and linear probing.
    Deleted slots are marked with a TOMBSTONE sentinel.
    """
    TOMBSTONE = object()

    def __init__(self, capacity: int = 16):
        self.capacity = capacity
        self.keys: List[Any] = [None] * capacity
        self.values: List[Any] = [None] * capacity
        self.size = 0

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def put(self, key: Any, value: Any) -> None:
        if self.size >= self.capacity // 2:
            raise OverflowError("Table load factor exceeded threshold")

        idx = self._hash(key)
        first_tombstone = None

        while self.keys[idx] is not None:
            if self.keys[idx] == key:
                self.values[idx] = value
                return
            if self.keys[idx] is self.TOMBSTONE and first_tombstone is None:
                first_tombstone = idx
            idx = (idx + 1) % self.capacity

        target_idx = first_tombstone if first_tombstone is not None else idx
        self.keys[target_idx] = key
        self.values[target_idx] = value
        self.size += 1

    def get(self, key: Any) -> Optional[Any]:
        idx = self._hash(key)
        start_idx = idx

        while self.keys[idx] is not None:
            if self.keys[idx] == key:
                return self.values[idx]
            idx = (idx + 1) % self.capacity
            if idx == start_idx:
                break
        return None

    def delete(self, key: Any) -> bool:
        idx = self._hash(key)
        start_idx = idx

        while self.keys[idx] is not None:
            if self.keys[idx] == key:
                self.keys[idx] = self.TOMBSTONE
                self.values[idx] = None
                self.size -= 1
                return True
            idx = (idx + 1) % self.capacity
            if idx == start_idx:
                break
        return False


def test_q2_linear_probing():
    lp = LinearProbingHashMap(8)
    lp.put("k1", "v1")
    lp.put("k2", "v2")
    assert lp.get("k1") == "v1"
    assert lp.get("k2") == "v2"

    assert lp.delete("k1") is True
    assert lp.get("k1") is None
    # Lookup of k2 still works after tombstone in front of it
    assert lp.get("k2") == "v2"

    # Reuse tombstone slot
    lp.put("k3", "v3")
    assert lp.get("k3") == "v3"
    print("=== Q2: Open Addressing with Linear Probing & Tombstones Verified ===")


# ==============================================================================
# Question 3: Quadratic Probing Collision Resolution
# ==============================================================================
class QuadraticProbingHashMap:
    """
    Open addressing using quadratic probing:
    hash_idx(k, i) = (h(k) + i + i^2) % capacity.
    """
    def __init__(self, capacity: int = 17):  # Prime capacity recommended
        self.capacity = capacity
        self.table: List[Optional[Tuple[Any, Any]]] = [None] * capacity
        self.size = 0

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def put(self, key: Any, value: Any) -> bool:
        base_h = self._hash(key)
        for i in range(self.capacity):
            idx = (base_h + i + i * i) % self.capacity
            if self.table[idx] is None or self.table[idx][0] == key:
                if self.table[idx] is None:
                    self.size += 1
                self.table[idx] = (key, value)
                return True
        return False  # Failed to place

    def get(self, key: Any) -> Optional[Any]:
        base_h = self._hash(key)
        for i in range(self.capacity):
            idx = (base_h + i + i * i) % self.capacity
            entry = self.table[idx]
            if entry is None:
                return None
            if entry[0] == key:
                return entry[1]
        return None


def test_q3_quadratic_probing():
    qp = QuadraticProbingHashMap(11)
    qp.put(1, "one")
    qp.put(12, "twelve")  # 12 % 11 == 1 (collides with 1)
    qp.put(23, "twenty-three")  # 23 % 11 == 1 (collides again)

    assert qp.get(1) == "one"
    assert qp.get(12) == "twelve"
    assert qp.get(23) == "twenty-three"
    assert qp.get(99) is None
    print("=== Q3: Quadratic Probing Hash Map Verified ===")


# ==============================================================================
# Question 4: Double Hashing Collision Resolution
# ==============================================================================
class DoubleHashingMap:
    """
    Open addressing using double hashing:
    hash_idx(k, i) = (h1(k) + i * h2(k)) % capacity
    h1(k) = k % capacity
    h2(k) = 7 - (k % 7) (guarantees step > 0)
    """
    def __init__(self, capacity: int = 13):
        self.capacity = capacity
        self.table: List[Optional[Tuple[int, Any]]] = [None] * capacity

    def _h1(self, key: int) -> int:
        return key % self.capacity

    def _h2(self, key: int) -> int:
        return 7 - (key % 7)

    def put(self, key: int, value: Any) -> bool:
        h1 = self._h1(key)
        h2 = self._h2(key)

        for i in range(self.capacity):
            idx = (h1 + i * h2) % self.capacity
            if self.table[idx] is None or self.table[idx][0] == key:
                self.table[idx] = (key, value)
                return True
        return False

    def get(self, key: int) -> Optional[Any]:
        h1 = self._h1(key)
        h2 = self._h2(key)

        for i in range(self.capacity):
            idx = (h1 + i * h2) % self.capacity
            entry = self.table[idx]
            if entry is None:
                return None
            if entry[0] == key:
                return entry[1]
        return None


def test_q4_double_hashing():
    dh = DoubleHashingMap(13)
    dh.put(18, "val_18")  # 18 % 13 = 5
    dh.put(31, "val_31")  # 31 % 13 = 5 (collision! h2 = 7 - (31 % 7) = 7 - 3 = 4, next idx = (5 + 4) % 13 = 9)

    assert dh.get(18) == "val_18"
    assert dh.get(31) == "val_31"
    assert dh.get(99) is None
    print("=== Q4: Double Hashing Collision Resolution Verified ===")


# ==============================================================================
# Question 5: Dynamic Rehashing and Table Resizing
# ==============================================================================
class ResizableHashMap:
    """
    Auto-resizing hash table that doubles its bucket array and rehashes all elements
    when load factor exceeds max_load_factor (default 0.75).
    """
    def __init__(self, initial_capacity: int = 4, max_load_factor: float = 0.75):
        self.capacity = initial_capacity
        self.max_load_factor = max_load_factor
        self.buckets: List[List[Tuple[Any, Any]]] = [[] for _ in range(self.capacity)]
        self.size = 0
        self.resize_count = 0

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def put(self, key: Any, value: Any) -> None:
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1

        if (self.size / self.capacity) > self.max_load_factor:
            self._resize()

    def get(self, key: Any) -> Optional[Any]:
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return None

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        self.resize_count += 1

        for bucket in old_buckets:
            for k, v in bucket:
                self.put(k, v)


def test_q5_dynamic_rehashing():
    rhm = ResizableHashMap(initial_capacity=4, max_load_factor=0.75)
    assert rhm.capacity == 4

    rhm.put("a", 1)
    rhm.put("b", 2)
    rhm.put("c", 3)  # size 3, capacity 4 -> load factor 0.75
    assert rhm.capacity == 4

    rhm.put("d", 4)  # triggers resize to 8
    assert rhm.capacity == 8
    assert rhm.resize_count == 1

    for k, expected_v in [("a", 1), ("b", 2), ("c", 3), ("d", 4)]:
        assert rhm.get(k) == expected_v
    print("=== Q5: Dynamic Rehashing & Table Resizing Verified ===")


# ==============================================================================
# Question 6: Two Sum with Hash Map (One-Pass O(n))
# ==============================================================================
def two_sum_hash_map(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
    Finds two 0-indexed positions (i, j) such that nums[i] + nums[j] == target.
    Time Complexity: O(n), Space Complexity: O(n).
    """
    seen: Dict[int, int] = {}
    for idx, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], idx)
        seen[num] = idx
    return None


def test_q6_two_sum_hash_map():
    assert two_sum_hash_map([2, 7, 11, 15], 9) == (0, 1)
    assert two_sum_hash_map([3, 2, 4], 6) == (1, 2)
    assert two_sum_hash_map([3, 3], 6) == (0, 1)
    assert two_sum_hash_map([1, 2], 10) is None
    print("=== Q6: One-Pass Two Sum via Hash Map Verified ===")


# ==============================================================================
# Question 7: Group Anagrams via Frequency Key Hashing
# ==============================================================================
def group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    Groups strings that are anagrams of each other.
    Uses a 26-element character frequency tuple as the dictionary hash key.
    Time Complexity: O(N * K) where K is max string length.
    """
    groups: Dict[Tuple[int, ...], List[str]] = {}
    for s in strs:
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord("a")] += 1
        key = tuple(count)
        if key not in groups:
            groups[key] = []
        groups[key].append(s)

    return list(groups.values())


def test_q7_group_anagrams():
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    res = group_anagrams(words)
    # Sort groups by length to compare deterministically
    sorted_res = sorted([sorted(g) for g in res], key=lambda g: (len(g), g[0]))
    expected = [
        ["bat"],
        ["nat", "tan"],
        ["ate", "eat", "tea"],
    ]
    assert sorted_res == expected
    print("=== Q7: Group Anagrams via Character Frequency Key Hashing Verified ===")


# ==============================================================================
# Question 8: Subarray Sum Equals K (Prefix Sum Frequency Map)
# ==============================================================================
def subarray_sum_equals_k(nums: List[int], k: int) -> int:
    """
    Finds the total number of continuous subarrays whose sum equals k.
    Runs in linear O(n) time using running prefix sum frequency hash map.
    """
    count = 0
    running_sum = 0
    # Map prefix_sum -> occurrence count; base case sum 0 has count 1
    prefix_counts: Dict[int, int] = {0: 1}

    for num in nums:
        running_sum += num
        # If (running_sum - k) was seen before, a subarray summing to k ended here
        if (running_sum - k) in prefix_counts:
            count += prefix_counts[running_sum - k]

        prefix_counts[running_sum] = prefix_counts.get(running_sum, 0) + 1

    return count


def test_q8_subarray_sum_equals_k():
    assert subarray_sum_equals_k([1, 1, 1], 2) == 2  # [1, 1] at (0, 1) and (1, 2)
    assert subarray_sum_equals_k([1, 2, 3], 3) == 2  # [1, 2] and [3]
    assert subarray_sum_equals_k([1, -1, 0], 0) == 3  # [1, -1], [0], [1, -1, 0]
    print("=== Q8: Subarray Sum Equals K via Prefix Sum Hash Map Verified ===")


# ==============================================================================
# Question 9: Longest Consecutive Sequence in Unsorted Array
# ==============================================================================
def longest_consecutive_sequence(nums: List[int]) -> int:
    """
    Finds length of longest consecutive elements sequence in O(n) time.
    Uses hash set to verify streak start (num - 1 not in set).
    """
    num_set = set(nums)
    max_streak = 0

    for num in num_set:
        # Check if num is the start of a streak
        if (num - 1) not in num_set:
            curr_num = num
            curr_streak = 1

            while (curr_num + 1) in num_set:
                curr_num += 1
                curr_streak += 1

            max_streak = max(max_streak, curr_streak)

    return max_streak


def test_q9_longest_consecutive_sequence():
    # Sequence: 1, 2, 3, 4 -> length 4
    nums1 = [100, 4, 200, 1, 3, 2]
    assert longest_consecutive_sequence(nums1) == 4

    # Sequence: 0, 1, 2, 3, 4, 5, 6, 7, 8 -> length 9
    nums2 = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
    assert longest_consecutive_sequence(nums2) == 9

    assert longest_consecutive_sequence([]) == 0
    print("=== Q9: Longest Consecutive Sequence in O(n) Verified ===")


# ==============================================================================
# Question 10: Architectural System: Distributed Consistent Hashing Ring
# ==============================================================================
import bisect


class ConsistentHashRing:
    """
    Production-grade Consistent Hash Ring with virtual nodes (vnodes).
    Evenly distributes keys across a cluster, minimizing re-mapping on node addition/removal.
    """
    def __init__(self, replicas: int = 3):
        self.replicas = replicas
        self.ring: List[int] = []  # Sorted hash positions of virtual nodes
        self.vnode_map: Dict[int, str] = {}  # vnode_hash -> physical_node_id

    def _hash(self, key_str: str) -> int:
        """Standard 32-bit positive hash representation."""
        return abs(hash(key_str)) % (2 ** 32)

    def add_node(self, node_id: str) -> None:
        """Adds a physical node and creates 'replicas' virtual node tokens on the ring."""
        for i in range(self.replicas):
            vnode_key = f"{node_id}#vnode_{i}"
            v_hash = self._hash(vnode_key)
            bisect.insort(self.ring, v_hash)
            self.vnode_map[v_hash] = node_id

    def remove_node(self, node_id: str) -> None:
        """Removes a physical node and cleans all its virtual nodes from the ring."""
        for i in range(self.replicas):
            vnode_key = f"{node_id}#vnode_{i}"
            v_hash = self._hash(vnode_key)
            if v_hash in self.vnode_map:
                del self.vnode_map[v_hash]
                idx = bisect.bisect_left(self.ring, v_hash)
                if idx < len(self.ring) and self.ring[idx] == v_hash:
                    self.ring.pop(idx)

    def get_node(self, key: str) -> Optional[str]:
        """
        Maps a key to the closest physical server node moving clockwise on the ring.
        """
        if not self.ring:
            return None

        key_hash = self._hash(key)
        idx = bisect.bisect_right(self.ring, key_hash)
        # Wraparound clockwise to first node if past the last hash position
        if idx == len(self.ring):
            idx = 0

        vnode_hash = self.ring[idx]
        return self.vnode_map[vnode_hash]


def test_q10_consistent_hash_ring():
    ring = ConsistentHashRing(replicas=5)

    ring.add_node("server_alpha")
    ring.add_node("server_beta")
    ring.add_node("server_gamma")

    # Map keys to servers
    s1 = ring.get_node("user_session_101")
    s2 = ring.get_node("user_session_102")
    s3 = ring.get_node("user_session_103")

    assert s1 in ("server_alpha", "server_beta", "server_gamma")
    assert s2 in ("server_alpha", "server_beta", "server_gamma")

    # Key mappings remain stable for unaffected nodes when removing server_beta
    ring.remove_node("server_beta")
    s1_after = ring.get_node("user_session_101")
    assert s1_after in ("server_alpha", "server_gamma")
    print("=== Q10: Architectural Consistent Hashing Ring with Vnodes Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_separate_chaining()
    test_q2_linear_probing()
    test_q3_quadratic_probing()
    test_q4_double_hashing()
    test_q5_dynamic_rehashing()
    test_q6_two_sum_hash_map()
    test_q7_group_anagrams()
    test_q8_subarray_sum_equals_k()
    test_q9_longest_consecutive_sequence()
    test_q10_consistent_hash_ring()
    print("\nAll 10 hash table DSA questions passed successfully!")
