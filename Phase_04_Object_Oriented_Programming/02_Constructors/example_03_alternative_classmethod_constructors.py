"""
Phase 4 - Topic 02: Constructors
Example 03: Alternative Constructors Using `@classmethod` (`from_dict`, `from_iso`)

Demonstrates:
  - Why Python only supports ONE `__init__` method per class (no Java/C++ constructor overloading)
  - The Pythonic idiom for multiple constructors: `@classmethod` factory methods
"""

from datetime import datetime


class EventTicket:
    """Represents a concert/conference ticket with multiple construction pathways."""

    def __init__(self, event_name: str, attendee: str, price: float, event_date: str) -> None:
        self.event_name = event_name
        self.attendee = attendee
        self.price = price
        self.event_date = event_date

    @classmethod
    def from_csv_row(cls, csv_line: str) -> "EventTicket":
        """Alternative constructor #1: parse a comma-separated string."""
        name, attendee, price_str, date_str = [part.strip() for part in csv_line.split(",")]
        return cls(name, attendee, float(price_str), date_str)

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "EventTicket":
        """Alternative constructor #2: build from a JSON/dict payload."""
        return cls(
            event_name=str(payload["event_name"]),
            attendee=str(payload["attendee"]),
            price=float(str(payload["price"])),
            event_date=str(payload["event_date"]),
        )

    @classmethod
    def complimentary_vip(cls, event_name: str, attendee: str) -> "EventTicket":
        """Alternative constructor #3: create a free VIP pass for today's date."""
        today_str = datetime(2026, 11, 4).strftime("%Y-%m-%d")
        return cls(f"{event_name} [VIP]", attendee, 0.0, today_str)

    def format_ticket(self) -> str:
        return (
            f"Ticket({self.event_name!r}, attendee={self.attendee!r}, "
            f"price=INR {self.price:,.2f}, date={self.event_date})"
        )


def main() -> None:
    print("=== Constructing `EventTicket` via 4 Different Pathways ===")
    t1 = EventTicket("PyCon India", "Divya", 2500.0, "2026-11-15")
    t2 = EventTicket.from_csv_row("Cloud Summit, Aarav, 1800.50, 2026-12-01")
    t3 = EventTicket.from_dict(
        {
            "event_name": "AI Workshop",
            "attendee": "Priya",
            "price": 999.0,
            "event_date": "2026-11-20",
        }
    )
    t4 = EventTicket.complimentary_vip("PyCon India", "Keynote Speaker")

    for idx, ticket in enumerate((t1, t2, t3, t4), start=1):
        print(f"  Pathway #{idx} : {ticket.format_ticket()}")


if __name__ == "__main__":
    main()
