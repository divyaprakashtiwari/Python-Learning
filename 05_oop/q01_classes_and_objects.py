"""
Topic 05: Object-Oriented Programming (OOP)
Question 01: Classes and Objects (Deep Dive)

Master fundamental OOP mechanics in Python:
- Class definitions, instantiation, and the role of the 'self' parameter
- Object construction pipeline: __new__ (allocator) vs __init__ (initializer)
- Type inspection: isinstance() vs issubclass() vs type() identity
- Class namespace vs instance namespace (__dict__)
- Dynamic attribute manipulation: getattr(), setattr(), hasattr(), delattr()
- String representations: __str__ (user display) vs __repr__ (developer inspection)
- Object lifecycle and garbage collection (__del__ finalizer caveats)
- Value equality (__eq__) and hashability contracts (__hash__)
- Metaclass dynamic class generation via type() factory
- Production-grade domain entity: BankAccount with transaction history ledger
"""

from typing import Any, Dict, List, Optional


# ============================================================
# Q1: Class Definition, Instantiation, and the 'self' Parameter
# ============================================================
# Question: Define a Car class with attributes. Explain the 'self' parameter:
# demonstrate that `car.start_engine()` is syntactic sugar for `Car.start_engine(car)`.

print("=== Q1: Class Definition & 'self' Mechanics ===")

class Car:
    def __init__(self, make: str, model: str, year: int):
        self.make = make
        self.model = model
        self.year = year
        self.is_running = False

    def start_engine(self) -> str:
        self.is_running = True
        return f"{self.year} {self.make} {self.model} engine started."

# Method invocation via instance
sedan = Car("Toyota", "Camry", 2024)
res_inst = sedan.start_engine()
print(f"  Instance call: {res_inst}")
assert sedan.is_running is True

# Method invocation via Class explicitly passing the instance as 'self'
suv = Car("Honda", "CR-V", 2023)
res_cls = Car.start_engine(suv)  # Explicitly passing 'suv' as self
print(f"  Class call:    {res_cls}")
assert suv.is_running is True

# Explanation: 'self' is not a keyword (merely a convention), but represents
# the specific instance receiving the method call. In Python, `instance.method(arg)`
# translates directly to `Class.method(instance, arg)`.


# ============================================================
# Q2: __new__ (Object Allocation) vs __init__ (Initialization)
# ============================================================
# Question: Demonstrate the separation of duties between `__new__` (allocates the raw object)
# and `__init__` (populates object attributes). Implement a Singleton class using `__new__`.

print("\n=== Q2: __new__ vs __init__ (Singleton Pattern) ===")

class DatabaseConnectionPool:
    _instance: Optional["DatabaseConnectionPool"] = None

    def __new__(cls, *args, **kwargs) -> "DatabaseConnectionPool":
        """__new__ is the true constructor: allocates and returns a new instance."""
        if cls._instance is None:
            # Allocate instance via super().__new__
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, dsn: str):
        """__init__ initializes instance state, called after __new__ returns."""
        if not getattr(self, "_initialized", False):
            self.dsn = dsn
            self._initialized = True

pool1 = DatabaseConnectionPool("postgres://primary-db:5432/main")
pool2 = DatabaseConnectionPool("postgres://replica-db:5432/main")

print(f"  pool1 DSN: {pool1.dsn}")
print(f"  pool2 DSN: {pool2.dsn}")
print(f"  pool1 is pool2 (Identical memory address): {pool1 is pool2}")

assert pool1 is pool2
assert pool2.dsn == "postgres://primary-db:5432/main"  # Preserved original

# Explanation: `__new__` is a static method that takes `cls` and returns an object instance.
# `__init__` takes `self` and mutates it. Python calls `__init__` only if `__new__` returns
# an instance of `cls`.


# ============================================================
# Q3: Type Inspection: isinstance() vs issubclass() vs type()
# ============================================================
# Question: Compare `type(obj) is Class` against `isinstance(obj, Class)`.
# Explain why `isinstance` is preferred for polymorphic class hierarchies.

print("\n=== Q3: isinstance() vs type() Identity ===")

class Animal:
    pass

class Dog(Animal):
    pass

class GoldenRetriever(Dog):
    pass

buddy = GoldenRetriever()

# 1. type() checks for EXACT class equality (ignores inheritance!)
is_exact_dog = type(buddy) is Dog
is_exact_retriever = type(buddy) is GoldenRetriever

print(f"  type(buddy) is Dog:             {is_exact_dog} (False: ignores inheritance!)")
print(f"  type(buddy) is GoldenRetriever: {is_exact_retriever}")

assert not is_exact_dog
assert is_exact_retriever

# 2. isinstance() supports inheritance and polymorphism
is_inst_retriever = isinstance(buddy, GoldenRetriever)
is_inst_dog = isinstance(buddy, Dog)
is_inst_animal = isinstance(buddy, Animal)

print(f"  isinstance(buddy, Dog):         {is_inst_dog}")
print(f"  isinstance(buddy, Animal):      {is_inst_animal}")

assert is_inst_retriever and is_inst_dog and is_inst_animal

# 3. issubclass() checks class-to-class relationship
assert issubclass(GoldenRetriever, Animal)
assert not issubclass(Animal, Dog)

# Explanation: Use `isinstance(obj, Class)` to support polymorphic inheritance.
# Use `type(obj) is Class` only when strictly requiring exact class identity.


# ============================================================
# Q4: Class Namespace vs Instance Namespace (__dict__)
# ============================================================
# Question: Inspect the `__dict__` dictionary of both a class and its instances.
# Demonstrate that instances don't store class-level attributes in their own `__dict__`.

print("\n=== Q4: Namespace Dictionaries (__dict__) ===")

class Employee:
    company_name = "TechCorp Global"  # Class-level attribute
    employee_count = 0

    def __init__(self, name: str, role: str):
        self.name = name              # Instance-level attribute
        self.role = role
        Employee.employee_count += 1

emp = Employee("Alice", "Backend Engineer")

# Inspect instance __dict__
print(f"  Instance __dict__: {emp.__dict__}")
assert "company_name" not in emp.__dict__
assert "name" in emp.__dict__ and "role" in emp.__dict__

# Accessing class attribute via instance delegates to Class.__dict__
print(f"  emp.company_name: '{emp.company_name}' (Delegated to Employee.company_name)")
assert emp.company_name == "TechCorp Global"

# Overriding class attribute on instance creates a NEW key in instance __dict__
emp.company_name = "Subsidiary Inc"
print(f"  After override -> instance __dict__: {emp.__dict__}")
print(f"  Class company_name remains:          '{Employee.company_name}'")

assert emp.__dict__["company_name"] == "Subsidiary Inc"
assert Employee.company_name == "TechCorp Global"

# Explanation: Python searches for attributes first in `instance.__dict__`. If not found,
# it traverses the class hierarchy via `type(instance).__dict__` and MRO.


# ============================================================
# Q5: Dynamic Attribute Introspection (getattr, setattr, hasattr, delattr)
# ============================================================
# Question: Build a dynamic record serializer that accesses, mutates, and deletes
# object fields dynamically using standard introspection built-ins.

print("\n=== Q5: Dynamic Attribute Introspection ===")

class DynamicRecord:
    def __init__(self, **fields: Any):
        for key, val in fields.items():
            setattr(self, key, val)

rec = DynamicRecord(hostname="srv-prod-01", port=443, ssl_enabled=True)

# 1. hasattr
has_port = hasattr(rec, "port")
has_token = hasattr(rec, "token")
print(f"  hasattr('port'): {has_port}, hasattr('token'): {has_token}")
assert has_port is True and has_token is False

# 2. getattr with default fallback
retrieved_port = getattr(rec, "port")
missing_token = getattr(rec, "token", "DEFAULT_TOKEN")
print(f"  getattr('port'): {retrieved_port}, getattr('token', default): '{missing_token}'")
assert retrieved_port == 443
assert missing_token == "DEFAULT_TOKEN"

# 3. setattr dynamically
setattr(rec, "environment", "production")
assert rec.environment == "production"

# 4. delattr dynamically
delattr(rec, "ssl_enabled")
assert not hasattr(rec, "ssl_enabled")

# Explanation: `getattr`, `setattr`, `hasattr`, and `delattr` allow building flexible
# ORMs, JSON deserializers, and configuration mappers without hardcoding field names.


# ============================================================
# Q6: String Representations: __str__ vs __repr__
# ============================================================
# Question: Implement both `__str__` and `__repr__` for a 2D Vector class.
# Explain the difference: `__str__` is user-friendly; `__repr__` is unambiguous for debugging
# and ideally can be passed into `eval()` to reconstruct the object.

print("\n=== Q6: __str__ vs __repr__ ===")

class Vector2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """Unambiguous representation for developers: Vector2D(x, y)."""
        return f"Vector2D({self.x!r}, {self.y!r})"

    def __str__(self) -> str:
        """Human-friendly display string: (x, y)."""
        return f"({self.x}, {self.y})"

v = Vector2D(3.5, 4.0)

str_output = str(v)
repr_output = repr(v)

print(f"  str(v)  -> '{str_output}' (User readable)")
print(f"  repr(v) -> '{repr_output}' (Code representation)")

assert str_output == "(3.5, 4.0)"
assert repr_output == "Vector2D(3.5, 4.0)"

# In containers (lists, dicts), Python always displays repr()!
vec_list = [v]
print(f"  In list: {vec_list}")
assert str(vec_list) == "[Vector2D(3.5, 4.0)]"

# Verify eval() reconstruction using repr
reconstructed = eval(repr_output)
assert reconstructed.x == v.x and reconstructed.y == v.y

# Explanation: Rule of thumb: `__repr__` is for developers (detailed, unambiguous).
# `__str__` is for end users (clean, readable). If only `__repr__` is defined,
# Python falls back to it when `__str__` is called.


# ============================================================
# Q7: Value Equality (__eq__) & Hashability (__hash__)
# ============================================================
# Question: Define a Point2D class. Implement `__eq__` so that two distinct instances
# with identical coordinates compare equal. Implement `__hash__` so they can be stored in sets.

print("\n=== Q7: Value Equality & Hashability Contracts ===")

class Point2D:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Point2D):
            return NotImplemented
        return self._x == other._x and self._y == other._y

    def __hash__(self) -> int:
        """Hash must be based on immutable attributes used in __eq__."""
        return hash((self._x, self._y))

    def __repr__(self) -> str:
        return f"Point2D({self._x}, {self._y})"

p1 = Point2D(10, 20)
p2 = Point2D(10, 20)
p3 = Point2D(5, 15)

print(f"  p1 is p2 (same object in RAM):  {p1 is p2} (False: distinct objects)")
print(f"  p1 == p2 (value equality):      {p1 == p2} (True via __eq__)")
assert p1 is not p2
assert p1 == p2
assert p1 != p3

# Test Set deduplication using hashability
point_set = {p1, p2, p3}
print(f"  Set of points {point_set} has length: {len(point_set)}")
assert len(point_set) == 2  # p1 and p2 deduplicated!

# Explanation: In Python, defining `__eq__` automatically sets `__hash__ = None`
# to prevent mutable objects from breaking hash table invariants. You must explicitly
# implement `__hash__` if the object is immutable and hashable.


# ============================================================
# Q8: Object Lifecycle & __del__ Finalizer Caveats
# ============================================================
# Question: Demonstrate the object lifecycle when references reach zero.
# Explain why relying on `__del__` for critical resource cleanup (like files or sockets)
# is hazardous compared to context managers (`with`).

print("\n=== Q8: Object Lifecycle & __del__ Finalizer ===")

lifecycle_events: List[str] = []

class ManagedResource:
    def __init__(self, resource_id: str):
        self.resource_id = resource_id
        lifecycle_events.append(f"ACQUIRED: {self.resource_id}")

    def __del__(self):
        # Called when reference count drops to zero
        lifecycle_events.append(f"RELEASED: {self.resource_id}")

res = ManagedResource("RES_001")
assert lifecycle_events == ["ACQUIRED: RES_001"]

# Dropping reference count to 0 triggers __del__
del res
print(f"  Lifecycle events after 'del res': {lifecycle_events}")
assert "RELEASED: RES_001" in lifecycle_events

# Explanation: `__del__` is invoked when garbage collection deallocates the instance.
# However, circular references or interpreter shutdown can delay or prevent `__del__`
# from executing. Always use context managers (`with`) for deterministic resource disposal.


# ============================================================
# Q9: Dynamic Class Generation via type() Metaclass
# ============================================================
# Question: Demonstrate how Python classes are themselves runtime objects created by `type()`.
# Dynamically create a new class `ProductRecord` at runtime without using the `class` statement.

print("\n=== Q9: Dynamic Class Generation via type() ===")

def product_to_dict(self) -> Dict[str, Any]:
    return {"sku": self.sku, "price": self.price}

# type(name, bases, dict) dynamically constructs a new class!
DynamicProduct = type(
    "DynamicProduct",                        # Class name
    (object,),                               # Base classes
    {                                        # Class attributes and methods
        "category": "Merchandise",
        "to_dict": product_to_dict,
        "__init__": lambda self, sku, price: setattr(self, "sku", sku) or setattr(self, "price", price)
    }
)

# Instantiate and verify
prod = DynamicProduct("SKU-9942", 49.99)
print(f"  Created class:      {type(prod).__name__}")
print(f"  Class category:     {prod.category}")
print(f"  prod.to_dict():     {prod.to_dict()}")

assert type(prod).__name__ == "DynamicProduct"
assert prod.sku == "SKU-9942"
assert prod.price == 49.99
assert prod.to_dict() == {"sku": "SKU-9942", "price": 49.99}

# Explanation: In Python, `class MyClass:` is syntactic sugar that compiles into
# `type('MyClass', bases, namespace_dict)`. Understanding this unlocks metaclasses and dynamic frameworks.


# ============================================================
# Q10: Production-Grade Domain Entity (BankAccount with Ledger)
# ============================================================
# Question: Build a robust BankAccount entity demonstrating OOP best practices:
# private balance encapsulation, immutable transaction ledger records,
# deposit/withdrawal validation, and audit summaries.

print("\n=== Q10: Domain Entity: BankAccount with Ledger ===")

class InsufficientFundsError(ValueError):
    """Raised when withdrawal exceeds available balance."""
    pass

class NegativeAmountError(ValueError):
    """Raised when deposit or withdrawal amount is not positive."""
    pass

class BankAccount:
    def __init__(self, account_number: str, account_holder: str, initial_deposit: float = 0.0):
        if initial_deposit < 0:
            raise NegativeAmountError("Initial deposit cannot be negative")

        self.account_number = account_number
        self.account_holder = account_holder
        self._balance = float(initial_deposit)
        self._transactions: List[Dict[str, Any]] = []

        if initial_deposit > 0:
            self._record_transaction("OPENING_DEPOSIT", initial_deposit)

    @property
    def balance(self) -> float:
        """Read-only property protecting internal balance from external mutation."""
        return self._balance

    def _record_transaction(self, tx_type: str, amount: float) -> None:
        self._transactions.append({
            "type": tx_type,
            "amount": amount,
            "resulting_balance": self._balance
        })

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise NegativeAmountError("Deposit amount must be strictly positive")
        self._balance = round(self._balance + amount, 2)
        self._record_transaction("DEPOSIT", amount)
        return self._balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise NegativeAmountError("Withdrawal amount must be strictly positive")
        if amount > self._balance:
            raise InsufficientFundsError(
                f"Cannot withdraw ${amount:.2f}: available balance is only ${self._balance:.2f}"
            )
        self._balance = round(self._balance - amount, 2)
        self._record_transaction("WITHDRAWAL", amount)
        return self._balance

    def get_statement(self) -> List[Dict[str, Any]]:
        """Returns defensive copy of the transaction ledger."""
        return [dict(tx) for tx in self._transactions]

    def __repr__(self) -> str:
        return f"BankAccount(account_number={self.account_number!r}, holder={self.account_holder!r}, balance={self._balance:.2f})"

# Run banking transactions
account = BankAccount("ACCT-10029", "Divya Prakash", 500.0)
account.deposit(250.0)
account.withdraw(120.0)

print(f"  Account Summary: {account}")
print(f"  Current Balance: ${account.balance:.2f}")

assert account.balance == 630.0
assert len(account.get_statement()) == 3

# Test negative amount error
caught_neg = False
try:
    account.deposit(-50.0)
except NegativeAmountError:
    caught_neg = True
assert caught_neg

# Test insufficient funds error
caught_insufficient = False
try:
    account.withdraw(10_000.0)
except InsufficientFundsError as err:
    caught_insufficient = True
    print(f"  Caught expected insufficient funds: {err}")
assert caught_insufficient

print("\nAll 10 classes and objects questions executed and asserted successfully!")
