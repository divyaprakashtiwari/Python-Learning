"""
Topic 13: Testing and Debugging
Question 02: Test Fixtures (setUp/tearDown)

A comprehensive, production-grade guide to test fixtures and lifecycle management in Python's
`unittest` framework. Covers method-level setUp/tearDown, class-level setUpClass/tearDownClass,
module-level fixtures, robust cleanups via addCleanup (LIFO), temporary filesystem isolation,
database transaction isolation, environment variable patching with restoration, subTest iteration,
reusable fixture mixins, and an architectural Scoped Fixture Dependency Injection Container.

Every question contains standalone runnable exercises verified with 100% assertions.
"""

import unittest
import io
import os
import tempfile
import sqlite3
from typing import List, Dict, Any, Callable, Optional


# =====================================================================
# Q1: Method-Level Fixtures: setUp and tearDown Lifecycle
# =====================================================================
lifecycle_log: List[str] = []


class MethodFixtureTestCase(unittest.TestCase):
    def setUp(self):
        lifecycle_log.append("setUp")
        self.resource = [1, 2, 3]

    def tearDown(self):
        lifecycle_log.append("tearDown")
        self.resource.clear()

    def test_alpha(self):
        lifecycle_log.append("test_alpha")
        self.resource.append(4)
        self.assertEqual(len(self.resource), 4)

    def test_beta(self):
        lifecycle_log.append("test_beta")
        # Assert clean isolated state from setUp
        self.assertEqual(len(self.resource), 3)


def q1_method_level_fixtures():
    global lifecycle_log
    lifecycle_log = []

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(MethodFixtureTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 2
    # Verify exact chronological order
    expected_order = [
        "setUp", "test_alpha", "tearDown",
        "setUp", "test_beta", "tearDown"
    ]
    assert lifecycle_log == expected_order

    print("=== Q1: Method-Level Fixtures (setUp / tearDown) Verified ===")


# =====================================================================
# Q2: Class-Level Fixtures: setUpClass and tearDownClass
# =====================================================================
class_lifecycle_log: List[str] = []


class ClassFixtureTestCase(unittest.TestCase):
    shared_db_connection = None

    @classmethod
    def setUpClass(cls):
        class_lifecycle_log.append("setUpClass")
        cls.shared_db_connection = {"connected": True, "pool_id": 999}

    @classmethod
    def tearDownClass(cls):
        class_lifecycle_log.append("tearDownClass")
        cls.shared_db_connection = None

    def test_query_one(self):
        class_lifecycle_log.append("test_1")
        self.assertIsNotNone(self.shared_db_connection)
        self.assertEqual(self.shared_db_connection["pool_id"], 999)

    def test_query_two(self):
        class_lifecycle_log.append("test_2")
        self.assertTrue(self.shared_db_connection["connected"])


def q2_class_level_fixtures():
    global class_lifecycle_log
    class_lifecycle_log = []

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ClassFixtureTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 2
    assert class_lifecycle_log == ["setUpClass", "test_1", "test_2", "tearDownClass"]

    print("=== Q2: Class-Level Fixtures (setUpClass / tearDownClass) Verified ===")


# =====================================================================
# Q3: Module-Level Fixtures (setUpModule and tearDownModule)
# =====================================================================
module_log: List[str] = []


def fake_setup_module():
    module_log.append("module_setup")


def fake_teardown_module():
    module_log.append("module_teardown")


class DummyCase1(unittest.TestCase):
    def test_m1(self):
        module_log.append("test_m1")


class DummyCase2(unittest.TestCase):
    def test_m2(self):
        module_log.append("test_m2")


def q3_module_level_fixtures():
    """Demonstrates executing module fixtures surrounding multiple TestCases."""
    global module_log
    module_log = []

    fake_setup_module()
    suite = unittest.TestSuite()
    suite.addTest(DummyCase1("test_m1"))
    suite.addTest(DummyCase2("test_m2"))
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)
    fake_teardown_module()

    assert result.wasSuccessful() is True
    assert module_log == ["module_setup", "test_m1", "test_m2", "module_teardown"]

    print("=== Q3: Module-Level Fixture Lifecycle Verified ===")


# =====================================================================
# Q4: Robust Cleanup Handlers via addCleanup (LIFO Execution)
# =====================================================================
cleanup_log: List[str] = []


class AddCleanupTestCase(unittest.TestCase):
    def setUp(self):
        # Register cleanups in LIFO order
        self.addCleanup(lambda: cleanup_log.append("cleanup_step_1"))
        self.addCleanup(lambda: cleanup_log.append("cleanup_step_2"))

    def test_action(self):
        cleanup_log.append("test_action_run")


def q4_add_cleanup_lifo():
    global cleanup_log
    cleanup_log = []

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(AddCleanupTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    # addCleanup executes in Last-In First-Out order
    assert cleanup_log == ["test_action_run", "cleanup_step_2", "cleanup_step_1"]

    print("=== Q4: addCleanup LIFO Execution Verified ===")


# =====================================================================
# Q5: Temporary Filesystem Isolation Fixture
# =====================================================================
class TempDirectoryFixtureTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        # Guarantee cleanup even if tests fail or throw exceptions
        self.addCleanup(self._cleanup_dir)

    def _cleanup_dir(self):
        if os.path.exists(self.temp_dir):
            for fname in os.listdir(self.temp_dir):
                os.remove(os.path.join(self.temp_dir, fname))
            os.rmdir(self.temp_dir)

    def test_file_operations(self):
        test_file = os.path.join(self.temp_dir, "config.json")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write('{"env": "test"}')

        self.assertTrue(os.path.exists(test_file))
        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content, '{"env": "test"}')


def q5_temp_filesystem_fixture():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TempDirectoryFixtureTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 1

    print("=== Q5: Temporary Filesystem Isolation Fixture Verified ===")


# =====================================================================
# Q6: Database Transaction and Table Seeding Isolation
# =====================================================================
class DatabaseIsolationTestCase(unittest.TestCase):
    conn: sqlite3.Connection

    @classmethod
    def setUpClass(cls):
        # Create schema once for the class
        cls.conn = sqlite3.connect(":memory:")
        cls.conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);")

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def setUp(self):
        # Reset and seed table before each test
        self.conn.execute("DELETE FROM users;")
        self.conn.execute("INSERT INTO users (id, name) VALUES (1, 'Alice');")
        self.conn.commit()

    def test_insert_user(self):
        self.conn.execute("INSERT INTO users (id, name) VALUES (2, 'Bob');")
        self.conn.commit()
        cursor = self.conn.execute("SELECT COUNT(*) FROM users;")
        self.assertEqual(cursor.fetchone()[0], 2)

    def test_isolation_from_previous_test(self):
        # Must only see 'Alice' (count=1), proves Bob from test_insert_user was wiped!
        cursor = self.conn.execute("SELECT COUNT(*) FROM users;")
        self.assertEqual(cursor.fetchone()[0], 1)
        cursor = self.conn.execute("SELECT name FROM users WHERE id = 1;")
        self.assertEqual(cursor.fetchone()[0], "Alice")


def q6_database_transaction_isolation():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DatabaseIsolationTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 2

    print("=== Q6: Database State Isolation Verified ===")


# =====================================================================
# Q7: Environment Variable Patching with Auto-Restoration
# =====================================================================
class EnvPatchingTestCase(unittest.TestCase):
    def patch_env(self, key: str, value: str):
        old_value = os.environ.get(key)
        os.environ[key] = value

        def restore():
            if old_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = old_value

        self.addCleanup(restore)

    def test_custom_env_variable(self):
        self.patch_env("APP_SECRET_KEY", "temporary_test_token_123")
        self.assertEqual(os.environ.get("APP_SECRET_KEY"), "temporary_test_token_123")


def q7_environment_variable_patching():
    # Ensure key does not exist initially
    os.environ.pop("APP_SECRET_KEY", None)

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(EnvPatchingTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    # Verify environment restored cleanly
    assert "APP_SECRET_KEY" not in os.environ

    print("=== Q7: Environment Variable Patching with Auto-Restoration Verified ===")


# =====================================================================
# Q8: SubTest Context Manager for Isolated Iterative Assertions
# =====================================================================
class SubTestTestCase(unittest.TestCase):
    def test_even_numbers(self):
        cases = [(2, True), (4, True), (6, True), (7, False), (8, True)]
        for number, expected_even in cases:
            with self.subTest(num=number, expected=expected_even):
                is_even = (number % 2 == 0)
                self.assertEqual(is_even, expected_even)


def q8_subtest_context_manager():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SubTestTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 1

    print("=== Q8: subTest Context Manager Verified ===")


# =====================================================================
# Q9: Reusable Fixture Mixins
# =====================================================================
class MemoryCacheMixin:
    """Reusable fixture mixin providing in-memory key-value cache with cleanup."""
    cache: Dict[str, Any]

    def setUp(self):
        super().setUp()
        self.cache = {}
        self.addCleanup(self.cache.clear)


class UserSessionMixin:
    """Reusable fixture mixin providing mock authentication session."""
    session: Dict[str, Any]

    def setUp(self):
        super().setUp()
        self.session = {"user_id": 101, "role": "admin"}
        self.addCleanup(self.session.clear)


class CompositeServiceTestCase(MemoryCacheMixin, UserSessionMixin, unittest.TestCase):
    def test_service_with_mixins(self):
        # Both cache and session are initialized via multiple inheritance
        self.assertEqual(self.session["role"], "admin")
        self.cache["token"] = "xyz"
        self.assertEqual(self.cache["token"], "xyz")


def q9_reusable_fixture_mixins():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CompositeServiceTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 1

    print("=== Q9: Reusable Fixture Mixins Verified ===")


# =====================================================================
# Q10: Architectural Scoped Fixture Dependency Injection Container
# =====================================================================
class FixtureScope:
    FUNCTION = "function"
    SESSION = "session"


class FixtureContainer:
    """
    Lightweight dependency injection fixture container:
    - Supports 'session' and 'function' scoped fixtures
    - Automatic tearDown invocation in reverse registration order
    """
    def __init__(self):
        self._session_cache: Dict[str, Any] = {}
        self._session_cleanups: List[Callable[[], None]] = []

    def session_fixture(self, name: str, factory: Callable[[], Any], cleanup: Optional[Callable[[Any], None]] = None):
        if name not in self._session_cache:
            instance = factory()
            self._session_cache[name] = instance
            if cleanup:
                self._session_cleanups.append(lambda: cleanup(instance))
        return self._session_cache[name]

    def close(self):
        while self._session_cleanups:
            cb = self._session_cleanups.pop()
            cb()
        self._session_cache.clear()


class DIIntegrationTestCase(unittest.TestCase):
    container = FixtureContainer()
    events = []

    @classmethod
    def setUpClass(cls):
        cls.events = []
        cls.db = cls.container.session_fixture(
            "db_client",
            factory=lambda: {"client_id": "session_001"},
            cleanup=lambda res: cls.events.append(f"closed_{res['client_id']}")
        )

    @classmethod
    def tearDownClass(cls):
        cls.container.close()

    def test_use_fixture_1(self):
        self.assertEqual(self.db["client_id"], "session_001")

    def test_use_fixture_2(self):
        self.assertEqual(self.db["client_id"], "session_001")


def q10_architectural_fixture_container():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DIIntegrationTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 2
    # Verify cleanup ran on container close
    assert DIIntegrationTestCase.events == ["closed_session_001"]

    print("=== Q10: Architectural Scoped Fixture Container Verified ===")


# =====================================================================
# Main Test Runner
# =====================================================================
if __name__ == "__main__":
    q1_method_level_fixtures()
    q2_class_level_fixtures()
    q3_module_level_fixtures()
    q4_add_cleanup_lifo()
    q5_temp_filesystem_fixture()
    q6_database_transaction_isolation()
    q7_environment_variable_patching()
    q8_subtest_context_manager()
    q9_reusable_fixture_mixins()
    q10_architectural_fixture_container()

    print("\nAll 10 test fixtures practice questions passed successfully!")
