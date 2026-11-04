"""
Phase 5 - Topic 04: Iterators
Example 03: Reusable Iterable vs Single-Pass Iterator Exhaustion Trap

Demonstrates:
  - The crucial distinction between an **Iterable** (a container whose `__iter__` returns a
    fresh iterator each time) and an **Iterator** (which is exhausted after a single pass)
  - Using `iter(callable, sentinel)` two-argument form for sentinel-driven iteration
"""


class SinglePassFibonacci:
    """ANTI-PATTERN for reusable containers: acts as its own iterator (exhausts after 1 loop)."""

    def __init__(self, count: int) -> None:
        self.count = count
        self._index = 0
        self._a, self._b = 0, 1

    def __iter__(self) -> "SinglePassFibonacci":
        return self

    def __next__(self) -> int:
        if self._index >= self.count:
            raise StopIteration
        val = self._a
        self._a, self._b = self._b, self._a + self._b
        self._index += 1
        return val


class ReusableFibonacciIterable:
    """BEST PRACTICE: `__iter__` returns a fresh iterator instance on every loop."""

    def __init__(self, count: int) -> None:
        self.count = count

    def __iter__(self) -> SinglePassFibonacci:
        return SinglePassFibonacci(self.count)


def main() -> None:
    print("=== 1. Single-Pass Iterator Exhaustion Trap ===")
    single_pass = SinglePassFibonacci(6)
    print(f"  Pass 1: {list(single_pass)}")
    print(f"  Pass 2: {list(single_pass)}  <-- Empty! Already exhausted")

    print("\n=== 2. Reusable Iterable Returning Fresh Iterators ===")
    reusable = ReusableFibonacciIterable(6)
    print(f"  Pass 1: {list(reusable)}")
    print(f"  Pass 2: {list(reusable)}  <-- Works repeatedly!")

    print("\n=== 3. Two-Argument `iter(callable, sentinel)` Form ===")
    buffer = ["chunk-1", "chunk-2", "EOF", "ignored-chunk"]
    cursor = iter(buffer)
    # Calls `lambda: next(cursor)` repeatedly until it returns `"EOF"`
    chunks = list(iter(lambda: next(cursor), "EOF"))
    print(f"  Read chunks until 'EOF' sentinel: {chunks}")


if __name__ == "__main__":
    main()
