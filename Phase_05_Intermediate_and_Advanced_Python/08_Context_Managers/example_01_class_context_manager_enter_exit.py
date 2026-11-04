"""
Phase 5 - Topic 08: Context Managers
Example 01: Class-Based Context Manager (`__enter__` and `__exit__`) — Database Transaction Simulator

Demonstrates:
  - Implementing the Context Manager protocol (`__enter__` and `__exit__`) on a custom class
  - Automatic `COMMIT` when the `with` block exits cleanly (`exc_type is None`)
  - Automatic `ROLLBACK` when an exception occurs inside the `with` block (`exc_type is not None`)
"""

from types import TracebackType


class TransactionalList:
    """Wrap a list in an atomic transaction: commit on clean exit, rollback on exception."""

    def __init__(self, target: list[str]) -> None:
        self._target = target
        self._working_copy: list[str] = []

    def __enter__(self) -> list[str]:
        self._working_copy = list(self._target)
        print(f"  [__enter__] Transaction started (snapshot={self._working_copy})")
        return self._working_copy

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        if exc_type is None:
            self._target[:] = self._working_copy
            print(f"  [__exit__]  COMMIT succeeded -> {self._target}")
        else:
            print(f"  [__exit__]  ROLLBACK triggered due to {exc_type.__name__}: {exc_val}")
        # Returning False propagates any exception outward instead of swallowing it
        return False


def main() -> None:
    ledger = ["tx-100"]

    print("=== 1. Successful Transaction (`exc_type is None` -> COMMIT) ===")
    with TransactionalList(ledger) as working:
        working.append("tx-101")
        working.append("tx-102")
    print(f"  Ledger after commit: {ledger}")

    print("\n=== 2. Failed Transaction (`RuntimeError` -> ROLLBACK) ===")
    try:
        with TransactionalList(ledger) as working:
            working.append("tx-corrupted")
            raise RuntimeError("Payment gateway rejected batch")
    except RuntimeError:
        print(f"  Ledger after rollback (unchanged!): {ledger}")


if __name__ == "__main__":
    main()
