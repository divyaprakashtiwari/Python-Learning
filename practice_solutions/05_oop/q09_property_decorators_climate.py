"""
Topic 05 - Object-Oriented Programming (OOP): Question 9
Problem: HVAC ClimateZone monitoring using @property, @setter, and @deleter decorators.
"""


class ClimateZone:
    """Manages environmental zone parameters with bi-directional unit conversion and validation."""

    def __init__(self, zone_name: str, initial_celsius: float = 22.0, humidity_pct: float = 45.0):
        self.zone_name = zone_name
        self._celsius = 20.0
        self._humidity_pct = 45.0

        # Utilize setters for initial invariant validation
        self.celsius = initial_celsius
        self.humidity_pct = humidity_pct

    @property
    def celsius(self) -> float:
        """Internal Celsius temperature reading."""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if not (-40.0 <= value <= 85.0):
            raise ValueError(f"Temperature {value}°C is out of allowable range (-40°C to 85°C)")
        self._celsius = round(float(value), 2)

    @celsius.deleter
    def celsius(self) -> None:
        self._celsius = 20.0
        print("Temperature reset to default safe setpoint (20.0°C).")

    @property
    def fahrenheit(self) -> float:
        """Computed Fahrenheit reading from internal Celsius state."""
        return round((self._celsius * 9.0 / 5.0) + 32.0, 2)

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        converted_c = (value - 32.0) * 5.0 / 9.0
        # Re-use validation in celsius setter
        self.celsius = converted_c

    @property
    def humidity_pct(self) -> float:
        """Relative humidity percentage [0.0 - 100.0]."""
        return self._humidity_pct

    @humidity_pct.setter
    def humidity_pct(self, value: float) -> None:
        if not (0.0 <= value <= 100.0):
            raise ValueError(f"Humidity {value}% is out of allowable range (0.0% to 100.0%)")
        self._humidity_pct = float(value)

    @property
    def heat_index_celsius(self) -> float:
        """Read-only computed apparent temperature metric."""
        return round(self._celsius + 0.025 * self._humidity_pct, 2)


# Verification & Execution
zone = ClimateZone("Server-Room-B", initial_celsius=20.0, humidity_pct=50.0)
print(f"Initial Temperature: {zone.celsius:.1f}°C | {zone.fahrenheit:.1f}°F | Humidity: {zone.humidity_pct:.1f}%")

zone.fahrenheit = 77.0  # Updates Celsius to 25.0
print("After Setting Fahrenheit to 77.0°F:")
print(f"Updated Celsius: {zone.celsius:.1f}°C | Current Fahrenheit: {zone.fahrenheit:.1f}°F")
print(f"Heat Index: {zone.heat_index_celsius:.2f}°C")

del zone.celsius  # Reset to 20.0
print(f"Current Celsius: {zone.celsius:.1f}°C")

# Boundary testing:
try:
    zone.celsius = 120.0
except ValueError as err:
    print("Caught:", err)

# Read-only test:
try:
    zone.heat_index_celsius = 30.0  # type: ignore
except AttributeError as err:
    print("Caught Read-Only Error:", err)
