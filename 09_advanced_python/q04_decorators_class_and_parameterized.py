"""
Topic: Advanced Python - Class Decorators and Parameterized Decorators
---------------------------------------------------------------------
Questions Covered:
1. Parameterized Decorator Factory: 3-level nesting pattern configuring decorators with arguments.
2. Dual-Use Decorator: Supporting both bare '@decorator' and parameterized '@decorator(arg=val)'.
3. Singleton Class Decorator: Restricting class instantiation to a single persistent instance.
4. Registry Class Decorator: Dynamically registering classes into a categorized plugin registry.
5. Class-Based Decorator (__call__): Implementing stateful callable decorators as classes.
6. Parameterized Class-Based Decorator: Class initialized with options, producing wrappers.
7. Auto-Tracing Class Decorator: Iterating class attributes to automatically wrap all public methods.
8. Method Decorators & The Descriptor Protocol (__get__): Correctly binding 'self' on class methods.
9. Interface Augmentation Class Decorator: Injecting serialization methods (.to_json(), .from_json()).
10. Architectural System: Dependency Injection (DI) Container with @service and @inject decorators.
"""

import functools
import inspect
import json
import types
from typing import Callable, Any, Dict, List, Optional, Type


# ==============================================================================
# Question 1: Parameterized Decorator Factory
# ==============================================================================
def repeat(times: int = 1):
    """Decorator factory that repeats the target function execution 'times' times, returning last."""
    if times < 1:
        raise ValueError("times must be >= 1")

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = None
            for _ in range(times):
                res = func(*args, **kwargs)
            return res
        return wrapper
    return decorator


execution_counter = 0


@repeat(times=4)
def ping_service() -> str:
    global execution_counter
    execution_counter += 1
    return f"ping_{execution_counter}"


def test_q1_parameterized_decorator_factory():
    global execution_counter
    execution_counter = 0
    res = ping_service()
    assert execution_counter == 4
    assert res == "ping_4"
    print("=== Q1: Parameterized Decorator Factory Verified ===")


# ==============================================================================
# Question 2: Dual-Use Decorator (Bare @decor or @decor(prefix=...))
# ==============================================================================
def tag_output(_func: Optional[Callable] = None, *, prefix: str = "[DEFAULT]"):
    """
    Decorator that works both with or without parentheses:
    @tag_output
    or
    @tag_output(prefix="[CUSTOM]")
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f"{prefix} {result}"
        return wrapper

    if _func is None:
        # Called with parentheses: @tag_output(...)
        return decorator
    else:
        # Called without parentheses: @tag_output
        return decorator(_func)


@tag_output
def message_default(text: str) -> str:
    return text


@tag_output(prefix="[SYSTEM]")
def message_custom(text: str) -> str:
    return text


def test_q2_dual_use_decorator():
    assert message_default("Hello") == "[DEFAULT] Hello"
    assert message_custom("Alert") == "[SYSTEM] Alert"
    print("=== Q2: Dual-Use Decorator Verified ===")


# ==============================================================================
# Question 3: Singleton Class Decorator
# ==============================================================================
def singleton(cls: Type[Any]) -> Callable[..., Any]:
    """Class decorator guaranteeing only a single instance of cls is ever constructed."""
    instances: Dict[Type[Any], Any] = {}

    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    # Preserve original class reference
    get_instance.__wrapped__ = cls
    return get_instance


@singleton
class DatabasePool:
    def __init__(self, connection_str: str):
        self.connection_str = connection_str
        self.query_count = 0

    def query(self, sql: str) -> str:
        self.query_count += 1
        return f"Executing {sql}"


def test_q3_singleton_class_decorator():
    pool1 = DatabasePool("sqlite:///:memory:")
    pool2 = DatabasePool("postgres://localhost:5432/db")  # args ignored on second instantiation

    assert pool1 is pool2
    assert pool1.connection_str == "sqlite:///:memory:"

    pool1.query("SELECT 1")
    pool2.query("SELECT 2")
    assert pool1.query_count == 2
    assert pool2.query_count == 2
    print("=== Q3: Singleton Class Decorator Verified ===")


# ==============================================================================
# Question 4: Class Registry Pattern Decorator
# ==============================================================================
PARSER_REGISTRY: Dict[str, Type[Any]] = {}


def register_parser(format_name: str):
    """Class decorator registering the target parser class into PARSER_REGISTRY."""
    def decorator(cls: Type[Any]) -> Type[Any]:
        fmt = format_name.lower()
        if fmt in PARSER_REGISTRY:
            raise KeyError(f"Parser format '{fmt}' already registered")
        PARSER_REGISTRY[fmt] = cls
        cls.format_name = fmt
        return cls
    return decorator


@register_parser("json")
class JsonParser:
    def parse(self, text: str) -> Any:
        return json.loads(text)


@register_parser("csv")
class CsvParser:
    def parse(self, text: str) -> List[List[str]]:
        return [line.split(",") for line in text.strip().splitlines()]


def test_q4_class_registry():
    assert "json" in PARSER_REGISTRY
    assert "csv" in PARSER_REGISTRY
    assert PARSER_REGISTRY["json"] is JsonParser

    parser = PARSER_REGISTRY["json"]()
    data = parser.parse('{"status": "ok"}')
    assert data == {"status": "ok"}

    try:
        @register_parser("json")
        class DuplicateParser:
            pass
        assert False, "Should raise KeyError for duplicate parser"
    except KeyError as exc:
        assert "already registered" in str(exc)
    print("=== Q4: Class Registry Decorator Verified ===")


# ==============================================================================
# Question 5: Class-Based Decorator (Stateful via __call__)
# ==============================================================================
class CallLimiter:
    """Decorator implemented as a class that limits total invocations to max_calls."""
    def __init__(self, func: Callable):
        self.func = func
        self.calls = 0
        self.max_calls = 3
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        if self.calls >= self.max_calls:
            raise RuntimeError(f"Function '{self.func.__name__}' exceeded max calls ({self.max_calls})")
        self.calls += 1
        return self.func(*args, **kwargs)


@CallLimiter
def secure_token_generator(prefix: str) -> str:
    return f"{prefix}_token"


def test_q5_class_based_decorator():
    assert secure_token_generator.calls == 0
    assert secure_token_generator("AUTH") == "AUTH_token"
    assert secure_token_generator("SESSION") == "SESSION_token"
    assert secure_token_generator("REFRESH") == "REFRESH_token"
    assert secure_token_generator.calls == 3

    try:
        secure_token_generator("FAIL")
        assert False, "Should raise RuntimeError"
    except RuntimeError as e:
        assert "exceeded max calls" in str(e)
    print("=== Q5: Class-Based Decorator (__call__) Verified ===")


# ==============================================================================
# Question 6: Parameterized Class-Based Decorator with Custom Options
# ==============================================================================
class CacheWithTTL:
    """
    Class-based parameterized decorator.
    __init__ accepts options, and __call__ accepts the target function.
    """
    def __init__(self, default_value: Any = None):
        self.default_value = default_value
        self.cache: Dict[Tuple[Any, ...], Any] = {}

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args):
            if args in self.cache:
                return self.cache[args]
            try:
                res = func(*args)
            except Exception:
                res = self.default_value
            self.cache[args] = res
            return res

        wrapper.cache = self.cache
        return wrapper


@CacheWithTTL(default_value="FALLBACK")
def safe_calculator(x: int, y: int) -> str:
    if y == 0:
        raise ZeroDivisionError("division by zero")
    return f"Result: {x // y}"


def test_q6_parameterized_class_decorator():
    # Successful calculation
    assert safe_calculator(10, 2) == "Result: 5"
    assert (10, 2) in safe_calculator.cache

    # Fallback upon error
    assert safe_calculator(10, 0) == "FALLBACK"
    assert safe_calculator(10, 0) == "FALLBACK"  # cached fallback
    print("=== Q6: Parameterized Class Decorator Verified ===")


# ==============================================================================
# Question 7: Auto-Tracing Class Decorator
# ==============================================================================
def trace_all_methods(cls: Type[Any]) -> Type[Any]:
    """
    Class decorator that automatically instruments all public callable methods
    with execution logging attached to cls._method_call_log.
    """
    cls._method_call_log = []

    for name, attr in list(cls.__dict__.items()):
        if callable(attr) and not name.startswith("_"):
            def make_wrapper(orig_method, method_name):
                @functools.wraps(orig_method)
                def method_wrapper(self, *args, **kwargs):
                    cls._method_call_log.append(f"{cls.__name__}.{method_name}")
                    return orig_method(self, *args, **kwargs)
                return method_wrapper

            setattr(cls, name, make_wrapper(attr, name))
    return cls


@trace_all_methods
class BankAccount:
    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> float:
        self.balance += amount
        return self.balance

    def withdraw(self, amount: float) -> float:
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        return self.balance


def test_q7_auto_tracing_class_decorator():
    account = BankAccount("Alice", 100.0)
    account.deposit(50.0)
    account.withdraw(30.0)

    assert account.balance == 120.0
    assert BankAccount._method_call_log == ["BankAccount.deposit", "BankAccount.withdraw"]
    print("=== Q7: Auto-Tracing Class Decorator Verified ===")


# ==============================================================================
# Question 8: Method Decorators and Descriptor Protocol (__get__)
# ==============================================================================
class MethodCounter:
    """
    Class-based decorator that works on methods by implementing the descriptor
    protocol (__get__), binding instance properly so 'self' is passed correctly.
    """
    def __init__(self, func: Callable):
        self.func = func
        self.calls = 0
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.func(*args, **kwargs)

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        # Bind the method to the specific instance using MethodType
        return types.MethodType(self, instance)


class OrderProcessor:
    def __init__(self, store_name: str):
        self.store_name = store_name

    @MethodCounter
    def process(self, order_id: str) -> str:
        return f"{self.store_name} processed {order_id}"


def test_q8_method_counter_descriptor():
    p1 = OrderProcessor("AcmeStore")
    res1 = p1.process("ORD_001")
    assert res1 == "AcmeStore processed ORD_001"

    # Counter on descriptor class
    assert OrderProcessor.process.calls == 1
    p1.process("ORD_002")
    assert OrderProcessor.process.calls == 2
    print("=== Q8: Method Decorator with Descriptor Protocol (__get__) Verified ===")


# ==============================================================================
# Question 9: Interface Augmentation Class Decorator
# ==============================================================================
def serializable(cls: Type[Any]) -> Type[Any]:
    """
    Class decorator injecting to_dict(), to_json(), and from_dict() into the target class.
    """
    def to_dict(self) -> Dict[str, Any]:
        return {
            k: v for k, v in self.__dict__.items()
            if not k.startswith("_")
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)

    @classmethod
    def from_dict(klass, data: Dict[str, Any]):
        instance = klass.__new__(klass)
        instance.__dict__.update(data)
        return instance

    cls.to_dict = to_dict
    cls.to_json = to_json
    cls.from_dict = from_dict
    return cls


@serializable
class EmployeeProfile:
    def __init__(self, emp_id: str, name: str, role: str):
        self.emp_id = emp_id
        self.name = name
        self.role = role


def test_q9_interface_augmentation():
    emp = EmployeeProfile("E101", "Alice Smith", "Staff Engineer")
    d = emp.to_dict()
    assert d == {"emp_id": "E101", "name": "Alice Smith", "role": "Staff Engineer"}

    j = emp.to_json()
    assert '"emp_id": "E101"' in j
    assert '"name": "Alice Smith"' in j

    # Reconstitute from dict
    emp_reconstituted = EmployeeProfile.from_dict({"emp_id": "E102", "name": "Bob", "role": "Manager"})
    assert isinstance(emp_reconstituted, EmployeeProfile)
    assert emp_reconstituted.emp_id == "E102"
    assert emp_reconstituted.name == "Bob"
    print("=== Q9: Interface Augmentation Class Decorator Verified ===")


# ==============================================================================
# Question 10: Architectural System: Dependency Injection (DI) Container
# ==============================================================================
class DIContainer:
    """Production dependency injection container managing lifecycles and resolution."""
    def __init__(self):
        self._registry: Dict[str, Dict[str, Any]] = {}
        self._singletons: Dict[str, Any] = {}

    def service(self, name: Optional[str] = None, lifecycle: str = "singleton"):
        """Class decorator registering class into DI container."""
        def decorator(cls: Type[Any]) -> Type[Any]:
            key = name or cls.__name__
            self._registry[key] = {"class": cls, "lifecycle": lifecycle}
            return cls
        return decorator

    def resolve(self, key: str) -> Any:
        if key not in self._registry:
            raise KeyError(f"Service '{key}' not registered in DI container")

        entry = self._registry[key]
        if entry["lifecycle"] == "singleton":
            if key not in self._singletons:
                # Instantiate dependencies if needed (default zero-arg constructor here)
                self._singletons[key] = entry["class"]()
            return self._singletons[key]
        else:
            return entry["class"]()

    def inject(self, func: Callable) -> Callable:
        """
        Function decorator inspecting parameters and automatically resolving
        unsupplied parameters matching registered service names.
        """
        sig = inspect.signature(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bound_args = sig.bind_partial(*args, **kwargs)
            for param_name, param in sig.parameters.items():
                if param_name not in bound_args.arguments and param_name in self._registry:
                    bound_args.arguments[param_name] = self.resolve(param_name)
            return func(*bound_args.args, **bound_args.kwargs)

        return wrapper


di = DIContainer()


@di.service(name="logger", lifecycle="singleton")
class SystemLogger:
    def __init__(self):
        self.logs: List[str] = []

    def log(self, msg: str):
        self.logs.append(msg)


@di.service(name="hasher", lifecycle="transient")
class HashService:
    def hash_text(self, val: str) -> str:
        return f"hash_{hash(val)}"


@di.inject
def authenticate_user(username: str, password_raw: str, logger: SystemLogger = None, hasher: HashService = None) -> Dict[str, Any]:
    logger.log(f"Authenticating user {username}")
    token = hasher.hash_text(password_raw)
    return {"user": username, "token": token}


def test_q10_di_container():
    # Call without passing logger or hasher -> auto-injected
    result1 = authenticate_user("alice", "secret123")
    assert result1["user"] == "alice"
    assert result1["token"].startswith("hash_")

    logger_instance = di.resolve("logger")
    assert len(logger_instance.logs) == 1
    assert "Authenticating user alice" in logger_instance.logs[0]

    # Verify singleton vs transient lifecycle
    l1 = di.resolve("logger")
    l2 = di.resolve("logger")
    assert l1 is l2  # singleton

    h1 = di.resolve("hasher")
    h2 = di.resolve("hasher")
    assert h1 is not h2  # transient produces new instances
    print("=== Q10: Architectural Dependency Injection Container Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_parameterized_decorator_factory()
    test_q2_dual_use_decorator()
    test_q3_singleton_class_decorator()
    test_q4_class_registry()
    test_q5_class_based_decorator()
    test_q6_parameterized_class_decorator()
    test_q7_auto_tracing_class_decorator()
    test_q8_method_counter_descriptor()
    test_q9_interface_augmentation()
    test_q10_di_container()
    print("\nAll 10 class and parameterized decorator practice questions passed successfully!")
