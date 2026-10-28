"""
Question 10: Modern Command Router with Positional/Keyword Parameters, Walrus & Pattern Matching
Topic: Advanced Python

Key Concepts Tested:
- Positional-only (/) and keyword-only (*) parameter enforcement
- Assignment expressions (walrus operator :=) in comprehensions
- Structural pattern matching (match...case) with mapping patterns, guards, and sequence unpacking
- Fallback wildcard matching (case _)
- TypeError handling on parameter constraint violations
"""

from typing import List, Dict, Any


class ModernCommandRouter:
    """
    Modern command processing and message routing engine leveraging
    positional-only arguments, the walrus operator, and structural pattern matching.
    """

    @staticmethod
    def dispatch_task(
        task_code: str,
        /,
        cluster_zone: str,
        *,
        priority: int = 1,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """
        Dispatches a task enforcing parameter calling conventions:
        - task_code: strictly positional-only (precedes /)
        - cluster_zone: standard positional or keyword
        - priority, dry_run: strictly keyword-only (succeeds *)
        """
        return {
            "task": task_code,
            "zone": cluster_zone,
            "priority": priority,
            "dry_run": dry_run,
        }

    @staticmethod
    def process_stream_chunks(raw_buffer: List[str], max_chunk_len: int = 4) -> List[Dict[str, Any]]:
        """
        Filters stream items using assignment expressions (walrus operator :=)
        to strip whitespace and measure token length in a single pass.
        """
        return [
            {"token": tok, "length": l}
            for item in raw_buffer
            if (l := len(tok := item.strip())) > max_chunk_len
        ]

    @staticmethod
    def route_event(event_payload: Any) -> Dict[str, Any]:
        """
        Routes dynamic event payloads using structural pattern matching (match...case)
        with mapping patterns, guards, and sequence destructuring.
        """
        match event_payload:
            case {"type": "AUTH", "user": {"id": uid, "role": "SUPERUSER"}}:
                return {"status": "ROUTE_ROOT", "target_uid": uid}

            case {"type": "PAYMENT", "amount": amt, "currency": curr} if amt >= 10000.0:
                return {"status": "ROUTE_COMPLIANCE_HOLD", "amount": amt, "currency": curr}

            case {"type": "PAYMENT", "amount": amt, "currency": curr}:
                return {"status": "ROUTE_AUTO_SETTLE", "amount": amt, "currency": curr}

            case [str(cmd), *args] if cmd in {"PING", "STATUS"}:
                return {"status": "ROUTE_SYSTEM_CLI", "command": cmd, "args": args}

            case _:
                return {"status": "ROUTE_UNRECOGNIZED", "raw": event_payload}


if __name__ == "__main__":
    router = ModernCommandRouter()

    print("=== 1. Positional-Only & Keyword-Only Task Dispatch ===")
    task_res = router.dispatch_task("DEPLOY", "us-central-1", priority=2, dry_run=True)
    print(f"Task Dispatch Result:\n{task_res}")

    print("\n=== 2. Walrus Operator Filter ===")
    buffer = ["  ok  ", "   superlongtoken   ", " tiny "]
    chunks = router.process_stream_chunks(buffer, max_chunk_len=5)
    print(f"Stream Chunks Filtered via Walrus:\n{chunks}")

    print("\n=== 3. Structural Pattern Matching ===")
    evt1 = {"type": "AUTH", "user": {"id": "U-99", "role": "SUPERUSER"}}
    evt2 = {"type": "PAYMENT", "amount": 25000.0, "currency": "USD"}
    evt3 = ["PING", "--verbose", "--all"]
    evt4 = "Invalid String Message"

    r1 = router.route_event(evt1)
    r2 = router.route_event(evt2)
    r3 = router.route_event(evt3)
    r4 = router.route_event(evt4)

    print(f"- Evt1: {r1}")
    print(f"- Evt2: {r2}")
    print(f"- Evt3: {r3}")
    print(f"- Evt4: {r4}")

    print("\n=== 4. Parameter Enforcement Violations ===")
    # 4a. Passing positional-only parameter as keyword
    try:
        router.dispatch_task(task_code="RUN", cluster_zone="us-east-1")  # type: ignore[call-arg]
    except TypeError as err:
        print(f"Positional-only violation caught:\n  TypeError: {err}")

    # 4b. Passing keyword-only parameter positionally
    try:
        router.dispatch_task("RUN", "us-east-1", 5)  # type: ignore[misc]
    except TypeError as err:
        print(f"Keyword-only violation caught:\n  TypeError: {err}")
