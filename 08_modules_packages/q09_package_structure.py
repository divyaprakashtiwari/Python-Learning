"""
Topic 08: Modules and Packages - Question 09: Package Structure

A comprehensive collection of 10 standalone, runnable exercises exploring
Python package architecture, regular vs namespace packages (PEP 420), `__init__.py`
facades, relative imports, nested subpackages, and `importlib.resources`.

Questions Covered:
 1. Regular Package Definition: The role and execution of __init__.py.
 2. Package Facade Pattern: Re-exporting nested submodule functions in __init__.py.
 3. Package __all__ Specification: Defining top-level star import boundaries.
 4. Relative Imports (. and ..): Sibling and parent package navigation mechanics.
 5. Deep Multi-Tier Subpackages: Structuring enterprise domain hierarchies.
 6. Package Data & Resources: Modern resource reading with importlib.resources.
 7. Package __path__ Attribute: Inspecting and manipulating module search locations.
 8. PEP 420 Native Namespace Packages: Multi-directory packages without __init__.py.
 9. Package Introspection: Inspecting __package__, __file__, and __spec__.
10. Advanced Project: Modular Microservice Package Harness with automated service registry.
"""

import importlib
import importlib.resources
import os
import shutil
import sys
import tempfile
from typing import Any


# ==============================================================================
# Question 1: Regular Package Definition (__init__.py)
# ==============================================================================
def exercise_q1_regular_package_init() -> None:
    """
    Demonstrate that a directory containing an `__init__.py` file is recognized
    as a regular Python package, and `__init__.py` executes on package import.
    """
    print("=== Q1: Regular Package Definition (__init__.py) ===")

    temp_dir = tempfile.mkdtemp(prefix="pkg_reg_")
    pkg_dir = os.path.join(temp_dir, "sample_package")
    os.makedirs(pkg_dir)

    try:
        # Create __init__.py with initialization flag
        with open(os.path.join(pkg_dir, "__init__.py"), "w", encoding="utf-8") as f:
            f.write("PACKAGE_LOADED = True\nINITIALIZED_AT = 2026\n")

        sys.path.insert(0, temp_dir)
        import sample_package  # type: ignore

        assert sample_package.PACKAGE_LOADED is True
        assert sample_package.INITIALIZED_AT == 2026
        # A package is a module with a __path__ attribute
        assert hasattr(sample_package, "__path__")

        print(f"  Package '{sample_package.__name__}' imported successfully.")
        print(f"  Package path: {sample_package.__path__}")

    finally:
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        sys.modules.pop("sample_package", None)
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 2: Package Facade Pattern (Re-exporting)
# ==============================================================================
def exercise_q2_package_facade_pattern() -> None:
    """
    Demonstrate the Package Facade Pattern: submodules are kept internal,
    while `__init__.py` imports and re-exports key functions so consumers
    can write `import my_pkg; my_pkg.quick_tool()` without knowing internal layout.
    """
    print("\n=== Q2: Package Facade Pattern (Re-exporting) ===")

    temp_dir = tempfile.mkdtemp(prefix="pkg_facade_")
    pkg_dir = os.path.join(temp_dir, "analytics")
    os.makedirs(pkg_dir)

    try:
        # Internal submodule 1: metrics.py
        with open(os.path.join(pkg_dir, "metrics.py"), "w", encoding="utf-8") as f:
            f.write("def calculate_mean(nums): return sum(nums) / len(nums)\n")

        # Internal submodule 2: formatter.py
        with open(os.path.join(pkg_dir, "formatter.py"), "w", encoding="utf-8") as f:
            f.write("def format_percent(val): return f'{val * 100:.1f}%'\n")

        # __init__.py re-exports selected public functions
        init_code = """
from .metrics import calculate_mean
from .formatter import format_percent

__all__ = ["calculate_mean", "format_percent"]
"""
        with open(os.path.join(pkg_dir, "__init__.py"), "w", encoding="utf-8") as f:
            f.write(init_code.strip())

        sys.path.insert(0, temp_dir)
        import analytics  # type: ignore

        # Clean top-level facade calls
        mean = analytics.calculate_mean([10, 20, 30])
        formatted = analytics.format_percent(0.856)

        assert mean == 20.0
        assert formatted == "85.6%"

        print(f"  Facade calculate_mean: {mean}")
        print(f"  Facade format_percent: {formatted}")

    finally:
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        sys.modules.pop("analytics", None)
        sys.modules.pop("analytics.metrics", None)
        sys.modules.pop("analytics.formatter", None)
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 3: Package __all__ Specification
# ==============================================================================
def exercise_q3_package_all_export() -> None:
    """
    Demonstrate how __all__ in a package's __init__.py determines which
    submodules or symbols are imported during `from my_package import *`.
    """
    print("\n=== Q3: Package __all__ Specification ===")

    temp_dir = tempfile.mkdtemp(prefix="pkg_all_")
    pkg_dir = os.path.join(temp_dir, "sdk_kit")
    os.makedirs(pkg_dir)

    try:
        with open(os.path.join(pkg_dir, "client.py"), "w", encoding="utf-8") as f:
            f.write("class Client: pass\n")
        with open(os.path.join(pkg_dir, "internal_auth.py"), "w", encoding="utf-8") as f:
            f.write("class AuthHelper: pass\n")

        # Only export 'client' submodule
        with open(os.path.join(pkg_dir, "__init__.py"), "w", encoding="utf-8") as f:
            f.write("__all__ = ['client']\nfrom . import client\n")

        sys.path.insert(0, temp_dir)
        import sdk_kit  # type: ignore

        assert sdk_kit.__all__ == ["client"]
        assert hasattr(sdk_kit, "client")

        print(f"  sdk_kit.__all__ exports: {sdk_kit.__all__}")

    finally:
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        sys.modules.pop("sdk_kit", None)
        sys.modules.pop("sdk_kit.client", None)
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 4: Relative Imports (. and ..)
# ==============================================================================
def exercise_q4_relative_imports() -> None:
    """
    Demonstrate explicit intra-package relative imports:
    - Single dot (.): current package / sibling submodule
    - Double dot (..): parent package
    """
    print("\n=== Q4: Relative Imports (. and ..) ===")

    temp_dir = tempfile.mkdtemp(prefix="pkg_rel_")
    root_pkg = os.path.join(temp_dir, "app_tree")
    sub_pkg = os.path.join(root_pkg, "sub")
    os.makedirs(sub_pkg)

    try:
        # root_pkg/__init__.py
        with open(os.path.join(root_pkg, "__init__.py"), "w", encoding="utf-8") as f:
            f.write("ROOT_TOKEN = 'ROOT_2026'\n")

        # root_pkg/common.py
        with open(os.path.join(root_pkg, "common.py"), "w", encoding="utf-8") as f:
            f.write("def shared_calc(): return 42\n")

        # root_pkg/sub/__init__.py
        with open(os.path.join(sub_pkg, "__init__.py"), "w", encoding="utf-8") as f:
            f.write("")

        # root_pkg/sub/worker.py (uses relative imports to sibling and parent)
        worker_code = """
from ..common import shared_calc
from .. import ROOT_TOKEN

def run_worker():
    return f"{ROOT_TOKEN}_{shared_calc()}"
"""
        with open(os.path.join(sub_pkg, "worker.py"), "w", encoding="utf-8") as f:
            f.write(worker_code.strip())

        sys.path.insert(0, temp_dir)
        import app_tree.sub.worker as worker_mod  # type: ignore

        res = worker_mod.run_worker()
        assert res == "ROOT_2026_42"

        print(f"  Relative import resolved from subpackage to parent: '{res}'")

    finally:
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        sys.modules.pop("app_tree", None)
        sys.modules.pop("app_tree.common", None)
        sys.modules.pop("app_tree.sub", None)
        sys.modules.pop("app_tree.sub.worker", None)
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 5: Deep Multi-Tier Subpackages
# ==============================================================================
def exercise_q5_deep_subpackages() -> None:
    """
    Structure a deep 3-tier enterprise package:
    enterprise/ -> core/ -> security/ -> encryption.py
    """
    print("\n=== Q5: Deep Multi-Tier Subpackages ===")

    temp_dir = tempfile.mkdtemp(prefix="pkg_deep_")
    deep_path = os.path.join(temp_dir, "enterprise", "core", "security")
    os.makedirs(deep_path)

    try:
        # Create intermediate __init__.py files
        with open(os.path.join(temp_dir, "enterprise", "__init__.py"), "w") as f:
            f.write("")
        with open(os.path.join(temp_dir, "enterprise", "core", "__init__.py"), "w") as f:
            f.write("")
        with open(os.path.join(temp_dir, "enterprise", "core", "security", "__init__.py"), "w") as f:
            f.write("")

        # Leaf module: encryption.py
        with open(os.path.join(deep_path, "encryption.py"), "w", encoding="utf-8") as f:
            f.write("def hash_token(s): return f'HASH_{s}'\n")

        sys.path.insert(0, temp_dir)
        import enterprise.core.security.encryption as enc  # type: ignore

        assert enc.hash_token("admin") == "HASH_admin"
        assert enc.__name__ == "enterprise.core.security.encryption"

        print(f"  Deep package module name: {enc.__name__}")
        print(f"  Leaf function output:     {enc.hash_token('admin')}")

    finally:
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        for k in list(sys.modules.keys()):
            if k.startswith("enterprise"):
                sys.modules.pop(k, None)
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 6: Package Data & Resources (importlib.resources)
# ==============================================================================
def exercise_q6_importlib_resources() -> None:
    """
    Demonstrate loading static asset files (JSON, schemas, templates) packaged
    alongside Python modules using modern `importlib.resources.files()`.
    """
    print("\n=== Q6: Package Data & Resources ===")

    temp_dir = tempfile.mkdtemp(prefix="pkg_res_")
    pkg_dir = os.path.join(temp_dir, "asset_package")
    os.makedirs(pkg_dir)

    try:
        with open(os.path.join(pkg_dir, "__init__.py"), "w", encoding="utf-8") as f:
            f.write("")

        # Embed static text resource inside package
        asset_file = os.path.join(pkg_dir, "config_schema.json")
        with open(asset_file, "w", encoding="utf-8") as f:
            f.write('{"schema_version": 2026, "type": "config"}')

        sys.path.insert(0, temp_dir)

        # Ingest resource using standard library importlib.resources
        res_traversable = importlib.resources.files("asset_package").joinpath("config_schema.json")
        content = res_traversable.read_text(encoding="utf-8")

        assert "schema_version" in content
        assert "2026" in content

        print(f"  Loaded package data resource via importlib.resources.files():\n    {content}")

    finally:
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        sys.modules.pop("asset_package", None)
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 7: Package __path__ Attribute Manipulation
# ==============================================================================
def exercise_q7_package_path_attribute() -> None:
    """
    Demonstrate that every package has a `__path__` attribute (a list of filesystem paths)
    where Python searches for submodules. Demonstrates extending `__path__` dynamically.
    """
    print("\n=== Q7: Package __path__ Attribute Manipulation ===")

    temp_dir1 = tempfile.mkdtemp(prefix="pkg_path1_")
    temp_dir2 = tempfile.mkdtemp(prefix="pkg_path2_")

    pkg_dir1 = os.path.join(temp_dir1, "dynamic_pkg")
    pkg_dir2 = os.path.join(temp_dir2, "dynamic_pkg_extra")
    os.makedirs(pkg_dir1)
    os.makedirs(pkg_dir2)

    try:
        with open(os.path.join(pkg_dir1, "__init__.py"), "w", encoding="utf-8") as f:
            f.write("")
        with open(os.path.join(pkg_dir1, "mod1.py"), "w", encoding="utf-8") as f:
            f.write("VAL1 = 'from_dir1'\n")

        # Second external folder has mod2
        with open(os.path.join(pkg_dir2, "mod2.py"), "w", encoding="utf-8") as f:
            f.write("VAL2 = 'from_dir2'\n")

        sys.path.insert(0, temp_dir1)
        import dynamic_pkg  # type: ignore

        import dynamic_pkg.mod1 as m1  # type: ignore
        assert m1.VAL1 == "from_dir1"

        # Extend package __path__ to also include the second directory
        dynamic_pkg.__path__.append(pkg_dir2)

        # Now dynamic_pkg can import mod2 from the external folder!
        import dynamic_pkg.mod2 as m2  # type: ignore
        assert m2.VAL2 == "from_dir2"

        print(f"  dynamic_pkg.__path__ extended to: {dynamic_pkg.__path__}")
        print(f"  Submodule 1: {m1.VAL1}, Submodule 2: {m2.VAL2}")

    finally:
        if temp_dir1 in sys.path:
            sys.path.remove(temp_dir1)
        for k in ["dynamic_pkg", "dynamic_pkg.mod1", "dynamic_pkg.mod2"]:
            sys.modules.pop(k, None)
        shutil.rmtree(temp_dir1, ignore_errors=True)
        shutil.rmtree(temp_dir2, ignore_errors=True)


# ==============================================================================
# Question 8: PEP 420 Native Namespace Packages
# ==============================================================================
def exercise_q8_native_namespace_packages() -> None:
    """
    Demonstrate PEP 420 Native Namespace Packages:
    Multiple disparate directories can contribute to the same logical package namespace
    WITHOUT any `__init__.py` files present in the namespace root directories.
    """
    print("\n=== Q8: PEP 420 Native Namespace Packages ===")

    # Create two separate root directories
    dir_a = tempfile.mkdtemp(prefix="ns_a_")
    dir_b = tempfile.mkdtemp(prefix="ns_b_")

    # Both share namespace folder "corp_namespace" WITHOUT __init__.py!
    ns_a = os.path.join(dir_a, "corp_namespace", "auth")
    ns_b = os.path.join(dir_b, "corp_namespace", "billing")
    os.makedirs(ns_a)
    os.makedirs(ns_b)

    try:
        # Submodule A
        with open(os.path.join(ns_a, "__init__.py"), "w", encoding="utf-8") as f:
            f.write("def login(): return 'AUTH_SUCCESS'\n")

        # Submodule B
        with open(os.path.join(ns_b, "__init__.py"), "w", encoding="utf-8") as f:
            f.write("def invoice(): return 'INVOICE_PAID'\n")

        # Add both root folders to sys.path
        sys.path.insert(0, dir_b)
        sys.path.insert(0, dir_a)

        # Import unified namespace
        import corp_namespace.auth as auth_mod  # type: ignore
        import corp_namespace.billing as bill_mod  # type: ignore

        assert auth_mod.login() == "AUTH_SUCCESS"
        assert bill_mod.invoice() == "INVOICE_PAID"

        # The parent namespace package has no __file__ attribute (it's a namespace!)
        import corp_namespace  # type: ignore
        assert corp_namespace.__file__ is None
        # It aggregates both physical locations into its _NamespacePath
        assert len(corp_namespace.__path__) >= 2

        print(f"  Namespace package __file__: {corp_namespace.__file__} (None as expected)")
        print(f"  Namespace __path__ locations count: {len(corp_namespace.__path__)}")
        print(f"  Unified namespace submodules: {auth_mod.login()} & {bill_mod.invoice()}")

    finally:
        if dir_a in sys.path:
            sys.path.remove(dir_a)
        if dir_b in sys.path:
            sys.path.remove(dir_b)
        for k in ["corp_namespace", "corp_namespace.auth", "corp_namespace.billing"]:
            sys.modules.pop(k, None)
        shutil.rmtree(dir_a, ignore_errors=True)
        shutil.rmtree(dir_b, ignore_errors=True)


# ==============================================================================
# Question 9: Package Introspection Attributes
# ==============================================================================
def exercise_q9_package_introspection() -> None:
    """
    Inspect package metadata attributes:
    - __package__: The package name for relative imports.
    - __file__: Path to package's __init__.py file.
    - __spec__: ModuleSpec describing the package origin and loader.
    """
    print("\n=== Q9: Package Introspection Attributes ===")

    import json

    assert json.__package__ == "json"
    assert json.__file__ is not None and json.__file__.endswith("__init__.py")
    assert json.__spec__ is not None
    assert json.__spec__.submodule_search_locations is not None

    print(f"  json.__package__: {json.__package__}")
    print(f"  json.__file__:    {os.path.basename(json.__file__)}")
    print(f"  json.__spec__:    {json.__spec__.name}")


# ==============================================================================
# Question 10: Advanced Project - Modular Microservice Package Architecture
# ==============================================================================
class MicroserviceRouter:
    """
    Simulates an enterprise microservice router that dynamically loads and routes
    requests to subpackages conforming to the service handler contract.
    """

    def __init__(self, services_root_dir: str) -> None:
        self.services_root_dir = services_root_dir
        self.handlers: dict[str, Any] = {}

    def register_service(self, service_name: str, handler_callable: Any) -> None:
        self.handlers[service_name] = handler_callable

    def route_request(self, service_name: str, payload: dict[str, Any]) -> dict[str, Any]:
        if service_name not in self.handlers:
            return {"status": 404, "error": f"Service '{service_name}' not found"}
        handler = self.handlers[service_name]
        return {"status": 200, "data": handler(payload)}


def exercise_q10_modular_microservice_package() -> None:
    """
    Test MicroserviceRouter with simulated modular package services.
    """
    print("\n=== Q10: Modular Microservice Package Architecture ===")

    temp_dir = tempfile.mkdtemp(prefix="pkg_svc_")

    try:
        router = MicroserviceRouter(temp_dir)

        # Register Service 1: Payment Handler
        def handle_payment(req: dict[str, Any]) -> str:
            return f"Processed ${req.get('amount', 0):.2f}"

        # Register Service 2: Notification Handler
        def handle_notification(req: dict[str, Any]) -> str:
            return f"Email dispatched to {req.get('to')}"

        router.register_service("payments", handle_payment)
        router.register_service("notifications", handle_notification)

        res1 = router.route_request("payments", {"amount": 99.50})
        assert res1["status"] == 200
        assert res1["data"] == "Processed $99.50"

        res2 = router.route_request("notifications", {"to": "alice@corp.internal"})
        assert res2["status"] == 200
        assert res2["data"] == "Email dispatched to alice@corp.internal"

        res_missing = router.route_request("unknown_svc", {})
        assert res_missing["status"] == 404

        print(f"  Payment Service:      {res1['data']}")
        print(f"  Notification Service: {res2['data']}")
        print(f"  Unknown Service:      {res_missing['error']}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_regular_package_init()
    exercise_q2_package_facade_pattern()
    exercise_q3_package_all_export()
    exercise_q4_relative_imports()
    exercise_q5_deep_subpackages()
    exercise_q6_importlib_resources()
    exercise_q7_package_path_attribute()
    exercise_q8_native_namespace_packages()
    exercise_q9_package_introspection()
    exercise_q10_modular_microservice_package()

    print("\nAll 10 package structure questions executed and asserted successfully!")
