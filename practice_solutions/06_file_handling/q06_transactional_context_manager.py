"""
Topic 06 - File Handling: Question 6
Problem: Transactional File Editor Context Manager with Automatic Rollback on Exceptions.
"""

from contextlib import contextmanager
import os
import shutil
from typing import Generator, List


class TransactionalFileEditor:
    """Guarantees atomic file updates with automatic rollback via __enter__ and __exit__."""

    def __init__(self, filepath: str):
        self.filepath: str = filepath
        self.bak_path: str = f"{filepath}.bak"
        self.was_new: bool = False

    def __enter__(self) -> "TransactionalFileEditor":
        if os.path.exists(self.filepath):
            shutil.copy2(self.filepath, self.bak_path)
            print(f"Backup created at: {self.bak_path}")
        else:
            self.was_new = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            print(f"Exception encountered: {exc_type.__name__}('{exc_val}')")
            if os.path.exists(self.bak_path):
                shutil.copy2(self.bak_path, self.filepath)
                os.remove(self.bak_path)
                print(f"Rollback executed: Restored {self.filepath} from {self.bak_path}.")
            elif self.was_new and os.path.exists(self.filepath):
                os.remove(self.filepath)
                print(f"Rollback executed: Purged incomplete new file {self.filepath}.")
            return False  # Propagate exception
        else:
            if os.path.exists(self.bak_path):
                os.remove(self.bak_path)
            print("Transaction committed successfully. Backup removed.")
            return True

    def append_text(self, text: str) -> None:
        """Appends string directly to the active working file."""
        with open(self.filepath, mode="a", encoding="utf-8") as f:
            f.write(text)

    def write_lines(self, lines: List[str]) -> None:
        """Overwrites working file with specified lines."""
        with open(self.filepath, mode="w", encoding="utf-8") as f:
            f.writelines(lines)


@contextmanager
def suppress_and_log_io_errors(logger_tag: str) -> Generator[None, None, None]:
    """Generator-based context manager suppressing and logging I/O exceptions."""
    try:
        yield
    except (OSError, FileNotFoundError) as err:
        print(f"[{logger_tag}] Suppressed IO Error: {err}")


# Verification & Execution
config_file = "config.ini"

try:
    # Initialize base config
    with open(config_file, "w", encoding="utf-8") as f:
        f.write("[server]\nport = 8080\n")

    print("Scenario A:")
    with TransactionalFileEditor(config_file) as editor:
        editor.append_text("timeout = 60\n")
        editor.append_text("retries = 3\n")

    print("\nScenario B:")
    try:
        with TransactionalFileEditor(config_file) as editor:
            editor.append_text("corrupted_line = True\n")
            raise RuntimeError("Simulated process crash during file update!")
    except RuntimeError as err:
        print("Caught:", err)

    with open(config_file, "r", encoding="utf-8") as f:
        content = f.read()
    if "corrupted_line" not in content and "retries = 3" in content:
        print("File content verified: Matches pre-transaction state without corrupted_line.")

    # Test generator context manager
    print("\nGenerator Context Manager Test:")
    with suppress_and_log_io_errors("AUDIT"):
        with open("non_existent_system_drive.xyz", "r") as _:
            pass

finally:
    if os.path.exists(config_file):
        os.remove(config_file)
    if os.path.exists(f"{config_file}.bak"):
        os.remove(f"{config_file}.bak")
