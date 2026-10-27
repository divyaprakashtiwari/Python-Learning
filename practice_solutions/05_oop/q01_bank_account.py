"""
Topic 05 - Object-Oriented Programming (OOP): Question 1
Problem: BankAccount class modeling account lifecycle, deposit, withdrawal, and error handling.
"""


class BankAccount:
    """Models a financial bank account with balance tracking and transaction guards."""

    _account_counter: int = 1000

    def __init__(self, account_holder: str, initial_balance: float = 0.0):
        if initial_balance < 0.0:
            raise ValueError("Initial balance cannot be negative")

        BankAccount._account_counter += 1
        self.account_number: str = f"ACC-{BankAccount._account_counter}"
        self.account_holder: str = account_holder
        self.balance: float = float(initial_balance)

    def deposit(self, amount: float) -> float:
        """Deposits funds into the account, returning updated balance."""
        if amount <= 0:
            raise ValueError("Deposit amount must be strictly positive")
        self.balance += amount
        return self.balance

    def withdraw(self, amount: float) -> float:
        """Withdraws funds from the account, raising ValueError if insufficient."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be strictly positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return self.balance

    def __str__(self) -> str:
        return f"BankAccount(Holder: {self.account_holder}, Account#: {self.account_number}, Balance: ${self.balance:.2f})"


# Verification & Simulation
account = BankAccount("Alice Smith", 500.0)
print(f"Account Created: {account}")

bal_dep = account.deposit(250.0)
print(f"After Deposit ($250.00): Balance = ${bal_dep:.2f}")

bal_with = account.withdraw(120.0)
print(f"After Withdrawal ($120.00): Balance = ${bal_with:.2f}")

# Overdraft attempt
print("Overdraft Attempt ($700.00):")
try:
    account.withdraw(700.0)
except ValueError as err:
    print(f'Caught Expected Error: ValueError("{err}")')
