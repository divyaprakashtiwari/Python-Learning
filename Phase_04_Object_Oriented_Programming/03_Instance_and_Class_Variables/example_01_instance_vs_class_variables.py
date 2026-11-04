"""
Phase 4 - Topic 03: Instance and Class Variables
Example 01: Shared Class Variables vs Per-Object Instance Variables

Demonstrates:
  - Defining class variables at the top of the `class` body (shared across all instances)
  - Defining instance variables on `self` inside `__init__` (unique per instance)
  - How Python's attribute lookup checks `instance.__dict__` first, then `Class.__dict__`
"""


class CloudSubscription:
    """Models a SaaS subscription with a shared class-level GST rate and instancecounter."""

    # Class variables (shared across all instances, stored in `CloudSubscription.__dict__`)
    gst_rate: float = 0.18
    active_subscriptions: int = 0

    def __init__(self, tenant_name: str, monthly_base_fee: float) -> None:
        # Instance variables (unique per object, stored in `self.__dict__`)
        self.tenant_name = tenant_name
        self.monthly_base_fee = monthly_base_fee
        # Increment the class variable on the class itself
        CloudSubscription.active_subscriptions += 1

    def total_monthly_bill(self) -> float:
        """Read `self.gst_rate` (which falls back to `CloudSubscription.gst_rate`)."""
        return round(self.monthly_base_fee * (1.0 + self.gst_rate), 2)


def main() -> None:
    print("=== 1. Creating Instances & Tracking Class-Level Counter ===")
    sub_a = CloudSubscription("Acme Corp", 10000.0)
    sub_b = CloudSubscription("Zenith Labs", 25000.0)
    print(f"  Active subscriptions : {CloudSubscription.active_subscriptions}")
    print(f"  Acme bill (18% GST)  : INR {sub_a.total_monthly_bill():,.2f}")
    print(f"  Zenith bill (18% GST): INR {sub_b.total_monthly_bill():,.2f}")

    print("\n=== 2. Updating a Class Variable on the Class Affects All Instances ===")
    CloudSubscription.gst_rate = 0.12
    print(f"  Acme bill (12% GST)  : INR {sub_a.total_monthly_bill():,.2f}")
    print(f"  Zenith bill (12% GST): INR {sub_b.total_monthly_bill():,.2f}")


if __name__ == "__main__":
    main()
