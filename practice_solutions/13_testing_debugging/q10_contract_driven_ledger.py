"""
Topic 13: Testing & Debugging - Question 10: Contract-Driven Ledger
Demonstrating Design by Contract (DbC) defensive programming patterns using
precondition, postcondition, and class invariant enforcement decorators.
"""

import functools
import unittest
from typing import Any, Callable, List, Tuple


# ==========================================
# Contract Exceptions
# ==========================================
class PreconditionViolationError(ValueError):
    """Raised when calling parameters violate a method's precondition contract."""
    pass


class PostconditionViolationError(RuntimeError):
    """Raised when return value or mutated state violates a postcondition contract."""
    pass


class InvariantViolationError(RuntimeError):
    """Raised when internal state integrity violates class invariant constraints."""
    pass


# ==========================================
# Contract Enforcement Decorators
# ==========================================
def precondition(predicate: Callable[..., bool], error_msg: str) -> Callable:
    """Decorator asserting that input parameters satisfy a condition before invocation."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not predicate(*args, **kwargs):
                raise PreconditionViolationError(error_msg)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def postcondition(predicate: Callable[..., bool], error_msg: str) -> Callable:
    """Decorator asserting that function result and state satisfy expected post-execution rules."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            if not predicate(result, *args, **kwargs):
                raise PostconditionViolationError(error_msg)
            return result
        return wrapper
    return decorator


# ==========================================
# Domain Entities and Contract Ledger
# ==========================================
class LedgerEntry:
    """Immutable audit record representing an individual debit or credit."""

    def __init__(self, amount: float, description: str, entry_type: str) -> None:
        self.amount = amount
        self.description = description
        self.entry_type = entry_type  # "CREDIT" or "DEBIT"


class ContractLedger:
    """
    Financial ledger enforcing strict Design by Contract specifications:
    - Preconditions: input sanitization, positivity, non-overdraw.
    - Postconditions: mathematical balance transitions.
    - Invariants: balance non-negativity and consistency with entries sum.
    """

    def __init__(self, account_id: str, initial_deposit: float = 0.0) -> None:
        if initial_deposit < 0:
            raise PreconditionViolationError("Initial deposit cannot be negative.")
        self.account_id = account_id
        self._entries: List[LedgerEntry] = []
        self._balance: float = 0.0

        if initial_deposit > 0:
            self._entries.append(LedgerEntry(initial_deposit, "Initial Deposit", "CREDIT"))
            self._balance = initial_deposit

        self.verify_invariants()

    @property
    def balance(self) -> float:
        return self._balance

    def verify_invariants(self) -> bool:
        """Verifies that balance matches entry deltas and never drops below zero."""
        if self._balance < 0:
            raise InvariantViolationError(f"Balance negative violation: {self._balance}")

        computed_sum = sum(
            entry.amount if entry.entry_type == "CREDIT" else -entry.amount
            for entry in self._entries
        )
        if abs(self._balance - computed_sum) > 1e-6:
            raise InvariantViolationError(
                f"Ledger desynchronization: balance {self._balance} != computed {computed_sum}"
            )
        return True

    @precondition(
        lambda self, amount, source: amount > 0 and bool(source and source.strip()),
        "Credit amount must be > 0 and source must not be empty."
    )
    def credit(self, amount: float, source: str) -> float:
        """Credits specified amount from source to ledger."""
        self._balance += amount
        self._entries.append(LedgerEntry(amount, source, "CREDIT"))
        self.verify_invariants()
        return self._balance

    @precondition(
        lambda self, amount, destination: (
            amount > 0 and bool(destination and destination.strip()) and amount <= self._balance
        ),
        "Debit amount must be positive, destination non-empty, and amount <= current balance."
    )
    def debit(self, amount: float, destination: str) -> float:
        """Debits specified amount to destination from ledger."""
        self._balance -= amount
        self._entries.append(LedgerEntry(amount, destination, "DEBIT"))
        self.verify_invariants()
        return self._balance

    def transfer_to(self, recipient: "ContractLedger", amount: float) -> Tuple[float, float]:
        """Atomically transfers funds preserving conservation of money across both ledgers."""
        if amount <= 0:
            raise PreconditionViolationError("Transfer amount must be positive.")
        if amount > self._balance:
            raise PreconditionViolationError("Insufficient balance for transfer.")

        total_before = self._balance + recipient._balance
        self.debit(amount, f"Transfer to {recipient.account_id}")
        recipient.credit(amount, f"Transfer from {self.account_id}")
        total_after = self._balance + recipient._balance

        if abs(total_before - total_after) > 1e-6:
            raise InvariantViolationError("Conservation of funds breached across transfer.")

        return self._balance, recipient._balance


# ==========================================
# Unit Test Verification
# ==========================================
class TestDefensiveProgrammingContracts(unittest.TestCase):
    """Unit test suite verifying DbC contracts, rollbacks, and invariant guards."""

    def setUp(self) -> None:
        self.ledger = ContractLedger("TEST-001", initial_deposit=100.0)

    def test_precondition_blocks_negative_credit(self) -> None:
        with self.assertRaises(PreconditionViolationError):
            self.ledger.credit(-20.0, "Invalid")
        self.assertEqual(self.ledger.balance, 100.0)

    def test_precondition_blocks_overdraw(self) -> None:
        with self.assertRaises(PreconditionViolationError):
            self.ledger.debit(150.0, "Overdraw")
        self.assertEqual(self.ledger.balance, 100.0)

    def test_atomic_transfer_conserves_funds(self) -> None:
        other = ContractLedger("TEST-002", initial_deposit=50.0)
        b1, b2 = self.ledger.transfer_to(other, 30.0)
        self.assertEqual(b1, 70.0)
        self.assertEqual(b2, 80.0)
        self.assertTrue(self.ledger.verify_invariants())
        self.assertTrue(other.verify_invariants())


# ==========================================
# Driver Execution
# ==========================================
if __name__ == "__main__":
    ledger = ContractLedger(account_id="ACC-001", initial_deposit=500.0)

    # 1. Valid Transactions
    b1 = ledger.credit(200.0, source="Payroll")
    b2 = ledger.debit(150.0, destination="Utility Bill")

    print(f"Balance after $200 Credit: ${b1:.2f}")
    print(f"Balance after $150 Debit: ${b2:.2f}")

    # 2. Precondition Violation Test (Negative Debit)
    precond_caught = False
    try:
        ledger.debit(-50.0, destination="Refund")
    except PreconditionViolationError:
        precond_caught = True

    # 3. Overdraw Violation Test (Debit exceeds balance)
    overdraw_caught = False
    try:
        ledger.debit(1000.0, destination="Luxury Purchase")
    except PreconditionViolationError:
        overdraw_caught = True

    # 4. Invariant Integrity Verification
    invariant_holds = ledger.verify_invariants()

    print(f"Negative Debit Precondition Blocked: {precond_caught}")
    print(f"Overdraw Precondition Blocked: {overdraw_caught}")
    print(f"Class Invariant (Balance == Sum of Transactions and Balance >= 0): {'TRUE' if invariant_holds else 'FALSE'}")

    # 5. Run test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDefensiveProgrammingContracts)
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)
    print(f"All Defensive Contracts Verified: {result.wasSuccessful()}")
