"""
Topic 08: Modules and Packages - Question 02: Creating Your Own Module

A comprehensive collection of 10 standalone, runnable exercises exploring
how to design, structure, export, document, and manage custom Python modules,
including __all__ exports, module-level singletons, PEP 562 dynamic attribute lookup,
and side-effect isolation.

Questions Covered:
 1. Module Anatomy: Structuring constants, functions, classes, and docstrings.
 2. Public API Definition with __all__: Controlling wildcard star imports.
 3. Module Privacy Conventions: Leading underscore _private functions vs __all__.
 4. Module-Level Singletons: Managing shared process state via module variables.
 5. Module Docstrings & Introspection: Inspecting __doc__ and function signatures.
 6. Module PEP 562 __getattr__: Intercepting module-level attribute lookups dynamically.
 7. Module PEP 562 __dir__: Customizing dir(module) autocomplete and reflection.
 8. Pure Utility Modules: Designing standalone mathematical and string helpers.
 9. Import Side-Effect Prevention: Separating definition time from execution time.
10. Advanced Project: Dynamic Feature Flag & Configuration Registry Engine with PEP 562.
"""

import inspect
import os
import shutil
import sys
import tempfile
import types
from typing import Any


# ==============================================================================
# Question 1: Module Anatomy Fundamentals
# ==============================================================================
def exercise_q1_module_anatomy() -> None:
    """
    Demonstrate the standard anatomy of a well-formed Python module:
    - Module-level docstring
    - Metadata (__version__, __author__)
    - Exported constants
    - Functions and classes
    """
    print("=== Q1: Module Anatomy Fundamentals ===")

    temp_dir = tempfile.mkdtemp(prefix="mod_anatomy_")
    mod_file = os.path.join(temp_dir, "geometry_utils.py")

    try:
        code = '''"""
Geometry calculation utilities.
Provides area and perimeter formulas for common 2D polygons.
"""

__version__ = "1.2.0"
__author__ = "Antigravity Engineering"

PI = 3.141592653589793

def circle_area(radius: float) -> float:
    """Calculates area of a circle given radius."""
    if radius < 0:
        raise ValueError("Radius must be non-negative")
    return PI * (radius ** 2)

class Rectangle:
    """Represents a 2D rectangle."""
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height
'''
        with open(mod_file, "w", encoding="utf-8") as f:
            f.write(code)

        sys.path.insert(0, temp_dir)
        import geometry_utils  # type: ignore

        assert geometry_utils.__version__ == "1.2.0"
        assert geometry_utils.__author__ == "Antigravity Engineering"
        assert round(geometry_utils.circle_area(3.0), 2) == 28.27

        rect = geometry_utils.Rectangle(4, 5)
        assert rect.area() == 20.0

        print(f"  Module '{geometry_utils.__name__}' v{geometry_utils.__version__} loaded successfully.")
        print(f"  circle_area(3.0) = {round(geometry_utils.circle_area(3.0), 4)}")

    finally:
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        sys.modules.pop("geometry_utils", None)
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 2: Public API Definition with __all__
# ==============================================================================
def exercise_q2_public_api_all() -> None:
    """
    Demonstrate that `__all__` strictly governs which symbols are exported
    when a consumer executes `from my_module import *`.
    """
    print("\n=== Q2: Public API Definition with __all__ ===")

    temp_dir = tempfile.mkdtemp(prefix="mod_all_")
    mod_file = os.path.join(temp_dir, "export_filter.py")

    try:
        code = '''
__all__ = ["public_api_fn", "PUBLIC_CONSTANT"]

PUBLIC_CONSTANT = "EXPOSED"
SECRET_CONSTANT = "HIDDEN"

def public_api_fn() -> str:
    return "PUBLIC"

def unlisted_internal_fn() -> str:
    return "INTERNAL"
'''
        with open(mod_file, "w", encoding="utf-8") as f:
            f.write(code)

        sys.path.insert(0, temp_dir)
        import export_filter  # type: ignore

        # __all__ is an explicit list of strings
        assert export_filter.__all__ == ["public_api_fn", "PUBLIC_CONSTANT"]

        # When imported directly by name, unlisted symbols ARE accessible:
        assert export_filter.SECRET_CONSTANT == "HIDDEN"
        assert export_filter.unlisted_internal_fn() == "INTERNAL"

        # Simulating `from export_filter import *`:
        # Python filters globals to only include keys present in __all__
        star_exported = {
            k: getattr(export_filter, k)
            for k in export_filter.__all__
        }

        assert "public_api_fn" in star_exported
        assert "PUBLIC_CONSTANT" in star_exported
        assert "SECRET_CONSTANT" not in star_exported
        assert "unlisted_internal_fn" not in star_exported

        print(f"  Module __all__ defined exports: {export_filter.__all__}")
        print("  Star import simulation safely filtered unlisted symbols.")

    finally:
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        sys.modules.pop("export_filter", None)
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 3: Module Privacy Conventions (Leading Underscore)
# ==============================================================================
def exercise_q3_privacy_conventions() -> None:
    """
    Demonstrate that when __all__ is NOT defined, wildcard star imports
    automatically export all symbols EXCEPT those starting with an underscore (_).
    """
    print("\n=== Q3: Module Privacy Conventions ===")

    temp_dir = tempfile.mkdtemp(prefix="mod_privacy_")
    mod_file = os.path.join(temp_dir, "convention_module.py")

    try:
        code = '''
# No __all__ defined here!
public_value = 100
_private_helper = 200
_INTERNAL_SALT = "s3cr3t"

def public_calculator(x: int) -> int:
    return x + _private_helper
'''
        with open(mod_file, "w", encoding="utf-8") as f:
            f.write(code)

        sys.path.insert(0, temp_dir)
        import convention_module  # type: ignore

        # Python default star import rule when __all__ is absent:
        # includes all symbols that do NOT start with '_'
        exported_defaults = [k for k in dir(convention_module) if not k.startswith("_")]

        assert "public_value" in exported_defaults
        assert "public_calculator" in exported_defaults
        assert "_private_helper" not in exported_defaults
        assert "_INTERNAL_SALT" not in exported_defaults

        print(f"  Convention-based public exports: {exported_defaults}")
        print("  Leading underscore variables correctly excluded from default exports.")

    finally:
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        sys.modules.pop("convention_module", None)
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 4: Module-Level Singletons
# ==============================================================================
def exercise_q4_module_singletons() -> None:
    """
    Demonstrate using module-level state as a thread-safe, process-wide Singleton.
    Because Python modules are initialized only once in sys.modules, top-level
    state is universally shared across all importing files.
    """
    print("\n=== Q4: Module-Level Singletons ===")

    temp_dir = tempfile.mkdtemp(prefix="mod_singleton_")
    mod_file = os.path.join(temp_dir, "db_session_pool.py")

    try:
        code = '''
# Module-level shared singleton registry
_active_connections: dict[str, str] = {}

def connect(client_id: str) -> None:
    _active_connections[client_id] = "ACTIVE"

def disconnect(client_id: str) -> None:
    _active_connections.pop(client_id, None)

def get_active_count() -> int:
    return len(_active_connections)
'''
        with open(mod_file, "w", encoding="utf-8") as f:
            f.write(code)

        sys.path.insert(0, temp_dir)

        # Import in Consumer A
        import db_session_pool as pool_a  # type: ignore
        pool_a.connect("worker_1")
        pool_a.connect("worker_2")
        assert pool_a.get_active_count() == 2

        # Import in Consumer B (separate import statement in another part of app)
        import db_session_pool as pool_b  # type: ignore
        # Sees the EXACT same singleton state!
        assert pool_b.get_active_count() == 2
        pool_b.connect("worker_3")

        assert pool_a.get_active_count() == 3

        print(f"  Module singleton state shared across import references: {pool_a.get_active_count()} connections.")

    finally:
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        sys.modules.pop("db_session_pool", None)
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 5: Module Docstrings & Introspection
# ==============================================================================
def exercise_q5_module_docstrings_and_introspection() -> None:
    """
    Demonstrate accessing module-level docstrings, inspecting function docstrings,
    and programmatically generating API documentation from module objects.
    """
    print("\n=== Q5: Module Docstrings & Introspection ===")

    temp_dir = tempfile.mkdtemp(prefix="mod_docs_")
    mod_file = os.path.join(temp_dir, "documented_service.py")

    try:
        code = '''"""
Documented Service Module.
Provides mission-critical telemetry collection.
"""

def submit_metric(metric_name: str, value: float) -> bool:
    """Submits a telemetry metric reading to the aggregator."""
    return True
'''
        with open(mod_file, "w", encoding="utf-8") as f:
            f.write(code)

        sys.path.insert(0, temp_dir)
        import documented_service  # type: ignore

        # Inspect module docstring
        mod_doc = inspect.getdoc(documented_service)
        assert mod_doc is not None
        assert "Documented Service Module." in mod_doc

        # Inspect function docstring and signature
        fn = documented_service.submit_metric
        fn_doc = inspect.getdoc(fn)
        sig = inspect.signature(fn)

        assert fn_doc == "Submits a telemetry metric reading to the aggregator."
        assert str(sig) == "(metric_name: str, value: float) -> bool"

        print(f"  Module doc:    '{mod_doc.splitlines()[0]}'")
        print(f"  Function sig:  submit_metric{sig}")
        print(f"  Function doc:  '{fn_doc}'")

    finally:
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        sys.modules.pop("documented_service", None)
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 6: PEP 562 Dynamic Module __getattr__
# ==============================================================================
def exercise_q6_pep562_module_getattr() -> None:
    """
    Demonstrate PEP 562 module-level `__getattr__(name)`.
    Allows modules to intercept attribute lookups dynamically, enabling
    deprecation warnings, dynamic configuration, and lazy variable initialization.
    """
    print("\n=== Q6: PEP 562 Dynamic Module __getattr__ ===")

    temp_dir = tempfile.mkdtemp(prefix="mod_getattr_")
    mod_file = os.path.join(temp_dir, "dynamic_settings.py")

    try:
        code = '''
# Static attributes
APP_ENV = "production"

# PEP 562 module-level __getattr__
def __getattr__(name: str):
    if name == "DATABASE_URL":
        # Dynamic calculation / lazy loading
        return "postgresql://cluster-primary.internal:5432/db"
    elif name == "LEGACY_TIMEOUT":
        # Deprecated attribute hook
        return 30
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
'''
        with open(mod_file, "w", encoding="utf-8") as f:
            f.write(code)

        sys.path.insert(0, temp_dir)
        import dynamic_settings  # type: ignore

        # Static attribute access
        assert dynamic_settings.APP_ENV == "production"

        # Dynamic attribute access intercepted via module __getattr__
        assert dynamic_settings.DATABASE_URL == "postgresql://cluster-primary.internal:5432/db"
        assert dynamic_settings.LEGACY_TIMEOUT == 30

        # Unhandled dynamic attribute raises AttributeError
        caught_attr_err = False
        try:
            _ = dynamic_settings.UNKNOWN_FIELD
        except AttributeError as exc:
            caught_attr_err = True
            assert "has no attribute 'UNKNOWN_FIELD'" in str(exc)

        assert caught_attr_err is True
        print(f"  Static attribute:   {dynamic_settings.APP_ENV}")
        print(f"  Dynamic PEP 562:    {dynamic_settings.DATABASE_URL}")

    finally:
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        sys.modules.pop("dynamic_settings", None)
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 7: PEP 562 Dynamic Module __dir__
# ==============================================================================
def exercise_q7_pep562_module_dir() -> None:
    """
    Demonstrate PEP 562 module-level `__dir__()`.
    Allows modules with dynamic `__getattr__` to advertise their dynamic attributes
    so `dir(module)` and IDE autocompletion display them accurately.
    """
    print("\n=== Q7: PEP 562 Dynamic Module __dir__ ===")

    temp_dir = tempfile.mkdtemp(prefix="mod_dir_")
    mod_file = os.path.join(temp_dir, "custom_dir_mod.py")

    try:
        code = '''
STATIC_VAL = 42

def __getattr__(name: str):
    if name == "DYNAMIC_SECRET":
        return "classified"
    raise AttributeError(name)

def __dir__():
    # Return standard globals plus advertised dynamic attributes
    return ["STATIC_VAL", "DYNAMIC_SECRET"]
'''
        with open(mod_file, "w", encoding="utf-8") as f:
            f.write(code)

        sys.path.insert(0, temp_dir)
        import custom_dir_mod  # type: ignore

        dir_listing = dir(custom_dir_mod)
        assert "STATIC_VAL" in dir_listing
        assert "DYNAMIC_SECRET" in dir_listing

        print(f"  dir(custom_dir_mod) output: {dir_listing}")

    finally:
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        sys.modules.pop("custom_dir_mod", None)
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 8: Pure Utility Modules (Math & String Helpers)
# ==============================================================================
def exercise_q8_pure_utility_module() -> None:
    """
    Design and test a standalone pure-function utility module with clean isolation.
    """
    print("\n=== Q8: Pure Utility Modules ===")

    temp_dir = tempfile.mkdtemp(prefix="mod_util_")
    mod_file = os.path.join(temp_dir, "string_utils.py")

    try:
        code = '''
def slugify(text: str) -> str:
    """Converts a text string into a URL-friendly slug."""
    import re
    cleaned = re.sub(r'[^a-zA-Z0-9\\s-]', '', text).strip().lower()
    return re.sub(r'[\\s-]+', '-', cleaned)

def truncate(text: str, max_chars: int = 20, suffix: str = '...') -> str:
    """Truncates text safely with trailing suffix."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars - len(suffix)] + suffix
'''
        with open(mod_file, "w", encoding="utf-8") as f:
            f.write(code)

        sys.path.insert(0, temp_dir)
        import string_utils  # type: ignore

        assert string_utils.slugify("Hello World! 2026 Test") == "hello-world-2026-test"
        assert string_utils.truncate("The quick brown fox jumps", max_chars=15) == "The quick br..."

        print(f"  slugify result:  '{string_utils.slugify('Hello World! 2026 Test')}'")
        print(f"  truncate result: '{string_utils.truncate('The quick brown fox jumps', 15)}'")

    finally:
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        sys.modules.pop("string_utils", None)
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 9: Import Side-Effect Prevention
# ==============================================================================
def exercise_q9_import_side_effects() -> None:
    """
    Demonstrate designing modules without unintended top-level execution side-effects.
    Modules should define functions, classes, and constants without initiating
    network requests, disk writes, or heavy operations on `import`.
    """
    print("\n=== Q9: Import Side-Effect Prevention ===")

    temp_dir = tempfile.mkdtemp(prefix="mod_side_")
    mod_file = os.path.join(temp_dir, "safe_service.py")

    try:
        code = '''
# Pure declarations - NO active side-effects at import time
_client_connected = False

def initialize_service() -> bool:
    """Explicit lifecycle method called intentionally by consumer."""
    global _client_connected
    _client_connected = True
    return _client_connected

def is_ready() -> bool:
    return _client_connected
'''
        with open(mod_file, "w", encoding="utf-8") as f:
            f.write(code)

        sys.path.insert(0, temp_dir)
        import safe_service  # type: ignore

        # Importing must NOT have initialized the client
        assert safe_service.is_ready() is False

        # Consumer explicitly controls execution lifecycle
        safe_service.initialize_service()
        assert safe_service.is_ready() is True

        print("  Import executed with ZERO side-effects; lifecycle explicitly controlled.")

    finally:
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        sys.modules.pop("safe_service", None)
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 10: Advanced Project - Dynamic Feature Flags Registry Module
# ==============================================================================
def exercise_q10_feature_flag_module() -> None:
    """
    Build and test a complete dynamic configuration module utilizing PEP 562
    to serve feature flags with environment overrides and default fallbacks.
    """
    print("\n=== Q10: Dynamic Feature Flag & Config Registry Module ===")

    temp_dir = tempfile.mkdtemp(prefix="mod_flags_")
    mod_file = os.path.join(temp_dir, "feature_flags.py")

    try:
        code = '''
"""
Enterprise Dynamic Feature Flags Module.
Provides dynamic flag resolution with PEP 562 __getattr__.
"""
import os

_DEFAULT_FLAGS = {
    "ENABLE_NEW_CHECKOUT": True,
    "MAX_BATCH_SIZE": 100,
    "MAINTENANCE_MODE": False,
}

_DYNAMIC_OVERRIDES = {}

def set_override(flag_name: str, value):
    _DYNAMIC_OVERRIDES[flag_name] = value

def clear_overrides():
    _DYNAMIC_OVERRIDES.clear()

def __getattr__(name: str):
    # 1. Check runtime dynamic overrides
    if name in _DYNAMIC_OVERRIDES:
        return _DYNAMIC_OVERRIDES[name]

    # 2. Check OS environment variable
    env_key = f"FLAG_{name}"
    if env_key in os.environ:
        raw_val = os.environ[env_key]
        if raw_val.lower() in ("true", "1", "yes"):
            return True
        elif raw_val.lower() in ("false", "0", "no"):
            return False
        return raw_val

    # 3. Check defaults
    if name in _DEFAULT_FLAGS:
        return _DEFAULT_FLAGS[name]

    raise AttributeError(f"Unknown feature flag: '{name}'")

def __dir__():
    return list(set(list(_DEFAULT_FLAGS.keys()) + list(_DYNAMIC_OVERRIDES.keys())))
'''
        with open(mod_file, "w", encoding="utf-8") as f:
            f.write(code)

        sys.path.insert(0, temp_dir)
        import feature_flags  # type: ignore

        # 1. Default lookup
        assert feature_flags.ENABLE_NEW_CHECKOUT is True
        assert feature_flags.MAX_BATCH_SIZE == 100
        assert feature_flags.MAINTENANCE_MODE is False

        # 2. Dynamic runtime override
        feature_flags.set_override("MAINTENANCE_MODE", True)
        assert feature_flags.MAINTENANCE_MODE is True

        # 3. Environment variable override
        os.environ["FLAG_ENABLE_NEW_CHECKOUT"] = "false"
        feature_flags.clear_overrides()
        assert feature_flags.ENABLE_NEW_CHECKOUT is False
        del os.environ["FLAG_ENABLE_NEW_CHECKOUT"]

        # 4. Unknown flag raises AttributeError
        try:
            _ = feature_flags.NON_EXISTENT_FLAG
            assert False
        except AttributeError as exc:
            assert "Unknown feature flag" in str(exc)

        print("  Feature flag module tested successfully:")
        print(f"    Default flag resolved:       ENABLE_NEW_CHECKOUT")
        print(f"    Dynamic override resolved:   MAINTENANCE_MODE=True")
        print(f"    Environment override tested: FLAG_ENABLE_NEW_CHECKOUT=false")

    finally:
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        sys.modules.pop("feature_flags", None)
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_module_anatomy()
    exercise_q2_public_api_all()
    exercise_q3_privacy_conventions()
    exercise_q4_module_singletons()
    exercise_q5_module_docstrings_and_introspection()
    exercise_q6_pep562_module_getattr()
    exercise_q7_pep562_module_dir()
    exercise_q8_pure_utility_module()
    exercise_q9_import_side_effects()
    exercise_q10_feature_flag_module()

    print("\nAll 10 creating modules questions executed and asserted successfully!")
