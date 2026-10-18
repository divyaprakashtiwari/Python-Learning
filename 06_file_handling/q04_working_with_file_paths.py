"""
Topic 06: File Handling - Question 04: Working with File Paths

A comprehensive collection of 10 standalone, runnable exercises exploring
file path operations in Python using both legacy `os.path` and modern `pathlib.Path`.

Questions Covered:
 1. os.path vs pathlib.Path: Fundamentals of path construction, joining, and splitting.
 2. Path Decomposition: Stem, suffix, multi-suffixes (.tar.gz), parent hierarchy, and parts.
 3. Absolute vs Relative Paths: resolve(), is_absolute(), and relative_to() calculations.
 4. Directory Traversal with iterdir(): Inspecting file types, sizes, and filtering entries.
 5. Pattern Matching and Globbing: glob() and rglob() for recursive directory discovery.
 6. Path Normalization and Expansion: normpath(), resolving symlinks/dots, and expanduser().
 7. Directory Tree Management: mkdir(parents=True, exist_ok=True) and recursive directory cleanup.
 8. Direct Path I/O: read_text(), write_text(), touch(), and unlink() convenience methods.
 9. Cross-Platform Pure Paths & Path Sanitization: Handling Windows vs POSIX path separators.
10. Advanced Project: File Cataloger & Directory Tree Analyzer with size metrics and depth limits.
"""

import os
import shutil
import tempfile
from pathlib import Path, PurePosixPath, PureWindowsPath


# ==============================================================================
# Question 1: os.path vs pathlib.Path Fundamentals
# ==============================================================================
def exercise_q1_path_fundamentals() -> None:
    """
    Demonstrate foundational path operations using both os.path and pathlib.Path:
    joining path segments, extracting basename, dirname, and file extensions.
    """
    print("=== Q1: os.path vs pathlib.Path Fundamentals ===")

    # Legacy os.path approach
    legacy_dir = os.path.join("var", "log", "app")
    legacy_file = os.path.join(legacy_dir, "server.log")
    legacy_base = os.path.basename(legacy_file)
    legacy_dir_name = os.path.dirname(legacy_file)
    legacy_root, legacy_ext = os.path.splitext(legacy_file)

    assert legacy_base == "server.log"
    assert legacy_ext == ".log"

    # Modern pathlib.Path approach (operator overloading with /)
    modern_path = Path("var") / "log" / "app" / "server.log"
    modern_base = modern_path.name
    modern_dir_name = str(modern_path.parent)
    modern_stem = modern_path.stem
    modern_suffix = modern_path.suffix

    assert modern_base == "server.log"
    assert modern_stem == "server"
    assert modern_suffix == ".log"
    assert modern_path.parts[-1] == "server.log"

    print(f"  Legacy joined path: {legacy_file}")
    print(f"  Modern joined path: {modern_path}")
    print(f"  Stem: {modern_stem}, Extension: {modern_suffix}")


# ==============================================================================
# Question 2: Path Decomposition & Multi-Suffix Inspection
# ==============================================================================
def exercise_q2_path_decomposition() -> None:
    """
    Demonstrate deep decomposition of file paths: extracting parent directories,
    iterating through parent hierarchies, and inspecting complex extensions like .tar.gz.
    """
    print("\n=== Q2: Path Decomposition & Multi-Suffix Inspection ===")

    archive_path = Path("backup") / "2026" / "october" / "database_dump.tar.gz"

    # Extracting parts
    parts = archive_path.parts
    assert parts[-1] == "database_dump.tar.gz"

    # Stem and suffix behavior for multi-extension files
    primary_stem = archive_path.stem      # database_dump.tar
    single_suffix = archive_path.suffix    # .gz
    all_suffixes = archive_path.suffixes  # ['.tar', '.gz']

    assert primary_stem == "database_dump.tar"
    assert single_suffix == ".gz"
    assert all_suffixes == [".tar", ".gz"]

    # Full stem stripping (custom helper)
    full_stem = archive_path.name.split(".")[0]
    assert full_stem == "database_dump"

    # Traversing parents hierarchy
    parents = list(archive_path.parents)
    # parents[0] = backup/2026/october
    # parents[1] = backup/2026
    # parents[2] = backup
    # parents[3] = .
    assert len(parents) == 4
    assert parents[0].name == "october"
    assert parents[1].name == "2026"

    print(f"  File name:     {archive_path.name}")
    print(f"  Stem:          {primary_stem}")
    print(f"  All suffixes:  {all_suffixes}")
    print(f"  Parent depths: {[str(p) for p in parents]}")


# ==============================================================================
# Question 3: Absolute vs Relative Paths & Resolution
# ==============================================================================
def exercise_q3_absolute_relative_paths() -> None:
    """
    Illustrate checking for absolute paths, resolving relative paths to canonical
    absolute paths, and calculating relative paths between two distinct locations.
    """
    print("\n=== Q3: Absolute vs Relative Paths & Resolution ===")

    rel_path = Path("06_file_handling") / "q01_reading_files.py"
    assert not rel_path.is_absolute()

    # Resolving to canonical absolute path
    resolved_path = rel_path.resolve()
    assert resolved_path.is_absolute()
    assert resolved_path.name == "q01_reading_files.py"

    # Calculating relative distance between directories
    base_dir = Path("/home/user/projects/webapp/src").resolve()
    target_file = Path("/home/user/projects/webapp/config/settings.json").resolve()

    # relative_to works when target is a subpath of base.
    # When stepping sideways, we can compute common ancestors:
    common = Path(os.path.commonpath([str(base_dir), str(target_file)]))
    rel_from_base = Path(os.path.relpath(target_file, base_dir))

    # Path relative verification
    expected_rel = Path("..") / "config" / "settings.json"
    assert rel_from_base == expected_rel

    print(f"  Relative path:  {rel_path}")
    print(f"  Resolved path:  {resolved_path}")
    print(f"  Common base:    {common}")
    print(f"  Relative step:  {rel_from_base}")


# ==============================================================================
# Question 4: Directory Traversal with iterdir()
# ==============================================================================
def exercise_q4_directory_traversal() -> None:
    """
    Use Path.iterdir() to iterate over direct children of a directory,
    differentiating between regular files, directories, and checking existence.
    """
    print("\n=== Q4: Directory Traversal with iterdir() ===")

    temp_dir = tempfile.mkdtemp(prefix="path_iter_")
    root = Path(temp_dir)

    try:
        # Create nested test files and subfolders
        (root / "doc1.txt").write_text("Document 1", encoding="utf-8")
        (root / "doc2.md").write_text("# Markdown Doc", encoding="utf-8")
        (root / "subfolder").mkdir()
        (root / "subfolder" / "nested.txt").write_text("Nested", encoding="utf-8")

        # iterdir() iterates non-recursively
        children = list(root.iterdir())
        files = [p for p in children if p.is_file()]
        dirs = [p for p in children if p.is_dir()]

        assert len(files) == 2
        assert len(dirs) == 1
        assert any(p.name == "doc1.txt" for p in files)
        assert any(p.name == "doc2.md" for p in files)
        assert dirs[0].name == "subfolder"

        print(f"  Directory items found: {len(children)}")
        print(f"  Files: {[f.name for f in files]}")
        print(f"  Folders: {[d.name for d in dirs]}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 5: Pattern Matching and Globbing
# ==============================================================================
def exercise_q5_pattern_matching_glob() -> None:
    """
    Demonstrate glob() and recursive rglob() to discover files matching wildcard patterns
    and extension filters across deep directory trees.
    """
    print("\n=== Q5: Pattern Matching and Globbing ===")

    temp_dir = tempfile.mkdtemp(prefix="path_glob_")
    root = Path(temp_dir)

    try:
        # Build structure:
        # root/
        #   report_2026.csv
        #   report_2025.csv
        #   notes.txt
        #   logs/
        #     app_2026.log
        #     err_2026.log
        #     nested/
        #       summary_2026.csv
        (root / "report_2026.csv").write_text("a,b", encoding="utf-8")
        (root / "report_2025.csv").write_text("c,d", encoding="utf-8")
        (root / "notes.txt").write_text("notes", encoding="utf-8")
        nested_log_dir = root / "logs" / "nested"
        nested_log_dir.mkdir(parents=True)
        (root / "logs" / "app_2026.log").write_text("app log", encoding="utf-8")
        (root / "logs" / "err_2026.log").write_text("err log", encoding="utf-8")
        (nested_log_dir / "summary_2026.csv").write_text("e,f", encoding="utf-8")

        # 1. Non-recursive glob for csv files in root only
        root_csvs = sorted(p.name for p in root.glob("*.csv"))
        assert root_csvs == ["report_2025.csv", "report_2026.csv"]

        # 2. Recursive rglob for all csv files in entire tree
        all_csvs = sorted(p.name for p in root.rglob("*.csv"))
        assert all_csvs == ["report_2025.csv", "report_2026.csv", "summary_2026.csv"]

        # 3. Matching with wildcards in filename
        reports_2026 = sorted(p.name for p in root.rglob("*_2026.*"))
        assert reports_2026 == [
            "app_2026.log",
            "err_2026.log",
            "report_2026.csv",
            "summary_2026.csv",
        ]

        # 4. Path.match() method
        sample = root / "logs" / "app_2026.log"
        assert sample.match("*.log")
        assert sample.match("**/logs/*.log")
        assert not sample.match("*.csv")

        print(f"  Root CSVs:       {root_csvs}")
        print(f"  All CSVs:        {all_csvs}")
        print(f"  2026 Files:      {reports_2026}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 6: Path Normalization, Symlinks, and Expansions
# ==============================================================================
def exercise_q6_normalization_and_expansion() -> None:
    """
    Demonstrate resolving redundant dots ('.', '..'), expanding user home directories (~),
    and normalizing uncanonical path strings.
    """
    print("\n=== Q6: Path Normalization, Symlinks, and Expansions ===")

    # Redundant separator and navigation tokens
    messy_path_str = "folder/subfolder/../subfolder/./data//file.txt"
    normalized_os = os.path.normpath(messy_path_str)
    normalized_pathlib = Path(messy_path_str).resolve()

    # os.path.normpath cleans redundant segments textually without hitting the filesystem
    expected_clean_part = os.path.join("folder", "subfolder", "data", "file.txt")
    assert normalized_os == expected_clean_part

    # User home expansion
    home_dir = Path.home()
    tilde_path = Path("~/my_documents/notes.txt")
    expanded_path = tilde_path.expanduser()

    assert not tilde_path.is_absolute()
    assert expanded_path.is_absolute()
    assert str(expanded_path).startswith(str(home_dir))

    print(f"  Messy input:     {messy_path_str}")
    print(f"  Normpath output: {normalized_os}")
    print(f"  Expanded ~ path: {expanded_path}")


# ==============================================================================
# Question 7: Directory Tree Management (mkdir & rmdir)
# ==============================================================================
def exercise_q7_directory_management() -> None:
    """
    Explore safe recursive directory creation with Path.mkdir(parents=True, exist_ok=True)
    and controlled deletion.
    """
    print("\n=== Q7: Directory Tree Management ===")

    temp_dir = tempfile.mkdtemp(prefix="path_mkdir_")
    base = Path(temp_dir)

    try:
        nested_target = base / "level1" / "level2" / "level3" / "logs"
        assert not nested_target.exists()

        # Creating intermediate parents automatically
        nested_target.mkdir(parents=True, exist_ok=True)
        assert nested_target.is_dir()

        # Idempotent re-run with exist_ok=True
        nested_target.mkdir(parents=True, exist_ok=True)

        # Standard rmdir() only removes EMPTY directories
        nested_target.rmdir()
        assert not nested_target.exists()

        # Parent level3 still exists
        assert (base / "level1" / "level2" / "level3").exists()

        print(f"  Successfully created and cleaned directory tree: {nested_target}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 8: Direct Path Object I/O Operations
# ==============================================================================
def exercise_q8_direct_path_io() -> None:
    """
    Leverage Path's built-in file methods: write_text, read_text, write_bytes,
    read_bytes, touch, and unlink for clean, compact file management.
    """
    print("\n=== Q8: Direct Path Object I/O Operations ===")

    temp_dir = tempfile.mkdtemp(prefix="path_io_")
    root = Path(temp_dir)

    try:
        file_path = root / "config.ini"

        # 1. touch() creates empty file or updates mtime
        file_path.touch()
        assert file_path.is_file()
        assert file_path.stat().st_size == 0

        # 2. write_text() / read_text()
        file_path.write_text("[settings]\nenv = production\nport = 8080", encoding="utf-8")
        text_content = file_path.read_text(encoding="utf-8")
        assert "port = 8080" in text_content

        # 3. write_bytes() / read_bytes()
        binary_file = root / "blob.bin"
        payload = b"\x00\xff\xfe\xfd\x01\x02"
        binary_file.write_bytes(payload)
        read_payload = binary_file.read_bytes()
        assert read_payload == payload

        # 4. unlink() to delete
        assert binary_file.exists()
        binary_file.unlink()
        assert not binary_file.exists()

        print(f"  Read back written text length: {len(text_content)} chars")
        print(f"  Binary payload verified and unlinked successfully.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 9: Cross-Platform Pure Paths & Path Sanitization
# ==============================================================================
def exercise_q9_cross_platform_pure_paths() -> None:
    """
    Demonstrate PureWindowsPath and PurePosixPath for manipulating file paths
    belonging to other operating systems without performing actual filesystem lookups,
    and implement an unreserved path sanitizer.
    """
    print("\n=== Q9: Cross-Platform Pure Paths & Path Sanitization ===")

    # 1. Inspecting Windows path on any platform
    win_path = PureWindowsPath(r"C:\Users\Admin\Documents\Project\config.yaml")
    assert win_path.drive == "C:"
    assert win_path.root == "\\"
    assert win_path.stem == "config"
    assert win_path.as_posix() == "C:/Users/Admin/Documents/Project/config.yaml"

    # 2. Inspecting POSIX path on any platform
    posix_path = PurePosixPath("/etc/nginx/sites-available/default.conf")
    assert posix_path.root == "/"
    assert posix_path.parent == PurePosixPath("/etc/nginx/sites-available")
    assert posix_path.suffix == ".conf"

    # 3. Path Sanitizer: removes illegal characters across platforms
    def sanitize_filename(filename: str) -> str:
        # Invalid in Windows / NTFS filenames: < > : " / \ | ? * and ASCII 0-31
        invalid_chars = '<>:"/\\|?*'
        cleaned = "".join(c if c not in invalid_chars and ord(c) >= 32 else "_" for c in filename)
        # Strip trailing dots or spaces which Windows forbids
        cleaned = cleaned.strip(". ")
        return cleaned or "unnamed"

    dirty_name = 'Invoice: #1234/5 <FINAL>?.pdf'
    sanitized = sanitize_filename(dirty_name)
    assert sanitized == "Invoice_ #1234_5 _FINAL__.pdf"
    assert not any(c in sanitized for c in '<>:"/\\|?*')

    print(f"  PureWindowsPath as POSIX: {win_path.as_posix()}")
    print(f"  PurePosixPath parent:     {posix_path.parent}")
    print(f"  Sanitized Filename:       {sanitized}")


# ==============================================================================
# Question 10: Advanced Engine - Directory Tree Analyzer & Cataloger
# ==============================================================================
class DirectoryCataloger:
    """
    High-performance directory analyzer that traverses a filesystem tree,
    calculates hierarchical sizes, aggregates extension metrics, respects
    depth limits, and produces structured summaries.
    """

    def __init__(self, root_path: Path, max_depth: int = 5) -> None:
        self.root = root_path.resolve()
        self.max_depth = max_depth

    def analyze(self) -> dict:
        total_files = 0
        total_dirs = 0
        total_bytes = 0
        extension_counts: dict[str, int] = {}
        extension_bytes: dict[str, int] = {}

        def _traverse(current_path: Path, current_depth: int) -> None:
            nonlocal total_files, total_dirs, total_bytes

            if current_depth > self.max_depth:
                return

            try:
                entries = list(current_path.iterdir())
            except (PermissionError, OSError):
                return

            for entry in entries:
                if entry.is_dir():
                    total_dirs += 1
                    _traverse(entry, current_depth + 1)
                elif entry.is_file():
                    total_files += 1
                    try:
                        size = entry.stat().st_size
                    except OSError:
                        size = 0

                    total_bytes += size
                    ext = entry.suffix.lower() or "<no_ext>"
                    extension_counts[ext] = extension_counts.get(ext, 0) + 1
                    extension_bytes[ext] = extension_bytes.get(ext, 0) + size

        _traverse(self.root, 0)

        return {
            "root": str(self.root),
            "total_files": total_files,
            "total_dirs": total_dirs,
            "total_bytes": total_bytes,
            "extension_counts": extension_counts,
            "extension_bytes": extension_bytes,
        }


def exercise_q10_directory_cataloger_engine() -> None:
    """
    Demonstrate DirectoryCataloger on a synthetic multi-tier folder hierarchy.
    """
    print("\n=== Q10: Directory Cataloger Engine ===")

    temp_dir = tempfile.mkdtemp(prefix="path_catalog_")
    root = Path(temp_dir)

    try:
        # Construct synthetic project structure
        (root / "src").mkdir()
        (root / "src" / "main.py").write_text("print('hello')", encoding="utf-8")
        (root / "src" / "utils.py").write_text("def helper(): pass", encoding="utf-8")

        (root / "docs").mkdir()
        (root / "docs" / "index.md").write_text("# Welcome", encoding="utf-8")
        (root / "docs" / "api.md").write_text("# API Reference", encoding="utf-8")

        (root / "data").mkdir()
        (root / "data" / "dataset.csv").write_text("id,val\n1,100\n2,200", encoding="utf-8")
        (root / "LICENSE").write_text("MIT License", encoding="utf-8")

        cataloger = DirectoryCataloger(root, max_depth=3)
        metrics = cataloger.analyze()

        assert metrics["total_files"] == 6
        assert metrics["total_dirs"] == 3
        assert metrics["extension_counts"][".py"] == 2
        assert metrics["extension_counts"][".md"] == 2
        assert metrics["extension_counts"][".csv"] == 1
        assert metrics["extension_counts"]["<no_ext>"] == 1
        assert metrics["total_bytes"] > 0

        print(f"  Cataloged Root:   {metrics['root']}")
        print(f"  Total Files:      {metrics['total_files']}")
        print(f"  Total Dirs:       {metrics['total_dirs']}")
        print(f"  Total Bytes:      {metrics['total_bytes']}")
        print(f"  Extension Counts: {metrics['extension_counts']}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_path_fundamentals()
    exercise_q2_path_decomposition()
    exercise_q3_absolute_relative_paths()
    exercise_q4_directory_traversal()
    exercise_q5_pattern_matching_glob()
    exercise_q6_normalization_and_expansion()
    exercise_q7_directory_management()
    exercise_q8_direct_path_io()
    exercise_q9_cross_platform_pure_paths()
    exercise_q10_directory_cataloger_engine()

    print("\nAll 10 file path questions executed and asserted successfully!")
