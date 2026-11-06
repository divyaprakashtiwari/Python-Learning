"""
Phase 5 - Topic 16: Dataclasses
Example 03: Immutable, Hashable, Ordered, & Slotted Dataclasses (`frozen=True, order=True, slots=True`)

Demonstrates:
  - Creating immutable value objects (`frozen=True`) that can be used as `dict` keys or `set` members
  - Automatic comparison ordering (`order=True`) with `field(compare=False)` for non-sort fields
  - Memory/speed optimization via `slots=True` (Python 3.10+) and immutable updates via `replace()`
"""

from dataclasses import dataclass, field, replace


@dataclass(frozen=True, order=True, slots=True)
class PriorityTask:
    priority: int
    task_id: str = field(compare=False)


def main() -> None:
    print("=== 1. Sorting & Hashing with `@dataclass(frozen=True, order=True, slots=True)` ===")
    tasks = [
        PriorityTask(priority=3, task_id="cleanup-logs"),
        PriorityTask(priority=1, task_id="fix-prod-outage"),
        PriorityTask(priority=2, task_id="deploy-release"),
    ]
    print(f"  Sorted by priority : {sorted(tasks)}")
    task_set = {tasks[0], tasks[1]}
    print(f"  Usable in `set`?   : {len(task_set) == 2} | Has __dict__? {hasattr(tasks[0], '__dict__')}")

    print("\n=== 2. Creating Modified Clones of Frozen Dataclasses (`dataclasses.replace`) ===")
    escalated = replace(tasks[0], priority=0)
    print(f"  Original  : {tasks[0]}")
    print(f"  Escalated : {escalated}")


if __name__ == "__main__":
    main()
