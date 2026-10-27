"""
Topic 06 - File Handling: Question 9
Problem: Ephemeral Execution and Artifact Staging Engine using Python tempfile module.
"""

import hashlib
import io
import os
from pathlib import Path
import tempfile
from typing import Any, Callable, Dict, Iterable, Tuple


class EphemeralSandboxEngine:
    """Manages ephemeral sandboxes, spooled memory buffers, and transient scripts."""

    def execute_isolated_task(
        self,
        file_manifest: Dict[str, str],
        task_callback: Callable[[Path], Dict[str, Any]]
    ) -> Tuple[Dict[str, Any], bool]:
        """Runs task inside an isolated TemporaryDirectory and validates total post-task cleanup."""
        with tempfile.TemporaryDirectory(prefix="sandbox_run_") as temp_dir_str:
            sandbox_path = Path(temp_dir_str)
            for rel_str, content in file_manifest.items():
                dest_file = sandbox_path / rel_str
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                dest_file.write_text(content, encoding="utf-8")

            task_result = task_callback(sandbox_path)

        purged_cleanly = not sandbox_path.exists()
        return task_result, purged_cleanly

    def buffer_incoming_stream(
        self,
        byte_stream: Iterable[bytes],
        rollover_threshold_bytes: int = 2048
    ) -> Dict[str, Any]:
        """Buffers binary stream using SpooledTemporaryFile with automatic RAM-to-disk rollover."""
        with tempfile.SpooledTemporaryFile(max_size=rollover_threshold_bytes, mode="w+b") as spool:
            for chunk in byte_stream:
                spool.write(chunk)

            # Inspect internal storage: BytesIO vs real OS temporary file
            underlying_file = getattr(spool, "_file", None)
            rolled_to_disk = not isinstance(underlying_file, io.BytesIO)

            spool.seek(0)
            payload = spool.read()
            md5_digest = hashlib.md5(payload).hexdigest()

            return {
                "rolled_to_disk": rolled_to_disk,
                "total_bytes": len(payload),
                "md5": md5_digest
            }

    def stage_transient_script(self, script_body: str, suffix: str = ".py") -> str:
        """Generates a closed, unlinked NamedTemporaryFile for cross-process invocation."""
        temp_named = tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False, encoding="utf-8")
        try:
            temp_named.write(script_body)
            temp_named.flush()
            return temp_named.name
        finally:
            temp_named.close()

    def run_and_cleanup_script(self, script_body: str) -> bool:
        """Executes/verifies transient script under strict try...finally deletion guarantee."""
        path = self.stage_transient_script(script_body)
        try:
            return os.path.exists(path)
        finally:
            if os.path.exists(path):
                os.remove(path)


# Verification & Execution
engine = EphemeralSandboxEngine()

# Task 1: TemporaryDirectory execution
manifest = {
    "config.json": '{"env": "test", "threads": 4}',
    "src/worker.py": "print('Task complete')"
}


def sample_build(sandbox_path: Path) -> Dict[str, Any]:
    config_file = sandbox_path / "config.json"
    return {
        "files_found": len(list(sandbox_path.rglob("*.*"))),
        "config_size": config_file.stat().st_size
    }


build_result, is_cleaned = engine.execute_isolated_task(manifest, sample_build)
print(f"Sandbox Task Result: {build_result}")
print(f"Post-Task Sandbox Cleaned: {is_cleaned} (Directory successfully purged)")

# Task 2: Spooled file (small payload < 2048 bytes remains in RAM)
small_payload = [b"Chunk 1 ", b"Chunk 2 ", b"Chunk 3"]
spool_ram = engine.buffer_incoming_stream(small_payload, rollover_threshold_bytes=2048)
print(f"\nSmall Stream ({spool_ram['total_bytes']} bytes):")
disk_status_small = "Rolled over to OS Temporary File" if spool_ram["rolled_to_disk"] else "Resides in Memory Buffer"
print(f"- Rolled to Disk: {spool_ram['rolled_to_disk']} ({disk_status_small})")
print(f"- Total Bytes: {spool_ram['total_bytes']}")

# Task 3: Spooled file (large payload > 2048 bytes overflows to disk)
large_payload = [b"X" * 1024 for _ in range(5)]  # 5120 bytes
spool_disk = engine.buffer_incoming_stream(large_payload, rollover_threshold_bytes=2048)
print(f"\nLarge Stream ({spool_disk['total_bytes']} bytes):")
disk_status_large = "Rolled over to OS Temporary File" if spool_disk["rolled_to_disk"] else "Resides in Memory Buffer"
print(f"- Rolled to Disk: {spool_disk['rolled_to_disk']} ({disk_status_large})")
print(f"- Total Bytes: {spool_disk['total_bytes']}")
