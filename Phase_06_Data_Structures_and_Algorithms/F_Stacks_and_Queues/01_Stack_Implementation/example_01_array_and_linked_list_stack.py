"""
Phase 6 - Data Structures and Algorithms
Section F: Stacks and Queues
Topic 01: Stack Implementation
Example 01: Array-Backed Stack (`list`) vs Pointer-Backed Linked Stack (`Node`)

A Stack is a Last-In, First-Out (LIFO) linear data structure supporting three core
O(1) operations:
  - `push(x)` : Insert element `x` onto the top of the stack.
  - `pop()`   : Remove and return the top element (raises IndexError if empty).
  - `peek()`  : Inspect the top element without removing it.

We compare two industrial implementations:
  1. Dynamic Array Stack (backed by Python `list`):
     - Amortized O(1) push/pop, contiguous cache-friendly memory, minimal per-element
       pointer overhead.
  2. Singly Linked List Stack (push/pop at `head`):
     - Strict worst-case O(1) push/pop (never triggers array reallocation/resizing),
       at the cost of one node allocation per push.
"""

from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class ArrayStack(Generic[T]):
    """LIFO Stack backed by a dynamic array (Python list)."""

    def __init__(self) -> None:
        self._data: List[T] = []

    def push(self, item: T) -> None:
        """Pushes `item` onto the top of the stack in amortized O(1) time."""
        self._data.append(item)

    def pop(self) -> T:
        """Removes and returns the top item in amortized O(1) time."""
        if not self._data:
            raise IndexError("pop from an empty ArrayStack")
        return self._data.pop()

    def peek(self) -> T:
        """Returns the top item without removing it in O(1) time."""
        if not self._data:
            raise IndexError("peek from an empty ArrayStack")
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)

    def to_list_top_down(self) -> List[T]:
        """Returns stack contents ordered from TOP to BOTTOM."""
        return list(reversed(self._data))


class _StackNode(Generic[T]):
    __slots__ = ("val", "next")

    def __init__(self, val: T, next_node: Optional["_StackNode[T]"] = None) -> None:
        self.val: T = val
        self.next: Optional["_StackNode[T]"] = next_node


class LinkedStack(Generic[T]):
    """LIFO Stack backed by a singly linked list head pointer (strict worst-case O(1))."""

    def __init__(self) -> None:
        self._head: Optional[_StackNode[T]] = None
        self._size: int = 0

    def push(self, item: T) -> None:
        """Prepends a new node at `_head` in strict O(1) time."""
        self._head = _StackNode(item, self._head)
        self._size += 1

    def pop(self) -> T:
        """Unlinks and returns `_head.val` in strict O(1) time."""
        if self._head is None:
            raise IndexError("pop from an empty LinkedStack")
        top_val = self._head.val
        self._head = self._head.next
        self._size -= 1
        return top_val

    def peek(self) -> T:
        """Returns `_head.val` in O(1) time."""
        if self._head is None:
            raise IndexError("peek from an empty LinkedStack")
        return self._head.val

    def is_empty(self) -> bool:
        return self._head is None

    def __len__(self) -> int:
        return self._size

    def to_list_top_down(self) -> List[T]:
        """Returns stack contents ordered from TOP to BOTTOM."""
        out: List[T] = []
        curr = self._head
        while curr is not None:
            out.append(curr.val)
            curr = curr.next
        return out


if __name__ == "__main__":
    print("=" * 72)
    print("ArrayStack (`list`) vs LinkedStack (`_StackNode`) LIFO Verification")
    print("=" * 72)

    arr_stack: ArrayStack[str] = ArrayStack()
    lnk_stack: LinkedStack[str] = LinkedStack()

    actions = ["main()", "parse_request()", "validate_token()", "query_db()"]
    for fn in actions:
        arr_stack.push(fn)
        lnk_stack.push(fn)

    print(f"After pushing 4 call frames:")
    print(f"  ArrayStack  (top -> bottom): {arr_stack.to_list_top_down()}")
    print(f"  LinkedStack (top -> bottom): {lnk_stack.to_list_top_down()}")
    print(f"  Current Top (`peek()`)     : {arr_stack.peek()} == {lnk_stack.peek()}")

    print("\nUnwinding call stack via `pop()`:")
    while not arr_stack.is_empty():
        a_pop = arr_stack.pop()
        l_pop = lnk_stack.pop()
        assert a_pop == l_pop
        print(f"  Popped frame: {a_pop:<18} | Remaining depth: {len(arr_stack)}")

