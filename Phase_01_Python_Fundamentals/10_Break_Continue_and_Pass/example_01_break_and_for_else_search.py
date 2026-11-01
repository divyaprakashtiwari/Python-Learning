"""
Topic 10: Break, Continue and Pass
Example 01: `break` for Early Termination and Python's `for ... else` Construct

Demonstrates how `break` exits a loop immediately when a target or divisor is found,
and how the `else` block on a loop runs ONLY if the loop did NOT hit `break`.
"""


def find_transaction(transactions: list[dict], target_id: str) -> None:
    print(f"Searching for Transaction ID {target_id!r}...")
    for index, txn in enumerate(transactions):
        if txn["id"] == target_id:
            print(f"  [FOUND at index {index}] Amount: Rs.{txn['amount']} | Status: {txn['status']}")
            break
    else:
        # Runs ONLY if the loop finishes all iterations without hitting `break`
        print(f"  [NOT FOUND] Transaction {target_id!r} does not exist.")


def is_prime_with_for_else(n: int) -> bool:
    """Check primality using a for...else loop and break."""
    if n < 2:
        return False
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            break
    else:
        return True
    return False


def main() -> None:
    ledger = [
        {"id": "TXN-101", "amount": 500, "status": "SUCCESS"},
        {"id": "TXN-102", "amount": 1200, "status": "PENDING"},
        {"id": "TXN-103", "amount": 850, "status": "SUCCESS"},
    ]
    print("=== 1. Early Exit with break and for...else ===")
    find_transaction(ledger, "TXN-102")
    find_transaction(ledger, "TXN-999")

    print("\n=== 2. Prime Number Verification using for...else ===")
    for candidate in [2, 15, 29, 49, 97]:
        print(f"  is_prime({candidate:>2}) -> {is_prime_with_for_else(candidate)}")


if __name__ == "__main__":
    main()
