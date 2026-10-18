"""
Topic 07: Exceptions - Question 07: Context Manager Exception Handling

A comprehensive collection of 10 standalone, runnable exercises exploring
how context managers intercept, suppress, transform, and unwind exceptions
using `__exit__`, `contextlib.contextmanager`, and `contextlib.suppress`.

Questions Covered:
 1. __exit__ Signature & Clean Parameters: exc_type, exc_val, and exc_tb as None.
 2. Suppressing Exceptions via return True: Preventing exceptions from bubbling out.
 3. Selective Exception Propagation: Returning False/None to allow specific errors to escape.
 4. Exception Transformation in __exit__: Raising high-level errors to wrap inner block failures.
 5. Generator Context Managers with @contextmanager: Handling errors around the yield statement.
 6. contextlib.suppress Idiom: Standard library one-liner for ignoring expected benign errors.
 7. ExitStack Error Callbacks: Registering compensation callbacks executed only on failure.
 8. Nested Context Manager Unwinding: Trace the order of __exit__ execution during an exception.
 9. Async Context Managers: __aexit__ exception interception with asyncio.run().
10. Advanced Project: Transactional Saga Session Orchestrator with automated compensation and audit ledger.
"""

import asyncio
import contextlib
import types
from typing import Any, Generator


# ==============================================================================
# Question 1: __exit__ Parameters on Clean Execution
# ==============================================================================
class ExecutionAuditor:
    """Audits whether __exit__ received clean or error arguments."""

    def __init__(self) -> None:
        self.recorded_type: type[BaseException] | None = None
        self.recorded_val: BaseException | None = None
        self.recorded_tb: types.TracebackType | None = None

    def __enter__(self) -> "ExecutionAuditor":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> bool:
        self.recorded_type = exc_type
        self.recorded_val = exc_val
        self.recorded_tb = exc_tb
        return False


def exercise_q1_clean_exit_parameters() -> None:
    """
    Verify that when no exception is raised inside the with block,
    all three __exit__ parameters are precisely None.
    """
    print("=== Q1: __exit__ Parameters on Clean Execution ===")

    auditor = ExecutionAuditor()
    with auditor:
        x = 10 + 20
        assert x == 30

    assert auditor.recorded_type is None
    assert auditor.recorded_val is None
    assert auditor.recorded_tb is None

    print("  Clean execution verified: exc_type=None, exc_val=None, exc_tb=None.")


# ==============================================================================
# Question 2: Suppressing Exceptions via return True
# ==============================================================================
class SuppressAllErrors:
    """Context manager that unconditionally suppresses any exception in the with block."""

    def __init__(self) -> None:
        self.suppressed_count = 0

    def __enter__(self) -> "SuppressAllErrors":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> bool:
        if exc_type is not None:
            self.suppressed_count += 1
            # Returning True suppresses the exception from propagating!
            return True
        return False


def exercise_q2_suppress_via_return_true() -> None:
    """
    Demonstrate that returning True from __exit__ prevents exceptions from escaping.
    """
    print("\n=== Q2: Suppressing Exceptions via return True ===")

    suppressor = SuppressAllErrors()
    with suppressor:
        raise ZeroDivisionError("10 / 0 error inside block")

    assert suppressor.suppressed_count == 1

    with suppressor:
        raise KeyError("missing_key")

    assert suppressor.suppressed_count == 2
    print(f"  Successfully suppressed {suppressor.suppressed_count} exceptions without crashing caller.")


# ==============================================================================
# Question 3: Selective Exception Propagation
# ==============================================================================
class SelectiveSuppressor:
    """Suppresses only specified exception classes; allows others to bubble up."""

    def __init__(self, allowed_errors: tuple[type[BaseException], ...]) -> None:
        self.allowed_errors = allowed_errors
        self.intercepted_error: BaseException | None = None

    def __enter__(self) -> "SelectiveSuppressor":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> bool:
        if exc_type is not None and issubclass(exc_type, self.allowed_errors):
            self.intercepted_error = exc_val
            return True  # Suppress
        return False  # Propagate


def exercise_q3_selective_propagation() -> None:
    """
    Demonstrate selectively suppressing ValueError while propagating TypeError.
    """
    print("\n=== Q3: Selective Exception Propagation ===")

    # Case A: Suppressed ValueError
    with SelectiveSuppressor((ValueError,)):
        raise ValueError("Invalid number format")
    print("  ValueError suppressed cleanly.")

    # Case B: Propagated TypeError
    caught_type_error = False
    try:
        with SelectiveSuppressor((ValueError,)):
            raise TypeError("Mismatched type pairing")
    except TypeError:
        caught_type_error = True

    assert caught_type_error is True
    print("  TypeError correctly propagated past selective context manager.")


# ==============================================================================
# Question 4: Exception Transformation in __exit__
# ==============================================================================
class ServiceGatewayContext:
    """
    Intercepts low-level socket/OS exceptions and raises a high-level ServiceGatewayError.
    """

    def __enter__(self) -> "ServiceGatewayContext":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> bool:
        if exc_type is not None and issubclass(exc_type, (ConnectionError, TimeoutError)):
            # Raise a new exception from __exit__ to transform it
            raise RuntimeError(f"Service gateway failed due to transport error: {exc_val}") from exc_val
        return False


def exercise_q4_exception_transformation() -> None:
    """
    Demonstrate transforming low-level errors into high-level errors inside __exit__.
    """
    print("\n=== Q4: Exception Transformation in __exit__ ===")

    caught_transformed = None
    try:
        with ServiceGatewayContext():
            raise ConnectionError("Host unreachable: 10.0.0.1")
    except RuntimeError as err:
        caught_transformed = err

    assert caught_transformed is not None
    assert "Service gateway failed" in str(caught_transformed)
    assert isinstance(caught_transformed.__cause__, ConnectionError)

    print(f"  Transformed exception: {caught_transformed}")
    print(f"  Original cause:        {caught_transformed.__cause__}")


# ==============================================================================
# Question 5: @contextlib.contextmanager Generator Error Trapping
# ==============================================================================
@contextlib.contextmanager
def safe_database_transaction(tx_name: str) -> Generator[list[str], None, None]:
    """
    Generator-based context manager that catches exceptions around yield,
    rolls back changes, and re-raises.
    """
    log: list[str] = [f"BEGIN_{tx_name}"]
    try:
        yield log
        log.append(f"COMMIT_{tx_name}")
    except Exception as exc:
        log.append(f"ROLLBACK_{tx_name}_{type(exc).__name__}")
        raise


def exercise_q5_generator_context_manager() -> None:
    """
    Test @contextlib.contextmanager error interception and rollback logging.
    """
    print("\n=== Q5: @contextlib.contextmanager Generator Error Trapping ===")

    # Scenario A: Clean commit
    log_a: list[str] = []
    with safe_database_transaction("TX_1") as tx_log:
        log_a = tx_log
        tx_log.append("INSERT_USER")

    assert log_a == ["BEGIN_TX_1", "INSERT_USER", "COMMIT_TX_1"]

    # Scenario B: Failed rollback
    log_b: list[str] = []
    caught = False
    try:
        with safe_database_transaction("TX_2") as tx_log:
            log_b = tx_log
            tx_log.append("INSERT_ORDER")
            raise ValueError("Duplicate order key")
    except ValueError:
        caught = True

    assert caught is True
    assert log_b == ["BEGIN_TX_2", "INSERT_ORDER", "ROLLBACK_TX_2_ValueError"]

    print(f"  Committed log:  {log_a}")
    print(f"  Rollback log:   {log_b}")


# ==============================================================================
# Question 6: contextlib.suppress Idiom
# ==============================================================================
def exercise_q6_contextlib_suppress() -> None:
    """
    Demonstrate contextlib.suppress(*exceptions) to cleanly bypass expected
    non-critical errors without boilerplate try/except/pass blocks.
    """
    print("\n=== Q6: contextlib.suppress Idiom ===")

    lookup_table = {"id": 101, "name": "Alice"}

    # Safely remove optional key without KeyError
    with contextlib.suppress(KeyError):
        del lookup_table["non_existent_key"]

    # Safely convert without crashing on ValueError
    num = 0
    with contextlib.suppress(ValueError):
        num = int("not_a_number")

    assert num == 0
    assert lookup_table["id"] == 101
    print("  contextlib.suppress safely ignored KeyError and ValueError cleanly.")


# ==============================================================================
# Question 7: ExitStack Error Callbacks
# ==============================================================================
def exercise_q7_exit_stack_error_callbacks() -> None:
    """
    Demonstrate using contextlib.ExitStack with callback() and pop_all()
    to register undo actions that execute ONLY if an exception occurs.
    """
    print("\n=== Q7: ExitStack Error Callbacks ===")

    audit_trail: list[str] = []

    def perform_staged_action(should_fail: bool) -> bool:
        with contextlib.ExitStack() as stack:
            # Register compensatory undo action
            stack.callback(lambda: audit_trail.append("COMPENSATION_TRIGGERED"))

            audit_trail.append("STEP_1_APPLIED")
            if should_fail:
                raise RuntimeError("Step 2 crashed")

            audit_trail.append("STEP_2_APPLIED")
            # If we reach here cleanly, pop_all transfers callbacks out so compensation is cancelled!
            stack.pop_all()
            return True
        return False

    # Clean run
    audit_trail.clear()
    ok = perform_staged_action(should_fail=False)
    assert ok is True
    assert audit_trail == ["STEP_1_APPLIED", "STEP_2_APPLIED"]

    # Failing run
    audit_trail.clear()
    caught = False
    try:
        perform_staged_action(should_fail=True)
    except RuntimeError:
        caught = True

    assert caught is True
    assert audit_trail == ["STEP_1_APPLIED", "COMPENSATION_TRIGGERED"]

    print("  ExitStack clean run trail:   ['STEP_1_APPLIED', 'STEP_2_APPLIED']")
    print("  ExitStack failure run trail: ['STEP_1_APPLIED', 'COMPENSATION_TRIGGERED']")


# ==============================================================================
# Question 8: Nested Context Manager Unwinding Order
# ==============================================================================
class UnwindTracker:
    def __init__(self, name: str, suppress: bool = False) -> None:
        self.name = name
        self.suppress = suppress

    def __enter__(self) -> "UnwindTracker":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        unwind_log.append(f"EXIT_{self.name}")
        return self.suppress


unwind_log: list[str] = []


def exercise_q8_nested_unwinding_order() -> None:
    """
    Demonstrate that when multiple context managers are nested (or bound in a single
    compound with statement), their __exit__ methods execute in REVERSE order (LIFO).
    """
    print("\n=== Q8: Nested Context Manager Unwinding Order ===")

    unwind_log.clear()

    # Outer is A, Inner is B
    with UnwindTracker("A", suppress=True):
        with UnwindTracker("B", suppress=False):
            unwind_log.append("BODY")
            raise ValueError("Crash inside inner body")

    # Order must be: BODY -> EXIT_B (inner first) -> EXIT_A (outer second, which suppresses)
    assert unwind_log == ["BODY", "EXIT_B", "EXIT_A"]

    print(f"  Unwinding execution order verified (LIFO): {unwind_log}")


# ==============================================================================
# Question 9: Asynchronous Context Manager Exception Handling
# ==============================================================================
class AsyncExceptionInterceptor:
    """Async context manager that intercepts and audits exceptions in async blocks."""

    def __init__(self) -> None:
        self.captured_error: str | None = None

    async def __aenter__(self) -> "AsyncExceptionInterceptor":
        await asyncio.sleep(0.005)
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        await asyncio.sleep(0.005)
        if exc_type is not None:
            self.captured_error = f"{exc_type.__name__}: {exc_val}"
            return True  # Suppress async error
        return False


async def _async_runner() -> AsyncExceptionInterceptor:
    interceptor = AsyncExceptionInterceptor()
    async with interceptor:
        await asyncio.sleep(0.005)
        raise ConnectionResetError("Async peer closed socket")
    return interceptor


def exercise_q9_async_exception_interception() -> None:
    """
    Run async context manager within asyncio.run() and verify exception suppression.
    """
    print("\n=== Q9: Asynchronous Context Manager Exception Handling ===")

    res = asyncio.run(_async_runner())
    assert res.captured_error is not None
    assert "ConnectionResetError: Async peer closed socket" in res.captured_error

    print(f"  Async __aexit__ cleanly intercepted error: {res.captured_error}")


# ==============================================================================
# Question 10: Advanced Project - Transactional Saga Orchestrator
# ==============================================================================
class SagaStep:
    def __init__(self, name: str, action: Any, compensation: Any) -> None:
        self.name = name
        self.action = action
        self.compensation = compensation


class SagaOrchestrator:
    """
    Enterprise Distributed Saga Context Manager.
    Executes multiple stateful steps. If any step raises an exception:
    1. Intercepts the exception in __exit__.
    2. Executes compensation actions for completed steps in reverse order.
    3. Records an audit ledger of executed and compensated actions.
    4. Re-raises the original exception with compensation results attached.
    """

    def __init__(self, saga_name: str) -> None:
        self.saga_name = saga_name
        self.completed_steps: list[SagaStep] = []
        self.compensation_log: list[str] = []

    def __enter__(self) -> "SagaOrchestrator":
        return self

    def execute_step(self, step: SagaStep) -> Any:
        result = step.action()
        self.completed_steps.append(step)
        return result

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> bool:
        if exc_type is not None:
            # Compensate in reverse order (LIFO)
            for step in reversed(self.completed_steps):
                try:
                    step.compensation()
                    self.compensation_log.append(f"COMPENSATED_{step.name}")
                except Exception as comp_err:
                    self.compensation_log.append(f"COMPENSATION_FAILED_{step.name}_{comp_err}")

            # Do not suppress: allow original exception to propagate with audit log
            return False
        return True


def exercise_q10_saga_orchestrator() -> None:
    """
    Test SagaOrchestrator rollback on partial execution failure.
    """
    print("\n=== Q10: Transactional Saga Orchestrator ===")

    order_state: list[str] = []

    s1 = SagaStep(
        name="RESERVE_INVENTORY",
        action=lambda: order_state.append("INVENTORY_RESERVED"),
        compensation=lambda: order_state.append("INVENTORY_RELEASED"),
    )
    s2 = SagaStep(
        name="CHARGE_CARD",
        action=lambda: order_state.append("CARD_CHARGED"),
        compensation=lambda: order_state.append("CARD_REFUNDED"),
    )
    s3 = SagaStep(
        name="DISPATCH_NOTIFICATION",
        action=lambda: (_ for _ in ()).throw(RuntimeError("Email gateway down")),  # Crashes!
        compensation=lambda: None,
    )

    caught = False
    orchestrator = SagaOrchestrator("ORDER_CHECKOUT_SAGA")

    try:
        with orchestrator:
            orchestrator.execute_step(s1)
            orchestrator.execute_step(s2)
            orchestrator.execute_step(s3)  # Crashes here!
    except RuntimeError:
        caught = True

    assert caught is True
    # Step 1 and 2 completed, then compensated in reverse (Card refunded, then Inventory released)
    assert order_state == [
        "INVENTORY_RESERVED",
        "CARD_CHARGED",
        "CARD_REFUNDED",
        "INVENTORY_RELEASED",
    ]
    assert orchestrator.compensation_log == [
        "COMPENSATED_CHARGE_CARD",
        "COMPENSATED_RESERVE_INVENTORY",
    ]

    print(f"  Order state history: {order_state}")
    print(f"  Compensations executed: {orchestrator.compensation_log}")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_clean_exit_parameters()
    exercise_q2_suppress_via_return_true()
    exercise_q3_selective_propagation()
    exercise_q4_exception_transformation()
    exercise_q5_generator_context_manager()
    exercise_q6_contextlib_suppress()
    exercise_q7_exit_stack_error_callbacks()
    exercise_q8_nested_unwinding_order()
    exercise_q9_async_exception_interception()
    exercise_q10_saga_orchestrator()

    print("\nAll 10 context manager exception handling questions executed and asserted successfully!")
