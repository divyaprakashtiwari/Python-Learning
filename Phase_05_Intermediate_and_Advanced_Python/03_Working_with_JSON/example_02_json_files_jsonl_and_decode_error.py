"""
Phase 5 - Topic 03: Working with JSON
Example 02: File-Based JSON (`json.dump` / `json.load`), JSON Lines (`.jsonl`), & `JSONDecodeError`

Demonstrates:
  - Writing and reading a JSON configuration file via `json.dump()` and `json.load()`
  - Streaming newline-delimited JSON (`.jsonl` / NDJSON) logs line by line
  - Catching `json.JSONDecodeError` with exact line and column diagnostics (`err.lineno`, `err.colno`)
"""

import json
from pathlib import Path
import tempfile


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_path = Path(tmp_dir) / "settings.json"
        jsonl_path = Path(tmp_dir) / "events.jsonl"

        print("=== 1. Writing & Reading `settings.json` (`json.dump` / `json.load`) ===")
        with open(config_path, mode="w", encoding="utf-8") as fh:
            json.dump({"host": "127.0.0.1", "port": 8000, "debug": False}, fh, indent=2)

        with open(config_path, mode="r", encoding="utf-8") as fh:
            loaded_cfg = json.load(fh)
        print(f"  Loaded config: {loaded_cfg}")

        print("\n=== 2. Streaming JSON Lines (`.jsonl`) ===")
        events = [
            {"event": "login", "user": "aarav"},
            {"event": "purchase", "user": "diya", "amount": 1499},
        ]
        with open(jsonl_path, mode="w", encoding="utf-8") as fh:
            for ev in events:
                fh.write(json.dumps(ev) + "\n")

        with open(jsonl_path, mode="r", encoding="utf-8") as fh:
            for idx, line in enumerate(fh, start=1):
                record = json.loads(line)
                print(f"  JSONL Record #{idx}: {record}")

        print("\n=== 3. Handling Malformed JSON (`json.JSONDecodeError`) ===")
        corrupted = '{"user": "rohan", "active": true,}'  # Trailing comma is invalid in standard JSON
        try:
            json.loads(corrupted)
        except json.JSONDecodeError as err:
            print(f"  Caught JSONDecodeError: {err.msg} (line={err.lineno}, col={err.colno}, pos={err.pos})")


if __name__ == "__main__":
    main()
