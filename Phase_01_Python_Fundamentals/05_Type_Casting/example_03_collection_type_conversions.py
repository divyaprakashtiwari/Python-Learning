"""
Topic 05: Type Casting
Example 03: Casting Between Collections (`list`, `tuple`, `set`, `dict`, `str`)

Demonstrates practical real-world conversions between collection types:
- Splitting a string into a list of characters
- Removing duplicates via `set()` or `dict.fromkeys()`
- Converting a list of `(key, value)` tuples into a `dict`
"""


def main() -> None:
    # 1. String <-> List of Characters
    word = "algorithm"
    char_list = list(word)
    rejoined_word = "".join(char_list)
    print("=== 1. String and List Conversion ===")
    print(f"list({word!r}) -> {char_list}")
    print(f"''.join(char_list) -> {rejoined_word!r}")

    # 2. Deduplicating a list of student IDs
    raw_submissions = [104, 101, 102, 104, 101, 105]
    unique_sorted = sorted(set(raw_submissions))
    unique_order_preserved = list(dict.fromkeys(raw_submissions))

    print("\n=== 2. Deduplication via Collection Casting ===")
    print(f"Raw Submissions          : {raw_submissions}")
    print(f"Sorted Unique (via set)  : {unique_sorted}")
    print(f"Order-Preserved Unique   : {unique_order_preserved}")

    # 3. Sequence of pairs -> Dictionary and Immutable Tuple
    key_value_pairs = [("host", "localhost"), ("port", 8080), ("debug", True)]
    config_dict = dict(key_value_pairs)
    frozen_keys = tuple(config_dict.keys())
    print("\n=== 3. Pairs to Dict & Tuple ===")
    print(f"Config Dict : {config_dict}")
    print(f"Frozen Keys : {frozen_keys}")


if __name__ == "__main__":
    main()
