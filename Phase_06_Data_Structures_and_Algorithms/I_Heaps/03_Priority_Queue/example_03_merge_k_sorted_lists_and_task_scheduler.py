"""
Phase 6 - Section I.03: Priority Queue
Example 03: Merge K Sorted Lists and Task Scheduler

Demonstrating:
1. Merge K Sorted Lists in O(N log K) time using a Priority Queue.
2. CPU Task Scheduler with cooldown intervals using Max-Priority Queue + Queue.
"""

import heapq
from collections import Counter, deque


class ListNode:
    """Singly-linked list node."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_k_sorted_lists(lists):
    """
    Merge k sorted linked lists in O(N log k) time and O(k) space.
    Uses entry tuple (node.val, list_index, node) to safely break ties.
    """
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    dummy = ListNode(0)
    tail = dummy

    while heap:
        val, i, node = heapq.heappop(heap)
        tail.next = node
        tail = tail.next

        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next


def least_interval_task_scheduler(tasks, n):
    """
    CPU Task Scheduler with cooldown period n between identical tasks.
    Time Complexity: O(total_tasks)
    Space Complexity: O(distinct_tasks)
    """
    counts = Counter(tasks)
    # Max-heap of task counts (negated)
    max_heap = [-cnt for cnt in counts.values()]
    heapq.heapify(max_heap)

    # Queue stores: (remaining_count, ready_time)
    cooldown_q = deque()
    time = 0

    while max_heap or cooldown_q:
        time += 1

        if max_heap:
            cnt = 1 + heapq.heappop(max_heap)  # Note: negative count + 1 = decrement frequency
            if cnt < 0:
                cooldown_q.append((cnt, time + n))

        if cooldown_q and cooldown_q[0][1] == time:
            ready_cnt, _ = cooldown_q.popleft()
            heapq.heappush(max_heap, ready_cnt)

    return time


def list_to_array(head):
    res = []
    curr = head
    while curr:
        res.append(curr.val)
        curr = curr.next
    return res


def array_to_list(arr):
    dummy = ListNode(0)
    tail = dummy
    for x in arr:
        tail.next = ListNode(x)
        tail = tail.next
    return dummy.next


def main():
    print("=" * 60)
    print("1. Merge K Sorted Lists (O(N log K))")
    print("=" * 60)
    l1 = array_to_list([1, 4, 5])
    l2 = array_to_list([1, 3, 4])
    l3 = array_to_list([2, 6])
    input_lists = [l1, l2, l3]

    merged_head = merge_k_sorted_lists(input_lists)
    print("Input Lists : [[1, 4, 5], [1, 3, 4], [2, 6]]")
    print("Merged List :", list_to_array(merged_head))

    print("\n" + "=" * 60)
    print("2. CPU Task Scheduler with Cooldown")
    print("=" * 60)
    tasks1 = ["A", "A", "A", "B", "B", "B"]
    cooldown1 = 2
    cycles1 = least_interval_task_scheduler(tasks1, cooldown1)
    print(f"Tasks: {tasks1}, Cooldown: {cooldown1} -> Minimum CPU Cycles: {cycles1}")

    tasks2 = ["A", "C", "A", "B", "D", "B"]
    cooldown2 = 1
    cycles2 = least_interval_task_scheduler(tasks2, cooldown2)
    print(f"Tasks: {tasks2}, Cooldown: {cooldown2} -> Minimum CPU Cycles: {cycles2}")


if __name__ == "__main__":
    main()
