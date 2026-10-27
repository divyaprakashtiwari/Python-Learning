"""
Topic 03 - Data Structures
Practice Question 1 Solution: List Slicing, Step Indexing & In-Place Slice Mutation

Problem Statement:
1. Slicing extractions: first 4, last 3, even indices, full reverse.
2. In-place slice mutation: replace middle slice [2:5] with [999, 888, 777].
3. In-place deletion: del list[1::2] to delete all elements at odd indices.
"""


def perform_slice_operations(data: list[int]) -> dict[str, object]:
    """Performs extraction slices and in-place slice mutations."""
    # Slices create new lists
    first_4 = data[:4]
    last_3 = data[-3:]
    even_indices = data[::2]
    reversed_list = data[::-1]

    # In-place mutations on a copy of data
    mutated = list(data)
    mutated[2:5] = [999, 888, 777]
    after_replacement = list(mutated)

    del mutated[1::2]
    after_deletion = list(mutated)

    return {
        "first_4": first_4,
        "last_3": last_3,
        "even_indices": even_indices,
        "reversed_list": reversed_list,
        "after_replacement": after_replacement,
        "after_deletion": after_deletion,
    }


def main() -> None:
    initial_list = [10, 20, 30, 40, 50, 60, 70, 80]
    res = perform_slice_operations(initial_list)

    print(f"First 4 Elements: {res['first_4']}")
    print(f"Last 3 Elements: {res['last_3']}")
    print(f"Even Indices: {res['even_indices']}")
    print(f"Reversed List: {res['reversed_list']}")
    print("After Slice Replacement [2:5] = [999, 888, 777]:")
    print(res["after_replacement"])
    print("After Deleting Odd Indices:")
    print(res["after_deletion"])


if __name__ == "__main__":
    main()
