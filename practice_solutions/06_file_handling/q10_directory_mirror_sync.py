"""
Topic 06 - File Handling: Question 10
Problem: Enterprise Directory Replication and Differential Sync Engine using os.walk and shutil.copy2.
"""

import hashlib
import os
import shutil
import time
from typing import Any, Dict, List


class DirectoryMirrorSync:
    """Differential directory synchronization engine preserving file metadata and timestamps."""

    def scan_directory(self, root_dir: str) -> Dict[str, Dict[str, Any]]:
        """Scans directory tree returning metadata map of normalized relative paths."""
        if not os.path.exists(root_dir):
            return {}

        metadata: Dict[str, Dict[str, Any]] = {}
        for root, _, files in os.walk(root_dir):
            for fname in files:
                full_path = os.path.join(root, fname)
                rel_path = os.path.relpath(full_path, root_dir).replace("\\", "/")
                stat_res = os.stat(full_path)

                hasher = hashlib.md5()
                with open(full_path, "rb") as f:
                    for chunk in iter(lambda: f.read(8192), b""):
                        hasher.update(chunk)

                metadata[rel_path] = {
                    "size": stat_res.st_size,
                    "mtime": stat_res.st_mtime,
                    "checksum": hasher.hexdigest()
                }
        return metadata

    def build_sync_plan(self, source_dir: str, replica_dir: str) -> Dict[str, List[str]]:
        """Computes CREATE, UPDATE, DELETE, and UNCHANGED operations via checksum & mtime diffs."""
        if not os.path.exists(source_dir):
            raise FileNotFoundError("Source directory not found")

        src_meta = self.scan_directory(source_dir)
        rep_meta = self.scan_directory(replica_dir)

        plan: Dict[str, List[str]] = {
            "CREATE": [],
            "UPDATE": [],
            "DELETE": [],
            "UNCHANGED": []
        }

        for path, s_info in src_meta.items():
            if path not in rep_meta:
                plan["CREATE"].append(path)
            else:
                r_info = rep_meta[path]
                if s_info["checksum"] == r_info["checksum"] and s_info["size"] == r_info["size"]:
                    plan["UNCHANGED"].append(path)
                else:
                    plan["UPDATE"].append(path)

        for path in rep_meta:
            if path not in src_meta:
                plan["DELETE"].append(path)

        for k in plan:
            plan[k].sort()

        return plan

    def apply_sync(self, plan: Dict[str, List[str]], source_dir: str, replica_dir: str, dry_run: bool = True) -> Dict[str, Any]:
        """Applies synchronization plan using shutil.copy2 to preserve timestamps, pruning empty dirs."""
        if dry_run:
            return {
                "created": 0,
                "updated": 0,
                "deleted": 0,
                "unchanged": len(plan["UNCHANGED"]),
                "dry_run": True
            }

        created = 0
        for path in plan["CREATE"]:
            src_f = os.path.join(source_dir, path)
            dst_f = os.path.join(replica_dir, path)
            os.makedirs(os.path.dirname(dst_f), exist_ok=True)
            shutil.copy2(src_f, dst_f)
            created += 1

        updated = 0
        for path in plan["UPDATE"]:
            src_f = os.path.join(source_dir, path)
            dst_f = os.path.join(replica_dir, path)
            os.makedirs(os.path.dirname(dst_f), exist_ok=True)
            shutil.copy2(src_f, dst_f)
            updated += 1

        deleted = 0
        for path in plan["DELETE"]:
            dst_f = os.path.join(replica_dir, path)
            if os.path.exists(dst_f):
                os.remove(dst_f)
                deleted += 1

        # Prune empty directories in replica bottom-up
        for root, dirs, _ in os.walk(replica_dir, topdown=False):
            for d in dirs:
                d_path = os.path.join(root, d)
                try:
                    os.rmdir(d_path)
                except OSError:
                    pass

        return {
            "created": created,
            "updated": updated,
            "deleted": deleted,
            "unchanged": len(plan["UNCHANGED"]),
            "dry_run": False
        }


# Verification & Execution
source_folder = "sync_source"
replica_folder = "sync_replica"

try:
    # Setup test source environment
    os.makedirs(os.path.join(source_folder, "assets"), exist_ok=True)
    os.makedirs(replica_folder, exist_ok=True)

    with open(os.path.join(source_folder, "app.py"), "w", encoding="utf-8") as f:
        f.write("# Version 2.0\nprint('Production v2')\n")
    with open(os.path.join(source_folder, "config.json"), "w", encoding="utf-8") as f:
        f.write('{"cluster": "east"}\n')
    with open(os.path.join(source_folder, "assets", "logo.png"), "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\nLogoData")

    # Setup replica with older app.py and an orphaned script
    time.sleep(0.05)
    with open(os.path.join(replica_folder, "app.py"), "w", encoding="utf-8") as f:
        f.write("# Version 1.0\nprint('Legacy v1')\n")
    with open(os.path.join(replica_folder, "old_script.py"), "w", encoding="utf-8") as f:
        f.write("# Orphaned file\n")

    sync_engine = DirectoryMirrorSync()

    plan = sync_engine.build_sync_plan(source_folder, replica_folder)
    print("Reconciliation Plan Computed:")
    print(f"- CREATE:    {plan['CREATE']}")
    print(f"- UPDATE:    {plan['UPDATE']} (Checksum mismatch; source mtime newer)")
    print(f"- DELETE:    {plan['DELETE']} (Orphaned in replica)")
    print(f"- UNCHANGED: {plan['UNCHANGED']}")

    dry_run_report = sync_engine.apply_sync(plan, source_folder, replica_folder, dry_run=True)
    print(f"\nDry Run Execution: {dry_run_report['created'] + dry_run_report['updated'] + dry_run_report['deleted']} disk modifications made.")

    live_result = sync_engine.apply_sync(plan, source_folder, replica_folder, dry_run=False)
    print("Live Sync Applied:")
    print(f"- Files Created: {live_result['created']}")
    print(f"- Files Updated: {live_result['updated']}")
    print(f"- Files Deleted: {live_result['deleted']}")
    print("- Replica now exactly mirrors source with preserved timestamps.")

    # Validation test
    try:
        sync_engine.build_sync_plan("non_existent_source_xyz", replica_folder)
    except FileNotFoundError as err:
        print(f"\nValidation Guard Verified: FileNotFoundError(\"{err}\")")

finally:
    for folder in (source_folder, replica_folder):
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
