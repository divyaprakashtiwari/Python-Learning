"""
Phase 5 - Topic 08: Context Managers
Example 03: Standard `contextlib` Power Tools (`suppress`, `redirect_stdout`, and `ExitStack`)

Demonstrates:
  - `contextlib.suppress()`: declarative replacement for `try: ... except FileNotFoundError: pass`
  - `contextlib.redirect_stdout()`: capturing `print()` output into an `io.StringIO` buffer
  - `contextlib.ExitStack()`: dynamically entering an arbitrary number of context managers at runtime
"""

from contextlib import ExitStack, redirect_stdout, suppress
import io
from pathlib import Path
import tempfile


def main() -> None:
    print("=== 1. `contextlib.suppress` for Intentional Error Ignoring ===")
    with suppress(FileNotFoundError):
        Path("non_existent_temp_file_12345.tmp").unlink()
    print("  Cleanly ignored missing file deletion via `with suppress(FileNotFoundError):`")

    print("\n=== 2. Capturing `print()` Output with `contextlib.redirect_stdout` ===")
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print("Line A captured in memory")
        print("Line B captured in memory")
    captured_lines = buffer.getvalue().splitlines()
    print(f"  Captured {len(captured_lines)} lines: {captured_lines}")

    print("\n=== 3. Dynamic Multi-File Management with `contextlib.ExitStack` ===")
    with tempfile.TemporaryDirectory() as tmp_dir:
        paths = [Path(tmp_dir) / f"shard_{i}.txt" for i in range(3)]
        with ExitStack() as stack:
            handles = [stack.enter_context(open(p, mode="w", encoding="utf-8")) for p in paths]
            for idx, fh in enumerate(handles):
                fh.write(f"Shard #{idx} payload\n")
        # All 3 files are guaranteed closed upon exiting `ExitStack`
        print(f"  All {len(paths)} handles closed? {[fh.closed for fh in handles]}")


if __name__ == "__main__":
    main()
