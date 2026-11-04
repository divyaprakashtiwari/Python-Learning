"""
Phase 3 - Topic 02: Parameters and Arguments
Example 02: Pass-by-Object-Reference (Immutable vs Mutable Arguments)

Demonstrates:
  - How Python passes object references (neither strict pass-by-value nor C++ reference)
  - Why reassigning a parameter inside a function NEVER modifies the caller's variable
  - Why mutating a mutable argument in-place DOES affect the caller's object
  - How to pass a defensive copy when mutation is unwanted
"""


def try_to_increment_number(score: int) -> int:
    """Reassign an immutable integer parameter inside the function."""
    print(f"    [Inside start] score={score}, id matches caller: True")
    score = score + 10  # Creates a brand-new int object; rebinds local `score`
    print(f"    [Inside after] score={score} (rebound to new int object)")
    return score


def mutate_cart_in_place(cart: list[str], new_item: str) -> None:
    """Mutate the caller's list directly via `.append()`."""
    cart.append(new_item)


def rebind_cart_locally(cart: list[str], new_item: str) -> list[str]:
    """Reassign the local parameter `cart` to a new list without mutating caller."""
    cart = cart + [new_item]  # `+` creates a brand-new list object
    return cart


def main() -> None:
    print("=== 1. Immutable Argument (`int`) - Caller Variable Unchanged ===")
    player_score = 50
    returned_score = try_to_increment_number(player_score)
    print(f"  Caller `player_score` after call : {player_score} (unchanged!)")
    print(f"  Returned value                   : {returned_score}")

    print("\n=== 2. Mutable Argument (`list`) - In-Place Mutation Affects Caller ===")
    shopping_cart = ["Laptop", "Mouse"]
    print(f"  Before `mutate_cart_in_place`    : {shopping_cart}")
    mutate_cart_in_place(shopping_cart, "Keyboard")
    print(f"  After  `mutate_cart_in_place`    : {shopping_cart} (mutated!)")

    print("\n=== 3. Mutable Argument (`list`) - Local Reassignment Does NOT Mutate ===")
    new_cart = rebind_cart_locally(shopping_cart, "Monitor")
    print(f"  Caller `shopping_cart`           : {shopping_cart} (unchanged!)")
    print(f"  Returned `new_cart`              : {new_cart}")

    print("\n=== 4. Defensive Copying at Call Site (`cart.copy()`) ===")
    mutate_cart_in_place(shopping_cart.copy(), "Headphones")
    print(f"  Caller `shopping_cart` after copy: {shopping_cart} (protected!)")


if __name__ == "__main__":
    main()
