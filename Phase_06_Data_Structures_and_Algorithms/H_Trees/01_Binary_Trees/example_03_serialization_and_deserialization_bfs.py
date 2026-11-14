"""
Phase 6 - Section H.01: Binary Trees
Example 03: Serialization and Deserialization using BFS

Demonstrating:
1. Converting a binary tree into a serialized string using BFS level-order traversal.
2. Reconstructing (deserializing) the exact tree back from the serialized string.
3. Verification of structural and value equality.
"""

from collections import deque


class TreeNode:
    """Standard Binary Tree Node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class TreeCodec:
    """Encodes a tree to a single string and decodes a string back to tree."""

    def serialize(self, root):
        """Encodes a tree to a single string."""
        if not root:
            return ""

        queue = deque([root])
        result = []

        while queue:
            node = queue.popleft()
            if node:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append("#")

        # Trim trailing null sentinels
        while result and result[-1] == "#":
            result.pop()

        return ",".join(result)

    def deserialize(self, data):
        """Decodes your encoded data to tree."""
        if not data:
            return None

        vals = data.split(",")
        root = TreeNode(int(vals[0]))
        queue = deque([root])
        i = 1

        while queue and i < len(vals):
            parent = queue.popleft()

            # Left child
            if i < len(vals) and vals[i] != "#":
                parent.left = TreeNode(int(vals[i]))
                queue.append(parent.left)
            i += 1

            # Right child
            if i < len(vals) and vals[i] != "#":
                parent.right = TreeNode(int(vals[i]))
                queue.append(parent.right)
            i += 1

        return root


def is_same_tree(p, q):
    """Check if two trees are structurally identical with equal values."""
    if not p and not q:
        return True
    if not p or not q:
        return False
    return p.val == q.val and is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)


def main():
    print("=" * 60)
    print("Serialization & Deserialization (BFS Level Order)")
    print("=" * 60)

    # Build Tree:
    #       1
    #      / \
    #     2   3
    #        / \
    #       4   5
    original = TreeNode(1)
    original.left = TreeNode(2)
    original.right = TreeNode(3, TreeNode(4), TreeNode(5))

    codec = TreeCodec()
    serialized_str = codec.serialize(original)
    print("Serialized String   :", serialized_str)

    restored_tree = codec.deserialize(serialized_str)
    reserialized_str = codec.serialize(restored_tree)
    print("Reserialized String :", reserialized_str)

    identical = is_same_tree(original, restored_tree)
    print("Trees are Identical :", identical)


if __name__ == "__main__":
    main()
