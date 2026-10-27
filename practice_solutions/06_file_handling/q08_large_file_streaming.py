"""
Topic 06 - File Handling: Question 8
Problem: Memory-Bounded Streaming Engine for Large Files (stream_grep, chunked SHA-256, rolling spike detection).
"""

from collections import deque
import hashlib
import os
from typing import Any, Dict, Iterator, List, Tuple


class LargeFileStreamEngine:
    """Processes arbitrarily large files in bounded O(1) memory via lazy generators and streaming."""

    def stream_grep(
        self,
        filepath: str,
        pattern: str,
        case_sensitive: bool = False
    ) -> Iterator[Tuple[int, str]]:
        """Yields (line_number, line_text) matching the pattern without loading full file into RAM."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        target_pattern = pattern if case_sensitive else pattern.lower()

        with open(filepath, mode="r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                comparison_line = line if case_sensitive else line.lower()
                if target_pattern in comparison_line:
                    yield (line_num, line.strip())

    def compute_file_sha256(self, filepath: str, chunk_size: int = 65536) -> str:
        """Computes SHA-256 digest by streaming binary chunks in bounded memory."""
        if chunk_size <= 0:
            raise ValueError("Chunk size must be strictly positive")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        hasher = hashlib.sha256()
        with open(filepath, mode="rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hasher.update(chunk)

        return hasher.hexdigest()

    def detect_error_spikes(
        self,
        filepath: str,
        window_size: int = 10,
        spike_threshold: int = 3
    ) -> List[Dict[str, Any]]:
        """Detects error spikes in rolling window using bounded collections.deque."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        window: deque = deque(maxlen=window_size)
        alerts: List[Dict[str, Any]] = []
        last_alert_end = -1

        with open(filepath, mode="r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                is_error = "ERROR" in line
                window.append((line_num, line.strip(), is_error))

                if len(window) == window_size and (line_num - last_alert_end >= window_size):
                    error_count = sum(1 for _, _, err in window if err)
                    if error_count >= spike_threshold:
                        alerts.append({
                            "window_end_line": line_num,
                            "error_count": error_count,
                            "recent_errors": [txt for _, txt, err in window if err]
                        })
                        last_alert_end = line_num

        return alerts


# Verification & Execution
log_file = "gigantic_server.log"

simulated_lines = [
    "2026-10-24 12:00:01 INFO System booted up",
    "2026-10-24 12:00:05 INFO Network routes configured",
    "2026-10-24 12:00:10 INFO Connecting to Database cluster",
    "2026-10-24 12:00:15 INFO Worker pool initialized with 8 threads",
    "2026-10-24 12:00:18 WARNING High thread queue occupancy",
    "2026-10-24 12:00:20 INFO Heartbeat ack received",
    "2026-10-24 12:00:22 ERROR Primary gateway unreachable",
    "2026-10-24 12:00:25 ERROR Database connection pool exhausted",
    "2026-10-24 12:00:28 ERROR Read replica timed out after 5000ms",
    "2026-10-24 12:00:32 INFO Failover routing to backup host",
    "2026-10-24 12:00:35 INFO Restored database connectivity",
    "2026-10-24 12:00:40 INFO Memory usage dropped to baseline",
    "2026-10-24 12:00:45 INFO Health check status green",
    "2026-10-24 12:00:50 INFO Metrics flushed to central collector",
    "2026-10-24 12:00:55 INFO Routine execution complete"
]

try:
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("\n".join(simulated_lines) + "\n")

    engine = LargeFileStreamEngine()

    grep_matches = list(engine.stream_grep(log_file, pattern="DATABASE", case_sensitive=False))
    print(f"Pattern Matches Found: {len(grep_matches)}")
    for l_num, text in grep_matches:
        print(f"- Line {l_num}: {text}")

    file_digest = engine.compute_file_sha256(log_file, chunk_size=1024)
    print(f"\nSHA-256 Digest (1KB chunks):\n{file_digest}")

    spikes = engine.detect_error_spikes(log_file, window_size=5, spike_threshold=3)
    if spikes:
        first_alert = spikes[0]
        print("\nSpike Alert Detected:")
        print(f"- Window End Line: {first_alert['window_end_line']}")
        print(f"- Error Count in Window: {first_alert['error_count']}")
        print(f"- Trigger: Error count ({first_alert['error_count']}) >= threshold (3)")

finally:
    if os.path.exists(log_file):
        os.remove(log_file)
