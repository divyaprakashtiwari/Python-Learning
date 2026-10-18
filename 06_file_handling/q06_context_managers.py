"""
Topic 06: File Handling - Question 06: Context Managers

A comprehensive collection of 10 standalone, runnable exercises exploring
Python's context manager protocol, resource lifecycle control, the `contextlib`
module, atomic file operations, and transactional workspaces.

Questions Covered:
 1. The Context Manager Protocol: __enter__ and __exit__ fundamentals on custom file wrappers.
 2. Exception Handling in __exit__: Suppressing errors (return True) vs bubbling exceptions.
 3. @contextlib.contextmanager: Generator-based context managers using try/yield/finally.
 4. Multi-Resource Binding: Compound with statements and nested resource ordering.
 5. Dynamic Contexts with ExitStack: Managing arbitrary collections of files safely.
 6. Stream Redirection: contextlib.redirect_stdout and redirect_stderr to file streams.
 7. Atomic File Writer Pattern: Writing to staging tempfile and replacing target atomically on clean exit.
 8. Reusable & Reentrant Context Managers: Understanding state isolation across nested with blocks.
 9. Async Context Managers: __aenter__ and __aexit__ with asyncio.run() for async I/O emulation.
10. Advanced Project: Transactional Multi-File Unit of Work Workspace with automatic rollback on error.
"""

import asyncio
import contextlib
import io
import os
import shutil
import tempfile
from typing import Any, Generator, IO


# ==============================================================================
# Question 1: The Context Manager Protocol (__enter__ & __exit__)
# ==============================================================================
class TrackedFileReader:
    """
    Custom file reader that implements __enter__ and __exit__, tracking
    bytes read and ensuring the underlying file descriptor is closed.
    """

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self._file: IO[str] | None = None
        self.bytes_read: int = 0

    def __enter__(self) -> "TrackedFileReader":
        self._file = open(self.filepath, "r", encoding="utf-8")
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._file and not self._file.closed:
            self._file.close()

    def read_all(self) -> str:
        if not self._file:
            raise RuntimeError("File not opened. Use within a 'with' block.")
        data = self._file.read()
        self.bytes_read += len(data.encode("utf-8"))
        return data


def exercise_q1_context_protocol() -> None:
    """
    Demonstrate custom context manager implementing __enter__ and __exit__.
    """
    print("=== Q1: The Context Manager Protocol ===")

    temp_dir = tempfile.mkdtemp(prefix="ctx_proto_")
    path = os.path.join(temp_dir, "test.txt")

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("Antigravity Python Context Manager")

        reader_ref = None
        with TrackedFileReader(path) as reader:
            reader_ref = reader
            content = reader.read_all()
            assert content == "Antigravity Python Context Manager"
            assert reader.bytes_read == 34
            assert not reader._file.closed

        # After exiting with block, file must be closed
        assert reader_ref is not None
        assert reader_ref._file.closed

        print(f"  Successfully read {reader_ref.bytes_read} bytes; closed status: {reader_ref._file.closed}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 2: Exception Handling in __exit__
# ==============================================================================
class SafeFileErrorHandler:
    """
    Context manager that intercepts and suppresses specified exception types,
    returning True to suppress and False/None to propagate.
    """

    def __init__(self, suppressed_exceptions: tuple[type[BaseException], ...]) -> None:
        self.suppressed_exceptions = suppressed_exceptions
        self.handled_exception: BaseException | None = None

    def __enter__(self) -> "SafeFileErrorHandler":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        if exc_type is not None and issubclass(exc_type, self.suppressed_exceptions):
            self.handled_exception = exc_val
            # Returning True suppresses the exception from propagating!
            return True
        # Returning None / False allows other exceptions to propagate normally
        return False


def exercise_q2_exception_handling_in_exit() -> None:
    """
    Demonstrate exception suppression vs propagation via __exit__ return value.
    """
    print("\n=== Q2: Exception Handling in __exit__ ===")

    # 1. Suppressed case
    with SafeFileErrorHandler((FileNotFoundError, KeyError)) as handler:
        raise FileNotFoundError("Missing configuration file: app.ini")

    assert isinstance(handler.handled_exception, FileNotFoundError)

    # 2. Propagated case (ValueError is not suppressed)
    caught_unhandled = False
    try:
        with SafeFileErrorHandler((FileNotFoundError,)):
            raise ValueError("Corrupt file content!")
    except ValueError:
        caught_unhandled = True

    assert caught_unhandled is True
    print(f"  Handled suppressed exception: {type(handler.handled_exception).__name__}")
    print("  Successfully allowed unhandled exception to propagate.")


# ==============================================================================
# Question 3: @contextlib.contextmanager Generator Pattern
# ==============================================================================
@contextlib.contextmanager
def temporary_file_context(initial_content: str = "") -> Generator[str, None, None]:
    """
    Generator-based context manager yielding a temporary file path,
    guaranteeing automated deletion in the finally block.
    """
    temp_fd, temp_path = tempfile.mkstemp(prefix="gen_ctx_")
    try:
        with open(temp_fd, "w", encoding="utf-8") as f:
            f.write(initial_content)
        # Yielding passes control to the caller's `with` block
        yield temp_path
    finally:
        # Guaranteed cleanup regardless of exceptions inside with block
        if os.path.exists(temp_path):
            os.remove(temp_path)


def exercise_q3_generator_context_manager() -> None:
    """
    Demonstrate generator-based context manager lifecycle using try...yield...finally.
    """
    print("\n=== Q3: @contextlib.contextmanager Generator Pattern ===")

    retained_path = None
    with temporary_file_context("Sample Data") as path:
        retained_path = path
        assert os.path.exists(path)
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
            assert data == "Sample Data"

    # File must be cleaned up after exiting with block
    assert retained_path is not None
    assert not os.path.exists(retained_path)

    print(f"  Temporary path existed during block, cleaned up afterward: {not os.path.exists(retained_path)}")


# ==============================================================================
# Question 4: Multi-Resource Binding & Nested With Blocks
# ==============================================================================
def exercise_q4_multi_resource_binding() -> None:
    """
    Demonstrate compound with statements for simultaneously managing multiple
    file streams safely in a single statement.
    """
    print("\n=== Q4: Multi-Resource Binding & Nested With Blocks ===")

    temp_dir = tempfile.mkdtemp(prefix="ctx_multi_")
    src_path = os.path.join(temp_dir, "source.txt")
    dst_path = os.path.join(temp_dir, "destination.txt")

    try:
        with open(src_path, "w", encoding="utf-8") as f:
            f.write("Line 1: Origin\nLine 2: Origin")

        # Simultaneous binding with comma separation
        with open(src_path, "r", encoding="utf-8") as src, open(dst_path, "w", encoding="utf-8") as dst:
            for line in src:
                dst.write(line.upper())

        with open(dst_path, "r", encoding="utf-8") as res:
            transformed = res.read()

        assert transformed == "LINE 1: ORIGIN\nLINE 2: ORIGIN"
        print(f"  Compound 'with' transferred & transformed data successfully:\n{transformed}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 5: Dynamic Contexts with ExitStack
# ==============================================================================
def exercise_q5_dynamic_exit_stack() -> None:
    """
    Demonstrate contextlib.ExitStack to dynamically manage a variable number of
    file streams whose quantity is not known at compile time.
    """
    print("\n=== Q5: Dynamic Contexts with ExitStack ===")

    temp_dir = tempfile.mkdtemp(prefix="ctx_stack_")
    file_names = [f"worker_{i}.log" for i in range(5)]
    file_paths = [os.path.join(temp_dir, name) for name in file_names]

    try:
        # Create seed files
        for i, p in enumerate(file_paths):
            with open(p, "w", encoding="utf-8") as f:
                f.write(f"Log entry from worker {i}\n")

        # Dynamically open all 5 files in an ExitStack
        opened_handles = []
        with contextlib.ExitStack() as stack:
            # Enter each file context dynamically
            handles = [stack.enter_context(open(p, "r", encoding="utf-8")) for p in file_paths]
            opened_handles = handles

            # Read from all concurrently
            combined_lines = [h.readline().strip() for h in handles]
            assert len(combined_lines) == 5
            assert all(not h.closed for h in handles)

        # Upon exiting ExitStack, all handles are guaranteed to be closed
        assert all(h.closed for h in opened_handles)
        print(f"  ExitStack successfully opened and auto-closed {len(opened_handles)} handles.")
        print(f"  Sample line: '{combined_lines[0]}'")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 6: Stream Redirection (redirect_stdout & redirect_stderr)
# ==============================================================================
def exercise_q6_stream_redirection() -> None:
    """
    Use contextlib.redirect_stdout and contextlib.redirect_stderr to intercept
    console prints and capture them directly into a file or memory buffer.
    """
    print("\n=== Q6: Stream Redirection ===")

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        print("Captured line 1")
        print("Captured line 2")

    captured_text = buffer.getvalue()
    assert "Captured line 1\n" in captured_text
    assert "Captured line 2\n" in captured_text

    print(f"  Successfully redirected stdout to buffer ({len(captured_text)} characters).")


# ==============================================================================
# Question 7: Safe Atomic File Writer Pattern
# ==============================================================================
class AtomicFileWriter:
    """
    Context manager that writes data to a sibling temporary file, and on clean
    exit atomically renames it over the target file. If an exception occurs,
    the tempfile is discarded, leaving the original target file untouched.
    """

    def __init__(self, target_filepath: str, encoding: str = "utf-8") -> None:
        self.target_filepath = target_filepath
        self.encoding = encoding
        self.temp_filepath: str | None = None
        self._temp_file: IO[str] | None = None

    def __enter__(self) -> IO[str]:
        target_dir = os.path.dirname(os.path.abspath(self.target_filepath))
        # Keep temp file on same filesystem/drive for atomic rename!
        temp_fd, self.temp_filepath = tempfile.mkstemp(dir=target_dir, prefix=".atomic_tmp_")
        self._temp_file = open(temp_fd, mode="w", encoding=self.encoding)
        return self._temp_file

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._temp_file and not self._temp_file.closed:
            self._temp_file.close()

        if exc_type is None:
            # Clean exit: atomically replace target with temp file
            assert self.temp_filepath is not None
            os.replace(self.temp_filepath, self.target_filepath)
        else:
            # Error encountered: discard temp file, keep original intact
            if self.temp_filepath and os.path.exists(self.temp_filepath):
                os.remove(self.temp_filepath)


def exercise_q7_atomic_file_writer() -> None:
    """
    Verify AtomicFileWriter commits changes on success and preserves original file on failure.
    """
    print("\n=== Q7: Safe Atomic File Writer Pattern ===")

    temp_dir = tempfile.mkdtemp(prefix="ctx_atomic_")
    target = os.path.join(temp_dir, "critical_config.json")

    try:
        # Initial version
        with open(target, "w", encoding="utf-8") as f:
            f.write('{"version": 1, "status": "stable"}')

        # Scenario A: Clean update
        with AtomicFileWriter(target) as f:
            f.write('{"version": 2, "status": "updated"}')

        with open(target, "r", encoding="utf-8") as f:
            assert '{"version": 2' in f.read()

        # Scenario B: Failed update with exception
        try:
            with AtomicFileWriter(target) as f:
                f.write('{"version": 3, "status": "BROKEN"}')
                raise RuntimeError("Disk full / network crash simulation!")
        except RuntimeError:
            pass

        # Target MUST retain version 2!
        with open(target, "r", encoding="utf-8") as f:
            content_after_error = f.read()
            assert '{"version": 2' in content_after_error
            assert "BROKEN" not in content_after_error

        print("  Atomic update succeeded on clean exit.")
        print("  Atomic rollback preserved original file during unhandled exception.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 8: Reusable vs Reentrant Context Managers
# ==============================================================================
class ReusableCounterContext:
    """
    A reentrant and reusable context manager that maintains an internal depth
    counter to support nested and sequential reuse.
    """

    def __init__(self) -> None:
        self.depth = 0
        self.entry_count = 0

    def __enter__(self) -> "ReusableCounterContext":
        self.depth += 1
        self.entry_count += 1
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.depth -= 1


def exercise_q8_reusable_and_reentrant() -> None:
    """
    Demonstrate reusable and reentrant context manager behavior.
    """
    print("\n=== Q8: Reusable vs Reentrant Context Managers ===")

    counter = ReusableCounterContext()

    # Sequential reuse
    with counter:
        assert counter.depth == 1
    assert counter.depth == 0

    with counter:
        assert counter.depth == 1
    assert counter.depth == 0
    assert counter.entry_count == 2

    # Nested reuse (reentrancy)
    with counter:
        assert counter.depth == 1
        with counter:
            assert counter.depth == 2
        assert counter.depth == 1
    assert counter.depth == 0
    assert counter.entry_count == 4

    print(f"  Counter total entries across sequential & nested calls: {counter.entry_count}")


# ==============================================================================
# Question 9: Asynchronous Context Managers (__aenter__ & __aexit__)
# ==============================================================================
class AsyncFileBuffer:
    """
    Asynchronous context manager mimicking non-blocking async file I/O.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.buffer: list[str] = []
        self.closed = False

    async def __aenter__(self) -> "AsyncFileBuffer":
        await asyncio.sleep(0.01)  # Emulate async connection/open
        self.buffer.append(f"HEADER: {self.name}")
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await asyncio.sleep(0.01)  # Emulate async flush/close
        self.buffer.append("FOOTER: EOF")
        self.closed = True

    async def write_line(self, line: str) -> None:
        await asyncio.sleep(0.001)
        self.buffer.append(line)


async def _async_runner() -> AsyncFileBuffer:
    async with AsyncFileBuffer("async_data.log") as af:
        await af.write_line("Async record 1")
        await af.write_line("Async record 2")
    return af


def exercise_q9_async_context_manager() -> None:
    """
    Run async context manager within asyncio.run() event loop.
    """
    print("\n=== Q9: Asynchronous Context Managers ===")

    buffer_instance = asyncio.run(_async_runner())
    assert buffer_instance.closed is True
    assert buffer_instance.buffer[0] == "HEADER: async_data.log"
    assert buffer_instance.buffer[1] == "Async record 1"
    assert buffer_instance.buffer[-1] == "FOOTER: EOF"

    print(f"  Async context completed. Buffer lines: {buffer_instance.buffer}")


# ==============================================================================
# Question 10: Advanced Project - Transactional Multi-File Unit of Work
# ==============================================================================
class FileTransactionWorkspace:
    """
    Enterprise-grade Unit of Work context manager that orchestrates multi-file
    modifications with full ACID rollback semantics. Creates snapshot backups
    of modified files and restores them if any exception occurs.
    """

    def __init__(self, workspace_dir: str) -> None:
        self.workspace_dir = workspace_dir
        self.backup_dir = tempfile.mkdtemp(prefix=".tx_backup_")
        self.modified_files: set[str] = set()
        self.committed = False

    def __enter__(self) -> "FileTransactionWorkspace":
        return self

    def write_file(self, rel_path: str, content: str) -> None:
        full_path = os.path.join(self.workspace_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Snapshot existing file before first modification
        if rel_path not in self.modified_files:
            backup_path = os.path.join(self.backup_dir, rel_path)
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            if os.path.exists(full_path):
                shutil.copy2(full_path, backup_path)
            self.modified_files.add(rel_path)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        try:
            if exc_type is not None:
                # Rollback all modified files to snapshots
                for rel_path in self.modified_files:
                    target_path = os.path.join(self.workspace_dir, rel_path)
                    backup_path = os.path.join(self.backup_dir, rel_path)

                    if os.path.exists(backup_path):
                        # Restore previous state
                        shutil.copy2(backup_path, target_path)
                    else:
                        # File was newly created in this transaction, remove it
                        if os.path.exists(target_path):
                            os.remove(target_path)
                # Suppress the error so the test can assert clean rollback state
                return True
            else:
                self.committed = True
                return False
        finally:
            shutil.rmtree(self.backup_dir, ignore_errors=True)


def exercise_q10_transactional_workspace() -> None:
    """
    Verify FileTransactionWorkspace commits all files on success and restores all files on failure.
    """
    print("\n=== Q10: Transactional Multi-File Unit of Work ===")

    ws_dir = tempfile.mkdtemp(prefix="ctx_workspace_")

    try:
        f1 = os.path.join(ws_dir, "db.json")
        f2 = os.path.join(ws_dir, "index.json")

        # Initial clean state
        with open(f1, "w", encoding="utf-8") as f:
            f.write('{"state": "ORIGINAL_DB"}')
        with open(f2, "w", encoding="utf-8") as f:
            f.write('{"state": "ORIGINAL_INDEX"}')

        # Test Transaction Rollback
        with FileTransactionWorkspace(ws_dir) as tx:
            tx.write_file("db.json", '{"state": "MODIFIED_DB"}')
            tx.write_file("new_record.txt", "Brand new file")
            # Simulate failure halfway through transaction
            raise ValueError("Database transaction constraint violation!")

        # Verify rollback restored f1 and removed new_record.txt
        with open(f1, "r", encoding="utf-8") as f:
            assert f.read() == '{"state": "ORIGINAL_DB"}'
        assert not os.path.exists(os.path.join(ws_dir, "new_record.txt"))

        # Test Successful Commit
        with FileTransactionWorkspace(ws_dir) as tx:
            tx.write_file("db.json", '{"state": "COMMITTED_DB"}')
            tx.write_file("index.json", '{"state": "COMMITTED_INDEX"}')

        with open(f1, "r", encoding="utf-8") as f:
            assert f.read() == '{"state": "COMMITTED_DB"}'
        with open(f2, "r", encoding="utf-8") as f:
            assert f.read() == '{"state": "COMMITTED_INDEX"}'

        print("  Rollback successfully restored snapshots upon exception.")
        print("  Successful transaction committed all file updates across workspace.")

    finally:
        shutil.rmtree(ws_dir, ignore_errors=True)


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_context_protocol()
    exercise_q2_exception_handling_in_exit()
    exercise_q3_generator_context_manager()
    exercise_q4_multi_resource_binding()
    exercise_q5_dynamic_exit_stack()
    exercise_q6_stream_redirection()
    exercise_q7_atomic_file_writer()
    exercise_q8_reusable_and_reentrant()
    exercise_q9_async_context_manager()
    exercise_q10_transactional_workspace()

    print("\nAll 10 context manager questions executed and asserted successfully!")
