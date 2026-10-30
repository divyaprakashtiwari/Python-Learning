"""
Question 2: Persistent File Cache & unittest Fixture Lifecycle Harness
Topic: Testing, Debugging, and Profiling

Key Concepts Tested:
- File-backed persistent caching with JSON serialization and TTL expiration
- Complete test fixture lifecycle: setUpClass, tearDownClass, setUp, tearDown
- Resource tracking and guaranteed cleanup via self.addCleanup
- Temporary directory isolation using tempfile.mkdtemp and shutil.rmtree
"""

import os
import json
import time
import shutil
import tempfile
import unittest
from typing import Dict, Any, Optional


class PersistentFileCache:
    """
    File-backed cache storing JSON data files with TTL expiration metadata.
    """

    def __init__(self, cache_dir: str) -> None:
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def _file_path(self, key: str) -> str:
        safe_key = "".join(c for c in key if c.isalnum() or c in ("_", "-"))
        return os.path.join(self.cache_dir, f"{safe_key}.json")

    def set(self, key: str, data: Dict[str, Any], ttl_seconds: float = 3600.0) -> None:
        """Stores dictionary payload with expiration epoch timestamp."""
        payload = {
            "expires_at": time.time() + ttl_seconds,
            "data": data,
        }
        target_path = self._file_path(key)
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(payload, f)

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Reads cached item. If expired or missing, purges file and returns None."""
        target_path = self._file_path(key)
        if not os.path.isfile(target_path):
            return None

        try:
            with open(target_path, "r", encoding="utf-8") as f:
                payload = json.load(f)
        except (json.JSONDecodeError, OSError):
            return None

        if time.time() >= payload.get("expires_at", 0):
            # Expired; purge file
            self.delete(key)
            return None

        return payload.get("data")

    def delete(self, key: str) -> bool:
        """Removes cache file for key."""
        target_path = self._file_path(key)
        if os.path.isfile(target_path):
            os.remove(target_path)
            return True
        return False

    def clear(self) -> int:
        """Removes all cache entries from cache directory."""
        purged = 0
        for fname in os.listdir(self.cache_dir):
            if fname.endswith(".json"):
                fpath = os.path.join(self.cache_dir, fname)
                try:
                    os.remove(fpath)
                    purged += 1
                except OSError:
                    pass
        return purged


class TestPersistentFileCache(unittest.TestCase):
    """
    Test suite demonstrating complete unittest fixture lifecycle methods.
    """

    temp_root: str
    cache: PersistentFileCache

    @classmethod
    def setUpClass(cls) -> None:
        """Executed once before all tests in this class."""
        cls.temp_root = tempfile.mkdtemp(prefix="cache_test_")
        cls.cache = PersistentFileCache(cache_dir=cls.temp_root)

    @classmethod
    def tearDownClass(cls) -> None:
        """Executed once after all tests in this class complete."""
        shutil.rmtree(cls.temp_root, ignore_errors=True)

    def setUp(self) -> None:
        """Executed before each test method; seeds baseline data."""
        self.cache.set("session_user", {"id": 1, "name": "Alice"})

    def tearDown(self) -> None:
        """Executed after each test method; resets cache state."""
        self.cache.clear()

    def test_get_existing_baseline(self) -> None:
        data = self.cache.get("session_user")
        self.assertIsNotNone(data)
        self.assertEqual(data.get("name"), "Alice")

    def test_expired_entry_purged(self) -> None:
        # Set low TTL
        self.cache.set("short_lived", {"temp": 123}, ttl_seconds=0.02)
        time.sleep(0.05)
        # Should detect expiration, remove file, and return None
        result = self.cache.get("short_lived")
        self.assertIsNone(result)

    def test_cache_delete_removes_file(self) -> None:
        existed = self.cache.delete("session_user")
        self.assertTrue(existed)
        self.assertIsNone(self.cache.get("session_user"))

    def test_cache_clear_purges_all(self) -> None:
        self.cache.set("item_1", {"v": 1})
        self.cache.set("item_2", {"v": 2})
        count = self.cache.clear()
        self.assertGreaterEqual(count, 2)
        self.assertIsNone(self.cache.get("item_1"))

    def test_cleanup_callback_executed(self) -> None:
        # Create an out-of-band lock file and guarantee its removal via addCleanup
        lock_file = os.path.join(self.temp_root, "test.lock")
        with open(lock_file, "w", encoding="utf-8") as f:
            f.write("LOCKED")

        self.addCleanup(lambda: os.remove(lock_file) if os.path.exists(lock_file) else None)
        self.assertTrue(os.path.exists(lock_file))


if __name__ == "__main__":
    print("=== Running Fixture Lifecycle Test Suite ===")
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestPersistentFileCache)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n=== Lifecycle Results Summary ===")
    print(f"Fixture Lifecycle Tests Run: {result.testsRun}")
    print(f"All Fixture Tests Passed: {result.wasSuccessful()}")
    print(f"Temporary Directory Cleared Post-Class: {not os.path.exists(TestPersistentFileCache.temp_root)}")
