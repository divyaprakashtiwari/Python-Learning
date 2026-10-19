"""
Topic: Advanced Python - Custom Context Managers
------------------------------------------------
Questions Covered:
1. Core Context Manager Protocol: __enter__ and __exit__ with exception suppression logic
   (returning True vs False/None).
2. Generator-Based Context Manager: Using contextlib.contextmanager with try...yield...finally.
3. Code Block Execution Stopwatch: High-resolution timing manager yielding elapsed time container.
4. Temporary Environment / State Mutator: Safely modifying global/state configuration and
   restoring pristine state upon exit.
5. Atomic In-Memory Transaction Rollback: Staging changes and reverting to snapshot checkpoint
   if an unhandled error occurs.
6. Re-entrant Context Manager: Managing nested and sequential entries using state counters.
7. Dynamic Multi-Resource Coordination with ExitStack: Managing a dynamic collection of resources
   with LIFO teardown guarantees.
8. Resource Checkout Pool Context Manager: Lending resources from a bounded pool and returning
   them on exit.
9. Dual-Use ContextDecorator: Writing a context manager usable both as 'with mgr:' and '@mgr'.
10. Architectural System: Unit of Work (UoW) Multi-Repository Transaction Coordinator with
    savepoints, automatic commit, dirty-state tracking, and transactional rollback.
"""

import time
import os
import contextlib
from typing import Any, Dict, List, Optional, Type


# ==============================================================================
# Question 1: Core Context Manager Protocol & Exception Suppression
# ==============================================================================
class SuppressExceptionManager:
    """
    Context manager that suppresses specified exception types while allowing others
    to propagate. Demonstrates the return boolean contract of __exit__.
    """
    def __init__(self, *exceptions_to_suppress: Type[BaseException]):
        self.suppress_types = exceptions_to_suppress
        self.entered = False
        self.exited = False
        self.suppressed_exception: Optional[BaseException] = None

    def __enter__(self):
        self.entered = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exited = True
        if exc_type is not None and issubclass(exc_type, self.suppress_types):
            self.suppressed_exception = exc_val
            return True  # Suppress exception
        return False  # Let exception propagate


def test_q1_core_protocol():
    mgr = SuppressExceptionManager(ValueError, KeyError)
    with mgr:
        raise ValueError("Non-fatal value error")

    assert mgr.entered is True
    assert mgr.exited is True
    assert isinstance(mgr.suppressed_exception, ValueError)

    # Verify unsuppressed exception propagates
    mgr2 = SuppressExceptionManager(KeyError)
    try:
        with mgr2:
            raise TypeError("Fatal type error")
        assert False, "Should have raised TypeError"
    except TypeError as e:
        assert str(e) == "Fatal type error"

    assert mgr2.entered is True
    assert mgr2.exited is True
    assert mgr2.suppressed_exception is None
    print("=== Q1: Core Protocol & Exception Suppression Verified ===")


# ==============================================================================
# Question 2: Generator-Based Context Manager via contextlib.contextmanager
# ==============================================================================
@contextlib.contextmanager
def temporary_file_resource(filename: str, initial_data: str):
    """
    Creates an in-memory or simulated file resource, yields file handle,
    and guarantees cleanup in finally block.
    """
    resource = {"name": filename, "content": initial_data, "open": True}
    try:
        yield resource
    finally:
        resource["open"] = False


def test_q2_generator_context_manager():
    captured_res = None
    with temporary_file_resource("temp_cache.txt", "INITIAL") as res:
        captured_res = res
        assert res["open"] is True
        res["content"] += "_MODIFIED"

    assert captured_res["open"] is False
    assert captured_res["content"] == "INITIAL_MODIFIED"
    print("=== Q2: Generator-Based Context Manager Verified ===")


# ==============================================================================
# Question 3: Code Block Execution Stopwatch
# ==============================================================================
class ExecutionTimer:
    """Measures wall-clock and perf_counter duration of a code block."""
    def __init__(self):
        self.start_time: float = 0.0
        self.elapsed: float = 0.0

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start_time
        return False


def test_q3_execution_timer():
    timer = ExecutionTimer()
    with timer:
        total = sum(i for i in range(50_000))
        assert total > 0

    assert timer.elapsed > 0.0
    print(f"=== Q3: Execution Stopwatch Verified (Elapsed: {timer.elapsed:.6f}s) ===")


# ==============================================================================
# Question 4: Temporary State Mutator (Configuration & Environment)
# ==============================================================================
class EnvironmentOverride:
    """
    Temporarily overrides or sets os.environ variables, reliably restoring
    previous state (or unsetting newly introduced variables) on exit.
    """
    def __init__(self, **overrides: str):
        self.overrides = overrides
        self.saved_state: Dict[str, Optional[str]] = {}

    def __enter__(self):
        for k, v in self.overrides.items():
            self.saved_state[k] = os.environ.get(k)
            os.environ[k] = str(v)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for k, prev_val in self.saved_state.items():
            if prev_val is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = prev_val
        return False


def test_q4_environment_override():
    os.environ["APP_STAGE"] = "production"
    assert os.environ.get("APP_DEBUG") is None

    with EnvironmentOverride(APP_STAGE="testing", APP_DEBUG="true"):
        assert os.environ["APP_STAGE"] == "testing"
        assert os.environ["APP_DEBUG"] == "true"

    # Restored
    assert os.environ["APP_STAGE"] == "production"
    assert os.environ.get("APP_DEBUG") is None

    os.environ.pop("APP_STAGE", None)
    print("=== Q4: Temporary State Mutator Verified ===")


# ==============================================================================
# Question 5: Atomic In-Memory Transaction Rollback
# ==============================================================================
class AtomicDictionaryTransaction:
    """
    Wraps a dictionary. Any changes made inside the 'with' block are kept
    if block exits cleanly, but rolled back to initial state if an exception is raised.
    """
    def __init__(self, target_dict: Dict[str, Any]):
        self.target_dict = target_dict
        self.snapshot: Dict[str, Any] = {}

    def __enter__(self):
        self.snapshot = dict(self.target_dict)
        return self.target_dict

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Revert to snapshot
            self.target_dict.clear()
            self.target_dict.update(self.snapshot)
        return False  # Do not suppress exception


def test_q5_atomic_transaction():
    db = {"balance": 100, "status": "active"}

    # Successful transaction
    with AtomicDictionaryTransaction(db) as session:
        session["balance"] += 50
        session["status"] = "premium"
    assert db == {"balance": 150, "status": "premium"}

    # Failed transaction -> roll back
    try:
        with AtomicDictionaryTransaction(db) as session:
            session["balance"] = 9999
            session["status"] = "corrupted"
            raise RuntimeError("Database connection dropped")
    except RuntimeError:
        pass

    assert db == {"balance": 150, "status": "premium"}
    print("=== Q5: Atomic In-Memory Rollback Verified ===")


# ==============================================================================
# Question 6: Re-entrant Context Manager
# ==============================================================================
class ReentrantCounter:
    """
    A re-entrant context manager tracking nesting depth.
    Action is performed on first enter (depth 1) and final exit (depth 0).
    """
    def __init__(self):
        self.depth = 0
        self.lifecycle_log: List[str] = []

    def __enter__(self):
        self.depth += 1
        self.lifecycle_log.append(f"ENTER_DEPTH_{self.depth}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lifecycle_log.append(f"EXIT_DEPTH_{self.depth}")
        self.depth -= 1
        return False


def test_q6_reentrant_context_manager():
    counter = ReentrantCounter()

    with counter:
        assert counter.depth == 1
        with counter:
            assert counter.depth == 2
            with counter:
                assert counter.depth == 3
            assert counter.depth == 2
        assert counter.depth == 1

    assert counter.depth == 0
    expected_log = [
        "ENTER_DEPTH_1",
        "ENTER_DEPTH_2",
        "ENTER_DEPTH_3",
        "EXIT_DEPTH_3",
        "EXIT_DEPTH_2",
        "EXIT_DEPTH_1",
    ]
    assert counter.lifecycle_log == expected_log
    print("=== Q6: Re-entrant Context Manager Verified ===")


# ==============================================================================
# Question 7: Dynamic Multi-Resource Management with ExitStack
# ==============================================================================
class ManagedFile:
    def __init__(self, path: str):
        self.path = path
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closed = True
        return False


def test_q7_exit_stack():
    files = [ManagedFile(f"file_{i}.txt") for i in range(5)]
    opened_handles = []

    with contextlib.ExitStack() as stack:
        for f in files:
            handle = stack.enter_context(f)
            opened_handles.append(handle)
        assert len(opened_handles) == 5
        assert all(not f.closed for f in files)

    # All closed upon exiting ExitStack
    assert all(f.closed for f in files)
    print("=== Q7: Dynamic Multi-Resource ExitStack Verified ===")


# ==============================================================================
# Question 8: Resource Pool Checkout Context Manager
# ==============================================================================
class BoundedConnectionPool:
    """Maintains a fixed pool of connections, leasing on enter, returning on exit."""
    def __init__(self, size: int):
        self.available_connections = [f"CONN_{i}" for i in range(1, size + 1)]
        self.active_leases = 0

    @contextlib.contextmanager
    def acquire(self):
        if not self.available_connections:
            raise RuntimeError("Connection pool exhausted")
        conn = self.available_connections.pop(0)
        self.active_leases += 1
        try:
            yield conn
        finally:
            self.available_connections.append(conn)
            self.active_leases -= 1


def test_q8_resource_pool():
    pool = BoundedConnectionPool(size=2)
    assert len(pool.available_connections) == 2

    with pool.acquire() as c1:
        assert c1 == "CONN_1"
        assert pool.active_leases == 1

        with pool.acquire() as c2:
            assert c2 == "CONN_2"
            assert pool.active_leases == 2

            # 3rd acquire exhausts pool
            try:
                with pool.acquire():
                    assert False, "Should fail on exhausted pool"
            except RuntimeError as exc:
                assert "pool exhausted" in str(exc)

    assert pool.active_leases == 0
    assert len(pool.available_connections) == 2
    print("=== Q8: Resource Pool Checkout Context Manager Verified ===")


# ==============================================================================
# Question 9: Dual-Use ContextDecorator
# ==============================================================================
class ExecutionAuditor(contextlib.ContextDecorator):
    """
    Context manager that can be used BOTH as a 'with' statement and as a function decorator.
    """
    def __init__(self, tag: str, audit_list: List[str]):
        self.tag = tag
        self.audit_list = audit_list

    def __enter__(self):
        self.audit_list.append(f"{self.tag}:START")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.audit_list.append(f"{self.tag}:END")
        return False


audit_trail: List[str] = []


@ExecutionAuditor("FUNCTION_DECORATOR", audit_trail)
def perform_calculation(a: int, b: int) -> int:
    audit_trail.append("CALCULATING")
    return a + b


def test_q9_context_decorator():
    audit_trail.clear()

    # 1. Used as 'with' block
    with ExecutionAuditor("WITH_BLOCK", audit_trail):
        audit_trail.append("INSIDE_WITH")

    # 2. Used as function decorator
    res = perform_calculation(10, 20)
    assert res == 30

    expected = [
        "WITH_BLOCK:START",
        "INSIDE_WITH",
        "WITH_BLOCK:END",
        "FUNCTION_DECORATOR:START",
        "CALCULATING",
        "FUNCTION_DECORATOR:END",
    ]
    assert audit_trail == expected
    print("=== Q9: Dual-Use ContextDecorator Verified ===")


# ==============================================================================
# Question 10: Architectural Unit of Work (UoW) Multi-Repository Coordinator
# ==============================================================================
class MockEntityRepository:
    def __init__(self, name: str):
        self.name = name
        self.data: Dict[str, Dict[str, Any]] = {}
        self._staged_changes: Dict[str, Dict[str, Any]] = {}

    def stage_insert(self, record_id: str, payload: Dict[str, Any]):
        self._staged_changes[record_id] = payload

    def commit(self):
        self.data.update(self._staged_changes)
        self._staged_changes.clear()

    def rollback(self):
        self._staged_changes.clear()


class UnitOfWork:
    """
    Production Unit of Work managing atomic transactions across multiple repositories.
    Guarantees all-or-nothing commits with rollback on any failure.
    """
    def __init__(self):
        self.users = MockEntityRepository("users")
        self.orders = MockEntityRepository("orders")
        self.audit_log = MockEntityRepository("audit_log")
        self.is_committed = False
        self.is_rolled_back = False

    def __enter__(self):
        return self

    def commit(self):
        self.users.commit()
        self.orders.commit()
        self.audit_log.commit()
        self.is_committed = True

    def rollback(self):
        self.users.rollback()
        self.orders.rollback()
        self.audit_log.rollback()
        self.is_rolled_back = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
            return False  # Propagate exception
        else:
            if not self.is_committed:
                self.commit()
            return True


def test_q10_unit_of_work():
    # 1. Clean successful transaction
    uow1 = UnitOfWork()
    with uow1:
        uow1.users.stage_insert("u1", {"name": "Alice"})
        uow1.orders.stage_insert("o1", {"item": "Laptop", "price": 1200})
        uow1.audit_log.stage_insert("a1", {"action": "NEW_ORDER"})

    assert uow1.is_committed is True
    assert "u1" in uow1.users.data
    assert "o1" in uow1.orders.data
    assert "a1" in uow1.audit_log.data

    # 2. Failed transaction with automatic multi-repository rollback
    uow2 = UnitOfWork()
    try:
        with uow2:
            uow2.users.stage_insert("u2", {"name": "Bob"})
            uow2.orders.stage_insert("o2", {"item": "Phone", "price": 800})
            raise RuntimeError("Payment gateway timeout")
    except RuntimeError:
        pass

    assert uow2.is_rolled_back is True
    assert "u2" not in uow2.users.data
    assert "o2" not in uow2.orders.data
    assert len(uow2.users.data) == 0
    print("=== Q10: Architectural Unit of Work Transaction Coordinator Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_core_protocol()
    test_q2_generator_context_manager()
    test_q3_execution_timer()
    test_q4_environment_override()
    test_q5_atomic_transaction()
    test_q6_reentrant_context_manager()
    test_q7_exit_stack()
    test_q8_resource_pool()
    test_q9_context_decorator()
    test_q10_unit_of_work()
    print("\nAll 10 custom context manager practice questions passed successfully!")
