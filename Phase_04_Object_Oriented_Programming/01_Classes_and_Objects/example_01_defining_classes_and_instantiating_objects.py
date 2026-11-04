"""
Phase 4 - Topic 01: Classes and Objects
Example 01: Defining a Class Blueprint and Instantiating Independent Objects

Demonstrates:
  - Defining a class using the `class` keyword and PascalCase naming (PEP 8)
  - How a class acts as a blueprint while objects (instances) hold independent state
  - How Python automatically passes the instance as the first argument (`self`)
    when calling an instance method (`obj.method()` == `Class.method(obj)`)
"""


class SmartThermostat:
    """Blueprint for a smart home thermostat device."""

    def __init__(self, room_name: str, current_temp_c: float, target_temp_c: float) -> None:
        self.room_name = room_name
        self.current_temp_c = current_temp_c
        self.target_temp_c = target_temp_c

    def heating_status(self) -> str:
        """Return whether the thermostat is HEATING, COOLING, or IDLE."""
        if self.current_temp_c < self.target_temp_c:
            return "HEATING"
        if self.current_temp_c > self.target_temp_c:
            return "COOLING"
        return "IDLE"

    def describe(self) -> str:
        """Return a formatted status line for this thermostat instance."""
        return (
            f"[{self.room_name:<12}] Current: {self.current_temp_c:.1f}C | "
            f"Target: {self.target_temp_c:.1f}C | Mode: {self.heating_status()}"
        )


def main() -> None:
    print("=== 1. Instantiating Multiple Independent Objects from One Class ===")
    living_room = SmartThermostat("Living Room", 21.5, 24.0)
    bedroom = SmartThermostat("Master Bed", 26.0, 22.0)
    study = SmartThermostat("Home Office", 23.0, 23.0)

    for device in (living_room, bedroom, study):
        print(f"  {device.describe()}")

    print("\n=== 2. Modifying State on One Instance Does Not Affect Others ===")
    living_room.current_temp_c = 24.0
    print(f"  Updated Living Room : {living_room.describe()}")
    print(f"  Unchanged Bedroom   : {bedroom.describe()}")

    print("\n=== 3. How `self` Works Under the Hood ===")
    # `living_room.heating_status()` is syntactic sugar for:
    bound_result = living_room.heating_status()
    unbound_result = SmartThermostat.heating_status(living_room)
    print(f"  living_room.heating_status()                 -> {bound_result}")
    print(f"  SmartThermostat.heating_status(living_room)  -> {unbound_result}")


if __name__ == "__main__":
    main()
