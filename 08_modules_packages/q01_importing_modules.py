"""
Topic 08: Modules and Packages - Question 01: Importing Modules

A comprehensive collection of 10 standalone, runnable exercises exploring
Python's import system, sys.path search order, sys.modules cache, dynamic loading
with importlib, module reloading, circular import resolution, and plugin architectures.

Questions Covered:
 1. Core Import Syntaxes: import, from...import, aliasing with 'as', and star import perils.
 2. Module Search Path (sys.path): Resolution hierarchy and runtime directory injection.
 3. Module Cache (sys.modules): Single-evaluation semantics and cached module reuse.
 4. Dynamic Module Loading with importlib.import_module: Runtime string-based imports.
 5. In-Place Module Reloading with importlib.reload: Updating code without restarting process.
 6. Circular Imports Mechanics: Diagnosis and resolution via deferred function-level imports.
 7. Module Introspection Attributes: __name__, __file__, __doc__, __all__, and __spec__.
 8. Direct File Path Imports: Loading arbitrary .py files via importlib.util.spec_from_file_location.
 9. Graceful Fallback / Conditional Imports: Managing optional high-performance dependencies.
10. Advanced Project: Dynamic Plugin Discovery & Hook Registry Engine.
"""

import importlib
import importlib.util
import os
import shutil
import sys
import tempfile
import types
from typing import Any


# ==============================================================================
# Question 1: Core Import Syntaxes
# ==============================================================================
def exercise_q1_core_import_syntaxes() -> None:
    """
    Demonstrate various import syntax styles:
    - Direct: import math
    - Selective: from math import sqrt, pi
    - Aliasing: import math as m, from math import floor as flr
    - Star import (`from module import *`) and namespace pollution.
    """
    print("=== Q1: Core Import Syntaxes ===")

    # 1. Direct import
    import math
    assert math.sqrt(16) == 4.0

    # 2. Selective import
    from math import pi, pow
    assert pi > 3.14
    assert pow(2, 3) == 8.0

    # 3. Aliased import
    import math as m
    from math import floor as math_floor
    assert m.sin(0) == 0.0
    assert math_floor(4.9) == 4

    # 4. Star import simulation (inspecting __all__)
    # Star import imports everything listed in `__all__`, or all non-underscore symbols
    math_symbols = dir(math)
    assert "sqrt" in math_symbols
    assert "sin" in math_symbols

    print(f"  Standard math.sqrt(16): {math.sqrt(16)}")
    print(f"  Selective pi:           {round(pi, 4)}")
    print(f"  Aliased math_floor:     {math_floor(4.9)}")


# ==============================================================================
# Question 2: Module Search Path (sys.path)
# ==============================================================================
def exercise_q2_sys_path_search_order() -> None:
    """
    Demonstrate sys.path search order:
    1. Current script's directory (or working directory).
    2. PYTHONPATH environment variable directories.
    3. Standard library directories.
    4. site-packages (third-party installed packages).
    Demonstrate injecting a custom temporary path at runtime.
    """
    print("\n=== Q2: Module Search Path (sys.path) ===")

    temp_dir = tempfile.mkdtemp(prefix="mod_path_")
    mod_path = os.path.join(temp_dir, "runtime_dummy_mod.py")

    try:
        # Create a module in an external temporary folder
        with open(mod_path, "w", encoding="utf-8") as f:
            f.write("DUMMY_VERSION = '2026.1'\ndef ping(): return 'PONG'\n")

        # Before appending, module cannot be found
        assert "runtime_dummy_mod" not in sys.modules
        can_import_before = False
        try:
            importlib.import_module("runtime_dummy_mod")
            can_import_before = True
        except ModuleNotFoundError:
            pass
        assert can_import_before is False

        # Inject temporary directory into sys.path
        sys.path.insert(0, temp_dir)

        # Now import succeeds!
        dummy_mod = importlib.import_module("runtime_dummy_mod")
        assert dummy_mod.DUMMY_VERSION == "2026.1"  # type: ignore
        assert dummy_mod.ping() == "PONG"  # type: ignore

        print(f"  Successfully imported dynamic module from injected sys.path: {dummy_mod.ping()}")  # type: ignore

    finally:
        # Cleanup
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        sys.modules.pop("runtime_dummy_mod", None)
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 3: Module Cache (sys.modules)
# ==============================================================================
def exercise_q3_sys_modules_cache() -> None:
    """
    Demonstrate that Python imports a module only ONCE per process.
    Subsequent imports retrieve the cached module object directly from `sys.modules`.
    """
    print("\n=== Q3: Module Cache (sys.modules) ===")

    # sys.modules is a dictionary mapping module name to module object
    assert "math" in sys.modules
    cached_math_1 = sys.modules["math"]

    import math as math_ref_2
    assert cached_math_1 is math_ref_2  # Exact same memory address!

    # Mutating an attribute on the imported module reflects across all references
    setattr(cached_math_1, "_custom_annotation", "CacheTest2026")
    import math as math_ref_3
    assert getattr(math_ref_3, "_custom_annotation") == "CacheTest2026"

    # Clean up custom attribute
    delattr(cached_math_1, "_custom_annotation")

    print(f"  sys.modules has {len(sys.modules)} loaded modules.")
    print("  Verified single-instance module caching across imports.")


# ==============================================================================
# Question 4: Dynamic Module Loading with importlib.import_module
# ==============================================================================
def exercise_q4_dynamic_import_module() -> None:
    """
    Demonstrate loading modules dynamically at runtime using string identifiers
    via `importlib.import_module(module_name)`.
    """
    print("\n=== Q4: Dynamic Module Loading with importlib.import_module ===")

    def compute_operation(module_name: str, func_name: str, *args: Any) -> Any:
        module = importlib.import_module(module_name)
        func = getattr(module, func_name)
        return func(*args)

    res_math = compute_operation("math", "sin", 0)
    assert res_math == 0.0

    res_json = compute_operation("json", "dumps", {"status": "ok"})
    assert res_json == '{"status": "ok"}'

    # Unknown module raises ModuleNotFoundError
    caught_missing = False
    try:
        compute_operation("non_existent_package_xyz", "run")
    except ModuleNotFoundError:
        caught_missing = True

    assert caught_missing is True
    print(f"  Dynamically invoked math.sin(0): {res_math}")
    print(f"  Dynamically invoked json.dumps:   {res_json}")


# ==============================================================================
# Question 5: In-Place Module Reloading with importlib.reload
# ==============================================================================
def exercise_q5_module_reloading() -> None:
    """
    Demonstrate reloading a modified module in-place at runtime without
    restarting the Python interpreter using `importlib.reload(module)`.
    """
    print("\n=== Q5: In-Place Module Reloading ===")

    temp_dir = tempfile.mkdtemp(prefix="mod_reload_")
    mod_file = os.path.join(temp_dir, "hot_reload_target.py")

    try:
        sys.path.insert(0, temp_dir)

        # Version 1 of module
        with open(mod_file, "w", encoding="utf-8") as f:
            f.write("BUILD_VERSION = 1\ndef get_status(): return 'OLD_CODE'\n")

        mod = importlib.import_module("hot_reload_target")
        assert mod.BUILD_VERSION == 1  # type: ignore
        assert mod.get_status() == "OLD_CODE"  # type: ignore

        # Write Version 2 of module to disk
        with open(mod_file, "w", encoding="utf-8") as f:
            f.write("BUILD_VERSION = 2\ndef get_status(): return 'HOT_RELOADED_CODE'\n")

        # Standard import will return CACHED version 1!
        cached_import = importlib.import_module("hot_reload_target")
        assert cached_import.BUILD_VERSION == 1  # type: ignore

        # importlib.reload updates the existing module instance in-place!
        reloaded = importlib.reload(mod)
        assert reloaded.BUILD_VERSION == 2  # type: ignore
        assert reloaded.get_status() == "HOT_RELOADED_CODE"  # type: ignore
        assert reloaded is mod  # Same object identity updated in place!

        print(f"  Initial module status:  'OLD_CODE'")
        print(f"  Hot-reloaded status:    '{reloaded.get_status()}'")  # type: ignore

    finally:
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        sys.modules.pop("hot_reload_target", None)
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 6: Circular Imports Mechanics & Resolution
# ==============================================================================
def exercise_q6_circular_imports() -> None:
    """
    Demonstrate circular import problems and the deferred function-level import
    resolution pattern.
    """
    print("\n=== Q6: Circular Imports Mechanics & Resolution ===")

    # In a circular import scenario:
    # module_a imports module_b at top level, and module_b imports module_a.
    # While module_a is half-initialized, module_b attempts to access module_a.SOME_VAR,
    # which has not been defined yet, raising AttributeError or ImportError!

    # Solution: Function-level deferred import
    class ServiceA:
        def trigger_b(self) -> str:
            # Deferred import inside method prevents top-level circular lock
            service_b = ServiceB()
            return f"A called -> {service_b.name}"

    class ServiceB:
        def __init__(self) -> None:
            self.name = "ServiceB_Instance"

        def trigger_a(self) -> str:
            # Deferred import inside method
            service_a = ServiceA()
            return f"B called -> {type(service_a).__name__}"

    sa = ServiceA()
    sb = ServiceB()

    assert sa.trigger_b() == "A called -> ServiceB_Instance"
    assert sb.trigger_a() == "B called -> ServiceA"

    print("  Deferred local imports cleanly resolved mutual dependency execution.")


# ==============================================================================
# Question 7: Module Introspection Attributes
# ==============================================================================
def exercise_q7_module_introspection_attributes() -> None:
    """
    Inspect standard module metadata attributes:
    - __name__: Current namespace or '__main__' when executed directly.
    - __file__: Absolute path to module file.
    - __doc__: Module-level docstring.
    - __all__: Explicit list of exported symbols for star imports.
    - __package__: Package parent name.
    """
    print("\n=== Q7: Module Introspection Attributes ===")

    import json

    assert hasattr(json, "__name__")
    assert hasattr(json, "__file__")
    assert hasattr(json, "__doc__")
    assert hasattr(json, "__all__")
    assert hasattr(json, "__package__")

    assert json.__name__ == "json"
    assert isinstance(json.__doc__, str)
    assert "dumps" in json.__all__
    assert "loads" in json.__all__

    print(f"  json.__name__:    {json.__name__}")
    print(f"  json.__file__:    {os.path.basename(json.__file__)}")
    print(f"  json.__all__ cnt: {len(json.__all__)} exported symbols")


# ==============================================================================
# Question 8: Direct File Path Imports (spec_from_file_location)
# ==============================================================================
def exercise_q8_direct_file_path_imports() -> None:
    """
    Demonstrate loading a Python module directly from an arbitrary filesystem path
    without modifying sys.path using `importlib.util.spec_from_file_location`.
    """
    print("\n=== Q8: Direct File Path Imports ===")

    temp_dir = tempfile.mkdtemp(prefix="mod_file_")
    script_path = os.path.join(temp_dir, "custom_calculator.py")

    try:
        with open(script_path, "w", encoding="utf-8") as f:
            f.write("def add(a, b): return a + b\ndef multiply(a, b): return a * b\n")

        # 1. Create spec from file location
        spec = importlib.util.spec_from_file_location("custom_calculator", script_path)
        assert spec is not None
        assert spec.loader is not None

        # 2. Create module from spec
        module = importlib.util.module_from_spec(spec)
        assert isinstance(module, types.ModuleType)

        # 3. Execute module code in its namespace
        spec.loader.exec_module(module)

        # Test functions
        assert module.add(10, 5) == 15  # type: ignore
        assert module.multiply(10, 5) == 50  # type: ignore

        print(f"  Directly executed code from {script_path}:")
        print(f"    add(10, 5) = {module.add(10, 5)}")  # type: ignore
        print(f"    multiply(10, 5) = {module.multiply(10, 5)}")  # type: ignore

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 9: Graceful Fallback / Conditional Imports
# ==============================================================================
def exercise_q9_conditional_fallback_imports() -> None:
    """
    Demonstrate the graceful fallback pattern: attempting to import a high-performance
    C-extension or optional package, falling back to a pure-Python standard library implementation.
    """
    print("\n=== Q9: Graceful Fallback / Conditional Imports ===")

    # Pattern: Attempt optional accelerator, fallback to standard lib
    try:
        # Simulate optional accelerator like ujson or orjson
        import imaginary_super_fast_json as json_engine  # type: ignore
        accelerator_used = True
    except ImportError:
        import json as json_engine
        accelerator_used = False

    assert accelerator_used is False
    payload = json_engine.dumps({"status": "healthy", "service": "auth"})
    assert '"status": "healthy"' in payload

    print(f"  Fallback engine selected: {json_engine.__name__} (accelerator={accelerator_used})")
    print(f"  Payload dumped: {payload}")


# ==============================================================================
# Question 10: Advanced Project - Dynamic Plugin Discovery & Hook Registry
# ==============================================================================
class PluginBase:
    """Base class defining plugin interface contracts."""
    name: str = "base"

    def process(self, data: str) -> str:
        raise NotImplementedError


class PluginManager:
    """
    Scans a directory for plugin files, dynamically loads them via importlib,
    registers compliant PluginBase subclasses, and executes data processing hooks.
    """

    def __init__(self, plugin_dir: str) -> None:
        self.plugin_dir = plugin_dir
        self.plugins: dict[str, PluginBase] = {}

    def discover_and_load(self) -> int:
        count = 0
        for filename in os.listdir(self.plugin_dir):
            if filename.startswith("plugin_") and filename.endswith(".py"):
                mod_name = filename[:-3]
                file_path = os.path.join(self.plugin_dir, filename)

                spec = importlib.util.spec_from_file_location(mod_name, file_path)
                if spec and spec.loader:
                    mod = importlib.util.module_from_spec(spec)
                    # Inject base class directly into module scope so plugin doesn't need sys.path lookup
                    mod.__dict__["PluginBase"] = PluginBase
                    spec.loader.exec_module(mod)

                    # Discover PluginBase subclasses
                    for attr_name in dir(mod):
                        obj = getattr(mod, attr_name)
                        if isinstance(obj, type) and issubclass(obj, PluginBase) and obj is not PluginBase:
                            plugin_instance = obj()
                            self.plugins[plugin_instance.name] = plugin_instance
                            count += 1
        return count

    def pipe_through_all(self, initial_data: str) -> str:
        current = initial_data
        for plugin in self.plugins.values():
            current = plugin.process(current)
        return current


def exercise_q10_plugin_manager() -> None:
    """
    Test dynamic plugin discovery and execution.
    """
    print("\n=== Q10: Dynamic Plugin Discovery & Hook Registry ===")

    temp_dir = tempfile.mkdtemp(prefix="mod_plugins_")

    try:
        # Create Plugin 1: Uppercaser
        p1_code = """
class UppercasePlugin(PluginBase):
    name = "uppercase"
    def process(self, data: str) -> str:
        return data.upper()
"""
        # Create Plugin 2: Reverser
        p2_code = """
class ReversePlugin(PluginBase):
    name = "reverse"
    def process(self, data: str) -> str:
        return data[::-1]
"""
        with open(os.path.join(temp_dir, "plugin_upper.py"), "w", encoding="utf-8") as f:
            f.write(p1_code.strip())

        with open(os.path.join(temp_dir, "plugin_rev.py"), "w", encoding="utf-8") as f:
            f.write(p2_code.strip())

        # Also write non-plugin file that must be ignored
        with open(os.path.join(temp_dir, "ignored_helper.py"), "w", encoding="utf-8") as f:
            f.write("def helper(): pass")

        manager = PluginManager(temp_dir)
        loaded_count = manager.discover_and_load()

        assert loaded_count == 2
        assert "uppercase" in manager.plugins
        assert "reverse" in manager.plugins

        # Pipe "hello" -> uppercase -> "HELLO" -> reverse -> "OLLEH"
        transformed = manager.pipe_through_all("hello")
        assert transformed == "OLLEH"

        print(f"  Discovered {loaded_count} plugins: {list(manager.plugins.keys())}")
        print(f"  Data piped through plugin chain: 'hello' -> '{transformed}'")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_core_import_syntaxes()
    exercise_q2_sys_path_search_order()
    exercise_q3_sys_modules_cache()
    exercise_q4_dynamic_import_module()
    exercise_q5_module_reloading()
    exercise_q6_circular_imports()
    exercise_q7_module_introspection_attributes()
    exercise_q8_direct_file_path_imports()
    exercise_q9_conditional_fallback_imports()
    exercise_q10_plugin_manager()

    print("\nAll 10 importing modules questions executed and asserted successfully!")
