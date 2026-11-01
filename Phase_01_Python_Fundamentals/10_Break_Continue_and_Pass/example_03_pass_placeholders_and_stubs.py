"""
Topic 10: Break, Continue and Pass
Example 03: Using `pass` as a Syntactic Null Operation for Stubs & Classes

Demonstrates why `pass` exists in Python: indented blocks cannot be empty,
so `pass` acts as a no-op placeholder in class hierarchies, function stubs,
and ignored branches.
"""


class PaymentGatewayError(Exception):
    """Custom domain exception that needs no extra methods beyond Exception."""
    pass


class NotificationService:
    """Skeleton service interface designed before concrete implementation."""

    def send_email(self, recipient: str, subject: str) -> None:
        # TODO: Integrate SMTP provider in Phase 5
        pass

    def send_sms(self, phone: str, message: str) -> None:
        pass


def main() -> None:
    print("=== 1. Instantiating Stub Class with `pass` ===")
    notifier = NotificationService()
    notifier.send_email("student@example.com", "Welcome to Python DSA")
    print("Stub method executed cleanly with no-op `pass` (returned None).")

    print("\n=== 2. Catching Custom Exception Defined with `pass` ===")
    try:
        raise PaymentGatewayError("Gateway timeout after 5000ms")
    except PaymentGatewayError as exc:
        print(f"Caught {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
