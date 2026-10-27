"""
Topic 07 - Exception Handling: Question 7
Problem: Resilient Execution Context Manager (FaultTolerantScope) with Selective Error Suppression.
"""

from typing import Any, Callable, Optional, Tuple, Type


class FaultTolerantScope:
    """Configurable context manager inspecting exceptions in __exit__ for selective suppression."""

    FORBIDDEN_SUPPRESSIONS = (KeyboardInterrupt, SystemExit)

    def __init__(
        self,
        suppress_types: Tuple[Type[BaseException], ...],
        on_suppress_hook: Optional[Callable[[BaseException], None]] = None
    ):
        self.suppress_types = suppress_types
        self.on_suppress_hook = on_suppress_hook
        self.suppressed_exception: Optional[BaseException] = None
        self.was_suppressed: bool = False

    def __enter__(self) -> "FaultTolerantScope":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is None:
            return False

        # Strictly never suppress critical system interruptions
        if issubclass(exc_type, self.FORBIDDEN_SUPPRESSIONS):
            return False

        # Check whether the encountered exception matches configured suppressible types
        if issubclass(exc_type, self.suppress_types):
            self.suppressed_exception = exc_val
            self.was_suppressed = True
            if callable(self.on_suppress_hook):
                self.on_suppress_hook(exc_val)
            # Returning True swallows the exception and continues execution
            return True

        # Returning False propagates unhandled exception up the stack
        return False


# Verification & Execution
suppressed_events = []


def record_event(err: BaseException) -> None:
    suppressed_events.append(f"Handled {type(err).__name__}: {err}")


# Test 1: Suppressing KeyError
with FaultTolerantScope(suppress_types=(KeyError,), on_suppress_hook=record_event) as scope1:
    data = {"a": 1}
    val = data["missing_key"]

print("Continued after Scope 1. Suppressed?", scope1.was_suppressed)
print("Suppressed Events:", suppressed_events)

# Test 2: Unhandled TypeError escapes
try:
    with FaultTolerantScope(suppress_types=(ValueError,)):
        num = int("123")
        res = "abc" + 10  # type: ignore # Raises TypeError
except TypeError as unhandled:
    print("Caught unhandled escaping error:", unhandled)
