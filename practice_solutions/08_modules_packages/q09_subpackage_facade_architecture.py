"""
Question 9: Multi-Tiered Package Architecture & Facade Pattern
Topic: Modules and Packages

Key Concepts Tested:
- Package layout with sub-packages (__init__.py)
- Inter-subpackage relative imports (from ..subpkg import module)
- Top-level Facade API masking complex internal module hierarchies
- __all__ export control at package level
- Package reflection (inspecting __path__, __file__, __package__)
- Relative import caveat when executed as __main__
"""

import sys
import os
import shutil
import tempfile
import importlib
from typing import Any, Dict, List


def create_mock_package_structure(root_dir: str) -> str:
    """
    Creates a physical directory tree representing 'analytics_core':

    analytics_core/
      __init__.py
      ingestion/
        __init__.py
        loader.py
      transform/
        __init__.py
        cleaner.py
      reporting/
        __init__.py
        formatter.py
    """
    pkg_root = os.path.join(root_dir, "analytics_core")
    os.makedirs(os.path.join(pkg_root, "ingestion"), exist_ok=True)
    os.makedirs(os.path.join(pkg_root, "transform"), exist_ok=True)
    os.makedirs(os.path.join(pkg_root, "reporting"), exist_ok=True)

    # 1. transform/cleaner.py
    cleaner_code = '''"""Data transformation and cleaning utilities."""

def sanitize_dataset(raw_data: list) -> list:
    """Strips whitespace, converts non-nulls, filters out corrupt records."""
    cleaned = []
    for item in raw_data:
        if isinstance(item, dict) and "val" in item and item["val"] is not None:
            cleaned.append({"id": item.get("id"), "val": round(float(item["val"]), 2)})
    return cleaned
'''
    with open(os.path.join(pkg_root, "transform", "cleaner.py"), "w", encoding="utf-8") as f:
        f.write(cleaner_code)

    with open(os.path.join(pkg_root, "transform", "__init__.py"), "w", encoding="utf-8") as f:
        f.write('from .cleaner import sanitize_dataset\n__all__ = ["sanitize_dataset"]\n')

    # 2. ingestion/loader.py (Demonstrates relative import from sibling sub-package: ..transform.cleaner)
    loader_code = '''"""Data ingestion utilities."""
from ..transform.cleaner import sanitize_dataset

def fetch_records(raw_source: list) -> list:
    """Ingests raw records and applies initial sanitization via sibling package."""
    return sanitize_dataset(raw_source)
'''
    with open(os.path.join(pkg_root, "ingestion", "loader.py"), "w", encoding="utf-8") as f:
        f.write(loader_code)

    with open(os.path.join(pkg_root, "ingestion", "__init__.py"), "w", encoding="utf-8") as f:
        f.write('from .loader import fetch_records\n__all__ = ["fetch_records"]\n')

    # 3. reporting/formatter.py
    formatter_code = '''"""Report formatting engine."""

def generate_report(dataset: list, title: str = "Pipeline Summary") -> dict:
    total_val = sum(r["val"] for r in dataset)
    avg_val = total_val / len(dataset) if dataset else 0.0
    return {
        "title": title,
        "record_count": len(dataset),
        "total": round(total_val, 2),
        "average": round(avg_val, 2),
    }
'''
    with open(os.path.join(pkg_root, "reporting", "formatter.py"), "w", encoding="utf-8") as f:
        f.write(formatter_code)

    with open(os.path.join(pkg_root, "reporting", "__init__.py"), "w", encoding="utf-8") as f:
        f.write('from .formatter import generate_report\n__all__ = ["generate_report"]\n')

    # 4. Top-level analytics_core/__init__.py (Facade API)
    facade_code = '''"""
analytics_core - Unified facade for ingestion, transformation, and reporting.
Hides internal module paths from consumers.
"""
from .ingestion.loader import fetch_records
from .transform.cleaner import sanitize_dataset
from .reporting.formatter import generate_report

def run_full_pipeline(raw_data: list, title: str = "Execution Run") -> dict:
    """Facade helper coordinating ingestion, cleaning, and reporting."""
    clean_data = fetch_records(raw_data)
    report = generate_report(clean_data, title=title)
    return report

__all__ = [
    "run_full_pipeline",
    "fetch_records",
    "sanitize_dataset",
    "generate_report",
]
'''
    with open(os.path.join(pkg_root, "__init__.py"), "w", encoding="utf-8") as f:
        f.write(facade_code)

    return pkg_root


def audit_package_architecture(pkg: Any) -> Dict[str, Any]:
    """
    Reflective audit inspecting package attributes:
    - __name__, __file__, __package__, __path__
    - __all__ exposed symbols
    - Presence of sub-packages
    """
    is_package = hasattr(pkg, "__path__")
    paths = list(pkg.__path__) if is_package else []
    exposed_symbols = getattr(pkg, "__all__", [])

    return {
        "package_name": getattr(pkg, "__name__", None),
        "is_package": is_package,
        "entry_file": getattr(pkg, "__file__", None),
        "path_dirs": paths,
        "parent_package": getattr(pkg, "__package__", None),
        "public_exports": exposed_symbols,
    }


def explain_relative_import_caveat() -> str:
    """
    Explains why relative imports fail when running a submodule directly with python submodule.py.
    """
    return (
        "Caveat: Relative imports (e.g., 'from ..transform import cleaner') rely on the "
        "module's `__name__` and `__package__` attributes set by the Python import machinery. "
        "When running a module directly via `python path/to/module.py`, Python sets `__name__ = '__main__'` "
        "and `__package__ = None` (or empty). As a result, Python has no knowledge of where the module sits "
        "in the package hierarchy, raising: "
        "'ImportError: attempted relative import with no known parent package'. "
        "To execute package submodules as CLI scripts, use `python -m package.subpackage.module`."
    )


if __name__ == "__main__":
    temp_dir = tempfile.mkdtemp(prefix="agy_pkg_test_")
    try:
        # Create physical package structure
        pkg_root = create_mock_package_structure(temp_dir)
        sys.path.insert(0, temp_dir)

        # Import top-level facade package
        analytics_core = importlib.import_module("analytics_core")

        print("=== 1. Package Architecture Reflection Audit ===")
        audit = audit_package_architecture(analytics_core)
        for key, val in audit.items():
            print(f"  {key}: {val}")

        print("\n=== 2. Facade API Execution ===")
        sample_raw = [
            {"id": 1, "val": "100.55"},
            {"id": 2, "val": 250.2},
            {"id": 3, "val": None},  # corrupt / filtered
            {"id": 4, "val": "49.25"},
        ]

        # Call facade method
        result = analytics_core.run_full_pipeline(sample_raw, title="Q3 Financial Analytics")
        print(f"Pipeline Result: {result}")

        # Call direct imported facade symbol
        direct_ingest = analytics_core.fetch_records(sample_raw)
        print(f"Sanitized Records count: {len(direct_ingest)}")

        print("\n=== 3. Relative Import Explanation ===")
        print(explain_relative_import_caveat())

    finally:
        # Cleanup
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        for mod in list(sys.modules.keys()):
            if mod.startswith("analytics_core"):
                del sys.modules[mod]
        shutil.rmtree(temp_dir, ignore_errors=True)
