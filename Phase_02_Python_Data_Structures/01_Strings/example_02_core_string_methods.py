"""
Topic 01: Strings
Example 02: Essential String Methods for Cleaning, Searching, and Joining

Demonstrates `.strip()`, `.lower()`, `.title()`, `.startswith()`, `.endswith()`,
`.find()`, `.count()`, `.replace()`, `.split()`, and `.join()`.
"""


def main() -> None:
    raw_log = "   [WARN] 2026-11-01 | user=divya_tiwari | action=login_retry   "

    print("=== 1. Whitespace Stripping & Case Normalization ===")
    cleaned = raw_log.strip()
    print(f"Cleaned Log       : {cleaned!r}")
    print(f"Starts with [WARN]: {cleaned.startswith('[WARN]')}")
    print(f"Ends with retry   : {cleaned.endswith('login_retry')}")

    print("\n=== 2. Searching & Replacing ===")
    pos = cleaned.find("user=")
    print(f"Index of 'user='  : {pos}")
    print(f"Count of '|'      : {cleaned.count('|')}")
    promoted_log = cleaned.replace("[WARN]", "[INFO]", 1)
    print(f"Replaced Log      : {promoted_log}")

    print("\n=== 3. Splitting and Joining (`split` & `join`) ===")
    fields = [part.strip() for part in cleaned.split("|")]
    print(f"Parsed Fields     : {fields}")
    csv_line = ",".join(fields)
    print(f"Joined as CSV     : {csv_line}")


if __name__ == "__main__":
    main()
