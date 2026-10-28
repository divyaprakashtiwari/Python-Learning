"""
Question 9: Immutable Orderable Equity Trade Order Model
Topic: Advanced Python

Key Concepts Tested:
- dataclasses (@dataclass, field, default_factory)
- Immutability enforcement (frozen=True) and FrozenInstanceError
- Automatic ordering comparison (order=True) via hidden sort_key field
- Field validation and mutating frozen instances during __post_init__ using object.__setattr__
- Serialization to dictionary via dataclasses.asdict()
"""

from dataclasses import dataclass, field, asdict, FrozenInstanceError
from typing import List


@dataclass(frozen=True, order=True)
class TradeOrder:
    """
    Immutable, orderable equity trade order.
    Orders are natively sorted by total trade value in descending order
    using an internal negative sort_key.
    """

    sort_key: float = field(init=False, repr=False)
    order_id: str
    ticker: str
    shares: int
    price_per_share: float
    execution_venue: str = "NASDAQ"
    metadata_tags: List[str] = field(default_factory=list, compare=False)

    def __post_init__(self) -> None:
        if self.shares <= 0:
            raise ValueError("Shares must be positive")
        if self.price_per_share <= 0.0:
            raise ValueError("Price must be positive")

        trade_value = self.shares * self.price_per_share
        # In frozen dataclasses, direct assignment fails; use object.__setattr__
        object.__setattr__(self, "sort_key", -trade_value)

    @property
    def total_value(self) -> float:
        return self.shares * self.price_per_share


if __name__ == "__main__":
    order1 = TradeOrder(order_id="ORD-01", ticker="AAPL", shares=100, price_per_share=150.0)  # $15,000
    order2 = TradeOrder(order_id="ORD-02", ticker="GOOG", shares=10, price_per_share=2800.0)   # $28,000
    order3 = TradeOrder(order_id="ORD-03", ticker="MSFT", shares=50, price_per_share=300.0)    # $15,000

    print("=== 1. Dataclass Representation ===")
    print(f"Order 1 Summary: {order1}")

    print("\n=== 2. Native Sorting via sort_key (Descending Trade Value) ===")
    order_book = [order1, order2, order3]
    sorted_orders = sorted(order_book)
    print("Sorted Order Book (Descending Trade Value):")
    for idx, order in enumerate(sorted_orders, 1):
        print(f"{idx}. {order.order_id} ({order.ticker}): Value = ${order.total_value:,.2f}")

    print("\n=== 3. Serialization to Dictionary ===")
    order1_dict = {k: v for k, v in asdict(order1).items() if k != "sort_key"}
    print(f"Serialized Dict Keys: {list(order1_dict.keys())}")
    print(f"Serialized Dict Data: {order1_dict}")

    print("\n=== 4. Immutability Violation Test ===")
    try:
        order1.shares = 200  # type: ignore[misc]
    except FrozenInstanceError as err:
        print(f"Caught Mutation Breach: {err}")

    print("\n=== 5. Invariant Validation Tests ===")
    try:
        TradeOrder(order_id="ORD-BAD", ticker="BAD", shares=-5, price_per_share=100.0)
    except ValueError as err:
        print(f"Caught negative shares invariant: {err}")

    try:
        TradeOrder(order_id="ORD-BAD", ticker="BAD", shares=10, price_per_share=-50.0)
    except ValueError as err:
        print(f"Caught negative price invariant: {err}")
