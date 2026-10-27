"""
Topic 03 - Data Structures
Practice Question 2 Solution: Dynamic Score Registry using Built-in List Methods

Problem Statement:
Manages a score registry using in-place list methods:
1. Ingestion: append() and extend().
2. Mutation: insert() at index 1, remove(), and pop().
3. Querying: count() of score 100, index() of entry.
4. In-place ordering: sort(key=..., reverse=True) and reverse().
"""


def manage_score_registry() -> dict[str, object]:
    """Demonstrates all standard in-place list mutation methods."""
    roster: list[tuple[str, int]] = []

    # 1. Ingestion
    roster.append(("Alice", 92))
    roster.append(("Bob", 85))
    roster.extend([("Charlie", 100), ("Diana", 78), ("Evan", 100)])

    # 2. Positional insertion and removal
    roster.insert(1, ("Fiona", 88))
    if ("Diana", 78) in roster:
        roster.remove(("Diana", 78))
    popped_entry = roster.pop()

    state_after_mutations = list(roster)

    # 3. Querying
    scores_only = [score for _, score in roster]
    count_100 = scores_only.count(100)
    # Find position of Alice (score 92)
    alice_index = roster.index(("Alice", 92))

    # 4. In-Place Sorting
    roster.sort(key=lambda item: item[1], reverse=True)
    sorted_desc = list(roster)

    roster.reverse()
    reversed_asc = list(roster)

    return {
        "roster_after_mutations": state_after_mutations,
        "popped_entry": popped_entry,
        "count_100": count_100,
        "alice_index": alice_index,
        "sorted_desc": sorted_desc,
        "reversed_asc": reversed_asc,
    }


def main() -> None:
    res = manage_score_registry()

    print("Roster after insertions and removals:")
    print(res["roster_after_mutations"])
    print(f"Popped Entry: {res['popped_entry']}")
    print(f"Count of Perfect 100 Scores: {res['count_100']}")
    print(f"Index of Alice (Score 92): {res['alice_index']}")
    print("Sorted Descending by Score:")
    print(res["sorted_desc"])
    print("Reversed (Ascending):")
    print(res["reversed_asc"])


if __name__ == "__main__":
    main()
