"""
Topic 07: Dictionary Comprehensions
Example 03: Inverting Dictionaries and Nested Dictionary Comprehensions

Demonstrates swapping keys and values (`{v: k for k, v in d.items()}`),
what happens when values collide during inversion, and building a 2D lookup dict.
"""


def main() -> None:
    # 1. Inverting a 1-to-1 dictionary (Country -> Capital to Capital -> Country)
    country_to_capital = {
        "India": "New Delhi",
        "Japan": "Tokyo",
        "France": "Paris",
    }
    capital_to_country = {capital: country for country, capital in country_to_capital.items()}
    print("=== 1. Inverted 1-to-1 Dictionary ===")
    print(f"Capital -> Country : {capital_to_country}")

    # 2. Key Collision Behavior in Dict Comprehensions (last key wins!)
    user_scores = {"Aarav": 90, "Divya": 95, "Rohan": 90}
    score_to_last_user = {score: user for user, score in user_scores.items()}
    print("\n=== 2. Collision Behavior When Inverting Non-Unique Values ===")
    print(f"Original           : {user_scores}")
    print(f"Inverted (90 overwritten by 'Rohan'): {score_to_last_user}")

    # 3. Nested Dictionary Comprehension (3x3 Multiplication Lookup Table)
    mult_table = {
        r: {c: r * c for c in range(1, 4)}
        for r in range(1, 4)
    }
    print("\n=== 3. Nested Dict Comprehension (3x3 Table) ===")
    for row_key, inner_dict in mult_table.items():
        print(f"  Row {row_key} -> {inner_dict}")


if __name__ == "__main__":
    main()
