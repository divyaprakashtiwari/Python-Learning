"""
Topic 07 - Exception Handling: Question 10
Problem: Distributed Service Resilience Engine: Circuit Breaker, Exponential Backoff, and Fallbacks.
"""

import time
from typing import Any, Callable, Dict, Optional


# 1. Custom Resilience Exceptions
class CircuitBreakerOpenError(Exception):
    """Raised when incoming requests are fast-rejected due to an open circuit."""
    pass


class ServiceUnavailableError(Exception):
    """Simulated remote service downstream outage error."""
    pass


# 2. Resilient Service Client
class ResilientServiceClient:
    """Manages circuit breaker states, exponential backoff retries, and graceful degradation."""

    def __init__(self, failure_threshold: int = 3, cooldown_seconds: float = 1.0):
        self.failure_threshold: int = failure_threshold
        self.cooldown_seconds: float = cooldown_seconds
        self.state: str = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.consecutive_failures: int = 0
        self.tripped_at: float = 0.0

    def _check_circuit_state(self) -> None:
        """Inspects and transitions circuit breaker state using monotonic timestamps."""
        if self.state == "OPEN":
            elapsed = time.monotonic() - self.tripped_at
            if elapsed >= self.cooldown_seconds:
                self.state = "HALF_OPEN"
                print("State transitions to HALF_OPEN.")
            else:
                raise CircuitBreakerOpenError(
                    f"Circuit is OPEN (cooldown remaining: {self.cooldown_seconds - elapsed:.2f}s)"
                )

    def execute_with_retry(
        self,
        operation_func: Callable[[], Any],
        max_retries: int = 3,
        base_delay: float = 0.02
    ) -> Any:
        """Executes operation with exponential backoff; updates failure counts and trips breaker."""
        self._check_circuit_state()

        last_error: Optional[Exception] = None
        for attempt in range(max_retries):
            try:
                result = operation_func()
                # On successful execution
                if self.state == "HALF_OPEN":
                    self.state = "CLOSED"
                    self.consecutive_failures = 0
                    print("Canary succeeds -> Circuit state resets to CLOSED.")
                elif self.state == "CLOSED":
                    self.consecutive_failures = 0
                return result

            except ServiceUnavailableError as err:
                last_error = err
                time.sleep(base_delay * (2 ** attempt))

        # All retries exhausted
        if self.state == "HALF_OPEN":
            self.state = "OPEN"
            self.tripped_at = time.monotonic()
        elif self.state == "CLOSED":
            self.consecutive_failures += 1
            if self.consecutive_failures >= self.failure_threshold:
                self.state = "OPEN"
                self.tripped_at = time.monotonic()
                print(
                    f"Retried {max_retries} times -> Failed -> "
                    f"Circuit failure count: {self.consecutive_failures} -> State tripped to OPEN!"
                )
            else:
                print(
                    f"Retried {max_retries} times -> Failed -> "
                    f"Circuit failure count: {self.consecutive_failures}"
                )

        raise last_error if last_error else RuntimeError("Execution failed")

    def safe_fetch_user_profile(
        self,
        user_id: str,
        cached_fallback: Dict[str, Any],
        operation_func: Callable[[], Any]
    ) -> Dict[str, Any]:
        """Wraps remote operation with graceful degradation fallback upon outage or open breaker."""
        _ = user_id
        try:
            data = self.execute_with_retry(operation_func)
            return {"data": data, "status": "LIVE", "circuit_state": self.state}
        except (CircuitBreakerOpenError, ServiceUnavailableError) as err:
            if isinstance(err, CircuitBreakerOpenError):
                print("Call 4: Fast-failed immediately! Caught CircuitBreakerOpenError. Fallback returned.")
            return {"data": cached_fallback, "status": "DEGRADED", "circuit_state": self.state}


# Verification & Simulation
client = ResilientServiceClient(failure_threshold=3, cooldown_seconds=1.0)
fallback_profile = {"id": "U-100", "name": "Cached User", "tier": "FREE"}

call_counter = 0


def mock_flaky_remote() -> Dict[str, Any]:
    global call_counter
    call_counter += 1
    # Fails for first 15 internal attempts (across multiple calls)
    if call_counter <= 15:
        raise ServiceUnavailableError("503 Service Unavailable")
    return {"id": "U-100", "name": "Live Alice", "tier": "PREMIUM"}


# 1. Calls 1 through 3 fail, tripping breaker
for i in range(1, 4):
    print(f"Call {i}:", end=" ")
    res = client.safe_fetch_user_profile(f"U-{i}", fallback_profile, mock_flaky_remote)

# 2. Call 4: Fast-fails immediately due to OPEN state
res_fast_fail = client.safe_fetch_user_profile("U-4", fallback_profile, mock_flaky_remote)
print("Result for Call 4:", res_fast_fail)

# 3. Canary Probe Test after cooldown
print("\nCanary Probe Test (after 1.0s cooldown):")
time.sleep(1.05)


def mock_recovered_remote() -> Dict[str, Any]:
    return {"id": "U-100", "name": "Live Alice", "tier": "PREMIUM"}


canary_res = client.safe_fetch_user_profile("U-Canary", fallback_profile, mock_recovered_remote)
print(f"Post-Recovery Circuit State: {client.state}")
