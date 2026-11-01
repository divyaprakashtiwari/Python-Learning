"""
Topic 08: Nested Data Structures
Example 02: List of Dictionaries — JSON-Style Student & Placement Analytics

Demonstrates querying, filtering, and aggregating a list of nested dictionary
records (the exact structure returned by REST APIs and MongoDB queries).
"""


def main() -> None:
    students = [
        {
            "id": 101,
            "name": "Divya Prakash",
            "skills": ["Python", "DSA", "SQL"],
            "scores": {"coding": 95, "system_design": 88},
        },
        {
            "id": 102,
            "name": "Aarav Sharma",
            "skills": ["Java", "Spring", "SQL"],
            "scores": {"coding": 84, "system_design": 91},
        },
        {
            "id": 103,
            "name": "Sneha Verma",
            "skills": ["Python", "PyTorch", "DSA"],
            "scores": {"coding": 92, "system_design": 85},
        },
    ]

    print("=== 1. Filtering Nested Records (Python + DSA Skills) ===")
    python_dsa_candidates = [
        s["name"]
        for s in students
        if "Python" in s["skills"] and "DSA" in s["skills"]
    ]
    print(f"Python + DSA Candidates : {python_dsa_candidates}")

    print("\n=== 2. Ranking by Nested Total Score ===")
    ranked = sorted(
        students,
        key=lambda s: s["scores"]["coding"] + s["scores"]["system_design"],
        reverse=True,
    )
    for rank, s in enumerate(ranked, start=1):
        total = s["scores"]["coding"] + s["scores"]["system_design"]
        print(f"  #{rank}: {s['name']:<15} | Total: {total} (Coding: {s['scores']['coding']})")


if __name__ == "__main__":
    main()
