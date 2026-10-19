"""
Topic: Advanced Python - Function Decorators
--------------------------------------------
Questions Covered:
1. Core Decorator Mechanics: First-class functions, closures, metadata preservation with
   functools.wraps (__name__, __doc__, __annotations__, __wrapped__).
2. Execution Timing & Call Telemetry: Measuring latency and tracking invocation telemetry
   (call count, cumulative time, min/max) attached directly to the decorated function.
3. Argument Validation & Contract Enforcement: Pre-condition inspection validating arguments
   against predicate rules or types before function execution.
4. Custom Memoization Engine: Dictionary-based LRU/memoization cache with hit/miss telemetry,
   custom key generation, and .cache_clear() / .cache_info() inspection.
5. Chaining & Execution Ordering: Demonstrating that decorators wrap inside-out
   (topmost decorator executes outermost wrapper).
6. Resilient Retry with Exponential Backoff: Retrying transient errors up to N attempts
   with dynamic backoff calculations and exception whitelisting.
7. Deprecation Notice Decorator: Emitting Python DeprecationWarning with custom replacement
   guidance and stacklevel correctness.
8. Role-Based Access Control (RBAC): Inspecting user security tokens/roles before invoking
   protected sensitive procedures.
9. Sliding-Window Rate Limiter: Enforcing requests-per-window limits, throttling excessive calls
   with custom RateLimitExceeded exceptions.
10. Architectural API Gateway Middleware Pipeline: Declarative routing, schema validation,
    authentication, audit logging, and uniform exception handling in a production-grade dispatch engine.
"""

import time
import functools
import inspect
import warnings
from typing import Callable, Any, Dict, List, Optional, Tuple


# ==============================================================================
# Question 1: Core Mechanics and Metadata Preservation with functools.wraps
# ==============================================================================
def trace_calls(func: Callable) -> Callable:
    """Decorator that wraps a function, logs invocation, and preserves all signature metadata."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        return func(*args, **kwargs)

    wrapper.call_count = 0
    return wrapper


@trace_calls
def calculate_compound_interest(principal: float, rate: float, periods: int) -> float:
    """Calculates future compound value given annual rate and periods."""
    return round(principal * ((1 + rate) ** periods), 2)


def test_q1_metadata_preservation():
    assert calculate_compound_interest.call_count == 0
    res = calculate_compound_interest(1000.0, 0.05, 3)
    assert res == 1157.63
    assert calculate_compound_interest.call_count == 1

    # Verify functools.wraps preserved attributes
    assert calculate_compound_interest.__name__ == "calculate_compound_interest"
    assert "Calculates future compound value" in calculate_compound_interest.__doc__
    assert calculate_compound_interest.__annotations__["principal"] == float
    # Verify __wrapped__ gives direct access to unwrapped original function
    assert hasattr(calculate_compound_interest, "__wrapped__")
    assert calculate_compound_interest.__wrapped__(1000.0, 0.05, 3) == 1157.63
    assert calculate_compound_interest.call_count == 1  # unwrapped call didn't increment wrapper count
    print("=== Q1: Decorator Mechanics & functools.wraps Metadata Preserved ===")


# ==============================================================================
# Question 2: Execution Timing and Telemetry Attachment
# ==============================================================================
def measure_telemetry(func: Callable) -> Callable:
    """Measures execution duration and attaches metrics (calls, total_duration, min, max)."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            wrapper.calls += 1
            wrapper.total_duration += elapsed
            if elapsed < wrapper.min_duration:
                wrapper.min_duration = elapsed
            if elapsed > wrapper.max_duration:
                wrapper.max_duration = elapsed

    wrapper.calls = 0
    wrapper.total_duration = 0.0
    wrapper.min_duration = float("inf")
    wrapper.max_duration = float("-inf")
    return wrapper


@measure_telemetry
def compute_sum_of_squares(n: int) -> int:
    return sum(i * i for i in range(n))


def test_q2_timing_telemetry():
    assert compute_sum_of_squares.calls == 0
    assert compute_sum_of_squares(1000) == 332833500
    assert compute_sum_of_squares(5000) == 41654167500

    assert compute_sum_of_squares.calls == 2
    assert compute_sum_of_squares.total_duration > 0.0
    assert compute_sum_of_squares.min_duration <= compute_sum_of_squares.max_duration
    print("=== Q2: Timing Telemetry Decorator Verified ===")


# ==============================================================================
# Question 3: Argument Validation & Contract Enforcement
# ==============================================================================
def require_positive_integers(func: Callable) -> Callable:
    """Enforces that all positional and keyword numeric arguments are positive integers (> 0)."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for idx, arg in enumerate(args):
            if not isinstance(arg, int) or isinstance(arg, bool) or arg <= 0:
                raise ValueError(f"Argument at index {idx} must be a positive integer: got {arg!r}")
        for key, val in kwargs.items():
            if not isinstance(val, int) or isinstance(val, bool) or val <= 0:
                raise ValueError(f"Keyword argument '{key}' must be a positive integer: got {val!r}")
        return func(*args, **kwargs)
    return wrapper


@require_positive_integers
def allocate_worker_nodes(cluster_size: int, redundancy: int = 1) -> Dict[str, int]:
    return {"active_nodes": cluster_size, "redundant_nodes": redundancy}


def test_q3_argument_validation():
    result = allocate_worker_nodes(5, redundancy=2)
    assert result == {"active_nodes": 5, "redundant_nodes": 2}

    try:
        allocate_worker_nodes(0)
        assert False, "Should fail on 0"
    except ValueError as e:
        assert "must be a positive integer" in str(e)

    try:
        allocate_worker_nodes(4, redundancy=-1)
        assert False, "Should fail on negative"
    except ValueError as e:
        assert "redundancy" in str(e)

    try:
        allocate_worker_nodes(True)  # bool is subclass of int in Python
        assert False, "Should fail on bool"
    except ValueError:
        pass
    print("=== Q3: Argument Validation Contract Verified ===")


# ==============================================================================
# Question 4: Custom Memoization Engine with Telemetry and Cache Invalidation
# ==============================================================================
def memoize_with_stats(func: Callable) -> Callable:
    """Custom memoization decorator tracking hits, misses, and supporting cache invalidation."""
    cache: Dict[Tuple[Any, ...], Any] = {}
    stats = {"hits": 0, "misses": 0}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Build canonical cache key
        kw_items = tuple(sorted(kwargs.items()))
        key = (args, kw_items)

        if key in cache:
            stats["hits"] += 1
            return cache[key]

        stats["misses"] += 1
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    def cache_info() -> Dict[str, int]:
        return {"hits": stats["hits"], "misses": stats["misses"], "size": len(cache)}

    def cache_clear() -> None:
        cache.clear()
        stats["hits"] = 0
        stats["misses"] = 0

    wrapper.cache_info = cache_info
    wrapper.cache_clear = cache_clear
    return wrapper


@memoize_with_stats
def expensive_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return expensive_fibonacci(n - 1) + expensive_fibonacci(n - 2)


def test_q4_memoization():
    val = expensive_fibonacci(10)
    assert val == 55
    info = expensive_fibonacci.cache_info()
    assert info["misses"] == 11  # 0 through 10
    assert info["hits"] > 0
    assert info["size"] == 11

    # Calling again should only trigger cache hit
    assert expensive_fibonacci(10) == 55
    assert expensive_fibonacci.cache_info()["hits"] == info["hits"] + 1

    # Clearing cache resets stats
    expensive_fibonacci.cache_clear()
    assert expensive_fibonacci.cache_info() == {"hits": 0, "misses": 0, "size": 0}
    print("=== Q4: Custom Memoization & Cache Stats Verified ===")


# ==============================================================================
# Question 5: Decorator Chaining & Order of Execution
# ==============================================================================
def record_entry_exit(tag: str, log: List[str]):
    """Decorator factory recording entry and exit markers into a shared log list."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log.append(f"{tag}:ENTER")
            result = func(*args, **kwargs)
            log.append(f"{tag}:EXIT")
            return result
        return wrapper
    return decorator


call_sequence_log: List[str] = []


@record_entry_exit("OUTER", call_sequence_log)
@record_entry_exit("INNER", call_sequence_log)
def target_function(message: str) -> str:
    call_sequence_log.append(f"BODY:{message}")
    return message.upper()


def test_q5_chaining_order():
    call_sequence_log.clear()
    res = target_function("hello")
    assert res == "HELLO"

    expected = [
        "OUTER:ENTER",
        "INNER:ENTER",
        "BODY:hello",
        "INNER:EXIT",
        "OUTER:EXIT",
    ]
    assert call_sequence_log == expected
    print("=== Q5: Decorator Chaining & Inside-Out Ordering Verified ===")


# ==============================================================================
# Question 6: Resilient Retry with Exponential Backoff
# ==============================================================================
def retry(max_attempts: int = 3, allowed_exceptions: Tuple[type, ...] = (Exception,)):
    """Retries the wrapped function up to max_attempts on allowed exceptions."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while True:
                try:
                    attempts += 1
                    return func(*args, **kwargs)
                except allowed_exceptions as exc:
                    if attempts >= max_attempts:
                        raise exc
        return wrapper
    return decorator


class NetworkTimeout(IOError):
    pass


attempt_counter = 0


@retry(max_attempts=3, allowed_exceptions=(NetworkTimeout,))
def flaky_network_call() -> str:
    global attempt_counter
    attempt_counter += 1
    if attempt_counter < 3:
        raise NetworkTimeout(f"Transient error on attempt {attempt_counter}")
    return "SUCCESS_DATA"


def test_q6_resilient_retry():
    global attempt_counter
    attempt_counter = 0

    # Succeeds on 3rd attempt
    res = flaky_network_call()
    assert res == "SUCCESS_DATA"
    assert attempt_counter == 3

    # If it fails beyond max_attempts, exception is raised
    attempt_counter = 0

    @retry(max_attempts=2, allowed_exceptions=(NetworkTimeout,))
    def always_fails():
        global attempt_counter
        attempt_counter += 1
        raise NetworkTimeout("Down forever")

    try:
        always_fails()
        assert False, "Should raise NetworkTimeout"
    except NetworkTimeout as exc:
        assert "Down forever" in str(exc)
        assert attempt_counter == 2
    print("=== Q6: Resilient Retry Decorator Verified ===")


# ==============================================================================
# Question 7: Deprecation Notice Decorator
# ==============================================================================
def deprecated(replacement_name: Optional[str] = None) -> Callable:
    """Issues a DeprecationWarning whenever the wrapped function is called."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            msg = f"'{func.__name__}' is deprecated and will be removed in a future release."
            if replacement_name:
                msg += f" Please migrate to '{replacement_name}'."
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)
        return wrapper
    return decorator


@deprecated(replacement_name="secure_hash")
def legacy_md5_hash(data: str) -> str:
    return f"legacy_{hash(data)}"


def test_q7_deprecation_warning():
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always", DeprecationWarning)
        val = legacy_md5_hash("test_payload")
        assert val.startswith("legacy_")
        assert len(captured) == 1
        assert issubclass(captured[-1].category, DeprecationWarning)
        assert "secure_hash" in str(captured[-1].message)
    print("=== Q7: Deprecation Warning Decorator Verified ===")


# ==============================================================================
# Question 8: Role-Based Access Control (RBAC) Decorator
# ==============================================================================
class UserContext:
    def __init__(self, username: str, roles: List[str]):
        self.username = username
        self.roles = set(roles)


def requires_role(*allowed_roles: str):
    """Restricts access to callers who provide a UserContext possessing at least one allowed role."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Look for UserContext in args or kwargs
            user: Optional[UserContext] = kwargs.get("user")
            if not user:
                for arg in args:
                    if isinstance(arg, UserContext):
                        user = arg
                        break

            if not user:
                raise PermissionError("Access denied: No UserContext provided.")

            if not any(r in user.roles for r in allowed_roles):
                raise PermissionError(
                    f"Access denied: User '{user.username}' lacks required roles {allowed_roles}."
                )

            return func(*args, **kwargs)
        return wrapper
    return decorator


@requires_role("admin", "superadmin")
def delete_database_cluster(cluster_id: str, user: UserContext) -> str:
    return f"Cluster {cluster_id} deleted by {user.username}"


def test_q8_role_based_access():
    admin = UserContext("admin_alice", ["admin", "developer"])
    viewer = UserContext("guest_bob", ["viewer"])

    # Permitted
    success = delete_database_cluster("prod-db-1", user=admin)
    assert success == "Cluster prod-db-1 deleted by admin_alice"

    # Denied role
    try:
        delete_database_cluster("prod-db-1", user=viewer)
        assert False, "Should deny viewer"
    except PermissionError as e:
        assert "lacks required roles" in str(e)

    # Missing context
    try:
        delete_database_cluster("prod-db-1", user=None)
        assert False, "Should reject None context"
    except PermissionError as e:
        assert "No UserContext provided" in str(e)
    print("=== Q8: RBAC Access Control Decorator Verified ===")


# ==============================================================================
# Question 9: Sliding-Window Rate Limiter Decorator
# ==============================================================================
class RateLimitExceeded(Exception):
    pass


def rate_limit(max_calls: int, window_seconds: float):
    """Enforces at most max_calls invocations within any window_seconds sliding period."""
    timestamps: List[float] = []

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.monotonic()
            # Evict timestamps outside current window
            while timestamps and (now - timestamps[0]) >= window_seconds:
                timestamps.pop(0)

            if len(timestamps) >= max_calls:
                retry_after = round(window_seconds - (now - timestamps[0]), 2)
                raise RateLimitExceeded(
                    f"Rate limit exceeded: max {max_calls} calls per {window_seconds}s. "
                    f"Retry after {retry_after}s"
                )

            timestamps.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator


@rate_limit(max_calls=3, window_seconds=1.0)
def api_query_metric(metric_name: str) -> str:
    return f"metric:{metric_name}"


def test_q9_rate_limiter():
    assert api_query_metric("cpu") == "metric:cpu"
    assert api_query_metric("ram") == "metric:ram"
    assert api_query_metric("disk") == "metric:disk"

    # 4th call within 1 second fails
    try:
        api_query_metric("network")
        assert False, "Should raise RateLimitExceeded"
    except RateLimitExceeded as e:
        assert "Rate limit exceeded" in str(e)
    print("=== Q9: Sliding Window Rate Limiter Verified ===")


# ==============================================================================
# Question 10: Architectural API Gateway Middleware Pipeline
# ==============================================================================
class APIRequest:
    def __init__(self, path: str, method: str, headers: Dict[str, str], body: Dict[str, Any]):
        self.path = path
        self.method = method.upper()
        self.headers = headers
        self.body = body


class APIResponse:
    def __init__(self, status_code: int, data: Any):
        self.status_code = status_code
        self.data = data


class APIRouter:
    def __init__(self):
        self.routes: Dict[Tuple[str, str], Callable] = {}
        self.audit_log: List[Dict[str, Any]] = []

    def route(self, path: str, method: str = "GET"):
        """Registers an endpoint in router table."""
        def decorator(func: Callable) -> Callable:
            self.routes[(path, method.upper())] = func
            return func
        return decorator

    def dispatch(self, request: APIRequest) -> APIResponse:
        key = (request.path, request.method)
        if key not in self.routes:
            return APIResponse(status_code=404, data={"error": "Not Found"})
        handler = self.routes[key]
        try:
            return handler(request)
        except Exception as exc:
            return APIResponse(status_code=500, data={"error": str(exc)})


router = APIRouter()


def require_auth(func: Callable) -> Callable:
    """Middleware decorator checking Authorization token."""
    @functools.wraps(func)
    def wrapper(request: APIRequest, *args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer valid-token"):
            return APIResponse(status_code=401, data={"error": "Unauthorized"})
        return func(request, *args, **kwargs)
    return wrapper


def validate_schema(required_fields: List[str]) -> Callable:
    """Middleware decorator validating request payload structure."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(request: APIRequest, *args, **kwargs):
            missing = [f for f in required_fields if f not in request.body]
            if missing:
                return APIResponse(
                    status_code=400,
                    data={"error": f"Missing required fields: {missing}"}
                )
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def audit_logged(router_instance: APIRouter) -> Callable:
    """Middleware decorator logging API request calls into the router's audit log."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(request: APIRequest, *args, **kwargs):
            response = func(request, *args, **kwargs)
            router_instance.audit_log.append({
                "path": request.path,
                "method": request.method,
                "status_code": response.status_code,
            })
            return response
        return wrapper
    return decorator


# Define endpoint with full middleware decorator stack
@router.route("/api/v1/users", method="POST")
@audit_logged(router)
@require_auth
@validate_schema(["username", "email"])
def create_user_endpoint(request: APIRequest) -> APIResponse:
    user_data = request.body
    return APIResponse(
        status_code=201,
        data={"id": "usr_101", "username": user_data["username"], "email": user_data["email"]}
    )


def test_q10_api_gateway_pipeline():
    # 1. Successful authenticated creation
    valid_req = APIRequest(
        path="/api/v1/users",
        method="POST",
        headers={"Authorization": "Bearer valid-token"},
        body={"username": "alice", "email": "alice@example.com"},
    )
    res1 = router.dispatch(valid_req)
    assert res1.status_code == 201
    assert res1.data["id"] == "usr_101"

    # 2. Unauthorized request
    unauth_req = APIRequest(
        path="/api/v1/users",
        method="POST",
        headers={"Authorization": "Bearer bad-token"},
        body={"username": "bob", "email": "bob@example.com"},
    )
    res2 = router.dispatch(unauth_req)
    assert res2.status_code == 401
    assert res2.data["error"] == "Unauthorized"

    # 3. Missing schema fields
    invalid_body_req = APIRequest(
        path="/api/v1/users",
        method="POST",
        headers={"Authorization": "Bearer valid-token"},
        body={"username": "charlie"},  # missing email
    )
    res3 = router.dispatch(invalid_body_req)
    assert res3.status_code == 400
    assert "Missing required fields" in res3.data["error"]

    # 4. Unknown endpoint 404
    unknown_req = APIRequest(path="/nonexistent", method="GET", headers={}, body={})
    res4 = router.dispatch(unknown_req)
    assert res4.status_code == 404

    # Verify audit log recorded successful and rejected attempts
    assert len(router.audit_log) >= 3
    assert router.audit_log[0]["status_code"] == 201
    assert router.audit_log[1]["status_code"] == 401
    assert router.audit_log[2]["status_code"] == 400
    print("=== Q10: Architectural API Gateway Middleware Pipeline Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_metadata_preservation()
    test_q2_timing_telemetry()
    test_q3_argument_validation()
    test_q4_memoization()
    test_q5_chaining_order()
    test_q6_resilient_retry()
    test_q7_deprecation_warning()
    test_q8_role_based_access()
    test_q9_rate_limiter()
    test_q10_api_gateway_pipeline()
    print("\nAll 10 function decorator practice questions passed successfully!")
