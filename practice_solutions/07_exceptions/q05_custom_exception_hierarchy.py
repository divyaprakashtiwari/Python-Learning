"""
Topic 07 - Exception Handling: Question 5
Problem: Domain-Specific Custom Exception Hierarchy with Error Metadata and Polymorphism.
"""

from typing import Any, Dict


# 1. Base Domain Exception
class PaymentGatewayError(Exception):
    """Base exception for all payment gateway domain errors."""

    def __init__(self, message: str, error_code: str, transaction_id: str):
        super().__init__(message)
        self.message: str = message
        self.error_code: str = error_code
        self.transaction_id: str = transaction_id

    def __str__(self) -> str:
        return f"[{self.error_code}] Tx '{self.transaction_id}': {self.message}"


# 2. Specialized Subclasses with Domain Metadata
class InsufficientFundsError(PaymentGatewayError):
    """Raised when account balance is lower than the attempted charge amount."""

    def __init__(self, transaction_id: str, available_balance: float, attempted_amount: float):
        self.available_balance: float = available_balance
        self.attempted_amount: float = attempted_amount
        self.shortfall: float = round(attempted_amount - available_balance, 2)
        super().__init__(
            message=f"Insufficient funds: Shortfall of ${self.shortfall:.2f}",
            error_code="ERR_INSUFFICIENT_FUNDS",
            transaction_id=transaction_id
        )


class CardExpiredError(PaymentGatewayError):
    """Raised when payment card has passed its expiration date."""

    def __init__(self, transaction_id: str, card_last4: str, expiry_date: str):
        self.card_last4: str = card_last4
        self.expiry_date: str = expiry_date
        super().__init__(
            message=f"Card ending in {card_last4} expired on {expiry_date}",
            error_code="ERR_CARD_EXPIRED",
            transaction_id=transaction_id
        )


class FraudRiskBlockError(PaymentGatewayError):
    """Raised when machine learning fraud detection flags anomalous transactions."""

    def __init__(self, transaction_id: str, risk_score: float):
        self.risk_score: float = risk_score
        super().__init__(
            message=f"Transaction blocked due to elevated fraud score ({risk_score:.2f} > 0.85)",
            error_code="ERR_FRAUD_TRIGGERED",
            transaction_id=transaction_id
        )


# 3. Settlement Engine
def process_charge(tx_id: str, card: Dict[str, Any], balance: float, charge_amount: float) -> Dict[str, Any]:
    """Processes financial charge enforcing fraud checks, expiry, and balance verification."""
    if card.get("risk_score", 0.0) > 0.85:
        raise FraudRiskBlockError(tx_id, card["risk_score"])

    if card.get("is_expired", False):
        raise CardExpiredError(tx_id, card["last4"], card["expiry"])

    if balance < charge_amount:
        raise InsufficientFundsError(tx_id, balance, charge_amount)

    return {
        "tx_id": tx_id,
        "status": "APPROVED",
        "new_balance": round(balance - charge_amount, 2)
    }


# Verification & Polymorphic Catching
card_ok = {"last4": "4242", "expiry": "12/28", "is_expired": False, "risk_score": 0.12}
card_exp = {"last4": "1111", "expiry": "01/22", "is_expired": True, "risk_score": 0.05}
card_fraud = {"last4": "9999", "expiry": "05/27", "is_expired": False, "risk_score": 0.94}

# Test 1: Low balance (catching specific subclass with shortfall metadata)
try:
    process_charge("TX-1001", card_ok, balance=50.0, charge_amount=120.0)
except InsufficientFundsError as err:
    print("Caught Specific:", err)
    print("Actionable Metadata: Shortfall =", err.shortfall)

# Test 2: Expired card caught via generic base exception
try:
    process_charge("TX-1002", card_exp, balance=500.0, charge_amount=20.0)
except PaymentGatewayError as err:
    print("Caught via Base:", err.error_code, "|", err)

# Test 3: Fraud block caught polymorphically
try:
    process_charge("TX-1003", card_fraud, balance=1000.0, charge_amount=50.0)
except PaymentGatewayError as err:
    print("Caught via Base:", err.error_code, "|", err)
