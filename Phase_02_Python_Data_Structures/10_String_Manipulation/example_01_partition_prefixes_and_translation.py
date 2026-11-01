"""
Topic 10: String Manipulation
Example 01: `removeprefix`/`removesuffix`, `partition`, and `str.translate`

Demonstrates modern, bug-free string manipulation methods that avoid the
pitfalls of `.strip("chars")` and repeated `.replace()` calls.
"""

import string


def main() -> None:
    # 1. Python 3.9+ removeprefix() and removesuffix() vs strip()
    filename = "test_user_controller.py"
    clean_stem = filename.removeprefix("test_").removesuffix(".py")
    print("=== 1. Exact Prefix & Suffix Removal ===")
    print(f"Original Filename : {filename!r}")
    print(f"Cleaned Stem      : {clean_stem!r}")

    # 2. partition() and rpartition() -> Always returns a 3-tuple (head, sep, tail)
    email = "divya.tiwari@university.edu.in"
    username, _, domain = email.partition("@")
    subdomain, _, top_level = domain.rpartition(".")
    print("\n=== 2. Safe Splitting with partition() & rpartition() ===")
    print(f"Username          : {username!r}")
    print(f"Full Domain       : {domain!r} (Sub: {subdomain!r}, TLD: {top_level!r})")

    # 3. High-speed character translation & punctuation stripping with str.maketrans()
    messy_sentence = "Hello, World! Python-3.13 is #1 for DSA!!!"
    # Map '-' -> ' ' and delete all other punctuation in a single C-level pass
    delete_chars = string.punctuation.replace("-", "").replace(".", "")
    trans_table = str.maketrans("-", " ", delete_chars)
    cleaned_sentence = messy_sentence.translate(trans_table)
    print("\n=== 3. Single-Pass Translation & Punctuation Removal ===")
    print(f"Before translate  : {messy_sentence}")
    print(f"After translate   : {cleaned_sentence}")


if __name__ == "__main__":
    main()
