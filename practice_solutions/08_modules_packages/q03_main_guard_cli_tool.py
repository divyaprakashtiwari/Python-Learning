"""
Topic 08 - Modules and Packages: Question 3
Problem: Dual-Mode Cryptographic Utility demonstrating if __name__ == "__main__" and CLI dispatch.
"""

import argparse
import hashlib
import os
import sys
from typing import List, Optional


# 1. Reusable Library API (When Imported)
def hash_string(text: str, algorithm: str = "sha256") -> str:
    """Computes cryptographic hex digest for a text string."""
    algo_lower = algorithm.lower()
    allowed = {"sha256", "sha512", "md5"}
    if algo_lower not in allowed:
        raise ValueError(f"Unsupported algorithm '{algorithm}'. Choose from {allowed}")

    hasher = hashlib.new(algo_lower)
    hasher.update(text.encode("utf-8"))
    return hasher.hexdigest()


def hash_file_stream(filepath: str, algorithm: str = "sha256", chunk_size: int = 65536) -> str:
    """Streams a file in binary chunks and computes cryptographic digest."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Target file not found: {filepath}")

    algo_lower = algorithm.lower()
    allowed = {"sha256", "sha512", "md5"}
    if algo_lower not in allowed:
        raise ValueError(f"Unsupported algorithm '{algorithm}'. Choose from {allowed}")

    hasher = hashlib.new(algo_lower)
    with open(filepath, mode="rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hasher.update(chunk)

    return hasher.hexdigest()


# 2. CLI Dispatch Entry Point
def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point parsing arguments and returning standard process exit codes."""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Cryptographic Hashing CLI Utility", add_help=False)
    parser.add_argument("--algo", default="sha256", help="Hash algorithm (sha256, sha512, md5)")
    parser.add_argument("--text", help="String payload to hash")
    parser.add_argument("--file", help="Filepath to hash")

    try:
        args, _ = parser.parse_known_args(argv)
    except Exception as parse_err:
        print(f"Error parsing arguments: {parse_err}", file=sys.stderr)
        return 2

    # Enforce exactly one of --text or --file
    has_text = args.text is not None
    has_file = args.file is not None

    if (has_text and has_file) or (not has_text and not has_file):
        print("Error: Exactly one of --text or --file must be specified.", file=sys.stderr)
        return 2

    try:
        if has_text:
            digest = hash_string(args.text, algorithm=args.algo)
        else:
            digest = hash_file_stream(args.file, algorithm=args.algo)

        print(f"{args.algo.upper()}: {digest}")
        return 0

    except Exception as err:
        print(f"Execution Error: {err}", file=sys.stderr)
        return 1


# 3. Demonstration & Standalone Execution Guard
if __name__ == "__main__":
    # If invoked directly without arguments, run demonstration suite
    if len(sys.argv) <= 1:
        print("Library Import Call Result:")
        h_val = hash_string("Hello World", algorithm="sha256")
        print(h_val)

        print("\nCLI Execution Output:")
        sys.stdout.flush()
        cli_exit_code = main(["--algo", "sha256", "--text", "Hello World"])
        print(f"CLI Exit Code: {cli_exit_code}")

        print("\nCLI Missing Arguments Error:")
        sys.stdout.flush()
        cli_error_code = main([])
        sys.stderr.flush()
        print(f"CLI Exit Code: {cli_error_code}")
    else:
        # Standard CLI execution
        sys.exit(main(sys.argv[1:]))
