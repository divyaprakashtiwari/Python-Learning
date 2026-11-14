"""
Phase 6 - Section G.05: Hashing Problems
Example 02: Copy List with Random Pointer

Demonstrating:
1. Deep copy of linked list with random pointers using Hash Map (Node -> Clone).
2. Interleaving in-place pointer copying for O(1) auxiliary space optimization.
"""


class Node:
    """Linked list node with next and random pointer."""
    def __init__(self, val, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


def copy_random_list_hashmap(head):
    """
    Clone list using Hash Map mapping old_node -> new_node.
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not head:
        return None

    clone_map = {}

    # Pass 1: create all clones without wiring
    curr = head
    while curr:
        clone_map[curr] = Node(curr.val)
        curr = curr.next

    # Pass 2: wire next and random pointers
    curr = head
    while curr:
        if curr.next:
            clone_map[curr].next = clone_map[curr.next]
        if curr.random:
            clone_map[curr].random = clone_map[curr.random]
        curr = curr.next

    return clone_map[head]


def copy_random_list_interleaved(head):
    """
    Clone list in-place by interleaving cloned nodes.
    Time Complexity: O(n)
    Space Complexity: O(1) auxiliary
    """
    if not head:
        return None

    # Step 1: Interleave cloned nodes (A -> A' -> B -> B')
    curr = head
    while curr:
        clone = Node(curr.val, next=curr.next)
        curr.next = clone
        curr = clone.next

    # Step 2: Assign random pointers
    curr = head
    while curr:
        if curr.random:
            curr.next.random = curr.random.next
        curr = curr.next.next

    # Step 3: Separate the two lists
    dummy = Node(0)
    copy_tail = dummy
    curr = head
    while curr:
        copy_tail.next = curr.next
        copy_tail = copy_tail.next
        curr.next = curr.next.next
        curr = curr.next

    return dummy.next


def list_to_repr(head):
    """Serialize list nodes and random targets for verification."""
    nodes = []
    curr = head
    index_map = {}
    idx = 0
    while curr:
        index_map[curr] = idx
        nodes.append(curr)
        curr = curr.next
        idx += 1

    result = []
    for node in nodes:
        rand_idx = index_map[node.random] if node.random else None
        result.append((node.val, rand_idx))
    return result


def main():
    print("=" * 60)
    print("Copy List with Random Pointer")
    print("=" * 60)

    # Build test list: [[7,null],[13,0],[11,4],[10,2],[1,0]]
    n0 = Node(7)
    n1 = Node(13)
    n2 = Node(11)
    n3 = Node(10)
    n4 = Node(1)

    n0.next = n1
    n1.next = n2
    n2.next = n3
    n3.next = n4

    n1.random = n0
    n2.random = n4
    n3.random = n2
    n4.random = n0

    print("Original List Structure [(val, random_index)]:")
    print(" ", list_to_repr(n0))

    clone1 = copy_random_list_hashmap(n0)
    print("\nClone via Hash Map [(val, random_index)]:")
    print(" ", list_to_repr(clone1))
    print("Verified distinct nodes in memory:", clone1 is not n0 and clone1.next is not n1)

    clone2 = copy_random_list_interleaved(n0)
    print("\nClone via Interleaving O(1) Space [(val, random_index)]:")
    print(" ", list_to_repr(clone2))
    print("Verified distinct nodes in memory:", clone2 is not n0 and clone2.next is not n1)


if __name__ == "__main__":
    main()
