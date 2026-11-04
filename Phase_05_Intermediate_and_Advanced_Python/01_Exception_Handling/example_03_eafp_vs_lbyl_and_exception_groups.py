"""
Phase 5 - Topic 01: Exception Handling
Example 03: EAFP vs LBYL Style & `ExceptionGroup` / `except*` (Python 3.11+)

Demonstrates:
  - LBYL ("Look Before You Leap") vs Pythonic EAFP ("Easier to Ask Forgiveness than Permission")
  - Adding contextual notes to exceptions with `err.add_note()` (Python 3.11+)
  - Handling multiple concurrent failures with `ExceptionGroup` and `except*` (Python 3.11+)
"""


def lookup_price_lbyl(catalog: dict[str, dict[str, float]], category: str, item: str) -> float:
    """LBYL: Multiple pre-checks before accessing nested keys."""
    if category in catalog and item in catalog[category]:
        return catalog[category][item]
    return 0.0


def lookup_price_eafp(catalog: dict[str, dict[str, float]], category: str, item: str) -> float:
    """EAFP: Attempt the direct lookup and catch `KeyError` on miss."""
    try:
        return catalog[category][item]
    except KeyError:
        return 0.0


def validate_batch_records(records: list[dict[str, object]]) -> None:
    """Collect all validation errors across a batch into an `ExceptionGroup` (Python 3.11+)."""
    errors: list[Exception] = []
    for idx, rec in enumerate(records):
        if "id" not in rec:
            err = KeyError("Missing 'id' field")
            err.add_note(f"Occurred at batch row index {idx}")
            errors.append(err)
        elif not isinstance(rec["id"], int):
            err_type = TypeError(f"Expected int 'id', got {type(rec['id']).__name__}")
            err_type.add_note(f"Occurred at batch row index {idx}")
            errors.append(err_type)

    if errors:
        raise ExceptionGroup("Batch validation failed", errors)


def main() -> None:
    print("=== 1. Comparing LBYL vs EAFP Nested Lookups ===")
    catalog = {"electronics": {"keyboard": 2499.0}}
    print(f"  Hit  (LBYL / EAFP) : {lookup_price_lbyl(catalog, 'electronics', 'keyboard')} / {lookup_price_eafp(catalog, 'electronics', 'keyboard')}")
    print(f"  Miss (LBYL / EAFP) : {lookup_price_lbyl(catalog, 'books', 'novel')} / {lookup_price_eafp(catalog, 'books', 'novel')}")

    print("\n=== 2. Handling Multiple Concurrent Errors with `ExceptionGroup` & `except*` ===")
    batch = [{"id": 101}, {}, {"id": "bad-id"}]
    try:
        validate_batch_records(batch)
    except* KeyError as key_group:
        for e in key_group.exceptions:
            print(f"  [except* KeyError]  {e} | notes={getattr(e, '__notes__', [])}")
    except* TypeError as type_group:
        for e in type_group.exceptions:
            print(f"  [except* TypeError] {e} | notes={getattr(e, '__notes__', [])}")


if __name__ == "__main__":
    main()
