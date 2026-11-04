"""
Phase 4 - Topic 07: Polymorphism
Example 01: Subtype Polymorphism (Uniform Interface Across a Class Hierarchy)

Demonstrates:
  - Calling the exact same method (`.send_alert(message)`) on a heterogeneous collection
    of subclass instances (`EmailNotifier`, `SMSNotifier`, `WebhookNotifier`)
  - How adding a new `Notifier` subclass requires ZERO changes to `broadcast_incident()`
    (the Open/Closed Principle)
"""


class Notifier:
    """Base notification channel contract."""

    def send_alert(self, message: str) -> str:
        raise NotImplementedError("Subclasses must implement send_alert()")


class EmailNotifier(Notifier):
    def __init__(self, recipient_email: str) -> None:
        self.recipient_email = recipient_email

    def send_alert(self, message: str) -> str:
        return f"[EMAIL -> {self.recipient_email}] Subject: ALERT | Body: {message}"


class SMSNotifier(Notifier):
    def __init__(self, phone_number: str) -> None:
        self.phone_number = phone_number

    def send_alert(self, message: str) -> str:
        return f"[SMS   -> {self.phone_number}] {message[:60]}"


class SlackWebhookNotifier(Notifier):
    def __init__(self, channel: str) -> None:
        self.channel = channel

    def send_alert(self, message: str) -> str:
        return f"[SLACK -> #{self.channel}] :rotating_light: {message}"


def broadcast_incident(channels: list[Notifier], incident_msg: str) -> None:
    """
    Polymorphic dispatcher: knows NOTHING about Email, SMS, or Slack specifics!
    Simply invokes `channel.send_alert(incident_msg)` on every object.
    """
    for channel in channels:
        print(f"  {channel.send_alert(incident_msg)}")


def main() -> None:
    print("=== Subtype Polymorphism: Broadcasting Across Heterogeneous Channels ===")
    on_call_channels: list[Notifier] = [
        EmailNotifier("sre-team@techcorp.in"),
        SMSNotifier("+91-9876543210"),
        SlackWebhookNotifier("prod-incidents"),
    ]
    broadcast_incident(on_call_channels, "Database replica lag exceeded 30 seconds")


if __name__ == "__main__":
    main()
