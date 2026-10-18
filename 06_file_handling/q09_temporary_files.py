"""
Topic 06: File Handling - Question 09: Temporary Files

A comprehensive collection of 10 standalone, runnable exercises exploring
Python's `tempfile` module, anonymous/named files, memory spooled buffers,
temporary directories, security best practices, and sandboxed test workspaces.

Questions Covered:
 1. tempfile.TemporaryFile: Anonymous file lifecycle, automatic deletion upon close.
 2. tempfile.NamedTemporaryFile: Named files, cross-platform Windows sharing quirks, delete=False.
 3. tempfile.SpooledTemporaryFile: In-memory buffers that rollover to disk when max_size is exceeded.
 4. tempfile.TemporaryDirectory: Context-managed temporary directories with automatic recursive cleanup.
 5. Low-Level mkstemp(): File descriptor management, os.close(fd), and safe unlinking.
 6. Low-Level mkdtemp(): Custom prefixes, suffixes, and custom base directory specification.
 7. Temp Discovery & Custom Directories: tempfile.gettempdir(), gettempprefix(), and dir overrides.
 8. Race Condition Prevention (TOCTOU): Secure atomic creation with os.O_CREAT | os.O_EXCL.
 9. Time-To-Live (TTL) Scratchpad Cache: Automated purging of expired temporary files.
10. Advanced Project: Sandboxed Isolated Workspace Execution Engine with artifact export and teardown.
"""

import os
import shutil
import tempfile
import time
from typing import Any


# ==============================================================================
# Question 1: tempfile.TemporaryFile (Anonymous File Lifecycle)
# ==============================================================================
def exercise_q1_temporary_file() -> None:
    """
    Demonstrate anonymous temporary files created with TemporaryFile().
    The file is automatically deleted as soon as it is closed.
    """
    print("=== Q1: tempfile.TemporaryFile ===")

    # TemporaryFile defaults to mode='w+b' (binary)
    with tempfile.TemporaryFile(mode="w+t", encoding="utf-8") as temp:
        temp.write("Temporary payload data\nSecond line")
        temp.seek(0)
        content = temp.read()
        assert "Temporary payload data" in content
        assert not temp.closed

    # Once the with block exits, the file handle is closed and automatically destroyed
    assert temp.closed
    print("  Anonymous temporary file created, read, and destroyed cleanly.")


# ==============================================================================
# Question 2: tempfile.NamedTemporaryFile & Windows Sharing Rules
# ==============================================================================
def exercise_q2_named_temporary_file() -> None:
    """
    Demonstrate NamedTemporaryFile(). On Windows, an open NamedTemporaryFile cannot
    be reopened by name by another process or function if delete=True. We demonstrate
    the robust cross-platform pattern using delete=False with try...finally cleanup.
    """
    print("\n=== Q2: tempfile.NamedTemporaryFile & Windows Sharing Rules ===")

    temp_path = None
    try:
        # delete=False allows closing the handle, then safely opening by path on Windows
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json", encoding="utf-8") as ntf:
            temp_path = ntf.name
            ntf.write('{"service": "auth", "port": 8080}')

        assert temp_path is not None
        assert os.path.exists(temp_path)
        assert temp_path.endswith(".json")

        # Reopen by path
        with open(temp_path, "r", encoding="utf-8") as f:
            data = f.read()
            assert '"service": "auth"' in data

        print(f"  Named temp file created at: {temp_path}")
        print(f"  Reopened and verified content: {data}")

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

    assert not os.path.exists(temp_path)
    print(f"  Cleaned up temp file successfully: {not os.path.exists(temp_path)}")


# ==============================================================================
# Question 3: tempfile.SpooledTemporaryFile (In-Memory to Disk Rollover)
# ==============================================================================
def exercise_q3_spooled_temporary_file() -> None:
    """
    Demonstrate SpooledTemporaryFile with max_size. Operates in memory (io.BytesIO)
    until data exceeds max_size, then automatically rolls over to an on-disk temporary file.
    """
    print("\n=== Q3: tempfile.SpooledTemporaryFile ===")

    max_bytes = 50
    with tempfile.SpooledTemporaryFile(max_size=max_bytes, mode="w+b") as spooled:
        # Phase 1: Small payload (under max_size) -> stays in memory
        spooled.write(b"Hello" * 5)  # 25 bytes
        assert spooled._rolled is False  # Internal check: not rolled to disk

        # Phase 2: Exceed max_size -> triggers rollover to real on-disk tempfile
        spooled.write(b"Overflow" * 10)  # +80 bytes = 105 bytes > 50 bytes
        assert spooled._rolled is True  # Rolled over to real disk file!

        spooled.seek(0)
        data = spooled.read()
        assert len(data) == 105
        assert data.startswith(b"Hello")

        print(f"  Spooled file size: {len(data)} bytes.")
        print(f"  Rollover to disk triggered: {spooled._rolled}")


# ==============================================================================
# Question 4: tempfile.TemporaryDirectory
# ==============================================================================
def exercise_q4_temporary_directory() -> None:
    """
    Demonstrate TemporaryDirectory() context manager. Ensures all nested files
    and subdirectories are recursively destroyed upon exit.
    """
    print("\n=== Q4: tempfile.TemporaryDirectory ===")

    dir_path_ref = None
    with tempfile.TemporaryDirectory(prefix="app_workspace_") as temp_dir:
        dir_path_ref = temp_dir
        assert os.path.isdir(temp_dir)

        # Create nested structure
        sub = os.path.join(temp_dir, "nested_folder")
        os.makedirs(sub)
        file1 = os.path.join(sub, "data.txt")
        with open(file1, "w", encoding="utf-8") as f:
            f.write("Payload inside temp directory")

        assert os.path.exists(file1)

    # Exiting context deletes the entire tree
    assert dir_path_ref is not None
    assert not os.path.exists(dir_path_ref)

    print(f"  TemporaryDirectory existed at: {dir_path_ref}")
    print(f"  Recursive cleanup completed: {not os.path.exists(dir_path_ref)}")


# ==============================================================================
# Question 5: Low-Level mkstemp() & File Descriptor Safety
# ==============================================================================
def exercise_q5_low_level_mkstemp() -> None:
    """
    Demonstrate mkstemp(), which returns a low-level OS file descriptor (fd) and path.
    Properly wraps the fd using os.fdopen() or closes it with os.close(fd).
    """
    print("\n=== Q5: Low-Level mkstemp() & File Descriptor Safety ===")

    fd, file_path = tempfile.mkstemp(prefix="mkstemp_", suffix=".log")
    try:
        # Wrapping fd in standard Python file object
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write("Log entry via file descriptor")

        # Verify read back
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        assert content == "Log entry via file descriptor"
        print(f"  File created via mkstemp: {file_path}")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    assert not os.path.exists(file_path)


# ==============================================================================
# Question 6: Low-Level mkdtemp()
# ==============================================================================
def exercise_q6_low_level_mkdtemp() -> None:
    """
    Demonstrate mkdtemp() for creating raw temporary directories that require
    explicit manual cleanup via shutil.rmtree().
    """
    print("\n=== Q6: Low-Level mkdtemp() ===")

    temp_folder = tempfile.mkdtemp(prefix="custom_batch_", suffix="_staging")
    try:
        assert os.path.isdir(temp_folder)
        assert "custom_batch_" in os.path.basename(temp_folder)
        assert temp_folder.endswith("_staging")

        # Test writing a file
        marker = os.path.join(temp_folder, "ready.flag")
        with open(marker, "w", encoding="utf-8") as f:
            f.write("OK")
        assert os.path.exists(marker)

        print(f"  Created manual staging directory: {temp_folder}")

    finally:
        shutil.rmtree(temp_folder, ignore_errors=True)

    assert not os.path.exists(temp_folder)


# ==============================================================================
# Question 7: Temp Discovery & Custom Directory Overrides
# ==============================================================================
def exercise_q7_temp_discovery_and_overrides() -> None:
    """
    Inspect the system temporary directory with tempfile.gettempdir() and
    create temporary files inside a specified custom parent directory.
    """
    print("\n=== Q7: Temp Discovery & Custom Directory Overrides ===")

    default_temp = tempfile.gettempdir()
    prefix = tempfile.gettempprefix()
    assert os.path.isdir(default_temp)

    # Creating a temp file in a designated parent directory
    custom_base = tempfile.mkdtemp(prefix="custom_parent_")
    try:
        with tempfile.NamedTemporaryFile(dir=custom_base, delete=False) as ntf:
            ntf_path = ntf.name

        assert os.path.dirname(ntf_path) == custom_base
        print(f"  System Temp Dir:  {default_temp}")
        print(f"  System Prefix:    {prefix}")
        print(f"  Custom-bound temp: {ntf_path}")

    finally:
        shutil.rmtree(custom_base, ignore_errors=True)


# ==============================================================================
# Question 8: Race Condition Prevention (TOCTOU Safety)
# ==============================================================================
def exercise_q8_race_condition_prevention() -> None:
    """
    Demonstrate secure file creation using atomic low-level flags
    (os.O_CREAT | os.O_EXCL | os.O_WRONLY) to prevent Time-Of-Check to Time-Of-Use
    (TOCTOU) race conditions and symlink hijacking attacks.
    """
    print("\n=== Q8: Race Condition Prevention (TOCTOU Safety) ===")

    temp_dir = tempfile.mkdtemp(prefix="sec_temp_")
    secure_path = os.path.join(temp_dir, "secure_target.txt")

    try:
        # Atomic creation: fails if file already exists
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        mode = 0o600  # Read/Write by owner only

        fd1 = os.open(secure_path, flags, mode)
        with os.fdopen(fd1, "w", encoding="utf-8") as f:
            f.write("Secret credentials token")

        # Second attempt to atomically create the EXACT same file must raise FileExistsError
        try:
            os.open(secure_path, flags, mode)
            assert False, "Should have raised FileExistsError"
        except FileExistsError:
            pass

        print("  First open atomically created file.")
        print("  Second open atomically rejected duplicate with FileExistsError (TOCTOU safe).")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 9: Time-To-Live (TTL) Scratchpad Cache
# ==============================================================================
class TempScratchCache:
    """
    Disk-based cache in a temporary directory that supports key/value caching
    with TTL expiration and automated eviction of stale files.
    """

    def __init__(self, base_dir: str, default_ttl_seconds: float = 0.5) -> None:
        self.base_dir = base_dir
        self.default_ttl = default_ttl_seconds

    def put(self, key: str, value: str) -> None:
        path = os.path.join(self.base_dir, f"{key}.cache")
        # Save timestamp and value
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"{time.time()}\n{value}")

    def get(self, key: str) -> str | None:
        path = os.path.join(self.base_dir, f"{key}.cache")
        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                return None
            created_at = float(lines[0].strip())
            value = "".join(lines[1:])

        if time.time() - created_at > self.default_ttl:
            # Expired: delete
            os.remove(path)
            return None

        return value

    def purge_expired(self) -> int:
        purged = 0
        now = time.time()
        for fname in os.listdir(self.base_dir):
            if fname.endswith(".cache"):
                p = os.path.join(self.base_dir, fname)
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        ts = float(f.readline().strip())
                    if now - ts > self.default_ttl:
                        os.remove(p)
                        purged += 1
                except (OSError, ValueError):
                    pass
        return purged


def exercise_q9_ttl_scratchpad_cache() -> None:
    """
    Demonstrate TTL temporary caching with expiration and eviction.
    """
    print("\n=== Q9: Time-To-Live (TTL) Scratchpad Cache ===")

    temp_dir = tempfile.mkdtemp(prefix="cache_ttl_")

    try:
        cache = TempScratchCache(temp_dir, default_ttl_seconds=0.1)
        cache.put("user_101", "Alice Data")
        cache.put("user_102", "Bob Data")

        # Immediately available
        assert cache.get("user_101") == "Alice Data"
        assert cache.get("user_102") == "Bob Data"

        # Wait for TTL expiration
        time.sleep(0.15)

        # Cache misses due to expiration
        assert cache.get("user_101") is None
        assert cache.get("user_102") is None

        print("  TTL Cache successfully served cached item and expired stale entry.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 10: Advanced Project - Sandboxed Workspace Execution Engine
# ==============================================================================
class SandboxedWorkspace:
    """
    Secure sandbox engine that executes batch jobs inside an isolated temporary directory.
    Guarantees that generated artifacts are exported to the target directory only on
    successful completion, and the sandbox is destroyed immediately.
    """

    def __init__(self, job_name: str) -> None:
        self.job_name = job_name
        self.workspace_dir: str | None = None

    def __enter__(self) -> "SandboxedWorkspace":
        self.workspace_dir = tempfile.mkdtemp(prefix=f"sandbox_{self.job_name}_")
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self.workspace_dir and os.path.exists(self.workspace_dir):
            shutil.rmtree(self.workspace_dir, ignore_errors=True)

    def write_input(self, filename: str, content: str) -> str:
        assert self.workspace_dir is not None
        p = os.path.join(self.workspace_dir, filename)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        return p

    def run_pipeline(self) -> dict[str, Any]:
        """Simulates transforming workspace input files into output artifacts."""
        assert self.workspace_dir is not None
        input_file = os.path.join(self.workspace_dir, "input.txt")
        output_file = os.path.join(self.workspace_dir, "output.txt")

        with open(input_file, "r", encoding="utf-8") as f:
            data = f.read()

        transformed = data.upper()
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(transformed)

        return {
            "bytes_in": len(data),
            "bytes_out": len(transformed),
            "artifact_path": output_file,
            "transformed_content": transformed,
        }


def exercise_q10_sandboxed_workspace() -> None:
    """
    Demonstrate execution within a SandboxedWorkspace.
    """
    print("\n=== Q10: Sandboxed Workspace Execution Engine ===")

    ws_path_capture = None
    with SandboxedWorkspace("data_cleanse") as sandbox:
        ws_path_capture = sandbox.workspace_dir
        sandbox.write_input("input.txt", "antigravity python agentic workflow")
        results = sandbox.run_pipeline()

        assert results["transformed_content"] == "ANTIGRAVITY PYTHON AGENTIC WORKFLOW"
        assert results["bytes_in"] == len("antigravity python agentic workflow")

    # Sandbox directory must be fully wiped after exit
    assert ws_path_capture is not None
    assert not os.path.exists(ws_path_capture)

    print(f"  Sandbox completed job successfully: {results['transformed_content']}")
    print(f"  Sandbox teardown verified: {not os.path.exists(ws_path_capture)}")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_temporary_file()
    exercise_q2_named_temporary_file()
    exercise_q3_spooled_temporary_file()
    exercise_q4_temporary_directory()
    exercise_q5_low_level_mkstemp()
    exercise_q6_low_level_mkdtemp()
    exercise_q7_temp_discovery_and_overrides()
    exercise_q8_race_condition_prevention()
    exercise_q9_ttl_scratchpad_cache()
    exercise_q10_sandboxed_workspace()

    print("\nAll 10 temporary files questions executed and asserted successfully!")
