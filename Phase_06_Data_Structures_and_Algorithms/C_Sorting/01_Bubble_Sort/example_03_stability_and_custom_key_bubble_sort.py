"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 01: Bubble Sort
Example 03: Sorting Stability Verification & Custom Key Function

Demonstrates:
1. Why Bubble Sort is a STABLE sorting algorithm:
   Because we swap ONLY on strict inequality (`key(a[j]) > key(a[j + 1])`) and NEVER on
   equality (`==`), two equal-key records never cross each other!
2. Supporting a custom `key` callable and `reverse` flag (just like Python's `list.sort`).
"""

from dataclasses import dataclass
from typing import Callable, TypeVar

T = TypeVar("T")


@dataclass
class SupportTicket:
    ticket_id: str
    priority: int  # 1 = Urgent, 2 = High, 3 = Normal
    submitted_order: int


def stable_bubble_sort_by_key(
    items: list[T],
    key: Callable[[T], int | float | str],
    reverse: bool = False,
) -> list[T]:
    """
    Generic, stable Bubble Sort supporting a custom `key` function and `reverse` order.
    Uses strict inequality (`>` or `<`) so items with equal keys preserve their original
    relative order (FIFO stability).
    """
    result = items.copy()
    n = len(result)

    for pass_num in range(n - 1):
        swapped = False
        for j in range(n - 1 - pass_num):
            left_key = key(result[j])
            right_key = key(result[j + 1])

            should_swap = (left_key < right_key) if reverse else (left_key > right_key)
            if should_swap:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True

        if not swapped:
            break

    return result


if __name__ == "__main__":
    print("=" * 72)
    print("1. VERIFYING SORTING STABILITY ON SUPPORT TICKET QUEUE")
    print("=" * 72)

    tickets = [
        SupportTicket("TCK-101", priority=2, submitted_order=1),
        SupportTicket("TCK-102", priority=1, submitted_order=2),
        SupportTicket("TCK-103", priority=2, submitted_order=3),
        SupportTicket("TCK-104", priority=1, submitted_order=4),
        SupportTicket("TCK-105", priority=3, submitted_order=5),
        SupportTicket("TCK-106", priority=1, submitted_order=6),
    ]

    sorted_tickets = stable_bubble_sort_by_key(tickets, key=lambda t: t.priority)

    print("Sorted by Priority (1 = Urgent first), preserving FIFO submission order:")
    for t in sorted_tickets:
        print(
            f"  {t.ticket_id} | Priority: {t.priority} | "
            f"Original Arrival Order: #{t.submitted_order}"
        )

    # Verify that within Priority 1, arrival order is strictly increasing [2, 4, 6]
    p1_orders = [t.submitted_order for t in sorted_tickets if t.priority == 1]
    print(f"\nPriority-1 arrival orders after sort: {p1_orders} (Strictly increasing -> STABLE!)")
