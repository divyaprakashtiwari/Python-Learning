"""
Topic 06: File Handling
Question 01: Reading Files (Deep Dive)

Master file reading mechanics and stream navigation in Python:
- Reading entire contents with read()
- Line-by-line reading with readline() and EOF detection
- Loading lines into memory with readlines() and newline stripping
- Memory-efficient streaming iteration (for line in file)
- Chunked reading with fixed buffer size (f.read(chunk_size))
- Cursor navigation with tell() and seek(offset, whence)
- Character encoding handling (UTF-8, UTF-16, ASCII) and error strategies
- Resilient error handling (FileNotFoundError, PermissionError)
- Universal newlines mode and newline parameter variations
- Production-grade INI/Config File Parser reading structured key-value sections
"""

import io
import os
import tempfile
from typing import Any, Dict, Generator, List, Optional, Tuple


# ============================================================
# Q1: Reading Entire File with read()
# ============================================================
# Question: Demonstrate reading an entire file into memory using `.read()`.
# Explain when `.read()` is suitable (small/medium files) and when it causes OOM errors.

print("=== Q1: Reading Entire File with read() ===")

with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
    tmp.write("Line 1: System Boot\nLine 2: CPU Check OK\nLine 3: Ready")
    tmp_path = tmp.name

try:
    with open(tmp_path, "r", encoding="utf-8") as f:
        full_content = f.read()

    print(f"  Full file content:\n{full_content}")
    assert "Line 1: System Boot" in full_content
    assert full_content.endswith("Ready")
    assert len(full_content.splitlines()) == 3
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: `file.read()` loads the entire file into a single `str` (or `bytes`) in memory.
# It is fast and simple for small-to-medium files (e.g. configs, small JSON), but should
# not be used on multi-gigabyte datasets where memory is constrained.


# ============================================================
# Q2: Line-by-Line Reading with readline() and EOF Detection
# ============================================================
# Question: Read a file line-by-line using `readline()`.
# Explain how Python detects EOF (returns an empty string `""`), whereas a blank line returns `"\n"`.

print("\n=== Q2: readline() and EOF Detection ===")

with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
    tmp.write("Alpha\n\nBeta\n")  # Contains a blank line between Alpha and Beta
    tmp_path = tmp.name

try:
    lines_read = []
    with open(tmp_path, "r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if line == "":  # EOF reached!
                break
            lines_read.append(line)

    print(f"  Total lines read: {len(lines_read)}")
    print(f"  Line 1 repr: {repr(lines_read[0])} (Non-empty content + newline)")
    print(f"  Line 2 repr: {repr(lines_read[1])} (Blank line: '\\n', NOT EOF!)")
    print(f"  Line 3 repr: {repr(lines_read[2])} (Non-empty content + newline)")

    assert lines_read[0] == "Alpha\n"
    assert lines_read[1] == "\n"   # Blank line is NOT empty string!
    assert lines_read[2] == "Beta\n"
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: `readline()` returns `"\n"` for a blank line, and `""` (empty string)
# exclusively when the end-of-file (EOF) is reached.


# ============================================================
# Q3: Loading All Lines with readlines() & Stripping Newlines
# ============================================================
# Question: Read all lines into a list using `readlines()`.
# Demonstrate stripping trailing newline characters using list comprehension.

print("\n=== Q3: readlines() & Trailing Newline Stripping ===")

sample_text = "Host=127.0.0.1\nPort=8080\nTimeout=30\nDebug=True\n"

with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
    tmp.write(sample_text)
    tmp_path = tmp.name

try:
    with open(tmp_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    # Clean newlines
    clean_lines = [line.rstrip("\r\n") for line in raw_lines]

    print(f"  Raw lines count:   {len(raw_lines)}")
    print(f"  Clean lines:       {clean_lines}")

    assert raw_lines[0] == "Host=127.0.0.1\n"
    assert clean_lines[0] == "Host=127.0.0.1"
    assert clean_lines[1] == "Port=8080"
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: `readlines()` reads all lines into a list of strings, retaining `\n`.
# Using `line.rstrip('\r\n')` safely removes trailing carriage returns and line feeds.


# ============================================================
# Q4: Memory-Efficient Streaming Iteration
# ============================================================
# Question: Demonstrate reading a file using the file iterator: `for line in f:`.
# Explain why this is preferred over `readlines()` for arbitrarily large files.

print("\n=== Q4: Memory-Efficient File Iteration ===")

with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
    for i in range(100):
        tmp.write(f"log_entry_id_{i:04d} severity=INFO latency={i * 2}ms\n")
    tmp_path = tmp.name

try:
    processed_count = 0
    total_latency = 0

    with open(tmp_path, "r", encoding="utf-8") as f:
        # File object acts as a generator/iterator, yielding one line at a time
        for line in f:
            processed_count += 1
            if "latency=" in line:
                lat = int(line.split("latency=")[1].replace("ms\n", ""))
                total_latency += lat

    avg_latency = total_latency / processed_count
    print(f"  Streamed {processed_count} lines without buffering entire file.")
    print(f"  Computed average latency: {avg_latency:.1f} ms")

    assert processed_count == 100
    assert avg_latency == 99.0  # Sum of 2*i for i in 0..99 / 100 = 99.0
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: The file iterator uses internal C-level read-ahead buffering (typically 8KB),
# loading chunks as needed and yielding lines lazily without consuming RAM for the entire file.


# ============================================================
# Q5: Chunked Reading with Fixed Buffer Size
# ============================================================
# Question: Read a file in fixed-size character/byte chunks using `f.read(chunk_size)`
# until empty. Count total chunks processed.

print("\n=== Q5: Fixed-Size Chunked Reading ===")

def read_in_chunks(file_obj, chunk_size: int = 16) -> Generator[str, None, None]:
    """Yields file content in fixed-size chunks."""
    while True:
        chunk = file_obj.read(chunk_size)
        if not chunk:
            break
        yield chunk

sample_data = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
    tmp.write(sample_data)
    tmp_path = tmp.name

try:
    chunks_list = []
    with open(tmp_path, "r", encoding="utf-8") as f:
        for chk in read_in_chunks(f, chunk_size=10):
            chunks_list.append(chk)

    print(f"  Total data length:  {len(sample_data)} characters")
    print(f"  Chunks received:    {chunks_list}")
    print(f"  Reconstructed text: '{''.join(chunks_list)}'")

    assert len(chunks_list) == 4  # 10 + 10 + 10 + 6
    assert chunks_list[0] == "ABCDEFGHIJ"
    assert chunks_list[3] == "456789"
    assert "".join(chunks_list) == sample_data
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: Passing an integer `chunk_size` to `.read(N)` specifies the maximum
# number of characters (in text mode) or bytes (in binary mode) to read.


# ============================================================
# Q6: File Cursor Navigation (tell() and seek())
# ============================================================
# Question: Demonstrate file pointer tracking using `.tell()` and cursor repositioning
# using `.seek(offset, whence)`.

print("\n=== Q6: tell() and seek() Cursor Navigation ===")

with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
    tmp.write("0123456789abcdefghij")
    tmp_path = tmp.name

try:
    with open(tmp_path, "r", encoding="utf-8") as f:
        # Initial cursor position
        assert f.tell() == 0

        # Read first 5 chars
        part1 = f.read(5)
        pos_after_read = f.tell()
        print(f"  Read 5 chars: '{part1}', cursor at: {pos_after_read}")
        assert part1 == "01234"
        assert pos_after_read == 5

        # Seek back to beginning (offset 0, whence 0)
        f.seek(0)
        print(f"  After seek(0), cursor at: {f.tell()}")
        assert f.tell() == 0
        reread = f.read(5)
        assert reread == "01234"

        # Seek to offset 10 from start
        f.seek(10)
        part2 = f.read(6)
        print(f"  Read from offset 10: '{part2}'")
        assert part2 == "abcdef"
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: `f.tell()` returns the current byte position of the cursor.
# `f.seek(offset, whence)` moves the cursor: whence 0=start of file, 1=current, 2=end of file.
# Note: in text mode on Python 3, relative seeks (whence 1 or 2) require offset=0 or binary mode.


# ============================================================
# Q7: Encodings and Handling Decode Errors
# ============================================================
# Question: Demonstrate reading files with specific encodings (UTF-8 vs Latin-1).
# Show how `errors='replace'` and `errors='ignore'` handle invalid byte sequences gracefully.

print("\n=== Q7: Character Encodings & Decode Error Strategies ===")

# Write raw bytes in Latin-1 / CP1252 that are invalid UTF-8 sequences
raw_bytes = b"Price: \xa3100.00 (GBP)"  # \xa3 is British Pound in Latin-1

with tempfile.NamedTemporaryFile("wb", delete=False) as tmp:
    tmp.write(raw_bytes)
    tmp_path = tmp.name

try:
    # 1. Reading with strict UTF-8 raises UnicodeDecodeError
    caught_decode_error = False
    try:
        with open(tmp_path, "r", encoding="utf-8", errors="strict") as f:
            f.read()
    except UnicodeDecodeError as err:
        caught_decode_error = True
        print(f"  Caught expected UnicodeDecodeError: {err.reason}")
    assert caught_decode_error

    # 2. Reading with errors='replace': replaces invalid bytes with replacement character
    with open(tmp_path, "r", encoding="utf-8", errors="replace") as f:
        replaced_text = f.read()
    print(f"  Read with errors='replace': {ascii(replaced_text)}")
    assert "Price:" in replaced_text

    # 3. Reading with correct encoding (latin-1) decodes accurately
    with open(tmp_path, "r", encoding="latin-1") as f:
        correct_text = f.read()
    print(f"  Read with correct 'latin-1': {ascii(correct_text)}")
    assert "Price: \xa3100.00 (GBP)" == correct_text
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: Text files are sequences of bytes mapped via a character encoding.
# Always explicitly specify `encoding='utf-8'` (or appropriate encoding) to prevent
# OS-dependent default encoding mismatches.


# ============================================================
# Q8: Resilient Error Handling (FileNotFoundError, PermissionError)
# ============================================================
# Question: Implement a safe reader function `safe_read_file(path, default=None)`
# that catches `FileNotFoundError`, `IsADirectoryError`, and `PermissionError` without crashing.

print("\n=== Q8: Resilient File Error Handling ===")

def safe_read_file(filepath: str, default: Optional[str] = None) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Returns (success: bool, content: Optional[str], error_message: Optional[str]).
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return True, f.read(), None
    except FileNotFoundError:
        return False, default, f"File not found: '{filepath}'"
    except IsADirectoryError:
        return False, default, f"Path is a directory, not a file: '{filepath}'"
    except PermissionError:
        return False, default, f"Permission denied for: '{filepath}'"
    except Exception as exc:
        return False, default, f"Unexpected I/O error: {exc}"

# Test 1: Non-existent file
ok1, content1, err1 = safe_read_file("non_existent_file_9999.txt", default="EMPTY")
print(f"  Non-existent: ok={ok1}, content={content1}, error='{err1}'")
assert ok1 is False
assert content1 == "EMPTY"
assert "File not found" in str(err1)

# Test 2: Reading a directory path as a file
ok2, content2, err2 = safe_read_file(".", default=None)
print(f"  Directory as file: ok={ok2}, error='{err2}'")
assert ok2 is False
assert "is a directory" in str(err2) or "Permission denied" in str(err2)

# Explanation: Wrapping file access with granular `OSError` subclasses prevents
# unexpected filesystem conditions from terminating server processes.


# ============================================================
# Q9: Universal Newlines Mode
# ============================================================
# Question: Explain Python's universal newlines mode: how Python automatically translates
# Windows `\r\n`, Unix `\n`, and legacy Mac `\r` line endings to `\n` in text mode.

print("\n=== Q9: Universal Newlines Translation ===")

# Create binary content containing mixed line endings: Unix (\n), Windows (\r\n), Mac (\r)
mixed_endings_bytes = b"Unix line\nWindows line\r\nLegacy Mac line\rEnd"

with tempfile.NamedTemporaryFile("wb", delete=False) as tmp:
    tmp.write(mixed_endings_bytes)
    tmp_path = tmp.name

try:
    # Reading in default text mode translates all variants to '\n'
    with open(tmp_path, "r", encoding="utf-8") as f:
        lines_translated = f.readlines()

    print(f"  Lines with universal newlines: {[repr(l) for l in lines_translated]}")
    assert lines_translated[0] == "Unix line\n"
    assert lines_translated[1] == "Windows line\n"
    assert lines_translated[2] == "Legacy Mac line\n"
    assert lines_translated[3] == "End"

    # Reading with newline='' preserves raw original line endings!
    with open(tmp_path, "r", encoding="utf-8", newline="") as f:
        raw_lines = f.readlines()

    print(f"  Raw lines without translation: {[repr(l) for l in raw_lines]}")
    assert raw_lines[1] == "Windows line\r\n"
    assert raw_lines[2] == "Legacy Mac line\r"
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# Explanation: Python 3 opens text files in universal newlines mode by default,
# transparently normalizing all CRLF and CR endings into standard LF (`\n`).


# ============================================================
# Q10: Production-Grade INI/Config File Parser
# ============================================================
# Question: Implement a production-grade configuration reader that parses INI-style files:
# ignores comments (`#`, `;`) and empty lines, extracts `[section]` headers,
# parses `key = value` pairs, and casts numeric/boolean values.

print("\n=== Q10: Production-Grade INI Config File Parser ===")

raw_ini_content = """
# System Configuration File
; Auto-generated 2026

[database]
host = db.internal.org
port = 5432
max_connections = 100
ssl_enabled = true

[server]
host = 0.0.0.0
port = 8080
debug = false
timeout = 30.5

# End of file
"""

def parse_ini_file(filepath: str) -> Dict[str, Dict[str, Any]]:
    """Parses an INI configuration file into structured dictionary sections."""
    sections: Dict[str, Dict[str, Any]] = {}
    current_section = "default"

    def _cast_val(raw_val: str) -> Any:
        v = raw_val.strip()
        if v.lower() == "true": return True
        if v.lower() == "false": return False
        if v.isdigit(): return int(v)
        try:
            return float(v)
        except ValueError:
            return v

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            clean = line.strip()
            # Ignore empty lines and comments
            if not clean or clean.startswith(("#", ";")):
                continue

            # Section header: [section_name]
            if clean.startswith("[") and clean.endswith("]"):
                current_section = clean[1:-1].strip()
                sections.setdefault(current_section, {})
            elif "=" in clean:
                key, val = clean.split("=", 1)
                key = key.strip()
                sections.setdefault(current_section, {})[key] = _cast_val(val)

    return sections

with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
    tmp.write(raw_ini_content)
    tmp_path = tmp.name

try:
    parsed_config = parse_ini_file(tmp_path)

    print("  Parsed Configuration Structure:")
    for section, values in parsed_config.items():
        print(f"    [{section}]")
        for k, v in values.items():
            print(f"      {k} = {v} (type: {type(v).__name__})")

    assert "database" in parsed_config
    assert "server" in parsed_config
    assert parsed_config["database"]["port"] == 5432
    assert parsed_config["database"]["ssl_enabled"] is True
    assert parsed_config["server"]["debug"] is False
    assert parsed_config["server"]["timeout"] == 30.5
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

print("\nAll 10 reading files questions executed and asserted successfully!")
