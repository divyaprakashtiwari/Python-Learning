"""
Topic 08: Modules and Packages - Question 03: __name__ == "__main__"

A comprehensive collection of 10 standalone, runnable exercises exploring
Python's script execution entry point (`if __name__ == "__main__":`),
module vs script duality, sys.exit codes, python -m execution, __main__.py packages,
sys.argv and argparse CLI tools.

Questions Covered:
 1. __name__ Variable Mechanics: Differences between direct execution and module import.
 2. The Canonical main() Entry Point: Structuring script logic cleanly inside a main() function.
 3. OS Exit Codes with sys.exit(): Returning 0 for success and non-zero for error states.
 4. Executing Modules as Scripts via python -m: How -m discovers and executes packages.
 5. Executable Directories via __main__.py: Running a multi-file directory directly.
 6. Command-Line Arguments via sys.argv: Accessing and validating raw CLI parameters.
 7. Declarative CLI Parsing with argparse: Flags, positional args, types, and defaults.
 8. Dual-Use Modules: Designing code that is both an importable library and a standalone CLI tool.
 9. Programmatic Testing of __main__: Invoking entry points safely with mock arguments.
10. Advanced Project: Production-Ready Subcommand Dispatch CLI Runner with exit code management.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from typing import Any


# ==============================================================================
# Question 1: __name__ Variable Mechanics
# ==============================================================================
def exercise_q1_name_mechanics() -> None:
    """
    Demonstrate that `__name__` evaluates to `"__main__"` when a file is executed
    directly, but evaluates to the module's qualified name when imported.
    """
    print("=== Q1: __name__ Variable Mechanics ===")

    temp_dir = tempfile.mkdtemp(prefix="name_main_")
    mod_file = os.path.join(temp_dir, "name_reporter.py")

    try:
        code = '''
def get_current_name() -> str:
    return __name__

RECORDED_NAME = __name__
'''
        with open(mod_file, "w", encoding="utf-8") as f:
            f.write(code)

        sys.path.insert(0, temp_dir)

        # 1. When imported, __name__ is the module name
        import name_reporter  # type: ignore
        assert name_reporter.get_current_name() == "name_reporter"
        assert name_reporter.RECORDED_NAME == "name_reporter"

        # 2. When run directly as a script via subprocess, __name__ is "__main__"
        script_run = """
import name_reporter
print(f"RUN_AS:{__name__}")
"""
        runner_file = os.path.join(temp_dir, "runner.py")
        with open(runner_file, "w", encoding="utf-8") as f:
            f.write(script_run)

        result = subprocess.run(
            [sys.executable, runner_file],
            capture_output=True,
            text=True,
            check=True,
        )
        assert "RUN_AS:__main__" in result.stdout

        print("  Imported module __name__: 'name_reporter'")
        print("  Directly executed script __name__: '__main__'")

    finally:
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        sys.modules.pop("name_reporter", None)
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 2: The Canonical main() Entry Point
# ==============================================================================
def exercise_q2_canonical_main_pattern() -> None:
    """
    Demonstrate structuring scripts with a distinct main() function.
    Prevents polluting module-level global scope with temporary variables.
    """
    print("\n=== Q2: The Canonical main() Entry Point ===")

    def main_routine(args: list[str]) -> dict[str, Any]:
        """Encapsulated script execution logic."""
        records_processed = len(args)
        status = "COMPLETED"
        return {"count": records_processed, "status": status}

    # Simulate invocation
    output = main_routine(["file1.txt", "file2.txt"])
    assert output["count"] == 2
    assert output["status"] == "COMPLETED"

    print(f"  Canonical main routine output: {output}")


# ==============================================================================
# Question 3: OS Exit Codes with sys.exit()
# ==============================================================================
def exercise_q3_os_exit_codes() -> None:
    """
    Demonstrate passing exit codes back to the parent operating system:
    - 0 indicates clean success.
    - 1-255 indicates an error or failure condition.
    """
    print("\n=== Q3: OS Exit Codes with sys.exit() ===")

    temp_dir = tempfile.mkdtemp(prefix="name_exit_")

    try:
        # Script that exits with code 0 on success
        success_script = os.path.join(temp_dir, "exit_success.py")
        with open(success_script, "w", encoding="utf-8") as f:
            f.write("import sys\nsys.exit(0)\n")

        res_ok = subprocess.run([sys.executable, success_script])
        assert res_ok.returncode == 0

        # Script that exits with error code 42
        fail_script = os.path.join(temp_dir, "exit_fail.py")
        with open(fail_script, "w", encoding="utf-8") as f:
            f.write("import sys\nsys.exit(42)\n")

        res_fail = subprocess.run([sys.executable, fail_script])
        assert res_fail.returncode == 42

        print(f"  Clean exit returned OS code: {res_ok.returncode}")
        print(f"  Error exit returned OS code: {res_fail.returncode}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 4: Executing Modules via python -m
# ==============================================================================
def exercise_q4_python_minus_m() -> None:
    """
    Demonstrate executing a module as a script using `python -m <module>`.
    Example: standard library `timeit` or `json.tool`.
    """
    print("\n=== Q4: Executing Modules via python -m ===")

    # Run Python's built-in timeit module via -m flag
    result = subprocess.run(
        [sys.executable, "-m", "timeit", "-n", "10", "-r", "1", "sum([1, 2, 3])"],
        capture_output=True,
        text=True,
        check=True,
    )

    assert "loop" in result.stdout or "usec" in result.stdout or "nsec" in result.stdout
    print("  Successfully executed standard library module via 'python -m timeit':")
    print(f"    {result.stdout.strip()}")


# ==============================================================================
# Question 5: Executable Directories via __main__.py
# ==============================================================================
def exercise_q5_executable_package_directory() -> None:
    """
    Demonstrate that adding a `__main__.py` file inside a package folder makes
    the entire directory executable by name (`python my_package_dir`).
    """
    print("\n=== Q5: Executable Directories via __main__.py ===")

    temp_dir = tempfile.mkdtemp(prefix="name_pkg_")
    pkg_dir = os.path.join(temp_dir, "app_tool")
    os.makedirs(pkg_dir)

    try:
        # Create __init__.py
        with open(os.path.join(pkg_dir, "__init__.py"), "w", encoding="utf-8") as f:
            f.write("APP_NAME = 'PackageCLI'\n")

        # Create __main__.py (entry point for directory execution)
        with open(os.path.join(pkg_dir, "__main__.py"), "w", encoding="utf-8") as f:
            f.write("import sys\nprint('EXECUTED_FROM_PACKAGE_MAIN')\nsys.exit(0)\n")

        # Run directory directly: python app_tool
        result = subprocess.run(
            [sys.executable, pkg_dir],
            capture_output=True,
            text=True,
            check=True,
        )

        assert "EXECUTED_FROM_PACKAGE_MAIN" in result.stdout
        print(f"  Successfully ran directory {os.path.basename(pkg_dir)} directly via __main__.py.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 6: Command-Line Arguments via sys.argv
# ==============================================================================
def parse_raw_cli_args(argv_list: list[str]) -> dict[str, Any]:
    """
    Parses low-level sys.argv list.
    argv_list[0] is the script name; subsequent items are arguments.
    """
    if len(argv_list) < 2:
        return {"command": "help", "args": []}

    return {
        "script": argv_list[0],
        "command": argv_list[1],
        "args": argv_list[2:],
    }


def exercise_q6_sys_argv() -> None:
    """
    Demonstrate parsing raw command-line parameters from sys.argv.
    """
    print("\n=== Q6: Command-Line Arguments via sys.argv ===")

    sample_argv = ["deploy_tool.py", "build", "--env=prod", "--verbose"]
    parsed = parse_raw_cli_args(sample_argv)

    assert parsed["script"] == "deploy_tool.py"
    assert parsed["command"] == "build"
    assert parsed["args"] == ["--env=prod", "--verbose"]

    print(f"  Parsed command: {parsed['command']}, args: {parsed['args']}")


# ==============================================================================
# Question 7: Declarative CLI Parsing with argparse
# ==============================================================================
def create_cli_parser() -> argparse.ArgumentParser:
    """
    Constructs a standard declarative CLI argument parser with options, flags, and types.
    """
    parser = argparse.ArgumentParser(description="Image Processor CLI Tool")
    parser.add_argument("input_path", type=str, help="Path to input image")
    parser.add_argument("--quality", type=int, default=85, help="Output compression quality (1-100)")
    parser.add_argument("--grayscale", action="store_true", help="Convert image to grayscale")
    return parser


def exercise_q7_argparse_cli() -> None:
    """
    Test declarative argument parsing with argparse.
    """
    print("\n=== Q7: Declarative CLI Parsing with argparse ===")

    parser = create_cli_parser()

    # Test 1: Standard arguments
    args1 = parser.parse_args(["photo.jpg", "--quality", "95", "--grayscale"])
    assert args1.input_path == "photo.jpg"
    assert args1.quality == 95
    assert args1.grayscale is True

    # Test 2: Defaults
    args2 = parser.parse_args(["banner.png"])
    assert args2.input_path == "banner.png"
    assert args2.quality == 85
    assert args2.grayscale is False

    print(f"  Parsed image: {args1.input_path}, quality: {args1.quality}, gray: {args1.grayscale}")
    print(f"  Parsed defaults: quality: {args2.quality}, gray: {args2.grayscale}")


# ==============================================================================
# Question 8: Dual-Use Modules (Library + CLI Tool)
# ==============================================================================
# Library function
def format_currency(amount: float, symbol: str = "$") -> str:
    """Pure library function for external imports."""
    return f"{symbol}{amount:,.2f}"


def _dual_use_cli_main(cli_args: list[str]) -> int:
    """CLI handler invoked only when run as main."""
    if not cli_args:
        print("Usage: currency_formatter <amount> [symbol]")
        return 1
    amount = float(cli_args[0])
    symbol = cli_args[1] if len(cli_args) > 1 else "$"
    print(format_currency(amount, symbol))
    return 0


def exercise_q8_dual_use_modules() -> None:
    """
    Demonstrate module serving as both an importable library and a command-line script.
    """
    print("\n=== Q8: Dual-Use Modules ===")

    # 1. As an imported library:
    res = format_currency(1234567.89, "USD ")
    assert res == "USD 1,234,567.89"

    # 2. As an executed CLI tool:
    exit_code = _dual_use_cli_main(["5000.5", "$"])
    assert exit_code == 0

    print(f"  Library formatted result: {res}")
    print("  CLI handler executed cleanly.")


# ==============================================================================
# Question 9: Programmatic Testing of __main__ Blocks
# ==============================================================================
def exercise_q9_testing_main_blocks() -> None:
    """
    Demonstrate how to write unit tests for scripts with `__main__` entry points
    by monkeypatching `sys.argv` and capturing stdout.
    """
    print("\n=== Q9: Programmatic Testing of __main__ Blocks ===")

    import io
    import contextlib

    def script_entrypoint() -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--name", default="World")
        args = parser.parse_args(sys.argv[1:])
        print(f"Hello, {args.name}!")
        return 0

    # Test by overriding sys.argv and intercepting stdout
    captured_stream = io.StringIO()
    original_argv = sys.argv.copy()

    try:
        sys.argv = ["script_test.py", "--name", "Antigravity"]
        with contextlib.redirect_stdout(captured_stream):
            exit_code = script_entrypoint()

        assert exit_code == 0
        assert "Hello, Antigravity!" in captured_stream.getvalue()

        print(f"  Tested entry point cleanly: '{captured_stream.getvalue().strip()}'")

    finally:
        sys.argv = original_argv


# ==============================================================================
# Question 10: Advanced Project - Production Subcommand Dispatch CLI Runner
# ==============================================================================
class SubcommandRunner:
    """
    Production-grade CLI dispatcher supporting hierarchical subcommands:
    - 'run': executes workload with --dry-run option
    - 'status': inspects service health
    - 'config': reads/writes application settings
    """

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(prog="taskctl", description="Enterprise Task Runner")
        subparsers = self.parser.add_subparsers(dest="subcommand", required=True)

        # 'run' subcommand
        run_p = subparsers.add_parser("run", help="Run a scheduled task")
        run_p.add_argument("task_name", type=str, help="Name of task to execute")
        run_p.add_argument("--dry-run", action="store_true", help="Simulate execution without mutations")

        # 'status' subcommand
        status_p = subparsers.add_parser("status", help="Query service status")
        status_p.add_argument("--service", default="all", help="Filter by service name")

        # 'config' subcommand
        config_p = subparsers.add_parser("config", help="View configuration")
        config_p.add_argument("key", type=str, help="Configuration key name")

    def dispatch(self, args_list: list[str]) -> dict[str, Any]:
        args = self.parser.parse_args(args_list)

        if args.subcommand == "run":
            return {
                "action": "RUN",
                "task": args.task_name,
                "dry_run": args.dry_run,
                "exit_code": 0,
            }
        elif args.subcommand == "status":
            return {
                "action": "STATUS",
                "service": args.service,
                "health": "UP",
                "exit_code": 0,
            }
        elif args.subcommand == "config":
            return {
                "action": "CONFIG",
                "key": args.key,
                "value": "prod_active",
                "exit_code": 0,
            }
        raise ValueError("Invalid subcommand")


def exercise_q10_subcommand_dispatch_runner() -> None:
    """
    Test SubcommandRunner across various CLI commands.
    """
    print("\n=== Q10: Production Subcommand Dispatch CLI Runner ===")

    cli = SubcommandRunner()

    # 1. Test 'run' with --dry-run
    res_run = cli.dispatch(["run", "backup_db", "--dry-run"])
    assert res_run["action"] == "RUN"
    assert res_run["task"] == "backup_db"
    assert res_run["dry_run"] is True

    # 2. Test 'status'
    res_status = cli.dispatch(["status", "--service", "billing"])
    assert res_status["action"] == "STATUS"
    assert res_status["service"] == "billing"
    assert res_status["health"] == "UP"

    # 3. Test 'config'
    res_cfg = cli.dispatch(["config", "MAX_WORKERS"])
    assert res_cfg["action"] == "CONFIG"
    assert res_cfg["key"] == "MAX_WORKERS"

    print(f"  Subcommand 'run':    {res_run}")
    print(f"  Subcommand 'status': {res_status}")
    print(f"  Subcommand 'config': {res_cfg}")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_name_mechanics()
    exercise_q2_canonical_main_pattern()
    exercise_q3_os_exit_codes()
    exercise_q4_python_minus_m()
    exercise_q5_executable_package_directory()
    exercise_q6_sys_argv()
    exercise_q7_argparse_cli()
    exercise_q8_dual_use_modules()
    exercise_q9_testing_main_blocks()
    exercise_q10_subcommand_dispatch_runner()

    print("\nAll 10 __name__ == '__main__' questions executed and asserted successfully!")
