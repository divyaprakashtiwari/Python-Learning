"""
Topic 09: Advanced Python - Question 01: Iterators and __iter__/__next__

A comprehensive collection of 10 standalone, runnable exercises exploring
Python's iterator protocol, iterable vs iterator separation, sentinel iter(),
bidirectional and peekable iterators, and paged cursor streaming.

Questions Covered:
 1. The Iterator Protocol: Implementing __iter__() and __next__() with StopIteration.
 2. Decoupling Iterable from Iterator: Multi-pass iteration support across fresh instances.
 3. Sentinel-Based iter(callable, sentinel): Generating streams from null-terminated sources.
 4. Infinite Stream Iterator: Unbounded Fibonacci stream with state progression.
 5. Reversible Iterators: Implementing __reversed__() for custom collections.
 6. Peekable Iterator Wrapper: Inspecting upcoming elements without advancing the cursor.
 7. Cyclic Bounded Iterator: Circular carousel traversal with iteration limits.
 8. Chunked Window Iterator: Grouping continuous streams into fixed-size tuples.
 9. Hierarchical Tree Traversal: Depth-first pre-order iterator using an internal stack.
10. Advanced Project: Paged Database Cursor & Stream Consumer with lazy batch loading.
"""

from typing import Any, Callable, Iterator


# ==============================================================================
# Question 1: The Basic Iterator Protocol
# ==============================================================================
class BoundedRangeIterator:
    """
    Direct iterator that counts from `start` up to `stop` (exclusive),
    raising StopIteration when limit is reached.
    """

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self) -> "BoundedRangeIterator":
        # An iterator must return itself from __iter__()
        return self

    def __next__(self) -> int:
        if (self.step > 0 and self.current >= self.stop) or (self.step < 0 and self.current <= self.stop):
            raise StopIteration
        val = self.current
        self.current += self.step
        return val


def exercise_q1_basic_iterator_protocol() -> None:
    """
    Demonstrate manual next() invocation and for-loop exhaustion.
    """
    print("=== Q1: The Basic Iterator Protocol ===")

    it = BoundedRangeIterator(1, 5)
    assert next(it) == 1
    assert next(it) == 2
    assert next(it) == 3
    assert next(it) == 4

    # Exhausted: next call must raise StopIteration
    caught_stop = False
    try:
        next(it)
    except StopIteration:
        caught_stop = True

    assert caught_stop is True

    # For-loop consumption on new instance
    items = list(BoundedRangeIterator(10, 25, step=5))
    assert items == [10, 15, 20]

    print(f"  Single steps verified; list(BoundedRangeIterator(10, 25, 5)) = {items}")


# ==============================================================================
# Question 2: Decoupling Iterable from Iterator
# ==============================================================================
class DataSetIterator:
    """The stateful single-use iterator."""

    def __init__(self, records: list[str]) -> None:
        self._records = records
        self._index = 0

    def __iter__(self) -> "DataSetIterator":
        return self

    def __next__(self) -> str:
        if self._index >= len(self._records):
            raise StopIteration
        item = self._records[self._index]
        self._index += 1
        return item


class DataSet:
    """
    The multi-pass iterable container. Every call to __iter__() creates
    a FRESH DataSetIterator, allowing independent, reusable passes.
    """

    def __init__(self, records: list[str]) -> None:
        self.records = records

    def __iter__(self) -> DataSetIterator:
        return DataSetIterator(self.records)


def exercise_q2_decoupling_iterable_iterator() -> None:
    """
    Demonstrate that decoupling container from iterator allows multiple concurrent
    and sequential loops over the same container without exhausting it.
    """
    print("\n=== Q2: Decoupling Iterable from Iterator ===")

    dataset = DataSet(["ALPHA", "BETA", "GAMMA"])

    # Pass 1
    pass1 = list(dataset)
    assert pass1 == ["ALPHA", "BETA", "GAMMA"]

    # Pass 2: Still works! Container is NOT exhausted
    pass2 = list(dataset)
    assert pass2 == ["ALPHA", "BETA", "GAMMA"]

    # Concurrent independent iteration
    it1 = iter(dataset)
    it2 = iter(dataset)
    assert next(it1) == "ALPHA"
    assert next(it2) == "ALPHA"
    assert next(it1) == "BETA"
    assert next(it2) == "BETA"

    print(f"  Pass 1: {pass1}, Pass 2: {pass2}")
    print("  Independent concurrent iterators successfully demonstrated.")


# ==============================================================================
# Question 3: Sentinel-Based iter(callable, sentinel)
# ==============================================================================
def exercise_q3_sentinel_iter() -> None:
    """
    Demonstrate the 2-argument form of built-in iter(callable, sentinel).
    Calls `callable()` on every step until the return value equals `sentinel`.
    """
    print("\n=== Q3: Sentinel-Based iter(callable, sentinel) ===")

    stream_data = [10, 20, 30, -1, 40, 50]  # -1 is EOF sentinel
    data_cursor = 0

    def read_sensor_packet() -> int:
        nonlocal data_cursor
        val = stream_data[data_cursor]
        data_cursor += 1
        return val

    # iter(read_sensor_packet, -1) halts cleanly when read_sensor_packet() returns -1
    sensor_stream = iter(read_sensor_packet, -1)
    packets = list(sensor_stream)

    assert packets == [10, 20, 30]
    assert -1 not in packets
    assert 40 not in packets

    print(f"  Consumed packets before sentinel (-1): {packets}")


# ==============================================================================
# Question 4: Infinite Stream Iterator (Fibonacci)
# ==============================================================================
class InfiniteFibonacci:
    """
    Infinite iterator producing Fibonacci numbers with O(1) space.
    """

    def __init__(self) -> None:
        self.a = 0
        self.b = 1

    def __iter__(self) -> "InfiniteFibonacci":
        return self

    def __next__(self) -> int:
        val = self.a
        self.a, self.b = self.b, self.a + self.b
        return val


def exercise_q4_infinite_stream_iterator() -> None:
    """
    Demonstrate generating elements on-demand from an infinite iterator.
    """
    print("\n=== Q4: Infinite Stream Iterator ===")

    fib = InfiniteFibonacci()
    first_8 = [next(fib) for _ in range(8)]
    assert first_8 == [0, 1, 1, 2, 3, 5, 8, 13]

    print(f"  First 8 numbers of infinite Fibonacci stream: {first_8}")


# ==============================================================================
# Question 5: Reversible Iterators (__reversed__)
# ==============================================================================
class BidirectionalPlaylist:
    """
    Collection implementing both __iter__() and __reversed__().
    """

    def __init__(self, tracks: list[str]) -> None:
        self.tracks = tracks

    def __iter__(self) -> Iterator[str]:
        return iter(self.tracks)

    def __reversed__(self) -> Iterator[str]:
        # Yield tracks in reverse order
        for i in range(len(self.tracks) - 1, -1, -1):
            yield self.tracks[i]


def exercise_q5_reversible_iterator() -> None:
    """
    Demonstrate custom reversed() support via __reversed__().
    """
    print("\n=== Q5: Reversible Iterators (__reversed__) ===")

    playlist = BidirectionalPlaylist(["Track 1", "Track 2", "Track 3"])

    forward = list(playlist)
    backward = list(reversed(playlist))

    assert forward == ["Track 1", "Track 2", "Track 3"]
    assert backward == ["Track 3", "Track 2", "Track 1"]

    print(f"  Forward:  {forward}")
    print(f"  Reversed: {backward}")


# ==============================================================================
# Question 6: Peekable Iterator Wrapper
# ==============================================================================
class PeekableIterator:
    """
    Wraps any standard iterator to provide a peek() method that inspects
    the next item without consuming it from the stream.
    """

    _SENTINEL = object()

    def __init__(self, iterable: Any) -> None:
        self._iterator = iter(iterable)
        self._peeked: Any = self._SENTINEL

    def __iter__(self) -> "PeekableIterator":
        return self

    def __next__(self) -> Any:
        if self._peeked is not self._SENTINEL:
            val = self._peeked
            self._peeked = self._SENTINEL
            return val
        return next(self._iterator)

    def peek(self, default: Any = None) -> Any:
        if self._peeked is self._SENTINEL:
            try:
                self._peeked = next(self._iterator)
            except StopIteration:
                return default
        return self._peeked

    def has_next(self) -> bool:
        return self.peek(self._SENTINEL) is not self._SENTINEL


def exercise_q6_peekable_iterator() -> None:
    """
    Test peekable iterator without advancing the stream position.
    """
    print("\n=== Q6: Peekable Iterator Wrapper ===")

    peekable = PeekableIterator([100, 200, 300])

    # Peek upcoming element without consuming
    assert peekable.has_next() is True
    assert peekable.peek() == 100
    assert peekable.peek() == 100  # Still 100!

    # Now consume
    assert next(peekable) == 100
    assert peekable.peek() == 200
    assert next(peekable) == 200
    assert next(peekable) == 300

    # Exhausted
    assert peekable.has_next() is False
    assert peekable.peek(default="EMPTY") == "EMPTY"

    print("  PeekableIterator successfully inspected ahead without consuming elements.")


# ==============================================================================
# Question 7: Cyclic Bounded Iterator
# ==============================================================================
class CyclicBoundedIterator:
    """
    Iterates over a sequence cyclically up to a maximum total step count.
    """

    def __init__(self, sequence: list[Any], max_steps: int) -> None:
        if not sequence:
            raise ValueError("Sequence cannot be empty")
        self.sequence = sequence
        self.max_steps = max_steps
        self.steps_taken = 0
        self.index = 0

    def __iter__(self) -> "CyclicBoundedIterator":
        return self

    def __next__(self) -> Any:
        if self.steps_taken >= self.max_steps:
            raise StopIteration

        item = self.sequence[self.index]
        self.index = (self.index + 1) % len(self.sequence)
        self.steps_taken += 1
        return item


def exercise_q7_cyclic_bounded_iterator() -> None:
    """
    Demonstrate cycling through items up to a bounded quota.
    """
    print("\n=== Q7: Cyclic Bounded Iterator ===")

    colors = ["RED", "GREEN", "BLUE"]
    cycler = CyclicBoundedIterator(colors, max_steps=7)

    result = list(cycler)
    assert result == ["RED", "GREEN", "BLUE", "RED", "GREEN", "BLUE", "RED"]

    print(f"  Cyclic bounded steps (7): {result}")


# ==============================================================================
# Question 8: Chunked Window Iterator
# ==============================================================================
class ChunkedIterator:
    """
    Consumes any underlying iterator in fixed-size tuples of length N.
    """

    def __init__(self, iterable: Any, chunk_size: int) -> None:
        self.iterator = iter(iterable)
        self.chunk_size = chunk_size

    def __iter__(self) -> "ChunkedIterator":
        return self

    def __next__(self) -> tuple[Any, ...]:
        chunk = []
        for _ in range(self.chunk_size):
            try:
                chunk.append(next(self.iterator))
            except StopIteration:
                break

        if not chunk:
            raise StopIteration

        return tuple(chunk)


def exercise_q8_chunked_iterator() -> None:
    """
    Demonstrate chunked batches of arbitrary stream inputs.
    """
    print("\n=== Q8: Chunked Window Iterator ===")

    items = range(1, 9)  # 1, 2, 3, 4, 5, 6, 7, 8
    chunker = ChunkedIterator(items, chunk_size=3)

    chunks = list(chunker)
    assert chunks == [(1, 2, 3), (4, 5, 6), (7, 8)]

    print(f"  Chunked batches of 3: {chunks}")


# ==============================================================================
# Question 9: Hierarchical Tree Traversal Iterator
# ==============================================================================
class TreeNode:
    def __init__(self, val: str, children: list["TreeNode"] | None = None) -> None:
        self.val = val
        self.children = children or []

    def __iter__(self) -> "TreeDepthFirstIterator":
        return TreeDepthFirstIterator(self)


class TreeDepthFirstIterator:
    """
    Iterates over tree nodes in depth-first pre-order using an explicit stack.
    """

    def __init__(self, root: TreeNode) -> None:
        self.stack: list[TreeNode] = [root]

    def __iter__(self) -> "TreeDepthFirstIterator":
        return self

    def __next__(self) -> str:
        if not self.stack:
            raise StopIteration

        node = self.stack.pop()
        # Push children in reverse order so leftmost child is popped first
        for child in reversed(node.children):
            self.stack.append(child)

        return node.val


def exercise_q9_tree_traversal_iterator() -> None:
    """
    Test depth-first tree iterator over hierarchical nodes.
    """
    print("\n=== Q9: Hierarchical Tree Traversal Iterator ===")

    # Tree:
    #       Root
    #      /    \
    #    NodeA  NodeB
    #    /   \
    # Leaf1 Leaf2
    tree = TreeNode("Root", [
        TreeNode("NodeA", [TreeNode("Leaf1"), TreeNode("Leaf2")]),
        TreeNode("NodeB"),
    ])

    traversal = list(tree)
    assert traversal == ["Root", "NodeA", "Leaf1", "Leaf2", "NodeB"]

    print(f"  Depth-first pre-order traversal: {traversal}")


# ==============================================================================
# Question 10: Advanced Project - Paged Database Cursor Stream Engine
# ==============================================================================
class PagedDatabaseCursor:
    """
    Transparently iterates through individual records by fetching multi-record
    pages lazily on demand, maintaining low memory consumption.
    """

    def __init__(self, fetch_page_fn: Callable[[int, int], list[dict[str, Any]]], page_size: int = 3) -> None:
        self.fetch_page_fn = fetch_page_fn
        self.page_size = page_size
        self.current_page: list[dict[str, Any]] = []
        self.page_offset = 0
        self.item_index = 0
        self.exhausted = False
        self.total_fetched = 0

    def __iter__(self) -> "PagedDatabaseCursor":
        return self

    def __next__(self) -> dict[str, Any]:
        # If current buffer is empty, fetch next page
        if self.item_index >= len(self.current_page):
            if self.exhausted:
                raise StopIteration

            new_page = self.fetch_page_fn(self.page_offset, self.page_size)
            if not new_page:
                self.exhausted = True
                raise StopIteration

            self.current_page = new_page
            self.page_offset += len(new_page)
            self.item_index = 0
            self.total_fetched += len(new_page)

            # If page returned fewer than page_size items, this was the last page
            if len(new_page) < self.page_size:
                self.exhausted = True

        record = self.current_page[self.item_index]
        self.item_index += 1
        return record


def exercise_q10_paged_database_cursor() -> None:
    """
    Test PagedDatabaseCursor transparently consuming a multi-page backend table.
    """
    print("\n=== Q10: Paged Database Cursor Stream Engine ===")

    # Synthetic backend storage of 8 records
    mock_db = [
        {"id": i, "name": f"User_{i:02d}"}
        for i in range(1, 9)
    ]

    fetch_call_count = 0

    def mock_fetch_page(offset: int, limit: int) -> list[dict[str, Any]]:
        nonlocal fetch_call_count
        fetch_call_count += 1
        return mock_db[offset:offset + limit]

    cursor = PagedDatabaseCursor(mock_fetch_page, page_size=3)

    records = list(cursor)
    assert len(records) == 8
    assert records[0]["id"] == 1
    assert records[-1]["id"] == 8

    # 8 records with page_size=3 -> Page 1 (3), Page 2 (3), Page 3 (2 < 3, marks exhausted)
    # Total calls: 3 fetches
    assert fetch_call_count == 3
    assert cursor.total_fetched == 8

    print(f"  Transparently yielded {len(records)} records across {fetch_call_count} lazy database page fetches:")
    print(f"    First: {records[0]}")
    print(f"    Last:  {records[-1]}")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_basic_iterator_protocol()
    exercise_q2_decoupling_iterable_iterator()
    exercise_q3_sentinel_iter()
    exercise_q4_infinite_stream_iterator()
    exercise_q5_reversible_iterator()
    exercise_q6_peekable_iterator()
    exercise_q7_cyclic_bounded_iterator()
    exercise_q8_chunked_iterator()
    exercise_q9_tree_traversal_iterator()
    exercise_q10_paged_database_cursor()

    print("\nAll 10 iterator questions executed and asserted successfully!")
