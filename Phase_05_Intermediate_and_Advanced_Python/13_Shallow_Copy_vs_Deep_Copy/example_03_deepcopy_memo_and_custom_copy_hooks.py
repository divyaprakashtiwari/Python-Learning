"""
Phase 5 - Topic 13: Shallow Copy vs Deep Copy
Example 03: Circular References in `deepcopy` (`memo` dict) & Custom `__copy__` / `__deepcopy__`

Demonstrates:
  - How `copy.deepcopy()` handles cyclic/self-referential graphs without infinite recursion
    using its internal `memo` dictionary
  - Implementing custom `__copy__` and `__deepcopy__` hooks on a class
"""

import copy


class CacheNode:
    """Custom class controlling how shallow and deep copies behave."""

    def __init__(self, name: str, tags: list[str], connection_id: int) -> None:
        self.name = name
        self.tags = tags
        self.connection_id = connection_id

    def __copy__(self) -> "CacheNode":
        # Shallow copy: keep same `tags` list reference, preserve `connection_id`
        return CacheNode(self.name, self.tags, self.connection_id)

    def __deepcopy__(self, memo: dict[int, object]) -> "CacheNode":
        # Deep copy: clone `tags`, but reset `connection_id` to 0 for the new clone
        cloned_tags = copy.deepcopy(self.tags, memo)
        new_node = CacheNode(self.name, cloned_tags, connection_id=0)
        memo[id(self)] = new_node
        return new_node


def main() -> None:
    print("=== 1. Cyclic Graph Handling in `copy.deepcopy()` ===")
    cyclic: list[object] = ["root"]
    cyclic.append(cyclic)  # Self-reference!
    cloned_cyclic = copy.deepcopy(cyclic)
    print(f"  Cloned cyclic structure valid? {cloned_cyclic[1] is cloned_cyclic} (no RecursionError!)")

    print("\n=== 2. Custom `__copy__` vs `__deepcopy__` Hooks ===")
    node = CacheNode("redis-primary", ["fast", "lru"], connection_id=42)
    s_node = copy.copy(node)
    d_node = copy.deepcopy(node)
    print(f"  Shallow copy : tags shared={node.tags is s_node.tags} | connection_id={s_node.connection_id}")
    print(f"  Deep copy    : tags shared={node.tags is d_node.tags} | connection_id={d_node.connection_id}")


if __name__ == "__main__":
    main()
