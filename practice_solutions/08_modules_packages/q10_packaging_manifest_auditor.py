"""
Question 10: Enterprise Python Environment Auditor & Packaging Manifest Generator
Topic: Modules and Packages

Key Concepts Tested:
- Virtual environment detection & introspection (sys.prefix vs sys.base_prefix, VIRTUAL_ENV)
- Robust parsing of requirements.txt files with version specifiers and warnings
- PEP 508 / PEP 621 pyproject.toml manifest generation with strict validation
- Installed dependency verification (satisfied, mismatched, missing)
"""

import sys
import os
import re
from typing import Dict, List, Optional, Any


class PythonEnvPackagingAuditor:
    """
    Auditor for inspecting Python virtual environments, parsing dependency specifications,
    and generating standard PEP 621 pyproject.toml manifests.
    """

    PEP_508_NAME_PATTERN = re.compile(r"^([a-z0-9]|[a-z0-9][a-z0-9._-]*[a-z0-9])$")
    SPECIFIER_PATTERN = re.compile(r"^([a-zA-Z0-9_\-\.]+)\s*(==|>=|<=|~=|!=|<|>)?\s*([0-9a-zA-Z_\.\-\*]*)$")

    def inspect_virtual_environment(self) -> Dict[str, Any]:
        """
        Programmatically detects whether the runtime is executing inside an isolated virtual environment.
        """
        base_prefix = getattr(sys, "base_prefix", sys.prefix)
        is_virtualenv = sys.prefix != base_prefix or bool(os.environ.get("VIRTUAL_ENV"))

        return {
            "is_virtualenv": is_virtualenv,
            "prefix_path": sys.prefix,
            "base_prefix_path": base_prefix,
            "python_executable": sys.executable,
            "virtual_env_variable": os.environ.get("VIRTUAL_ENV"),
        }

    def parse_requirements(self, raw_text: str) -> List[Dict[str, Any]]:
        """
        Parses requirements.txt lines, stripping comments and inline whitespace.
        Extracts package name, version operator, version spec, and pinned status.
        Flags unpinned dependencies with a warning.
        """
        parsed_entries = []

        for line_num, line in enumerate(raw_text.splitlines(), start=1):
            # Strip comments and whitespace
            clean_line = line.split("#")[0].strip()
            if not clean_line:
                continue

            # Strip options like --index-url if present
            if clean_line.startswith("-"):
                continue

            match = self.SPECIFIER_PATTERN.match(clean_line)
            if not match:
                continue

            pkg_name, operator, version_spec = match.groups()
            pkg_name = pkg_name.strip().lower()
            operator = operator.strip() if operator else None
            version_spec = version_spec.strip() if version_spec else None

            is_pinned = operator == "=="
            warning = "Warning: Unpinned!" if operator is None else None

            parsed_entries.append({
                "package_name": pkg_name,
                "operator": operator,
                "version_spec": version_spec,
                "is_pinned": is_pinned,
                "warning": warning,
            })

        return parsed_entries

    def build_pyproject_toml(
        self,
        project_name: str,
        version: str,
        dependencies: List[str],
        build_backend: str = "setuptools.build_meta",
    ) -> str:
        """
        Generates modern PEP 621 compliant pyproject.toml content.
        Validates project name against PEP 508 rules.
        """
        # Validate project name
        if not self.PEP_508_NAME_PATTERN.match(project_name):
            raise ValueError(f"Invalid PEP 508 package name: '{project_name}'")

        dep_lines = "\n".join(f'    "{dep}",' for dep in dependencies)

        toml_content = f"""[build-system]
requires = ["setuptools>=61.0"]
build-backend = "{build_backend}"

[project]
name = "{project_name}"
version = "{version}"
dependencies = [
{dep_lines}
]
"""
        return toml_content

    @staticmethod
    def _parse_version(v_str: str) -> List[int]:
        """Simple numeric version parser for comparison."""
        parts = []
        for segment in re.split(r"[.\-]", v_str):
            if segment.isdigit():
                parts.append(int(segment))
        return parts

    def audit_installed_versions(
        self,
        installed_map: Dict[str, str],
        required_specs: List[Dict[str, Any]],
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Compares installed packages against required specifications.
        Categorizes into satisfied, mismatched, and missing.
        """
        audit_result = {
            "satisfied": [],
            "mismatched": [],
            "missing": [],
        }

        # Normalize installed map keys
        normalized_installed = {k.lower(): v for k, v in installed_map.items()}

        for spec in required_specs:
            pkg = spec["package_name"]
            op = spec["operator"]
            target_ver = spec["version_spec"]

            if pkg not in normalized_installed:
                audit_result["missing"].append({
                    "package": pkg,
                    "required": f"{op or ''}{target_ver or 'any'}",
                })
                continue

            installed_ver = normalized_installed[pkg]
            if op is None or target_ver is None:
                audit_result["satisfied"].append({
                    "package": pkg,
                    "installed": installed_ver,
                    "required": "any",
                })
                continue

            inst_parts = self._parse_version(installed_ver)
            target_parts = self._parse_version(target_ver)

            is_match = False
            if op == "==":
                is_match = inst_parts == target_parts
            elif op == ">=":
                is_match = inst_parts >= target_parts
            elif op == "<=":
                is_match = inst_parts <= target_parts
            elif op == ">":
                is_match = inst_parts > target_parts
            elif op == "<":
                is_match = inst_parts < target_parts
            elif op == "!=":
                is_match = inst_parts != target_parts
            else:
                is_match = True

            if is_match:
                audit_result["satisfied"].append({
                    "package": pkg,
                    "installed": installed_ver,
                    "required": f"{op}{target_ver}",
                })
            else:
                audit_result["mismatched"].append({
                    "package": pkg,
                    "installed": installed_ver,
                    "required": f"{op}{target_ver}",
                })

        return audit_result


if __name__ == "__main__":
    auditor = PythonEnvPackagingAuditor()

    print("=== 1. Virtual Environment Introspection ===")
    env_info = auditor.inspect_virtual_environment()
    print(f"Is Virtualenv:       {env_info['is_virtualenv']}")
    print(f"Active Interpreter:  {env_info['python_executable']}")
    print(f"Virtual Env Root:    {env_info['prefix_path']}")
    print(f"Base System Root:    {env_info['base_prefix_path']}")
    print(f"VIRTUAL_ENV Env Var: {env_info['virtual_env_variable']}")

    print("\n=== 2. Strict Requirements Parser ===")
    sample_reqs = """
    # Core Production Dependencies
    fastapi==0.110.0
    uvicorn>=0.28.0
    pydantic  # Warning: unpinned!
    requests~=2.31.0
    """
    parsed_reqs = auditor.parse_requirements(sample_reqs)
    for idx, req in enumerate(parsed_reqs, 1):
        status_note = f"({req['warning']})" if req["warning"] else f"Pinned: {req['is_pinned']}"
        print(f"{idx}. Package: {req['package_name']:<12} | Op: {str(req['operator']):<4} | Version: {str(req['version_spec']):<8} | {status_note}")

    print("\n=== 3. PEP 621 pyproject.toml Generation ===")
    manifest = auditor.build_pyproject_toml(
        project_name="cloud-telemetry-service",
        version="0.1.0",
        dependencies=["fastapi>=0.110.0", "uvicorn>=0.28.0", "pydantic>=2.5.0"],
    )
    print(manifest)

    print("=== 4. Dependency Compatibility Verification ===")
    mock_installed = {
        "fastapi": "0.110.0",
        "uvicorn": "0.25.0",  # Mismatched (< 0.28.0)
        "pydantic": "2.6.1",
        # 'requests' is missing
    }
    audit_results = auditor.audit_installed_versions(mock_installed, parsed_reqs)
    print(f"Satisfied:  {audit_results['satisfied']}")
    print(f"Mismatched: {audit_results['mismatched']}")
    print(f"Missing:    {audit_results['missing']}")

    print("\n=== 5. PEP 508 Project Name Validation Edge Case ===")
    try:
        auditor.build_pyproject_toml("Invalid Project Name!", "1.0.0", [])
    except ValueError as e:
        print(f"Caught expected error for invalid name: {e}")
