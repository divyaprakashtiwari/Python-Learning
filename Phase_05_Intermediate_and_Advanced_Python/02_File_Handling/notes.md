# Phase 5 — Topic 02: File Handling

## 1. Introduction

**File Handling** allows a Python program to persist data to disk and read it back across runs—whether plain-text logs, CSV spreadsheets, configuration files, or raw binary formats like PNG images and audio streams.

In modern Python, safe file I/O rests on three pillars:
1. Always opening files inside a `with open(...)` context manager so OS file descriptors are guaranteed to close even if an exception occurs.
2. Always specifying `encoding="utf-8"` explicitly on text files so behavior is identical across Windows, macOS, and Linux.
3. Using object-oriented `pathlib.Path` paths instead of brittle string concatenation.

---

## 2. Why is it used?

1. **Data Persistence:** Variables in RAM vanish when the Python process exits; files store logs, exports, checkpoints, and state permanently.
2. **Memory-Efficient Streaming:** Iterating over a file object (`for line in fh:`) streams one line at a time in $O(1)$ memory, enabling a laptop with 8 GB RAM to process a 50 GB log file without crashing.
3. **Crash-Safe Atomic Updates:** Writing to a temporary sibling file and calling `Path.replace()` ensures a power loss or crash mid-write never leaves a half-written, corrupted configuration file.
4. **Binary Protocol Inspection:** Reading raw bytes (`mode="rb"`) and navigating byte offsets (`seek` / `tell`) lets you validate file magic numbers (e.g., PNG or PDF headers) without loading entire multi-megabyte assets.

---

## 3. Syntax

```python
from pathlib import Path

# 1. Standard Context-Managed Text Read/Write
with open("report.txt", mode="w", encoding="utf-8") as fh:
    fh.write("Header line\n")

# 2. Memory-Efficient Line Streaming
with open("report.txt", mode="r", encoding="utf-8") as fh:
    for line in fh:
        process(line.rstrip("\n"))

# 3. File Modes Reference
# 'r'  -> Read text (default; raises FileNotFoundError if missing)
# 'w'  -> Write text (truncates/overwrites existing file or creates new)
# 'a'  -> Append text (writes at end of file; creates if missing)
# 'x'  -> Exclusive create (raises FileExistsError if file already exists)
# 'rb' / 'wb' -> Read / Write raw `bytes` (no encoding parameter allowed)

# 4. Concise pathlib One-Liners (for small files)
path = Path("config.ini")
path.write_text("[server]\nport=8080\n", encoding="utf-8")
content = path.read_text(encoding="utf-8")
```

---

## 4. Explanation (Step-by-Step)

1. **Why `with open(...)` Is Mandatory:**
   - Every open file consumes an operating system file descriptor (and holds file locks on Windows). Relying on garbage collection to close an unreferenced file (`open(...).read()`) can delay closing indefinitely on PyPy/GraalPy or exhaust OS file handles inside loops. The `with` statement calls `fh.close()` inside `__exit__` deterministically.
2. **Why Explicit `encoding="utf-8"` Matters:**
   - Until Python 3.15 (PEP 686 default UTF-8 mode), omitting `encoding=` causes `open()` to fall back to `locale.getpreferredencoding(False)`—which on Windows is often legacy `cp1252`, crashing with `UnicodeDecodeError` on emojis or `₹` symbols.
3. **Streaming vs `.read()` / `.readlines()`:**
   - `fh.read()` and `fh.readlines()` load the **entire file into RAM** at once. Iterating `for line in fh:` uses an internal C buffer to yield one line at a time lazily.
4. **Pointer Navigation (`tell()` and `seek()`):**
   - `fh.tell()` returns the current byte offset of the file cursor.
   - `fh.seek(offset, whence)` moves the cursor relative to the start of the file (`whence=0`, default), current position (`whence=1`, binary mode only), or end of file (`whence=2`, binary mode only).

---

## 5. Minimum 3 Examples

### Example 01: Reading, Writing, and Appending UTF-8 Text Files Safely
File: [`example_01_text_file_modes_and_utf8_context.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/02_File_Handling/example_01_text_file_modes_and_utf8_context.py)

```python
"""
Phase 5 - Topic 02: File Handling
Example 01: Reading, Writing, and Appending UTF-8 Text Files Safely (`with open(...)`)

Demonstrates:
  - Using `with open(..., encoding="utf-8")` context managers so file descriptors never leak
  - Modes: `'w'` (write/overwrite), `'a'` (append), `'r'` (read), and `'x'` (exclusive create)
  - Using `tempfile.TemporaryDirectory` so all file I/O is self-contained and leaves zero junk files
"""

from pathlib import Path
import tempfile


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        log_path = Path(tmp_dir) / "audit_log.txt"

        print("=== 1. Writing Initial Lines (`mode='w'`, `encoding='utf-8'`) ===")
        with open(log_path, mode="w", encoding="utf-8") as fh:
            fh.write("2026-11-04 09:00:00 | INFO  | Server started on port 8080\n")
            fh.write("2026-11-04 09:01:15 | WARN  | High memory usage (82%)\n")

        print("=== 2. Appending a Line (`mode='a'`) ===")
        with open(log_path, mode="a", encoding="utf-8") as fh:
            fh.write("2026-11-04 09:02:40 | ERROR | Connection timeout to replica\n")

        print("=== 3. Streaming Line-by-Line (`mode='r'`) ===")
        with open(log_path, mode="r", encoding="utf-8") as fh:
            for line_no, raw_line in enumerate(fh, start=1):
                print(f"  Line {line_no}: {raw_line.rstrip()}")

        print("\n=== 4. Exclusive Creation Guard (`mode='x'`) ===")
        try:
            with open(log_path, mode="x", encoding="utf-8") as fh:
                fh.write("Should not overwrite existing file\n")
        except FileExistsError:
            print("  [mode='x'] Blocked accidental overwrite: FileExistsError raised as expected!")


if __name__ == "__main__":
    main()
```

### Example 02: Structured CSV Processing & Atomic File Replacement Pattern
File: [`example_02_csv_dictreader_and_atomic_write.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/02_File_Handling/example_02_csv_dictreader_and_atomic_write.py)

```python
"""
Phase 5 - Topic 02: File Handling
Example 02: Structured CSV Processing & Atomic File Replacement Pattern

Demonstrates:
  - Reading and writing CSV data cleanly using `csv.DictReader` and `csv.DictWriter`
    with `newline=""` (preventing blank lines on Windows)
  - Atomic write pattern: writing to a `.tmp` file first and using `Path.replace()`
    so a crash mid-write never corrupts the target file
"""

import csv
from pathlib import Path
import tempfile


def write_inventory_atomically(target_path: Path, rows: list[dict[str, object]]) -> None:
    """Write CSV rows to a temporary sibling file, then atomically replace `target_path`."""
    temp_path = target_path.with_suffix(".csv.tmp")
    fieldnames = ["sku", "name", "qty", "price"]
    with open(temp_path, mode="w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    # Atomic OS-level rename/replace
    temp_path.replace(target_path)


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        csv_path = Path(tmp_dir) / "inventory.csv"
        initial_rows = [
            {"sku": "KB-101", "name": "Mechanical Keyboard", "qty": 15, "price": 3499.50},
            {"sku": "MS-202", "name": "Wireless Mouse", "qty": 4, "price": 1299.00},
            {"sku": "MN-303", "name": "27in 4K Monitor", "qty": 8, "price": 24999.00},
        ]

        print("=== 1. Atomic Write of `inventory.csv` ===")
        write_inventory_atomically(csv_path, initial_rows)
        print(f"  Exists: {csv_path.exists()} | Temp file cleaned up: {not csv_path.with_suffix('.csv.tmp').exists()}")

        print("\n=== 2. Reading with `csv.DictReader` & Computing Total Valuation ===")
        total_value = 0.0
        with open(csv_path, mode="r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                item_total = int(row["qty"]) * float(row["price"])
                total_value += item_total
                print(f"  {row['sku']} ({row['name']}): qty={row['qty']} -> Rs.{item_total:,.2f}")
        print(f"  Grand Total Valuation: Rs.{total_value:,.2f}")


if __name__ == "__main__":
    main()
```

### Example 03: Binary File I/O (`rb`/`wb`), Pointer Seeking (`seek`/`tell`), & `pathlib.Path` Helpers
File: [`example_03_binary_io_seek_tell_and_pathlib.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/02_File_Handling/example_03_binary_io_seek_tell_and_pathlib.py)

```python
"""
Phase 5 - Topic 02: File Handling
Example 03: Binary File I/O (`rb`/`wb`), Pointer Seeking (`seek`/`tell`), & `pathlib.Path` Helpers

Demonstrates:
  - Writing and inspecting binary headers with `mode='wb'` and `mode='rb'`
  - Navigating byte offsets with `fh.seek()` and `fh.tell()`
  - Concise one-shot file reads/writes using `Path.write_text()` and `Path.read_text()`
"""

from pathlib import Path
import struct
import tempfile


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        bin_path = Path(tmp_dir) / "sample_image.png"

        print("=== 1. Writing Binary Header + Width/Height (`mode='wb'`) ===")
        # Fake minimal PNG header: 8-byte signature + 4-byte length + b'IHDR' + width(1920) + height(1080)
        ihdr_payload = struct.pack(">II", 1920, 1080)
        with open(bin_path, mode="wb") as fh:
            fh.write(PNG_SIGNATURE)
            fh.write(struct.pack(">I", 8))
            fh.write(b"IHDR")
            fh.write(ihdr_payload)

        print("=== 2. Inspecting Binary Offsets with `seek()` and `tell()` (`mode='rb'`) ===")
        with open(bin_path, mode="rb") as fh:
            sig = fh.read(8)
            print(f"  Is valid PNG signature? {sig == PNG_SIGNATURE} (cursor at byte {fh.tell()})")
            # Jump over 4-byte chunk length + 4-byte 'IHDR' tag (8 bytes relative to current position)
            fh.seek(8, 1)
            print(f"  Cursor after relative seek(8, 1): byte {fh.tell()}")
            width, height = struct.unpack(">II", fh.read(8))
            print(f"  Unpacked Dimensions: {width}x{height} (cursor at byte {fh.tell()})")

        print("\n=== 3. Modern `pathlib.Path` One-Liners (`write_text` / `read_text`) ===")
        note_path = Path(tmp_dir) / "quick_note.txt"
        chars_written = note_path.write_text("Pathlib closes the file automatically!", encoding="utf-8")
        print(f"  Wrote {chars_written} characters -> Read back: {note_path.read_text(encoding='utf-8')!r}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== 1. Writing Initial Lines (`mode='w'`, `encoding='utf-8'`) ===
=== 2. Appending a Line (`mode='a'`) ===
=== 3. Streaming Line-by-Line (`mode='r'`) ===
  Line 1: 2026-11-04 09:00:00 | INFO  | Server started on port 8080
  Line 2: 2026-11-04 09:01:15 | WARN  | High memory usage (82%)
  Line 3: 2026-11-04 09:02:40 | ERROR | Connection timeout to replica

=== 4. Exclusive Creation Guard (`mode='x'`) ===
  [mode='x'] Blocked accidental overwrite: FileExistsError raised as expected!
```

### Output — Example 02
```text
=== 1. Atomic Write of `inventory.csv` ===
  Exists: True | Temp file cleaned up: True

=== 2. Reading with `csv.DictReader` & Computing Total Valuation ===
  KB-101 (Mechanical Keyboard): qty=15 -> Rs.52,492.50
  MS-202 (Wireless Mouse): qty=4 -> Rs.5,196.00
  MN-303 (27in 4K Monitor): qty=8 -> Rs.199,992.00
  Grand Total Valuation: Rs.257,680.50
```

### Output — Example 03
```text
=== 1. Writing Binary Header + Width/Height (`mode='wb'`) ===
=== 2. Inspecting Binary Offsets with `seek()` and `tell()` (`mode='rb'`) ===
  Is valid PNG signature? True (cursor at byte 8)
  Cursor after relative seek(8, 1): byte 16
  Unpacked Dimensions: 1920x1080 (cursor at byte 24)

=== 3. Modern `pathlib.Path` One-Liners (`write_text` / `read_text`) ===
  Wrote 38 characters -> Read back: 'Pathlib closes the file automatically!'
```

---

## 7. Code Explanation

1. **`mode="x"` Exclusive Creation (Example 01):** Unlike `mode="w"`, which silently truncates an existing file to 0 bytes, `mode="x"` atomically checks if the file exists and raises `FileExistsError` if so.
2. **`newline=""` in `csv` Module (Example 02):** The Python `csv` module performs its own `\r\n` line termination. Without `newline=""` in `open()`, Windows translates `\n` to `\r\n` a second time, producing `\r\r\n` and inserting blank rows between every CSV record.
3. **Binary `struct.pack` & Relative `seek(8, 1)` (Example 03):** `>II` packs two big-endian unsigned 32-bit integers (`1920` and `1080`). Calling `fh.seek(8, 1)` advances the cursor 8 bytes forward from its **current** offset (`whence=1`).

---

## 8. Common Mistakes

1. **Forgetting `encoding="utf-8"`:** Causes platform-dependent crashes when reading UTF-8 files on Windows systems where the legacy locale encoding is `cp1252`.
2. **Opening a File in `mode="w"` When You Meant `mode="a"` or `mode="r+"`:** Simply calling `open("data.txt", "w")` immediately wipes the file's contents to 0 bytes before you even call `.write()`.
3. **Calling `fh.read()` Twice Without Seeking Back to `0`:** After `fh.read()` reaches End-Of-File (EOF), the file cursor stays at the end, so a second `fh.read()` returns an empty string `""` unless you call `fh.seek(0)`.
4. **Splitting CSV Lines with `line.split(",")` Instead of the `csv` Module:** Naive `.split(",")` breaks whenever a quoted CSV field itself contains a comma (e.g., `"Bengaluru, KA"`).

---

## 9. Practice Questions

1. **Easy:** Write a function `count_error_lines(log_path: Path) -> int` that streams a potentially huge log file line-by-line without loading the whole file into memory and counts how many lines contain `"ERROR"`.
2. **Medium:** Write a function `tail_lines(file_path: Path, n: int) -> list[str]` using `collections.deque(fh, maxlen=n)` to return the last `n` lines of any text file in $O(n)$ memory.
3. **Hard:** Implement a safe file-rotation helper `rotate_log(log_path: Path, max_bytes: int)` that checks `log_path.stat().st_size` and, if it exceeds `max_bytes`, renames `app.log.1` -> `app.log.2`, `app.log` -> `app.log.1`, and creates a fresh empty `app.log`.

---

## 10. Interview Questions

### Q1: Why is `for line in file_handle:` preferred over `for line in file_handle.readlines():`?
**Answer:** `file_handle.readlines()` reads the entire file into a Python `list` in memory before the loop even starts, which can trigger an `MemoryError` on multi-gigabyte files. Iterating directly over `file_handle` uses the file object as a lazy iterator, holding only a single line (plus a small internal read buffer) in memory at any moment.

### Q2: What is the difference between `fh.flush()` and `os.fsync(fh.fileno())`?
**Answer:**
- `fh.flush()` pushes buffered bytes from Python's user-space I/O buffer out to the operating system's kernel page cache.
- `os.fsync(fh.fileno())` instructs the OS kernel to flush its page cache all the way to the physical disk controller so data survives a sudden power outage.

### Q3: Why can't you use non-zero relative seeks (`fh.seek(offset, 1)`) in text mode (`mode="r"`)?
**Answer:** Variable-width encodings like UTF-8 encode characters using 1 to 4 bytes per character. Because a character offset does not map 1:1 to a byte offset without scanning intermediate bytes, Python restricts arbitrary relative seeking (`whence=1` or `whence=2`) to binary mode (`"rb"`), allowing only `fh.seek(0)` or `fh.seek(cookie_from_tell)` in text mode.
