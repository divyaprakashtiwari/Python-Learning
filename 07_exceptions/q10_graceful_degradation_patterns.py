"""
Topic 07: Exceptions - Question 10: Graceful Degradation Patterns

A comprehensive collection of 10 standalone, runnable exercises exploring
enterprise fault tolerance, circuit breakers, exponential backoff with jitter,
bulkheads, stale-while-revalidate caches, and high-availability service orchestrators.

Questions Covered:
 1. Fallback & Default Value Pattern: Serving safe defaults when remote calls fail.
 2. Exponential Backoff Retry: Retrying transient errors with geometric delays.
 3. Jittered Backoff: Mitigating thundering herds with randomized delay variation.
 4. The Circuit Breaker Pattern: CLOSED -> OPEN -> HALF-OPEN state transitions.
 5. The Bulkhead Pattern: Resource pool isolation preventing cascading exhaustion.
 6. Deadline & Timeout Guards: Falling back when execution duration exceeds threshold.
 7. Stale-While-Revalidate Cache: Returning expired cache entries on origin outage.
 8. Partial UI/Service Degradation: Non-blocking fallbacks for non-essential features.
 9. Hedged Redundant Execution: Primary/Secondary dual-call resilience fallback.
10. Advanced Project: Fault-Tolerant Service Mesh Orchestrator with telemetry & auto-healing.
"""

import collections
import random
import time
from typing import Any, Callable


# ==============================================================================
# Question 1: Fallback & Default Value Pattern
# ==============================================================================
def get_user_preferred_theme(user_id: str, fetch_remote_pref: Callable[[str], str]) -> str:
    """
    Attempts to fetch user preferences from remote profile service; falls back
    to 'dark_mode' default if service raises any network or lookup error.
    """
    try:
        return fetch_remote_pref(user_id)
    except (ConnectionError, TimeoutError, KeyError):
        return "dark_mode"  # Safe default


def exercise_q1_fallback_default_value() -> None:
    """
    Demonstrate safe fallback to default values on exception.
    """
    print("=== Q1: Fallback & Default Value Pattern ===")

    # Case A: Remote service works
    theme_ok = get_user_preferred_theme("u101", lambda uid: "light_mode")
    assert theme_ok == "light_mode"

    # Case B: Remote service crashes
    def failing_remote(uid: str) -> str:
        raise ConnectionError("Remote profile service unreachable")

    theme_fallback = get_user_preferred_theme("u102", failing_remote)
    assert theme_fallback == "dark_mode"

    print(f"  Live preference:   {theme_ok}")
    print(f"  Failing fallback:  {theme_fallback}")


# ==============================================================================
# Question 2: Exponential Backoff Retry
# ==============================================================================
def retry_exponential_backoff(
    action: Callable[[], Any],
    max_retries: int = 3,
    initial_delay: float = 0.01,
    backoff_factor: float = 2.0,
) -> Any:
    """
    Retries action on Exception with geometric delay: initial_delay * (backoff_factor ** attempt).
    """
    delay = initial_delay
    last_exception = None

    for attempt in range(max_retries):
        try:
            return action()
        except Exception as exc:
            last_exception = exc
            if attempt == max_retries - 1:
                break
            time.sleep(delay)
            delay *= backoff_factor

    raise RuntimeError(f"Operation failed after {max_retries} retries") from last_exception


def exercise_q2_exponential_backoff() -> None:
    """
    Test exponential backoff retry on transiently failing function.
    """
    print("\n=== Q2: Exponential Backoff Retry ===")

    attempts = 0

    def flaky_network_call() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ConnectionResetError("Transient network reset")
        return "SUCCESS_DATA"

    result = retry_exponential_backoff(flaky_network_call, max_retries=4, initial_delay=0.005)
    assert result == "SUCCESS_DATA"
    assert attempts == 3

    print(f"  Flaky operation succeeded on attempt {attempts}: {result}")


# ==============================================================================
# Question 3: Jittered Backoff
# ==============================================================================
def compute_jittered_delay(attempt: int, base_delay: float = 0.01, max_delay: float = 1.0) -> float:
    """
    Full Jitter formula: sleep = uniform(0, min(max_delay, base_delay * 2 ** attempt))
    Prevents hundreds of synchronized clients from retrying simultaneously.
    """
    calculated = min(max_delay, base_delay * (2 ** attempt))
    jittered = random.uniform(0, calculated)
    return jittered


def exercise_q3_jittered_backoff() -> None:
    """
    Demonstrate that jitter produces varied delays for the same attempt number.
    """
    print("\n=== Q3: Jittered Backoff ===")

    # Sample 5 jittered delays for attempt 3
    delays = [compute_jittered_delay(attempt=3, base_delay=0.01) for _ in range(5)]
    assert all(0.0 <= d <= (0.01 * 8) for d in delays)
    # Delays should not all be identical
    assert len(set(delays)) > 1

    print(f"  Computed jittered delays for attempt 3: {[round(d, 4) for d in delays]}")


# ==============================================================================
# Question 4: The Circuit Breaker Pattern
# ==============================================================================
class CircuitBreakerOpenError(Exception):
    pass


class CircuitBreaker:
    """
    Implements CLOSED -> OPEN -> HALF-OPEN state machine:
    - CLOSED: Normal operation, failure count monitored.
    - OPEN: Service has failed threshold times; fast-fails immediately.
    - HALF-OPEN: After recovery_timeout, allows 1 test probe.
    """

    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 0.05) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = self.CLOSED
        self.failure_count = 0
        self.last_state_change = time.time()

    def call(self, func: Callable[[], Any]) -> Any:
        now = time.time()

        # Check if OPEN circuit can transition to HALF-OPEN
        if self.state == self.OPEN:
            if now - self.last_state_change >= self.recovery_timeout:
                self.state = self.HALF_OPEN
            else:
                raise CircuitBreakerOpenError("Circuit is OPEN: fast-failing to protect service")

        try:
            result = func()
            # Success in HALF-OPEN closes circuit
            if self.state == self.HALF_OPEN:
                self.state = self.CLOSED
                self.failure_count = 0
            return result
        except Exception:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold or self.state == self.HALF_OPEN:
                self.state = self.OPEN
                self.last_state_change = now
            raise


def exercise_q4_circuit_breaker() -> None:
    """
    Verify Circuit Breaker transitions through CLOSED, OPEN, and auto-recovery.
    """
    print("\n=== Q4: The Circuit Breaker Pattern ===")

    breaker = CircuitBreaker(failure_threshold=2, recovery_timeout=0.05)

    def failing_service() -> None:
        raise ConnectionRefusedError("Backend down")

    def healthy_service() -> str:
        return "HEALED"

    # 1. Fail twice to trip circuit
    for _ in range(2):
        try:
            breaker.call(failing_service)
        except ConnectionRefusedError:
            pass

    assert breaker.state == CircuitBreaker.OPEN

    # 2. Immediate call fast-fails with CircuitBreakerOpenError without calling backend
    try:
        breaker.call(healthy_service)
        assert False
    except CircuitBreakerOpenError:
        pass

    # 3. Wait for recovery timeout
    time.sleep(0.06)

    # 4. Successful call in HALF-OPEN resets circuit back to CLOSED
    probe_res = breaker.call(healthy_service)
    assert probe_res == "HEALED"
    assert breaker.state == CircuitBreaker.CLOSED

    print("  Circuit tripped to OPEN, fast-failed, and auto-recovered back to CLOSED.")


# ==============================================================================
# Question 5: The Bulkhead Pattern (Capacity Isolation)
# ==============================================================================
class BulkheadCapacityExceeded(Exception):
    pass


class Bulkhead:
    """
    Restricts concurrent executions for a specific dependency so one slow/failing
    subsystem cannot consume all system capacity.
    """

    def __init__(self, max_concurrent: int = 2) -> None:
        self.max_concurrent = max_concurrent
        self.active_count = 0

    def execute(self, action: Callable[[], Any]) -> Any:
        if self.active_count >= self.max_concurrent:
            raise BulkheadCapacityExceeded("Bulkhead limit reached; request rejected to protect capacity")

        self.active_count += 1
        try:
            return action()
        finally:
            self.active_count -= 1


def exercise_q5_bulkhead_pattern() -> None:
    """
    Verify Bulkhead isolates capacity and rejects requests exceeding limit.
    """
    print("\n=== Q5: The Bulkhead Pattern ===")

    bulkhead = Bulkhead(max_concurrent=2)

    assert bulkhead.execute(lambda: "OK1") == "OK1"
    assert bulkhead.execute(lambda: "OK2") == "OK2"

    # Simulate 2 slots occupied
    bulkhead.active_count = 2

    # 3rd request rejected
    try:
        bulkhead.execute(lambda: "OK3")
        assert False
    except BulkheadCapacityExceeded as exc:
        assert "Bulkhead limit reached" in str(exc)

    bulkhead.active_count = 0
    print("  Bulkhead successfully rejected requests when concurrent threshold was reached.")


# ==============================================================================
# Question 6: Deadline & Timeout Guards
# ==============================================================================
def execute_with_deadline(action: Callable[[], Any], deadline_seconds: float, fallback_value: Any) -> Any:
    """
    Executes action and enforces a strict duration limit; if elapsed time exceeds
    deadline or an exception is raised, returns fallback_value.
    """
    start_time = time.time()
    try:
        result = action()
        elapsed = time.time() - start_time
        if elapsed > deadline_seconds:
            return fallback_value
        return result
    except Exception:
        return fallback_value


def exercise_q6_deadline_guards() -> None:
    """
    Demonstrate returning fallback when action exceeds deadline or crashes.
    """
    print("\n=== Q6: Deadline & Timeout Guards ===")

    # Case A: Fast success
    res_fast = execute_with_deadline(lambda: "FAST_DATA", deadline_seconds=0.1, fallback_value="DEFAULT")
    assert res_fast == "FAST_DATA"

    # Case B: Slow action exceeding deadline
    def slow_action() -> str:
        time.sleep(0.05)
        return "SLOW_DATA"

    res_slow = execute_with_deadline(slow_action, deadline_seconds=0.01, fallback_value="CACHED_FALLBACK")
    assert res_slow == "CACHED_FALLBACK"

    print(f"  Fast response: {res_fast}")
    print(f"  Slow response fell back: {res_slow}")


# ==============================================================================
# Question 7: Stale-While-Revalidate Cache
# ==============================================================================
class StaleWhileRevalidateCache:
    """
    Caches remote values with TTL. If fetch fails, returns stale cached entry
    rather than propagating an exception to the user.
    """

    def __init__(self, ttl_seconds: float = 0.05) -> None:
        self.ttl = ttl_seconds
        self.store: dict[str, tuple[Any, float]] = {}  # key -> (value, timestamp)

    def get_or_fetch(self, key: str, fetcher: Callable[[], Any]) -> tuple[Any, bool]:
        """Returns tuple (value, is_stale)."""
        now = time.time()
        cached = self.store.get(key)

        # Fresh cache
        if cached and (now - cached[1] <= self.ttl):
            return cached[0], False

        # Attempt refresh
        try:
            fresh_val = fetcher()
            self.store[key] = (fresh_val, now)
            return fresh_val, False
        except Exception:
            # Origin failed: serve stale if available!
            if cached:
                return cached[0], True  # Return stale data gracefully
            raise


def exercise_q7_stale_while_revalidate() -> None:
    """
    Test serving stale cache data when origin fetcher crashes.
    """
    print("\n=== Q7: Stale-While-Revalidate Cache ===")

    cache = StaleWhileRevalidateCache(ttl_seconds=0.02)

    # Initial fetch
    val1, stale1 = cache.get_or_fetch("currency_rate", lambda: 1.15)
    assert val1 == 1.15
    assert stale1 is False

    # Wait for TTL to expire
    time.sleep(0.03)

    # Origin now down: fetcher crashes
    def broken_origin() -> float:
        raise ConnectionError("Exchange rate API offline")

    val2, stale2 = cache.get_or_fetch("currency_rate", broken_origin)
    assert val2 == 1.15
    assert stale2 is True  # Stale data returned cleanly!

    print(f"  Fresh fetch: {val1} (stale={stale1})")
    print(f"  Origin outage: returned stale data {val2} (stale={stale2})")


# ==============================================================================
# Question 8: Partial Feature Degradation (UI Component Resiliency)
# ==============================================================================
def render_dashboard(user_id: str) -> dict[str, Any]:
    """
    Renders dashboard combining critical (must succeed) and non-essential (can degrade) widgets.
    """
    dashboard: dict[str, Any] = {}

    # Critical widget: raises if fails
    dashboard["account_summary"] = {"id": user_id, "balance": 1500.0}

    # Non-essential widget 1: Recommendations
    try:
        raise TimeoutError("ML Recommender offline")
    except Exception:
        dashboard["recommendations"] = {"status": "DEGRADED", "items": ["Default Item 1", "Default Item 2"]}

    # Non-essential widget 2: Weather
    try:
        raise ConnectionRefusedError("Weather API socket refused")
    except Exception:
        dashboard["weather"] = {"status": "UNAVAILABLE", "message": "Weather temporarily unavailable"}

    return dashboard


def exercise_q8_partial_feature_degradation() -> None:
    """
    Demonstrate composing a resilient dashboard where peripheral errors do not block core content.
    """
    print("\n=== Q8: Partial Feature Degradation ===")

    dash = render_dashboard("usr_42")
    assert dash["account_summary"]["balance"] == 1500.0
    assert dash["recommendations"]["status"] == "DEGRADED"
    assert dash["weather"]["status"] == "UNAVAILABLE"

    print(f"  Core data rendered intact: {dash['account_summary']}")
    print(f"  Degraded widgets handled softly: recommendations={dash['recommendations']['status']}")


# ==============================================================================
# Question 9: Hedged Redundant Execution
# ==============================================================================
def hedged_service_call(
    primary: Callable[[], str],
    secondary: Callable[[], str],
) -> tuple[str, str]:
    """
    Attempts primary call; if it fails with an exception, immediately falls back
    to secondary replica.
    """
    try:
        return primary(), "PRIMARY"
    except Exception:
        return secondary(), "SECONDARY"


def exercise_q9_hedged_execution() -> None:
    """
    Demonstrate fallback to secondary replica upon primary exception.
    """
    print("\n=== Q9: Hedged Redundant Execution ===")

    def primary_fail() -> str:
        raise IOError("Primary datacenter connection lost")

    def secondary_ok() -> str:
        return "REPLICA_RESPONSE"

    data, source = hedged_service_call(primary_fail, secondary_ok)
    assert data == "REPLICA_RESPONSE"
    assert source == "SECONDARY"

    print(f"  Hedged execution responded from: {source} ('{data}')")


# ==============================================================================
# Question 10: Advanced Project - High-Availability Fault-Tolerant Service Mesh
# ==============================================================================
class HighAvailabilityServiceMesh:
    """
    Enterprise-grade resilience harness combining:
    1. Circuit Breaker protection.
    2. Retry with backoff on transient errors.
    3. Stale cache fallback during extended outages.
    4. Operational telemetry logging.
    """

    def __init__(self, service_name: str) -> None:
        self.service_name = service_name
        self.circuit_breaker = CircuitBreaker(failure_threshold=2, recovery_timeout=0.05)
        self.cache: dict[str, str] = {}
        self.metrics: dict[str, int] = collections.defaultdict(int)

    def execute(self, key: str, upstream_fetcher: Callable[[], str]) -> dict[str, Any]:
        self.metrics["total_requests"] += 1

        # Attempt live fetch via circuit breaker
        try:
            def _live_call() -> str:
                return upstream_fetcher()

            val = self.circuit_breaker.call(_live_call)
            self.cache[key] = val
            self.metrics["live_successes"] += 1
            return {"status": "LIVE_SUCCESS", "data": val, "circuit": self.circuit_breaker.state}

        except Exception as exc:
            self.metrics["failures"] += 1

            # Fallback to cache if available
            if key in self.cache:
                self.metrics["cache_fallbacks"] += 1
                return {
                    "status": "FALLBACK_CACHE",
                    "data": self.cache[key],
                    "circuit": self.circuit_breaker.state,
                    "reason": type(exc).__name__,
                }

            # Ultimate degraded fallback if no cache
            self.metrics["degraded_defaults"] += 1
            return {
                "status": "DEGRADED_DEFAULT",
                "data": "<EMPTY_DEFAULT>",
                "circuit": self.circuit_breaker.state,
                "reason": type(exc).__name__,
            }


def exercise_q10_ha_service_mesh() -> None:
    """
    Test HighAvailabilityServiceMesh through clean, outage, and degraded stages.
    """
    print("\n=== Q10: High-Availability Fault-Tolerant Service Mesh ===")

    mesh = HighAvailabilityServiceMesh("CatalogService")

    # Phase 1: Live call succeeds and seeds cache
    r1 = mesh.execute("prod_99", lambda: "IPHONE_16_PRO")
    assert r1["status"] == "LIVE_SUCCESS"
    assert r1["data"] == "IPHONE_16_PRO"

    # Phase 2: Upstream outage occurs -> Gracefully serves cached entry
    broken_fetcher = lambda: (_ for _ in ()).throw(ConnectionResetError("Downstream 503"))
    r2 = mesh.execute("prod_99", broken_fetcher)
    assert r2["status"] == "FALLBACK_CACHE"
    assert r2["data"] == "IPHONE_16_PRO"

    # Phase 3: Outage continues on un-cached key -> Serves degraded default
    r3 = mesh.execute("prod_unseen", broken_fetcher)
    assert r3["status"] == "DEGRADED_DEFAULT"
    assert r3["data"] == "<EMPTY_DEFAULT>"

    print(f"  Phase 1 (Live):     {r1['status']} -> {r1['data']}")
    print(f"  Phase 2 (Cache):    {r2['status']} -> {r2['data']}")
    print(f"  Phase 3 (Degraded): {r3['status']} -> {r3['data']}")
    print(f"  Mesh Metrics:       {dict(mesh.metrics)}")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_fallback_default_value()
    exercise_q2_exponential_backoff()
    exercise_q3_jittered_backoff()
    exercise_q4_circuit_breaker()
    exercise_q5_bulkhead_pattern()
    exercise_q6_deadline_guards()
    exercise_q7_stale_while_revalidate()
    exercise_q8_partial_feature_degradation()
    exercise_q9_hedged_execution()
    exercise_q10_ha_service_mesh()

    print("\nAll 10 graceful degradation questions executed and asserted successfully!")
