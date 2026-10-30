"""
Question 1: BankAccount Domain Model & Automated unittest Suite
Topic: Testing, Debugging, and Profiling

Key Concepts Tested:
- Domain model with read-only properties, invariant validation, and custom exceptions
- unittest.TestCase assertion methods (assertEqual, assertAlmostEqual, assertRaises)
- Programmatic test execution using unittest.TestLoader and unittest.TextTestRunner
- Inspecting TestResult telemetry (testsRun, failures, errors, wasSuccessful)
"""

import unittest
import sys
from typing import Optional


class InsufficientFundsError(Exception):
    """Raised when withdrawal exceeds available balance."""
    pass


class BankAccount:
    """
    Domain entity representing a bank account with balance tracking and transaction rules.
    """

    def __init__(self, account_holder: str, initial_balance: float = 0.0) -> None:
        if initial_balance < 0:
            raise ValueError(f"Initial balance cannot be negative, got: {initial_balance}")
        self._account_holder = account_holder
        self._balance = float(initial_balance)

    @property
    def account_holder(self) -> str:
        return self._account_holder

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError(f"Deposit amount must be strictly positive, got: {amount}")
        self._balance += amount
        return self._balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError(f"Withdrawal amount must be strictly positive, got: {amount}")
        if amount > self._balance:
            raise InsufficientFundsError(
                f"Cannot withdraw {amount:.2f}; available balance is {self._balance:.2f}"
            )
        self._balance -= amount
        return self._balance


class TestBankAccount(unittest.TestCase):
    """
    Automated unit test suite verifying BankAccount invariants and operations.
    """

    def setUp(self) -> None:
        self.account = BankAccount(account_holder="Alice Smith", initial_balance=100.0)

    def test_initial_balance_valid(self) -> None:
        self.assertEqual(self.account.account_holder, "Alice Smith")
        self.assertAlmostEqual(self.account.balance, 100.0, places=2)

    def test_initial_balance_negative(self) -> None:
        with self.assertRaises(ValueError):
            BankAccount(account_holder="Bob", initial_balance=-50.0)

    def test_deposit_success(self) -> None:
        new_balance = self.account.deposit(50.25)
        self.assertAlmostEqual(new_balance, 150.25, places=2)
        self.assertAlmostEqual(self.account.balance, 150.25, places=2)

    def test_deposit_invalid_amount(self) -> None:
        with self.assertRaises(ValueError):
            self.account.deposit(0.0)
        with self.assertRaises(ValueError):
            self.account.deposit(-10.0)

    def test_withdraw_success(self) -> None:
        new_balance = self.account.withdraw(40.50)
        self.assertAlmostEqual(new_balance, 59.50, places=2)
        self.assertAlmostEqual(self.account.balance, 59.50, places=2)

    def test_withdraw_insufficient_funds(self) -> None:
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(200.0)


if __name__ == "__main__":
    print("=== Running BankAccount unittest Suite Programmatically ===")
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestBankAccount)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n=== Test Suite Results Summary ===")
    print(f"Tests Run: {result.testsRun}")
    print(f"All Tests Passed: {result.wasSuccessful()}")
    print(f"Failures Count: {len(result.failures)}")
    print(f"Errors Count: {len(result.errors)}")
    print(f"Execution Status: {'SUCCESS' if result.wasSuccessful() else 'FAILURE'}")
