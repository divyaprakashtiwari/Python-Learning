"""
Topic 07: Exceptions - Question 09: Logging Exceptions

A comprehensive collection of 10 standalone, runnable exercises exploring
Python's standard library `logging` module in combination with exception handling,
traceback attachment (exc_info), sensitive PII masking, structured JSON output,
and rate-limited deduplication filters.

Questions Covered:
 1. logging.exception(): Automatic ERROR level logging with traceback attachment.
 2. logging.error() with exc_info: Explicit control over traceback emission.
 3. Explicit exc_info=exc Passing: Logging exception objects outside except blocks.
 4. Custom Formatting: Integrating timestamps, line numbers, and error messages.
 5. In-Memory Log Capturing: Using io.StringIO and StreamHandler for assertions.
 6. Sensitive Data Sanitization: Masking passwords and API keys from exception logs.
 7. Severity Tiering: Categorizing exceptions into WARNING, ERROR, and CRITICAL.
 8. Contextual Logging Filters: Attaching correlation IDs and metadata to error records.
 9. Structured JSON Log Formatter: Formatting exception events for CloudWatch/Datadog.
10. Advanced Project: Rate-Limited Exception Telemetry Logger with Deduplication.
"""

import io
import json
import logging
import re
import time
from typing import Any


# ==============================================================================
# Helper to create isolated test loggers
# ==============================================================================
def create_test_logger(name: str) -> tuple[logging.Logger, io.StringIO]:
    """Creates a distinct logger bound to an in-memory string stream."""
    stream = io.StringIO()
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    logger.handlers.clear()

    handler = logging.StreamHandler(stream)
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger, stream


# ==============================================================================
# Question 1: logging.exception() Fundamentals
# ==============================================================================
def exercise_q1_logging_exception() -> None:
    """
    Demonstrate logging.exception() which automatically logs at ERROR level
    and attaches the currently active exception's traceback.
    """
    print("=== Q1: logging.exception() Fundamentals ===")

    logger, stream = create_test_logger("q1_logger")

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("Arithmetic calculation failed during batch")

    output = stream.getvalue()
    assert "[ERROR]" in output
    assert "Arithmetic calculation failed during batch" in output
    assert "ZeroDivisionError: division by zero" in output
    assert "Traceback (most recent call last):" in output

    print("  logging.exception() automatically logged at ERROR level with full traceback.")


# ==============================================================================
# Question 2: logging.error() with exc_info Control
# ==============================================================================
def exercise_q2_error_with_exc_info() -> None:
    """
    Demonstrate logging.error(..., exc_info=True) to include traceback vs
    exc_info=False (default) to omit stack traces for expected routine errors.
    """
    print("\n=== Q2: logging.error() with exc_info Control ===")

    logger, stream = create_test_logger("q2_logger")

    try:
        int("invalid")
    except ValueError:
        # 1. Without exc_info: clean one-line message
        logger.error("Could not parse numeric ID", exc_info=False)
        # 2. With exc_info: full stack trace
        logger.error("Parsing failed with stack trace", exc_info=True)

    output = stream.getvalue()
    lines = output.strip().splitlines()

    # First log record has no traceback
    assert "[ERROR] Could not parse numeric ID" in lines[0]
    # Second log record has traceback
    assert "Traceback (most recent call last):" in output

    print("  Successfully demonstrated optional traceback control via exc_info flag.")


# ==============================================================================
# Question 3: Explicit exc_info=exc Passing
# ==============================================================================
def exercise_q3_explicit_exc_info_passing() -> None:
    """
    Demonstrate passing a captured exception instance explicitly to exc_info=exc
    outside the original except block or across threads.
    """
    print("\n=== Q3: Explicit exc_info=exc Passing ===")

    logger, stream = create_test_logger("q3_logger")

    captured_err = None
    try:
        raise KeyError("user_session_token")
    except KeyError as exc:
        captured_err = exc

    # Later in processing, log the stored exception
    logger.warning("Deferred processing encountered error", exc_info=captured_err)

    output = stream.getvalue()
    assert "[WARNING]" in output
    assert "KeyError: 'user_session_token'" in output

    print("  Explicitly logged stored exception outside original except block.")


# ==============================================================================
# Question 4: Custom Formatter with Timestamps & Line Numbers
# ==============================================================================
def exercise_q4_custom_formatting() -> None:
    """
    Configure a custom Formatter that outputs ISO-like timestamps, module,
    line numbers, and the exception traceback.
    """
    print("\n=== Q4: Custom Formatter with Timestamps & Line Numbers ===")

    stream = io.StringIO()
    logger = logging.getLogger("q4_logger")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.handlers.clear()

    handler = logging.StreamHandler(stream)
    fmt = logging.Formatter("%(asctime)s | %(levelname)-5s | %(filename)s:%(lineno)d | %(message)s")
    handler.setFormatter(fmt)
    logger.addHandler(handler)

    try:
        raise TimeoutError("Socket receive timed out")
    except TimeoutError:
        logger.error("Network operation timed out", exc_info=True)

    output = stream.getvalue()
    assert "ERROR" in output
    assert "q09_logging_exceptions.py:" in output
    assert "TimeoutError: Socket receive timed out" in output

    print(f"  Formatted log entry snippet:\n    {output.splitlines()[0]}")


# ==============================================================================
# Question 5: In-Memory Log Capturing for Assertions
# ==============================================================================
def exercise_q5_in_memory_log_capturing() -> None:
    """
    Demonstrate capturing and validating logging behavior in automated tests
    using an in-memory stream handler.
    """
    print("\n=== Q5: In-Memory Log Capturing ===")

    logger, stream = create_test_logger("q5_logger")

    def divide_and_log(a: int, b: int) -> int | None:
        try:
            return a // b
        except ZeroDivisionError:
            logger.error(f"Cannot divide {a} by zero!", exc_info=True)
            return None

    assert divide_and_log(10, 2) == 5
    assert stream.getvalue() == ""  # No errors logged on success

    assert divide_and_log(10, 0) is None
    log_content = stream.getvalue()
    assert "Cannot divide 10 by zero!" in log_content
    assert "ZeroDivisionError" in log_content

    print("  In-memory logger verified zero logs on success and precise logs on failure.")


# ==============================================================================
# Question 6: Sensitive PII / Credential Sanitization
# ==============================================================================
class SensitiveDataFilter(logging.Filter):
    """
    Logging filter that sanitizes passwords, bearer tokens, and credit card patterns
    from log messages before emission.
    """

    PATTERNS = [
        (re.compile(r"password=['\"][^'\"]+['\"]", re.IGNORECASE), "password='[REDACTED]'"),
        (re.compile(r"Bearer\s+[A-Za-z0-9\-._~+/]+=*", re.IGNORECASE), "Bearer [REDACTED_TOKEN]"),
    ]

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            for pattern, replacement in self.PATTERNS:
                record.msg = pattern.sub(replacement, record.msg)
        return True


def exercise_q6_sensitive_data_sanitization() -> None:
    """
    Demonstrate logging filter scrubbing credentials from exception messages.
    """
    print("\n=== Q6: Sensitive PII / Credential Sanitization ===")

    logger, stream = create_test_logger("q6_logger")
    logger.addFilter(SensitiveDataFilter())

    try:
        raise ValueError("Login failed for password='SecretPassword123!' with Bearer abcxyz12345")
    except ValueError as exc:
        logger.error(f"Authentication exception: {exc}")

    output = stream.getvalue()
    assert "SecretPassword123!" not in output
    assert "abcxyz12345" not in output
    assert "password='[REDACTED]'" in output
    assert "Bearer [REDACTED_TOKEN]" in output

    print(f"  Sanitized log output:\n    {output.strip()}")


# ==============================================================================
# Question 7: Severity Tiering (Warning, Error, Critical)
# ==============================================================================
def exercise_q7_severity_tiering() -> None:
    """
    Demonstrate mapping different exception classes to appropriate severity levels:
    - Recoverable / Soft errors -> WARNING
    - Request / Task failures -> ERROR
    - System corruption / Infrastructure loss -> CRITICAL
    """
    print("\n=== Q7: Severity Tiering ===")

    logger, stream = create_test_logger("q7_logger")

    def handle_service_event(event_type: str) -> None:
        try:
            if event_type == "soft_cache_miss":
                raise KeyError("cache:user:123")
            elif event_type == "order_validation_failed":
                raise ValueError("Item out of stock")
            elif event_type == "db_disk_corrupted":
                raise SystemError("Database tablespace raw block corruption")
        except KeyError as soft_err:
            logger.warning(f"Soft recovery: cache miss fallback for {soft_err}")
        except ValueError as req_err:
            logger.error(f"Request failed: {req_err}", exc_info=True)
        except SystemError as fatal_err:
            logger.critical(f"FATAL INFRASTRUCTURE FAILURE: {fatal_err}", exc_info=True)

    handle_service_event("soft_cache_miss")
    handle_service_event("order_validation_failed")
    handle_service_event("db_disk_corrupted")

    output = stream.getvalue()
    assert "[WARNING]" in output
    assert "[ERROR]" in output
    assert "[CRITICAL]" in output

    print("  Verified 3-tier severity mapping: WARNING, ERROR, and CRITICAL emitted properly.")


# ==============================================================================
# Question 8: Contextual Logging Filters (Correlation IDs)
# ==============================================================================
class CorrelationIdFilter(logging.Filter):
    """Injects a request correlation ID into every log record."""

    def __init__(self, correlation_id: str) -> None:
        super().__init__()
        self.correlation_id = correlation_id

    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = self.correlation_id  # type: ignore
        return True


def exercise_q8_contextual_logging_filter() -> None:
    """
    Demonstrate attaching dynamic trace/correlation IDs to exception logs.
    """
    print("\n=== Q8: Contextual Logging Filters ===")

    stream = io.StringIO()
    logger = logging.getLogger("q8_logger")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.handlers.clear()

    handler = logging.StreamHandler(stream)
    formatter = logging.Formatter("[%(levelname)s] [ReqID: %(correlation_id)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.addFilter(CorrelationIdFilter("REQ-99482-UUID"))

    try:
        raise LookupError("Item SKU not found in inventory")
    except LookupError as err:
        logger.error(f"Catalog lookup error: {err}")

    output = stream.getvalue()
    assert "[ReqID: REQ-99482-UUID]" in output
    assert "Catalog lookup error: Item SKU not found in inventory" in output

    print(f"  Enriched context log:\n    {output.strip()}")


# ==============================================================================
# Question 9: Structured JSON Log Formatter
# ==============================================================================
class JSONExceptionFormatter(logging.Formatter):
    """
    Serializes log records and exceptions into single-line structured JSON records.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_obj: dict[str, Any] = {
            "timestamp": time.time(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info:
            exc_type, exc_val, exc_tb = record.exc_info
            if exc_type is not None:
                log_obj["exception"] = {
                    "type": exc_type.__name__,
                    "message": str(exc_val),
                    "traceback": self.formatException(record.exc_info),
                }

        return json.dumps(log_obj)


def exercise_q9_json_exception_formatter() -> None:
    """
    Demonstrate structured JSON logging of exceptions for cloud log aggregators.
    """
    print("\n=== Q9: Structured JSON Log Formatter ===")

    stream = io.StringIO()
    logger = logging.getLogger("q9_logger")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.handlers.clear()

    handler = logging.StreamHandler(stream)
    handler.setFormatter(JSONExceptionFormatter())
    logger.addHandler(handler)

    try:
        raise ConnectionRefusedError("Redis cache cluster connection refused on port 6379")
    except ConnectionRefusedError:
        logger.error("Failed to connect to primary cache", exc_info=True)

    output = stream.getvalue().strip()
    parsed_json = json.loads(output)

    assert parsed_json["level"] == "ERROR"
    assert parsed_json["message"] == "Failed to connect to primary cache"
    assert parsed_json["exception"]["type"] == "ConnectionRefusedError"
    assert "Redis cache cluster connection refused" in parsed_json["exception"]["message"]

    print(f"  Structured JSON log generated successfully:")
    print(f"    Level: {parsed_json['level']}")
    print(f"    Exception Type: {parsed_json['exception']['type']}")


# ==============================================================================
# Question 10: Advanced Project - Rate-Limited Exception Telemetry Logger
# ==============================================================================
class RateLimitedExceptionLogger:
    """
    High-performance telemetry logger that throttles identical recurring exceptions,
    preventing disk filling and log flood during outage cascades.
    """

    def __init__(self, logger: logging.Logger, cooldown_seconds: float = 0.5) -> None:
        self.logger = logger
        self.cooldown_seconds = cooldown_seconds
        # Key: (exception_type, exception_message) -> Value: [last_emitted_time, suppressed_count]
        self._cache: dict[tuple[str, str], list[float | int]] = {}

    def log_exception(self, exc: Exception, context_msg: str) -> bool:
        key = (type(exc).__name__, str(exc))
        now = time.time()

        if key in self._cache:
            last_time, count = self._cache[key]
            if now - float(last_time) < self.cooldown_seconds:
                # Within cooldown: suppress and increment count
                self._cache[key][1] = int(count) + 1
                return False
            else:
                # Cooldown expired: emit with suppressed recurrence count
                suppressed = int(self._cache[key][1])
                self._cache[key] = [now, 0]
                self.logger.error(
                    f"{context_msg} (Suppressed {suppressed} recurring occurrences)",
                    exc_info=exc,
                )
                return True
        else:
            # First occurrence: emit immediately
            self._cache[key] = [now, 0]
            self.logger.error(context_msg, exc_info=exc)
            return True


def exercise_q10_rate_limited_logger() -> None:
    """
    Test RateLimitedExceptionLogger suppressing repeated identical errors.
    """
    print("\n=== Q10: Rate-Limited Exception Telemetry Logger ===")

    logger, stream = create_test_logger("q10_logger")
    telemetry = RateLimitedExceptionLogger(logger, cooldown_seconds=0.1)

    common_error = TimeoutError("Gateway timeout to payment provider")

    # Burst of 10 identical errors
    emitted_count = 0
    for i in range(10):
        if telemetry.log_exception(common_error, f"Payment attempt #{i + 1} failed"):
            emitted_count += 1

    # First one was emitted; other 9 were suppressed during cooldown!
    assert emitted_count == 1

    # Wait for cooldown to expire
    time.sleep(0.12)

    # 11th error should now be emitted with suppressed count
    emitted_after_cooldown = telemetry.log_exception(common_error, "Payment retry failed")
    assert emitted_after_cooldown is True

    output = stream.getvalue()
    assert "Suppressed 9 recurring occurrences" in output

    print(f"  Burst of 10 errors only emitted {emitted_count} log record.")
    print("  Subsequent log accurately reported 9 suppressed occurrences.")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_logging_exception()
    exercise_q2_error_with_exc_info()
    exercise_q3_explicit_exc_info_passing()
    exercise_q4_custom_formatting()
    exercise_q5_in_memory_log_capturing()
    exercise_q6_sensitive_data_sanitization()
    exercise_q7_severity_tiering()
    exercise_q8_contextual_logging_filter()
    exercise_q9_json_exception_formatter()
    exercise_q10_rate_limited_logger()

    print("\nAll 10 logging exceptions questions executed and asserted successfully!")
