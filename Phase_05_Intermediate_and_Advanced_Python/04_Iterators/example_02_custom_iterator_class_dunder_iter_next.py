"""
Phase 5 - Topic 04: Iterators
Example 02: Building a Custom Stateful Iterator Class (`__iter__` and `__next__`)

Demonstrates:
  - Implementing a custom `Countdown` iterator that computes values lazily on demand in O(1) memory
  - Why an iterator's `__iter__` method must `return self`
"""


class PaginatedRangeIterator:
    """Lazy iterator yielding `(page_number, start_offset, end_offset)` tuples."""

    def __init__(self, total_items: int, page_size: int) -> None:
        if page_size <= 0:
            raise ValueError("page_size must be positive")
        self.total_items = total_items
        self.page_size = page_size
        self._current_offset = 0
        self._page_num = 0

    def __iter__(self) -> "PaginatedRangeIterator":
        return self

    def __next__(self) -> tuple[int, int, int]:
        if self._current_offset >= self.total_items:
            raise StopIteration
        self._page_num += 1
        start = self._current_offset
        end = min(start + self.page_size, self.total_items)
        self._current_offset = end
        return (self._page_num, start, end)


def main() -> None:
    print("=== Lazy Pagination Iterator Over 25 Items (page_size=10) ===")
    pager = PaginatedRangeIterator(total_items=25, page_size=10)
    for page_no, start_idx, end_idx in pager:
        print(f"  Page {page_no}: slice[{start_idx}:{end_idx}] ({end_idx - start_idx} items)")


if __name__ == "__main__":
    main()
