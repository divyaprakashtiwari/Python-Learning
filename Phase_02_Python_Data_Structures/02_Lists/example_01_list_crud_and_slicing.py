"""
Topic 02: Lists
Example 01: List Creation, CRUD Operations (`append`, `extend`, `insert`, `pop`), and Slicing

Demonstrates how Python dynamic arrays (`list`) support fast O(1) end-operations
(`append`, `pop()`) and flexible slice assignments.
"""


def main() -> None:
    tasks = ["Setup Git", "Learn Variables", "Master Loops"]
    print("=== 1. Adding Elements: append(), extend(), insert() ===")
    print(f"Initial Tasks      : {tasks}")

    tasks.append("Study Lists")                     # O(1) amortized
    tasks.extend(["Practice Tuples", "Build Sets"]) # O(k) where k is number of new items
    tasks.insert(1, "Configure IDE")                # O(n) shifts elements right
    print(f"After Additions    : {tasks}")

    print("\n=== 2. Removing Elements: pop() and remove() ===")
    last_task = tasks.pop()                         # O(1) removes & returns last item
    second_task = tasks.pop(1)                      # O(n) removes & returns index 1
    tasks.remove("Learn Variables")                 # O(n) removes first matching value
    print(f"Popped Last        : {last_task!r}")
    print(f"Popped Index 1     : {second_task!r}")
    print(f"Remaining Tasks    : {tasks}")

    print("\n=== 3. Slice Assignment (In-Place Replacement) ===")
    scores = [10, 20, 99, 99, 50]
    scores[2:4] = [30, 40]
    print(f"Fixed Scores       : {scores}")


if __name__ == "__main__":
    main()
