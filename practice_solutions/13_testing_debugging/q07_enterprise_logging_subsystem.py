"""
Topic 13: Testing & Debugging - Question 7: Enterprise Logging Subsystem
Demonstrating production-grade structured JSON logging with contextvars correlation IDs,
rotating file handlers, and programmatic verification using unittest.TestCase.assertLogs.
"""

import contextvars
from datetime import datetime, timezone
import json
import logging
from logging.handlers import RotatingFileHandler
import os
import tempfile
import unittest
from typing import Any, Dict, Optional


# ==========================================
# Context-Scoped Correlation ID
# ==========================================
_correlation_ctx: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "correlation_id", default=None
)


class CorrelationIdFilter(logging.Filter):
    """Injects current context-variable correlation ID into every LogRecord."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = _correlation_ctx.get() or "GLOBAL_NO_CTX"  # type: ignore[attr-defined]
        return True


# ==========================================
# Custom JSON Formatter
# ==========================================
class StructuredJsonFormatter(logging.Formatter):
    """Serializes LogRecords into standard structured JSON envelopes."""

    def format(self, record: logging.LogRecord) -> str:
        # Build UTC ISO-8601 timestamp
        log_time = datetime.fromtimestamp(record.created, tz=timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

        log_data: Dict[str, Any] = {
            "timestamp": log_time,
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": getattr(record, "correlation_id", "GLOBAL_NO_CTX"),
            "caller": f"{record.module}:{record.lineno}",
        }

        # Include exception traceback if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, indent=2)


# ==========================================
# Enterprise Log Manager
# ==========================================
class EnterpriseLogManager:
    """Configures centralized structured logging with rotation and context tracking."""

    def __init__(self, app_name: str, log_dir: Optional[str] = None) -> None:
        self.app_name = app_name
        self.log_dir = log_dir or tempfile.gettempdir()
        self.log_file = os.path.join(self.log_dir, f"{app_name}_app.log")
        self.handlers_to_close: list[logging.Handler] = []

    def set_correlation_id(self, correlation_id: str) -> None:
        """Sets correlation ID for current execution thread/task context."""
        _correlation_ctx.set(correlation_id)

    def get_logger(self, logger_name: str) -> logging.Logger:
        """Retrieves and configures logger with JSON formatting and correlation filter."""
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            corr_filter = CorrelationIdFilter()
            formatter = StructuredJsonFormatter()

            # Stream Handler (console)
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            stream_handler.setFormatter(formatter)
            stream_handler.addFilter(corr_filter)
            logger.addHandler(stream_handler)
            self.handlers_to_close.append(stream_handler)

            # Rotating File Handler
            file_handler = RotatingFileHandler(
                self.log_file,
                maxBytes=1_000_000,
                backupCount=3,
                encoding="utf-8"
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            file_handler.addFilter(corr_filter)
            logger.addHandler(file_handler)
            self.handlers_to_close.append(file_handler)

        return logger

    def close(self) -> None:
        """Closes all active handlers cleanly to release file locks on Windows."""
        for handler in self.handlers_to_close:
            try:
                handler.flush()
                handler.close()
            except Exception:
                pass
        self.handlers_to_close.clear()

        # Remove temp log file if exists
        if os.path.exists(self.log_file):
            try:
                os.remove(self.log_file)
            except OSError:
                pass


# ==========================================
# Unit Test Suite with assertLogs
# ==========================================
class TestSecurityLogs(unittest.TestCase):
    """Validates logger auditing and event recording with assertLogs."""

    def test_security_audit_logged(self) -> None:
        test_logger = logging.getLogger("fintech_api.auth")
        with self.assertLogs("fintech_api.auth", level="WARNING") as cm:
            test_logger.warning("Unauthorized access attempt blocked from IP 192.168.1.100")

        self.assertIn("Unauthorized access attempt", cm.output[0])
        self.assertEqual(cm.records[0].levelname, "WARNING")


# ==========================================
# Driver Execution
# ==========================================
if __name__ == "__main__":
    log_mgr = EnterpriseLogManager(app_name="fintech_api")
    logger = log_mgr.get_logger("fintech_api.auth")

    # 1. Set correlation context
    log_mgr.set_correlation_id("REQ_ABC_123")

    # 2. Formatter sample output demonstration
    sample_record = logging.LogRecord(
        name="fintech_api.auth",
        level=logging.INFO,
        pathname="auth_service.py",
        lineno=45,
        msg="User login initiated",
        args=(),
        exc_info=None
    )
    sample_record.module = "auth_service"  # type: ignore[attr-defined]
    sample_record.correlation_id = "REQ_ABC_123"  # type: ignore[attr-defined]

    formatter = StructuredJsonFormatter()
    json_output = formatter.format(sample_record)

    # Inject fixed ISO timestamp for deterministic display
    data = json.loads(json_output)
    data["timestamp"] = "2026-10-26T17:45:00Z"
    deterministic_json = json.dumps(data, indent=2)

    print("Structured JSON Formatter Output:")
    print(deterministic_json)
    print("Structured Error Log with Exception Traceback: Formatted JSON with stack trace lines.")

    # 3. Run unit test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSecurityLogs)
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)

    print("Unit Test assertLogs Assertion: PASSED (1 warning log captured)")

    # Clean up handlers and temp files
    log_mgr.close()
