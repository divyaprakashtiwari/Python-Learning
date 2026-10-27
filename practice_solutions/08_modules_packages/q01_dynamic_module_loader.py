"""
Topic 08 - Modules and Packages: Question 1
Problem: Dynamic Module Introspection and Loader Utility using importlib and sys.modules.
"""

import importlib
import os
import sys
from typing import Any, Dict


class ModulePluginManager:
    """Manages runtime module discovery, dynamic loading, and reflection."""

    def add_lookup_path(self, dir_path: str) -> bool:
        """Prepends a directory to sys.path giving it top lookup priority."""
        abs_path = os.path.abspath(dir_path)
        if not os.path.isdir(abs_path):
            raise NotADirectoryError(f"Directory not found: {abs_path}")

        if abs_path not in sys.path:
            sys.path.insert(0, abs_path)
            return True
        return False

    def load_and_inspect_module(self, module_name: str) -> Dict[str, Any]:
        """Dynamically imports a module and inspects its cache status, origin, and exports."""
        was_cached = module_name in sys.modules

        # Dynamically import or fetch from cache
        module = importlib.import_module(module_name)
        file_location = getattr(module, "__file__", "BUILT_IN") or "BUILT_IN"

        public_callables = sorted([
            attr for attr in dir(module)
            if not attr.startswith("_") and callable(getattr(module, attr, None))
        ])

        return {
            "name": module.__name__,
            "file_location": file_location,
            "is_cached": was_cached,
            "public_callables": public_callables
        }

    def execute_plugin_function(self, module_name: str, function_name: str, *args: Any, **kwargs: Any) -> Any:
        """Looks up and executes a function dynamically by name from a module."""
        module = importlib.import_module(module_name)
        func = getattr(module, function_name, None)
        if func is None or not callable(func):
            raise AttributeError(f"Function '{function_name}' not found in '{module_name}'")

        return func(*args, **kwargs)


# Verification & Execution
manager = ModulePluginManager()
math_info = manager.load_and_inspect_module("math")
result_sqrt = manager.execute_plugin_function("math", "sqrt", 144)

print("Module Introspection (math):")
print(f"- Name: {math_info['name']}")
print(f"- File Location: {math_info['file_location']}")
print(f"- Was Already Cached: {math_info['is_cached']}")
print(f"- Sample Public Callables: {math_info['public_callables'][:10]} ...")
print(f"Dynamic Invocation (math.sqrt(144)): {result_sqrt}")

# Invocation of missing function
print("\nAttempting invocation of missing function ('non_existent_fn'):")
try:
    manager.execute_plugin_function("math", "non_existent_fn")
except AttributeError as err:
    print(f'Caught Expected: AttributeError("{err}")')
