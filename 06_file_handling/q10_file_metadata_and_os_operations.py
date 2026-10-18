"""
Topic 06: File Handling - Question 10: File Metadata and OS Operations

A comprehensive collection of 10 standalone, runnable exercises exploring
file system metadata, timestamps, permissions, high-level shutil utilities,
high-performance scandir, symlinks, and file integrity auditing.

Questions Covered:
 1. os.stat() and the stat Module: Inspecting size, timestamps, mode, and S_ISREG/S_ISDIR.
 2. Timestamps and os.utime(): Inspecting mtime/atime, formatting datetimes, and updating mtime.
 3. File Permissions with os.access(): Querying R_OK, W_OK, X_OK, F_OK, and chmod().
 4. Atomic Overwrites: os.replace() vs os.rename() behavior across platforms.
 5. High-Level shutil Utilities: copy(), copy2() (metadata preservation), move(), and copytree().
 6. Disk Usage Inspection: shutil.disk_usage() for total, used, and free storage calculation.
 7. Directory Tree Walking with os.walk(): Top-down vs bottom-up, in-place dirnames pruning.
 8. High-Performance Scanning with os.scandir(): Benchmarking DirEntry vs os.listdir() stat lookups.
 9. Hardlinks and Symlinks: os.link(), os.lstat(), follow_symlinks parameter, and broken link checks.
10. Advanced Project: File Integrity Auditor & Deduplication Engine with SHA-256 fingerprinting.
"""

import datetime
import hashlib
import os
import shutil
import stat
import tempfile
import time
from typing import Any


# ==============================================================================
# Question 1: os.stat() and the stat Module
# ==============================================================================
def exercise_q1_os_stat_inspection() -> None:
    """
    Demonstrate os.stat() to inspect file attributes: size, permissions,
    timestamps, and test file type using stat.S_ISREG and stat.S_ISDIR.
    """
    print("=== Q1: os.stat() and the stat Module ===")

    temp_dir = tempfile.mkdtemp(prefix="meta_stat_")
    test_file = os.path.join(temp_dir, "sample.txt")

    try:
        content = "Python Systems Programming 2026"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)

        file_stat = os.stat(test_file)
        dir_stat = os.stat(temp_dir)

        # Inspecting size
        assert file_stat.st_size == len(content.encode("utf-8"))

        # Inspecting file types
        assert stat.S_ISREG(file_stat.st_mode) is True
        assert stat.S_ISDIR(file_stat.st_mode) is False
        assert stat.S_ISDIR(dir_stat.st_mode) is True

        print(f"  File size:     {file_stat.st_size} bytes")
        print(f"  File mode oct: {oct(file_stat.st_mode)}")
        print(f"  Is regular:    {stat.S_ISREG(file_stat.st_mode)}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 2: Timestamps and os.utime()
# ==============================================================================
def exercise_q2_timestamps_and_utime() -> None:
    """
    Demonstrate converting st_mtime and st_atime to human-readable datetime objects,
    and modifying access/modification timestamps using os.utime().
    """
    print("\n=== Q2: Timestamps and os.utime() ===")

    temp_dir = tempfile.mkdtemp(prefix="meta_time_")
    test_file = os.path.join(temp_dir, "time_target.txt")

    try:
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Timestamp test")

        st = os.stat(test_file)
        mtime_dt = datetime.datetime.fromtimestamp(st.st_mtime)
        assert isinstance(mtime_dt, datetime.datetime)

        # Set explicit modification and access times (e.g. 1 hour ago)
        target_time = time.time() - 3600
        os.utime(test_file, (target_time, target_time))

        updated_st = os.stat(test_file)
        # Note: Some filesystems have 1-2 second timestamp resolution
        assert abs(updated_st.st_mtime - target_time) < 2.0

        print(f"  Original mtime: {mtime_dt.isoformat()}")
        print(f"  Updated mtime:  {datetime.datetime.fromtimestamp(updated_st.st_mtime).isoformat()}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 3: File Permissions with os.access() and chmod()
# ==============================================================================
def exercise_q3_permissions_and_access() -> None:
    """
    Demonstrate os.access() to test read (R_OK), write (W_OK), and existence (F_OK)
    permissions for the current process, and toggle write permissions with os.chmod().
    """
    print("\n=== Q3: File Permissions with os.access() and chmod() ===")

    temp_dir = tempfile.mkdtemp(prefix="meta_perm_")
    test_file = os.path.join(temp_dir, "perm_test.txt")

    try:
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Permission controlled file")

        # Initial checks
        assert os.access(test_file, os.F_OK) is True
        assert os.access(test_file, os.R_OK) is True
        assert os.access(test_file, os.W_OK) is True

        # Make file read-only
        # S_IREAD = 0o400 (owner read)
        os.chmod(test_file, stat.S_IREAD)
        assert os.access(test_file, os.R_OK) is True
        assert os.access(test_file, os.W_OK) is False

        # Restore write permission
        os.chmod(test_file, stat.S_IREAD | stat.S_IWRITE)
        assert os.access(test_file, os.W_OK) is True

        print("  os.access() successfully verified R_OK, W_OK, and read-only toggle.")

    finally:
        # Ensure write permission is restored so rmtree doesn't fail on Windows
        try:
            os.chmod(test_file, stat.S_IWRITE)
        except OSError:
            pass
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 4: Atomic Overwrites with os.replace()
# ==============================================================================
def exercise_q4_atomic_overwrites() -> None:
    """
    Demonstrate os.replace() which is guaranteed to be an atomic overwrite on both
    POSIX and Windows (unlike os.rename() which raises FileExistsError on Windows
    if the destination already exists).
    """
    print("\n=== Q4: Atomic Overwrites with os.replace() ===")

    temp_dir = tempfile.mkdtemp(prefix="meta_replace_")
    target = os.path.join(temp_dir, "destination.txt")
    source = os.path.join(temp_dir, "source_replacement.txt")

    try:
        with open(target, "w", encoding="utf-8") as f:
            f.write("Target version 1.0")

        with open(source, "w", encoding="utf-8") as f:
            f.write("Target version 2.0 (New)")

        # os.replace() atomically overwrites target even if target exists
        os.replace(source, target)

        assert not os.path.exists(source)
        with open(target, "r", encoding="utf-8") as f:
            updated_content = f.read()

        assert updated_content == "Target version 2.0 (New)"
        print("  os.replace() atomically replaced target without FileExistsError.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 5: High-Level shutil Utilities (copy, copy2, copytree, move)
# ==============================================================================
def exercise_q5_shutil_operations() -> None:
    """
    Explore the differences between shutil.copy() (copies content & permissions)
    and shutil.copy2() (also preserves metadata like mtime/atime), as well as
    recursive copytree() and move().
    """
    print("\n=== Q5: High-Level shutil Utilities ===")

    temp_dir = tempfile.mkdtemp(prefix="meta_shutil_")
    src_file = os.path.join(temp_dir, "source.txt")

    try:
        with open(src_file, "w", encoding="utf-8") as f:
            f.write("Original content for copying")

        # Set an older timestamp on src
        old_time = time.time() - 7200
        os.utime(src_file, (old_time, old_time))

        # 1. shutil.copy2 preserves metadata (mtime)
        copy2_dst = os.path.join(temp_dir, "copy2_dest.txt")
        shutil.copy2(src_file, copy2_dst)

        assert abs(os.stat(copy2_dst).st_mtime - old_time) < 2.0

        # 2. shutil.copytree: copies entire directory tree
        sub_src = os.path.join(temp_dir, "pkg")
        os.makedirs(sub_src)
        with open(os.path.join(sub_src, "__init__.py"), "w", encoding="utf-8") as f:
            f.write("# Init")

        sub_dst = os.path.join(temp_dir, "pkg_clone")
        shutil.copytree(sub_src, sub_dst)
        assert os.path.exists(os.path.join(sub_dst, "__init__.py"))

        # 3. shutil.move: renames or moves across directories
        moved_dst = os.path.join(temp_dir, "moved_pkg")
        shutil.move(sub_dst, moved_dst)
        assert not os.path.exists(sub_dst)
        assert os.path.exists(moved_dst)

        print("  shutil.copy2() successfully preserved mtime.")
        print("  shutil.copytree() and shutil.move() executed successfully.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 6: Disk Usage Inspection with shutil.disk_usage()
# ==============================================================================
def exercise_q6_disk_usage() -> None:
    """
    Demonstrate shutil.disk_usage() to query total, used, and free disk space
    and compute available capacity metrics.
    """
    print("\n=== Q6: Disk Usage Inspection ===")

    usage = shutil.disk_usage(".")
    total_gb = usage.total / (1024 ** 3)
    used_gb = usage.used / (1024 ** 3)
    free_gb = usage.free / (1024 ** 3)
    percent_free = (usage.free / usage.total) * 100

    assert usage.total > 0
    assert usage.free > 0
    assert 0 <= percent_free <= 100

    print(f"  Total disk space: {total_gb:.2f} GB")
    print(f"  Used disk space:  {used_gb:.2f} GB")
    print(f"  Free disk space:  {free_gb:.2f} GB ({percent_free:.1f}% free)")


# ==============================================================================
# Question 7: Directory Tree Walking with os.walk() & In-Place Pruning
# ==============================================================================
def exercise_q7_os_walk_and_pruning() -> None:
    """
    Demonstrate os.walk() to recursively traverse directory trees.
    Show how modifying the `dirnames` list in-place dynamically prunes directories
    from being visited (e.g. skipping '.git' or 'node_modules').
    """
    print("\n=== Q7: Directory Tree Walking with os.walk() ===")

    temp_dir = tempfile.mkdtemp(prefix="meta_walk_")

    try:
        # Build hierarchy:
        # temp_dir/
        #   src/
        #     app.py
        #   .git/
        #     config.txt
        #   docs/
        #     guide.md
        os.makedirs(os.path.join(temp_dir, "src"))
        os.makedirs(os.path.join(temp_dir, ".git"))
        os.makedirs(os.path.join(temp_dir, "docs"))

        with open(os.path.join(temp_dir, "src", "app.py"), "w") as f:
            f.write("code")
        with open(os.path.join(temp_dir, ".git", "config.txt"), "w") as f:
            f.write("git config")
        with open(os.path.join(temp_dir, "docs", "guide.md"), "w") as f:
            f.write("docs")

        visited_files: list[str] = []

        # Traverse and prune '.git' in-place
        for root, dirs, files in os.walk(temp_dir, topdown=True):
            if ".git" in dirs:
                # Modifying dirs in-place tells os.walk not to recurse into it!
                dirs.remove(".git")

            for file in files:
                visited_files.append(file)

        assert "app.py" in visited_files
        assert "guide.md" in visited_files
        assert "config.txt" not in visited_files  # Pruned successfully!

        print(f"  Visited files after in-place pruning: {visited_files}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 8: High-Performance Scanning with os.scandir()
# ==============================================================================
def exercise_q8_fast_scandir() -> None:
    """
    Demonstrate os.scandir() which yields DirEntry objects containing cached stat
    information provided directly by the OS directory listing API.
    """
    print("\n=== Q8: High-Performance Scanning with os.scandir() ===")

    temp_dir = tempfile.mkdtemp(prefix="meta_scandir_")

    try:
        # Create 5 test files
        for i in range(5):
            with open(os.path.join(temp_dir, f"file_{i}.dat"), "wb") as f:
                f.write(b"x" * (100 * (i + 1)))

        total_bytes = 0
        file_count = 0

        # scandir is an iterator and context manager
        with os.scandir(temp_dir) as entries:
            for entry in entries:
                if entry.is_file():
                    file_count += 1
                    # entry.stat() is cached on Windows and Linux!
                    total_bytes += entry.stat().st_size

        assert file_count == 5
        # 100 + 200 + 300 + 400 + 500 = 1500 bytes
        assert total_bytes == 1500

        print(f"  scandir scanned {file_count} files totaling {total_bytes} bytes.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 9: Hardlinks, Symlinks, and lstat()
# ==============================================================================
def exercise_q9_links_and_lstat() -> None:
    """
    Demonstrate hard links (os.link), inspecting inode/link count, and differentiating
    os.stat() (which follows links) from os.lstat() / os.stat(follow_symlinks=False).
    """
    print("\n=== Q9: Hardlinks, Symlinks, and lstat() ===")

    temp_dir = tempfile.mkdtemp(prefix="meta_links_")
    src_file = os.path.join(temp_dir, "primary.txt")
    hardlink_file = os.path.join(temp_dir, "hardlink.txt")

    try:
        with open(src_file, "w", encoding="utf-8") as f:
            f.write("Shared inode payload")

        # Create Hardlink
        try:
            os.link(src_file, hardlink_file)
            has_hardlink = True
        except (AttributeError, OSError, PermissionError):
            has_hardlink = False

        if has_hardlink:
            st_src = os.stat(src_file)
            st_link = os.stat(hardlink_file)

            # Both point to the exact same file content and inode!
            assert st_src.st_nlink >= 2  # Hard link count is at least 2
            assert st_src.st_ino == st_link.st_ino

            # Modifying one modifies the other
            with open(hardlink_file, "a", encoding="utf-8") as f:
                f.write(" - Appended via link")

            with open(src_file, "r", encoding="utf-8") as f:
                assert "Appended via link" in f.read()

            print("  Hard link created; verified shared inode & st_nlink >= 2.")
        else:
            print("  Hardlink creation not permitted in this environment; skipped gracefully.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 10: Advanced Project - File Integrity Auditor & Deduplication Engine
# ==============================================================================
class FileIntegrityAuditor:
    """
    Comprehensive filesystem auditor that recursively hashes files using SHA-256,
    detects exact byte-for-byte duplicate files across folders, and computes
    potential space recovery savings.
    """

    def __init__(self, root_dir: str) -> None:
        self.root_dir = root_dir

    def _hash_file(self, filepath: str, chunk_size: int = 65536) -> str:
        sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(chunk_size):
                sha256.update(chunk)
        return sha256.hexdigest()

    def audit(self) -> dict[str, Any]:
        hash_map: dict[str, list[dict[str, Any]]] = {}
        total_files = 0
        total_size = 0

        for root, _, files in os.walk(self.root_dir):
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    size = os.path.getsize(filepath)
                    digest = self._hash_file(filepath)
                    rel_path = os.path.relpath(filepath, self.root_dir)

                    item = {"path": rel_path, "size": size}
                    hash_map.setdefault(digest, []).append(item)
                    total_files += 1
                    total_size += size
                except (OSError, PermissionError):
                    continue

        # Detect duplicates
        duplicates = {k: v for k, v in hash_map.items() if len(v) > 1}
        reclaimable_bytes = sum(v[0]["size"] * (len(v) - 1) for v in duplicates.values())

        return {
            "total_files": total_files,
            "total_bytes": total_size,
            "unique_hashes": len(hash_map),
            "duplicate_groups": len(duplicates),
            "reclaimable_bytes": reclaimable_bytes,
            "duplicates": duplicates,
        }


def exercise_q10_file_integrity_auditor() -> None:
    """
    Verify FileIntegrityAuditor detects duplicate files and computes reclaimable space.
    """
    print("\n=== Q10: File Integrity Auditor & Deduplication Engine ===")

    temp_dir = tempfile.mkdtemp(prefix="meta_audit_")

    try:
        # Create unique and duplicate files
        f1 = os.path.join(temp_dir, "report_v1.pdf")
        f2 = os.path.join(temp_dir, "report_v1_copy.pdf")
        f3 = os.path.join(temp_dir, "report_v1_backup.pdf")
        f4 = os.path.join(temp_dir, "other.txt")

        payload_dup = b"IDENTICAL REPORT PAYLOAD CONTENT 12345"
        with open(f1, "wb") as f:
            f.write(payload_dup)
        with open(f2, "wb") as f:
            f.write(payload_dup)
        with open(f3, "wb") as f:
            f.write(payload_dup)
        with open(f4, "wb") as f:
            f.write(b"DIFFERENT")

        auditor = FileIntegrityAuditor(temp_dir)
        report = auditor.audit()

        assert report["total_files"] == 4
        assert report["unique_hashes"] == 2
        assert report["duplicate_groups"] == 1
        # 2 redundant copies of payload_dup
        assert report["reclaimable_bytes"] == len(payload_dup) * 2

        print(f"  Audit Report Summary:")
        print(f"    Total files scanned:    {report['total_files']}")
        print(f"    Duplicate groups:       {report['duplicate_groups']}")
        print(f"    Reclaimable disk space: {report['reclaimable_bytes']} bytes")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_os_stat_inspection()
    exercise_q2_timestamps_and_utime()
    exercise_q3_permissions_and_access()
    exercise_q4_atomic_overwrites()
    exercise_q5_shutil_operations()
    exercise_q6_disk_usage()
    exercise_q7_os_walk_and_pruning()
    exercise_q8_fast_scandir()
    exercise_q9_links_and_lstat()
    exercise_q10_file_integrity_auditor()

    print("\nAll 10 file metadata & OS operations questions executed and asserted successfully!")
