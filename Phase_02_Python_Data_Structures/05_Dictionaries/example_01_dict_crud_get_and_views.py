"""
Topic 05: Dictionaries
Example 01: Dictionary CRUD, Safe `.get()`, View Objects, and Merge Operators (`|`)

Demonstrates `O(1)` key-value lookups, avoiding `KeyError` with `.get()`,
iterating over `.items()`, and merging dictionaries in Python 3.9+ using `|`.
"""


def main() -> None:
    profile: dict[str, str | int] = {
        "username": "divya_tiwari",
        "role": "Learner",
        "streak_days": 15,
    }

    print("=== 1. Safe Lookup (.get) vs Direct Indexing ([]) ===")
    print(f"Username          : {profile['username']}")
    print(f"Missing key (.get): {profile.get('github_stars', 0)} (No KeyError!)")

    print("\n=== 2. Updating, Popping, and Merging (`|`) ===")
    profile["streak_days"] = 16
    extra_settings = {"role": "Contributor", "theme": "dark"}
    merged_profile = profile | extra_settings  # Right-hand values win on key collisions
    removed_theme = merged_profile.pop("theme", "default")
    print(f"Merged Profile    : {merged_profile}")
    print(f"Popped Theme      : {removed_theme!r}")

    print("\n=== 3. Iterating Over .keys(), .values(), and .items() ===")
    for key, value in merged_profile.items():
        print(f"  {key:<12} -> {value}")


if __name__ == "__main__":
    main()
