"""
Topic 05: Object-Oriented Programming (OOP)
Question 05: Polymorphism (Deep Dive)

Master polymorphism and interface decoupling in Python:
- Duck typing: implicit interface satisfaction without inheritance
- Subtype polymorphism: uniform method dispatch through abstract hierarchies
- Structural subtyping via Protocols (PEP 544 & @runtime_checkable)
- Operator overloading as polymorphic interfaces (__add__, __len__, __getitem__)
- Function overloading via single-dispatch (functools.singledispatch)
- Simulating method polymorphism with defaults and variadic arguments
- Polymorphic collections and uniform processing pipelines
- The Strategy pattern: runtime algorithm swapping via polymorphic classes
- The Adapter pattern: normalizing disparate interfaces to a common protocol
- Production-grade Cloud Storage Manager (AWS S3, GCP Cloud Storage, Local Filesystem)
"""

import functools
from typing import Any, Dict, List, Optional, Protocol, Union, runtime_checkable


# ============================================================
# Q1: Duck Typing (Dynamic Polymorphism)
# ============================================================
# Question: Demonstrate Python's classic "Duck Typing" philosophy.
# Write a function `transmit_payload(sender)` that works with any object that provides
# a `send(data: str)` method, regardless of class inheritance.

print("=== Q1: Duck Typing (Dynamic Polymorphism) ===")

class EmailService:
    def send(self, data: str) -> str:
        return f"[EMAIL] Sent '{data}' via SMTP"

class SmsService:
    def send(self, data: str) -> str:
        return f"[SMS] Dispatched '{data}' via Twilio Gateway"

class MockSender:
    def send(self, data: str) -> str:
        return f"[MOCK] Buffered '{data}' for offline testing"

def transmit_payload(sender: Any, payload: str) -> str:
    # Python doesn't care about the type; only that it provides .send()!
    return sender.send(payload)

res_email = transmit_payload(EmailService(), "Welcome!")
res_sms = transmit_payload(SmsService(), "Your OTP is 9841")
res_mock = transmit_payload(MockSender(), "Telemetry log")

print(f"  Email: {res_email}")
print(f"  SMS:   {res_sms}")
print(f"  Mock:  {res_mock}")

assert "[EMAIL]" in res_email
assert "[SMS]" in res_sms
assert "[MOCK]" in res_mock

# Explanation: "If it walks like a duck and quacks like a duck, it's a duck."
# Duck typing decouples client functions from rigid class inheritance trees.


# ============================================================
# Q2: Subtype Polymorphism (Inheritance-Based)
# ============================================================
# Question: Implement an `AudioPlayer` hierarchy with specialized subclasses:
# `Mp3Player`, `FlacPlayer`, and `WavPlayer`. Demonstrate uniform polymorphic dispatch.

print("\n=== Q2: Subtype Polymorphism ===")

class AudioPlayer:
    def __init__(self, filename: str):
        self.filename = filename

    def play(self) -> str:
        raise NotImplementedError("Subclasses must implement play()")

class Mp3Player(AudioPlayer):
    def play(self) -> str:
        return f"Decoding MP3 frame stream from '{self.filename}'"

class FlacPlayer(AudioPlayer):
    def play(self) -> str:
        return f"Decompressing lossless FLAC audio from '{self.filename}'"

class WavPlayer(AudioPlayer):
    def play(self) -> str:
        return f"Streaming uncompressed PCM WAV data from '{self.filename}'"

playlist: List[AudioPlayer] = [
    Mp3Player("track1.mp3"),
    FlacPlayer("orchestra.flac"),
    WavPlayer("sfx.wav")
]

# Uniform dispatch across the collection
playback_logs = [player.play() for player in playlist]

print("  Playback sequence:")
for log in playback_logs:
    print(f"    {log}")

assert "MP3 frame" in playback_logs[0]
assert "lossless FLAC" in playback_logs[1]
assert "PCM WAV" in playback_logs[2]

# Explanation: Subtype polymorphism allows heterogeneous subclasses sharing a common
# interface to be manipulated uniformly through base class method calls.


# ============================================================
# Q3: Structural Typing via Protocols (PEP 544)
# ============================================================
# Question: Use `typing.Protocol` with `@runtime_checkable` to define an explicit structural
# interface `Serializable`. Verify that any class providing `serialize() -> str` satisfies
# the protocol without inheriting from it.

print("\n=== Q3: Structural Typing with Protocols (PEP 544) ===")

@runtime_checkable
class Serializable(Protocol):
    def serialize(self) -> str:
        """Protocol method: converts entity to string."""
        ...

class UserProfile:
    # Does NOT inherit from Serializable!
    def __init__(self, username: str):
        self.username = username

    def serialize(self) -> str:
        return f'{{"username": "{self.username}"}}'

class DeviceConfig:
    # Does NOT inherit from Serializable!
    def __init__(self, device_id: str, ip: str):
        self.device_id = device_id
        self.ip = ip

    def serialize(self) -> str:
        return f"{self.device_id}@{self.ip}"

class UnserializableObject:
    def __init__(self):
        self.val = 123

u = UserProfile("alice")
d = DeviceConfig("DEV_01", "192.168.1.10")
bad_obj = UnserializableObject()

# Check protocol compliance at runtime via isinstance
print(f"  isinstance(UserProfile, Serializable):    {isinstance(u, Serializable)}")
print(f"  isinstance(DeviceConfig, Serializable):   {isinstance(d, Serializable)}")
print(f"  isinstance(BadObject, Serializable):      {isinstance(bad_obj, Serializable)}")

assert isinstance(u, Serializable)
assert isinstance(d, Serializable)
assert not isinstance(bad_obj, Serializable)

# Explanation: Protocols provide static and runtime duck typing: classes satisfy
# the protocol simply by implementing the requisite methods, without subclassing coupling.


# ============================================================
# Q4: Operator Overloading as Polymorphic Interfaces
# ============================================================
# Question: Implement operator overloading (`+`, `*`, `len()`, `[]`) on a custom `Polynomial` class.
# Show how built-in operators dispatch polymorphically to custom implementations.

print("\n=== Q4: Operator Overloading ===")

class Polynomial:
    def __init__(self, *coefficients: float):
        """Coefficients ordered from lowest degree to highest: a0 + a1*x + a2*x^2 ..."""
        self.coeffs = list(coefficients)

    def __add__(self, other: "Polynomial") -> "Polynomial":
        # Pad shorter polynomial with zeros
        max_len = max(len(self.coeffs), len(other.coeffs))
        c1 = self.coeffs + [0.0] * (max_len - len(self.coeffs))
        c2 = other.coeffs + [0.0] * (max_len - len(other.coeffs))
        return Polynomial(*[a + b for a, b in zip(c1, c2)])

    def __len__(self) -> int:
        return len(self.coeffs)

    def __getitem__(self, degree: int) -> float:
        return self.coeffs[degree] if degree < len(self.coeffs) else 0.0

    def __repr__(self) -> str:
        terms = [f"{c}x^{i}" if i > 0 else f"{c}" for i, c in enumerate(self.coeffs) if c != 0]
        return " + ".join(terms) if terms else "0"

p1 = Polynomial(2, 3)     # 2 + 3x
p2 = Polynomial(1, 4, 5)  # 1 + 4x + 5x^2
p_sum = p1 + p2           # 3 + 7x + 5x^2

print(f"  p1:             {p1}")
print(f"  p2:             {p2}")
print(f"  p1 + p2:        {p_sum}")
print(f"  len(p_sum):     {len(p_sum)}")
print(f"  p_sum[2] (x^2): {p_sum[2]}")

assert p_sum.coeffs == [3.0, 7.0, 5.0]
assert len(p_sum) == 3
assert p_sum[2] == 5.0

# Explanation: Python's dunder methods (`__add__`, `__len__`, `__getitem__`) allow
# user-defined types to hook into standard operator semantics polymorphically.


# ============================================================
# Q5: Single-Dispatch Polymorphism (functools.singledispatch)
# ============================================================
# Question: Implement a generic payload serializer using `@functools.singledispatch`.
# Overload formatting logic for `dict`, `list`, `int`, and fallback types without `if/isinstance` ladders.

print("\n=== Q5: Single-Dispatch Polymorphism ===")

@functools.singledispatch
def format_payload(arg: Any) -> str:
    """Base generic implementation: handles fallback unknown types."""
    return f"FALLBACK_STR: {repr(arg)}"

@format_payload.register(int)
def _(arg: int) -> str:
    return f"INTEGER: {arg:,}"

@format_payload.register(float)
def _(arg: float) -> str:
    return f"FLOAT: {arg:.2f}"

@format_payload.register(dict)
def _(arg: Dict[Any, Any]) -> str:
    items = [f"{k}={v}" for k, v in sorted(arg.items())]
    return f"DICTIONARY: {{{', '.join(items)}}}"

@format_payload.register(list)
def _(arg: List[Any]) -> str:
    return f"LIST(len={len(arg)}): [{', '.join(str(x) for x in arg)}]"

res_int = format_payload(1_000_000)
res_float = format_payload(3.14159)
res_dict = format_payload({"status": "active", "code": 200})
res_list = format_payload([1, 2, 3])
res_unknown = format_payload((10, 20))  # Tuple falls back to base

print(f"  Int:     {res_int}")
print(f"  Float:   {res_float}")
print(f"  Dict:    {res_dict}")
print(f"  List:    {res_list}")
print(f"  Default: {res_unknown}")

assert res_int == "INTEGER: 1,000,000"
assert res_float == "FLOAT: 3.14"
assert "DICTIONARY:" in res_dict
assert res_list == "LIST(len=3): [1, 2, 3]"
assert res_unknown.startswith("FALLBACK_STR:")

# Explanation: `functools.singledispatch` transforms a regular function into a generic
# function that selects different implementations based on the runtime type of the first argument.


# ============================================================
# Q6: Simulating Method Overloading in Python Classes
# ============================================================
# Question: Python does not support multiple methods with the same name in a class.
# Show how to achieve method polymorphism using `*args`, `**kwargs`, and type branching.

print("\n=== Q6: Simulated Class Method Overloading ===")

class AreaCalculator:
    def calculate(self, *args: float) -> float:
        """
        Polymorphic area calculation:
          - 1 argument:  Circle area (pi * r^2)
          - 2 arguments: Rectangle area (width * height)
          - 3 arguments: Triangle area via Heron's formula
        """
        if len(args) == 1:
            r = args[0]
            return round(3.14159 * r * r, 2)
        elif len(args) == 2:
            w, h = args
            return round(w * h, 2)
        elif len(args) == 3:
            a, b, c = args
            s = (a + b + c) / 2.0
            return round((s * (s - a) * (s - b) * (s - c)) ** 0.5, 2)
        else:
            raise ValueError(f"No area formula for {len(args)} arguments")

calc = AreaCalculator()
area_circle = calc.calculate(5.0)          # 1 arg -> Circle
area_rect = calc.calculate(4.0, 6.0)       # 2 args -> Rectangle
area_tri = calc.calculate(3.0, 4.0, 5.0)   # 3 args -> 3-4-5 Triangle

print(f"  Circle area (r=5):        {area_circle}")
print(f"  Rectangle area (4x6):     {area_rect}")
print(f"  Triangle area (3, 4, 5):  {area_tri}")

assert area_circle == 78.54
assert area_rect == 24.0
assert area_tri == 6.0

# Explanation: In Python, later `def` definitions overwrite earlier ones with the same name.
# Variadic parameters (`*args`) allow a single method to handle multiple arities cleanly.


# ============================================================
# Q7: Polymorphic Rendering Pipeline
# ============================================================
# Question: Build a UI layout renderer that processes a list of diverse UI widgets
# (`Button`, `TextInput`, `ProgressBar`) by invoking `.render()` uniformly.

print("\n=== Q7: Polymorphic UI Rendering Pipeline ===")

class UIWidget:
    def render(self) -> str:
        raise NotImplementedError

class Button(UIWidget):
    def __init__(self, label: str):
        self.label = label
    def render(self) -> str:
        return f"<button>{self.label}</button>"

class TextInput(UIWidget):
    def __init__(self, placeholder: str):
        self.placeholder = placeholder
    def render(self) -> str:
        return f"<input placeholder='{self.placeholder}'/>"

class ProgressBar(UIWidget):
    def __init__(self, percent: int):
        self.percent = percent
    def render(self) -> str:
        return f"<progress value='{self.percent}' max='100'/>"

# Heterogeneous widget collection
screen_components: List[UIWidget] = [
    TextInput("Enter search query..."),
    Button("Search"),
    ProgressBar(65)
]

rendered_ui = "\n".join(widget.render() for widget in screen_components)
print("  Rendered Screen Components:")
for line in rendered_ui.splitlines():
    print(f"    {line}")

assert "<button>Search</button>" in rendered_ui
assert "progress value='65'" in rendered_ui

# Explanation: The rendering engine doesn't need to know the specific concrete class
# of each component; it relies entirely on the polymorphic `.render()` contract.


# ============================================================
# Q8: Strategy Pattern via Polymorphic Classes
# ============================================================
# Question: Implement the Strategy design pattern for order discount calculation.
# Allow switching discount strategies at runtime without modifying the Order class.

print("\n=== Q8: Strategy Pattern ===")

class DiscountStrategy(Protocol):
    def apply_discount(self, total: float) -> float: ...

class PercentageDiscount:
    def __init__(self, percent: float):
        self.percent = percent
    def apply_discount(self, total: float) -> float:
        return round(total * (1.0 - self.percent / 100.0), 2)

class FlatVoucherDiscount:
    def __init__(self, voucher_amount: float):
        self.voucher = voucher_amount
    def apply_discount(self, total: float) -> float:
        return round(max(0.0, total - self.voucher), 2)

class OrderContext:
    def __init__(self, base_total: float, strategy: DiscountStrategy):
        self.base_total = base_total
        self.strategy = strategy

    def calculate_payable(self) -> float:
        # Delegates calculation to current polymorphic strategy
        return self.strategy.apply_discount(self.base_total)

order = OrderContext(200.0, PercentageDiscount(15.0))  # 15% off $200 = $170
p1 = order.calculate_payable()
print(f"  Order with 15% discount: ${p1:.2f}")
assert p1 == 170.0

# Swap strategy dynamically at runtime
order.strategy = FlatVoucherDiscount(50.0)  # $50 off $200 = $150
p2 = order.calculate_payable()
print(f"  Order with $50 voucher:  ${p2:.2f}")
assert p2 == 150.0

# Explanation: The Strategy pattern uses polymorphism to decouple algorithms from the
# context object that uses them, adhering to the Open/Closed Principle.


# ============================================================
# Q9: Adapter Pattern (Normalizing Incompatible Interfaces)
# ============================================================
# Question: Adapt a legacy third-party weather API (`LegacyWeatherFeed.fetch_fahrenheit()`)
# to satisfy a target `StandardWeatherService` interface (`get_celsius()`).

print("\n=== Q9: Adapter Pattern ===")

class LegacyWeatherFeed:
    """Third-party legacy class with incompatible method names and units."""
    def fetch_fahrenheit(self, city_code: str) -> float:
        # Mock weather data
        feed_data = {"NYC": 68.0, "LON": 59.0, "TYO": 77.0}
        return feed_data.get(city_code, 70.0)

@runtime_checkable
class StandardWeatherService(Protocol):
    """Target interface expected by modern application."""
    def get_celsius(self, city_name: str) -> float: ...

class WeatherAdapter:
    """Adapter wrapping the legacy feed to conform to StandardWeatherService."""
    CITY_MAPPINGS = {"New York": "NYC", "London": "LON", "Tokyo": "TYO"}

    def __init__(self, legacy_feed: LegacyWeatherFeed):
        self._legacy = legacy_feed

    def get_celsius(self, city_name: str) -> float:
        city_code = self.CITY_MAPPINGS.get(city_name, "NYC")
        f_temp = self._legacy.fetch_fahrenheit(city_code)
        c_temp = (f_temp - 32.0) * (5.0 / 9.0)
        return round(c_temp, 2)

legacy_feed = LegacyWeatherFeed()
adapter = WeatherAdapter(legacy_feed)

nyc_celsius = adapter.get_celsius("New York")
lon_celsius = adapter.get_celsius("London")

print(f"  New York: {nyc_celsius} deg C (from 68 deg F)")
print(f"  London:   {lon_celsius} deg C (from 59 deg F)")

assert nyc_celsius == 20.0
assert lon_celsius == 15.0
assert isinstance(adapter, StandardWeatherService)

# Explanation: The Adapter pattern translates an incompatible interface into the
# interface clients expect, allowing classes to work together polymorphically.


# ============================================================
# Q10: Production-Grade Cloud Storage Polymorphic Engine
# ============================================================
# Question: Implement an abstract `CloudStorageClient` with polymorphic implementations
# for AWS S3, Google Cloud Storage (GCS), and Local Filesystem. Verify consistent behavior.

print("\n=== Q10: Cloud Storage Polymorphic Engine ===")

class CloudStorageClient(Protocol):
    def put_object(self, path: str, content: bytes) -> bool: ...
    def get_object(self, path: str) -> Optional[bytes]: ...
    def delete_object(self, path: str) -> bool: ...

class S3StorageAdapter:
    def __init__(self, bucket: str):
        self.bucket = bucket
        self._s3_store: Dict[str, bytes] = {}

    def put_object(self, path: str, content: bytes) -> bool:
        self._s3_store[f"s3://{self.bucket}/{path}"] = content
        return True

    def get_object(self, path: str) -> Optional[bytes]:
        return self._s3_store.get(f"s3://{self.bucket}/{path}")

    def delete_object(self, path: str) -> bool:
        return self._s3_store.pop(f"s3://{self.bucket}/{path}", None) is not None

class LocalFileSystemAdapter:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self._local_disk: Dict[str, bytes] = {}

    def put_object(self, path: str, content: bytes) -> bool:
        self._local_disk[f"{self.base_dir}/{path}"] = content
        return True

    def get_object(self, path: str) -> Optional[bytes]:
        return self._local_disk.get(f"{self.base_dir}/{path}")

    def delete_object(self, path: str) -> bool:
        return self._local_disk.pop(f"{self.base_dir}/{path}", None) is not None

def backup_application_config(storage: CloudStorageClient, config_data: bytes) -> bool:
    """Client function operating completely polymorphically over storage adapters."""
    target_filename = "app_config_backup.json"
    ok = storage.put_object(target_filename, config_data)
    retrieved = storage.get_object(target_filename)
    return ok and retrieved == config_data

s3_client = S3StorageAdapter("prod-backups")
local_client = LocalFileSystemAdapter("/var/data")

test_payload = b'{"version": "2.4.1", "active": true}'

res_s3 = backup_application_config(s3_client, test_payload)
res_local = backup_application_config(local_client, test_payload)

print(f"  Backup to S3 succeeded:    {res_s3}")
print(f"  Backup to Local succeeded: {res_local}")

assert res_s3 is True
assert res_local is True
assert s3_client.get_object("app_config_backup.json") == test_payload
assert local_client.get_object("app_config_backup.json") == test_payload

print("\nAll 10 polymorphism questions executed and asserted successfully!")
