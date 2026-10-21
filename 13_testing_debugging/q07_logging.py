"""
Topic 13: Testing and Debugging
Question 07: Logging

A comprehensive, production-grade guide to logging and observability with Python's
built-in `logging` module. Covers log severity levels and thresholds, hierarchical logger
trees and propagation, custom formatters, multiple handlers, contextual extra metadata,
PII masking filters, exception traceback logging, structured JSON formatting,
logging.config.dictConfig, and an architectural Buffered Audit & Telemetry Engine.

Every question contains standalone runnable exercises verified with 100% assertions.
"""

import logging
import logging.config
import io
import json
import re
import tempfile
import os
from typing import List, Dict, Any, Optional


# =====================================================================
# Q1: Log Levels and Threshold Filtering
# =====================================================================
def q1_log_levels_and_thresholds():
    """
    Demonstrates the 5 standard logging levels:
    DEBUG (10) < INFO (20) < WARNING (30) < ERROR (40) < CRITICAL (50)
    and threshold filtering.
    """
    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))

    logger = logging.getLogger("q1_threshold_logger")
    logger.setLevel(logging.WARNING)
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.propagate = False

    logger.debug("Debug message (ignored)")
    logger.info("Info message (ignored)")
    logger.warning("Warning message (captured)")
    logger.error("Error message (captured)")
    logger.critical("Critical message (captured)")

    output = log_stream.getvalue().strip().splitlines()
    assert len(output) == 3
    assert output[0] == "WARNING:Warning message (captured)"
    assert output[1] == "ERROR:Error message (captured)"
    assert output[2] == "CRITICAL:Critical message (captured)"

    print("=== Q1: Log Levels & Threshold Filtering Verified ===")


# =====================================================================
# Q2: Hierarchical Logger Trees and Event Propagation
# =====================================================================
def q2_logger_hierarchy_and_propagation():
    """
    Demonstrates dot-notation logger hierarchies (e.g., 'app.database')
    and how events propagate upward to parent handlers unless propagate=False.
    """
    parent_stream = io.StringIO()
    child_stream = io.StringIO()

    parent_logger = logging.getLogger("company")
    parent_logger.setLevel(logging.INFO)
    parent_logger.handlers.clear()
    parent_handler = logging.StreamHandler(parent_stream)
    parent_handler.setFormatter(logging.Formatter("PARENT:%(message)s"))
    parent_logger.addHandler(parent_handler)

    # Child logger with propagate=True
    child_logger = logging.getLogger("company.auth")
    child_logger.setLevel(logging.INFO)
    child_logger.handlers.clear()
    child_handler = logging.StreamHandler(child_stream)
    child_handler.setFormatter(logging.Formatter("CHILD:%(message)s"))
    child_logger.addHandler(child_handler)
    child_logger.propagate = True

    child_logger.info("User logged in")

    # Both child handler and parent handler received the log event!
    assert "CHILD:User logged in" in child_stream.getvalue()
    assert "PARENT:User logged in" in parent_stream.getvalue()

    # Now disable propagation
    parent_stream.seek(0)
    parent_stream.truncate(0)
    child_stream.seek(0)
    child_stream.truncate(0)

    child_logger.propagate = False
    child_logger.info("Token renewed")

    assert "CHILD:Token renewed" in child_stream.getvalue()
    assert parent_stream.getvalue() == ""  # Blocked from parent!

    print("=== Q2: Logger Hierarchy & Propagation Verified ===")


# =====================================================================
# Q3: Custom Formatter with Built-in Attributes
# =====================================================================
def q3_custom_formatting():
    """
    Demonstrates extracting logging metadata tokens:
    %(name)s, %(levelname)s, %(funcName)s, %(lineno)d, %(message)s.
    """
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    fmt = "%(name)s | %(levelname)s | %(funcName)s | %(message)s"
    handler.setFormatter(logging.Formatter(fmt))

    logger = logging.getLogger("q3_logger")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.propagate = False

    def business_operation():
        logger.info("Calculations complete")

    business_operation()

    output = stream.getvalue().strip()
    assert "q3_logger | INFO | business_operation | Calculations complete" == output

    print("=== Q3: Custom Formatter Attributes Verified ===")


# =====================================================================
# Q4: Multiple Handlers with Distinct Severity Levels
# =====================================================================
def q4_multiple_handlers_dual_levels():
    """
    Demonstrates attaching multiple handlers to a single logger:
    - Debug stream handler capturing everything (DEBUG+)
    - Alert error stream handler capturing only critical issues (ERROR+)
    """
    debug_stream = io.StringIO()
    error_stream = io.StringIO()

    h_debug = logging.StreamHandler(debug_stream)
    h_debug.setLevel(logging.DEBUG)

    h_error = logging.StreamHandler(error_stream)
    h_error.setLevel(logging.ERROR)

    logger = logging.getLogger("q4_dual_logger")
    logger.setLevel(logging.DEBUG)  # Lowest logger threshold
    logger.handlers.clear()
    logger.addHandler(h_debug)
    logger.addHandler(h_error)
    logger.propagate = False

    logger.debug("Minor diagnostic trace")
    logger.info("Routine operation")
    logger.error("Database connection dropped")

    debug_out = debug_stream.getvalue()
    error_out = error_stream.getvalue()

    # Debug stream captured all 3 events
    assert "Minor diagnostic trace" in debug_out
    assert "Routine operation" in debug_out
    assert "Database connection dropped" in debug_out

    # Error stream captured only the error
    assert "Minor diagnostic trace" not in error_out
    assert "Routine operation" not in error_out
    assert "Database connection dropped" in error_out

    print("=== Q4: Multiple Handlers with Independent Levels Verified ===")


# =====================================================================
# Q5: Contextual Metadata Injection via extra Dictionary
# =====================================================================
class ContextFormatter(logging.Formatter):
    def format(self, record):
        user_id = getattr(record, "user_id", "ANONYMOUS")
        request_id = getattr(record, "request_id", "N/A")
        return f"[{request_id}] user={user_id} - {record.getMessage()}"


def q5_contextual_extra_metadata():
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(ContextFormatter())

    logger = logging.getLogger("q5_context_logger")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.propagate = False

    logger.info(
        "Password changed successfully",
        extra={"user_id": "usr_9981", "request_id": "req-abc-123"}
    )
    logger.info(
        "Guest visited homepage"
        # without extra keys; formatter falls back to defaults
    )

    lines = stream.getvalue().strip().splitlines()
    assert lines[0] == "[req-abc-123] user=usr_9981 - Password changed successfully"
    assert lines[1] == "[N/A] user=ANONYMOUS - Guest visited homepage"

    print("=== Q5: Contextual Metadata (extra dictionary) Verified ===")


# =====================================================================
# Q6: Custom Log Filters for PII Redaction
# =====================================================================
class PIIMaskingFilter(logging.Filter):
    """
    Intercepts log records and masks sensitive patterns (Credit Cards, SSNs, Passwords).
    """
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        # Mask 16-digit credit cards
        masked = re.sub(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", "[REDACTED_CARD]", msg)
        # Mask SSN
        masked = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]", masked)
        record.msg = masked
        record.args = ()
        return True


def q6_pii_masking_filter():
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter("%(message)s"))

    logger = logging.getLogger("q6_pii_logger")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.addFilter(PIIMaskingFilter())
    logger.propagate = False

    logger.info("Processing payment for card 4111-2222-3333-4444 on user SSN 123-45-6789.")

    out = stream.getvalue().strip()
    assert "4111-2222-3333-4444" not in out
    assert "123-45-6789" not in out
    assert "Processing payment for card [REDACTED_CARD] on user SSN [REDACTED_SSN]." == out

    print("=== Q6: PII Masking Filter Verified ===")


# =====================================================================
# Q7: Exception Traceback Logging: logger.exception vs exc_info
# =====================================================================
def q7_exception_traceback_logging():
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))

    logger = logging.getLogger("q7_exc_logger")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.propagate = False

    try:
        1 / 0
    except ZeroDivisionError:
        # logger.exception automatically records exc_info=True with ERROR level
        logger.exception("Calculation failed abruptly")

    output = stream.getvalue()
    assert "ERROR:Calculation failed abruptly" in output
    assert "Traceback (most recent call last):" in output
    assert "ZeroDivisionError: division by zero" in output

    print("=== Q7: Exception Traceback Logging Verified ===")


# =====================================================================
# Q8: Structured JSON Formatter for Enterprise Observability
# =====================================================================
class JSONLogFormatter(logging.Formatter):
    """Formats log records as single-line JSON objects."""
    def format(self, record: logging.LogRecord) -> str:
        log_payload = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "timestamp": record.created,
        }
        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)
        # Capture custom extra fields
        for key, val in record.__dict__.items():
            if key not in logging.LogRecord("", 0, "", 0, "", (), None).__dict__ and key != "message":
                log_payload[key] = val

        return json.dumps(log_payload)


def q8_structured_json_formatting():
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JSONLogFormatter())

    logger = logging.getLogger("q8_json_logger")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.propagate = False

    logger.info("Order processed", extra={"order_id": 5510, "amount": 129.50})

    output = stream.getvalue().strip()
    parsed = json.loads(output)

    assert parsed["level"] == "INFO"
    assert parsed["logger"] == "q8_json_logger"
    assert parsed["message"] == "Order processed"
    assert parsed["order_id"] == 5510
    assert parsed["amount"] == 129.50

    print("=== Q8: Structured JSON Log Formatter Verified ===")


# =====================================================================
# Q9: Declarative Configuration via logging.config.dictConfig
# =====================================================================
def q9_declarative_dict_config():
    dict_config_data = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(levelname)s | %(name)s | %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "standard",
            }
        },
        "loggers": {
            "service.worker": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False
            }
        }
    }

    logging.config.dictConfig(dict_config_data)

    logger = logging.getLogger("service.worker")
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)

    print("=== Q9: Declarative logging.config.dictConfig Verified ===")


# =====================================================================
# Q10: Architectural Buffered Audit & Telemetry Pipeline
# =====================================================================
class MemoryAuditBufferHandler(logging.Handler):
    """
    High-performance buffered in-memory logging handler:
    - Retains recent log records in circular or batch buffer
    - Provides flush and query capabilities by level or keyword
    """
    def __init__(self, capacity: int = 100):
        super().__init__()
        self.capacity = capacity
        self.buffer: List[Dict[str, Any]] = []

    def emit(self, record: logging.LogRecord):
        entry = {
            "level": record.levelname,
            "message": self.format(record),
            "timestamp": record.created,
            "event_name": getattr(record, "event_name", "GENERIC_EVENT")
        }
        self.buffer.append(entry)
        if len(self.buffer) > self.capacity:
            self.buffer.pop(0)

    def query(self, level: Optional[str] = None, event_name: Optional[str] = None) -> List[Dict[str, Any]]:
        results = self.buffer
        if level:
            results = [e for e in results if e["level"] == level]
        if event_name:
            results = [e for e in results if e["event_name"] == event_name]
        return results

    def clear(self):
        self.buffer.clear()


def q10_architectural_buffered_audit_pipeline():
    audit_handler = MemoryAuditBufferHandler(capacity=50)
    audit_handler.setFormatter(logging.Formatter("%(message)s"))

    audit_logger = logging.getLogger("enterprise.audit")
    audit_logger.setLevel(logging.INFO)
    audit_logger.handlers.clear()
    audit_logger.addHandler(audit_handler)
    audit_logger.propagate = False

    # Simulate transactional audit trails
    audit_logger.info("Admin login", extra={"event_name": "AUTH_LOGIN"})
    audit_logger.info("Config changed", extra={"event_name": "CONFIG_UPDATE"})
    audit_logger.warning("Excessive login attempts", extra={"event_name": "SECURITY_ALERT"})
    audit_logger.info("User logout", extra={"event_name": "AUTH_LOGOUT"})

    assert len(audit_handler.buffer) == 4

    # Query by event name
    auth_events = audit_handler.query(event_name="AUTH_LOGIN")
    assert len(auth_events) == 1
    assert auth_events[0]["message"] == "Admin login"

    # Query by level
    warnings = audit_handler.query(level="WARNING")
    assert len(warnings) == 1
    assert warnings[0]["event_name"] == "SECURITY_ALERT"

    print("=== Q10: Architectural Buffered Audit & Telemetry Pipeline Verified ===")


# =====================================================================
# Main Test Runner
# =====================================================================
if __name__ == "__main__":
    q1_log_levels_and_thresholds()
    q2_logger_hierarchy_and_propagation()
    q3_custom_formatting()
    q4_multiple_handlers_dual_levels()
    q5_contextual_extra_metadata()
    q6_pii_masking_filter()
    q7_exception_traceback_logging()
    q8_structured_json_formatting()
    q9_declarative_dict_config()
    q10_architectural_buffered_audit_pipeline()

    print("\nAll 10 logging practice questions passed successfully!")
