"""
Topic 07: Exceptions - Question 06: Exception Chaining

A comprehensive collection of 10 standalone, runnable exercises exploring
Python's PEP 3134 exception chaining mechanisms, explicit chaining (`from cause`),
implicit chaining (`__context__`), suppressing context (`from None`), and root cause analysis.

Questions Covered:
 1. Explicit Chaining with raise ... from: Establishing an explicit __cause__.
 2. Implicit Chaining via __context__: How Python tracks exceptions raised in except blocks.
 3. Suppressing Context with raise ... from None: Hiding low-level implementation details.
 4. __cause__ vs __context__ Mechanics: Intentional chaining vs incidental runtime errors.
 5. Root Cause Extraction: Unwrapping chained exceptions recursively to find the origin.
 6. Exception Translation Pattern: Wrapping infrastructure errors into domain errors.
 7. Traceback Formatting: Inspecting chained tracebacks via traceback.format_exception.
 8. Preventing Exception Cycles: Guarding against recursive __context__ / __cause__ loops.
 9. Multi-Tier Wrap Chain: Tracing 3-tier application exception cascades (Driver -> DAO -> Service).
10. Advanced Project: Automated Incident Triage & Root Cause Diagnostic Engine.
"""

import traceback
from typing import Any


# ==============================================================================
# Question 1: Explicit Chaining with raise ... from
# ==============================================================================
class DatabaseQueryError(Exception):
    pass


def exercise_q1_explicit_chaining() -> None:
    """
    Demonstrate explicit exception chaining using `raise NewException from original_exception`.
    Verifies that `__cause__` is set to the original exception.
    """
    print("=== Q1: Explicit Chaining with raise ... from ===")

    def execute_query(sql: str) -> None:
        try:
            # Low-level system driver error
            raise ConnectionResetError("TCP socket connection reset by peer")
        except ConnectionResetError as net_err:
            # Explicitly chain to high-level domain error
            raise DatabaseQueryError(f"Failed to execute query: {sql}") from net_err

    caught_wrapper = None
    try:
        execute_query("SELECT * FROM users")
    except DatabaseQueryError as err:
        caught_wrapper = err

    assert caught_wrapper is not None
    assert caught_wrapper.__cause__ is not None
    assert isinstance(caught_wrapper.__cause__, ConnectionResetError)
    assert "TCP socket connection reset" in str(caught_wrapper.__cause__)

    print(f"  Wrapper exception: {type(caught_wrapper).__name__} ('{caught_wrapper}')")
    print(f"  Explicit cause:    {type(caught_wrapper.__cause__).__name__} ('{caught_wrapper.__cause__}')")


# ==============================================================================
# Question 2: Implicit Chaining via __context__
# ==============================================================================
def exercise_q2_implicit_chaining() -> None:
    """
    Demonstrate implicit exception chaining: when an exception occurs inside an
    `except` block without `from`, Python automatically attaches the original
    exception as `__context__`.
    """
    print("\n=== Q2: Implicit Chaining via __context__ ===")

    caught_err = None
    try:
        try:
            # Primary error
            raise ValueError("Corrupted user input")
        except ValueError:
            # Bug inside error handler: raises secondary error
            raise KeyError("missing_error_template_key")
    except KeyError as exc:
        caught_err = exc

    assert caught_err is not None
    assert caught_err.__cause__ is None  # No explicit 'from' was used
    assert caught_err.__context__ is not None  # Python implicitly sets __context__
    assert isinstance(caught_err.__context__, ValueError)

    print(f"  Secondary error: {type(caught_err).__name__}")
    print(f"  Implicit context: {type(caught_err.__context__).__name__} ('{caught_err.__context__}')")


# ==============================================================================
# Question 3: Suppressing Context with raise ... from None
# ==============================================================================
class CleanPublicError(Exception):
    pass


def exercise_q3_suppressing_context() -> None:
    """
    Demonstrate `raise ... from None` to intentionally suppress the underlying
    cause and context, preventing internal stack traces from leaking to callers.
    """
    print("\n=== Q3: Suppressing Context with raise ... from None ===")

    def authenticate_user(token: str) -> None:
        try:
            int(token)  # Sensitive internal parsing
        except ValueError:
            # Suppress internal ValueError details!
            raise CleanPublicError("Invalid authentication credentials") from None

    caught = None
    try:
        authenticate_user("secret_token_abc")
    except CleanPublicError as exc:
        caught = exc

    assert caught is not None
    assert caught.__cause__ is None
    # __suppress_context__ flag is set to True by 'from None'
    assert caught.__suppress_context__ is True

    print(f"  Public error: {caught}")
    print(f"  __cause__: {caught.__cause__}, __suppress_context__: {caught.__suppress_context__}")


# ==============================================================================
# Question 4: __cause__ vs __context__ Mechanics
# ==============================================================================
def exercise_q4_cause_vs_context() -> None:
    """
    Contrast `__cause__` (explicit, deliberate causality via 'raise ... from')
    versus `__context__` (implicit, accidental failure during handling).
    """
    print("\n=== Q4: __cause__ vs __context__ Mechanics ===")

    # Scenario A: Explicit
    try:
        try:
            raise OSError("Disk failure")
        except OSError as e:
            raise RuntimeError("App failure") from e
    except RuntimeError as explicit_exc:
        assert explicit_exc.__cause__ is not None
        assert explicit_exc.__suppress_context__ is True  # explicit cause suppresses default context display

    # Scenario B: Implicit
    try:
        try:
            raise OSError("Disk failure")
        except OSError:
            raise RuntimeError("Handler bug")
    except RuntimeError as implicit_exc:
        assert implicit_exc.__cause__ is None
        assert implicit_exc.__context__ is not None
        assert implicit_exc.__suppress_context__ is False

    print("  Explicit: __cause__ is set, __suppress_context__ is True.")
    print("  Implicit: __cause__ is None, __context__ is set, __suppress_context__ is False.")


# ==============================================================================
# Question 5: Root Cause Extraction
# ==============================================================================
def find_root_cause(exc: BaseException) -> BaseException:
    """
    Walks up the exception chain (inspecting __cause__ first, then __context__)
    to locate the original root cause that triggered the cascade.
    """
    current = exc
    visited: set[int] = {id(current)}

    while True:
        # Check explicit cause first, fallback to implicit context if not suppressed
        next_exc = current.__cause__
        if next_exc is None and not current.__suppress_context__:
            next_exc = current.__context__

        if next_exc is None or id(next_exc) in visited:
            break

        visited.add(id(next_exc))
        current = next_exc

    return current


def exercise_q5_root_cause_extraction() -> None:
    """
    Demonstrate extracting the initial root cause from a multi-link chain.
    """
    print("\n=== Q5: Root Cause Extraction ===")

    e1 = FileNotFoundError("config.yaml not found on disk")
    e2 = RuntimeError("Configuration subsystem failed to load")
    e2.__cause__ = e1
    e3 = DatabaseQueryError("Application initialization aborted")
    e3.__cause__ = e2

    root = find_root_cause(e3)
    assert root is e1
    assert isinstance(root, FileNotFoundError)
    assert "config.yaml not found" in str(root)

    print(f"  Top-level error: {type(e3).__name__}")
    print(f"  Unwrapped root:  {type(root).__name__} ('{root}')")


# ==============================================================================
# Question 6: Exception Translation Pattern
# ==============================================================================
class StorageServiceError(Exception):
    pass


def exercise_q6_exception_translation() -> None:
    """
    Demonstrate the Exception Translation design pattern: translating third-party
    or low-level OS exceptions into a stable, published application abstraction.
    """
    print("\n=== Q6: Exception Translation Pattern ===")

    def read_cached_blob(blob_id: str) -> bytes:
        try:
            # Low-level I/O simulation
            if blob_id == "corrupted":
                raise PermissionError("Access denied by OS filesystem ACL")
            return b"OK"
        except (OSError, PermissionError) as sys_err:
            # Translate to StorageServiceError while retaining sys_err in __cause__
            raise StorageServiceError(f"Storage backend rejected read for blob '{blob_id}'") from sys_err

    caught_translated = None
    try:
        read_cached_blob("corrupted")
    except StorageServiceError as err:
        caught_translated = err

    assert caught_translated is not None
    assert isinstance(caught_translated.__cause__, PermissionError)
    print(f"  Translated exception caught: {caught_translated}")
    print(f"  Preserved underlying driver: {caught_translated.__cause__}")


# ==============================================================================
# Question 7: Traceback Formatting with Chained Exceptions
# ==============================================================================
def exercise_q7_traceback_formatting() -> None:
    """
    Demonstrate rendering full chained exception tracebacks into strings using
    traceback.format_exception().
    """
    print("\n=== Q7: Traceback Formatting with Chained Exceptions ===")

    formatted_traceback = ""
    try:
        try:
            int("invalid")
        except ValueError as original:
            raise RuntimeError("High-level computation aborted") from original
    except RuntimeError as final_exc:
        lines = traceback.format_exception(final_exc)
        formatted_traceback = "".join(lines)

    assert "ValueError: invalid literal for int()" in formatted_traceback
    assert "The above exception was the direct cause of the following exception" in formatted_traceback
    assert "RuntimeError: High-level computation aborted" in formatted_traceback

    print("  Rendered chained traceback contains both original cause and direct cause markers.")


# ==============================================================================
# Question 8: Preventing Exception Cycles
# ==============================================================================
def exercise_q8_preventing_exception_cycles() -> None:
    """
    Demonstrate that circular exception references (A causes B, B causes A)
    can be detected and safely navigated without infinite loops.
    """
    print("\n=== Q8: Preventing Exception Cycles ===")

    err_a = ValueError("Error A")
    err_b = TypeError("Error B")

    # Artificially create cycle: A -> B -> A
    err_a.__cause__ = err_b
    err_b.__cause__ = err_a

    # find_root_cause must terminate safely using cycle detection
    root = find_root_cause(err_a)
    assert root in (err_a, err_b)

    print(f"  Cycle safely broken; terminated without infinite loop on: {type(root).__name__}")


# ==============================================================================
# Question 9: Multi-Tier Wrap Chain (Driver -> DAO -> Service)
# ==============================================================================
class DriverConnectionError(Exception):
    pass


class RepositoryError(Exception):
    pass


class UserServiceError(Exception):
    pass


def exercise_q9_multi_tier_wrap_chain() -> None:
    """
    Trace a real-world 3-tier enterprise exception chain:
    Low-level network driver -> Data access repository -> High-level business service.
    """
    print("\n=== Q9: Multi-Tier Wrap Chain ===")

    def driver_call() -> None:
        raise DriverConnectionError("Socket timeout on replica:5433")

    def repository_call() -> None:
        try:
            driver_call()
        except DriverConnectionError as d_err:
            raise RepositoryError("User repository query failed") from d_err

    def service_call() -> None:
        try:
            repository_call()
        except RepositoryError as r_err:
            raise UserServiceError("User registration failed") from r_err

    top_err = None
    try:
        service_call()
    except UserServiceError as exc:
        top_err = exc

    assert top_err is not None
    assert isinstance(top_err, UserServiceError)
    assert isinstance(top_err.__cause__, RepositoryError)
    assert isinstance(top_err.__cause__.__cause__, DriverConnectionError)

    print(f"  Tier 3 (Service):    {type(top_err).__name__}")
    print(f"  Tier 2 (Repository): {type(top_err.__cause__).__name__}")
    print(f"  Tier 1 (Driver):     {type(top_err.__cause__.__cause__).__name__}")


# ==============================================================================
# Question 10: Advanced Project - Incident Triage & Root Cause Diagnostic Engine
# ==============================================================================
class IncidentDiagnosticEngine:
    """
    Enterprise incident triage analyzer that inspects an exception cascade,
    extracts the linear chain of events, detects root causes, and generates
    a structured diagnostic incident report.
    """

    @classmethod
    def analyze(cls, exc: BaseException) -> dict[str, Any]:
        chain: list[dict[str, Any]] = []
        current: BaseException | None = exc
        visited: set[int] = set()

        while current is not None and id(current) not in visited:
            visited.add(id(current))
            link_info = {
                "type": type(current).__name__,
                "message": str(current),
                "is_explicit_cause": current.__cause__ is not None,
            }
            chain.append(link_info)

            # Next in chain
            if current.__cause__ is not None:
                current = current.__cause__
            elif not current.__suppress_context__:
                current = current.__context__
            else:
                current = None

        root_cause = chain[-1] if chain else None

        return {
            "chain_depth": len(chain),
            "top_level_error": chain[0] if chain else None,
            "root_cause": root_cause,
            "cascade_path": " -> ".join(link["type"] for link in chain),
        }


def exercise_q10_incident_diagnostic_engine() -> None:
    """
    Verify IncidentDiagnosticEngine correctly parses a 3-layer exception cascade.
    """
    print("\n=== Q10: Incident Triage & Root Cause Diagnostic Engine ===")

    try:
        try:
            try:
                raise TimeoutError("TCP connection timed out to shard-03")
            except TimeoutError as t_err:
                raise ConnectionError("Database replica uncontactable") from t_err
        except ConnectionError as conn_err:
            raise RuntimeError("Order checkout failed") from conn_err
    except RuntimeError as top_exc:
        report = IncidentDiagnosticEngine.analyze(top_exc)

    assert report["chain_depth"] == 3
    assert report["top_level_error"]["type"] == "RuntimeError"
    assert report["root_cause"]["type"] == "TimeoutError"
    assert "TCP connection timed out" in report["root_cause"]["message"]
    assert report["cascade_path"] == "RuntimeError -> ConnectionError -> TimeoutError"

    print(f"  Incident Analysis:")
    print(f"    Depth:        {report['chain_depth']}")
    print(f"    Cascade Path: {report['cascade_path']}")
    print(f"    Root Cause:   {report['root_cause']['type']}: '{report['root_cause']['message']}'")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_explicit_chaining()
    exercise_q2_implicit_chaining()
    exercise_q3_suppressing_context()
    exercise_q4_cause_vs_context()
    exercise_q5_root_cause_extraction()
    exercise_q6_exception_translation()
    exercise_q7_traceback_formatting()
    exercise_q8_preventing_exception_cycles()
    exercise_q9_multi_tier_wrap_chain()
    exercise_q10_incident_diagnostic_engine()

    print("\nAll 10 exception chaining questions executed and asserted successfully!")
