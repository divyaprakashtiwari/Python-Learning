"""
Topic 13: Testing and Debugging
Question 10: Defensive Programming

A comprehensive, production-grade guide to defensive programming patterns in Python.
Covers Design by Contract (preconditions, postconditions, invariants), EAFP vs LBYL race
condition avoidance, immutability & defensive copying, fail-fast input boundary validation,
graceful degradation & fallback defaults, idempotent operations, Circuit Breaker state machines,
resource leak prevention guards, path traversal taint neutralization, and an architectural
Resilient Microservice Gateway Defensive Shield.

Every question contains standalone runnable exercises verified with 100% assertions.
"""

import copy
import os
import time
from types import MappingProxyType
from typing import List, Dict, Any, Callable, Optional


# =====================================================================
# Q1: Design by Contract: Preconditions and Postconditions
# =====================================================================
def contract(precondition: Callable[[Any], bool], postcondition: Callable[[Any], bool]):
    """
    Decorator enforcing Design by Contract:
    - Verifies preconditions on input arguments before execution
    - Verifies postconditions on returned output before returning to caller
    """
    def decorator(fn: Callable):
        def wrapper(*args, **kwargs):
            if not precondition(*args, **kwargs):
                raise ValueError(f"Precondition failed for {fn.__name__} with args={args}, kwargs={kwargs}")
            result = fn(*args, **kwargs)
            if not postcondition(result):
                raise ValueError(f"Postcondition failed for {fn.__name__} with result={result}")
            return result
        return wrapper
    return decorator


@contract(
    precondition=lambda principal, rate, years: principal > 0 and 0.0 <= rate <= 1.0 and years >= 1,
    postcondition=lambda total: total > 0
)
def calculate_compound_interest(principal: float, rate: float, years: int) -> float:
    return principal * ((1.0 + rate) ** years)


def q1_design_by_contract():
    # Valid execution
    total = calculate_compound_interest(1000.0, 0.05, 3)
    assert round(total, 2) == 1157.63

    # Precondition violation: negative principal
    caught_pre = False
    try:
        calculate_compound_interest(-500.0, 0.05, 2)
    except ValueError as err:
        caught_pre = True
        assert "Precondition failed" in str(err)
    assert caught_pre is True

    # Precondition violation: rate > 1.0 (e.g. 150%)
    caught_rate = False
    try:
        calculate_compound_interest(1000.0, 1.5, 2)
    except ValueError:
        caught_rate = True
    assert caught_rate is True

    print("=== Q1: Design by Contract (Pre & Postconditions) Verified ===")


# =====================================================================
# Q2: EAFP vs LBYL: Race Condition (TOCTOU) Defense
# =====================================================================
def q2_eafp_vs_lbyl():
    """
    Demonstrates EAFP (Easier to Ask for Forgiveness than Permission)
    vs LBYL (Look Before You Leap) and why EAFP prevents Time-of-Check to
    Time-of-Use (TOCTOU) race conditions in concurrent systems.
    """
    store = {"balance": 150}

    # LBYL pattern (Look Before You Leap) - vulnerable to race conditions if key is deleted between check and read
    if "balance" in store:
        val_lbyl = store["balance"]
    else:
        val_lbyl = 0
    assert val_lbyl == 150

    # EAFP pattern (Easier to Ask for Forgiveness than Permission) - atomic & resilient
    try:
        val_eafp = store["balance"]
    except KeyError:
        val_eafp = 0
    assert val_eafp == 150

    # EAFP handles missing or deleted key without double lookup
    try:
        missing_val = store["missing_key"]
    except KeyError:
        missing_val = -1
    assert missing_val == -1

    print("=== Q2: EAFP vs LBYL Race Condition Defense Verified ===")


# =====================================================================
# Q3: Immutability and Defensive Copying
# =====================================================================
class SecureRegistry:
    """
    Defensively protects internal mutable state from external tampering
    using defensive copying and MappingProxyType read-only views.
    """
    def __init__(self, initial_items: List[Dict[str, Any]]):
        # Defensive deep copy on input to prevent caller from mutating internal state
        self._items = copy.deepcopy(initial_items)
        self._config = {"environment": "production", "max_retries": 3}

    def get_items(self) -> List[Dict[str, Any]]:
        # Defensive deep copy on output
        return copy.deepcopy(self._items)

    @property
    def config(self) -> MappingProxyType:
        # Read-only proxy view: mutating config raises TypeError
        return MappingProxyType(self._config)


def q3_immutability_and_defensive_copying():
    original_list = [{"id": 1, "name": "Secret Key"}]
    registry = SecureRegistry(original_list)

    # 1. Caller mutates original_list outside; internal registry is unaffected
    original_list[0]["name"] = "MUTATED_OUTSIDE"
    assert registry.get_items()[0]["name"] == "Secret Key"

    # 2. Caller mutates returned items; internal registry is unaffected
    leaked_list = registry.get_items()
    leaked_list[0]["name"] = "MUTATED_LEAK"
    assert registry.get_items()[0]["name"] == "Secret Key"

    # 3. Read-only MappingProxyType blocks dict mutation
    caught_proxy_mutation = False
    try:
        registry.config["environment"] = "development"
    except TypeError:
        caught_proxy_mutation = True
    assert caught_proxy_mutation is True
    assert registry.config["environment"] == "production"

    print("=== Q3: Immutability & Defensive Copying Verified ===")


# =====================================================================
# Q4: Fail-Fast Input Boundary Validation
# =====================================================================
def register_user_account(username: str, age: int, roles: List[str]) -> Dict[str, Any]:
    """
    Validates all inputs upfront (fail-fast) before allocating resources or performing side-effects.
    """
    if not isinstance(username, str) or not username.strip():
        raise ValueError("Username must be a non-empty string")
    if len(username) < 3 or len(username) > 30:
        raise ValueError("Username length must be between 3 and 30 characters")
    if not isinstance(age, int) or age < 18 or age > 120:
        raise ValueError("Age must be an integer between 18 and 120")
    if not isinstance(roles, list) or not roles:
        raise ValueError("Roles must be a non-empty list of strings")

    return {"username": username.strip(), "age": age, "roles": list(roles)}


def q4_fail_fast_input_validation():
    # Valid
    user = register_user_account("alice", 25, ["viewer"])
    assert user["username"] == "alice"

    # Fail fast on blank username
    caught_blank = False
    try:
        register_user_account("   ", 25, ["admin"])
    except ValueError as err:
        caught_blank = True
        assert "non-empty string" in str(err)
    assert caught_blank is True

    # Fail fast on under-age
    caught_age = False
    try:
        register_user_account("bob", 16, ["user"])
    except ValueError as err:
        caught_age = True
        assert "between 18 and 120" in str(err)
    assert caught_age is True

    print("=== Q4: Fail-Fast Boundary Validation Verified ===")


# =====================================================================
# Q5: Graceful Degradation and Fallback Patterns
# =====================================================================
def fetch_weather_recommendation(api_client: Callable[[], str]) -> str:
    """
    Calls primary weather API. If external service fails or times out,
    gracefully degrades to static default recommendation without crashing.
    """
    fallback_recommendation = "Moderate weather: dress comfortably."
    try:
        live_data = api_client()
        return f"Live forecast: {live_data}"
    except (TimeoutError, ConnectionError, RuntimeError):
        return fallback_recommendation


def q5_graceful_degradation_and_fallbacks():
    # Primary service online
    live_result = fetch_weather_recommendation(lambda: "Sunny and 72F")
    assert live_result == "Live forecast: Sunny and 72F"

    # Primary service fails (raises TimeoutError)
    def failing_service():
        raise TimeoutError("Weather provider unreachable")

    fallback_result = fetch_weather_recommendation(failing_service)
    assert fallback_result == "Moderate weather: dress comfortably."

    print("=== Q5: Graceful Degradation & Fallback Defaults Verified ===")


# =====================================================================
# Q6: Idempotent Operations and Deduplication Keys
# =====================================================================
class IdempotentAccount:
    """
    Guarantees that repeated executions of the same transaction (e.g. on network retries)
    execute exactly once using idempotency keys.
    """
    def __init__(self, initial_balance: float):
        self.balance = initial_balance
        self._processed_idempotency_keys: Dict[str, float] = {}

    def credit(self, amount: float, idempotency_key: str) -> float:
        if idempotency_key in self._processed_idempotency_keys:
            # Return cached result of previous execution without re-applying credit
            return self._processed_idempotency_keys[idempotency_key]

        self.balance += amount
        self._processed_idempotency_keys[idempotency_key] = self.balance
        return self.balance


def q6_idempotent_operations():
    account = IdempotentAccount(100.0)

    # First attempt applies credit
    bal1 = account.credit(50.0, idempotency_key="tx_req_001")
    assert bal1 == 150.0
    assert account.balance == 150.0

    # Duplicate network retry with same idempotency key
    bal2 = account.credit(50.0, idempotency_key="tx_req_001")
    assert bal2 == 150.0
    assert account.balance == 150.0  # NOT 200.0!

    # New transaction applies normally
    bal3 = account.credit(20.0, idempotency_key="tx_req_002")
    assert bal3 == 170.0
    assert account.balance == 170.0

    print("=== Q6: Idempotent Operations with Idempotency Keys Verified ===")


# =====================================================================
# Q7: Circuit Breaker State Machine
# =====================================================================
class CircuitBreakerOpenException(Exception):
    pass


class CircuitBreaker:
    """
    Prevents cascading system failure by short-circuiting calls to failing services.
    States: CLOSED (normal), OPEN (failing fast), HALF_OPEN (probing recovery).
    """
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

    def __init__(self, failure_threshold: int = 3, recovery_time_sec: float = 0.05):
        self.failure_threshold = failure_threshold
        self.recovery_time_sec = recovery_time_sec
        self.failure_count = 0
        self.state = self.CLOSED
        self.last_failure_time = 0.0

    def call(self, fn: Callable, *args, **kwargs) -> Any:
        now = time.time()

        if self.state == self.OPEN:
            if now - self.last_failure_time >= self.recovery_time_sec:
                self.state = self.HALF_OPEN
            else:
                raise CircuitBreakerOpenException("Circuit is OPEN: fast-failing call")

        try:
            result = fn(*args, **kwargs)
            # Success in CLOSED or HALF_OPEN resets breaker
            self.state = self.CLOSED
            self.failure_count = 0
            return result
        except Exception:
            self.failure_count += 1
            self.last_failure_time = now
            if self.failure_count >= self.failure_threshold:
                self.state = self.OPEN
            raise


def q7_circuit_breaker_pattern():
    cb = CircuitBreaker(failure_threshold=2, recovery_time_sec=0.03)

    def faulty_service(should_fail=True):
        if should_fail:
            raise ConnectionResetError("Remote server reset")
        return "SUCCESS"

    # Call 1 fails
    try:
        cb.call(faulty_service, should_fail=True)
    except ConnectionResetError:
        pass
    assert cb.state == CircuitBreaker.CLOSED

    # Call 2 fails -> reaches failure_threshold -> transitions to OPEN
    try:
        cb.call(faulty_service, should_fail=True)
    except ConnectionResetError:
        pass
    assert cb.state == CircuitBreaker.OPEN

    # Call 3 is immediately rejected by Circuit Breaker without calling service!
    caught_cb_open = False
    try:
        cb.call(faulty_service, should_fail=True)
    except CircuitBreakerOpenException:
        caught_cb_open = True
    assert caught_cb_open is True

    # Wait for recovery timeout
    time.sleep(0.04)

    # Probing call succeeds -> transitions back to CLOSED
    recovered_res = cb.call(faulty_service, should_fail=False)
    assert recovered_res == "SUCCESS"
    assert cb.state == CircuitBreaker.CLOSED

    print("=== Q7: Circuit Breaker State Machine Verified ===")


# =====================================================================
# Q8: Resource Leak Prevention Guards
# =====================================================================
class ManagedLock:
    def __init__(self):
        self.is_locked = False

    def acquire(self):
        self.is_locked = True

    def release(self):
        self.is_locked = False

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        # Does not suppress exceptions (returns None / False)


def q8_resource_leak_prevention():
    lock = ManagedLock()

    # Normal acquisition and release
    with lock:
        assert lock.is_locked is True
    assert lock.is_locked is False

    # Exception inside block: lock is guaranteed to release
    caught = False
    try:
        with lock:
            assert lock.is_locked is True
            raise RuntimeError("Unexpected failure during locked work")
    except RuntimeError:
        caught = True

    assert caught is True
    assert lock.is_locked is False  # Guaranteed unlocked!

    print("=== Q8: Resource Leak Prevention Guards Verified ===")


# =====================================================================
# Q9: Taint Checking & Path Traversal Neutralization
# =====================================================================
def safe_resolve_path(base_dir: str, untrusted_user_filename: str) -> str:
    """
    Defends against Directory Traversal Attacks (e.g. '../../etc/passwd').
    Ensures resolved path stays strictly within base_dir.
    """
    # 1. Neutralize null bytes
    clean_name = untrusted_user_filename.replace("\0", "")

    # 2. Resolve absolute path
    base_abs = os.path.abspath(base_dir)
    target_abs = os.path.abspath(os.path.join(base_abs, clean_name))

    # 3. Verify target_abs starts with base_abs
    common = os.path.commonpath([base_abs, target_abs])
    if common != base_abs:
        raise ValueError(f"Path traversal detected for filename: '{untrusted_user_filename}'")

    return target_abs


def q9_path_traversal_neutralization():
    base_sandbox = os.path.abspath("c:\\sandbox\\uploads" if os.name == "nt" else "/tmp/sandbox/uploads")

    # Safe path
    safe_path = safe_resolve_path(base_sandbox, "user_avatar.png")
    assert safe_path.startswith(base_sandbox)

    # Malicious path traversal
    caught_traversal = False
    try:
        safe_resolve_path(base_sandbox, "../../system/config.ini")
    except ValueError as err:
        caught_traversal = True
        assert "Path traversal detected" in str(err)

    assert caught_traversal is True
    print("=== Q9: Path Traversal Neutralization Verified ===")


# =====================================================================
# Q10: Architectural Resilient Microservice Gateway Defensive Shield
# =====================================================================
class DefensiveMicroserviceGateway:
    """
    Enterprise Defensive Shield combining:
    - Fail-fast parameter boundary validation
    - Defensive input payload copying
    - Circuit Breaker fault isolation
    - Graceful fallback degradation
    - Audit logging
    """
    def __init__(self, failure_threshold: int = 2):
        self.breaker = CircuitBreaker(failure_threshold=failure_threshold, recovery_time_sec=0.04)
        self.audit_log: List[str] = []

    def dispatch(self, payload: Dict[str, Any], remote_caller: Callable) -> Dict[str, Any]:
        # 1. Fail-fast input validation
        if not isinstance(payload, dict):
            raise TypeError("Payload must be a dictionary")
        if "action" not in payload:
            raise ValueError("Payload missing required 'action' field")

        # 2. Defensive copy
        safe_payload = copy.deepcopy(payload)

        # 3. Circuit breaker protected call with graceful fallback
        try:
            res = self.breaker.call(remote_caller, safe_payload)
            self.audit_log.append(f"SUCCESS:{safe_payload['action']}")
            return {"status": "SUCCESS", "data": res}
        except (CircuitBreakerOpenException, ConnectionError, TimeoutError) as err:
            self.audit_log.append(f"FALLBACK:{safe_payload['action']}:{type(err).__name__}")
            return {
                "status": "DEGRADED",
                "fallback": True,
                "reason": str(err),
                "data": {"cached_default": True}
            }


def q10_architectural_defensive_gateway():
    gateway = DefensiveMicroserviceGateway(failure_threshold=2)

    # 1. Normal dispatch
    res1 = gateway.dispatch({"action": "GET_RATES"}, lambda p: {"USD_EUR": 0.92})
    assert res1["status"] == "SUCCESS"
    assert res1["data"]["USD_EUR"] == 0.92

    # 2. Failing remote service triggers graceful fallback and opens breaker
    def bad_service(p):
        raise ConnectionError("Upstream dropped")

    res_f1 = gateway.dispatch({"action": "GET_RATES"}, bad_service)
    assert res_f1["status"] == "DEGRADED"
    assert res_f1["fallback"] is True

    res_f2 = gateway.dispatch({"action": "GET_RATES"}, bad_service)
    assert res_f2["status"] == "DEGRADED"

    # Circuit breaker is now OPEN; subsequent call short-circuits gracefully
    res_f3 = gateway.dispatch({"action": "GET_RATES"}, bad_service)
    assert res_f3["status"] == "DEGRADED"
    assert "Circuit is OPEN" in res_f3["reason"]

    # Verify audit logs
    assert len(gateway.audit_log) == 4
    assert gateway.audit_log[0] == "SUCCESS:GET_RATES"
    assert "CircuitBreakerOpenException" in gateway.audit_log[3]

    print("=== Q10: Architectural Defensive Gateway Shield Verified ===")


# =====================================================================
# Main Test Runner
# =====================================================================
if __name__ == "__main__":
    q1_design_by_contract()
    q2_eafp_vs_lbyl()
    q3_immutability_and_defensive_copying()
    q4_fail_fast_input_validation()
    q5_graceful_degradation_and_fallbacks()
    q6_idempotent_operations()
    q7_circuit_breaker_pattern()
    q8_resource_leak_prevention()
    q9_path_traversal_neutralization()
    q10_architectural_defensive_gateway()

    print("\nAll 10 defensive programming practice questions passed successfully!")
