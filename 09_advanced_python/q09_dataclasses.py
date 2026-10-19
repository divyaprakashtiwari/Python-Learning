"""
Topic: Advanced Python - Dataclasses (dataclasses Module)
--------------------------------------------------------
Questions Covered:
1. Basic @dataclass Generation: Auto-generated __init__, __repr__, and __eq__ semantics.
2. Field Customization: Using field() with default_factory, repr=False, and compare=False.
3. Immutability & Hashing with frozen=True: Preventing mutations and enabling hashability.
4. Ordering & Rich Comparisons: order=True generating __lt__, __le__, __gt__, and __ge__.
5. Post-Initialization with __post_init__: Invariant validation and derived field computations.
6. Init-Only Variables with InitVar: Accepting parameters in __init__ without storing as fields.
7. Dataclass Inheritance: Field resolution order and subclassing behavior.
8. Conversion & Reflection Utilities: asdict, astuple, replace, and fields() metadata inspection.
9. High-Performance Memory Optimization with slots=True: Preventing __dict__ allocation.
10. Architectural System: Domain-Driven Design (DDD) Value Objects, Entities, and Aggregate Root.
"""

import time
from dataclasses import (
    dataclass,
    field,
    asdict,
    astuple,
    replace,
    fields,
    FrozenInstanceError,
    InitVar,
)
from typing import List, Dict, Optional, Any


# ==============================================================================
# Question 1: Basic @dataclass Generation
# ==============================================================================
@dataclass
class Point2D:
    x: float
    y: float


def test_q1_basic_dataclass():
    p1 = Point2D(3.0, 4.0)
    p2 = Point2D(3.0, 4.0)
    p3 = Point2D(5.0, 1.0)

    # 1. Structural equality __eq__
    assert p1 == p2
    assert p1 != p3

    # 2. String representation __repr__
    assert repr(p1) == "Point2D(x=3.0, y=4.0)"

    # 3. Direct attribute access
    assert p1.x == 3.0 and p1.y == 4.0
    print("=== Q1: Basic @dataclass Generation Verified ===")


# ==============================================================================
# Question 2: Field Customization (default_factory, repr, compare)
# ==============================================================================
@dataclass
class UserSession:
    user_id: str
    auth_token: str = field(repr=False, compare=False)  # Hidden from __repr__ and __eq__
    roles: List[str] = field(default_factory=list)  # Independent list per instance
    last_active: float = field(default=0.0, compare=False)  # Excluded from __eq__


def test_q2_field_customization():
    s1 = UserSession("u100", "secret_token_123", ["admin"], last_active=100.0)
    s2 = UserSession("u100", "secret_token_999", ["admin"], last_active=999.0)

    # 1. repr=False hides auth_token
    rep = repr(s1)
    assert "u100" in rep
    assert "secret_token_123" not in rep

    # 2. compare=False ignores last_active and compares only user_id and roles
    assert s1 == s2

    # 3. default_factory guarantees mutable isolation
    s3 = UserSession("u200", "tok")
    s4 = UserSession("u300", "tok")
    s3.roles.append("editor")
    assert "editor" not in s4.roles
    print("=== Q2: Field Customization (default_factory, repr, compare) Verified ===")


# ==============================================================================
# Question 3: Immutability and Hashing with frozen=True
# ==============================================================================
@dataclass(frozen=True)
class GeoCoordinate:
    latitude: float
    longitude: float


def test_q3_frozen_immutability():
    loc = GeoCoordinate(37.7749, -122.4194)

    # 1. Attempting mutation raises FrozenInstanceError
    try:
        loc.latitude = 40.7128  # type: ignore
        assert False, "Should raise FrozenInstanceError"
    except FrozenInstanceError:
        pass

    # 2. Frozen dataclasses generate __hash__ and can be used in sets and dict keys
    location_cache = {loc: "San Francisco"}
    assert location_cache[GeoCoordinate(37.7749, -122.4194)] == "San Francisco"
    assert len({loc, GeoCoordinate(37.7749, -122.4194)}) == 1
    print("=== Q3: Frozen Dataclass Immutability & Hashing Verified ===")


# ==============================================================================
# Question 4: Ordering and Rich Comparisons with order=True
# ==============================================================================
@dataclass(order=True)
class TaskPriority:
    # Priority is compared first in generated tuple comparison
    priority_level: int
    task_name: str = field(compare=False)  # Only priority_level determines order
    created_timestamp: float = field(compare=False, default=0.0)


def test_q4_ordering():
    t_high = TaskPriority(1, "Critical Security Patch")
    t_med = TaskPriority(5, "Refactor Logging")
    t_low = TaskPriority(10, "Update Readme")

    assert t_high < t_med < t_low
    unsorted = [t_low, t_high, t_med]
    sorted_tasks = sorted(unsorted)
    assert [t.priority_level for t in sorted_tasks] == [1, 5, 10]
    print("=== Q4: Dataclass Ordering and Rich Comparisons Verified ===")


# ==============================================================================
# Question 5: Post-Initialization Processing (__post_init__)
# ==============================================================================
@dataclass
class ProductItem:
    sku: str
    unit_price: float
    quantity: int
    discount_pct: float = 0.0
    # Derived total field computed in __post_init__
    total_price: float = field(init=False)

    def __post_init__(self):
        if self.unit_price < 0 or self.quantity < 0:
            raise ValueError("Price and quantity must be non-negative")
        self.sku = self.sku.strip().upper()
        discount_multiplier = 1.0 - (self.discount_pct / 100.0)
        self.total_price = round(self.unit_price * self.quantity * discount_multiplier, 2)


def test_q5_post_init():
    item = ProductItem("  prod-abc-123  ", unit_price=50.0, quantity=4, discount_pct=10.0)
    assert item.sku == "PROD-ABC-123"
    assert item.total_price == 180.0  # 50 * 4 * 0.9

    try:
        ProductItem("INVALID", unit_price=-10.0, quantity=1)
        assert False, "Should raise ValueError on negative price"
    except ValueError as e:
        assert "non-negative" in str(e)
    print("=== Q5: Post-Initialization (__post_init__) Verified ===")


# ==============================================================================
# Question 6: Init-Only Variables with InitVar
# ==============================================================================
@dataclass
class EncryptedSecret:
    raw_payload: str = field(init=False)
    cipher_key: InitVar[int]  # Parameter passed to __init__ and __post_init__, but not saved
    plain_text: InitVar[str]

    def __post_init__(self, cipher_key: int, plain_text: str):
        # XOR cipher encryption simulation
        self.raw_payload = "".join(chr(ord(c) ^ cipher_key) for c in plain_text)


def test_q6_initvar():
    secret = EncryptedSecret(cipher_key=42, plain_text="hello")
    # cipher_key and plain_text are not attributes on secret
    assert hasattr(secret, "raw_payload")
    assert not hasattr(secret, "cipher_key")
    assert not hasattr(secret, "plain_text")

    # Decrypt to verify
    decrypted = "".join(chr(ord(c) ^ 42) for c in secret.raw_payload)
    assert decrypted == "hello"
    print("=== Q6: Init-Only Variables (InitVar) Verified ===")


# ==============================================================================
# Question 7: Dataclass Inheritance
# ==============================================================================
@dataclass
class BaseEntity:
    entity_id: str
    created_at: float = field(default_factory=time.time)


@dataclass
class OrganizationUser(BaseEntity):
    email: str = ""
    department: str = "General"


def test_q7_inheritance():
    user = OrganizationUser(entity_id="USR-404", email="dev@company.com", department="DevOps")
    assert user.entity_id == "USR-404"
    assert user.email == "dev@company.com"
    assert user.department == "DevOps"
    assert isinstance(user, BaseEntity)
    assert user.created_at > 0.0
    print("=== Q7: Dataclass Inheritance Verified ===")


# ==============================================================================
# Question 8: Conversion & Reflection Utilities (asdict, astuple, replace)
# ==============================================================================
@dataclass
class ServerSpec:
    hostname: str
    ip: str
    cores: int
    memory_gb: int


def test_q8_reflection_utilities():
    spec = ServerSpec("web-prod-1", "10.0.1.25", 8, 32)

    # 1. asdict
    d = asdict(spec)
    assert d == {"hostname": "web-prod-1", "ip": "10.0.1.25", "cores": 8, "memory_gb": 32}

    # 2. astuple
    t = astuple(spec)
    assert t == ("web-prod-1", "10.0.1.25", 8, 32)

    # 3. replace (shallow copy with overrides)
    upgraded_spec = replace(spec, cores=16, memory_gb=64)
    assert upgraded_spec.hostname == "web-prod-1"
    assert upgraded_spec.cores == 16
    assert spec.cores == 8  # original untouched

    # 4. fields() reflection
    field_names = [f.name for f in fields(ServerSpec)]
    assert field_names == ["hostname", "ip", "cores", "memory_gb"]
    print("=== Q8: Dataclass Reflection & Conversion Utilities Verified ===")


# ==============================================================================
# Question 9: High-Performance Dataclasses with slots=True
# ==============================================================================
@dataclass(slots=True)
class FastPacket:
    packet_id: int
    payload_hash: str
    timestamp: float


def test_q9_slots_dataclass():
    pkt = FastPacket(1001, "abc123hash", 1700000000.0)
    assert pkt.packet_id == 1001

    # slots=True eliminates __dict__ on instances, optimizing memory
    assert not hasattr(pkt, "__dict__")

    # Dynamic attribute injection is disallowed
    try:
        pkt.arbitrary_extra_attr = "invalid"  # type: ignore
        assert False, "Should raise AttributeError on slotted dataclass"
    except AttributeError:
        pass
    print("=== Q9: High-Performance Dataclasses with slots=True Verified ===")


# ==============================================================================
# Question 10: Architectural System: DDD Value Objects, Entities, and Aggregate Root
# ==============================================================================
@dataclass(frozen=True)
class Money:
    """DDD Value Object: immutable, compared strictly by value."""
    amount: float
    currency: str = "USD"

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Currency mismatch: {self.currency} vs {other.currency}")
        return Money(round(self.amount + other.amount, 2), self.currency)


@dataclass
class OrderLineItem:
    """DDD Entity: compared strictly by line_id."""
    line_id: str
    product_name: str = field(compare=False)
    price: Money = field(compare=False)
    quantity: int = field(compare=False)


@dataclass(frozen=True)
class OrderPlacedEvent:
    """DDD Domain Event: immutable snapshot."""
    order_id: str
    total_amount: float
    currency: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class OrderAggregateRoot:
    """
    DDD Aggregate Root: Coordinates line items, enforces invariants,
    and publishes domain events upon state transition.
    """
    order_id: str
    customer_id: str
    items: List[OrderLineItem] = field(default_factory=list)
    domain_events: List[Any] = field(default_factory=list)
    status: str = "PENDING"

    def add_item(self, line_id: str, product: str, price: Money, qty: int) -> None:
        if self.status != "PENDING":
            raise RuntimeError("Cannot modify a finalized order")
        self.items.append(OrderLineItem(line_id, product, price, qty))

    def calculate_total(self) -> Money:
        total = Money(0.0, "USD")
        for item in self.items:
            item_total = Money(round(item.price.amount * item.quantity, 2), item.price.currency)
            total = total.add(item_total)
        return total

    def place_order(self) -> None:
        if not self.items:
            raise ValueError("Order must contain at least one item")
        total = self.calculate_total()
        self.status = "PLACED"
        self.domain_events.append(
            OrderPlacedEvent(
                order_id=self.order_id,
                total_amount=total.amount,
                currency=total.currency,
            )
        )


def test_q10_ddd_aggregate_root():
    order = OrderAggregateRoot("ORD-2026", "CUST-901")

    # Add items
    order.add_item("L1", "Mechanical Keyboard", Money(120.50), 1)
    order.add_item("L2", "USB-C Cable", Money(15.00), 2)

    total = order.calculate_total()
    assert total == Money(150.50, "USD")

    # Finalize order
    order.place_order()
    assert order.status == "PLACED"
    assert len(order.domain_events) == 1

    event = order.domain_events[0]
    assert isinstance(event, OrderPlacedEvent)
    assert event.order_id == "ORD-2026"
    assert event.total_amount == 150.50

    # Modifications after finalization are rejected
    try:
        order.add_item("L3", "Mousepad", Money(20.00), 1)
        assert False, "Should raise RuntimeError"
    except RuntimeError as err:
        assert "finalized order" in str(err)
    print("=== Q10: Architectural DDD Entities, Value Objects, and Aggregate Root Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_basic_dataclass()
    test_q2_field_customization()
    test_q3_frozen_immutability()
    test_q4_ordering()
    test_q5_post_init()
    test_q6_initvar()
    test_q7_inheritance()
    test_q8_reflection_utilities()
    test_q9_slots_dataclass()
    test_q10_ddd_aggregate_root()
    print("\nAll 10 dataclass practice questions passed successfully!")
