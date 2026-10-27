"""
Topic 05 - Object-Oriented Programming (OOP): Question 10
Problem: Enterprise E-commerce Checkout with Composition, Dependency Injection, and Strategy Pattern.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


# 1. Strategy Interface and Concrete Strategies
class PaymentStrategy(ABC):
    """Abstract strategy contract for financial payment processing."""

    @abstractmethod
    def process_payment(self, amount: float) -> Dict[str, Any]:
        pass


class CreditCardPayment(PaymentStrategy):
    """Credit Card processor with 2.5% card processing fee."""

    def __init__(self, card_number: str, cvv: str):
        if not (isinstance(card_number, str) and len(card_number) == 16 and card_number.isdigit()):
            raise ValueError("Credit card must be 16 digits")
        if not (isinstance(cvv, str) and len(cvv) == 3 and cvv.isdigit()):
            raise ValueError("CVV must be 3 digits")
        self.card_number = card_number
        self.cvv = cvv

    def process_payment(self, amount: float) -> Dict[str, Any]:
        fee = round(amount * 0.025, 2)
        return {
            "method": "CREDIT_CARD",
            "base_amount": amount,
            "fee": fee,
            "total_charged": amount + fee,
            "status": "APPROVED"
        }


class CryptoPayment(PaymentStrategy):
    """Crypto payment processor with $4.50 flat gas fee."""

    def __init__(self, wallet_address: str):
        if not (isinstance(wallet_address, str) and wallet_address.startswith("0x") and len(wallet_address) == 42):
            raise ValueError("Invalid crypto wallet address")
        self.wallet_address = wallet_address

    def process_payment(self, amount: float) -> Dict[str, Any]:
        fee = 4.50
        return {
            "method": "CRYPTO",
            "base_amount": amount,
            "fee": fee,
            "total_charged": amount + fee,
            "status": "CONFIRMED"
        }


class PayPalPayment(PaymentStrategy):
    """PayPal payment processor with 3.0% variable + $0.30 fixed fee."""

    def __init__(self, email: str):
        if not (isinstance(email, str) and "@" in email and "." in email):
            raise ValueError("Invalid email address")
        self.email = email

    def process_payment(self, amount: float) -> Dict[str, Any]:
        fee = round(amount * 0.03 + 0.30, 2)
        return {
            "method": "PAYPAL",
            "base_amount": amount,
            "fee": fee,
            "total_charged": amount + fee,
            "status": "SETTLED"
        }


# 2. Composed Domain Components
class OrderItem:
    """Discrete purchase item inside an order."""

    def __init__(self, sku: str, title: str, unit_price: float, quantity: int):
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")
        if unit_price <= 0:
            raise ValueError("Unit price must be positive")
        self.sku = sku
        self.title = title
        self.unit_price = float(unit_price)
        self.quantity = int(quantity)

    @property
    def subtotal(self) -> float:
        return round(self.unit_price * self.quantity, 2)


# 3. Orchestrator Engine using Composition and Dependency Injection
class Order:
    """Orchestrates order items and processes checkout via injected payment strategy."""

    def __init__(self, order_id: str, customer_id: str, payment_strategy: Any):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items: List[OrderItem] = []
        self.is_paid: bool = False
        self.payment_strategy: Any = None
        self.set_payment_strategy(payment_strategy)

    def set_payment_strategy(self, new_strategy: Any) -> None:
        """Dynamically swaps the payment strategy at runtime with duck-typing validation."""
        if not callable(getattr(new_strategy, "process_payment", None)):
            raise TypeError("Strategy must implement callable process_payment()")
        self.payment_strategy = new_strategy

    def add_item(self, item: OrderItem) -> None:
        self.items.append(item)

    def calculate_subtotal(self) -> float:
        return round(sum(i.subtotal for i in self.items), 2)

    def checkout(self) -> Dict[str, Any]:
        """Finalizes order, executes payment strategy, and generates invoice receipt."""
        if self.is_paid:
            raise RuntimeError("Order is already paid and completed")
        if not self.items:
            raise ValueError("Cannot checkout empty order")

        subtotal = self.calculate_subtotal()
        receipt = self.payment_strategy.process_payment(subtotal)
        self.is_paid = True

        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "items": self.items,
            "subtotal": subtotal,
            "receipt": receipt,
            "status": "COMPLETED"
        }


# Verification & Execution
item1 = OrderItem("SKU-101", "Mechanical Keyboard", 120.0, 1)
item2 = OrderItem("SKU-202", "USB-C Cable", 15.0, 2)

order = Order("ORD-9001", "CUST-42", CreditCardPayment("4111222233334444", "123"))
order.add_item(item1)
order.add_item(item2)

# Dynamically swap strategy to Crypto
order.set_payment_strategy(CryptoPayment("0x5aAeb6053F3E94C9b9A09f33669435E7Ef1bEAed"))
invoice = order.checkout()

print(f"Order ID: {invoice['order_id']}")
print("Items Ordered:")
for itm in invoice["items"]:
    print(f"- {itm.title} (x{itm.quantity}): ${itm.subtotal:.2f}")

print(f"Order Subtotal: ${invoice['subtotal']:.2f}")
print(f"Payment Strategy: {invoice['receipt']['method']}")
print(f"Network Fee: ${invoice['receipt']['fee']:.2f}")
print(f"Total Billed: ${invoice['receipt']['total_charged']:.2f}")
print(f"Payment Status: {invoice['receipt']['status']}")
print(f"Order Checkout Status: {invoice['status']}")

# Validation Tests
print("\nValidation Tests:")
try:
    CreditCardPayment("1234", "123")
except ValueError as err:
    print(f'- Invalid Card Number ("1234"): ValueError("{err}")')

try:
    empty_order = Order("ORD-EMPTY", "CUST-00", PayPalPayment("test@example.com"))
    empty_order.checkout()
except ValueError as err:
    print(f'- Empty Order Checkout: ValueError("{err}")')

try:
    # Attempting to checkout order again
    order.checkout()
except RuntimeError as err:
    print(f'- Double Checkout Attempt: RuntimeError("{err}")')
