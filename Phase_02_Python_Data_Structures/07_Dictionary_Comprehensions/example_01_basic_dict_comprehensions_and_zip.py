"""
Topic 07: Dictionary Comprehensions
Example 01: Building Dictionaries from Iterables, `zip()`, and `enumerate()`

Demonstrates `{key_expr: val_expr for item in iterable}` for number mappings,
pairing parallel lists with `zip()`, and building `O(1)` index lookup tables.
"""


def main() -> None:
    # 1. Basic numeric mapping: number -> cube
    cubes = {n: n ** 3 for n in range(1, 6)}
    print("=== 1. Number to Cube Mapping ===")
    print(f"Cubes Dict : {cubes}")

    # 2. Pairing two parallel lists with zip()
    headers = ["id", "name", "track"]
    row_values = [101, "Divya Prakash", "Python + DSA"]
    record_dict = {col: val for col, val in zip(headers, row_values)}
    print("\n=== 2. Pairing Lists via zip() ===")
    print(f"Row Record : {record_dict}")

    # 3. Building an O(1) Value-to-Index Lookup Table via enumerate()
    sorted_primes = [2, 3, 5, 7, 11, 13, 17]
    prime_to_index = {prime: idx for idx, prime in enumerate(sorted_primes)}
    print("\n=== 3. Value-to-Index Lookup Table ===")
    print(f"Lookup Table      : {prime_to_index}")
    print(f"Index of prime 13 : {prime_to_index[13]}")


if __name__ == "__main__":
    main()
