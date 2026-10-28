"""
Question 5: Environment & Stream Sandbox Context Manager
Topic: Advanced Python

Key Concepts Tested:
- Context manager protocol (__enter__, __exit__)
- State isolation and teardown guarantees
- Reversible environment mutations (os.environ)
- I/O stream redirection (sys.stdout to io.StringIO)
- Reentrancy / nesting support across stacked context scopes
"""

import sys
import os
import io
from typing import Dict, Optional, Any


class ExecutionSandbox:
    """
    Context manager that temporarily overrides environment variables
    and optionally redirects standard output to an in-memory buffer.
    Guarantees clean restoration upon scope exit, even if exceptions occur.
    """

    def __init__(self, env_overrides: Dict[str, str], capture_stdout: bool = False) -> None:
        self.env_overrides = env_overrides
        self.capture_stdout = capture_stdout
        self._previous_env: Dict[str, Optional[str]] = {}
        self.captured_output: Optional[io.StringIO] = io.StringIO() if capture_stdout else None
        self._original_stdout: Optional[Any] = None

    def __enter__(self) -> "ExecutionSandbox":
        # 1. Backup current environment state
        for key in self.env_overrides:
            if key in os.environ:
                self._previous_env[key] = os.environ[key]
            else:
                self._previous_env[key] = None

        # 2. Apply environment overrides
        for key, value in self.env_overrides.items():
            os.environ[key] = str(value)

        # 3. Redirect stdout if requested
        if self.capture_stdout and self.captured_output is not None:
            self._original_stdout = sys.stdout
            sys.stdout = self.captured_output

        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        # 1. Restore standard output
        if self._original_stdout is not None:
            sys.stdout = self._original_stdout
            self._original_stdout = None

        # 2. Revert environment variables to backed-up state
        for key, previous_val in self._previous_env.items():
            if previous_val is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = previous_val

        # Do not suppress exceptions
        return False


if __name__ == "__main__":
    # Setup initial environment
    os.environ["APP_ENV"] = "production"
    os.environ["API_KEY"] = "prod-secret-999"

    print("=== Initial Environment State ===")
    print(f"APP_ENV: '{os.environ.get('APP_ENV')}', API_KEY: '{os.environ.get('API_KEY')}'")

    print("\n=== Executing Sandbox with Stdout Capture & Nested Scope ===")
    with ExecutionSandbox(
        env_overrides={"APP_ENV": "staging", "NEW_FLAG": "ENABLED"},
        capture_stdout=True
    ) as sandbox:
        print("Executing staging dry run...")
        inside_env = os.environ.get("APP_ENV")
        inside_flag = os.environ.get("NEW_FLAG")

        # Nested sub-scope with further overrides
        with ExecutionSandbox(env_overrides={"APP_ENV": "testing"}):
            nested_env = os.environ.get("APP_ENV")

        post_nested_env = os.environ.get("APP_ENV")

    # Outside sandbox
    post_sandbox_env = os.environ.get("APP_ENV")
    is_new_flag_cleaned = "NEW_FLAG" not in os.environ
    stdout_result = sandbox.captured_output.getvalue().strip() if sandbox.captured_output else ""

    print(f"Inside Sandbox: APP_ENV = '{inside_env}', NEW_FLAG = '{inside_flag}'")
    print(f"Inside Nested:  APP_ENV = '{nested_env}'")
    print(f"After Nested:   APP_ENV = '{post_nested_env}' (Cleanly restored to outer scope)")
    print(f"Captured Stdout: '{stdout_result}'")

    print("\n=== Post-Sandbox Verification ===")
    print(f"- APP_ENV: '{post_sandbox_env}' (Fully restored)")
    print(f"- NEW_FLAG in os.environ: {not is_new_flag_cleaned} (Newly created key purged: {is_new_flag_cleaned})")
    print(f"- sys.stdout redirected back to system terminal: {sys.stdout is sys.__stdout__}")

    print("\n=== Exception Teardown Guarantee Verification ===")
    try:
        with ExecutionSandbox(env_overrides={"APP_ENV": "emergency_fix"}):
            raise RuntimeError("Fatal database connection crash!")
    except RuntimeError as err:
        print(f"Caught deliberate exception: {err}")

    print(f"- Post-exception APP_ENV restored: '{os.environ.get('APP_ENV')}' (Matches 'production': {os.environ.get('APP_ENV') == 'production'})")
