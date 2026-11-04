r"""
Phase 5 - Topic 09: Regular Expressions
Example 01: `re.search()`, `re.match()`, `re.fullmatch()`, `re.findall()`, & Raw Strings (`r"..."`)

Demonstrates:
  - Why raw strings (`r"..."`) are essential for regex patterns (`\b`, `\d`, `\s`)
  - The difference between `re.match()` (anchored at start), `re.search()` (anywhere),
    and `re.fullmatch()` (entire string must match)
  - Extracting all occurrences with `re.findall()` and `re.finditer()`
"""

import re


def main() -> None:
    text = "Order #4091 placed on 2026-11-04; Order #5102 placed on 2026-11-05."

    print("=== 1. `re.match` vs `re.search` vs `re.fullmatch` ===")
    print(f"  re.match(r'#\\d+', text)     : {re.match(r'#\d+', text)} (None: '#' is not at index 0)")
    first_hit = re.search(r"#\d+", text)
    print(f"  re.search(r'#\\d+', text)    : {first_hit.group(0) if first_hit else None} at span {first_hit.span() if first_hit else None}")
    print(f"  re.fullmatch(r'\\d{{4}}', '4091'): {bool(re.fullmatch(r'\d{4}', '4091'))}")

    print("\n=== 2. Extracting All Matches with `re.findall` & `re.finditer` ===")
    order_ids = re.findall(r"#(\d+)", text)
    print(f"  re.findall(r'#(\\d+)', text) : {order_ids} (returns captured group strings)")

    for match in re.finditer(r"\b(\d{4})-(\d{2})-(\d{2})\b", text):
        year, month, day = match.groups()
        print(f"  re.finditer date at {match.span()}: year={year}, month={month}, day={day}")


if __name__ == "__main__":
    main()
