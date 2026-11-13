"""
Phase 6 - Data Structures and Algorithms
Section F: Stacks and Queues
Topic 04: Deque (Double-Ended Queue)
Example 02: Python's `collections.deque` Internals, Bounded `maxlen`, Rotation &
            Palindrome / Work-Stealing Scheduler

Demonstrates Python's C-accelerated `collections.deque`:
  1. `append`, `appendleft`, `pop`, `popleft`, and `rotate(k)` in O(1) / O(k) time.
  2. Bounded `deque(maxlen=k)` for automatic O(1) opposite-end eviction (`tail -n`
     log reader).
  3. Multi-Worker Work-Stealing Task Scheduler:
     - Each worker pushes/pops its own spawned subtasks in **LIFO order at its own
       front** (`appendleft` / `popleft`) for hot CPU cache locality.
     - An idle worker steals large parent tasks from the **rear (FIFO end)** of the
       busiest worker's deque (`pop()`) in O(1) time!
"""

from collections import deque
from typing import Deque, List


def is_palindrome_via_deque(text: str) -> bool:
    """Checks alphanumeric palindrome by popping from both ends of a deque simultaneously."""
    cleaned = [ch.lower() for ch in text if ch.isalnum()]
    dq: Deque[str] = deque(cleaned)
    while len(dq) > 1:
        if dq.popleft() != dq.pop():
            return False
    return True


def simulate_work_stealing_scheduler() -> None:
    """Simulates a 2-worker Fork-Join Work-Stealing Deque scheduler."""
    worker_0_deque: Deque[str] = deque()
    worker_1_deque: Deque[str] = deque()

    # Worker 0 starts with 3 coarse root tasks pushed at the rear
    for root_task in ["Root_Chunk_A", "Root_Chunk_B", "Root_Chunk_C"]:
        worker_0_deque.append(root_task)

    # Worker 0 spawns two fine-grained child tasks at its own hot front (`appendleft`)
    worker_0_deque.appendleft("Subtask_A2")
    worker_0_deque.appendleft("Subtask_A1")

    print(f"Initial Worker 0 Deque (front -> rear): {list(worker_0_deque)}")
    print(f"Initial Worker 1 Deque (idle)         : {list(worker_1_deque)}")

    # Worker 1 is idle, so it steals from the REAR (`pop()`) of Worker 0's deque!
    stolen = worker_0_deque.pop()
    worker_1_deque.appendleft(stolen)
    print(f"\nWorker 1 steals coarse task from Worker 0's rear -> '{stolen}'")
    print(f"Worker 0 Deque now: {list(worker_0_deque)}")
    print(f"Worker 1 Deque now: {list(worker_1_deque)}")

    # Worker 0 executes its own hot front task (`popleft()`)
    executed_w0 = worker_0_deque.popleft()
    executed_w1 = worker_1_deque.popleft()
    print(f"Worker 0 executes front (LIFO): '{executed_w0}'")
    print(f"Worker 1 executes stolen task : '{executed_w1}'")


if __name__ == "__main__":
    print("=" * 72)
    print("1. `collections.deque` Rotation & Bounded `maxlen` Tail Window")
    print("=" * 72)

    ring: Deque[int] = deque([10, 20, 30, 40, 50])
    ring.rotate(2)   # Right rotation by 2
    print(f"After rotate(+2) on [10..50]: {list(ring)}")
    ring.rotate(-2)  # Left rotation by 2 restores original
    print(f"After rotate(-2)            : {list(ring)}")

    tail_lines: Deque[str] = deque(maxlen=3)
    for i in range(1, 7):
        tail_lines.append(f"log_line_{i}")
    print(f"Bounded deque(maxlen=3) after 6 lines: {list(tail_lines)}")

    print("\n" + "=" * 72)
    print("2. Two-Ended Deque Palindrome Check")
    print("=" * 72)
    for phrase in ["A man, a plan, a canal: Panama", "Race a car"]:
        print(f"  '{phrase}' -> {is_palindrome_via_deque(phrase)}")

    print("\n" + "=" * 72)
    print("3. Work-Stealing Deque Scheduler (LIFO Local Front, FIFO Steal Rear)")
    print("=" * 72)
    simulate_work_stealing_scheduler()

