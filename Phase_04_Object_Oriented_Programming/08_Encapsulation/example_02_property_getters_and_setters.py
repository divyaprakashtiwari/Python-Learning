"""
Phase 4 - Topic 08: Encapsulation
Example 02: Pythonic Getters & Setters Using `@property` and `@<name>.setter`

Demonstrates:
  - Why Python uses `@property` instead of Java-style `get_price()` / `set_price()` methods
  - Adding validation to an attribute without breaking callers who use dot notation (`p.price = 500`)
  - Creating read-only computed properties (`@property` with no setter)
"""


class CloudGpuInstance:
    """Encapsulates GPU count and hourly rate with validated `@property` descriptors."""

    def __init__(self, instance_id: str, gpu_count: int, hourly_rate_usd: float) -> None:
        self._instance_id = instance_id
        # Assigning to `self.gpu_count` inside `__init__` invokes the `@gpu_count.setter`!
        self.gpu_count = gpu_count
        self.hourly_rate_usd = hourly_rate_usd

    @property
    def instance_id(self) -> str:
        """Read-only property (no setter defined)."""
        return self._instance_id

    @property
    def gpu_count(self) -> int:
        """Getter for `gpu_count`."""
        return self._gpu_count

    @gpu_count.setter
    def gpu_count(self, value: int) -> None:
        """Validated setter for `gpu_count`."""
        if value not in (1, 2, 4, 8):
            raise ValueError(f"gpu_count must be 1, 2, 4, or 8 (got {value})")
        self._gpu_count = value

    @property
    def daily_cost_usd(self) -> float:
        """Computed read-only property derived from live state."""
        return round(self._gpu_count * self.hourly_rate_usd * 24, 2)


def main() -> None:
    print("=== 1. Reading and Updating `@property` via Clean Dot Syntax ===")
    node = CloudGpuInstance("gpu-a100-01", gpu_count=2, hourly_rate_usd=3.50)
    print(f"  Instance {node.instance_id}: {node.gpu_count} GPUs -> Daily Cost: ${node.daily_cost_usd:,.2f}")

    node.gpu_count = 8
    print(f"  Scaled to {node.gpu_count} GPUs            -> Daily Cost: ${node.daily_cost_usd:,.2f}")

    print("\n=== 2. Setter Rejects Invalid Values (`ValueError`) ===")
    try:
        node.gpu_count = 3
    except ValueError as err:
        print(f"  Caught expected ValueError: {err}")

    print("\n=== 3. Read-Only Property Rejects Reassignment (`AttributeError`) ===")
    try:
        node.instance_id = "hacked-id"  # type: ignore[misc]
    except AttributeError as err:
        print(f"  Caught expected AttributeError: {err}")


if __name__ == "__main__":
    main()
