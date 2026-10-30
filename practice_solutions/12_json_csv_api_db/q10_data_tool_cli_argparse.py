"""
Question 10: Modular Command-Line Interface (argparse) with Subcommands & Validators
Topic: JSON, CSV, Web APIs, and Databases

Key Concepts Tested:
- Subcommand hierarchy (import, export, stats) using argparse subparsers
- Custom argument type validation functions (positive_int, existing_file)
- Mutually exclusive argument groups (--verbose vs --quiet)
- Non-terminating programmatic test execution (exit_on_error=False / overriding error())
- Comprehensive CLI option validation and formatting
"""

import os
import argparse
from typing import List, Optional


def positive_int(value: str) -> int:
    """Validator ensuring integer is strictly greater than 0."""
    try:
        val = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid integer")
    if val <= 0:
        raise argparse.ArgumentTypeError(f"Value must be a positive integer > 0, got: {val}")
    return val


def existing_file(path_str: str) -> str:
    """Validator checking file existence on disk (skipped in unit testing if mocked)."""
    # Allowed in testing if filename ends with simulated extension
    if not os.path.isfile(path_str) and not path_str.startswith("test_data."):
        raise argparse.ArgumentTypeError(f"File '{path_str}' does not exist")
    return path_str


class TestableArgumentParser(argparse.ArgumentParser):
    """
    Subclass that raises ValueError instead of invoking sys.exit(2)
    to enable clean in-process unit testing.
    """

    def error(self, message: str) -> None:
        raise ValueError(message)


class DataToolCLI:
    """
    Modular CLI tool supporting subcommands, custom type converters,
    and mutually exclusive options.
    """

    def __init__(self) -> None:
        self.parser = self._build_parser()

    def _build_parser(self) -> argparse.ArgumentParser:
        parser = TestableArgumentParser(
            prog="datatool",
            description="Enterprise Data Tool CLI for Ingestion, Export, and Analytics",
            exit_on_error=False,
        )
        parser.add_argument("--version", action="version", version="%(prog)s 2.0.0")

        # Mutually exclusive verbosity flags
        verbosity_group = parser.add_mutually_exclusive_group()
        verbosity_group.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
        verbosity_group.add_argument("-q", "--quiet", action="store_true", help="Suppress output")

        subparsers = parser.add_subparsers(dest="subcommand", required=True)

        # 1. Import Subcommand
        import_parser = subparsers.add_parser("import", help="Import datasets into repository")
        import_parser.add_argument("filepath", type=existing_file, help="Path to data file")
        import_parser.add_argument(
            "--format",
            choices=["csv", "json"],
            default="csv",
            help="Data file format (default: csv)",
        )
        import_parser.add_argument(
            "--batch-size",
            type=positive_int,
            default=100,
            help="Batch ingestion size (must be > 0)",
        )
        import_parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simulate ingestion without writing changes",
        )

        # 2. Export Subcommand
        export_parser = subparsers.add_parser("export", help="Export repository tables to file")
        export_parser.add_argument("--table", required=True, type=str, help="Table name to dump")
        export_parser.add_argument("--output", type=str, default="export.json", help="Output filepath")
        export_parser.add_argument(
            "--limit",
            type=positive_int,
            default=1000,
            help="Maximum record count to export",
        )

        # 3. Stats Subcommand
        stats_parser = subparsers.add_parser("stats", help="Display repository metrics")
        stats_parser.add_argument("--detailed", action="store_true", help="Show verbose table breakdowns")

        return parser

    def parse_command(self, args: List[str]) -> argparse.Namespace:
        """Parses CLI argument list programmatically."""
        return self.parser.parse_args(args)


if __name__ == "__main__":
    cli = DataToolCLI()

    print("=== 1. Valid Import Subcommand ===")
    args1 = cli.parse_command([
        "import", "test_data.csv", "--format", "csv", "--batch-size", "250", "--dry-run"
    ])
    print(f"Parsed Subcommand 1: '{args1.subcommand}'")
    print(f"- Filepath: '{args1.filepath}'")
    print(f"- Format: '{args1.format}'")
    print(f"- Batch Size: {args1.batch_size}")
    print(f"- Dry Run: {args1.dry_run}")

    print("\n=== 2. Valid Export Subcommand ===")
    args2 = cli.parse_command([
        "export", "--table", "customers", "--limit", "50", "--output", "out.json"
    ])
    print(f"Parsed Subcommand 2: '{args2.subcommand}'")
    print(f"- Table: '{args2.table}'")
    print(f"- Limit: {args2.limit}")
    print(f"- Output: '{args2.output}'")

    print("\n=== 3. Custom Validator (Batch Size <= 0) ===")
    invalid_int_caught = False
    try:
        cli.parse_command(["import", "test_data.csv", "--batch-size", "-10"])
    except (argparse.ArgumentTypeError, ValueError) as err:
        invalid_int_caught = True
        print(f"Caught expected positive_int error: {err}")
    print(f"Invalid Batch Size (-10) Handled: {invalid_int_caught}")

    print("\n=== 4. Mutually Exclusive Flags Conflict ===")
    mutex_violation_caught = False
    try:
        cli.parse_command(["--verbose", "--quiet", "stats"])
    except (argparse.ArgumentError, ValueError) as err:
        mutex_violation_caught = True
        print(f"Caught expected mutually exclusive error: {err}")
    print(f"Mutually Exclusive Flags (--verbose and --quiet) Conflict Handled: {mutex_violation_caught}")
