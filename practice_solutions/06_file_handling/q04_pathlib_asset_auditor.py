"""
Topic 06 - File Handling: Question 4
Problem: Filesystem Path Inspection, Audit, and Traversal Guard via pathlib.Path.
"""

import shutil
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union


class ProjectAssetAuditor:
    """Audits directory assets and enforces path traversal security using pathlib.Path."""

    def __init__(self, root_directory: Union[str, Path]):
        self.root: Path = Path(root_directory).resolve()
        if not self.root.is_dir():
            raise NotADirectoryError(f"Path '{self.root}' is not a valid directory")

    def audit_extensions(self, target_extensions: Tuple[str, ...]) -> List[Dict[str, Any]]:
        """Recursively audits regular files matching given suffixes."""
        assets = []
        for file in self.root.rglob("*"):
            if file.is_file() and file.suffix.lower() in target_extensions:
                assets.append({
                    "relative_path": file.relative_to(self.root).as_posix(),
                    "stem": file.stem,
                    "suffix": file.suffix,
                    "parent_folder": file.parent.name,
                    "size_bytes": file.stat().st_size
                })
        return sorted(assets, key=lambda x: x["relative_path"])

    def generate_backup_path(self, source_file: Union[str, Path], backup_root: Union[str, Path]) -> Path:
        """Computes mirror destination path with '.bak' appended to filename."""
        source_path = Path(source_file).resolve()
        relative_subpath = source_path.relative_to(self.root)
        backup_target = Path(backup_root) / relative_subpath.parent / f"{relative_subpath.name}.bak"
        return backup_target

    def safe_resolve_subpath(self, untrusted_relative_path: str) -> Path:
        """Guards against directory traversal attacks (e.g. '../../etc/passwd')."""
        resolved_target = (self.root / untrusted_relative_path).resolve()
        try:
            resolved_target.relative_to(self.root)
        except ValueError:
            raise PermissionError("Path traversal attack detected")
        return resolved_target


# Verification & Execution
temp_workspace = Path("./workspace_test")
project_dir = temp_workspace / "sample_project"

try:
    # Set up mock project structure
    utils_dir = project_dir / "utils"
    utils_dir.mkdir(parents=True, exist_ok=True)

    helper_file = utils_dir / "helper.py"
    helper_file.write_text("def assist():\n    return 'OK'\n", encoding="utf-8")

    config_file = project_dir / "config.txt"
    config_file.write_text("DEBUG=True\nPORT=8080\n", encoding="utf-8")

    auditor = ProjectAssetAuditor(project_dir)
    print(f"Auditor Root: {auditor.root.as_posix()}")

    matched_assets = auditor.audit_extensions(target_extensions=(".py", ".txt"))
    print(f"Found {len(matched_assets)} matching assets:")
    for idx, asset in enumerate(matched_assets, 1):
        print(f"{idx}. {asset['relative_path']} | Size: {asset['size_bytes']} bytes | Parent: {asset['parent_folder']}")

    backup_target = auditor.generate_backup_path(helper_file, Path("./backups"))
    print(f"\nBackup Destination: {backup_target.as_posix()}")

    # Traversal exploit simulation
    try:
        auditor.safe_resolve_subpath("../../outside_secret.key")
    except PermissionError as err:
        print("Caught Security Violation:", err)

finally:
    if temp_workspace.exists():
        shutil.rmtree(temp_workspace, ignore_errors=True)
