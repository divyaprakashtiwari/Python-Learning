"""
Phase 6 - Data Structures and Algorithms
Section E: Linked Lists - Topic 03: Circular Linked List
Example 03: Round-Robin CPU Process Scheduler & The Josephus Problem Simulation

Demonstrates:
1. OS Round-Robin Time-Slice Scheduler using a Circular Singly Linked List:
   Each active task gets a fixed `time_quantum` (e.g., 4 ms). If it still has remaining
   burst time, we rotate the ring in O(1) (`ring.rotate_forward()`); if it finishes, we
   remove it from the front in O(1) (`ring.pop_front()`)!
2. Simulating the classic Flavius Josephus Elimination Circle on a Circular Linked List.
"""

from dataclasses import dataclass
from example_01_tail_anchored_circular_singly_linked_list import (
    CNode,
    CircularSinglyLinkedList,
)


@dataclass
class TaskBurst:
    name: str
    remaining_ms: int


def simulate_round_robin_scheduler(
    tasks: list[tuple[str, int]], quantum_ms: int
) -> list[tuple[str, int]]:
    """
    Simulate an OS Round-Robin CPU scheduler using a tail-anchored Circular Linked List.
    Returns list of `(task_name, completion_time_ms)` in order of completion.
    """
    ring = CircularSinglyLinkedList()
    for name, burst in tasks:
        ring.insert_back( TaskBurst(name, burst) )  # type: ignore[arg-type]

    clock_ms = 0
    completed: list[tuple[str, int]] = []

    while len(ring) > 0:
        assert ring.tail is not None and ring.tail.next is not None
        head_task: TaskBurst = ring.tail.next.val  # type: ignore[assignment]
        run_slice = min(quantum_ms, head_task.remaining_ms)
        clock_ms += run_slice
        head_task.remaining_ms -= run_slice

        if head_task.remaining_ms == 0:
            ring.pop_front()
            completed.append((head_task.name, clock_ms))
        else:
            # Rotate active task to the back of the circular queue in O(1)!
            ring.rotate_forward()

    return completed


def josephus_circle_simulation(n: int, k: int) -> tuple[int, list[int]]:
    """
    Simulate the Josephus Problem for `n` people (numbered `1..n`) eliminating every `k`-th
    person around a Circular Linked List until 1 survivor remains.
    Returns `(survivor, elimination_order)`.
    """
    ring = CircularSinglyLinkedList()
    for person in range(1, n + 1):
        ring.insert_back(person)

    eliminated: list[int] = []
    while len(ring) > 1:
        # Advance k - 1 steps around the circle
        for _ in range(k - 1):
            ring.rotate_forward()
        # Pop the k-th person from the front of the ring
        eliminated.append(ring.pop_front())

    survivor = ring.pop_front()
    return survivor, eliminated


if __name__ == "__main__":
    print("=" * 72)
    print("1. OS ROUND-ROBIN CPU SCHEDULER (TIME QUANTUM = 4 ms)")
    print("=" * 72)
    workload = [("P1_Web", 10), ("P2_DB", 4), ("P3_Auth", 6)]
    print(f"Initial Tasks (Name, Burst ms): {workload}")
    finish_log = simulate_round_robin_scheduler(workload, quantum_ms=4)
    for name, t_done in finish_log:
        print(f"  Task {name:<8} completed at t = {t_done:>2} ms")

    print("\n" + "=" * 72)
    print("2. JOSEPHUS ELIMINATION CIRCLE (N = 7, EVERY K = 3RD ELIMINATED)")
    print("=" * 72)
    surv, order = josephus_circle_simulation(n=7, k=3)
    print(f"Elimination Order : {order}")
    print(f"Last Survivor     : Person #{surv}")

