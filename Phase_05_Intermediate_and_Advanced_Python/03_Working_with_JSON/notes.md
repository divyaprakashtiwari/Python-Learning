# Phase 5 — Topic 03: Working with JSON

## 1. Introduction

**JSON (JavaScript Object Notation)** is the universal language-independent text format for REST APIs, webhooks, NoSQL document stores, and configuration files. Python's built-in `json` standard library module translates seamlessly between Python data structures (`dict`, `list`, `str`, `int`, `float`, `bool`, `None`) and JSON strings or files.

Understanding how Python types map to JSON types—and how to serialize custom objects like `datetime.date`, `set`, or `@dataclass` instances—is a daily requirement in backend, data, and AI engineering.

---

## 2. Why is it used?

1. **Cross-Language Interoperability:** A Python microservice can serialize a dictionary with `json.dumps()` and send it over HTTP to a Go, Rust, TypeScript, or Java client with zero custom binary parsing.
2. **Structured Logging (`.jsonl` / NDJSON):** Modern observability pipelines (ELK, Datadog, CloudWatch) ingest newline-delimited JSON objects where each log line is a standalone JSON document.
3. **Safe Serialization:** Unlike `pickle`, which can execute arbitrary malicious code during deserialization, `json.loads()` only constructs harmless primitive containers.
4. **Extensible Hooks:** `default=` and `object_hook=` allow custom domain classes (`Decimal`, `UUID`, `date`, dataclasses) to round-trip cleanly.

---

## 3. Syntax

```python
import json

# 1. String-based Serialization & Deserialization (Notice the 's' = string)
json_str: str = json.dumps(data, indent=2, sort_keys=True)
restored: dict = json.loads(json_str)

# 2. File-based Serialization & Deserialization (No 's' = file stream)
with open("data.json", mode="w", encoding="utf-8") as fh:
    json.dump(data, fh, indent=2)

with open("data.json", mode="r", encoding="utf-8") as fh:
    loaded = json.load(fh)

# 3. Python <-> JSON Type Mapping Table
# Python `dict`        <-> JSON `object`  {...}
# Python `list`        <-> JSON `array`   [...]
# Python `tuple`        -> JSON `array`   [...] (decodes back as Python `list`!)
# Python `str`         <-> JSON `string`  "..."
# Python `int`/`float` <-> JSON `number`  42 / 3.14
# Python `True`/`False`<-> JSON `true`/`false`
# Python `None`        <-> JSON `null`
```

---

## 4. Explanation (Step-by-Step)

1. **`dumps`/`loads` vs `dump`/`load`:**
   - The trailing **`s`** stands for **string** (`json.dumps` returns a `str`; `json.loads` parses a `str` or `bytes`).
   - Without the **`s`**, `json.dump(obj, fp)` and `json.load(fp)` write to or read from an open **file-like object**.
2. **One-Way Type Coercions to Watch Out For:**
   - **Tuples become Lists:** JSON has only one sequence type (`array`), so `(1, 2)` serializes to `[1, 2]` and deserializes back as a `list`.
   - **Dictionary Keys Must Be Strings:** JSON object keys must be double-quoted strings. In Python, `json.dumps({101: "Alice"})` silently coerces the integer key `101` into the string key `"101"`.
3. **Custom Serialization with `default=`:**
   - When `json.dumps()` encounters an unsupported type (like `date`, `set`, or a custom class), it calls `default(obj)`, which must return a JSON-serializable structure or raise `TypeError`.
4. **Custom Deserialization with `object_hook=`:**
   - During `json.loads()`, Python calls `object_hook(dct)` for every decoded JSON `{...}` object from the innermost nested dictionary outward, letting you inspect a type tag (e.g., `"__type__"`) and return a custom class instance.

---

## 5. Minimum 3 Examples

### Example 01: `json.dumps()` and `json.loads()` — Pretty-Printing, Key Sorting, & Type Mapping
File: [`example_01_dumps_loads_formatting_and_types.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/03_Working_with_JSON/example_01_dumps_loads_formatting_and_types.py)

```python
"""
Phase 5 - Topic 03: Working with JSON
Example 01: `json.dumps()` and `json.loads()` — Pretty-Printing, Key Sorting, & Type Mapping

Demonstrates:
  - Converting Python objects (`dict`, `list`, `tuple`, `bool`, `None`) to JSON strings with `json.dumps()`
  - Controlling formatting (`indent=2`, `sort_keys=True`, `separators=(',', ':')`)
  - Parsing JSON strings back into Python objects with `json.loads()` (notice `tuple` becomes `list`)
"""

import json


def main() -> None:
    course_payload = {
        "title": "Python Complete Notes - Free Open Source",
        "phase": 5,
        "published": True,
        "prerequisites": ("Phase 1", "Phase 2", "Phase 3", "Phase 4"),
        "certificate_url": None,
        "metrics": {"topics": 142, "rating": 4.95},
    }

    print("=== 1. Pretty-Printed & Key-Sorted JSON String (`json.dumps`) ===")
    json_str = json.dumps(course_payload, indent=2, sort_keys=True)
    print(json_str)

    print("\n=== 2. Compact Wire Format (`separators=(',', ':')`) ===")
    compact_str = json.dumps(course_payload, separators=(",", ":"))
    print(f"  Length comparison: pretty={len(json_str)} chars vs compact={len(compact_str)} chars")

    print("\n=== 3. Round-Trip Parsing (`json.loads`) & Tuple->List Coercion ===")
    restored = json.loads(json_str)
    print(f"  Restored type: {type(restored).__name__} | published={restored['published']!r}")
    print(f"  Original prerequisites type: {type(course_payload['prerequisites']).__name__}")
    print(f"  Restored prerequisites type: {type(restored['prerequisites']).__name__} -> {restored['prerequisites']}")


if __name__ == "__main__":
    main()
```

### Example 02: File-Based JSON (`json.dump` / `json.load`), JSON Lines (`.jsonl`), & `JSONDecodeError`
File: [`example_02_json_files_jsonl_and_decode_error.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/03_Working_with_JSON/example_02_json_files_jsonl_and_decode_error.py)

```python
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
```

### Example 03: Custom Serialization (`default=`) & Deserialization (`object_hook=`)
File: [`example_03_custom_serialization_default_and_object_hook.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/03_Working_with_JSON/example_03_custom_serialization_default_and_object_hook.py)

```python
"""
Phase 5 - Topic 03: Working with JSON
Example 03: Custom Serialization (`default=`) & Deserialization (`object_hook=`)

Demonstrates:
  - Teaching `json.dumps()` how to serialize `datetime.date`, `set`, and custom classes
    using a custom `default=` serializer function
  - Reconstructing typed domain objects during `json.loads()` using `object_hook=`
"""

from dataclasses import dataclass
from datetime import date
import json


@dataclass(frozen=True)
class ReleaseBuild:
    version: str
    released_on: date
    tags: set[str]


def custom_json_default(obj: object) -> object:
    """Convert non-JSON-native Python types into tagged dictionaries."""
    if isinstance(obj, ReleaseBuild):
        return {
            "__type__": "ReleaseBuild",
            "version": obj.version,
            "released_on": obj.released_on.isoformat(),
            "tags": sorted(obj.tags),
        }
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def custom_json_object_hook(dct: dict[str, object]) -> object:
    """Reconstruct `ReleaseBuild` instances when `__type__ == 'ReleaseBuild'` is encountered."""
    if dct.get("__type__") == "ReleaseBuild":
        return ReleaseBuild(
            version=str(dct["version"]),
            released_on=date.fromisoformat(str(dct["released_on"])),
            tags=set(dct["tags"]),  # type: ignore[arg-type]
        )
    return dct


def main() -> None:
    build = ReleaseBuild(version="2.4.0", released_on=date(2026, 11, 4), tags={"stable", "lts"})

    print("=== 1. Serializing Custom Object with `default=custom_json_default` ===")
    encoded = json.dumps(build, default=custom_json_default, indent=2)
    print(encoded)

    print("\n=== 2. Deserializing Back to Domain Object with `object_hook=` ===")
    decoded = json.loads(encoded, object_hook=custom_json_object_hook)
    print(f"  Decoded object : {decoded!r}")
    print(f"  Equality check : {decoded == build} (type={type(decoded).__name__})")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== 1. Pretty-Printed & Key-Sorted JSON String (`json.dumps`) ===
{
  "certificate_url": null,
  "metrics": {
    "rating": 4.95,
    "topics": 142
  },
  "phase": 5,
  "prerequisites": [
    "Phase 1",
    "Phase 2",
    "Phase 3",
    "Phase 4"
  ],
  "published": true,
  "title": "Python Complete Notes - Free Open Source"
}

=== 2. Compact Wire Format (`separators=(',', ':')`) ===
  Length comparison: pretty=262 chars vs compact=199 chars

=== 3. Round-Trip Parsing (`json.loads`) & Tuple->List Coercion ===
  Restored type: dict | published=True
  Original prerequisites type: tuple
  Restored prerequisites type: list -> ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4']
```

### Output — Example 02
```text
=== 1. Writing & Reading `settings.json` (`json.dump` / `json.load`) ===
  Loaded config: {'host': '127.0.0.1', 'port': 8000, 'debug': False}

=== 2. Streaming JSON Lines (`.jsonl`) ===
  JSONL Record #1: {'event': 'login', 'user': 'aarav'}
  JSONL Record #2: {'event': 'purchase', 'user': 'diya', 'amount': 1499}

=== 3. Handling Malformed JSON (`json.JSONDecodeError`) ===
  Caught JSONDecodeError: Illegal trailing comma before end of object (line=1, col=33, pos=32)
```

### Output — Example 03
```text
=== 1. Serializing Custom Object with `default=custom_json_default` ===
{
  "__type__": "ReleaseBuild",
  "version": "2.4.0",
  "released_on": "2026-11-04",
  "tags": [
    "lts",
    "stable"
  ]
}

=== 2. Deserializing Back to Domain Object with `object_hook=` ===
  Decoded object : ReleaseBuild(version='2.4.0', released_on=datetime.date(2026, 11, 4), tags={'stable', 'lts'})
  Equality check : True (type=ReleaseBuild)
```

---

## 7. Code Explanation

1. **`separators=(",", ":")` (Example 01):** By default, `json.dumps()` uses `(", ", ": ")` with spaces after commas and colons. Passing `separators=(",", ":")` strips all non-essential whitespace, shrinking network payload sizes by ~20–30%.
2. **JSON Lines `.jsonl` (Example 02):** Standard JSON arrays (`[...]`) require reading the entire file to parse cleanly. Writing one compact JSON object per line (`.jsonl`) allows streaming billions of records in $O(1)$ memory and appending new events with `mode="a"`.
3. **`default` and `object_hook` (Example 03):** `custom_json_default` converts `ReleaseBuild` into a plain `dict` tagged with `"__type__": "ReleaseBuild"`, while `custom_json_object_hook` intercepts any decoded `dict` with that tag and rebuilds the `ReleaseBuild` dataclass.

---

## 8. Common Mistakes

1. **Confusing `json.loads()` with `json.load()`:** Calling `json.load('{"a": 1}')` raises `AttributeError: 'str' object has no attribute 'read'` because `json.load` expects an open file object, not a string.
2. **Using Single Quotes or Trailing Commas in Hand-Written JSON:** Unlike Python dicts, RFC 8259 JSON strictly requires **double quotes** (`"key"`) and forbids trailing commas (`{"a": 1,}`) or comments (`//`).
3. **Expecting Integer Dictionary Keys to Survive a Round-Trip:** `json.loads(json.dumps({1: "one"}))` produces `{"1": "one"}` with a `str` key.
4. **Serializing Floating-Point `NaN` or `Infinity` for External APIs:** By default, Python's `json.dumps()` allows `NaN` and `Infinity` (`allow_nan=True`), which violates strict RFC 8259 JSON and causes JavaScript `JSON.parse()` to throw `SyntaxError`. Pass `allow_nan=False` when strict compliance is required.

---

## 9. Practice Questions

1. **Easy:** Write a function `pretty_json(data: dict) -> str` that returns a sorted, 4-space-indented JSON string and raises `ValueError` if `data` contains `float('nan')` (hint: use `allow_nan=False`).
2. **Medium:** Write a function `filter_jsonl_logs(input_path: Path, output_path: Path, min_amount: float) -> int` that streams a `.jsonl` file line by line, skips malformed lines while logging their line number via `json.JSONDecodeError`, and writes valid records with `amount >= min_amount` to `output_path`.
3. **Hard:** Write a custom `Decimal` and `UUID` JSON encoder/decoder pair (`default` and `object_hook` or `parse_float=Decimal`) so financial transactions preserve exact decimal precision across JSON round-trips.

---

## 10. Interview Questions

### Q1: How can you prevent `float` precision loss when parsing financial JSON payloads with `json.loads()`?
**Answer:** Pass `parse_float=decimal.Decimal` to `json.loads(payload, parse_float=Decimal)`. Every JSON floating-point number in the payload will be parsed directly from its exact string representation into a `Decimal` object instead of an IEEE-754 `float`.

### Q2: Why should you never use `eval()` to parse a JSON string in Python?
**Answer:**
1. **Security (Remote Code Execution):** `eval()` executes arbitrary Python expressions embedded in the string (e.g., `__import__('os').system('...')`).
2. **Syntax Incompatibility:** JSON keywords `null`, `true`, and `false` are `NameError`s in Python (`None`, `True`, `False`). Always use `json.loads()`.

### Q3: What does `ensure_ascii=False` do in `json.dumps()`?
**Answer:** By default (`ensure_ascii=True`), `json.dumps()` escapes all non-ASCII Unicode characters into `\uXXXX` escape sequences so the output is pure 7-bit ASCII. Setting `ensure_ascii=False` outputs literal UTF-8 characters (such as `₹`, `é`, or `🐍`) directly, which is more human-readable and smaller when saved to a UTF-8 file.
