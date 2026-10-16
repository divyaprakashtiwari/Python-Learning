"""
Topic 01: Python Basics
Question 10: Constants, Naming Conventions, and Scope (Deep Dive)

Master Python's naming conventions (PEP 8), constant patterns,
variable scoping rules (LEGB), namespace inspection, keywords, and identifier rules.
"""

import sys
import builtins
import keyword
from typing import Final, NamedTuple
from dataclasses import dataclass

# ============================================================
# Q1: PEP 8 Naming Conventions and Validator
# ============================================================
# Question: Demonstrate PEP 8 naming conventions for all standard Python
# constructs and build a validator function to verify identifier style compliance.

print("=== Q1: PEP 8 Naming Conventions ===")

# Standard PEP 8 conventions:
# 1. Variables & Functions:   snake_case (all lowercase with underscores)
# 2. Constants:               SCREAMING_SNAKE_CASE (all uppercase with underscores)
# 3. Classes:                 PascalCase / CapWords (CamelCase starting with uppercase)
# 4. Modules:                 short_lowercase (underscores discouraged unless needed)
# 5. Packages:                short_lowercase (no underscores)
# 6. Protected attributes:    _single_leading_underscore
# 7. Private / Mangled:       __double_leading_underscore
# 8. Reserved keyword clash:  single_trailing_underscore_ (e.g., class_, type_)

def is_snake_case(name: str) -> bool:
    """Check if name is snake_case (e.g., user_profile_count)."""
    return name.islower() and not name.startswith("_") and not name.endswith("_") and ("_" in name or name.isalpha())

def is_screaming_snake(name: str) -> bool:
    """Check if name is SCREAMING_SNAKE_CASE (e.g., MAX_RETRY_COUNT)."""
    return name.isupper() and ("_" in name or name.isalpha())

def is_pascal_case(name: str) -> bool:
    """Check if name is PascalCase (e.g., DatabaseConnection)."""
    return name[0].isupper() and "_" not in name and not name.isupper()

def validate_identifier_style(identifier: str) -> dict:
    """Analyze an identifier and classify its PEP 8 naming style."""
    if not identifier.isidentifier():
        return {"identifier": identifier, "valid_syntax": False, "style": "INVALID_SYNTAX"}
    
    style = "UNKNOWN"
    if identifier.startswith("__") and identifier.endswith("__"):
        style = "DUNDER_MAGIC (Special Python method)"
    elif identifier.startswith("__"):
        style = "PRIVATE_MANGLED (__name)"
    elif identifier.startswith("_"):
        style = "INTERNAL_PROTECTED (_name)"
    elif identifier.endswith("_"):
        style = "KEYWORD_COLLISION_AVOIDANCE (name_)"
    elif is_screaming_snake(identifier):
        style = "CONSTANT (SCREAMING_SNAKE_CASE)"
    elif is_pascal_case(identifier):
        style = "CLASS_NAME (PascalCase)"
    elif is_snake_case(identifier):
        style = "VARIABLE_OR_FUNCTION (snake_case)"
    
    return {"identifier": identifier, "valid_syntax": True, "style": style}

test_names = [
    "user_account_id",
    "MAX_CONNECTIONS",
    "HttpRequestHandler",
    "_internal_cache",
    "__private_key",
    "class_",
    "__init__",
    "2nd_attempt",
]

for name in test_names:
    result = validate_identifier_style(name)
    status = "OK" if result["valid_syntax"] else "SYNTAX ERROR"
    print(f"  [{status:<12}] {name:<22} -> {result['style']}")

# Explanation: PEP 8 provides naming guidelines to maintain readability across codebases.
# Python allows identifiers matching [a-zA-Z_][a-zA-Z0-9_]*, but conventions convey intent.


# ============================================================
# Q2: Simulating Constants in Python
# ============================================================
# Question: Python lacks a `const` keyword. Demonstrate three distinct patterns
# to implement constants: typing.Final, a custom immutable namespace, and frozen dataclasses.

print("\n=== Q2: Simulating Constants ===")

# Approach 1: typing.Final (Type Checker level - Python 3.8+)
MAX_BUFFER_SIZE: Final[int] = 4096
API_TIMEOUT_SECONDS: Final[float] = 30.0
print(f"  typing.Final hint: MAX_BUFFER_SIZE = {MAX_BUFFER_SIZE}")
# Note: Python does NOT raise a runtime error if modified, but linters (mypy) flag it.

# Approach 2: Custom Constant container with runtime enforcement via __setattr__
class _ConstNamespace:
    """Container that forbids attribute mutation or re-assignment at runtime."""
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            super().__setattr__(k, v)
        self._locked = True

    def __setattr__(self, key, value):
        if getattr(self, "_locked", False):
            raise AttributeError(f"Cannot reassign constant '{key}' (Constants are immutable)")
        super().__setattr__(key, value)

    def __delattr__(self, key):
        raise AttributeError(f"Cannot delete constant '{key}'")

AppConst = _ConstNamespace(
    PI=3.141592653589793,
    DEFAULT_PORT=8080,
    ENVIRONMENT="production"
)

print(f"  Runtime Constant: AppConst.DEFAULT_PORT = {AppConst.DEFAULT_PORT}")
try:
    AppConst.DEFAULT_PORT = 9000
except AttributeError as e:
    print(f"  Runtime enforcement caught: {e}")

# Approach 3: Frozen Dataclass (Clean, Pythonic, and Immutable)
@dataclass(frozen=True)
class DatabaseConstants:
    HOST: str = "localhost"
    PORT: int = 5432
    MAX_POOL_SIZE: int = 20

db_cfg = DatabaseConstants()
print(f"  Frozen Dataclass: {db_cfg.HOST}:{db_cfg.PORT}")
try:
    db_cfg.PORT = 3306  # type: ignore
except Exception as e:
    print(f"  Frozen dataclass caught mutation: {type(e).__name__}: {e}")

# Explanation: While uppercase names are convention-only, runtime protection can be
# achieved via frozen dataclasses or custom descriptors/__setattr__ overrides.


# ============================================================
# Q3: Python Keywords and Built-in Shadowing
# ============================================================
# Question: Identify Python reserved keywords, show why shadowing built-ins
# causes subtle bugs, and demonstrate how to recover original built-ins safely.

print("\n=== Q3: Keywords and Built-in Shadowing ===")

# Total keywords in current Python runtime
print(f"  Python version: {sys.version.split()[0]}")
print(f"  Total reserved keywords: {len(keyword.kwlist)}")
print(f"  Sample keywords: {keyword.kwlist[:10]}")
print(f"  Soft keywords (match/case): {keyword.softkwlist}")

# Test if word is a keyword
for word in ["def", "class", "async", "variable", "yield", "goto"]:
    is_kw = keyword.iskeyword(word)
    print(f"    keyword.iskeyword('{word}'): {is_kw}")

# Built-in shadowing danger demonstration
def demonstrate_shadowing():
    # Bad practice: naming a variable 'list' or 'str'
    my_nums = [1, 2, 3]
    
    # Shadowing the built-in 'sum'
    sum_orig = sum(my_nums)
    print(f"\n  Original sum([1, 2, 3]) = {sum_orig}")
    
    # Intentionally shadow locally
    sum_val = 100  # Good name
    # If someone did: sum = 100
    # Then calling sum([4, 5]) raises TypeError: 'int' object is not callable
    
    # Recovering a shadowed built-in:
    # Always access via the 'builtins' module
    safe_sum = builtins.sum(my_nums)
    print(f"  Recovered built-in call: builtins.sum(my_nums) = {safe_sum}")

demonstrate_shadowing()

# Explanation: Python searches local -> enclosing -> global -> built-in (LEGB).
# If you name a variable `id`, `type`, `sum`, `list`, or `dict`, you hide the built-in
# within that scope. Access `builtins.<name>` to bypass local/global shadowing.


# ============================================================
# Q4: The LEGB Scoping Rule in Depth
# ============================================================
# Question: Write a program that clearly demonstrates each step of the
# LEGB lookup hierarchy: Local, Enclosing, Global, and Built-in.

print("\n=== Q4: The LEGB Scoping Rule ===")

# 1. Built-in scope: len is in builtins
# 2. Global scope:
x_scope = "G: Global Scope"

def outer_function():
    # 3. Enclosing scope:
    x_scope = "E: Enclosing Scope"
    
    def inner_function():
        # 4. Local scope:
        x_scope = "L: Local Scope"
        return f"    Inside inner(): {x_scope}"
    
    def inner_without_local():
        # Falls back to Enclosing
        return f"    Inside inner_without_local(): {x_scope}"

    print(inner_function())
    print(inner_without_local())

def outer_without_enclosing():
    def inner():
        # Falls back to Global
        return f"    Inside outer_without_enclosing(): {x_scope}"
    print(inner())

outer_function()
outer_without_enclosing()
print(f"    Module level: {x_scope}")

# Inspecting locals() and globals()
def inspect_namespaces(param_a, param_b="default"):
    local_calc = param_a * 2
    local_dict = locals()
    print("\n  Locals dictionary inside inspect_namespaces():")
    for k, v in local_dict.items():
        print(f"    {k} = {v!r}")

inspect_namespaces(21)

# Explanation: Python searches names from the inside out: Local first, then Enclosing
# functions, then Module Global, then Built-ins. It stops at the first match.


# ============================================================
# Q5: The `global` Keyword and Variable Modification
# ============================================================
# Question: Demonstrate the `UnboundLocalError` caused by assignment before `global`,
# how `global` resolves it, and why returning new state is preferred over `global`.

print("\n=== Q5: The global Keyword ===")

global_counter = 0

def buggy_increment():
    """Demonstrates UnboundLocalError when modifying global without declaring it."""
    try:
        # global_counter += 1
        # Python sees assignment 'global_counter = ...', marks it as LOCAL,
        # but reads it before assignment!
        exec("global_counter += 1")
    except NameError as e:
        print(f"  Caught expected error without global: {e}")

buggy_increment()

def correct_global_increment():
    """Correctly mutates global counter using the global keyword."""
    global global_counter
    global_counter += 1
    return global_counter

print(f"  After correct_global_increment(): global_counter = {correct_global_increment()}")

# Best Practice: Functional approach without mutating global state
def functional_increment(current_count: int, step: int = 1) -> int:
    """Pure function: takes value, returns new value without side effects."""
    return current_count + step

app_state = 10
app_state = functional_increment(app_state, 5)
print(f"  Pure functional increment result: {app_state}")

# Explanation: In Python, if a variable is assigned anywhere within a function,
# it is treated as local throughout that entire function unless explicitly declared `global`.


# ============================================================
# Q6: The `nonlocal` Keyword in Closures
# ============================================================
# Question: Build a stateful counter using closures and the `nonlocal` keyword.
# Contrast `nonlocal` with `global` and demonstrate the error when no enclosing variable exists.

print("\n=== Q6: The nonlocal Keyword in Closures ===")

def create_counter(start: int = 0, step: int = 1):
    """Factory returning a stateful counter closure with nonlocal access."""
    count = start
    history = []
    
    def increment():
        nonlocal count  # Binds to 'count' in immediate enclosing scope
        count += step
        history.append(count)
        return count
    
    def decrement():
        nonlocal count
        count -= step
        history.append(count)
        return count
    
    def get_stats():
        return {"current": count, "history": list(history)}
    
    return increment, decrement, get_stats

inc, dec, stats = create_counter(100, 10)
print(f"  Initial state: {stats()}")
print(f"  inc(): {inc()}")
print(f"  inc(): {inc()}")
print(f"  dec(): {dec()}")
print(f"  Final stats: {stats()}")

# Comparison:
# global: binds to top-level module scope
# nonlocal: binds to the nearest enclosing scope (excluding global and built-in)

try:
    code = """
def test():
    nonlocal orphan_var
    orphan_var = 1
"""
    compile(code, "<string>", "exec")
except SyntaxError as e:
    print(f"  SyntaxError when nonlocal has no enclosing binding: {e.msg}")

# Explanation: `nonlocal` allows nested functions to modify variables defined in
# outer (enclosing) functions without polluting global module namespace.


# ============================================================
# Q7: Variable Deletion and Lifecycle (`del` and Reference Count)
# ============================================================
# Question: Explain what the `del` statement really does in Python.
# Show how `del` unbinds names and how `sys.getrefcount` tracks references.

print("\n=== Q7: Variable Lifecycle and del ===")

# Create a shared list object
original_list = [10, 20, 30]
alias_list = original_list

print(f"  original_list id: {id(original_list)}")
print(f"  alias_list id:    {id(alias_list)}")
# Note: sys.getrefcount includes the temporary reference passed to getrefcount itself (+1)
print(f"  Reference count to object: {sys.getrefcount(original_list) - 1}")

# Delete the variable name 'original_list'
del original_list

# Does the object still exist? YES, because alias_list still references it!
print(f"  After 'del original_list', alias_list is still intact: {alias_list}")
print(f"  Reference count now: {sys.getrefcount(alias_list) - 1}")

# Attempting to access deleted variable raises NameError
try:
    print(original_list)  # type: ignore
except NameError as e:
    print(f"  Accessing original_list caught: {e}")

# Deleting items from a mutable container
data_map = {"host": "localhost", "port": 8080, "debug": True}
del data_map["debug"]
print(f"  After 'del data_map[\"debug\"]': {data_map}")

# Explanation: `del var` does NOT destroy the object directly; it removes the *binding*
# of `var` from the current namespace. The memory is reclaimed by the garbage collector
# only when the object's reference count drops to 0.


# ============================================================
# Q8: Name Mangling and Leading/Trailing Underscores
# ============================================================
# Question: Demonstrate the differences between `_single_leading`, `__double_leading`
# (name mangling), `single_trailing_`, and `__dunder__`.

print("\n=== Q8: Underscore Conventions and Name Mangling ===")

class BankAccount:
    """Class showcasing the 4 distinct underscore naming conventions."""
    
    # Public attribute
    account_holder: str
    
    # 1. Single leading underscore: internal convention (non-public)
    _internal_routing_code: str = "ROUT-9921"
    
    # 2. Double leading underscore: private with NAME MANGLING
    __secret_pin: str = "7412"
    
    def __init__(self, holder: str, balance: float):
        self.account_holder = holder
        self._balance = balance
        self.__secret_pin = "4321"

    # 3. Dunder: Python special methods
    def __repr__(self):
        return f"BankAccount(holder={self.account_holder!r}, balance={self._balance})"
    
    # 4. Trailing underscore: avoid clash with Python keyword 'format' or 'id'
    def audit_entry(self, id_: int, format_: str = "json") -> str:
        return f"Audit[ID={id_}, fmt={format_}]"

account = BankAccount("Alice", 5000.0)
print(f"  Account repr: {account}")
print(f"  Public attribute: {account.account_holder}")
print(f"  Protected attribute (accessible, but discouraged): {account._internal_routing_code}")

# Accessing private attribute directly fails
try:
    print(account.__secret_pin)  # type: ignore
except AttributeError as e:
    print(f"  Direct private access raised: {e}")

# Accessing via mangled name: _ClassName__attributeName
mangled_name = f"_BankAccount__secret_pin"
print(f"  Mangled name access '{mangled_name}': {getattr(account, mangled_name)}")

# Trailing underscore usage
print(f"  Keyword clash resolution method: {account.audit_entry(id_=101, format_='xml')}")

# Explanation:
# - `_var`: purely conventional hint for internal use.
# - `__var`: Python runtime transforms name to `_ClassName__var` to prevent subclass namespace collisions.
# - `var_`: used when the ideal variable name conflicts with a Python keyword (e.g. `class_`, `type_`).
# - `__var__`: reserved exclusively for Python magic dunder protocols.


# ============================================================
# Q9: Typed Configuration Management Pattern
# ============================================================
# Question: Create a production-ready constant configuration system using
# NamedTuple with type safety, defaults, and validation.

print("\n=== Q9: Typed Configuration Pattern ===")

class ServerSettings(NamedTuple):
    host: str = "127.0.0.1"
    port: int = 8000
    workers: int = 4
    reload: bool = False
    allowed_hosts: tuple = ("localhost", "127.0.0.1")

    @classmethod
    def from_dict(cls, config: dict):
        """Factory method with validation and defaults."""
        port = int(config.get("PORT", 8000))
        if not (1 <= port <= 65535):
            raise ValueError(f"Invalid port: {port}")
        
        workers = int(config.get("WORKERS", 4))
        if workers < 1:
            raise ValueError(f"Workers must be >= 1, got {workers}")
            
        return cls(
            host=str(config.get("HOST", "127.0.0.1")),
            port=port,
            workers=workers,
            reload=bool(config.get("RELOAD", False)),
            allowed_hosts=tuple(config.get("ALLOWED_HOSTS", ["localhost"])),
        )

# Create instances
default_cfg = ServerSettings()
print(f"  Default settings: {default_cfg}")

# Immutability verification
try:
    default_cfg.port = 9000  # type: ignore
except AttributeError as e:
    print(f"  NamedTuple immutability caught: {e}")

# Build from simulated environment dictionary
raw_env = {"HOST": "0.0.0.0", "PORT": "8443", "WORKERS": "8", "RELOAD": "True"}
prod_cfg = ServerSettings.from_dict(raw_env)
print(f"  Loaded from dict: Host={prod_cfg.host}, Port={prod_cfg.port}, Workers={prod_cfg.workers}")

# Explanation: NamedTuples are lightweight, immutable, fully type-annotated, and support
# dot-access without the overhead of heavy third-party configuration libraries.


# ============================================================
# Q10: Python Code Identifier Linter and Style Auditor
# ============================================================
# Question: Build a comprehensive identifier style auditor that inspects a list of
# identifiers and flags keyword collisions, built-in shadowing, invalid syntax,
# and non-standard PEP 8 naming.

print("\n=== Q10: Python Identifier Style Auditor ===")

class IdentifierLinter:
    """Lints variable and function names against Python standards and PEP 8."""
    
    # Set of common built-ins that beginners frequently shadow
    SENSITIVE_BUILTINS = {
        "id", "type", "sum", "min", "max", "list", "dict", "set", "str", "int",
        "float", "bool", "len", "open", "input", "print", "format", "range",
        "filter", "map", "all", "any", "dir", "help", "next", "iter"
    }

    def lint(self, identifier: str) -> dict:
        issues = []
        severity = "PASS"
        
        # Check 1: Valid Python identifier syntax
        if not identifier.isidentifier():
            return {
                "name": identifier,
                "status": "ERROR",
                "issues": ["Not a valid Python identifier (illegal characters or starts with digit)"]
            }
        
        # Check 2: Reserved Keyword
        if keyword.iskeyword(identifier):
            return {
                "name": identifier,
                "status": "ERROR",
                "issues": [f"Matches Python reserved keyword '{identifier}' (SyntaxError to assign)"]
            }

        # Check 3: Built-in Shadowing
        if identifier in self.SENSITIVE_BUILTINS:
            issues.append(f"Shadows Python built-in function/type '{identifier}'")
            severity = "WARNING"
            
        # Check 4: Capitalization / Naming conventions
        # CamelCase in variable names (mixedCase without being class)
        if identifier[0].islower() and any(c.isupper() for c in identifier):
            issues.append("Uses camelCase; PEP 8 recommends snake_case for variables and functions")
            severity = "STYLE_WARNING"
            
        # Check 5: Confusing single-character names
        if identifier in ("l", "O", "I"):
            issues.append(f"Single character '{identifier}' easily confused with 1 or 0 (PEP 8 discourages)")
            severity = "WARNING"
            
        if not issues:
            issues.append("Complies with PEP 8 and Python naming rules")

        return {
            "name": identifier,
            "status": severity,
            "issues": issues
        }

linter = IdentifierLinter()

test_identifiers = [
    "user_count",
    "total_price",
    "calculateAverage",
    "list",
    "sum",
    "while",
    "99_problems",
    "MAX_LIMIT",
    "l",
    "valid_var_name"
]

print(f"  {'Identifier':<20} {'Status':<16} {'Notes'}")
print("  " + "-" * 75)
for ident in test_identifiers:
    report = linter.lint(ident)
    notes = "; ".join(report["issues"])
    print(f"  {ident:<20} {report['status']:<16} {notes}")

# Summary Output
print("\n" + "=" * 55)
print("  All 10 Questions for Topic 01 - Q10 executed successfully!")
print("=" * 55)
