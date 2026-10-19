"""
Topic: Data Structures and Algorithms (DSA) - Linked List
---------------------------------------------------------
Questions Covered:
1. Singly Linked List Fundamentals: Head/tail insertion, deletion, lookup, and length.
2. In-Place Reversal (Iterative & Recursive): Three-pointer mutation reversing links in O(n).
3. Cycle Detection & Entry Point (Floyd's Algorithm): Tortoise and hare finding loop existence and cycle entry.
4. Middle of Linked List: Fast and slow pointer technique locating middle node in a single pass.
5. Merge Two Sorted Lists: Splicing sorted chains into a unified sorted list in O(1) auxiliary space.
6. Remove N-th Node From End: Fixed-gap pointer window deleting target in single pass.
7. Palindrome Linked List Verification: Splitting, second-half reversal, and in-place restoration.
8. Intersection Node of Two Lists: Two-pointer boundary cycling locating convergence point.
9. Reverse Nodes in K-Group: Reversing sublists in contiguous groups of size k.
10. Architectural System: Production LRU Cache with Doubly Linked List & Hash Map (O(1) Get/Put).
"""

from typing import List, Optional, Any, Dict, Tuple


# ==============================================================================
# Question 1: Singly Linked List Core Implementation
# ==============================================================================
class ListNode:
    def __init__(self, val: Any = 0, next_node: Optional["ListNode"] = None):
        self.val = val
        self.next = next_node


class SinglyLinkedList:
    def __init__(self):
        self.head: Optional[ListNode] = None
        self._size = 0

    def insert_head(self, val: Any) -> None:
        self.head = ListNode(val, self.head)
        self._size += 1

    def insert_tail(self, val: Any) -> None:
        new_node = ListNode(val)
        if not self.head:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node
        self._size += 1

    def delete_value(self, val: Any) -> bool:
        dummy = ListNode(0, self.head)
        prev = dummy
        curr = self.head
        found = False

        while curr:
            if curr.val == val:
                prev.next = curr.next
                self._size -= 1
                found = True
                break
            prev = curr
            curr = curr.next

        self.head = dummy.next
        return found

    def to_list(self) -> List[Any]:
        res = []
        curr = self.head
        while curr:
            res.append(curr.val)
            curr = curr.next
        return res

    def __len__(self) -> int:
        return self._size


def test_q1_singly_linked_list():
    sll = SinglyLinkedList()
    sll.insert_head(20)
    sll.insert_head(10)
    sll.insert_tail(30)
    assert sll.to_list() == [10, 20, 30]
    assert len(sll) == 3

    assert sll.delete_value(20) is True
    assert sll.to_list() == [10, 30]
    assert len(sll) == 2
    assert sll.delete_value(99) is False
    print("=== Q1: Singly Linked List Core Implementation Verified ===")


# ==============================================================================
# Question 2: In-Place Reversal (Iterative & Recursive)
# ==============================================================================
def reverse_list_iterative(head: Optional[ListNode]) -> Optional[ListNode]:
    """Reverses linked list in-place using 3 pointers: prev, curr, next_node."""
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev


def reverse_list_recursive(head: Optional[ListNode]) -> Optional[ListNode]:
    """Reverses linked list recursively."""
    if not head or not head.next:
        return head
    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head


def build_linked_list(vals: List[Any]) -> Optional[ListNode]:
    dummy = ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next


def linked_list_to_py_list(head: Optional[ListNode]) -> List[Any]:
    res = []
    curr = head
    while curr:
        res.append(curr.val)
        curr = curr.next
    return res


def test_q2_reverse_linked_list():
    l1 = build_linked_list([1, 2, 3, 4, 5])
    rev1 = reverse_list_iterative(l1)
    assert linked_list_to_py_list(rev1) == [5, 4, 3, 2, 1]

    l2 = build_linked_list([10, 20])
    rev2 = reverse_list_recursive(l2)
    assert linked_list_to_py_list(rev2) == [20, 10]

    assert reverse_list_iterative(None) is None
    print("=== Q2: In-Place Reversal (Iterative & Recursive) Verified ===")


# ==============================================================================
# Question 3: Cycle Detection & Entry Point (Floyd's Tortoise and Hare)
# ==============================================================================
def detect_cycle_entry(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Detects if a linked list contains a cycle.
    If so, returns the exact node where the cycle begins.
    If no cycle exists, returns None.
    Time: O(n), Auxiliary Space: O(1).
    """
    if not head or not head.next:
        return None

    slow = head
    fast = head

    # 1. Detect intersection
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # No cycle

    # 2. Find entry point: move slow to head, advance both by 1
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next

    return slow


def test_q3_cycle_detection():
    # Build list with cycle: 3 -> 2 -> 0 -> -4 -> (points back to node 2)
    node1 = ListNode(3)
    node2 = ListNode(2)
    node3 = ListNode(0)
    node4 = ListNode(-4)
    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node2  # Cycle back to node2

    entry = detect_cycle_entry(node1)
    assert entry is node2

    # Acyclic list
    acyclic = build_linked_list([1, 2, 3])
    assert detect_cycle_entry(acyclic) is None
    print("=== Q3: Cycle Detection & Entry Point Verified ===")


# ==============================================================================
# Question 4: Find Middle Node of Linked List
# ==============================================================================
def find_middle_node(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Returns the middle node of linked list using fast and slow pointers.
    If there are two middle nodes (even length), returns the second middle node.
    """
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


def test_q4_find_middle():
    # Odd length: middle is 3
    l_odd = build_linked_list([1, 2, 3, 4, 5])
    mid_odd = find_middle_node(l_odd)
    assert mid_odd is not None and mid_odd.val == 3

    # Even length: middle is 4 (second of 3 and 4)
    l_even = build_linked_list([1, 2, 3, 4, 5, 6])
    mid_even = find_middle_node(l_even)
    assert mid_even is not None and mid_even.val == 4
    print("=== Q4: Middle Node Detection Verified ===")


# ==============================================================================
# Question 5: Merge Two Sorted Linked Lists
# ==============================================================================
def merge_two_sorted_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Merges two sorted linked lists into one sorted linked list in O(n + m) time,
    using O(1) extra space by splicing existing nodes.
    """
    dummy = ListNode(0)
    tail = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next

    tail.next = l1 if l1 else l2
    return dummy.next


def test_q5_merge_sorted_lists():
    a = build_linked_list([1, 2, 4])
    b = build_linked_list([1, 3, 4])
    merged = merge_two_sorted_lists(a, b)
    assert linked_list_to_py_list(merged) == [1, 1, 2, 3, 4, 4]

    c = build_linked_list([5, 10])
    d = None
    assert linked_list_to_py_list(merge_two_sorted_lists(c, d)) == [5, 10]
    print("=== Q5: Merge Two Sorted Linked Lists Verified ===")


# ==============================================================================
# Question 6: Remove N-th Node From End of List
# ==============================================================================
def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """
    Removes the n-th node from the end of the list and returns its head in one pass.
    """
    dummy = ListNode(0, head)
    fast: Optional[ListNode] = dummy
    slow: Optional[ListNode] = dummy

    # Advance fast pointer by n + 1 steps
    for _ in range(n + 1):
        if fast:
            fast = fast.next

    while fast:
        fast = fast.next
        slow = slow.next

    # slow is now just before the node to be removed
    if slow and slow.next:
        slow.next = slow.next.next

    return dummy.next


def test_q6_remove_nth_from_end():
    l1 = build_linked_list([1, 2, 3, 4, 5])
    # Remove 2nd from end (node 4)
    res1 = remove_nth_from_end(l1, 2)
    assert linked_list_to_py_list(res1) == [1, 2, 3, 5]

    # Remove only node (1st from end)
    l2 = build_linked_list([10])
    res2 = remove_nth_from_end(l2, 1)
    assert linked_list_to_py_list(res2) == []

    # Remove head (2nd from end of length 2)
    l3 = build_linked_list([1, 2])
    res3 = remove_nth_from_end(l3, 2)
    assert linked_list_to_py_list(res3) == [2]
    print("=== Q6: Remove N-th Node From End in One Pass Verified ===")


# ==============================================================================
# Question 7: Palindrome Linked List Verification
# ==============================================================================
def is_palindrome_linked_list(head: Optional[ListNode]) -> bool:
    """
    Checks if a linked list is a palindrome in O(n) time and O(1) auxiliary space:
    1. Finds middle using slow/fast pointers.
    2. Reverses the second half in-place.
    3. Compares first half and second half.
    4. Restores second half (maintains list structure integrity).
    """
    if not head or not head.next:
        return True

    # 1. Find end of first half
    slow = head
    fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    # 2. Reverse second half
    second_half_head = reverse_list_iterative(slow.next)

    # 3. Check palindrome match
    p1 = head
    p2 = second_half_head
    is_pal = True
    while is_pal and p2:
        if p1.val != p2.val:
            is_pal = False
        p1 = p1.next
        p2 = p2.next

    # 4. Restore list
    slow.next = reverse_list_iterative(second_half_head)
    return is_pal


def test_q7_palindrome_linked_list():
    p1 = build_linked_list([1, 2, 2, 1])
    assert is_palindrome_linked_list(p1) is True
    # Verify structure was preserved after test
    assert linked_list_to_py_list(p1) == [1, 2, 2, 1]

    p2 = build_linked_list([1, 2, 3, 2, 1])
    assert is_palindrome_linked_list(p2) is True

    non_pal = build_linked_list([1, 2, 3])
    assert is_palindrome_linked_list(non_pal) is False
    print("=== Q7: Palindrome Linked List Verification Verified ===")


# ==============================================================================
# Question 8: Intersection of Two Linked Lists
# ==============================================================================
def get_intersection_node(head_a: Optional[ListNode], head_b: Optional[ListNode]) -> Optional[ListNode]:
    """
    Finds node where two singly linked lists intersect in O(n + m) time and O(1) space.
    Switches pointer to other head upon reaching end to equalize path lengths.
    """
    if not head_a or not head_b:
        return None

    p_a = head_a
    p_b = head_b

    while p_a != p_b:
        p_a = p_a.next if p_a else head_b
        p_b = p_b.next if p_b else head_a

    return p_a


def test_q8_intersection_node():
    common = ListNode(8, ListNode(4, ListNode(5)))

    # List A: 4 -> 1 -> common
    head_a = ListNode(4, ListNode(1, common))
    # List B: 5 -> 6 -> 1 -> common
    head_b = ListNode(5, ListNode(6, ListNode(1, common)))

    intersect = get_intersection_node(head_a, head_b)
    assert intersect is common
    assert intersect.val == 8

    # Non-intersecting lists
    sep_a = build_linked_list([1, 2])
    sep_b = build_linked_list([3, 4])
    assert get_intersection_node(sep_a, sep_b) is None
    print("=== Q8: Intersection of Two Linked Lists Verified ===")


# ==============================================================================
# Question 9: Reverse Nodes in K-Group
# ==============================================================================
def reverse_k_group(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """
    Reverses nodes of list k at a time and returns modified list.
    Nodes that do not form a full group of k remain untouched.
    """
    # Check if there are at least k nodes remaining
    curr = head
    count = 0
    while curr and count < k:
        curr = curr.next
        count += 1

    if count < k:
        return head  # Less than k nodes, return as is

    # Reverse k nodes
    prev = None
    curr = head
    for _ in range(k):
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    # head is now tail of this reversed group; link to recursively reversed rest
    head.next = reverse_k_group(curr, k)
    return prev


def test_q9_reverse_k_group():
    l1 = build_linked_list([1, 2, 3, 4, 5])
    # k=2: [2, 1, 4, 3, 5]
    res1 = reverse_k_group(l1, 2)
    assert linked_list_to_py_list(res1) == [2, 1, 4, 3, 5]

    l2 = build_linked_list([1, 2, 3, 4, 5])
    # k=3: [3, 2, 1, 4, 5]
    res2 = reverse_k_group(l2, 3)
    assert linked_list_to_py_list(res2) == [3, 2, 1, 4, 5]
    print("=== Q9: Reverse Nodes in K-Group Verified ===")


# ==============================================================================
# Question 10: Architectural System: Production LRU Cache with Doubly Linked List
# ==============================================================================
class DListNode:
    def __init__(self, key: Any = 0, val: Any = 0):
        self.key = key
        self.val = val
        self.prev: Optional["DListNode"] = None
        self.next: Optional["DListNode"] = None


class LRUCache:
    """
    High-performance LRU Cache implementing O(1) get and O(1) put.
    Uses hash map for key lookup and doubly linked list with sentinel dummy
    head and tail for constant-time node removal and front-insertion.
    """
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.cache: Dict[Any, DListNode] = {}
        # Sentinel dummy nodes
        self.head = DListNode()
        self.tail = DListNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: DListNode) -> None:
        """Removes an existing node from the doubly linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_front(self, node: DListNode) -> None:
        """Inserts node immediately after the sentinel dummy head."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: Any) -> Any:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)  # Move to most recently used
        return node.val

    def put(self, key: Any, value: Any) -> None:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            node.val = value
            self._add_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                # Evict least recently used (node before dummy tail)
                lru_node = self.tail.prev
                self._remove(lru_node)
                del self.cache[lru_node.key]

            new_node = DListNode(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)


def test_q10_lru_cache():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1       # returns 1, makes 1 most recently used
    cache.put(3, 3)                # evicts key 2 (least recently used)
    assert cache.get(2) == -1      # returns -1 (not found)
    cache.put(4, 4)                # evicts key 1 (least recently used)
    assert cache.get(1) == -1      # returns -1 (not found)
    assert cache.get(3) == 3       # returns 3
    assert cache.get(4) == 4       # returns 4
    print("=== Q10: Architectural Production LRU Cache Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_singly_linked_list()
    test_q2_reverse_linked_list()
    test_q3_cycle_detection()
    test_q4_find_middle()
    test_q5_merge_sorted_lists()
    test_q6_remove_nth_from_end()
    test_q7_palindrome_linked_list()
    test_q8_intersection_node()
    test_q9_reverse_k_group()
    test_q10_lru_cache()
    print("\nAll 10 linked list DSA questions passed successfully!")
