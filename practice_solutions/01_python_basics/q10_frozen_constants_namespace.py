"""
Topic 01 - Python Basics & Variables
Practice Question 10 Solution: Frozen Constants Namespace & PEP 8 Naming

Problem Statement:
Implements a runtime-enforced immutable constants namespace following PEP 8:
1. Validator `validate_constant_name(identifier: str) -> bool`:
   - Only uppercase ASCII letters, digits, underscores.
   - Begins with uppercase letter.
   - No consecutive underscores ("__") and does not end with underscore.
2. `FrozenConstants`:
   - Validates all keys upon initialization; raises ValueError on violation.
   - Overrides __setattr__ and __delattr__ raising AttributeError.
   - Provides as_dict() returning read-only mapping.
"""

import re
from typing import Any


def validate_constant_name(identifier: str) -> bool:
    """Validates that identifier strictly follows SCREAMING_SNAKE_CASE.

    - Begins with uppercase letter [A-Z].
    - Followed by [A-Z0-9] or single underscores.
    - No trailing underscore or consecutive underscores.
    """
    if not isinstance(identifier, str):
        return False
    # Pattern: Starts with uppercase letter, followed by alphanumeric or single underscores, ends with alphanumeric
    # Single-letter constant (e.g. 'X') is also valid.
    pattern = r"^[A-Z](?:[A-Z0-9]*(?:_[A-Z0-9]+)*)?$"
    return bool(re.match(pattern, identifier))


class FrozenConstants:
    """An immutable container that enforces SCREAMING_SNAKE_CASE constants."""

    def __init__(self, **constants: Any) -> None:
        # Use object.__setattr__ to bypass frozen protection during initialization
        object.__setattr__(self, "_store", {})

        for name, value in constants.items():
            if not validate_constant_name(name):
                raise ValueError(
                    f"Identifier '{name}' violates SCREAMING_SNAKE_CASE convention"
                )
            self._store[name] = value

        # Mark initialization as finalized
        object.__setattr__(self, "_is_frozen", True)

    def __getattr__(self, name: str) -> Any:
        store = object.__getattribute__(self, "_store")
        if name in store:
            return store[name]
        raise AttributeError(f"Constant '{name}' does not exist.")

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_is_frozen", False):
            raise AttributeError(f"Cannot modify frozen constant '{name}'")
        super().__setattr__(name, value)

    def __delattr__(self, name: str) -> None:
        raise AttributeError(f"Cannot delete frozen constant '{name}'")

    def as_dict(self) -> dict[str, Any]:
        """Returns a copy of the constants dictionary."""
        return dict(object.__getattribute__(self, "_store"))

    def __repr__(self) -> str:
        items = ", ".join(f"{k}={v!r}" for k, v in self.as_dict().items())
        return f"FrozenConstants({items})"


def main() -> None:
    valid_config = {
        "API_BASE_URL": "https://api.production.internal/v1",
        "MAX_RETRY_COUNT": 5,
        "TIMEOUT_SECONDS": 30.0,
        "IS_PRODUCTION": True,
    }

    constants = FrozenConstants(**valid_config)

    print("Constants Initialized Successfully:")
    for k, v in constants.as_dict().items():
        print(f"- {k}: {v}")

    print("\nAttempting Reassignment (MAX_RETRY_COUNT = 10):")
    try:
        constants.MAX_RETRY_COUNT = 10
    except AttributeError as err:
        print(f"Caught Expected Error: AttributeError(\"{err}\")")

    print("\nAttempting Invalid Name ('timeout_Seconds'):")
    try:
        FrozenConstants(timeout_Seconds=15)
    except ValueError as err:
        print(f"Caught Expected Error: ValueError(\"{err}\")")


if __name__ == "__main__":
    main()
