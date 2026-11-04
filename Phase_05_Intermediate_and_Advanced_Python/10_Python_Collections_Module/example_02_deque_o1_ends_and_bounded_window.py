"""
Phase 5 - Topic 10: Python Collections Module
Example 02: `deque` — O(1) Double-Ended Queue, Ring Buffer (`maxlen`), & `.rotate()`

Demonstrates:
  - O(1) `.appendleft()` and `.popleft()` on `collections.deque` (vs O(n) `list.pop(0)`)
  - Bounded ring buffer using `deque(maxlen=3)` to retain only the N most recent events
  - Circular rotation with `dq.rotate(k)`
"""

from collections import deque


def main() -> None:
    print("=== 1. O(1) Double-Ended Queue Operations (`appendleft` / `popleft`) ===")
    task_queue: deque[str] = deque(["normal-1", "normal-2"])
    task_queue.append("normal-3")
    task_queue.appendleft("URGENT-0")  # O(1) front insertion
    print(f"  Queue after urgent arrival: {list(task_queue)}")
    print(f"  Dispatched first (`popleft`): {task_queue.popleft()!r} -> remaining: {list(task_queue)}")

    print("\n=== 2. Bounded Sliding Ring Buffer (`deque(maxlen=3)`) ===")
    recent_errors: deque[str] = deque(maxlen=3)
    for idx in range(1, 6):
        recent_errors.append(f"ERR-10{idx}")
        print(f"  After ERR-10{idx}: {list(recent_errors)}")

    print("\n=== 3. Round-Robin Schedule via `deque.rotate(-1)` ===")
    on_call = deque(["Alice", "Bob", "Charlie"])
    for week in range(1, 4):
        print(f"  Week {week} primary on-call: {on_call[0]} (rotation={list(on_call)})")
        on_call.rotate(-1)


if __name__ == "__main__":
    main()
