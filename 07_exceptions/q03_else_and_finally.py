"""
Topic 07: Exceptions - Question 03: else and finally

A comprehensive collection of 10 standalone, runnable exercises exploring
the semantics, execution order, gotchas, and enterprise cleanup patterns
of Python's `else` and `finally` clauses in exception handling.

Questions Covered:
 1. The else Clause: Runs strictly when NO exception occurs in the try block.
 2. Why else Matters: Narrowing try scope to prevent accidental exception trapping.
 3. The finally Clause: Guaranteed execution for cleanup regardless of success or failure.
 4. Full Quartet Lifecycle: try -> except -> else -> finally execution timeline.
 5. Return Overrides in finally: How finally return overrides try/except return values.
 6. Exception Swallowing Quirk: How returning from finally suppresses active exceptions.
 7. Manual Resource Cleanup: Releasing locks and resetting state via finally.
 8. Pure try...finally: Resource lifecycle management without exception suppression.
 9. Loop Control Interactions: How break and continue execute finally before jumping.
10. Advanced Project: Distributed Lease & Lock Manager with heartbeat and fail-safe release.
"""

import time
from typing import Any


# ==============================================================================
# Question 1: The else Clause Fundamentals
# ==============================================================================
def exercise_q1_else_fundamentals() -> None:
    """
    Demonstrate that the `else` block executes ONLY when the `try` block
    completes cleanly without raising any exceptions.
    """
    print("=== Q1: The else Clause Fundamentals ===")

    def test_run(should_raise: bool) -> tuple[str, bool]:
        else_executed = False
        try:
            if should_raise:
                raise ValueError("Intentional error")
        except ValueError:
            return "CAUGHT_ERROR", else_executed
        else:
            else_executed = True
            return "CLEAN_SUCCESS", else_executed

    status_clean, else_clean = test_run(should_raise=False)
    assert status_clean == "CLEAN_SUCCESS"
    assert else_clean is True

    status_err, else_err = test_run(should_raise=True)
    assert status_err == "CAUGHT_ERROR"
    assert else_err is False

    print(f"  Clean run: status={status_clean}, else_ran={else_clean}")
    print(f"  Error run: status={status_err}, else_ran={else_err}")


# ==============================================================================
# Question 2: Why else Matters (Narrowing Try Scope)
# ==============================================================================
def exercise_q2_narrowing_try_scope() -> None:
    """
    Illustrate why placing post-operation logic in `else` prevents accidental
    trapping of unexpected errors from subsequent code.
    """
    print("\n=== Q2: Why else Matters (Narrowing Try Scope) ===")

    # BAD PATTERN: everything in try block
    # If process_parsed_data raises a ValueError, it gets mistakenly caught by the
    # parsing except block!
    def bad_parse_and_process(val_str: str) -> str:
        try:
            val = int(val_str)
            if val < 0:
                raise ValueError("Business rule violation: negative value not permitted!")
            return f"Processed: {val}"
        except ValueError as exc:
            # We mistakenly catch our own business rule violation here as a parse error!
            return f"PARSE_ERROR: {exc}"

    # GOOD PATTERN: narrow try block, business logic in else
    def good_parse_and_process(val_str: str) -> str:
        try:
            val = int(val_str)
        except ValueError as exc:
            return f"PARSE_ERROR: {exc}"
        else:
            # Code here is NOT guarded by the int parsing except block
            if val < 0:
                raise ValueError("Business rule violation: negative value not permitted!")
            return f"Processed: {val}"

    # 1. When passed non-integer "abc":
    assert "PARSE_ERROR" in bad_parse_and_process("abc")
    assert "PARSE_ERROR" in good_parse_and_process("abc")

    # 2. When passed negative integer "-10":
    # Bad pattern falsely reports it as a PARSE_ERROR
    assert "PARSE_ERROR" in bad_parse_and_process("-10")

    # Good pattern allows the business rule violation to propagate properly!
    caught_business_rule = False
    try:
        good_parse_and_process("-10")
    except ValueError as exc:
        if "Business rule violation" in str(exc):
            caught_business_rule = True

    assert caught_business_rule is True
    print("  Narrow try/else successfully separated syntax parsing errors from business rule errors.")


# ==============================================================================
# Question 3: The finally Clause Fundamentals
# ==============================================================================
def exercise_q3_finally_fundamentals() -> None:
    """
    Demonstrate that `finally` is guaranteed to execute regardless of whether
    the `try` block succeeded, raised a caught error, or raised an unhandled error.
    """
    print("\n=== Q3: The finally Clause Fundamentals ===")

    trail: list[str] = []

    def run_flow(scenario: str) -> None:
        try:
            trail.append("TRY")
            if scenario == "caught":
                raise KeyError("test key")
            elif scenario == "unhandled":
                raise TypeError("test type")
        except KeyError:
            trail.append("EXCEPT_KEY")
        finally:
            trail.append("FINALLY")

    # Clean flow
    trail.clear()
    run_flow("clean")
    assert trail == ["TRY", "FINALLY"]

    # Caught error flow
    trail.clear()
    run_flow("caught")
    assert trail == ["TRY", "EXCEPT_KEY", "FINALLY"]

    # Unhandled error flow
    trail.clear()
    try:
        run_flow("unhandled")
    except TypeError:
        trail.append("CALLER_CAUGHT")
    assert trail == ["TRY", "FINALLY", "CALLER_CAUGHT"]

    print("  Clean trail:     ['TRY', 'FINALLY']")
    print("  Caught trail:    ['TRY', 'EXCEPT_KEY', 'FINALLY']")
    print("  Unhandled trail: ['TRY', 'FINALLY', 'CALLER_CAUGHT']")


# ==============================================================================
# Question 4: Full Quartet Lifecycle (try / except / else / finally)
# ==============================================================================
def exercise_q4_full_quartet_lifecycle() -> None:
    """
    Trace the complete quartet lifecycle across both success and failure pathways.
    """
    print("\n=== Q4: Full Quartet Lifecycle ===")

    def quartet_runner(divide_by: int) -> tuple[int | None, list[str]]:
        events: list[str] = []
        result = None
        try:
            events.append("1: TRY")
            result = 100 // divide_by
        except ZeroDivisionError:
            events.append("2: EXCEPT")
        else:
            events.append("3: ELSE")
        finally:
            events.append("4: FINALLY")
        return result, events

    res_ok, events_ok = quartet_runner(5)
    assert res_ok == 20
    assert events_ok == ["1: TRY", "3: ELSE", "4: FINALLY"]

    res_err, events_err = quartet_runner(0)
    assert res_err is None
    assert events_err == ["1: TRY", "2: EXCEPT", "4: FINALLY"]

    print(f"  Success path: {events_ok}")
    print(f"  Failure path: {events_err}")


# ==============================================================================
# Question 5: Return Overrides in finally
# ==============================================================================
def exercise_q5_return_override_in_finally() -> None:
    """
    Demonstrate that if a `finally` block contains a `return` statement,
    it overrides ANY previous return value from `try` or `except`.
    (Note: This is considered an anti-pattern in production code!)
    """
    print("\n=== Q5: Return Overrides in finally ===")

    def tricky_return() -> str:
        try:
            return "VALUE_FROM_TRY"
        except Exception:
            return "VALUE_FROM_EXCEPT"
        finally:
            # Overrides VALUE_FROM_TRY!
            return "OVERRIDDEN_BY_FINALLY"

    result = tricky_return()
    assert result == "OVERRIDDEN_BY_FINALLY"

    print(f"  Tricky return result: '{result}' (finally hijacked try's return value)")


# ==============================================================================
# Question 6: Exception Swallowing Quirk in finally
# ==============================================================================
def exercise_q6_exception_swallowing_in_finally() -> None:
    """
    Demonstrate that returning from a `finally` block suppresses and swallows
    any unhandled exceptions that were actively propagating.
    """
    print("\n=== Q6: Exception Swallowing Quirk in finally ===")

    def dangerous_suppression() -> str:
        try:
            # Unhandled RuntimeError
            raise RuntimeError("CRITICAL HARDWARE FAILURE!")
        finally:
            # Returning here accidentally swallows the RuntimeError!
            return "SUPPRESSED_ACCIDENTALLY"

    res = dangerous_suppression()
    assert res == "SUPPRESSED_ACCIDENTALLY"

    print("  Demonstrated exception suppression: RuntimeError was swallowed by finally return.")


# ==============================================================================
# Question 7: Manual Resource Cleanup via finally
# ==============================================================================
class MockLock:
    """Simple lock object tracking acquisition state."""

    def __init__(self) -> None:
        self.locked = False

    def acquire(self) -> None:
        self.locked = True

    def release(self) -> None:
        self.locked = False


def exercise_q7_manual_resource_cleanup() -> None:
    """
    Demonstrate acquiring a resource before try, and guaranteeing release in finally.
    """
    print("\n=== Q7: Manual Resource Cleanup via finally ===")

    lock = MockLock()
    lock.acquire()
    assert lock.locked is True

    try:
        # Simulate business logic that crashes
        raise ArithmeticError("Simulation crash")
    except ArithmeticError:
        pass
    finally:
        # Guaranteed lock release
        lock.release()

    assert lock.locked is False
    print(f"  Lock acquisition restored to unlocked state in finally: {not lock.locked}")


# ==============================================================================
# Question 8: Pure try...finally (No except)
# ==============================================================================
def exercise_q8_pure_try_finally() -> None:
    """
    Demonstrate `try...finally` without `except`, where cleanup is guaranteed
    locally while allowing exceptions to propagate transparently to the caller.
    """
    print("\n=== Q8: Pure try...finally ===")

    cleaned_up = False

    def perform_action(trigger_error: bool) -> None:
        nonlocal cleaned_up
        try:
            if trigger_error:
                raise ValueError("Action failed")
        finally:
            cleaned_up = True

    # Error scenario
    caught = False
    try:
        perform_action(trigger_error=True)
    except ValueError:
        caught = True

    assert caught is True
    assert cleaned_up is True
    print(f"  Exception propagated cleanly to caller; finally cleaned up: {cleaned_up}")


# ==============================================================================
# Question 9: Loop Control Interactions (break/continue with finally)
# ==============================================================================
def exercise_q9_loop_control_with_finally() -> None:
    """
    Demonstrate that `break` or `continue` inside a try block will still
    cause the `finally` block to execute BEFORE the jump occurs.
    """
    print("\n=== Q9: Loop Control Interactions ===")

    events: list[str] = []

    for item in [1, 2, 3]:
        try:
            events.append(f"TRY_{item}")
            if item == 2:
                # break triggers finally before exiting loop!
                break
        finally:
            events.append(f"FINALLY_{item}")

    assert events == ["TRY_1", "FINALLY_1", "TRY_2", "FINALLY_2"]
    print(f"  Loop break executed finally before terminating: {events}")


# ==============================================================================
# Question 10: Advanced Project - Distributed Lease & Lock Manager
# ==============================================================================
class DistributedLeaseManager:
    """
    Enterprise-grade distributed lease simulator. Ensures lease tokens are
    released in finally, heartbeats are recorded in else, and failures are
    cleanly audited.
    """

    def __init__(self, resource_id: str) -> None:
        self.resource_id = resource_id
        self.held_by: str | None = None
        self.heartbeat_count = 0
        self.release_count = 0

    def acquire(self, client_id: str) -> bool:
        if self.held_by is None:
            self.held_by = client_id
            return True
        return False

    def heartbeat(self, client_id: str) -> None:
        if self.held_by == client_id:
            self.heartbeat_count += 1
        else:
            raise PermissionError("Client does not hold the lease")

    def release(self, client_id: str) -> None:
        if self.held_by == client_id:
            self.held_by = None
            self.release_count += 1

    def execute_critical_section(self, client_id: str, action_fn: Any) -> dict[str, Any]:
        if not self.acquire(client_id):
            return {"status": "FAILED_TO_ACQUIRE"}

        result = None
        error = None

        try:
            result = action_fn()
        except Exception as exc:
            error = str(exc)
        else:
            # Only heartbeat when action succeeded
            self.heartbeat(client_id)
        finally:
            # Always guarantee release regardless of exception
            self.release(client_id)

        return {
            "status": "SUCCESS" if error is None else "FAILED",
            "result": result,
            "error": error,
            "lease_freed": self.held_by is None,
        }


def exercise_q10_distributed_lease_manager() -> None:
    """
    Test DistributedLeaseManager across both successful and crashing workloads.
    """
    print("\n=== Q10: Distributed Lease & Lock Manager ===")

    manager = DistributedLeaseManager("DB_SHARD_01")

    # 1. Successful execution
    res1 = manager.execute_critical_section("worker_A", lambda: "COMPUTED_OUTPUT")
    assert res1["status"] == "SUCCESS"
    assert res1["result"] == "COMPUTED_OUTPUT"
    assert res1["lease_freed"] is True
    assert manager.heartbeat_count == 1
    assert manager.release_count == 1

    # 2. Failing execution
    def buggy_action() -> None:
        raise RuntimeError("Network split during compute")

    res2 = manager.execute_critical_section("worker_B", buggy_action)
    assert res2["status"] == "FAILED"
    assert "Network split" in res2["error"]
    assert res2["lease_freed"] is True  # Released even on crash!
    assert manager.release_count == 2
    assert manager.heartbeat_count == 1  # Heartbeat NOT incremented on failure

    print(f"  Successful transaction: {res1}")
    print(f"  Failed transaction:     {res2}")
    print(f"  Guaranteed lease release verified across all scenarios.")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_else_fundamentals()
    exercise_q2_narrowing_try_scope()
    exercise_q3_finally_fundamentals()
    exercise_q4_full_quartet_lifecycle()
    exercise_q5_return_override_in_finally()
    exercise_q6_exception_swallowing_in_finally()
    exercise_q7_manual_resource_cleanup()
    exercise_q8_pure_try_finally()
    exercise_q9_loop_control_with_finally()
    exercise_q10_distributed_lease_manager()

    print("\nAll 10 else and finally questions executed and asserted successfully!")
