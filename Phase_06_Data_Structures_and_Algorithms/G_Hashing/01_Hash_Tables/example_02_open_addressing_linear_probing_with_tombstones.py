"""
Phase 6 - Data Structures and Algorithms
Section G: Hashing
Topic 01: Hash Tables
Example 02: Open Addressing Hash Table with Linear Probing & Tombstone Deletion

In Open Addressing (used by CPython's built-in `dict` and Rust's `HashMap`), all
key-value pairs are stored **directly inside the contiguous bucket array** without
external linked-list chains!

1. **Linear / Quadratic Probing:** When bucket `idx` is occupied by a different key,
   probe `(idx + 1) % cap`, `(idx + 2) % cap`, ... until an empty slot is found.
2. **Why Deleted Slots MUST Be Marked as `_TOMBSTONE` (Lazy Deletion):**
   Suppose keys `K1` and `K2` both hash to slot `2`, so `K1` sits at slot `2` and
   `K2` probes forward to slot `3`.
   If we delete `K1` by setting slot `2` back to `_EMPTY` (`None`), a subsequent
   `get(K2)` will start at slot `2`, see `_EMPTY`, and **falsely conclude that `K2`
   does not exist**!
   Instead, deleting `K1` replaces slot `2` with a special `_TOMBSTONE` sentinel:
     - Searches (`get`) keep probing past `_TOMBSTONE`.
     - Insertions (`put`) can reuse the **first `_TOMBSTONE` slot** encountered!
"""

from typing import Any, List, Optional, Tuple


class _Sentinel:
    def __init__(self, label: str) -> None:
        self.label = label

    def __repr__(self) -> str:
        return self.label


_EMPTY = _Sentinel("<EMPTY>")
_TOMBSTONE = _Sentinel("<TOMBSTONE>")


class OpenAddressingHashTable:
    """
    Open-Addressing Hash Table using Linear Probing, Tombstone reuse, and automatic
    table resizing when `(size + tombstones) / capacity > 0.66`.
    """

    def __init__(self, capacity: int = 8) -> None:
        self._capacity: int = max(8, capacity)
        self._keys: List[Any] = [_EMPTY] * self._capacity
        self._values: List[Any] = [None] * self._capacity
        self._size: int = 0
        self._tombstones: int = 0

    def _hash(self, key: Any) -> int:
        # Use a deterministic polynomial hash on strings or built-in hash
        if isinstance(key, str):
            h = 0
            for ch in key:
                h = (h * 31 + ord(ch)) & 0x7FFFFFFF
            return h % self._capacity
        return (hash(key) & 0x7FFFFFFF) % self._capacity

    def _resize(self, new_capacity: int) -> None:
        old_keys = self._keys
        old_vals = self._values
        self._capacity = new_capacity
        self._keys = [_EMPTY] * new_capacity
        self._values = [None] * new_capacity
        self._size = 0
        self._tombstones = 0
        for k, v in zip(old_keys, old_vals):
            if k is not _EMPTY and k is not _TOMBSTONE:
                self.put(k, v)

    def put(self, key: Any, value: Any) -> int:
        """Inserts or updates `(key, value)` and returns the final slot index."""
        if (self._size + self._tombstones + 1) / self._capacity > 0.66:
            self._resize(self._capacity * 2)

        idx = self._hash(key)
        first_tombstone: Optional[int] = None

        while self._keys[idx] is not _EMPTY:
            if self._keys[idx] is _TOMBSTONE:
                if first_tombstone is None:
                    first_tombstone = idx
            elif self._keys[idx] == key:
                self._values[idx] = value
                return idx
            idx = (idx + 1) % self._capacity

        target = first_tombstone if first_tombstone is not None else idx
        if first_tombstone is not None:
            self._tombstones -= 1
        self._keys[target] = key
        self._values[target] = value
        self._size += 1
        return target

    def get(self, key: Any, default: Any = None) -> Tuple[Any, int]:
        """Returns `(value_or_default, probes_performed)`."""
        idx = self._hash(key)
        probes = 0
        while self._keys[idx] is not _EMPTY:
            probes += 1
            if self._keys[idx] is not _TOMBSTONE and self._keys[idx] == key:
                return self._values[idx], probes
            idx = (idx + 1) % self._capacity
        return default, probes + 1

    def remove(self, key: Any) -> bool:
        """Marks the key's slot with `_TOMBSTONE` so probe chains stay unbroken."""
        idx = self._hash(key)
        while self._keys[idx] is not _EMPTY:
            if self._keys[idx] is not _TOMBSTONE and self._keys[idx] == key:
                self._keys[idx] = _TOMBSTONE
                self._values[idx] = None
                self._size -= 1
                self._tombstones += 1
                return True
            idx = (idx + 1) % self._capacity
        return False


if __name__ == "__main__":
    print("=" * 72)
    print("Open Addressing with Linear Probing & Tombstone Slot Reuse")
    print("=" * 72)

    oa = OpenAddressingHashTable(capacity=8)
    # Deliberately insert keys that collide at bucket index 2 (multiples of 8 + 2)
    for k, v in [(2, "Val_2"), (10, "Val_10"), (18, "Val_18")]:
        slot = oa.put(k, v)
        print(f"  put({k:>2}, '{v}') -> hashed to {oa._hash(k)}, stored at slot {slot}")

    print(f"\nKeys Array after 3 colliding inserts: {oa._keys}")
    oa.remove(10)
    print(f"Keys Array after remove(10)         : {oa._keys}")

    val_18, probes_18 = oa.get(18)
    print(f"get(18) probes past <TOMBSTONE>     : value='{val_18}' in {probes_18} probes")

    reused_slot = oa.put(26, "Val_26")
    print(f"put(26, 'Val_26') reuses Tombstone  : stored at slot {reused_slot}")
    print(f"Keys Array after reusing Tombstone  : {oa._keys}")

