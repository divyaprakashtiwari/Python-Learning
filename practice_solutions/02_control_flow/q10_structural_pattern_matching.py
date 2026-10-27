"""
Topic 02 - Control Flow
Practice Question 10 Solution: Structural Pattern Matching (match-case) Dispatcher

Problem Statement:
Implements a robust event and command message dispatcher using Python 3.10+ match-case:
1. Mapping patterns (type: COMMAND, BATCH, ERROR).
2. Pattern guards (e.g. if code >= 500, if len(remaining) >= 2).
3. Sequence unpacking pattern ([first, *rest]).
4. Tuple pattern (("PING", int)).
5. Default wildcard capture case (_ as unhandled).
"""

from typing import Any


def dispatch_event(event: Any) -> str:
    """Dispatches heterogeneous events using Python structural pattern matching."""
    match event:
        case {"type": "COMMAND", "action": str(action), "payload": {"key": str(k), "value": v}}:
            return f"CONFIG SET: key='{k}' -> value='{v}'"

        case {"type": "BATCH", "items": [first_item, *remaining_items]} if len(remaining_items) >= 2:
            return f"BATCH PROCESSING: Primary='{first_item}', Trailing Items Count={len(remaining_items)}"

        case {"type": "ERROR", "code": int(code), "details": str(msg)} if code >= 500:
            return f"CRITICAL INCIDENT TRIGGERED: Error {code} - {msg}"

        case {"type": "ERROR", "code": int(code), "details": str(msg)}:
            return f"CLIENT ERROR LOGGED: Error {code} - {msg}"

        case ("PING", int(ts)):
            pong_response = ("PONG", ts, "ACK")
            return f"PING RECEIVED -> Responded: {pong_response}"

        case _ as unhandled:
            return f"REJECTED: Unrecognized event structure: {unhandled}"


def main() -> None:
    events = [
        {"type": "COMMAND", "action": "UPDATE_RATE", "payload": {"key": "refresh_hz", "value": 60}},
        {"type": "BATCH", "items": ["job_alpha", "job_beta", "job_gamma", "job_delta"]},
        {"type": "ERROR", "code": 503, "details": "Service Unavailable"},
        {"type": "ERROR", "code": 404, "details": "Resource Not Found"},
        ("PING", 1714001234),
        {"invalid": "payload"},
    ]

    for idx, ev in enumerate(events):
        result_msg = dispatch_event(ev)
        print(f"Event {idx}: {result_msg}")


if __name__ == "__main__":
    main()
