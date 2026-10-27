"""
Topic 05 - Object-Oriented Programming (OOP): Question 4
Problem: Multi-level Vehicle Rental Hierarchy, Inheritance, super(), and Polymorphic Overriding.
"""


class Vehicle:
    """Base vehicle class defining rental pricing and basic specifications."""

    def __init__(self, brand: str, model: str, daily_rate: float):
        if daily_rate <= 0:
            raise ValueError("Daily rate must be strictly positive")
        self.brand = brand
        self.model = model
        self.daily_rate = float(daily_rate)

    def calculate_rental(self, days: int) -> float:
        """Calculates base rental cost across specified days."""
        if days <= 0:
            raise ValueError("Rental days must be at least 1")
        return self.daily_rate * days

    def get_specs(self) -> str:
        """Returns standard specification string."""
        return f"Vehicle[Brand: {self.brand}, Model: {self.model}, Rate: ${self.daily_rate:.2f}/day]"


class ElectricVehicle(Vehicle):
    """Derived electric vehicle with discount incentives, battery specs, and prep fee."""

    def __init__(self, brand: str, model: str, daily_rate: float, battery_capacity: float, range_km: int):
        super().__init__(brand, model, daily_rate)
        if battery_capacity <= 0:
            raise ValueError("Battery capacity must be positive")
        self.battery_capacity = float(battery_capacity)
        self.range_km = int(range_km)

    def calculate_rental(self, days: int) -> float:
        """Applies 10% green discount on base rate plus flat $15.00 battery prep fee."""
        if days <= 0:
            raise ValueError("Rental days must be at least 1")
        base = super().calculate_rental(days)
        return (base * 0.90) + 15.00

    def estimate_recharge_time(self, charger_power_kw: float) -> float:
        """Calculates recharge duration given charger capacity in kW."""
        if charger_power_kw <= 0:
            raise ValueError("Charger power must be positive")
        return round(self.battery_capacity / charger_power_kw, 2)

    def get_specs(self) -> str:
        return f"{super().get_specs()} | Battery: {self.battery_capacity:.1f}kWh | Range: {self.range_km}km"


class AutonomousElectricVehicle(ElectricVehicle):
    """Multi-level derived autonomous vehicle with autopilot surcharge."""

    def __init__(
        self,
        brand: str,
        model: str,
        daily_rate: float,
        battery_capacity: float,
        range_km: int,
        autopilot_version: str
    ):
        super().__init__(brand, model, daily_rate, battery_capacity, range_km)
        self.autopilot_version = autopilot_version

    def calculate_rental(self, days: int) -> float:
        """Chains EV rental and adds $25.00/day autonomous features surcharge."""
        return super().calculate_rental(days) + (25.00 * days)

    def get_specs(self) -> str:
        return f"{super().get_specs()} | Autopilot: {self.autopilot_version}"


# Verification & Execution
v1 = Vehicle("Toyota", "Corolla", 50.0)
v2 = ElectricVehicle("Tesla", "Model 3", 80.0, 75.0, 500)
v3 = AutonomousElectricVehicle("Waymo-Jaguar", "I-Pace", 120.0, 90.0, 470, "v4.2-Pro")

rental_v1 = v1.calculate_rental(3)
rental_v2 = v2.calculate_rental(3)
rental_v3 = v3.calculate_rental(3)

print(f"Vehicle 1 (3 days): ${rental_v1:.2f}")
print(f"Vehicle 2 EV (3 days): ${rental_v2:.2f}")
print(f"Vehicle 3 Autonomous (3 days): ${rental_v3:.2f}")

recharge_hrs = v2.estimate_recharge_time(50.0)
print(f"EV Recharge Time at 50kW Charger: {recharge_hrs:.1f} hours")
print(f"Autonomous Vehicle Specs: {v3.get_specs()}")
