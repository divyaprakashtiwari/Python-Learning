"""
Phase 4 - Topic 04: Instance, Class and Static Methods
Example 02: Why `@classmethod` Beats `@staticmethod` for Inheritance-Aware Factories

Demonstrates:
  - How `@classmethod` automatically receives the actual subclass (`cls`) when called
    on a derived class (` PremiumOrder.from_json(...)` returns a `PremiumOrder`)
  - Why hardcoding the base class inside a `@staticmethod` breaks subclass factories
"""


class BaseSensor:
    """Base IoT sensor with a `@classmethod` factory."""

    unit: str = "raw"

    def __init__(self, sensor_id: str, reading: float) -> None:
        self.sensor_id = sensor_id
        self.reading = reading

    @classmethod
    def from_packet(cls, packet: str) -> "BaseSensor":
        """`cls` dynamically refers to whichever subclass invoked `from_packet`!"""
        sensor_id, val_str = packet.split(":")
        return cls(sensor_id.strip(), float(val_str))

    def report(self) -> str:
        return f"[{self.__class__.__name__}] id={self.sensor_id} -> {self.reading} {self.unit}"


class TemperatureSensor(BaseSensor):
    """Subclass that inherits `from_packet` without rewriting it."""

    unit: str = "Celsius"


class PressureSensor(BaseSensor):
    """Another subclass that inherits `from_packet`."""

    unit: str = "kPa"


def main() -> None:
    print("=== `@classmethod` Factory Preserves Subclass Type Automatically ===")
    raw_sensor = BaseSensor.from_packet("SNS-01:42.0")
    temp_sensor = TemperatureSensor.from_packet("TMP-09:23.5")
    pres_sensor = PressureSensor.from_packet("PRS-04:101.3")

    for s in (raw_sensor, temp_sensor, pres_sensor):
        print(f"  {s.report():<52} | type={type(s).__name__}")


if __name__ == "__main__":
    main()
