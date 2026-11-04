"""
Phase 4 - Topic 09: Abstraction
Example 03: Standard Library ABCs (`collections.abc`) & Virtual Subclass Registration

Demonstrates:
  - Implementing a custom read-only sequence by inheriting from `collections.abc.Sequence`
    (implementing just `__getitem__` and `__len__` gives `__contains__`, `__iter__`,
    `__reversed__`, `index()`, and `count()` for FREE!)
  - Registering a virtual subclass via `ABC.register()`
"""

from collections.abc import Sequence
from typing import overload


class ImmutableBatch(Sequence[str]):
    """
    Inherits from `collections.abc.Sequence`.
    By implementing ONLY `__getitem__` and `__len__`, `Sequence` provides
    `__iter__`, `__contains__` (`in`), `__reversed__`, `.index()`, and `.count()`!
    """

    def __init__(self, items: list[str]) -> None:
        self._items = tuple(items)

    @overload
    def __getitem__(self, index: int) -> str: ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[str]: ...

    def __getitem__(self, index: int | slice) -> str | Sequence[str]:
        return self._items[index]

    def __len__(self) -> int:
        return len(self._items)


def main() -> None:
    print("=== Inheriting Free Mixin Methods from `collections.abc.Sequence` ===")
    batch = ImmutableBatch(["task-A", "task-B", "task-A", "task-C"])

    print(f"  len(batch)              : {len(batch)}")
    print(f"  batch[1]                : {batch[1]!r}")
    print(f"  'task-C' in batch       : {'task-C' in batch} (provided by Sequence!)")
    print(f"  batch.count('task-A')   : {batch.count('task-A')} (provided by Sequence!)")
    print(f"  batch.index('task-C')   : {batch.index('task-C')} (provided by Sequence!)")
    print(f"  list(reversed(batch))   : {list(reversed(batch))} (provided by Sequence!)")


if __name__ == "__main__":
    main()
