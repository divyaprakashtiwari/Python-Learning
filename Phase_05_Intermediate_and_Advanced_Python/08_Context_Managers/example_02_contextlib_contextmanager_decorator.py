"""
Phase 5 - Topic 08: Context Managers
Example 02: Generator-Based Context Managers with `@contextlib.contextmanager`

Demonstrates:
  - Writing concise context managers using `@contextlib.contextmanager` and `try / yield / finally`
  - Why wrapping `yield` inside `try ... finally` is mandatory so cleanup still runs on exceptions
"""

from contextlib import contextmanager
import os
from pathlib import Path
import tempfile
from typing import Iterator


@contextmanager
def temporary_working_directory(target_dir: Path) -> Iterator[Path]:
    """Temporarily switch `os.getcwd()` to `target_dir` and restore original cwd on exit."""
    original_cwd = Path.cwd()
    os.chdir(target_dir)
    print(f"  [enter] Switched working directory to: {Path.cwd().name}")
    try:
        yield target_dir
    finally:
        os.chdir(original_cwd)
        print(f"  [exit]  Restored working directory to: {Path.cwd().name}")


def main() -> None:
    start_dir = Path.cwd()
    print(f"=== Starting in `{start_dir.name}` ===")

    with tempfile.TemporaryDirectory() as tmp_str:
        sandbox_dir = Path(tmp_str) / "workspace_sandbox"
        sandbox_dir.mkdir()
        try:
            with temporary_working_directory(sandbox_dir):
                marker = Path("inside_temp.txt")
                marker.write_text("hello", encoding="utf-8")
                print(f"  Inside block: created {marker.name} (exists={marker.exists()})")
                raise ValueError("Simulated error inside context block")
        except ValueError as err:
            print(f"  Caught expected error outside block: {err}")

    print(f"=== Verified cwd restored after exception: {Path.cwd() == start_dir} ===")


if __name__ == "__main__":
    main()
