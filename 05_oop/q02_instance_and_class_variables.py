"""
Topic 05: Object-Oriented Programming (OOP)
Question 02: Instance and Class Variables (Deep Dive)

Master class-level vs instance-level variable semantics:
- Shared class variable state across all instances
- The attribute shadowing trap (instance.attr = val creates instance binding)
- Mutable class variables pitfall (the shared list/dict bug)
- Class-level registry tracking all live instances
- Hierarchical configuration with instance overrides
- Memory optimization with __slots__ (eliminating __dict__ overhead)
- __slots__ mechanics across inheritance hierarchies
- Class variable resolution and subclass overrides
- Descriptors distinguishing instance vs class access (instance is None)
- Production-grade multi-tenant feature flag & rate-limit configuration engine
"""

import sys
import weakref
from typing import Any, Dict, List, Optional, Set


# ============================================================
# Q1: Class Variables & Shared State across Instances
# ============================================================
# Question: Define a class with a class-level variable `interest_rate`.
# Demonstrate that mutating `Bank.interest_rate` updates the rate across all existing
# instances simultaneously.

print("=== Q1: Class Variables & Shared State ===")

class BankAccount:
    annual_interest_rate = 0.04  # 4% shared across all accounts

    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self.balance = balance

    def calculate_interest(self) -> float:
        return round(self.balance * self.annual_interest_rate, 2)

acc1 = BankAccount("Alice", 1000.0)
acc2 = BankAccount("Bob", 2000.0)

print(f"  Alice interest at 4%: ${acc1.calculate_interest():.2f}")
print(f"  Bob interest at 4%:   ${acc2.calculate_interest():.2f}")
assert acc1.calculate_interest() == 40.0
assert acc2.calculate_interest() == 80.0

# Mutate the class variable at class level
BankAccount.annual_interest_rate = 0.05  # Increased to 5%

print(f"  After Bank update -> Alice: ${acc1.calculate_interest():.2f}, Bob: ${acc2.calculate_interest():.2f}")
assert acc1.calculate_interest() == 50.0
assert acc2.calculate_interest() == 100.0

# Explanation: Class variables are stored on the Class object. All instances without
# an instance-level attribute of the same name resolve lookups to the shared class attribute.


# ============================================================
# Q2: The Shadowing Trap (instance.attr = new_val)
# ============================================================
# Question: Demonstrate what happens when modifying a class variable via an instance.
# Prove that `acc.interest_rate = 0.06` creates a local instance attribute, shadowing
# the class variable rather than modifying it for other instances.

print("\n=== Q2: The Attribute Shadowing Trap ===")

acc_alice = BankAccount("Alice", 1000.0)
acc_bob = BankAccount("Bob", 1000.0)

# Alice gets a special promotional rate: assigning via instance!
acc_alice.annual_interest_rate = 0.08  # SHADOWING! Creates key in acc_alice.__dict__

print(f"  Alice __dict__: {acc_alice.__dict__}")
print(f"  Bob __dict__:   {acc_bob.__dict__}")

# Alice's instance now shadows the class variable
assert "annual_interest_rate" in acc_alice.__dict__
assert "annual_interest_rate" not in acc_bob.__dict__

print(f"  Alice special rate: {acc_alice.annual_interest_rate}")
print(f"  Bob standard rate:  {acc_bob.annual_interest_rate}")
print(f"  Bank class rate:    {BankAccount.annual_interest_rate}")

assert acc_alice.annual_interest_rate == 0.08
assert acc_bob.annual_interest_rate == 0.05
assert BankAccount.annual_interest_rate == 0.05

# Deleting the instance attribute un-shadows and restores class variable lookup
del acc_alice.annual_interest_rate
assert acc_alice.annual_interest_rate == 0.05
print(f"  After 'del acc_alice.annual_interest_rate', Alice restored to: {acc_alice.annual_interest_rate}")

# Explanation: In Python, attribute read traverses instance -> class -> base classes.
# However, attribute write (`instance.attr = val`) ALWAYS writes to `instance.__dict__`
# unless overridden by a descriptor or property setter.


# ============================================================
# Q3: Mutable Class Variables (The Shared List/Dict Bug)
# ============================================================
# Question: Demonstrate the infamous mutable class variable bug where declaring
# `tags = []` at the class level accidentally shares tags across all instances.
# Contrast with proper instance initialization.

print("\n=== Q3: Mutable Class Variables Pitfall ===")

# THE BUGGY CLASS: shared mutable list at class level!
class BuggyArticle:
    tags: List[str] = []  # Shared across ALL instances!

    def __init__(self, title: str):
        self.title = title

    def add_tag(self, tag: str) -> None:
        self.tags.append(tag)  # Mutates the shared class list!

art1 = BuggyArticle("Intro to Python")
art2 = BuggyArticle("Advanced Async")

art1.add_tag("beginner")
art1.add_tag("python")

# The bug: art2 has tags added by art1!
print(f"  Buggy Article 2 tags: {art2.tags} (Contaminated by Article 1!)")
assert art2.tags == ["beginner", "python"]
assert art1.tags is art2.tags

# THE CLEAN CLASS: initialize mutable collections inside __init__
class CleanArticle:
    def __init__(self, title: str):
        self.title = title
        self.tags: List[str] = []  # Unique instance list!

    def add_tag(self, tag: str) -> None:
        self.tags.append(tag)

c_art1 = CleanArticle("Intro to Python")
c_art2 = CleanArticle("Advanced Async")

c_art1.add_tag("beginner")
print(f"  Clean Article 1 tags: {c_art1.tags}")
print(f"  Clean Article 2 tags: {c_art2.tags} (Isolated!)")

assert c_art1.tags == ["beginner"]
assert c_art2.tags == []

# Explanation: Class-level assignments execute once when class is defined.
# Mutable objects (lists, dicts, sets) at class level are shared by all instances.
# Always instantiate fresh collections inside `__init__`.


# ============================================================
# Q4: Active Instance Registry via Weak References
# ============================================================
# Question: Implement a class that automatically tracks all active live instances
# in a class-level registry using `weakref.WeakSet` to prevent memory leaks.

print("\n=== Q4: Active Instance Registry with WeakSet ===")

class ActiveUserSession:
    # Class-level WeakSet automatically drops objects when they are deallocated
    _active_sessions: weakref.WeakSet["ActiveUserSession"] = weakref.WeakSet()

    def __init__(self, username: str, session_token: str):
        self.username = username
        self.session_token = session_token
        ActiveUserSession._active_sessions.add(self)

    @classmethod
    def get_active_count(cls) -> int:
        return len(cls._active_sessions)

    @classmethod
    def get_all_active_users(cls) -> List[str]:
        return [sess.username for sess in cls._active_sessions]

s1 = ActiveUserSession("alice", "token_a")
s2 = ActiveUserSession("bob", "token_b")
s3 = ActiveUserSession("charlie", "token_c")

print(f"  Active session count: {ActiveUserSession.get_active_count()}")
assert ActiveUserSession.get_active_count() == 3

# Deallocate session 2
del s2
print(f"  Active session count after 'del s2': {ActiveUserSession.get_active_count()}")
assert ActiveUserSession.get_active_count() == 2
assert "bob" not in ActiveUserSession.get_all_active_users()

# Explanation: Storing standard references in a class list keeps instances alive forever
# (memory leak). `weakref.WeakSet` holds non-owning references that auto-evict upon garbage collection.


# ============================================================
# Q5: Hierarchical Configuration with Instance Overrides
# ============================================================
# Question: Build a database query client where default timeout, retry count, and SSL
# are defined as class variables, and individual clients can selectively override any parameter.

print("\n=== Q5: Class Configuration Defaults & Instance Overrides ===")

class DatabaseClient:
    default_timeout = 10.0
    default_retries = 3
    default_ssl = True

    def __init__(self, host: str, **overrides: Any):
        self.host = host
        # Copy class defaults or apply instance-level overrides
        for key in ["timeout", "retries", "ssl"]:
            val = overrides.get(key, getattr(self.__class__, f"default_{key}"))
            setattr(self, key, val)

# Client 1 uses class defaults
c_default = DatabaseClient("db-main.internal")
print(f"  Default client: timeout={c_default.timeout}, retries={c_default.retries}, ssl={c_default.ssl}")
assert c_default.timeout == 10.0
assert c_default.retries == 3
assert c_default.ssl is True

# Client 2 overrides timeout and ssl
c_custom = DatabaseClient("db-dev.internal", timeout=2.5, ssl=False)
print(f"  Custom client:  timeout={c_custom.timeout}, retries={c_custom.retries}, ssl={c_custom.ssl}")
assert c_custom.timeout == 2.5
assert c_custom.retries == 3
assert c_custom.ssl is False

# Explanation: Establishing class-level configuration provides standardized defaults
# while permitting granular per-instance overrides.


# ============================================================
# Q6: Memory Optimization with __slots__
# ============================================================
# Question: Compare memory usage and attribute dynamics between a standard class
# (which allocates an instance `__dict__`) and a `__slots__` class.

print("\n=== Q6: Memory Optimization via __slots__ ===")

class StandardPixel:
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

class SlottedPixel:
    # Explicitly declare fixed attribute names; eliminates instance __dict__!
    __slots__ = ("r", "g", "b")

    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

p_std = StandardPixel(255, 128, 0)
p_slot = SlottedPixel(255, 128, 0)

# Standard pixel has a __dict__ and dynamic attribute capability
assert hasattr(p_std, "__dict__")
p_std.alpha = 255  # Allowed!
assert p_std.alpha == 255

# Slotted pixel has NO __dict__ and rejects arbitrary new attributes!
assert not hasattr(p_slot, "__dict__")
caught_slot_attr_err = False
try:
    p_slot.alpha = 255  # type: ignore
except AttributeError as err:
    caught_slot_attr_err = True
    print(f"  Caught expected __slots__ AttributeError: {err}")

assert caught_slot_attr_err

# Memory footprint comparison
# Note: sys.getsizeof() on instance + __dict__ overhead
std_size = sys.getsizeof(p_std) + sys.getsizeof(p_std.__dict__)
slot_size = sys.getsizeof(p_slot)

print(f"  Standard instance + __dict__ size: ~{std_size} bytes")
print(f"  Slotted instance size:             ~{slot_size} bytes")
print(f"  Memory savings per instance:       ~{(1 - slot_size / std_size) * 100:.1f}%")

assert slot_size < std_size

# Explanation: `__slots__` replaces the per-instance dictionary with a compact C-level
# array of fixed descriptors, reducing memory consumption by 50-70% for millions of objects.


# ============================================================
# Q7: __slots__ across Class Inheritance
# ============================================================
# Question: Demonstrate that if a subclass does NOT define `__slots__`, it automatically
# gains an instance `__dict__`, negating memory optimization benefits for the subclass.

print("\n=== Q7: __slots__ in Inheritance Hierarchies ===")

class SlottedBase:
    __slots__ = ("base_id",)
    def __init__(self, base_id: str):
        self.base_id = base_id

class UnslottedSubclass(SlottedBase):
    # Does NOT define __slots__ -> Python creates a __dict__ for this subclass!
    def __init__(self, base_id: str, extra_data: str):
        super().__init__(base_id)
        self.extra_data = extra_data

class ProperSlottedSubclass(SlottedBase):
    # Explicitly declares only the new attributes in __slots__
    __slots__ = ("extra_data",)
    def __init__(self, base_id: str, extra_data: str):
        super().__init__(base_id)
        self.extra_data = extra_data

unslotted = UnslottedSubclass("ID_1", "Extra")
proper = ProperSlottedSubclass("ID_2", "Extra")

print(f"  UnslottedSubclass has __dict__:     {hasattr(unslotted, '__dict__')} (Memory optimization LOST!)")
print(f"  ProperSlottedSubclass has __dict__: {hasattr(proper, '__dict__')} (Optimized!)")

assert hasattr(unslotted, "__dict__")
assert not hasattr(proper, "__dict__")

# Explanation: To retain `__slots__` memory benefits down an inheritance chain,
# every subclass must explicitly declare its own `__slots__` containing only its new attributes.


# ============================================================
# Q8: Class Variable Resolution & Subclass Overrides
# ============================================================
# Question: Demonstrate how subclasses inherit and override class variables without
# modifying the parent class or sister subclasses.

print("\n=== Q8: Class Variable Subclass Overrides ===")

class AnimalBase:
    kingdom = "Animalia"
    legs = 4
    sound = "Generic Sound"

class Bird(AnimalBase):
    legs = 2  # Override legs for Bird hierarchy
    sound = "Chirp"

class Snake(AnimalBase):
    legs = 0  # Override legs for Snake hierarchy
    sound = "Hiss"

print(f"  AnimalBase: legs={AnimalBase.legs}, sound='{AnimalBase.sound}'")
print(f"  Bird:       legs={Bird.legs}, sound='{Bird.sound}'")
print(f"  Snake:      legs={Snake.legs}, sound='{Snake.sound}'")

# All still share kingdom from AnimalBase
assert Bird.kingdom == Snake.kingdom == AnimalBase.kingdom == "Animalia"
assert Bird.legs == 2
assert Snake.legs == 0
assert AnimalBase.legs == 4

# Explanation: Subclasses inherit parent class variables. Overriding a class variable
# in a subclass places the key in `Subclass.__dict__`, leaving the parent untouched.


# ============================================================
# Q9: Descriptors: Distinguishing Instance vs Class Access
# ============================================================
# Question: Implement a descriptor that behaves differently depending on whether it is
# accessed via the class (`Class.field`) or via an instance (`instance.field`).

print("\n=== Q9: Descriptor Instance vs Class Access ===")

class ModelFieldDescriptor:
    def __init__(self, field_type: type, default: Any = None):
        self.field_type = field_type
        self.default = default
        self.name = ""

    def __set_name__(self, owner: type, name: str):
        self.name = name

    def __get__(self, instance: Optional[Any], owner: type) -> Any:
        # If accessed from class (e.g. User.age), return the descriptor object itself!
        if instance is None:
            return self
        # If accessed from instance (e.g. u.age), return the instance value
        return instance.__dict__.get(self.name, self.default)

    def __set__(self, instance: Any, value: Any):
        if not isinstance(value, self.field_type):
            raise TypeError(f"Field '{self.name}' must be of type {self.field_type.__name__}")
        instance.__dict__[self.name] = value

class UserRecord:
    username = ModelFieldDescriptor(str, default="Guest")
    score = ModelFieldDescriptor(int, default=0)

# Class access returns descriptor for introspection (like Django/SQLAlchemy models)
desc_score = UserRecord.score
print(f"  UserRecord.score (class access): {desc_score} (type: {type(desc_score).__name__})")
assert isinstance(desc_score, ModelFieldDescriptor)
assert desc_score.field_type is int

# Instance access returns concrete values
u = UserRecord()
print(f"  Default username: {u.username}, score: {u.score}")
assert u.username == "Guest" and u.score == 0

u.username = "Alice"
u.score = 150
print(f"  Updated user: {u.username}, score: {u.score}")
assert u.username == "Alice" and u.score == 150

# Explanation: When `instance is None`, the descriptor knows it was accessed on the
# class object, allowing ORMs to inspect schema metadata without requiring an instance.


# ============================================================
# Q10: Production-Grade Multi-Tenant Feature Flag & Rate Limiter
# ============================================================
# Question: Implement a production-grade multi-tenant configuration manager:
# - Class variables define global default rate limits and enabled features.
# - Instance variables provide tenant-specific overrides.
# - A class-level counter monitors aggregate global throughput.

print("\n=== Q10: Multi-Tenant Feature Flag & Rate Limiter ===")

class TenantServiceManager:
    # Global class-level default settings
    default_max_qps = 100
    global_total_requests = 0
    global_feature_flags: Dict[str, bool] = {
        "beta_ai_assistant": False,
        "streaming_export": True,
        "audit_logs": True
    }

    def __init__(self, tenant_id: str, max_qps_override: Optional[int] = None):
        self.tenant_id = tenant_id
        self.max_qps = max_qps_override if max_qps_override is not None else self.default_max_qps
        # Tenant specific feature flag overrides
        self._feature_overrides: Dict[str, bool] = {}
        self.tenant_request_count = 0

    def set_feature_override(self, feature_name: str, enabled: bool) -> None:
        self._feature_overrides[feature_name] = enabled

    def is_feature_enabled(self, feature_name: str) -> bool:
        # Check tenant override first; fallback to class global defaults
        if feature_name in self._feature_overrides:
            return self._feature_overrides[feature_name]
        return self.global_feature_flags.get(feature_name, False)

    def record_request(self) -> bool:
        """Records a request if under tenant rate limit."""
        if self.tenant_request_count >= self.max_qps:
            return False  # Rate limit exceeded for this tenant
        
        self.tenant_request_count += 1
        TenantServiceManager.global_total_requests += 1  # Updates class-level aggregate
        return True

# Tenant A: Standard Tier (Uses global max_qps=100 and default flags)
tenant_standard = TenantServiceManager("tenant_std_01")

# Tenant B: Enterprise Tier (High max_qps=500 and beta AI enabled)
tenant_enterprise = TenantServiceManager("tenant_ent_02", max_qps_override=500)
tenant_enterprise.set_feature_override("beta_ai_assistant", True)

# Feature flag verification
assert tenant_standard.is_feature_enabled("beta_ai_assistant") is False
assert tenant_enterprise.is_feature_enabled("beta_ai_assistant") is True
assert tenant_standard.is_feature_enabled("streaming_export") is True

# Process requests
for _ in range(50):
    tenant_standard.record_request()

for _ in range(75):
    tenant_enterprise.record_request()

print(f"  Tenant Standard requests:   {tenant_standard.tenant_request_count}")
print(f"  Tenant Enterprise requests: {tenant_enterprise.tenant_request_count}")
print(f"  Global total requests:      {TenantServiceManager.global_total_requests}")

assert tenant_standard.tenant_request_count == 50
assert tenant_enterprise.tenant_request_count == 75
assert TenantServiceManager.global_total_requests == 125

print("\nAll 10 instance and class variables questions executed and asserted successfully!")
