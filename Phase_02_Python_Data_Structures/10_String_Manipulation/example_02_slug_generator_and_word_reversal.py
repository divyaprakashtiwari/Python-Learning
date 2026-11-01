"""
Topic 10: String Manipulation
Example 02: URL Slug Generator and Reverse Words in a String (LeetCode 151)

Demonstrates practical text normalization for web URLs and the classic interview
problem of reversing words in a string with multiple spaces.
"""


def generate_url_slug(title: str) -> str:
    """Convert an article title into a clean, lowercase, hyphen-separated URL slug."""
    cleaned_chars = [
        ch.lower() if ch.isalnum() else " "
        for ch in title
    ]
    # .split() collapses all consecutive spaces automatically!
    words = "".join(cleaned_chars).split()
    return "-".join(words)


def reverse_words_in_string(s: str) -> str:
    """Reverse the order of words while collapsing multiple spaces to a single space."""
    return " ".join(s.split()[::-1])


def main() -> None:
    print("=== 1. Blog / E-Commerce URL Slug Generator ===")
    titles = [
        "  Phase 02: Python Data Structures & Algorithms! ",
        "Top 10 Interview Questions (2026 Edition)",
    ]
    for title in titles:
        print(f"  Title : {title!r}")
        print(f"  Slug  : {generate_url_slug(title)!r}")

    print("\n=== 2. Reverse Words in a String (Multiple Spaces Handled) ===")
    raw_input = "   the   sky   is   blue  "
    print(f"  Input  : {raw_input!r}")
    print(f"  Output : {reverse_words_in_string(raw_input)!r}")


if __name__ == "__main__":
    main()
