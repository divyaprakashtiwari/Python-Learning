"""
Topic 05: Object-Oriented Programming (OOP)
Question 06: Encapsulation (Deep Dive)

Master data hiding, access conventions, and boundary integrity in Python:
- Access levels: public, protected (_single_underscore), and private (__double_underscore)
- Name mangling mechanics (_ClassName__attribute) and subclass collision avoidance
- Preventing accidental override of internal helpers via name mangling
- Pythonic properties (@property) vs traditional getter/setter methods
- Enforcing domain invariants and validation rules in setters
- Defensive copying of internal mutable collections to preserve state integrity
- Write-once (immutable) entity attributes
- The Facade pattern: encapsulating multi-component subsystems
- Private methods and internal algorithm modularization
- Production-grade Secure Key Vault entity with auto-masking and access audit logs
"""

import copy
import time
from typing import Any, Dict, List, Optional, Tuple


# ============================================================
# Q1: Public, Protected (_), and Private (__) Conventions
# ============================================================
# Question: Define a class showcasing public, protected (_single_underscore),
# and private (__double_underscore) attributes. Explain Python's "consenting adults" philosophy.

print("=== Q1: Public, Protected, and Private Conventions ===")

class UserAccount:
    def __init__(self, username: str, email: str, pin: str):
        self.username = username      # Public: free access anywhere
        self._email = email          # Protected: internal convention; subclasses & module
        self.__pin = pin             # Private: name-mangled to prevent accidental access

    def verify_pin(self, candidate_pin: str) -> bool:
        """Authorized public method to verify private PIN."""
        return self.__pin == candidate_pin

user = UserAccount("alice", "alice@corp.org", "4321")

# Public access works directly
print(f"  Public username:    {user.username}")
assert user.username == "alice"

# Protected access works (Python does not block it, but convention advises caution)
print(f"  Protected _email:   {user._email}")
assert user._email == "alice@corp.org"

# Private access directly raises AttributeError
caught_attr_error = False
try:
    print(user.__pin)  # type: ignore
except AttributeError as err:
    caught_attr_error = True
    print(f"  Caught expected AttributeError on direct private access: {err}")

assert caught_attr_error
assert user.verify_pin("4321") is True

# Explanation: Python does not have compiler-enforced access modifiers (`public`, `private`).
# A single underscore `_var` is an agreed convention meaning "internal implementation".
# A double underscore `__var` triggers name mangling.


# ============================================================
# Q2: Name Mangling Mechanics (_ClassName__attribute)
# ============================================================
# Question: Inspect the instance's `__dict__` to observe how Python rewrites `__pin`
# to `_UserAccount__pin`. Demonstrate how mangled names can still be accessed if necessary.

print("\n=== Q2: Name Mangling Mechanics ===")

# Inspect the dictionary keys of the instance
instance_keys = list(user.__dict__.keys())
print(f"  Instance __dict__ keys: {instance_keys}")

assert "username" in user.__dict__
assert "_email" in user.__dict__
assert "__pin" not in user.__dict__
assert "_UserAccount__pin" in user.__dict__

# Accessing the mangled attribute directly
mangled_pin = getattr(user, "_UserAccount__pin")
print(f"  Mangled access (_UserAccount__pin): '{mangled_pin}'")
assert mangled_pin == "4321"

# Explanation: Any identifier with leading double underscores (and at most one trailing underscore)
# is textually replaced by the compiler with `_ClassName__identifier`.
# The purpose is to prevent name collisions in inheritance, not security obfuscation.


# ============================================================
# Q3: Preventing Subclass Collision via Name Mangling
# ============================================================
# Question: Demonstrate how name mangling protects internal base class setup methods
# from being accidentally overridden and broken by a subclass defining a method with the same name.

print("\n=== Q3: Preventing Subclass Collision via Name Mangling ===")

class BaseWorker:
    def __init__(self):
        # Calls private __setup()
        self.__setup()

    def __setup(self):
        self.state = "BASE_INITIALIZED"

    def get_base_state(self) -> str:
        return self.state

class SubWorker(BaseWorker):
    def __init__(self):
        super().__init__()
        # Subclass defines its own __setup() without knowing BaseWorker has one!
        self.__setup()

    def __setup(self):
        self.sub_state = "SUB_INITIALIZED"

worker = SubWorker()
print(f"  BaseWorker state: {worker.get_base_state()}")
print(f"  SubWorker state:  {worker.sub_state}")

# In __dict__, both methods co-exist harmlessly under different mangled names!
assert worker.get_base_state() == "BASE_INITIALIZED"
assert worker.sub_state == "SUB_INITIALIZED"
assert "_BaseWorker__setup" in dir(worker)
assert "_SubWorker__setup" in dir(worker)

# Explanation: Without name mangling, `SubWorker.__setup` would override `BaseWorker.__setup`,
# potentially corrupting base class initialization. Name mangling guarantees private isolation.


# ============================================================
# Q4: Pythonic Properties vs Java-Style Getters and Setters
# ============================================================
# Question: Contrast Java-style `get_temperature()` / `set_temperature()` methods with
# Python's idiomatic `@property` and `@prop.setter` decorators.

print("\n=== Q4: Pythonic Properties vs Java Getters/Setters ===")

class CelsiusTemperature:
    def __init__(self, initial_celsius: float = 0.0):
        self._celsius = float(initial_celsius)

    # Pythonic Getter
    @property
    def celsius(self) -> float:
        return self._celsius

    # Pythonic Setter with validation
    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError(f"Temperature {value} C is below absolute zero (-273.15 C)!")
        self._celsius = round(float(value), 2)

    # Derived read-only property computed on the fly
    @property
    def fahrenheit(self) -> float:
        return round((self._celsius * 9.0 / 5.0) + 32.0, 2)

temp = CelsiusTemperature(25.0)
print(f"  Initial temperature: {temp.celsius} C ({temp.fahrenheit} F)")
assert temp.celsius == 25.0
assert temp.fahrenheit == 77.0

# Natural assignment syntax executes setter logic
temp.celsius = 100.0
print(f"  After boiling update:{temp.celsius} C ({temp.fahrenheit} F)")
assert temp.celsius == 100.0
assert temp.fahrenheit == 212.0

# Setting below absolute zero triggers validation error
caught_abs_zero = False
try:
    temp.celsius = -300.0
except ValueError as err:
    caught_abs_zero = True
    print(f"  Caught expected boundary error: {err}")

assert caught_abs_zero

# Explanation: `@property` provides clean, dot-syntax attribute access while transparently
# encapsulating getters, setters, and boundary validation under the hood.


# ============================================================
# Q5: Enforcing Domain Invariants & Validation
# ============================================================
# Question: Implement an `EmployeeSalary` class that enforces business invariants:
# 1) Base salary must be between $30,000 and $500,000
# 2) Raises cannot exceed 25% of current salary in a single revision

print("\n=== Q5: Enforcing Domain Invariants ===")

class InvalidSalaryError(ValueError): pass
class ExcessiveRaiseError(ValueError): pass

class EmployeeSalary:
    MIN_SALARY = 30_000.0
    MAX_SALARY = 500_000.0
    MAX_RAISE_PERCENT = 0.25

    def __init__(self, starting_salary: float):
        if not (self.MIN_SALARY <= starting_salary <= self.MAX_SALARY):
            raise InvalidSalaryError(f"Starting salary must be between ${self.MIN_SALARY:,.0f} and ${self.MAX_SALARY:,.0f}")
        self._salary = float(starting_salary)

    @property
    def salary(self) -> float:
        return self._salary

    def apply_raise(self, percentage: float) -> float:
        if percentage <= 0:
            raise ValueError("Raise percentage must be strictly positive")
        if percentage > self.MAX_RAISE_PERCENT:
            raise ExcessiveRaiseError(f"Raise of {percentage*100:.1f}% exceeds max allowed {self.MAX_RAISE_PERCENT*100:.0f}%")

        new_salary = round(self._salary * (1.0 + percentage), 2)
        if new_salary > self.MAX_SALARY:
            raise InvalidSalaryError(f"New salary ${new_salary:,.2f} exceeds ceiling ${self.MAX_SALARY:,.0f}")
        
        self._salary = new_salary
        return self._salary

emp_comp = EmployeeSalary(80_000.0)
emp_comp.apply_raise(0.15)  # 15% raise
print(f"  Salary after 15% raise: ${emp_comp.salary:,.2f}")
assert emp_comp.salary == 92_000.0

# Excessive raise check (30% raise rejected)
caught_excessive = False
try:
    emp_comp.apply_raise(0.30)
except ExcessiveRaiseError as err:
    caught_excessive = True
    print(f"  Caught excessive raise: {err}")

assert caught_excessive

# Explanation: Encapsulation protects business invariants from being corrupted by
# raw attribute writes, routing all mutations through validated domain operations.


# ============================================================
# Q6: Defensive Copying for Mutable Attributes
# ============================================================
# Question: Demonstrate how returning an internal mutable list directly leaks private state,
# allowing external callers to bypass methods. Show the fix: returning defensive copies.

print("\n=== Q6: Defensive Copying of Mutable Collections ===")

class ShoppingCart:
    def __init__(self):
        self._items: List[str] = []

    def add_item(self, item: str) -> None:
        if not item or not isinstance(item, str):
            raise ValueError("Invalid item name")
        self._items.append(item.strip())

    # LEAKY PROPERTY: returning self._items directly allows external callers to append without validation!
    @property
    def leaky_items(self) -> List[str]:
        return self._items

    # DEFENSIVE PROPERTY: returns a shallow or deep copy, protecting internal collection
    @property
    def items(self) -> List[str]:
        return list(self._items)

cart = ShoppingCart()
cart.add_item("Apple")
cart.add_item("Banana")

# Modifying the defensive copy does NOT mutate the shopping cart!
external_list = cart.items
external_list.append("HACKED_ITEM_BYPASSING_VALIDATION")

print(f"  External modified copy: {external_list}")
print(f"  Internal cart items:    {cart.items}")

assert len(cart.items) == 2
assert "HACKED_ITEM_BYPASSING_VALIDATION" not in cart.items

# Explanation: Always return a copy (`list(self._items)` or `tuple(self._items)`)
# when exposing internal mutable collections to preserve encapsulation integrity.


# ============================================================
# Q7: Write-Once / Read-Only Immutable Attributes
# ============================================================
# Question: Implement an entity with write-once attributes (e.g. `uuid`, `created_at`).
# Allow initialization once, but raise `AttributeError` on any subsequent reassignment attempt.

print("\n=== Q7: Write-Once Immutable Attributes ===")

class AuditTransaction:
    def __init__(self, tx_id: str, amount: float):
        self._tx_id = tx_id
        self._amount = amount
        self._created_at = time.time()

    @property
    def tx_id(self) -> str:
        """Read-only property without a setter."""
        return self._tx_id

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def created_at(self) -> float:
        return self._created_at

tx = AuditTransaction("TX-99042", 540.0)
print(f"  Transaction ID: {tx.tx_id}, Amount: ${tx.amount:.2f}")

# Reassigning a read-only property raises AttributeError
caught_immutable_err = False
try:
    tx.tx_id = "NEW_TX_ID"  # type: ignore
except AttributeError as err:
    caught_immutable_err = True
    print(f"  Caught expected AttributeError on read-only attribute: {err}")

assert caught_immutable_err
assert tx.tx_id == "TX-99042"

# Explanation: Omitting the `@prop.setter` decorator turns a property into an immutable,
# read-only attribute, safeguarding identity keys and timestamps.


# ============================================================
# Q8: The Facade Pattern (Encapsulating Complex Subsystems)
# ============================================================
# Question: Implement a `ComputerFacade` that encapsulates the complex multi-step
# initialization of CPU, Memory, and Disk behind a simple `start_computer()` method.

print("\n=== Q8: Facade Pattern ===")

class CPU:
    def freeze(self) -> str: return "CPU frozen"
    def jump(self, position: int) -> str: return f"CPU jumped to 0x{position:X}"
    def execute(self) -> str: return "CPU executing instructions"

class Memory:
    def load(self, position: int, data: str) -> str:
        return f"Loaded '{data}' into RAM at 0x{position:X}"

class HardDrive:
    def read_boot_sector(self) -> str:
        return "BOOT_SECTOR_OS_KERNEL"

class ComputerFacade:
    """Facade: encapsulates multi-subsystem complexity into a single friendly interface."""
    def __init__(self):
        self._cpu = CPU()
        self._memory = Memory()
        self._disk = HardDrive()

    def start(self) -> List[str]:
        boot_log = []
        boot_log.append(self._cpu.freeze())
        boot_data = self._disk.read_boot_sector()
        boot_log.append(self._memory.load(0x00, boot_data))
        boot_log.append(self._cpu.jump(0x00))
        boot_log.append(self._cpu.execute())
        return boot_log

computer = ComputerFacade()
startup_sequence = computer.start()

print("  Computer boot sequence via Facade:")
for step in startup_sequence:
    print(f"    - {step}")

assert len(startup_sequence) == 4
assert startup_sequence[0] == "CPU frozen"
assert "BOOT_SECTOR_OS_KERNEL" in startup_sequence[1]

# Explanation: The Facade pattern uses encapsulation to hide subsystem complexity,
# providing client code with a simplified, high-level unified interface.


# ============================================================
# Q9: Private Methods & Modular Algorithm Encapsulation
# ============================================================
# Question: Build a `MarkdownParser` class where tokenization, sanitization,
# and link rendering are encapsulated in private helper methods (`_tokenize`, `_sanitize`),
# exposing only a single public `parse(markdown_text)` entry point.

print("\n=== Q9: Private Methods & Algorithm Modularization ===")

class MarkdownParser:
    def parse(self, raw_markdown: str) -> str:
        """Single public entry point."""
        sanitized = self._sanitize_html(raw_markdown)
        with_headers = self._parse_headers(sanitized)
        with_bold = self._parse_bold(with_headers)
        return with_bold

    def _sanitize_html(self, text: str) -> str:
        """Internal helper: escapes raw HTML script tags."""
        return text.replace("<script>", "").replace("</script>", "")

    def _parse_headers(self, text: str) -> str:
        """Internal helper: converts '# Header' to '<h1>Header</h1>'."""
        lines = []
        for line in text.splitlines():
            if line.startswith("# "):
                lines.append(f"<h1>{line[2:]}</h1>")
            else:
                lines.append(line)
        return "\n".join(lines)

    def _parse_bold(self, text: str) -> str:
        """Internal helper: converts '**text**' to '<b>text</b>'."""
        while "**" in text:
            first_idx = text.find("**")
            second_idx = text.find("**", first_idx + 2)
            if second_idx == -1:
                break
            bold_content = text[first_idx + 2:second_idx]
            text = text[:first_idx] + f"<b>{bold_content}</b>" + text[second_idx + 2:]
        return text

parser = MarkdownParser()
html_output = parser.parse("# Welcome\nThis is **bold** text.")

print("  Parsed HTML Output:")
for line in html_output.splitlines():
    print(f"    {line}")

assert "<h1>Welcome</h1>" in html_output
assert "<b>bold</b>" in html_output

# Explanation: Breaking complex procedures into private helper methods (`_method`)
# improves readability and unit testability while keeping the public interface concise.


# ============================================================
# Q10: Production-Grade Cryptographic Secret & Key Vault Entity
# ============================================================
# Question: Implement a production-grade `SecretKeyVault` entity:
# - Encapsulates raw secret keys with name mangling (`__secrets`)
# - Never reveals plaintext secrets in `__repr__` or `__str__` (auto-masked)
# - Records all retrieval attempts in an immutable access audit log
# - Enforces token authentication for key retrieval

print("\n=== Q10: Secure Key Vault Entity ===")

class UnauthorizedAccessError(PermissionError): pass
class SecretNotFoundError(KeyError): pass

class SecretKeyVault:
    def __init__(self, master_passphrase: str):
        self._master_hash = hash(master_passphrase)
        # Store secrets private with name mangling
        self.__secrets_store: Dict[str, str] = {}
        self._access_log: List[Dict[str, Any]] = []

    def set_secret(self, key_name: str, secret_val: str, passphrase: str) -> None:
        self._authenticate(passphrase)
        self.__secrets_store[key_name] = secret_val
        self._log_access("STORE", key_name, success=True)

    def get_secret(self, key_name: str, passphrase: str) -> str:
        try:
            self._authenticate(passphrase)
            if key_name not in self.__secrets_store:
                raise SecretNotFoundError(f"Key '{key_name}' does not exist")
            self._log_access("READ", key_name, success=True)
            return self.__secrets_store[key_name]
        except Exception as exc:
            self._log_access("READ", key_name, success=False, error=str(exc))
            raise

    def _authenticate(self, passphrase: str) -> None:
        if hash(passphrase) != self._master_hash:
            raise UnauthorizedAccessError("Invalid master passphrase")

    def _log_access(self, action: str, key_name: str, success: bool, error: Optional[str] = None) -> None:
        self._access_log.append({
            "action": action,
            "key": key_name,
            "success": success,
            "error": error,
            "timestamp": "2026-10-17"
        })

    @property
    def audit_trail(self) -> List[Dict[str, Any]]:
        """Defensive copy of access audit records."""
        return [dict(entry) for entry in self._access_log]

    def __repr__(self) -> str:
        # Crucial security practice: Never expose secrets in __repr__ or __str__!
        keys_summary = ", ".join(f"{k}: '***REDACTED***'" for k in sorted(self.__secrets_store.keys()))
        return f"SecretKeyVault(stored_keys=[{keys_summary}])"

vault = SecretKeyVault(master_passphrase="SuperSecretVaultPass123!")
vault.set_secret("STRIPE_KEY", "sk_live_994821a8c", "SuperSecretVaultPass123!")
vault.set_secret("DATABASE_PASSWORD", "DbPass#2026!", "SuperSecretVaultPass123!")

# Read valid secret
retrieved_stripe = vault.get_secret("STRIPE_KEY", "SuperSecretVaultPass123!")
print(f"  Retrieved valid secret: {retrieved_stripe[:7]}...")
assert retrieved_stripe == "sk_live_994821a8c"

# Test masked string representation
vault_repr = repr(vault)
print(f"  Vault repr (Masked): {vault_repr}")
assert "***REDACTED***" in vault_repr
assert "sk_live" not in vault_repr

# Test unauthorized read attempt
caught_auth_err = False
try:
    vault.get_secret("STRIPE_KEY", "WRONG_PASSWORD")
except UnauthorizedAccessError:
    caught_auth_err = True

assert caught_auth_err
assert len(vault.audit_trail) == 4
assert vault.audit_trail[-1]["success"] is False

print("\nAll 10 encapsulation questions executed and asserted successfully!")
