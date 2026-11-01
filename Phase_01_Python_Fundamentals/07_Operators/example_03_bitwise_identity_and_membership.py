"""
Topic 07: Operators
Example 03: Bitwise, Identity (`is`), Membership (`in`), and Walrus (`:=`) Operators

Demonstrates permission bitmasks using bitwise operators, identity vs equality,
`O(1)` set membership testing, and assignment expressions (`:=`).
"""


def main() -> None:
    # 1. Bitwise Permission Flags (Read=4, Write=2, Execute=1)
    READ = 0b100     # 4
    WRITE = 0b010    # 2
    EXEC = 0b001     # 1

    user_perms = READ | WRITE  # Grant Read and Write (0b110 = 6)
    print("=== 1. Bitwise Permission Flags ===")
    print(f"User Permissions Mask : {bin(user_perms)} ({user_perms})")
    print(f"Has READ permission?  : {bool(user_perms & READ)}")
    print(f"Has EXEC permission?  : {bool(user_perms & EXEC)}")

    # Toggle WRITE permission using XOR (^)
    user_perms ^= WRITE
    print(f"After toggling WRITE  : Has WRITE = {bool(user_perms & WRITE)}")

    # 2. Identity (`is`) vs Equality (`==`)
    print("\n=== 2. Identity (is) vs Equality (==) ===")
    list_a = [1, 2, 3]
    list_b = [1, 2, 3]
    print(f"list_a == list_b (same content) : {list_a == list_b}")
    print(f"list_a is list_b (same object)  : {list_a is list_b}")

    # 3. Membership (`in`) and Walrus Operator (`:=`)
    allowed_roles = {"admin", "instructor", "maintainer"}
    candidate_role = "instructor"
    print("\n=== 3. Membership & Walrus Operator (:=) ===")
    print(f"{candidate_role!r} in allowed_roles : {candidate_role in allowed_roles}")

    sample_text = "Python Operators Mastery"
    if (n := len(sample_text)) > 15:
        print(f"Sample text has length {n} (> 15 characters)")


if __name__ == "__main__":
    main()
