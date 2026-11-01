"""
Topic 04: Sets
Example 01: Set Creation (`set()` vs `{}`), `remove` vs `discard`, and Hash Equivalence

Demonstrates how sets store unique hashable elements, the difference between
`.remove()` and `.discard()`, and why `{1, True, 1.0}` has only 1 element.
"""


def main() -> None:
    print("=== 1. Creating Sets (Empty Set Must Use set()) ===")
    empty_dict = {}
    empty_set = set()
    print(f"{{}}     -> type: {type(empty_dict).__name__}")
    print(f"set()  -> type: {type(empty_set).__name__}")

    print("\n=== 2. Adding & Removing: add(), update(), discard(), remove() ===")
    skills = {"Python", "Git"}
    skills.add("SQL")
    skills.update(["Docker", "Python", "AWS"])  # Duplicate 'Python' ignored automatically
    skills.discard("Java")                      # No error if 'Java' is missing!
    skills.remove("Git")                        # Removes 'Git' (raises KeyError if missing)
    print(f"Current Skills (sorted for display): {sorted(skills)}")
    print(f"'Docker' in skills (O(1) lookup)   : {'Docker' in skills}")

    print("\n=== 3. The Classic Interview Puzzle: {1, True, 1.0} ===")
    puzzle_set = {1, True, 1.0}
    print(f"{{1, True, 1.0}} -> {puzzle_set} (Length: {len(puzzle_set)})")
    print(f"Why? 1 == True == 1.0 is {1 == True == 1.0} and hash(1) == hash(True) == hash(1.0)!")


if __name__ == "__main__":
    main()
