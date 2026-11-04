# Phase 4 — Topic 09: Abstraction

## 1. Introduction

**Abstraction** is the Object-Oriented Programming principle of **exposing only the essential high-level interface ("what an object does") while hiding the low-level implementation details ("how it does it")**.

In Python, formal interface contracts are defined using the built-in **`abc` (Abstract Base Classes)** module (`abc.ABC` and `@abc.abstractmethod`). An Abstract Base Class cannot be instantiated directly—it serves as an enforced contract that every concrete subclass must fulfill before it can be instantiated.

---

## 2. Why is it used?

- **Fail-Fast Contract Enforcement at Instantiation Time:** Without `@abstractmethod`, if a subclass forgets to implement `.download()`, you only discover the bug when that specific line of code is called in production (`NotImplementedError`). With `abc.ABC`, Python refuses to even instantiate the incomplete subclass (`TypeError: Can't instantiate abstract class ...`)!
- **The Template Method Pattern:** An ABC can implement a concrete workflow method (`run_pipeline()`) that calls abstract hook methods (`extract_raw()`, `transform_record()`) implemented by subclasses.
- **Free Standard Library Mixin Methods (`collections.abc`):** Inheriting from `collections.abc.Sequence` and implementing just 2 methods (`__getitem__` and `__len__`) automatically gives your class `.index()`, `.count()`, `__contains__` (`in`), `__iter__`, and `__reversed__`!

---

## 3. Syntax

```python
from abc import ABC, abstractmethod


# 1. Defining an Abstract Base Class (inherits from `ABC`)
class StorageBackend(ABC):
    @abstractmethod
    def upload(self, key: str, data: bytes) -> str:
        """Every concrete subclass MUST implement `upload`."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Every concrete subclass MUST implement the `provider_name` property."""
```

---

## 4. Explanation (Step-by-Step)

### Step 1: How `abc.ABC` and `@abstractmethod` Work
1. A class inherits from `abc.ABC` (which uses the metaclass `abc.ABCMeta`).
2. Methods or properties decorated with `@abstractmethod` are recorded in a `frozenset` attribute on the class called **`Class.__abstractmethods__`**.
3. When you try to instantiate `cls()`, `ABCMeta.__call__` checks if `bool(cls.__abstractmethods__)` is non-empty. If **any** abstract method remains unimplemented, Python immediately raises `TypeError: Can't instantiate abstract class ...`.

### Step 2: Combining `@property` and `@abstractmethod`
When creating an abstract property, **`@property` must be the outer (top) decorator and `@abstractmethod` must be the inner (bottom) decorator**:
```python
@property
@abstractmethod
def pipeline_name(self) -> str:
    ...
```

### Step 3: `collections.abc` Abstract Base Classes
Python's `collections.abc` module provides standard ABCs for containers (`Iterable`, `Iterator`, `Sequence`, `MutableSequence`, `Mapping`, `MutableMapping`, `Set`):

| `collections.abc` Class | Required Abstract Methods | Free Mixin Methods Provided Automatically |
| :--- | :--- | :--- |
| **`Sequence`** | `__getitem__`, `__len__` | `__contains__`, `__iter__`, `__reversed__`, `index`, `count` |
| **`Mapping`** | `__getitem__`, `__iter__`, `__len__` | `keys`, `items`, `values`, `get`, `__contains__`, `__eq__` |

---

## 5. Minimum 3 Examples

### Example 1: Abstract Base Classes (`abc.ABC` and `@abstractmethod`)
File: `example_01_abstract_base_classes_abc.py`

```python
from abc import ABC, abstractmethod


class StorageBackend(ABC):
    """Abstract contract for cloud or local object storage providers."""

    @abstractmethod
    def upload(self, key: str, data: bytes) -> str:
        """Store `data` under `key` and return a storage URI."""

    @abstractmethod
    def download(self, key: str) -> bytes:
        """Retrieve raw bytes stored under `key`."""


class InMemoryS3Backend(StorageBackend):
    """Concrete implementation that fulfills both `upload` and `download`."""

    def __init__(self, bucket_name: str) -> None:
        self.bucket_name = bucket_name
        self._store: dict[str, bytes] = {}

    def upload(self, key: str, data: bytes) -> str:
        self._store[key] = data
        return f"s3://{self.bucket_name}/{key}"

    def download(self, key: str) -> bytes:
        return self._store[key]


class IncompleteBackend(StorageBackend):
    """Missing `download()` implementation - remains abstract!"""

    def upload(self, key: str, data: bytes) -> str:
        return f"temp://{key}"


def main() -> None:
    print("=== 1. Cannot Instantiate `StorageBackend` Directly ===")
    try:
        StorageBackend()
    except TypeError as err:
        print(f"  Caught expected TypeError: {err}")

    print("\n=== 2. Cannot Instantiate Incomplete Subclass Missing `download` ===")
    try:
        IncompleteBackend()
    except TypeError as err:
        print(f"  Caught expected TypeError: {err}")

    print("\n=== 3. Using Complete Concrete Subclass (`InMemoryS3Backend`) ===")
    s3 = InMemoryS3Backend("prod-assets")
    uri = s3.upload("reports/q4.txt", b"Q4 Revenue Summary")
    payload = s3.download("reports/q4.txt")
    print(f"  Uploaded URI     : {uri}")
    print(f"  Downloaded Bytes : {payload!r}")


if __name__ == "__main__":
    main()
```

---

### Example 2: Abstract Properties (`@property` + `@abstractmethod`) & The Template Method Pattern
File: `example_02_abstract_properties_and_template_method.py`

```python
from abc import ABC, abstractmethod


class BaseETLPipeline(ABC):
    """
    Abstract Base Class using the Template Method Pattern:
    `run_pipeline()` is a concrete method on the ABC that orchestrates
    abstract steps (`pipeline_name`, `extract_raw`, `transform_record`).
    """

    @property
    @abstractmethod
    def pipeline_name(self) -> str:
        """Subclasses must provide a read-only `pipeline_name` property."""

    @abstractmethod
    def extract_raw(self) -> list[str]:
        """Subclasses must fetch raw records."""

    @abstractmethod
    def transform_record(self, raw: str) -> str:
        """Subclasses must clean/transform a single record."""

    def run_pipeline(self) -> list[str]:
        """Concrete template method shared by all subclasses."""
        raw_items = self.extract_raw()
        cleaned = [self.transform_record(item) for item in raw_items]
        print(f"  [{self.pipeline_name}] Processed {len(cleaned)} records: {cleaned}")
        return cleaned


class UserSignupETL(BaseETLPipeline):
    """Concrete ETL pipeline normalizing user signup emails."""

    @property
    def pipeline_name(self) -> str:
        return "UserSignup-ETL"

    def extract_raw(self) -> list[str]:
        return ["  AARAV@GMAIL.COM ", " Priya@TechCorp.in "]

    def transform_record(self, raw: str) -> str:
        return raw.strip().lower()


def main() -> None:
    print("=== Template Method Pattern with Abstract Properties & Methods ===")
    etl = UserSignupETL()
    etl.run_pipeline()


if __name__ == "__main__":
    main()
```

---

### Example 3: Standard Library ABCs (`collections.abc`)
File: `example_03_collections_abc_and_virtual_subclasses.py`

```python
from collections.abc import Sequence
from typing import overload


class ImmutableBatch(Sequence[str]):
    """
    Inherits from `collections.abc.Sequence`.
    By implementing ONLY `__getitem__` and `__len__`, `Sequence` provides
    `__iter__`, `__contains__` (`in`), `__reversed__`, `.index()`, and `.count()`!
    """

    def __init__(self, items: list[str]) -> None:
        self._items = tuple(items)

    @overload
    def __getitem__(self, index: int) -> str: ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[str]: ...

    def __getitem__(self, index: int | slice) -> str | Sequence[str]:
        return self._items[index]

    def __len__(self) -> int:
        return len(self._items)


def main() -> None:
    print("=== Inheriting Free Mixin Methods from `collections.abc.Sequence` ===")
    batch = ImmutableBatch(["task-A", "task-B", "task-A", "task-C"])

    print(f"  len(batch)              : {len(batch)}")
    print(f"  batch[1]                : {batch[1]!r}")
    print(f"  'task-C' in batch       : {'task-C' in batch} (provided by Sequence!)")
    print(f"  batch.count('task-A')   : {batch.count('task-A')} (provided by Sequence!)")
    print(f"  batch.index('task-C')   : {batch.index('task-C')} (provided by Sequence!)")
    print(f"  list(reversed(batch))   : {list(reversed(batch))} (provided by Sequence!)")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_abstract_base_classes_abc.py`)
```text
=== 1. Cannot Instantiate `StorageBackend` Directly ===
  Caught expected TypeError: Can't instantiate abstract class StorageBackend without an implementation for abstract methods 'download', 'upload'

=== 2. Cannot Instantiate Incomplete Subclass Missing `download` ===
  Caught expected TypeError: Can't instantiate abstract class IncompleteBackend without an implementation for abstract method 'download'

=== 3. Using Complete Concrete Subclass (`InMemoryS3Backend`) ===
  Uploaded URI     : s3://prod-assets/reports/q4.txt
  Downloaded Bytes : b'Q4 Revenue Summary'
```

### Output — Example 2 (`example_02_abstract_properties_and_template_method.py`)
```text
=== Template Method Pattern with Abstract Properties & Methods ===
  [UserSignup-ETL] Processed 2 records: ['aarav@gmail.com', 'priya@techcorp.in']
```

### Output — Example 3 (`example_03_collections_abc_and_virtual_subclasses.py`)
```text
=== Inheriting Free Mixin Methods from `collections.abc.Sequence` ===
  len(batch)              : 4
  batch[1]                : 'task-B'
  'task-C' in batch       : True (provided by Sequence!)
  batch.count('task-A')   : 2 (provided by Sequence!)
  batch.index('task-C')   : 3 (provided by Sequence!)
  list(reversed(batch))   : ['task-C', 'task-A', 'task-B', 'task-A'] (provided by Sequence!)
```

---

## 7. Code Explanation

1. **Instantiation Check (`example_01`):** `IncompleteBackend` implements `upload()` but omits `download()`. Because `IncompleteBackend.__abstractmethods__` still contains `frozenset({'download'})`, calling `IncompleteBackend()` immediately raises `TypeError`.
2. **Template Method (`example_02`):** `BaseETLPipeline.run_pipeline()` is a concrete method on an abstract class! Abstract classes in Python can contain rich shared logic alongside their `@abstractmethod` declarations.
3. **`collections.abc.Sequence` (`example_03`):** `ImmutableBatch` only defines `__init__`, `__getitem__`, and `__len__`, yet supports `'task-C' in batch`, `batch.count('task-A')`, `batch.index('task-C')`, and `reversed(batch)` inherited from `Sequence`.

---

## 8. Common Mistakes

1. **Using `@abstractmethod` on a class that does NOT inherit from `abc.ABC` (or `metaclass=ABCMeta`):**
   - If you forget `(ABC)` in `class StorageBackend:` and only write `@abstractmethod`, Python will **not** prevent instantiating `StorageBackend()` at runtime! Always inherit from `ABC`.
2. **Reversing `@abstractmethod` and `@property` decorator order:**
   - Writing `@abstractmethod` above `@property` fails to mark the property descriptor properly. `@abstractmethod` must always be the **innermost** decorator (closest to `def`).
3. **Thinking an `@abstractmethod` cannot have a body:**
   - An `@abstractmethod` **can** have a default implementation body that subclasses call via `super().my_abstract_method()` as part of their override!

---

## 9. Practice Questions

1. **Easy — `PaymentProcessor(ABC)` Contract:**
   Create an ABC `PaymentProcessor(ABC)` with abstract methods `authorize(amount: float) -> bool` and `capture(transaction_id: str) -> str`. Implement `UPIPaymentProcessor(PaymentProcessor)` and verify that an incomplete `CryptoProcessor(PaymentProcessor)` cannot be instantiated.

2. **Medium — File Exporter Template Method (`BaseExporter(ABC)`):**
   Create `BaseExporter(ABC)` with a concrete `export(records: list[dict]) -> str` method that calls abstract methods `header() -> str`, `format_row(row: dict) -> str`, and `footer() -> str`. Implement `CSVExporter` and `MarkdownTableExporter`.

3. **Hard — Custom Read-Only Dictionary (`collections.abc.Mapping`):**
   Implement a `CaseInsensitiveConfig(Mapping[str, str])` class by implementing only `__getitem__`, `__iter__`, and `__len__`, and verify that `.get()`, `.keys()`, `.items()`, and `==` work automatically.

---

## 10. Interview Questions

### Q1: What is the difference between Encapsulation and Abstraction in OOP?
**Answer:**
- **Abstraction (Design / Interface level):** Focuses on **hiding complexity** by exposing only *what* operations an object supports (`StorageBackend.upload(key, data)`) while hiding *how* the underlying network/disk protocol works.
- **Encapsulation (Implementation / Data-hiding level):** Focuses on **bundling data with methods and protecting internal state invariants** (`_store`, `@property` setters) from unauthorized external corruption.

### Q2: Why is `@abstractmethod` on `abc.ABC` preferred over raising `NotImplementedError` in base class methods?
**Answer:**
If a base method simply raises `NotImplementedError`, an incomplete subclass can be instantiated without error and will only crash at runtime when that specific method is eventually called. With `abc.ABC` and `@abstractmethod`, Python verifies completeness **at instantiation time (`obj = Subclass()`)**, catching missing methods immediately during startup or unit tests.

### Q3: Can an Abstract Base Class (`ABC`) have concrete methods and `__init__` in Python?
**Answer:**
**Yes!** Unlike Java's original `interface`, a Python `ABC` is a full class that can define `__init__`, instance attributes, concrete helper methods (Template Method Pattern), `@classmethod`s, and `@staticmethod`s alongside its `@abstractmethod`s.
