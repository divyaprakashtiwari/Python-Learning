"""
Phase 6 - Data Structures and Algorithms
Section F: Stacks and Queues
Topic 01: Stack Implementation
Example 02: MinStack — O(1) Push, Pop, Top, and GetMin (Two-Stack vs Single-Stack Delta)

Design a stack that supports `push(val)`, `pop()`, `top()`, and retrieving the
minimum element `get_min()` all in strict O(1) time (LeetCode 155).

We demonstrate two classic interview designs:
  1. Paired Tuple / Auxiliary Min-Tracker Stack (`(val, current_min)`):
     - Each stack entry stores both `val` and the minimum of all elements at or
       below this depth. Simple, overflow-safe, O(1) worst-case time.
  2. Single-Stack Mathematical Delta Encoding (O(1) extra space beyond raw values):
     - Maintains `current_min`. When pushing a new minimum `val < current_min`,
       pushes the encoded value `2 * val - current_min` (which is strictly less
       than `val`, acting as a sentinel flag!) and updates `current_min = val`.
     - When popping an encoded sentinel `< current_min`, recovers the previous
       minimum via `prev_min = 2 * current_min - encoded_top`!
"""

from typing import List, Tuple


class PairedMinStack:
    """Stores `(val, min_so_far)` pairs for O(1) `get_min()`."""

    def __init__(self) -> None:
        self._stack: List[Tuple[int, int]] = []

    def push(self, val: int) -> None:
        if not self._stack:
            self._stack.append((val, val))
        else:
            current_min = min(val, self._stack[-1][1])
            self._stack.append((val, current_min))

    def pop(self) -> int:
        if not self._stack:
            raise IndexError("pop from empty PairedMinStack")
        return self._stack.pop()[0]

    def top(self) -> int:
        if not self._stack:
            raise IndexError("top from empty PairedMinStack")
        return self._stack[-1][0]

    def get_min(self) -> int:
        if not self._stack:
            raise IndexError("get_min from empty PairedMinStack")
        return self._stack[-1][1]


class DeltaEncodedMinStack:
    """
    Stores a single integer per entry using `2*val - prev_min` encoding whenever a
    new minimum arrives, achieving O(1) auxiliary memory overhead.
    """

    def __init__(self) -> None:
        self._stack: List[int] = []
        self._min_val: int = 0

    def push(self, val: int) -> None:
        if not self._stack:
            self._stack.append(val)
            self._min_val = val
        elif val >= self._min_val:
            self._stack.append(val)
        else:
            # `val < self._min_val`: encode previous minimum into the pushed value
            encoded = 2 * val - self._min_val
            self._stack.append(encoded)
            self._min_val = val

    def pop(self) -> int:
        if not self._stack:
            raise IndexError("pop from empty DeltaEncodedMinStack")
        raw_top = self._stack.pop()
        if raw_top >= self._min_val:
            return raw_top
        else:
            # `raw_top < self._min_val` means `self._min_val` was the true pushed value!
            actual_val = self._min_val
            # Recover previous minimum
            self._min_val = 2 * self._min_val - raw_top
            return actual_val

    def top(self) -> int:
        if not self._stack:
            raise IndexError("top from empty DeltaEncodedMinStack")
        raw_top = self._stack[-1]
        return raw_top if raw_top >= self._min_val else self._min_val

    def get_min(self) -> int:
        if not self._stack:
            raise IndexError("get_min from empty DeltaEncodedMinStack")
        return self._min_val


if __name__ == "__main__":
    print("=" * 72)
    print("MinStack O(1) `get_min()`: Paired Tuple Stack vs Single-Stack Delta")
    print("=" * 72)

    s1 = PairedMinStack()
    s2 = DeltaEncodedMinStack()

    stream = [10, 5, 8, 2, 12, -3, 4]
    print("Pushing stream:", stream)
    for x in stream:
        s1.push(x)
        s2.push(x)
        assert s1.top() == s2.top() and s1.get_min() == s2.get_min()
        print(f"  push({x:>2}) -> top = {s1.top():>2}, get_min() = {s1.get_min():>2}")

    print("\nPopping elements one by one:")
    for _ in range(len(stream) - 1):
        p1 = s1.pop()
        p2 = s2.pop()
        assert p1 == p2 and s1.get_min() == s2.get_min()
        print(f"  pop() -> {p1:>2} | new top = {s1.top():>2}, new get_min() = {s1.get_min():>2}")

