"""
Question 3: Endpoint Security & Observability Decorator Suite
Topic: Advanced Python

Key Concepts Tested:
- Function decorators and closures
- Decorator metadata preservation via @functools.wraps
- Parameterized decorators with 3-tier function closures
- Decorator chaining semantics: bottom-up application vs top-down execution
- RBAC security gating and latency telemetry collection
"""

import time
import functools
from typing import Callable, Set, Any, Dict


def track_latency(func: Callable) -> Callable:
    """
    Observability decorator tracking call count and cumulative execution latency.
    Exposes metrics on wrapper.metrics.
    """
    metrics: Dict[str, Any] = {"call_count": 0, "total_time": 0.0}

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start_time
            metrics["call_count"] += 1
            metrics["total_time"] += elapsed

    wrapper.metrics = metrics  # type: ignore[attr-defined]
    return wrapper


def require_role(allowed_roles: Set[str]) -> Callable:
    """
    Parameterized RBAC security decorator (3-tier closure).
    Validates caller_role keyword argument against allowed_roles.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            caller_role = kwargs.get("caller_role")
            if caller_role not in allowed_roles:
                raise PermissionError(
                    f"Access forbidden: Role '{caller_role}' is not in {allowed_roles}"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Chained decorator demonstration
@track_latency
@require_role({"ADMIN", "SUPERUSER"})
def purge_expired_sessions(caller_role: str, max_age_days: int) -> int:
    """Purges expired user sessions from system storage."""
    # Simulated database purge operation
    time.sleep(0.005)
    return 42


if __name__ == "__main__":
    print("=== Decorator Chaining Semantics ===")
    print("Decoration Order: Bottom-up (@require_role wraps function, then @track_latency wraps that).")
    print("Execution Order:  Top-down (@track_latency timer starts, then @require_role checks authorization).\n")

    print("=== Test 1: Authorized Invocation ===")
    purged = purge_expired_sessions(caller_role="ADMIN", max_age_days=30)
    print(f"Purged Sessions Count: {purged}")
    print(f"Latency Metrics: {purge_expired_sessions.metrics}")

    print("\n=== Metadata Preservation Checks ===")
    print(f"Function Name Verified: '{purge_expired_sessions.__name__}'")
    print(f"Function Docstring Verified: '{purge_expired_sessions.__doc__}'")

    print("\n=== Test 2: Unauthorized Invocation ===")
    try:
        purge_expired_sessions(caller_role="GUEST", max_age_days=30)
    except PermissionError as err:
        print(f"Caught Security Violation: {err}")

    print(f"\nLatency Metrics After Failed Call: {purge_expired_sessions.metrics}")
