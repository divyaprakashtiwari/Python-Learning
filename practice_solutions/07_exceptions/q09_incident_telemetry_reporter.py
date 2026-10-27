"""
Topic 07 - Exception Handling: Question 9
Problem: Enterprise Incident Telemetry Reporter using Python logging and traceback introspection.
"""

import datetime
import io
import logging
import os
import sys
import traceback
import uuid
from typing import Any, Dict


class IncidentTelemetryReporter:
    """Captures active exception telemetry, formats stack traces, and produces structured incident envelopes."""

    def __init__(self):
        self.log_stream = io.StringIO()
        self.logger = logging.getLogger("TelemetryLogger")
        self.logger.setLevel(logging.DEBUG)

        # Clear existing handlers
        self.logger.handlers.clear()

        handler = logging.StreamHandler(self.log_stream)
        handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
        self.logger.addHandler(handler)

    def record_incident(self, context: str, severity: str = "ERROR") -> Dict[str, Any]:
        """Extracts active crash frame metadata and formats incident diagnostic envelope."""
        exc_type, exc_val, exc_tb = sys.exc_info()
        if exc_type is None or exc_tb is None:
            raise RuntimeError("record_incident must be called within an active exception handler")

        full_traceback = traceback.format_exc()
        tb_frames = traceback.extract_tb(exc_tb)
        last_frame = tb_frames[-1]

        file_name = os.path.basename(last_frame.filename)
        line_number = last_frame.lineno
        function_name = last_frame.name
        code_line = (last_frame.line or "").strip()

        # Log through dedicated logger with exc_info=True
        log_msg = f"Exception in context '{context}': {exc_val}"
        if severity.upper() == "CRITICAL":
            self.logger.critical(log_msg, exc_info=True)
        else:
            self.logger.error(log_msg, exc_info=True)

        incident_id = f"INC-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

        return {
            "incident_id": incident_id,
            "timestamp": timestamp,
            "error_type": exc_type.__name__,
            "message": str(exc_val),
            "crash_location": f"{file_name}:{line_number} in {function_name}()",
            "failing_line": code_line,
            "traceback_length": len(full_traceback),
            "stack_trace_captured": True
        }

    def get_log_output(self) -> str:
        """Returns captured log buffer contents."""
        return self.log_stream.getvalue().strip()


# Verification & Execution
reporter = IncidentTelemetryReporter()


def risky_data_pipeline(data_records: list):
    for i, record in enumerate(data_records):
        # Deliberate ZeroDivisionError on 3rd item
        metric = record["score"] / record["weight"]


try:
    bad_data = [{"score": 10, "weight": 2}, {"score": 20, "weight": 4}, {"score": 30, "weight": 0}]
    risky_data_pipeline(bad_data)
except Exception:
    incident = reporter.record_incident(context="RiskDataPipeline")

print("Telemetry Logger Output:")
print(reporter.get_log_output())

print("\nStructured Incident Report:")
print(f"- Incident ID: {incident['incident_id']}")
print(f"- Error Type: {incident['error_type']}")
print(f"- Message: {incident['message']}")
print(f"- Crash Location: {incident['crash_location']}")
print(f"- Failing Line: {incident['failing_line']}")
print(f"- Stack Trace Captured: {incident['stack_trace_captured']}")
