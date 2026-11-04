"""
Phase 4 - Topic 06: Multiple Inheritance
Example 03: Cooperative `__init__` with `**kwargs` & Catching Invalid MRO Hierarchies

Demonstrates:
  - How multiple parent classes with different `__init__` parameters cooperate safely
    by accepting and forwarding `**kwargs` up to `object.__init__()`
  - How Python rejects inconsistent inheritance graphs at class creation time with
    `TypeError: Cannot create a consistent method resolution order (MRO)`
"""

from typing import Any


class RootEntity:
    """Root class that strips no kwargs and calls `super().__init__()` (`object`)."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class GPSLocatable(RootEntity):
    """Initializes `latitude` and `longitude` and forwards remaining `**kwargs`."""

    def __init__(self, *, latitude: float, longitude: float, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.latitude = latitude
        self.longitude = longitude


class BatteryPowered(RootEntity):
    """Initializes `battery_pct` and forwards remaining `**kwargs`."""

    def __init__(self, *, battery_pct: int, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.battery_pct = battery_pct


class DeliveryDrone(GPSLocatable, BatteryPowered):
    """Cooperatively initializes `drone_id`, `GPSLocatable`, and `BatteryPowered`."""

    def __init__(self, drone_id: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.drone_id = drone_id


def main() -> None:
    print("=== 1. Cooperative Multiple Inheritance `__init__` Using `**kwargs` ===")
    drone = DeliveryDrone(
        "DRN-404",
        latitude=12.9716,
        longitude=77.5946,
        battery_pct=88,
    )
    print(
        f"  Drone {drone.drone_id}: coords=({drone.latitude}, {drone.longitude}), "
        f"battery={drone.battery_pct}%"
    )

    print("\n=== 2. Catching an Inconsistent MRO Graph (`TypeError`) ===")

    class X:
        pass

    class Y(X):
        pass

    try:
        # `X` precedes `Y` in `class Bad(X, Y)`, which contradicts `Y(X)` where `Y` precedes `X`!
        class BadHierarchy(X, Y):  # type: ignore[misc]
            pass
    except TypeError as err:
        print(f"  Caught expected MRO TypeError: {err}")


if __name__ == "__main__":
    main()
