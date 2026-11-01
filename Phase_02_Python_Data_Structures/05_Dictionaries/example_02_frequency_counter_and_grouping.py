"""
Topic 05: Dictionaries
Example 02: Frequency Counting (`d.get`) and Grouping Records (`d.setdefault`)

Demonstrates two of the most common real-world dictionary idioms:
1. Counting frequencies in a single pass with `counts[item] = counts.get(item, 0) + 1`.
2. Grouping items into lists by key with `groups.setdefault(key, []).append(val)`.
"""


def count_word_frequencies(sentence: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in sentence.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def group_students_by_department(records: list[tuple[str, str]]) -> dict[str, list[str]]:
    departments: dict[str, list[str]] = {}
    for student_name, dept in records:
        departments.setdefault(dept, []).append(student_name)
    return departments


def main() -> None:
    text = "python dsa python backend dsa python"
    print("=== 1. Word Frequency Counter ===")
    freq = count_word_frequencies(text)
    print(f"Frequencies : {freq}")

    print("\n=== 2. Grouping Students by Department (.setdefault) ===")
    enrollments = [
        ("Divya", "CSE"),
        ("Aarav", "ECE"),
        ("Rohan", "CSE"),
        ("Sneha", "IT"),
        ("Kabir", "ECE"),
    ]
    grouped = group_students_by_department(enrollments)
    for dept, students in grouped.items():
        print(f"  {dept:<4} -> {students}")


if __name__ == "__main__":
    main()
