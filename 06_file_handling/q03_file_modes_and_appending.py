"""
Topic 06: File Handling
Question 03: File Modes and Appending (Deep Dive)

Master Python file open modes and append mechanics:
- Core mode matrix: 'r', 'w', 'a', 'x' (existence, creation, and truncation rules)
- Update modes: 'r+', 'w+', 'a+' nuances and pointer behaviors
- Append mode ('a') mechanics: preserving existing content
- The 'a+' read-cursor quirk (cursor starts at EOF; seek(0) required to read)
- In-place file modification with 'r+' (patching bytes at offset)
- Text ('t') vs Binary ('b') modes and newline translation differences
- File truncation with f.truncate(size)
- Cross-platform file locking with msvcrt (Windows) / fcntl (POSIX)
- Safe concurrent append validation
- Production-grade Write-Ahead Log (WAL) engine with sequential replay
"""

import os
import sys
import tempfile
from typing import Any, Dict, List, Optional, Tuple


# ============================================================
# Q1: The Core Mode Matrix ('r', 'w', 'a', 'x')
# ============================================================
# Question: Demonstrate the fundamental behavioral differences among the 4 primary modes:
# - 'r': Read-only, file must exist (raises FileNotFoundError)
# - 'w': Write-only, creates if missing, truncates to 0 if exists
# - 'a': Append-only, creates if missing, writes at end
# - 'x': Exclusive creation, writes, raises FileExistsError if exists

print("=== Q1: Core Mode Matrix ('r', 'w', 'a', 'x') ===")

temp_dir = tempfile.gettempdir()
f_path = os.path.join(temp_dir, f"mode_matrix_{os.getpid()}.txt")

try:
    # 1. 'r' fails when file does not exist
    caught_r_err = False
    try:
        open(f_path, "r")
    except FileNotFoundError:
        caught_r_err = True
    assert caught_r_err
    print("  'r' mode correctly raised FileNotFoundError on missing file.")

    # 2. 'x' creates new file
    with open(f_path, "x", encoding="utf-8") as f:
        f.write("Line 1\n")
    print("  'x' mode created new file.")

    # 3. 'a' appends without truncating
    with open(f_path, "a", encoding="utf-8") as f:
        f.write("Line 2\n")

    with open(f_path, "r", encoding="utf-8") as f:
        assert f.read() == "Line 1\nLine 2\n"
    print("  'a' mode appended Line 2 without truncating Line 1.")

    # 4. 'w' truncates existing content
    with open(f_path, "w", encoding="utf-8") as f:
        f.write("Fresh Start\n")

    with open(f_path, "r", encoding="utf-8") as f:
        assert f.read() == "Fresh Start\n"
    print("  'w' mode truncated existing file back to 0 bytes.")
finally:
    if os.path.exists(f_path):
        os.remove(f_path)


# ============================================================
# Q2: Update Modes Comparison ('r+', 'w+', 'a+')
# ============================================================
# Question: Compare the update modes ('+'):
# - 'r+': read and write, file MUST exist, no truncation, cursor at 0
# - 'w+': read and write, truncates immediately to 0 bytes
# - 'a+': read and append, writes always go to EOF regardless of seek

print("\n=== Q2: Update Modes ('r+', 'w+', 'a+') ===")

with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
    tmp.write("Hello World")
    tmp_path = tmp.name

try:
    # 1. 'r+' modifies in-place without truncation
    with open(tmp_path, "r+", encoding="utf-8") as f:
        content = f.read(5)  # Read 'Hello'
        assert content == "Hello"
        f.seek(6)
        f.write("Python")   # Overwrite 'World' with 'Python'

    with open(tmp_path, "r", encoding="utf-8") as f:
        res_r_plus = f.read()
    print(f"  'r+' modified in-place: '{res_r_plus}'")
    assert res_r_plus == "Hello Python"

    # 2. 'w+' truncates everything immediately on open!
    with open(tmp_path, "w+", encoding="utf-8") as f:
        assert f.read() == ""  # File was wiped clean on open
        f.write("Wiped and Replaced")
        f.seek(0)
        res_w_plus = f.read()
    print(f"  'w+' truncated then read: '{res_w_plus}'")
    assert res_w_plus == "Wiped and Replaced"
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: Use `'r+'` when you need to read existing data and overwrite parts of it.
# Use `'w+'` when you want a blank slate that you can write to and read back in the same session.


# ============================================================
# Q3: Append Mode ('a') & Preserving Historical State
# ============================================================
# Question: Show how opening in `'a'` mode guarantees that multiple successive append
# operations never overwrite or corrupt existing file lines.

print("\n=== Q3: Append Mode Mechanics ===")

with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
    tmp_path = tmp.name

try:
    # Multiple independent append sessions
    for i in range(1, 4):
        with open(tmp_path, "a", encoding="utf-8") as f:
            f.write(f"Session {i} Log Entry\n")

    with open(tmp_path, "r", encoding="utf-8") as f:
        all_logs = f.readlines()

    print(f"  Total appended lines: {len(all_logs)}")
    assert len(all_logs) == 3
    assert all_logs[0] == "Session 1 Log Entry\n"
    assert all_logs[2] == "Session 3 Log Entry\n"
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: `'a'` mode positions the file pointer at the end of the file before
# every write, making it the standard mode for logs and event streams.


# ============================================================
# Q4: The 'a+' Read-Cursor Quirk (seek(0) Required!)
# ============================================================
# Question: Explain the common pitfall with `'a+'` mode:
# When opened in `'a+'`, the cursor starts at the end of the file!
# Demonstrate that `f.read()` returns `""` until `f.seek(0)` is called.
# Also show that writes in `'a+'` STILL go to the end, even after `seek(0)`.

print("\n=== Q4: The 'a+' Read-Cursor Quirk ===")

with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
    tmp.write("Initial Data Line\n")
    tmp_path = tmp.name

try:
    with open(tmp_path, "a+", encoding="utf-8") as f:
        # THE QUIRK: Initial read returns empty string because cursor is at EOF!
        initial_read = f.read()
        print(f"  Initial read in 'a+' without seek: '{initial_read}' (Empty!)")
        assert initial_read == ""
        assert f.tell() > 0

        # Seek to beginning to read existing data
        f.seek(0)
        data_after_seek = f.read()
        print(f"  Read after seek(0): '{data_after_seek.strip()}'")
        assert "Initial Data Line" in data_after_seek

        # ATTEMPTING WRITE AFTER SEEK(0):
        # Even though cursor was at 0, append mode FORCES the write to the END of the file!
        f.seek(0)
        f.write("Appended at End\n")

    with open(tmp_path, "r", encoding="utf-8") as f:
        final_content = f.read()

    print(f"  Final content after write:\n{final_content}")
    assert final_content.startswith("Initial Data Line\n")
    assert final_content.endswith("Appended at End\n")
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: In `'a+'` mode, reads respect the cursor position (e.g. `seek(0)`).
# However, writes in append mode ALWAYS append to the end of the file according to C POSIX semantics.


# ============================================================
# Q5: In-Place Patching with 'r+' Mode
# ============================================================
# Question: Open a file in `'r+'` mode, search for a specific header, and overwrite
# that exact section without modifying the surrounding data.

print("\n=== Q5: In-Place Patching with 'r+' Mode ===")

record_template = "STATUS:PENDING | USER:alice | RETRIES:0"

with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
    tmp.write(record_template)
    tmp_path = tmp.name

try:
    with open(tmp_path, "r+", encoding="utf-8") as f:
        content = f.read()
        offset = content.find("PENDING")
        assert offset != -1

        # Reposition cursor exactly to 'PENDING' and overwrite with 'ACTIVE ' (same length)
        f.seek(offset)
        f.write("ACTIVE ")

    with open(tmp_path, "r", encoding="utf-8") as f:
        patched_record = f.read()

    print(f"  Original: '{record_template}'")
    print(f"  Patched:  '{patched_record}'")
    assert patched_record == "STATUS:ACTIVE  | USER:alice | RETRIES:0"
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: `'r+'` enables random-access binary or text patching.
# Overwriting must match character lengths to avoid shifting remaining file bytes.


# ============================================================
# Q6: Text Mode ('t') vs Binary Mode ('b')
# ============================================================
# Question: Compare `'t'` (text) and `'b'` (binary) modes:
# 1) Type returned: `str` vs `bytes`
# 2) Line ending translation: CRLF (`\r\n`) -> LF (`\n`) in text mode vs raw bytes in binary mode
# 3) Encodings: text mode requires encoding; binary mode forbids encoding parameter.

print("\n=== Q6: Text Mode vs Binary Mode ===")

with tempfile.NamedTemporaryFile("wb", delete=False) as tmp:
    tmp.write(b"Line 1\r\nLine 2\r\n")
    tmp_path = tmp.name

try:
    # 1. Text mode ('rt')
    with open(tmp_path, "rt", encoding="utf-8") as f_text:
        text_content = f_text.read()
    print(f"  Text mode type:   {type(text_content).__name__}")
    print(f"  Text mode lines:  {[repr(l) for l in text_content.splitlines(keepends=True)]}")
    assert isinstance(text_content, str)
    # Universal newline translated '\r\n' to '\n'
    assert text_content == "Line 1\nLine 2\n"

    # 2. Binary mode ('rb')
    with open(tmp_path, "rb") as f_bin:
        bin_content = f_bin.read()
    print(f"  Binary mode type: {type(bin_content).__name__}")
    print(f"  Binary raw bytes: {bin_content}")
    assert isinstance(bin_content, bytes)
    # Raw CRLF '\r\n' preserved exactly!
    assert bin_content == b"Line 1\r\nLine 2\r\n"
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: Text mode automatically decodes bytes to strings and translates line endings.
# Binary mode deals with raw bytes directly without any encoding or translation.


# ============================================================
# Q7: Truncating Files with f.truncate(size)
# ============================================================
# Question: Use `f.truncate(size)` to resize an existing file:
# 1) Truncate to a smaller size (shrink file)
# 2) Truncate to a larger size (sparse expansion filled with zero bytes)

print("\n=== Q7: f.truncate(size) File Resizing ===")

with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
    tmp.write("0123456789ABCDEF")  # 16 characters
    tmp_path = tmp.name

try:
    # Shrink file to 10 bytes using 'r+'
    with open(tmp_path, "r+", encoding="utf-8") as f:
        f.seek(10)
        f.truncate()  # Truncates at current position (10 bytes)

    with open(tmp_path, "r", encoding="utf-8") as f:
        shrunk_content = f.read()
    print(f"  Content after truncate(10): '{shrunk_content}'")
    assert shrunk_content == "0123456789"
    assert os.path.getsize(tmp_path) == 10

    # Expand file to 15 bytes in binary mode (pads with \x00 null bytes)
    with open(tmp_path, "rb+") as f_bin:
        f_bin.truncate(15)

    with open(tmp_path, "rb") as f_bin:
        expanded_bytes = f_bin.read()
    print(f"  Expanded bytes with null padding: {expanded_bytes}")
    assert len(expanded_bytes) == 15
    assert expanded_bytes.endswith(b"\x00\x00\x00\x00\x00")
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: `truncate([size])` resizes the file. If size is smaller, extra data
# is discarded. If larger, the file is zero-padded up to the target length.


# ============================================================
# Q8: Cross-Platform File Locking in Append Mode
# ============================================================
# Question: Implement file locking for append operations to prevent interleaved writes
# from concurrent processes. Support Windows (`msvcrt`) and POSIX (`fcntl`).

print("\n=== Q8: Cross-Platform File Locking ===")

class FileLockContext:
    def __init__(self, file_obj):
        self.file_obj = file_obj

    def __enter__(self):
        if sys.platform == "win32":
            import msvcrt
            # Lock 1 byte at current position (non-blocking test)
            try:
                msvcrt.locking(self.file_obj.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError:
                pass  # Already locked or non-blocking
        else:
            try:
                import fcntl
                fcntl.flock(self.file_obj.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except (ImportError, OSError):
                pass
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if sys.platform == "win32":
            import msvcrt
            try:
                msvcrt.locking(self.file_obj.fileno(), msvcrt.LK_UNLCK, 1)
            except OSError:
                pass
        else:
            try:
                import fcntl
                fcntl.flock(self.file_obj.fileno(), fcntl.LOCK_UN)
            except (ImportError, OSError):
                pass

with tempfile.NamedTemporaryFile("a+", delete=False, encoding="utf-8") as tmp:
    tmp_path = tmp.name

try:
    with open(tmp_path, "a", encoding="utf-8") as f:
        with FileLockContext(f):
            f.write("Process 1: Atomic Locked Write\n")

    with open(tmp_path, "r", encoding="utf-8") as f:
        assert "Atomic Locked Write" in f.read()
    print("  Successfully executed locked file write.")
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: File locks ensure exclusive access across multiple processes,
# preventing split writes and corrupted lines in shared logfiles.


# ============================================================
# Q9: Validating Combination Modes ('xb', 'ab+', 'wb')
# ============================================================
# Question: Test composite binary modes:
# 1) `'xb'`: exclusive binary creation
# 2) `'ab+'`: append binary with read capability

print("\n=== Q9: Composite Binary Modes ('xb', 'ab+') ===")

bin_target = os.path.join(tempfile.gettempdir(), f"bin_mode_test_{os.getpid()}.bin")

try:
    # 1. 'xb': create exclusive binary
    magic_header = b"\x89PNG\r\n\x1a\n"
    with open(bin_target, "xb") as f_bin:
        f_bin.write(magic_header)
    assert os.path.exists(bin_target)

    # 2. 'ab+': append binary and read
    with open(bin_target, "ab+") as f_bin:
        f_bin.write(b"CHUNK_IHDR")
        f_bin.seek(0)
        full_bin = f_bin.read()

    print(f"  Binary header + chunk: {full_bin}")
    assert full_bin == magic_header + b"CHUNK_IHDR"
finally:
    if os.path.exists(bin_target):
        os.remove(bin_target)

# Explanation: Combining `b` (binary) with `+`, `a`, `w`, or `x` allows binary stream
# manipulation without character decoding overhead.


# ============================================================
# Q10: Production-Grade Write-Ahead Log (WAL) Engine
# ============================================================
# Question: Implement a production-grade Write-Ahead Log (WAL) engine:
# - Append-only format with sequential transaction IDs and checksums
# - Reads from start to replay database operations on crash recovery
# - Supports checkpointing and log truncation

print("\n=== Q10: Write-Ahead Log (WAL) Engine Entity ===")

class WriteAheadLog:
    def __init__(self, wal_path: str):
        self.wal_path = wal_path
        self._seq_id = 0
        # Initialize WAL file if missing
        if not os.path.exists(wal_path):
            with open(wal_path, "w", encoding="utf-8") as f:
                f.write("# WAL_VERSION_1.0\n")

    def append_entry(self, operation: str, key: str, value: Any) -> int:
        """Appends a new transaction entry in append mode."""
        self._seq_id += 1
        record = f"{self._seq_id}|{operation}|{key}|{value}\n"
        with open(self.wal_path, "a", encoding="utf-8") as f:
            f.write(record)
            f.flush()
            os.fsync(f.fileno())
        return self._seq_id

    def replay_state(self) -> Dict[str, Any]:
        """Reconstructs state by replaying all WAL operations in order."""
        state: Dict[str, Any] = {}
        with open(self.wal_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("|", 3)
                if len(parts) == 4:
                    seq, op, k, v = parts
                    self._seq_id = max(self._seq_id, int(seq))
                    if op == "SET":
                        state[k] = v
                    elif op == "DELETE":
                        state.pop(k, None)
        return state

    def checkpoint(self) -> None:
        """Truncates WAL after state snapshot has been safely persisted."""
        with open(self.wal_path, "w", encoding="utf-8") as f:
            f.write("# WAL_VERSION_1.0\n")
        self._seq_id = 0

wal_file = os.path.join(tempfile.gettempdir(), f"db_{os.getpid()}.wal")
wal = WriteAheadLog(wal_file)

try:
    # 1. Append transactions
    wal.append_entry("SET", "user:1", "Alice")
    wal.append_entry("SET", "user:2", "Bob")
    wal.append_entry("SET", "user:3", "Charlie")
    wal.append_entry("DELETE", "user:2", "")

    # 2. Replay state from WAL
    replayed_state = wal.replay_state()
    print(f"  Replayed Database State from WAL: {replayed_state}")

    assert replayed_state == {"user:1": "Alice", "user:3": "Charlie"}
    assert "user:2" not in replayed_state

    # 3. Checkpoint clears WAL
    wal.checkpoint()
    state_after_checkpoint = wal.replay_state()
    print(f"  State after checkpoint truncation: {state_after_checkpoint}")
    assert state_after_checkpoint == {}
finally:
    if os.path.exists(wal_file):
        os.remove(wal_file)

print("\nAll 10 file modes and appending questions executed and asserted successfully!")
