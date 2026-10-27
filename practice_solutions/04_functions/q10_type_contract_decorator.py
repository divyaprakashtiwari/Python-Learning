"""
Topic 04 - Functions: Question 10
Problem: Runtime Type-Contract Decorator via Signature and Annotation Introspection.
"""

import functools
import inspect
from typing import Any, Callable, Dict


def enforce_contracts(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that enforces argument and return value type annotations at runtime."""
    sig = inspect.signature(func)

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        for param_name, value in bound.arguments.items():
            param = sig.parameters.get(param_name)
            if param and param.annotation is not inspect.Parameter.empty:
                expected_type = param.annotation
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Parameter '{param_name}' expected type {expected_type.__name__}, got {type(value).__name__}"
                    )

        result = func(*args, **kwargs)

        if sig.return_annotation is not inspect.Signature.empty:
            if not isinstance(result, sig.return_annotation):
                raise TypeError(
                    f"Return value expected type {sig.return_annotation.__name__}, got {type(result).__name__}"
                )

        return result

    return wrapper


@enforce_contracts
def process_transaction(
    user_id: str,
    amount: float,
    currency: str = "USD",
    notify_user: bool = True
) -> dict:
    """Processes a financial transaction under runtime contract validation.

    Args:
        user_id (str): The unique customer identifier.
        amount (float): The transaction monetary value.
        currency (str, optional): ISO-4217 currency code. Defaults to "USD".
        notify_user (bool, optional): Whether to issue push alert. Defaults to True.

    Returns:
        dict: Processed transaction confirmation details.

    Raises:
        TypeError: If parameter or return types breach annotated contracts.
    """
    _ = notify_user
    return {
        "transaction_id": "TXN-98471-OK",
        "user_id": user_id,
        "amount": amount,
        "currency": currency,
        "status": "COMPLETED"
    }


# 1. Valid Call
valid_res = process_transaction("usr_8821", 149.50, currency="EUR", notify_user=False)
print("Valid Transaction Processed:")
print(valid_res)

# 2. Type Violation 1: invalid user_id (int instead of str)
print("\nType Violation 1 (user_id):")
try:
    process_transaction(12345, 149.50)  # type: ignore
except TypeError as err:
    print(f'Caught Expected Error: TypeError("{err}")')

# 3. Type Violation 2: invalid amount (str instead of float)
print("\nType Violation 2 (amount):")
try:
    process_transaction("usr_8821", "one hundred")  # type: ignore
except TypeError as err:
    print(f'Caught Expected Error: TypeError("{err}")')

# 4. Function Introspection
print("\nFunction Introspection:")
print(f"Name: '{process_transaction.__name__}'")
print(f"Annotations: {process_transaction.__annotations__}")
