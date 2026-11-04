"""
Phase 4 - Topic 06: Multiple Inheritance
Example 02: The Mixin Pattern (`JSONSerializableMixin`, `TimestampMixin`)

Demonstrates:
  - The most Pythonic real-world use of Multiple Inheritance: orthogonal Mixin classes
  - Adding reusable capabilities (`to_json()` and `summary_tag()`) to domain models
    without polluting a single monolithic base class
"""

import json


class JSONSerializableMixin:
    """Mixin providing `.to_json()` serialization for any object with `__dict__`."""

    def to_json(self) -> str:
        public_data = {
            k: v for k, v in self.__dict__.items() if not k.startswith("_")
        }
        return json.dumps(public_data, sort_keys=True)


class IdentifiableMixin:
    """Mixin providing a canonical `<ClassName#id>` display tag."""

    id: str | int

    def identity_tag(self) -> str:
        return f"<{self.__class__.__name__}#{self.id}>"


class BaseModel:
    """Core domain base class."""

    def __init__(self, record_id: str) -> None:
        self.id = record_id


class CustomerInvoice(JSONSerializableMixin, IdentifiableMixin, BaseModel):
    """Combines Mixins (left) with the primary `BaseModel` (right)."""

    def __init__(self, record_id: str, customer: str, total_inr: float) -> None:
        super().__init__(record_id)
        self.customer = customer
        self.total_inr = total_inr
        self._internal_secret = "do-not-serialize"


def main() -> None:
    print("=== Combining Orthogonal Mixin Classes with a Domain Model ===")
    inv = CustomerInvoice("INV-2026-09", "Aarav Tech", 59000.0)
    print(f"  Identity Tag (`IdentifiableMixin`)     : {inv.identity_tag()}")
    print(f"  JSON Payload (`JSONSerializableMixin`) : {inv.to_json()}")
    print(f"  MRO : {[c.__name__ for c in CustomerInvoice.mro()]}")


if __name__ == "__main__":
    main()
