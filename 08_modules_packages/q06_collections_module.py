"""
Topic 08: Modules and Packages - Question 06: collections Module

A comprehensive collection of 10 standalone, runnable exercises exploring
Python's standard library `collections` module: Counter, defaultdict, deque,
namedtuple, OrderedDict, ChainMap, UserDict, and UserList.

Questions Covered:
 1. collections.Counter: Frequency tabulation, most_common(), multiset algebra (+, -, &, |).
 2. collections.defaultdict: Automated key initialization with list, set, int, and lambdas.
 3. collections.deque: High-performance O(1) two-ended queue, maxlen ring buffers, and rotate().
 4. collections.namedtuple: Self-documenting immutable records, _replace(), and _asdict().
 5. collections.OrderedDict: Order-sensitive equality, move_to_end(), and FIFO/LIFO popitem().
 6. collections.ChainMap: Layered dictionary scoping (CLI args > Env vars > Defaults).
 7. collections.UserDict: Safely customizing dictionary behavior and validation.
 8. collections.UserList: Customizing list mutation semantics and element coercion.
 9. Multi-Tier Auto-Vivification: Infinite-depth nested dictionaries with recursive defaultdict.
10. Advanced Project: High-Performance LRU Cache with Access Analytics & Recency Tracking.
"""

from collections import (
    ChainMap,
    Counter,
    OrderedDict,
    UserDict,
    UserList,
    defaultdict,
    deque,
    namedtuple,
)
from typing import Any


# ==============================================================================
# Question 1: collections.Counter Mechanics & Multiset Algebra
# ==============================================================================
def exercise_q1_counter_mechanics() -> None:
    """
    Demonstrate Counter frequency counts, most_common(), element arithmetic,
    and multiset operations (union, intersection, addition, subtraction).
    """
    print("=== Q1: collections.Counter Mechanics ===")

    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    counts = Counter(words)

    # Frequency checks
    assert counts["apple"] == 3
    assert counts["banana"] == 2
    assert counts["cherry"] == 1
    assert counts["missing"] == 0  # Missing keys cleanly return 0, no KeyError!

    # most_common(n)
    top_2 = counts.most_common(2)
    assert top_2 == [("apple", 3), ("banana", 2)]

    # Multiset Algebra
    c1 = Counter(a=3, b=1)
    c2 = Counter(a=1, b=2)

    # Addition (+): adds counts together
    added = c1 + c2
    assert added == Counter(a=4, b=3)

    # Subtraction (-): subtracts counts, discarding non-positive counts
    subbed = c1 - c2
    assert subbed == Counter(a=2)  # b has 1 - 2 = -1 -> excluded

    # Intersection (&): minimum of corresponding counts
    inter = c1 & c2
    assert inter == Counter(a=1, b=1)

    # Union (|): maximum of corresponding counts
    union = c1 | c2
    assert union == Counter(a=3, b=2)

    print(f"  Top 2 common items:  {top_2}")
    print(f"  Multiset addition:    {added}")
    print(f"  Multiset intersection: {inter}")


# ==============================================================================
# Question 2: collections.defaultdict Fundamentals
# ==============================================================================
def exercise_q2_defaultdict_fundamentals() -> None:
    """
    Demonstrate defaultdict with different default factories:
    - list: for grouping items
    - int: for counting
    - set: for unique association
    """
    print("\n=== Q2: collections.defaultdict Fundamentals ===")

    # 1. Grouping with list factory
    grouped_by_dept = defaultdict(list)
    employees = [("Eng", "Alice"), ("Sales", "Bob"), ("Eng", "Charlie"), ("Sales", "Dave")]
    for dept, name in employees:
        grouped_by_dept[dept].append(name)

    assert grouped_by_dept["Eng"] == ["Alice", "Charlie"]
    assert grouped_by_dept["Sales"] == ["Bob", "Dave"]
    assert grouped_by_dept["HR"] == []  # Accessing uninitialized key creates empty list!

    # 2. Integer accumulator
    word_lengths = defaultdict(int)
    for word in ["code", "learn", "python"]:
        word_lengths[len(word)] += 1

    assert word_lengths[4] == 1
    assert word_lengths[5] == 1
    assert word_lengths[6] == 1

    print(f"  Grouped by department: {dict(grouped_by_dept)}")
    print(f"  Word lengths distribution: {dict(word_lengths)}")


# ==============================================================================
# Question 3: collections.deque (High-Performance Double-Ended Queue)
# ==============================================================================
def exercise_q3_deque_operations() -> None:
    """
    Demonstrate deque with O(1) appends and pops from both ends,
    fixed-capacity ring buffers with maxlen, and rotation.
    """
    print("\n=== Q3: collections.deque ===")

    # 1. Double-ended appends and pops
    dq = deque([10, 20])
    dq.append(30)       # Right append
    dq.appendleft(0)    # Left append: [0, 10, 20, 30]
    assert list(dq) == [0, 10, 20, 30]

    right_popped = dq.pop()      # 30
    left_popped = dq.popleft()   # 0
    assert right_popped == 30
    assert left_popped == 0
    assert list(dq) == [10, 20]

    # 2. Bounded ring buffer with maxlen (automatically evicts oldest)
    ring_buffer = deque(maxlen=3)
    for item in [1, 2, 3, 4, 5]:
        ring_buffer.append(item)
    # 1 and 2 were pushed out!
    assert list(ring_buffer) == [3, 4, 5]

    # 3. Rotation
    rot_dq = deque([1, 2, 3, 4, 5])
    rot_dq.rotate(2)  # Rotates 2 steps to the right: [4, 5, 1, 2, 3]
    assert list(rot_dq) == [4, 5, 1, 2, 3]

    print(f"  Ring buffer (maxlen=3): {list(ring_buffer)}")
    print(f"  Rotated deque:          {list(rot_dq)}")


# ==============================================================================
# Question 4: collections.namedtuple
# ==============================================================================
def exercise_q4_namedtuple_records() -> None:
    """
    Demonstrate namedtuple for creating lightweight, memory-efficient,
    immutable record types with field name access, _replace(), and _asdict().
    """
    print("\n=== Q4: collections.namedtuple ===")

    Point = namedtuple("Point", ["x", "y", "label"])
    p1 = Point(10.5, 20.0, "Origin_Marker")

    # Access by attribute or index
    assert p1.x == 10.5
    assert p1.y == 20.0
    assert p1[0] == 10.5

    # Immutability
    try:
        p1.x = 99.0  # type: ignore
        assert False
    except AttributeError:
        pass

    # _replace() creates a new instance with updated values
    p2 = p1._replace(x=50.0, label="Updated_Marker")
    assert p2.x == 50.0
    assert p2.y == 20.0
    assert p1.x == 10.5  # Original untouched!

    # _asdict() converts to dictionary
    p1_dict = p1._asdict()
    assert p1_dict == {"x": 10.5, "y": 20.0, "label": "Origin_Marker"}

    print(f"  Original namedtuple: {p1}")
    print(f"  Replaced namedtuple: {p2}")
    print(f"  Converted dict:      {p1_dict}")


# ==============================================================================
# Question 5: collections.OrderedDict
# ==============================================================================
def exercise_q5_ordered_dict() -> None:
    """
    Demonstrate OrderedDict features that differ from standard dict:
    - Order-sensitive equality check
    - move_to_end(key, last=False/True)
    - popitem(last=False) for FIFO vs popitem(last=True) for LIFO
    """
    print("\n=== Q5: collections.OrderedDict ===")

    # 1. Order-sensitive equality
    od1 = OrderedDict([("a", 1), ("b", 2)])
    od2 = OrderedDict([("b", 2), ("a", 1)])
    # In standard dict, d1 == d2 is True even with different key order.
    # In OrderedDict, equality requires identical order!
    assert od1 != od2

    # 2. move_to_end()
    od = OrderedDict([("first", 1), ("second", 2), ("third", 3)])
    # Move 'first' to end
    od.move_to_end("first", last=True)
    assert list(od.keys()) == ["second", "third", "first"]

    # Move 'third' to front
    od.move_to_end("third", last=False)
    assert list(od.keys()) == ["third", "second", "first"]

    # 3. FIFO popitem
    fifo_key, fifo_val = od.popitem(last=False)
    assert fifo_key == "third"
    assert fifo_val == 3

    print(f"  Order-sensitive equality verified: od1 == od2 is {od1 == od2}")
    print(f"  Remaining keys after FIFO popitem: {list(od.keys())}")


# ==============================================================================
# Question 6: collections.ChainMap (Layered Scoping)
# ==============================================================================
def exercise_q6_chain_map_scoping() -> None:
    """
    Demonstrate ChainMap for searching across prioritized hierarchical dictionaries
    without performing expensive dict merges.
    Order of precedence: CLI Args > Environment Config > Default Settings.
    """
    print("\n=== Q6: collections.ChainMap ===")

    defaults = {"theme": "light", "port": 8080, "workers": 4}
    env_config = {"port": 9000, "workers": 8}
    cli_args = {"theme": "dark"}

    # ChainMap prioritizes from left to right: cli_args > env_config > defaults
    config = ChainMap(cli_args, env_config, defaults)

    # 'theme' resolved from cli_args
    assert config["theme"] == "dark"
    # 'port' resolved from env_config
    assert config["port"] == 9000
    # 'workers' resolved from env_config
    assert config["workers"] == 8

    # Writes mutate ONLY the first mapping (cli_args)
    config["log_level"] = "DEBUG"
    assert "log_level" in cli_args
    assert "log_level" not in defaults

    print(f"  Resolved Config:")
    print(f"    theme:     {config['theme']} (from CLI)")
    print(f"    port:      {config['port']} (from Env)")
    print(f"    workers:   {config['workers']} (from Env)")
    print(f"    log_level: {config['log_level']} (mutated into CLI)")


# ==============================================================================
# Question 7: collections.UserDict (Safe Custom Dictionaries)
# ==============================================================================
class CaseInsensitiveDict(UserDict):
    """
    Dictionary subclass using UserDict that transparently normalizes all keys
    to lowercase, supporting case-insensitive lookups.
    """

    def __getitem__(self, key: Any) -> Any:
        norm_key = key.lower() if isinstance(key, str) else key
        return self.data[norm_key]

    def __setitem__(self, key: Any, value: Any) -> None:
        norm_key = key.lower() if isinstance(key, str) else key
        self.data[norm_key] = value

    def __contains__(self, key: Any) -> bool:
        norm_key = key.lower() if isinstance(key, str) else key
        return norm_key in self.data


def exercise_q7_user_dict() -> None:
    """
    Demonstrate UserDict customization for case-insensitive key resolution.
    """
    print("\n=== Q7: collections.UserDict ===")

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = "Bearer token_xyz"

    assert headers["content-type"] == "application/json"
    assert headers["CONTENT-TYPE"] == "application/json"
    assert "authorization" in headers
    assert len(headers) == 2

    print(f"  Case-insensitive lookup: headers['content-type'] = {headers['content-type']}")


# ==============================================================================
# Question 8: collections.UserList (Custom List Behaviors)
# ==============================================================================
class TypedNumberList(UserList):
    """
    List subclass using UserList that enforces all elements are numeric (int/float)
    and coerces string digits automatically.
    """

    def __init__(self, initlist: Any = None) -> None:
        super().__init__()
        if initlist is not None:
            self.extend(initlist)

    def append(self, item: Any) -> None:
        self.data.append(self._validate(item))

    def extend(self, other: Any) -> None:
        self.data.extend(self._validate(i) for i in other)

    def _validate(self, val: Any) -> float:
        if isinstance(val, (int, float)):
            return float(val)
        elif isinstance(val, str) and val.replace(".", "", 1).isdigit():
            return float(val)
        raise TypeError(f"Invalid numeric value: {val}")


def exercise_q8_user_list() -> None:
    """
    Demonstrate UserList with automatic type validation and coercion.
    """
    print("\n=== Q8: collections.UserList ===")

    num_list = TypedNumberList([1, 2, "3.5"])
    num_list.append("42")

    assert num_list == [1.0, 2.0, 3.5, 42.0]

    try:
        num_list.append("not_a_number")
        assert False
    except TypeError as exc:
        assert "Invalid numeric value" in str(exc)

    print(f"  TypedNumberList successfully validated elements: {num_list.data}")


# ==============================================================================
# Question 9: Multi-Tier Auto-Vivification (Nested defaultdict)
# ==============================================================================
def make_tree() -> defaultdict:
    """
    Recursive factory that auto-vivifies an arbitrary number of nested dictionary levels.
    """
    return defaultdict(make_tree)


def exercise_q9_nested_autovivification() -> None:
    """
    Demonstrate infinite-depth nested dictionary auto-vivification without KeyError.
    """
    print("\n=== Q9: Multi-Tier Auto-Vivification ===")

    fs_tree = make_tree()

    # Assign directly to deeply nested non-existent path
    fs_tree["home"]["user"]["documents"]["notes.txt"] = "File Content"
    fs_tree["etc"]["nginx"]["nginx.conf"] = "Server Config"

    assert fs_tree["home"]["user"]["documents"]["notes.txt"] == "File Content"
    assert fs_tree["etc"]["nginx"]["nginx.conf"] == "Server Config"

    # Reading an unassigned nested branch automatically instantiates child dicts
    assert isinstance(fs_tree["var"]["log"]["app"], defaultdict)

    print("  Successfully populated deep nested structure without intermediate initialization:")
    print(f"    Path: home/user/documents/notes.txt -> {fs_tree['home']['user']['documents']['notes.txt']}")


# ==============================================================================
# Question 10: Advanced Project - LRU Cache with Frequency & Recency Telemetry
# ==============================================================================
class AdvancedLRUCache:
    """
    Production-grade Least Recently Used (LRU) Cache utilizing:
    - OrderedDict: for O(1) eviction of oldest accessed item.
    - Counter: for tracking access frequency per key.
    - deque: for keeping audit history of evictions.
    """

    def __init__(self, capacity: int = 3) -> None:
        self.capacity = capacity
        self.cache: OrderedDict[str, Any] = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.access_counter: Counter[str] = Counter()
        self.eviction_history: deque[str] = deque(maxlen=5)

    def get(self, key: str) -> Any | None:
        if key not in self.cache:
            self.misses += 1
            return None

        self.hits += 1
        self.access_counter[key] += 1
        # Move accessed key to end to mark as most recently used
        self.cache.move_to_end(key, last=True)
        return self.cache[key]

    def put(self, key: str, value: Any) -> None:
        if key in self.cache:
            self.cache.move_to_end(key, last=True)
        else:
            if len(self.cache) >= self.capacity:
                # Evict least recently used (first item in OrderedDict)
                evicted_key, _ = self.cache.popitem(last=False)
                self.eviction_history.append(evicted_key)

        self.cache[key] = value
        self.access_counter[key] += 1


def exercise_q10_lru_cache() -> None:
    """
    Test AdvancedLRUCache eviction and access metrics.
    """
    print("\n=== Q10: Advanced LRU Cache Engine ===")

    lru = AdvancedLRUCache(capacity=3)

    lru.put("A", 100)
    lru.put("B", 200)
    lru.put("C", 300)

    # Access A so B becomes the oldest
    assert lru.get("A") == 100
    assert lru.hits == 1

    # Put D -> Evicts B (oldest)
    lru.put("D", 400)
    assert lru.get("B") is None  # B was evicted!
    assert lru.misses == 1
    assert list(lru.eviction_history) == ["B"]

    # Current cache contents: C, A, D
    assert list(lru.cache.keys()) == ["C", "A", "D"]

    # Most accessed key
    assert lru.access_counter.most_common(1)[0][0] == "A"

    print(f"  Cache keys after eviction: {list(lru.cache.keys())}")
    print(f"  Eviction history:          {list(lru.eviction_history)}")
    print(f"  Cache stats:               Hits={lru.hits}, Misses={lru.misses}")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_counter_mechanics()
    exercise_q2_defaultdict_fundamentals()
    exercise_q3_deque_operations()
    exercise_q4_namedtuple_records()
    exercise_q5_ordered_dict()
    exercise_q6_chain_map_scoping()
    exercise_q7_user_dict()
    exercise_q8_user_list()
    exercise_q9_nested_autovivification()
    exercise_q10_lru_cache()

    print("\nAll 10 collections module questions executed and asserted successfully!")
