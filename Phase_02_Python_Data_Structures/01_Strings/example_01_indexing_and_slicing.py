"""
Topic 01: Strings
Example 01: String Indexing, Slicing (`s[start:stop:step]`), and Immutability

Demonstrates positive and negative indexing, substring extraction via slicing,
string reversal (`s[::-1]`), and how modifying a string creates a new object.
"""


def main() -> None:
    course_code = "PYTHON-DSA-2026"

    print("=== 1. Positive and Negative Indexing ===")
    print(f"Full String       : {course_code!r} (Length: {len(course_code)})")
    print(f"First char [0]    : {course_code[0]!r}")
    print(f"Last char [-1]    : {course_code[-1]!r}")
    print(f"4th from end [-4] : {course_code[-4]!r}")

    print("\n=== 2. Slicing: s[start:stop:step] ===")
    print(f"Language [0:6]    : {course_code[:6]!r}")
    print(f"Topic [7:10]      : {course_code[7:10]!r}")
    print(f"Year [-4:]        : {course_code[-4:]!r}")
    print(f"Every 2nd char    : {course_code[::2]!r}")
    print(f"Reversed [::-1]   : {course_code[::-1]!r}")

    print("\n=== 3. String Immutability Proof ===")
    word = "cat"
    # word[0] = "b"  -> Would raise TypeError: 'str' object does not support item assignment
    modified_word = "b" + word[1:]
    print(f"Original word     : {word!r}")
    print(f"New sliced string : {modified_word!r}")


if __name__ == "__main__":
    main()
