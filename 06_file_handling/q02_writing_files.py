"""
Topic 06: File Handling
Question 02: Writing Files (Deep Dive)

Master file writing mechanisms, stream buffering, and atomic operations:
- Basic file writing with write() and tracking character counts
- Writing collections with writelines() and newline handling
- Exclusive file creation with 'x' mode to prevent accidental overwrites
- Redirecting print() output directly to file streams
- Buffer management: flush() vs os.fsync() durability guarantees
- Atomic file writing pattern using temporary sibling files and os.replace()
- Encodings during write (UTF-8 guarantees across OS platforms)
- Structured serialization with json.dump() vs json.dumps()
- In-memory stream writing with io.StringIO
- Production-grade Rotating Audit Log Writer with buffered flushing
"""

import io
import json
import os
import tempfile
from typing import Any, Dict, List, Optional


# ============================================================
# Q1: Basic Writing with write() & Return Values
# ============================================================
# Question: Demonstrate writing text to a file using `"w"` mode.
# Verify that `.write()` returns the exact number of characters written,
# and explain how `"w"` mode truncates existing files.

print("=== Q1: Basic write() & Character Return Counts ===")

with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
    tmp_path = tmp.name

try:
    with open(tmp_path, "w", encoding="utf-8") as f:
        chars_written_1 = f.write("Hello, World!\n")
        chars_written_2 = f.write("Second Line of Content.")

    print(f"  Chars written in write 1: {chars_written_1}")
    print(f"  Chars written in write 2: {chars_written_2}")

    assert chars_written_1 == len("Hello, World!\n")
    assert chars_written_2 == len("Second Line of Content.")

    # Reopening with "w" truncates the file back to 0 bytes!
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write("Truncated!")

    with open(tmp_path, "r", encoding="utf-8") as f:
        new_content = f.read()

    print(f"  Content after 'w' truncate: '{new_content}'")
    assert new_content == "Truncated!"
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: `file.write(str)` returns the number of characters written.
# Opening a file in `"w"` mode immediately truncates its size to 0 bytes if it already exists.


# ============================================================
# Q2: writelines() & The Missing Newline Pitfall
# ============================================================
# Question: Demonstrate `writelines()` with a sequence of strings.
# Explain the critical pitfall: `writelines()` does NOT append newlines automatically!
# Show how to append `\n` cleanly using generator expressions.

print("\n=== Q2: writelines() & Newline Handling ===")

lines_to_write = ["Server initialized", "Port 8080 active", "SSL enabled"]

with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
    tmp_path = tmp.name

try:
    # 1. THE PITFALL: writelines() without \n concatenates into one single line!
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.writelines(lines_to_write)

    with open(tmp_path, "r", encoding="utf-8") as f:
        jammed_content = f.read()
    print(f"  Jammed content without newlines:\n    '{jammed_content}'")
    assert jammed_content == "Server initializedPort 8080 activeSSL enabled"

    # 2. THE PROPER PATTERN: append \n via generator expression
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.writelines(f"{line}\n" for line in lines_to_write)

    with open(tmp_path, "r", encoding="utf-8") as f:
        formatted_lines = f.readlines()

    print(f"  Properly formatted lines count: {len(formatted_lines)}")
    assert len(formatted_lines) == 3
    assert formatted_lines[0] == "Server initialized\n"
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: Despite its name, `writelines()` simply writes an iterable of strings
# without adding separators or newlines.


# ============================================================
# Q3: Exclusive Creation Mode ('x')
# ============================================================
# Question: Demonstrate exclusive creation mode `"x"`. Show that it succeeds if the file
# does not exist, but raises `FileExistsError` if the file already exists.

print("\n=== Q3: Exclusive Creation Mode ('x') ===")

temp_dir = tempfile.gettempdir()
unique_target = os.path.join(temp_dir, f"exclusive_test_{os.getpid()}.txt")

try:
    # 1. First creation succeeds
    with open(unique_target, "x", encoding="utf-8") as f:
        f.write("Initial exclusive write")
    print(f"  Successfully created file exclusively: {unique_target}")
    assert os.path.exists(unique_target)

    # 2. Second creation fails with FileExistsError
    caught_exists_error = False
    try:
        with open(unique_target, "x", encoding="utf-8") as f:
            f.write("Attempting overwrite")
    except FileExistsError as err:
        caught_exists_error = True
        print(f"  Caught expected FileExistsError: {err}")

    assert caught_exists_error
finally:
    if os.path.exists(unique_target):
        os.remove(unique_target)

# Explanation: Mode `"x"` (exclusive creation) provides atomic file creation semantics,
# useful for lockfiles, PID files, or preventing accidental data destruction.


# ============================================================
# Q4: Redirecting print() to File Streams
# ============================================================
# Question: Use `print(..., file=f)` to write formatted text, utilizing custom
# separators (`sep=','`) and termination markers (`end='\n---\n'`).

print("\n=== Q4: print(file=f) Stream Redirection ===")

with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
    tmp_path = tmp.name

try:
    with open(tmp_path, "w", encoding="utf-8") as f:
        # Formatted CSV record
        print("2026-10-18", "USER_LOGIN", "alice", 200, sep=",", file=f)
        # Custom section divider
        print("REPORT_END", end="\n===\n", file=f)

    with open(tmp_path, "r", encoding="utf-8") as f:
        output_text = f.read()

    print(f"  File output from print():\n{output_text}")
    assert "2026-10-18,USER_LOGIN,alice,200\n" in output_text
    assert output_text.endswith("REPORT_END\n===\n")
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: `print()` accepts a `file` keyword argument. It automatically casts
# non-string objects to strings via `str()` and handles custom separators cleanly.


# ============================================================
# Q5: Buffering, flush(), and os.fsync() Durability
# ============================================================
# Question: Contrast Python's user-space buffer (`flush()`) with the OS kernel buffer
# (`os.fsync()`). Demonstrate that data is not guaranteed on physical disk without `fsync`.

print("\n=== Q5: Buffering, flush(), and os.fsync() ===")

with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
    tmp_path = tmp.name

try:
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write("Critical transactional log entry")
        
        # 1. f.flush() pushes data from Python's internal memory buffer to OS kernel buffer
        f.flush()
        
        # 2. os.fsync() forces OS kernel buffer to flush directly to physical disk controller
        os.fsync(f.fileno())

    print("  Flushed and synced critical transaction to physical storage.")
    assert os.path.getsize(tmp_path) > 0
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation:
# - Python writes to a userspace buffer.
# - `f.flush()` sends userspace bytes to the OS kernel page cache.
# - `os.fsync(f.fileno())` forces the OS kernel to commit page cache bytes to physical media.


# ============================================================
# Q6: Atomic File Writing Pattern (Write-Temp-and-Rename)
# ============================================================
# Question: Implement the production-standard Atomic File Writer:
# write to a temporary sibling file in the same directory, flush/sync,
# and atomically swap via `os.replace()`.

print("\n=== Q6: Atomic File Writing Pattern ===")

def atomic_write(filepath: str, content: str, encoding: str = "utf-8") -> None:
    """
    Atomically writes content to filepath by writing to a temporary file in the
    same directory and executing an atomic filesystem rename (os.replace).
    """
    directory = os.path.dirname(os.path.abspath(filepath))
    # Create temp file in the SAME filesystem directory to guarantee atomic rename
    with tempfile.NamedTemporaryFile("w", dir=directory, delete=False, encoding=encoding) as tmp:
        temp_path = tmp.name
        tmp.write(content)
        tmp.flush()
        os.fsync(tmp.fileno())

    # os.replace() is atomic on both POSIX and modern Windows NTFS
    os.replace(temp_path, filepath)

target_file = os.path.join(tempfile.gettempdir(), f"atomic_config_{os.getpid()}.json")

try:
    # Initial atomic write
    atomic_write(target_file, '{"state": "INITIAL"}')
    with open(target_file, "r") as f: assert "INITIAL" in f.read()

    # Second atomic update
    atomic_write(target_file, '{"state": "UPDATED"}')
    with open(target_file, "r") as f: assert "UPDATED" in f.read()

    print(f"  Atomic write successfully updated target: {target_file}")
finally:
    if os.path.exists(target_file):
        os.remove(target_file)

# Explanation: If power fails or a crash occurs mid-write, direct `open(file, "w")`
# leaves the file half-empty or corrupted. Atomic write ensures either the complete
# old file exists or the complete new file exists, never a corrupt intermediate state.


# ============================================================
# Q7: Multi-Language UTF-8 Encoding Guarantees
# ============================================================
# Question: Write a multi-language string containing Asian characters, European accented
# letters, and mathematical symbols using `encoding='utf-8'`.

print("\n=== Q7: Multi-Language UTF-8 Writing ===")

multilingual_payload = "English | Français | Español | 日本語 | العربية | Math: ∑(x) ≥ 0"

with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
    tmp_path = tmp.name

try:
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(multilingual_payload)

    with open(tmp_path, "r", encoding="utf-8") as f:
        read_back = f.read()

    print("  Successfully wrote and read back multi-language UTF-8 payload.")
    assert read_back == multilingual_payload
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: Omitting `encoding` causes Python to use the operating system's default
# encoding (e.g. CP1252 on Western Windows), which crashes when writing multilingual characters.


# ============================================================
# Q8: Structured Data Serialization (json.dump vs json.dumps)
# ============================================================
# Question: Contrast `json.dump(obj, file)` with `json.dumps(obj)`.
# Show that `json.dump()` streams directly into the file object without allocating
# a large intermediate JSON string in memory.

print("\n=== Q8: json.dump() Streaming Serialization ===")

payload_data = {
    "app_name": "DataIngestor",
    "version": "3.1.0",
    "settings": {
        "max_threads": 8,
        "allowed_hosts": ["localhost", "10.0.0.1"],
        "rate_limiting": True
    }
}

with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
    tmp_path = tmp.name

try:
    # json.dump streams directly to file object without intermediate string allocation
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(payload_data, f, indent=2, sort_keys=True)

    with open(tmp_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    print(f"  Deserialized JSON matches original: {loaded == payload_data}")
    assert loaded["app_name"] == "DataIngestor"
    assert loaded["settings"]["max_threads"] == 8
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: Use `json.dump(obj, f)` for files. It writes chunks directly to disk
# without constructing the entire monolithic JSON string in RAM first.


# ============================================================
# Q9: In-Memory File Writing with io.StringIO
# ============================================================
# Question: Use `io.StringIO` to simulate writing to a file stream purely in memory.
# Demonstrate that code expecting a file object works identically with `StringIO`.

print("\n=== Q9: In-Memory File Writing with io.StringIO ===")

def generate_csv_report(file_stream, headers: List[str], rows: List[List[Any]]) -> None:
    """Writes a CSV report to ANY writable text stream (file, StringIO, network)."""
    print(",".join(headers), file=file_stream)
    for row in rows:
        print(",".join(str(val) for val in row), file=file_stream)

# Test in-memory using StringIO without creating any physical disk file!
memory_buffer = io.StringIO()
headers = ["ID", "Name", "Score"]
records = [
    [101, "Alice", 95.5],
    [102, "Bob", 88.0],
    [103, "Charlie", 92.5]
]

generate_csv_report(memory_buffer, headers, records)

# Extract generated content
csv_text = memory_buffer.getvalue()
print(f"  In-memory generated CSV:\n{csv_text}")

assert "ID,Name,Score\n" in csv_text
assert "101,Alice,95.5\n" in csv_text
assert len(csv_text.splitlines()) == 4

# Explanation: `io.StringIO` implements Python's file interface in memory,
# making it ideal for unit testing, string accumulation, and avoiding temporary disk files.


# ============================================================
# Q10: Production-Grade Rotating Audit Log Writer
# ============================================================
# Question: Implement an `AuditLogWriter` class that:
# 1) Appends timestamped audit lines
# 2) Maintains a write buffer count and auto-flushes every N writes
# 3) Checks file size and automatically rotates to `logfile.1` when size exceeds threshold

print("\n=== Q10: Rotating Audit Log Writer Entity ===")

class RotatingAuditLogger:
    def __init__(self, base_filepath: str, max_bytes: int = 500, flush_interval: int = 3):
        self.base_path = base_filepath
        self.max_bytes = max_bytes
        self.flush_interval = flush_interval
        self._unflushed_count = 0
        self._file = open(self.base_path, "a", encoding="utf-8")

    def _rotate_if_needed(self) -> None:
        self._file.flush()
        current_size = os.path.getsize(self.base_path)
        if current_size >= self.max_bytes:
            self._file.close()
            backup_path = f"{self.base_path}.1"
            if os.path.exists(backup_path):
                os.remove(backup_path)
            os.rename(self.base_path, backup_path)
            self._file = open(self.base_path, "w", encoding="utf-8")

    def log(self, action: str, user: str) -> None:
        self._rotate_if_needed()
        entry = f"2026-10-18 | USER={user:<8} | ACTION={action}\n"
        self._file.write(entry)
        self._unflushed_count += 1

        if self._unflushed_count >= self.flush_interval:
            self._file.flush()
            self._unflushed_count = 0

    def close(self) -> None:
        if self._file and not self._file.closed:
            self._file.flush()
            self._file.close()

log_path = os.path.join(tempfile.gettempdir(), f"audit_{os.getpid()}.log")
logger = RotatingAuditLogger(log_path, max_bytes=200, flush_interval=2)

try:
    for i in range(10):
        logger.log(f"EVENT_{i:02d}", "admin")
    logger.close()

    has_backup = os.path.exists(f"{log_path}.1")
    print(f"  Log rotation occurred (backup exists): {has_backup}")
    assert has_backup is True
    assert os.path.exists(log_path)
finally:
    if os.path.exists(log_path): os.remove(log_path)
    if os.path.exists(f"{log_path}.1"): os.remove(f"{log_path}.1")

print("\nAll 10 writing files questions executed and asserted successfully!")
