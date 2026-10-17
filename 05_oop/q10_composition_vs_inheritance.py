"""
Topic 05: Object-Oriented Programming (OOP)
Question 10: Composition vs Inheritance (Deep Dive)

Master software architecture principles: "Favor Composition Over Inheritance":
- The "HAS-A" (composition) vs "IS-A" (inheritance) paradigm comparison
- Automatic method delegation and forwarding via __getattr__
- Dependency Injection through component composition
- The Decorator design pattern via composition (wrapping interfaces)
- The Strategy design pattern: avoiding inheritance explosion with behavioral components
- The Composite design pattern: uniform tree structures (Leaf vs Composite)
- Refactoring brittle multi-level inheritance hierarchies into clean components
- The State pattern: delegating state-dependent behaviors
- Hybrid architecture: combining interface inheritance with internal component composition
- Production-grade E-Commerce Order Processing Engine with decoupled service components
"""

from typing import Any, Dict, List, Optional, Protocol


# ============================================================
# Q1: Composition ("HAS-A") vs Inheritance ("IS-A")
# ============================================================
# Question: Contrast modeling a `Car` using inheritance vs composition.
# Show that a Car "HAS-A" Engine and "HAS-A" Battery, rather than "IS-AN" Engine.

print("=== Q1: Composition ('HAS-A') vs Inheritance ('IS-A') ===")

# Components (Modular building blocks)
class GasolineEngine:
    def start(self) -> str:
        return "V8 engine roaring to life"

class ElectricMotor:
    def start(self) -> str:
        return "Electric motor humming silently"

# Composed Car: accepts any engine component
class Car:
    def __init__(self, model: str, engine: Any):
        self.model = model
        self.engine = engine  # Composition: Car HAS-AN Engine!

    def drive(self) -> str:
        engine_sound = self.engine.start()
        return f"{self.model} moving: {engine_sound}"

gas_car = Car("Mustang", GasolineEngine())
ev_car = Car("Model S", ElectricMotor())

print(f"  Gas car: {gas_car.drive()}")
print(f"  EV car:  {ev_car.drive()}")

assert "V8 engine" in gas_car.drive()
assert "Electric motor" in ev_car.drive()

# Explanation: Inheritance ("IS-A") binds classes tightly at compile time.
# Composition ("HAS-A") allows swapping components at runtime without class proliferation.


# ============================================================
# Q2: Automatic Method Delegation via __getattr__
# ============================================================
# Question: Implement a generic wrapper `Delegator` that automatically forwards any
# attribute or method call it does not handle to an underlying composed object.

print("\n=== Q2: Automatic Method Delegation via __getattr__ ===")

class LegacyFileWriter:
    def write_line(self, line: str) -> str:
        return f"WRITTEN: {line}"

    def flush(self) -> str:
        return "FLUSHED_TO_DISK"

class AuditedWriter:
    """Composes LegacyFileWriter, adds audit logging, and delegates missing calls."""
    def __init__(self, target_writer: Any):
        self._target = target_writer
        self.audit_log: List[str] = []

    def write_line(self, line: str) -> str:
        # Intercept and log
        self.audit_log.append(f"AUDIT: {line}")
        return self._target.write_line(line)

    def __getattr__(self, name: str) -> Any:
        # Delegate any unhandled method (e.g. .flush()) to _target!
        return getattr(self._target, name)

legacy = LegacyFileWriter()
audited = AuditedWriter(legacy)

res_write = audited.write_line("Transaction record #42")
res_flush = audited.flush()  # Handled transparently by __getattr__ delegation!

print(f"  Write call result: {res_write}")
print(f"  Flush call result: {res_flush} (Delegated!)")
print(f"  Audit log:         {audited.audit_log}")

assert res_write == "WRITTEN: Transaction record #42"
assert res_flush == "FLUSHED_TO_DISK"
assert len(audited.audit_log) == 1

# Explanation: `__getattr__` enables seamless delegation: an outer class can selectively
# override specific methods and transparently pass all other operations to the composed inner object.


# ============================================================
# Q3: Dependency Injection via Composition
# ============================================================
# Question: Build a `UserService` that receives its `Notifier` and `Database` dependencies
# via constructor injection. Demonstrate swapping with Mock components for isolated unit testing.

print("\n=== Q3: Dependency Injection via Composition ===")

class DatabaseProtocol(Protocol):
    def save_user(self, user: str) -> bool: ...

class NotifierProtocol(Protocol):
    def send_welcome(self, user: str) -> bool: ...

class UserService:
    def __init__(self, db: DatabaseProtocol, notifier: NotifierProtocol):
        # Dependencies injected via composition
        self._db = db
        self._notifier = notifier

    def register_user(self, user: str) -> Dict[str, Any]:
        db_ok = self._db.save_user(user)
        notif_ok = self._notifier.send_welcome(user)
        return {"user": user, "db_saved": db_ok, "notified": notif_ok}

# Mock dependencies for testing
class MockDatabase:
    def __init__(self): self.saved = []
    def save_user(self, user: str) -> bool:
        self.saved.append(user)
        return True

class MockNotifier:
    def __init__(self): self.sent = []
    def send_welcome(self, user: str) -> bool:
        self.sent.append(user)
        return True

mock_db = MockDatabase()
mock_notif = MockNotifier()
service = UserService(mock_db, mock_notif)

result = service.register_user("alice")
print(f"  Service registration: {result}")

assert result["db_saved"] is True
assert "alice" in mock_db.saved
assert "alice" in mock_notif.sent

# Explanation: Composing dependencies via constructor injection decouples business logic
# from infrastructure, making code modular, testable, and maintainable.


# ============================================================
# Q4: The Decorator Pattern (Wrapping Interfaces via Composition)
# ============================================================
# Question: Implement the structural Decorator pattern using composition:
# Wrap a `SimpleDataSource` with an `EncryptionDecorator` and a `CompressionDecorator`.

print("\n=== Q4: The Decorator Pattern via Composition ===")

class DataSource(Protocol):
    def write_data(self, data: str) -> str: ...
    def read_data(self) -> str: ...

class StringDataSource:
    def __init__(self):
        self._content = ""

    def write_data(self, data: str) -> str:
        self._content = data
        return self._content

    def read_data(self) -> str:
        return self._content

class EncryptionDecorator:
    """Wraps any DataSource, adding reversible XOR encryption."""
    def __init__(self, wrapped: DataSource):
        self._wrapped = wrapped

    def write_data(self, data: str) -> str:
        encrypted = "".join(chr(ord(c) ^ 0x55) for c in data)
        return self._wrapped.write_data(encrypted)

    def read_data(self) -> str:
        encrypted = self._wrapped.read_data()
        decrypted = "".join(chr(ord(c) ^ 0x55) for c in encrypted)
        return decrypted

# Compose wrappers: Encryption -> Raw String Source
raw_storage = StringDataSource()
secure_storage = EncryptionDecorator(raw_storage)

secret_msg = "TopSecretCredentials123"
secure_storage.write_data(secret_msg)

print(f"  Raw underlying stored bytes: '{raw_storage.read_data()}' (Encrypted in storage!)")
print(f"  Decrypted read via wrapper:  '{secure_storage.read_data()}'")

assert raw_storage.read_data() != secret_msg
assert secure_storage.read_data() == secret_msg

# Explanation: The Decorator pattern attaches additional responsibilities to an object
# dynamically by wrapping it with another object that implements the same interface.


# ============================================================
# Q5: The Strategy Pattern (Behavioral Composition)
# ============================================================
# Question: Model a Duck simulation where flying and quacking behaviors are composed
# as Strategy components, preventing the inheritance combinatorial explosion problem.

print("\n=== Q5: Strategy Pattern (Behavioral Composition) ===")

# Fly strategies
class FlyWithWings:
    def fly(self) -> str: return "Flying with feathered wings!"

class FlyNoWay:
    def fly(self) -> str: return "Cannot fly."

# Quack strategies
class QuackAudible:
    def quack(self) -> str: return "Quack! Quack!"

class SqueakMuted:
    def quack(self) -> str: return "<< Squeak >>"

class Duck:
    def __init__(self, name: str, fly_behavior: Any, quack_behavior: Any):
        self.name = name
        self.fly_behavior = fly_behavior      # Composed strategy
        self.quack_behavior = quack_behavior  # Composed strategy

    def perform_fly(self) -> str:
        return self.fly_behavior.fly()

    def perform_quack(self) -> str:
        return self.quack_behavior.quack()

mallard = Duck("Mallard", FlyWithWings(), QuackAudible())
rubber_duck = Duck("Rubber Duck", FlyNoWay(), SqueakMuted())

print(f"  {mallard.name}: {mallard.perform_fly()} | {mallard.perform_quack()}")
print(f"  {rubber_duck.name}: {rubber_duck.perform_fly()} | {rubber_duck.perform_quack()}")

assert mallard.perform_fly() == "Flying with feathered wings!"
assert rubber_duck.perform_fly() == "Cannot fly."

# Dynamically change behavior at runtime!
rubber_duck.fly_behavior = FlyWithWings()  # Upgraded with rocket wings!
assert rubber_duck.perform_fly() == "Flying with feathered wings!"

# Explanation: By composing behaviors instead of subclassing, N flying behaviors and
# M quacking behaviors require only N+M classes instead of N*M combinatorial subclasses.


# ============================================================
# Q6: The Composite Pattern (Uniform Tree Processing)
# ============================================================
# Question: Implement the Composite design pattern for a filesystem hierarchy:
# `File` (Leaf) and `Directory` (Composite) both satisfy a common `FileSystemNode` interface.

print("\n=== Q6: The Composite Pattern (Tree Hierarchies) ===")

class FileSystemNode(Protocol):
    def get_size_kb(self) -> int: ...
    def display(self, indent: int = 0) -> List[str]: ...

class File:
    def __init__(self, name: str, size_kb: int):
        self.name = name
        self.size_kb = size_kb

    def get_size_kb(self) -> int:
        return self.size_kb

    def display(self, indent: int = 0) -> List[str]:
        return [f"{'  ' * indent}- File: {self.name} ({self.size_kb} KB)"]

class Directory:
    def __init__(self, name: str):
        self.name = name
        self.children: List[FileSystemNode] = []  # Composes nodes (Files or other Directories!)

    def add(self, node: FileSystemNode) -> None:
        self.children.append(node)

    def get_size_kb(self) -> int:
        return sum(child.get_size_kb() for child in self.children)

    def display(self, indent: int = 0) -> List[str]:
        lines = [f"{'  ' * indent}+ Dir: {self.name}/"]
        for child in self.children:
            lines.extend(child.display(indent + 1))
        return lines

# Build tree
root = Directory("root")
src = Directory("src")
src.add(File("app.py", 45))
src.add(File("utils.py", 20))
root.add(src)
root.add(File("README.md", 5))

total_size = root.get_size_kb()
tree_display = root.display()

print("  Filesystem Tree:")
for line in tree_display:
    print(f"    {line}")
print(f"  Total Tree Size: {total_size} KB")

assert total_size == 70
assert len(tree_display) == 5

# Explanation: The Composite pattern lets clients treat individual objects (Files)
# and compositions of objects (Directories) uniformly.


# ============================================================
# Q7: Refactoring Brittle Inheritance into Clean Composition
# ============================================================
# Question: Contrast a brittle deep inheritance hierarchy (e.g. `Vehicle -> WheeledVehicle -> MotorizedWheeledVehicle`)
# with a clean composition architecture using modular specs.

print("\n=== Q7: Refactoring Deep Inheritance into Composition ===")

class Wheel:
    def __init__(self, count: int, diameter_in: int):
        self.count = count
        self.diameter = diameter_in

class PowerSource:
    def __init__(self, type_str: str, hp: int):
        self.type_str = type_str
        self.hp = hp

# Clean composed Vehicle replaces 6+ subclasses
class ModularVehicle:
    def __init__(self, name: str, wheels: Wheel, power: PowerSource):
        self.name = name
        self.wheels = wheels
        self.power = power

    def specs(self) -> str:
        return f"{self.name}: {self.wheels.count} wheels ({self.wheels.diameter}\"), {self.power.type_str} engine ({self.power.hp} HP)"

bicycle = ModularVehicle("Bicycle", Wheel(2, 28), PowerSource("Human", 1))
truck = ModularVehicle("Semi-Truck", Wheel(18, 22), PowerSource("Diesel Turbo", 500))

print(f"  {bicycle.specs()}")
print(f"  {truck.specs()}")

assert "2 wheels" in bicycle.specs()
assert "18 wheels" in truck.specs()
assert "500 HP" in truck.specs()

# Explanation: Deep inheritance chains become rigid and break easily when new requirements emerge.
# Composing small, focused components provides limitless combinations without class explosion.


# ============================================================
# Q8: The State Pattern via Composition
# ============================================================
# Question: Implement the State pattern where an `OrderLifecycle` object delegates
# state-dependent operations (pay, ship, cancel) to a composed `OrderState` component.

print("\n=== Q8: The State Pattern via Composition ===")

class OrderState(Protocol):
    def pay(self, order: "OrderContext") -> str: ...
    def ship(self, order: "OrderContext") -> str: ...
    def cancel(self, order: "OrderContext") -> str: ...

class PendingPaymentState:
    def pay(self, order: "OrderContext") -> str:
        order.state = PaidState()  # Transition state!
        return "Payment processed. Order is now PAID."
    def ship(self, order: "OrderContext") -> str:
        raise ValueError("Cannot ship an unpaid order!")
    def cancel(self, order: "OrderContext") -> str:
        order.state = CancelledState()
        return "Order cancelled."

class PaidState:
    def pay(self, order: "OrderContext") -> str:
        raise ValueError("Order is already paid!")
    def ship(self, order: "OrderContext") -> str:
        order.state = ShippedState()
        return "Order dispatched for delivery."
    def cancel(self, order: "OrderContext") -> str:
        order.state = CancelledState()
        return "Payment refunded. Order cancelled."

class ShippedState:
    def pay(self, order: "OrderContext") -> str: raise ValueError("Already delivered")
    def ship(self, order: "OrderContext") -> str: raise ValueError("Already shipped")
    def cancel(self, order: "OrderContext") -> str: raise ValueError("Cannot cancel shipped order!")

class CancelledState:
    def pay(self, order: "OrderContext") -> str: raise ValueError("Order is cancelled")
    def ship(self, order: "OrderContext") -> str: raise ValueError("Order is cancelled")
    def cancel(self, order: "OrderContext") -> str: raise ValueError("Already cancelled")

class OrderContext:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.state: OrderState = PendingPaymentState()

    def pay(self) -> str: return self.state.pay(self)
    def ship(self) -> str: return self.state.ship(self)
    def cancel(self) -> str: return self.state.cancel(self)

order = OrderContext("ORD-9021")
assert isinstance(order.state, PendingPaymentState)

# Process payment
res_pay = order.pay()
print(f"  Step 1: {res_pay}")
assert isinstance(order.state, PaidState)

# Ship order
res_ship = order.ship()
print(f"  Step 2: {res_ship}")
assert isinstance(order.state, ShippedState)

# Trying to cancel a shipped order fails
caught_cancel_err = False
try:
    order.cancel()
except ValueError as err:
    caught_cancel_err = True
    print(f"  Caught expected error: {err}")

assert caught_cancel_err

# Explanation: The State pattern uses composition to encapsulate state-specific behavior.
# The context delegates calls to its current state object, which manages valid transitions.


# ============================================================
# Q9: Hybrid Architecture: Interface Inheritance + Component Composition
# ============================================================
# Question: Demonstrate standard enterprise architecture: an Abstract Base Class defines
# the interface contract (inheritance), while concrete implementations compose modular services.

print("\n=== Q9: Hybrid Architecture (Inheritance + Composition) ===")

from abc import ABC, abstractmethod

class NotifierService(ABC):
    """Abstract interface contract (Inheritance)."""
    @abstractmethod
    def notify(self, message: str) -> bool: pass

class PushNotificationSender:
    """Composed helper component."""
    def send_push(self, text: str) -> str:
        return f"APNS_SENT: {text}"

class MobileAppNotifier(NotifierService):
    """Concrete implementation that fulfills contract via composition."""
    def __init__(self, sender: PushNotificationSender):
        self._sender = sender  # Composed component

    def notify(self, message: str) -> bool:
        res = self._sender.send_push(message)
        return "APNS_SENT" in res

notifier: NotifierService = MobileAppNotifier(PushNotificationSender())
success = notifier.notify("Server alert: high CPU load")

print(f"  Notification dispatched successfully: {success}")
assert success is True
assert isinstance(notifier, NotifierService)

# Explanation: Use inheritance for high-level contracts and polymorphic typing (interfaces).
# Use composition for sharing implementation, logic, and infrastructure.


# ============================================================
# Q10: Production-Grade E-Commerce Order Processing Engine
# ============================================================
# Question: Build a production-grade `OrderProcessingPipeline` that cleanly composes
# independent service components: TaxCalculator, DiscountPolicy, PaymentService, and AuditLogger.

print("\n=== Q10: Domain Entity: Order Processing Engine ===")

class TaxCalculator(Protocol):
    def calculate_tax(self, subtotal: float) -> float: ...

class DiscountPolicy(Protocol):
    def calculate_discount(self, subtotal: float) -> float: ...

class PaymentService(Protocol):
    def charge(self, amount: float) -> str: ...

# Component 1: Standard Tax
class StandardTaxCalculator:
    def __init__(self, rate: float = 0.08):
        self.rate = rate
    def calculate_tax(self, subtotal: float) -> float:
        return round(subtotal * self.rate, 2)

# Component 2: VIP Discount
class VipDiscountPolicy:
    def __init__(self, percentage: float = 0.10):
        self.percentage = percentage
    def calculate_discount(self, subtotal: float) -> float:
        return round(subtotal * self.percentage, 2)

# Component 3: Mock Payment Gateway
class StripePaymentService:
    def charge(self, amount: float) -> str:
        return f"STRIPE_TX_APPROVED_${amount:.2f}"

# Composed Core Engine
class OrderProcessingEngine:
    def __init__(
        self,
        tax_calc: TaxCalculator,
        discount_policy: DiscountPolicy,
        payment_service: PaymentService
    ):
        self.tax_calc = tax_calc
        self.discount_policy = discount_policy
        self.payment_service = payment_service
        self.execution_ledger: List[Dict[str, Any]] = []

    def process_order(self, order_id: str, subtotal: float) -> Dict[str, Any]:
        discount = self.discount_policy.calculate_discount(subtotal)
        taxable = subtotal - discount
        tax = self.tax_calc.calculate_tax(taxable)
        final_payable = round(taxable + tax, 2)

        tx_code = self.payment_service.charge(final_payable)

        record = {
            "order_id": order_id,
            "subtotal": subtotal,
            "discount": discount,
            "tax": tax,
            "final_payable": final_payable,
            "tx_code": tx_code
        }
        self.execution_ledger.append(record)
        return record

engine = OrderProcessingEngine(
    tax_calc=StandardTaxCalculator(rate=0.08),
    discount_policy=VipDiscountPolicy(percentage=0.10),
    payment_service=StripePaymentService()
)

# Process order of $100.00
# Math: subtotal=$100, discount=10% ($10), taxable=$90, tax=8% ($7.20), final=$97.20
order_receipt = engine.process_order("ORD_5001", 100.0)

print("  Processed Order Receipt:")
print(f"    Order ID:      {order_receipt['order_id']}")
print(f"    Subtotal:     ${order_receipt['subtotal']:.2f}")
print(f"    Discount:    -${order_receipt['discount']:.2f}")
print(f"    Tax (8%):     +${order_receipt['tax']:.2f}")
print(f"    Final Paid:   ${order_receipt['final_payable']:.2f}")
print(f"    Receipt Code:  {order_receipt['tx_code']}")

assert order_receipt["final_payable"] == 97.20
assert "STRIPE_TX_APPROVED_$97.20" in order_receipt["tx_code"]
assert len(engine.execution_ledger) == 1

print("\nAll 10 composition vs inheritance questions executed and asserted successfully!")
