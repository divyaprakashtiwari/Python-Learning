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
