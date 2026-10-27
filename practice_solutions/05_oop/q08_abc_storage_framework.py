"""
Topic 05 - Object-Oriented Programming (OOP): Question 8
Problem: Abstract Storage Framework using Python's abc module (ABC, @abstractmethod).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class DataStorageEngine(ABC):
    """Abstract Base Class enforcing standard persistence contracts."""

    @abstractmethod
    def connect(self) -> None:
        """Establishes connection or initializes the target persistence backend."""
        pass

    @abstractmethod
    def save(self, key: str, payload: Dict[str, Any]) -> bool:
        """Persists payload dictionary under the designated string key."""
        pass

    @abstractmethod
    def load(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieves dictionary by key, or returns None if key does not exist."""
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Removes the record by key. Returns True if found and deleted, else False."""
        pass

    def batch_save(self, items: Dict[str, Dict[str, Any]]) -> int:
        """Template method batch-persisting multiple key-payload pairs."""
        count = 0
        for key, payload in items.items():
            if self.save(key, payload):
                count += 1
        return count


class IncompleteEngine(DataStorageEngine):
    """Fails instantiation because it omits the abstract method delete()."""

    def connect(self) -> None:
        pass

    def save(self, key: str, payload: Dict[str, Any]) -> bool:
        return True

    def load(self, key: str) -> Optional[Dict[str, Any]]:
        return None
    # delete() is intentionally omitted to verify contract enforcement


class InMemoryStorageEngine(DataStorageEngine):
    """Concrete in-memory implementation using a standard Python dictionary."""

    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}
        self._connected: bool = False

    def connect(self) -> None:
        self._connected = True
        print("InMemory Storage Connected Successfully.")

    def save(self, key: str, payload: Dict[str, Any]) -> bool:
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        self._store[key] = payload.copy()
        return True

    def load(self, key: str) -> Optional[Dict[str, Any]]:
        return self._store.get(key)

    def delete(self, key: str) -> bool:
        if key in self._store:
            del self._store[key]
            return True
        return False


class CacheBackedStorageEngine(DataStorageEngine):
    """Read-through cache layer backed by a primary persistent storage engine."""

    def __init__(self, primary: DataStorageEngine):
        self.primary = primary
        self._cache: Dict[str, Dict[str, Any]] = {}

    def connect(self) -> None:
        self.primary.connect()

    def save(self, key: str, payload: Dict[str, Any]) -> bool:
        self._cache[key] = payload.copy()
        return self.primary.save(key, payload)

    def load(self, key: str) -> Optional[Dict[str, Any]]:
        if key in self._cache:
            return self._cache[key]
        item = self.primary.load(key)
        if item is not None:
            self._cache[key] = item.copy()
        return item

    def delete(self, key: str) -> bool:
        self._cache.pop(key, None)
        return self.primary.delete(key)


# Verification & Execution
memory_engine = InMemoryStorageEngine()
memory_engine.connect()

saved_count = memory_engine.batch_save({
    "user:1": {"name": "Alice", "role": "Engineer"},
    "user:2": {"name": "Bob", "role": "Architect"}
})
print(f"Batch Saved: {saved_count} records.")

user1 = memory_engine.load("user:1")
print(f"Retrieved user:1: {user1}")

deleted = memory_engine.delete("user:2")
print(f"Deleted user:2: {deleted}")

missing = memory_engine.load("user:2")
print(f"Retrieved user:2 (post-delete): {missing}")

# Contract enforcement check:
try:
    incomplete = IncompleteEngine()  # type: ignore
except TypeError as err:
    print(f"Caught instantiation error: {err}")
