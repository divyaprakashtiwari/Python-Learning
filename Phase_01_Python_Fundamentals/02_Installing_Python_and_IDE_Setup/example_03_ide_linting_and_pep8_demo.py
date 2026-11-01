"""
Topic 02: Installing Python and IDE Setup
Example 03: IDE Features Demo — Docstrings, Type Hints, and PEP 8 Formatting

Demonstrates how writing PEP 8 compliant code with docstrings and type annotations
enables IDE autocomplete (IntelliSense), hover documentation, and static type checking.
"""


def format_student_badge(student_name: str, roll_number: int, track: str = "Python + DSA") -> str:
    """
    Create a formatted student badge string for IDE preview and console output.

    Args:
        student_name: Full name of the learner.
        roll_number: Unique numeric ID assigned to the learner.
        track: Enrolled curriculum track name.

    Returns:
        A single-line formatted badge string.
    """
    cleaned_name = student_name.strip().title()
    return f"[ID #{roll_number:04d}] {cleaned_name} | Track: {track}"


def main() -> None:
    badge_1 = format_student_badge("divya prakash tiwari", 1)
    badge_2 = format_student_badge("aarav sharma", 42, track="Backend Engineering")

    print("=== IDE-Friendly PEP 8 Code Output ===")
    print(badge_1)
    print(badge_2)
    print("\nFunction Docstring (__doc__) inspected by IDEs on hover:")
    first_doc_line = format_student_badge.__doc__.strip().splitlines()[0]
    print(f"  \"{first_doc_line}\"")
    print(f"Type Annotations (__annotations__): {format_student_badge.__annotations__}")


if __name__ == "__main__":
    main()
