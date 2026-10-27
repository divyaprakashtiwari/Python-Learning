"""
Topic 05 - Object-Oriented Programming (OOP): Question 5
Problem: Multi-Channel Notification Engine, Polymorphism, and Duck Typing.
"""

from typing import Any, Dict, List


class EmailService:
    """Email delivery service implementation."""

    def __init__(self, smtp_host: str, port: int):
        self.smtp_host = smtp_host
        self.port = port

    def send(self, recipient: str, message: str) -> Dict[str, Any]:
        _ = message
        return {
            "channel": "EMAIL",
            "recipient": recipient,
            "status": "SENT",
            "server": f"{self.smtp_host}:{self.port}"
        }


class SMSService:
    """SMS delivery service enforcing 160-character length limits."""

    def __init__(self, gateway_url: str, sender_id: str):
        self.gateway_url = gateway_url
        self.sender_id = sender_id

    def send(self, recipient: str, message: str) -> Dict[str, Any]:
        if len(message) > 160:
            raise ValueError("SMS message exceeds 160 character limit")
        return {
            "channel": "SMS",
            "recipient": recipient,
            "status": "SENT",
            "gateway": self.gateway_url
        }


class WebhookService:
    """Webhook HTTP delivery service."""

    def __init__(self, endpoint_url: str, auth_token: str):
        self.endpoint_url = endpoint_url
        self.auth_token = auth_token

    def send(self, recipient: str, message: str) -> Dict[str, Any]:
        _ = message
        return {
            "channel": "WEBHOOK",
            "target": recipient,
            "status": "POSTED",
            "endpoint": self.endpoint_url
        }


class NotificationDispatcher:
    """Polymorphic notification dispatcher relying strictly on duck typing."""

    def __init__(self):
        self._channels: List[Any] = []

    def register_channel(self, channel_obj: Any) -> None:
        """Enforces duck-typing conformance by verifying a callable send() method."""
        if not callable(getattr(channel_obj, "send", None)):
            raise TypeError("Invalid channel: must implement callable send()")
        self._channels.append(channel_obj)

    def broadcast(self, recipient: str, message: str) -> List[Dict[str, Any]]:
        """Dispatches notification across all registered channels cleanly capturing errors."""
        receipts = []
        for channel in self._channels:
            try:
                receipt = channel.send(recipient, message)
                receipts.append(receipt)
            except Exception as err:
                channel_name = getattr(channel, "__class__", type(channel)).__name__
                receipts.append({
                    "channel": channel_name,
                    "status": "FAILED",
                    "error": str(err)
                })
        return receipts


# Verification & Execution
dispatcher = NotificationDispatcher()
email_svc = EmailService("smtp.corp.net", 587)
sms_svc = SMSService("https://api.sms-relay.io", "ALERTS")
webhook_svc = WebhookService("https://hooks.slack.com/services/XYZ", "secret-token")

dispatcher.register_channel(email_svc)
dispatcher.register_channel(sms_svc)
dispatcher.register_channel(webhook_svc)

receipts = dispatcher.broadcast("admin@corp.net", "Critical: High memory utilization detected!")

print(f"Broadcast Results ({len(receipts)} channels dispatched):")
for idx, r in enumerate(receipts, 1):
    if r["channel"] == "EMAIL":
        print(f"{idx}. [EMAIL] To: {r['recipient']} | Status: {r['status']} | Server: {r['server']}")
    elif r["channel"] == "SMS":
        print(f"{idx}. [SMS] To: {r['recipient']} | Status: {r['status']} | Gateway: {r['gateway']}")
    elif r["channel"] == "WEBHOOK":
        print(f"{idx}. [WEBHOOK] Target: {r['target']} | Status: {r['status']} | Endpoint: {r['endpoint']}")

# Attempt invalid registration
print("\nAttempting invalid registration (int object 42):")
try:
    dispatcher.register_channel(42)  # type: ignore
except TypeError as err:
    print(f'Caught Expected Error: TypeError("{err}")')

# Attempt over-length message on SMS
print("\nAttempting SMS message with 170 characters:")
oversized_msg = "A" * 170
fail_receipts = dispatcher.broadcast("admin@corp.net", oversized_msg)
sms_fail = next(r for r in fail_receipts if r["channel"] in ("SMS", "SMSService") and r["status"] == "FAILED")
print(f'SMS Failed: ValueError("{sms_fail["error"]}")')
print("Dispatch continues without crashing other channels.")
