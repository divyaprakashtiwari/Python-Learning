"""
Phase 5 - Topic 05: Generators
Example 02: Subgenerator Delegation with `yield from` & Recursive Tree Flattening

Demonstrates:
  - Delegating iteration to sub-iterables cleanly using `yield from`
  - Flattening arbitrarily nested lists recursively in O(depth) memory using `yield from`
  - Capturing a subgenerator's `return` value via `result = yield from subgen()`
"""

from typing import Iterator


def flatten_nested(items: list[object]) -> Iterator[int]:
    """Recursively yield all integers from arbitrarily nested lists using `yield from`."""
    for element in items:
        if isinstance(element, list):
            yield from flatten_nested(element)
        elif isinstance(element, int):
            yield element


def chunk_checksum_subgen(chunk: list[int]) -> Iterator[int]:
    """Yield each number in `chunk` and return their sum as the generator's StopIteration value."""
    running = 0
    for num in chunk:
        running += num
        yield num
    return running


def stream_with_audit(batches: list[list[int]]) -> Iterator[int]:
    """Delegate to `chunk_checksum_subgen` and capture its `return` value via `yield from`."""
    for idx, batch in enumerate(batches, start=1):
        batch_sum = yield from chunk_checksum_subgen(batch)
        print(f"    [audit] Batch #{idx} finished with sum = {batch_sum}")


def main() -> None:
    print("=== 1. Recursive Nested List Flattening with `yield from` ===")
    nested: list[object] = [1, [2, 3, [4, 5]], [], [[6], 7]]
    print(f"  Flattened: {list(flatten_nested(nested))}")

    print("\n=== 2. Capturing Subgenerator Return Value (`total = yield from ...`) ===")
    streamed = list(stream_with_audit([[10, 20], [5, 15, 25]]))
    print(f"  All yielded items: {streamed}")


if __name__ == "__main__":
    main()
