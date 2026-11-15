"""
Phase 6 - Section H.07: Balanced Trees
Example 02: Convert Sorted Structures to Balanced BST

Demonstrating:
1. Convert Sorted Array to Height-Balanced BST via divide-and-conquer in O(n) time.
2. Convert Sorted Linked List to Balanced BST in O(n) time and O(log n) space using inorder simulation.
"""


class TreeNode:
    """Binary Search Tree Node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class ListNode:
    """Singly Linked List Node."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def sorted_array_to_bst(nums):
    """
    Construct a height-balanced BST from sorted array.
    Picks middle element as root to ensure equal partition.
    Time Complexity: O(n)
    Space Complexity: O(log n)
    """
    def build(left, right):
        if left > right:
            return None

        mid = (left + right) // 2
        root = TreeNode(nums[mid])
        root.left = build(left, mid - 1)
        root.right = build(mid + 1, right)
        return root

    return build(0, len(nums) - 1)


def sorted_list_to_bst(head):
    """
    Convert sorted linked list to balanced BST in O(n) time.
    Simulates inorder traversal while advancing list pointer.
    Time Complexity: O(n)
    Space Complexity: O(log n)
    """
    # Count list length
    length = 0
    curr = head
    while curr:
        length += 1
        curr = curr.next

    curr_head = head

    def convert(left, right):
        nonlocal curr_head
        if left > right:
            return None

        mid = (left + right) // 2

        # 1. Build left subtree
        left_child = convert(left, mid - 1)

        # 2. Current root is current list node
        root = TreeNode(curr_head.val)
        root.left = left_child
        curr_head = curr_head.next

        # 3. Build right subtree
        root.right = convert(mid + 1, right)

        return root

    return convert(0, length - 1)


def inorder_traversal(root):
    """Return inorder list of values."""
    res = []
    def dfs(node):
        if node:
            dfs(node.left)
            res.append(node.val)
            dfs(node.right)
    dfs(root)
    return res


def get_height(root):
    if not root:
        return 0
    return 1 + max(get_height(root.left), get_height(root.right))


def main():
    print("=" * 60)
    print("1. Sorted Array to Balanced BST")
    print("=" * 60)
    arr = [-10, -3, 0, 5, 9]
    bst_from_arr = sorted_array_to_bst(arr)
    print("Input Array    :", arr)
    print("Inorder of BST :", inorder_traversal(bst_from_arr))
    print("Height of BST  :", get_height(bst_from_arr))
    print("Root Value     :", bst_from_arr.val)

    print("\n" + "=" * 60)
    print("2. Sorted Linked List to Balanced BST (Inorder Simulation O(n))")
    print("=" * 60)
    # List: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7
    dummy = ListNode(0)
    tail = dummy
    for x in range(1, 8):
        tail.next = ListNode(x)
        tail = tail.next

    bst_from_list = sorted_list_to_bst(dummy.next)
    print("List Elements  :", list(range(1, 8)))
    print("Inorder of BST :", inorder_traversal(bst_from_list))
    print("Height of BST  :", get_height(bst_from_list))
    print("Root Value     :", bst_from_list.val)


if __name__ == "__main__":
    main()
