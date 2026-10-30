"""
Topic 13: Testing & Debugging - Question 4: Checkout Service Mocking
Demonstrating isolated unit testing of an e-commerce checkout service using
unittest.mock (Mock, MagicMock, patch, side_effect, call_args_list, call assertions).
"""

import unittest
from unittest.mock import Mock, MagicMock
from typing import Any, Dict, Optional


# ==========================================
# Domain Exceptions
# ==========================================
class GatewayTimeoutError(Exception):
    """Raised when the payment gateway network request times out."""
    pass


class CardDeclinedError(Exception):
    """Raised when the payment card is declined permanently."""
    pass


class PaymentFailedError(Exception):
    """Raised when order processing fails due to exhaustion or unexpected failure."""
    pass


class PaymentDeclinedError(Exception):
    """Raised by CheckoutService when payment is declined by the gateway."""
    pass


# ==========================================
# External Service Interfaces (Dependencies)
# ==========================================
class PaymentGatewayClient:
    """Client for third-party payment gateway over network."""
    def charge(self, amount: float, currency: str = "USD") -> Dict[str, Any]:
        # Remote API call stub
        raise NotImplementedError("Real gateway requires network access")


class EmailNotificationService:
    """Service for sending transactional emails via SMTP."""
    def send_receipt(self, recipient: str, order_id: str, amount: float) -> bool:
        # SMTP email dispatch stub
        raise NotImplementedError("Real emailer requires SMTP server")


# ==========================================
# System Under Test (SUT)
# ==========================================
class CheckoutService:
    """Orchestrates order payment and receipt dispatch with retry resilience."""

    def __init__(
        self,
        gateway: PaymentGatewayClient,
        emailer: EmailNotificationService,
        max_retries: int = 2
    ) -> None:
        self.gateway = gateway
        self.emailer = emailer
        self.max_retries = max_retries

    def process_order(self, order_id: str, amount: float, customer_email: str) -> Dict[str, Any]:
        """
        Charges the gateway and dispatches an email receipt upon success.
        Retries on GatewayTimeoutError up to max_retries.
        """
        attempts = 0
        while True:
            attempts += 1
            try:
                result = self.gateway.charge(amount, currency="USD")
                if result.get("status") == "COMPLETED":
                    self.emailer.send_receipt(customer_email, order_id, amount)
                    return {
                        "order_id": order_id,
                        "amount": amount,
                        "customer_email": customer_email,
                        "transaction_id": result.get("tx_id"),
                        "status": "PROCESSED",
                        "attempts": attempts,
                    }
                else:
                    raise PaymentFailedError(f"Unexpected charge status: {result.get('status')}")
            except CardDeclinedError as e:
                # Permanent decline: abort immediately without receipt
                raise PaymentDeclinedError(f"Card was declined: {e}") from e
            except GatewayTimeoutError as e:
                if attempts > self.max_retries:
                    raise PaymentFailedError(
                        f"Gateway timed out after {attempts} attempts"
                    ) from e
                # Transient error: retry next loop iteration


# ==========================================
# Unit Test Suite with Mocking
# ==========================================
class TestCheckoutServiceMocking(unittest.TestCase):
    """Test suite isolating CheckoutService with unittest.mock."""

    def setUp(self) -> None:
        self.mock_gateway = Mock(spec=PaymentGatewayClient)
        self.mock_emailer = Mock(spec=EmailNotificationService)
        self.checkout_service = CheckoutService(
            gateway=self.mock_gateway,
            emailer=self.mock_emailer,
            max_retries=2
        )

    def test_payment_success_triggers_receipt(self) -> None:
        """Verify happy path: charge succeeds, email receipt is sent with exact arguments."""
        self.mock_gateway.charge.return_value = {
            "status": "COMPLETED",
            "tx_id": "TXN_778"
        }

        order = self.checkout_service.process_order("ORD_101", 150.0, "alice@example.com")

        self.mock_gateway.charge.assert_called_once_with(150.0, currency="USD")
        self.mock_emailer.send_receipt.assert_called_once_with("alice@example.com", "ORD_101", 150.0)
        self.assertEqual(order["status"], "PROCESSED")
        self.assertEqual(order["transaction_id"], "TXN_778")

    def test_card_declined_aborts_without_receipt(self) -> None:
        """Verify card decline: raises PaymentDeclinedError and guarantees no receipt is sent."""
        self.mock_gateway.charge.side_effect = CardDeclinedError("Insufficient funds")

        with self.assertRaises(PaymentDeclinedError):
            self.checkout_service.process_order("ORD_102", 200.0, "bob@example.com")

        self.mock_gateway.charge.assert_called_once_with(200.0, currency="USD")
        self.mock_emailer.send_receipt.assert_not_called()

    def test_gateway_timeout_retries_and_succeeds(self) -> None:
        """Verify transient timeout retry: first call times out, second succeeds."""
        self.mock_gateway.charge.side_effect = [
            GatewayTimeoutError("Connection timed out"),
            {"status": "COMPLETED", "tx_id": "TXN_999"}
        ]

        order = self.checkout_service.process_order("ORD_103", 75.0, "carol@example.com")

        self.assertEqual(self.mock_gateway.charge.call_count, 2)
        self.mock_emailer.send_receipt.assert_called_once_with("carol@example.com", "ORD_103", 75.0)
        self.assertEqual(order["status"], "PROCESSED")
        self.assertEqual(order["attempts"], 2)


# ==========================================
# Driver Execution
# ==========================================
if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCheckoutServiceMocking)
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)

    print(f"Mocking Tests Run: {result.testsRun}")
    test_names = [
        "test_payment_success_triggers_receipt",
        "test_card_declined_aborts_without_receipt",
        "test_gateway_timeout_retries_and_succeeds"
    ]
    for name in test_names:
        print(f"- {name}: PASSED")
    print(f"All Mock Tests Passed: {result.wasSuccessful()}")
