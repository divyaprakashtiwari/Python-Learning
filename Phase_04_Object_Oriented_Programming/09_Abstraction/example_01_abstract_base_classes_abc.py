"""
Phase 4 - Topic 09: Abstraction
Example 01: Abstract Base Classes (`abc.ABC` and `@abstractmethod`)

Demonstrates:
  - Defining an Abstract Base Class (`StorageBackend(ABC)`) that cannot be instantiated directly
  - Enforcing an interface contract with `@abstractmethod` (`upload`, `download`)
  - Catching `TypeError` at instantiation time when a subclass forgets to implement
    any abstract method
"""

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
        StorageBackend()  # type: ignore[abstract]
    except TypeError as err:
        print(f"  Caught expected TypeError: {err}")

    print("\n=== 2. Cannot Instantiate Incomplete Subclass Missing `download` ===")
    try:
        IncompleteBackend()  # type: ignore[abstract]
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
