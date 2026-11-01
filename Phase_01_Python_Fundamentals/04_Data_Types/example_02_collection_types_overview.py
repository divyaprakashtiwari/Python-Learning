"""
Topic 04: Data Types
Example 02: Built-in Collection Data Types and Type Inspection

Demonstrates `list`, `tuple`, `set`, `dict`, `bytes`, and `range`, showing
how to inspect types safely using `type()` and `isinstance()`.
"""


def main() -> None:
    # Core built-in collection types
    languages_list = ["Python", "C++", "Java"]               # Ordered, mutable
    coordinates_tuple = (28.61, 77.20)                       # Ordered, immutable
    unique_tags_set = {"dsa", "python", "backend", "dsa"}    # Unordered, unique elements
    student_dict = {"name": "Divya", "phase": 1}             # Key-value mapping
    raw_bytes = b"HTTP/1.1"                                  # Immutable byte sequence

    samples = [
        ("languages_list", languages_list),
        ("coordinates_tuple", coordinates_tuple),
        ("unique_tags_set", unique_tags_set),
        ("student_dict", student_dict),
        ("raw_bytes", raw_bytes),
    ]

    print("=== Built-in Collection Data Types ===")
    for label, obj in samples:
        # Sort set only for deterministic display in output
        display_val = sorted(obj) if isinstance(obj, set) else obj
        print(f"{label:<18} | Type: {type(obj).__name__:<6} | Len: {len(obj)} | Value: {display_val}")


if __name__ == "__main__":
    main()
