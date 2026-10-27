"""
Topic 02 - Control Flow
Practice Question 5 Solution: Network Packet Ingestion Filter (break & continue)

Problem Statement:
Simulates a high-throughput network packet ingestion filter using break and continue:
- If source_ip in blocked_ips: increment blocked_count and continue.
- If status_code == 200 and payload_bytes == 0: continue (skip heartbeat ping).
- If is_malicious is True: log security alert and break immediately.
- Otherwise: accumulate total_bytes and increment valid_packets_processed.
"""

from typing import Any


def filter_packets(packets: list[dict[str, Any]], blocked_ips: set[str]) -> dict[str, Any]:
    """Filters network packets using continue for skips and break for security shutdown."""
    blocked_count = 0
    valid_packets = 0
    total_bytes = 0
    terminated_prematurely = False
    event_logs = []

    for pkt in packets:
        p_id = pkt["packet_id"]
        ip = pkt["source_ip"]
        bytes_len = pkt["payload_bytes"]
        status = pkt["status_code"]
        malicious = pkt.get("is_malicious", False)

        # 1. IP Blocklist check -> continue
        if ip in blocked_ips:
            blocked_count += 1
            event_logs.append(f"Packet {p_id}: Blocked by IP filter")
            continue

        # 2. Empty heartbeat ping check -> continue
        if status == 200 and bytes_len == 0:
            event_logs.append(f"Packet {p_id}: Heartbeat ping skipped")
            continue

        # 3. Malicious packet detection -> break
        if malicious:
            event_logs.append(f"CRITICAL ALERT: Malicious packet {p_id} detected! Pipeline shutdown initiated.")
            terminated_prematurely = True
            break

        # 4. Valid benign packet
        valid_packets += 1
        total_bytes += bytes_len
        event_logs.append(f"Packet {p_id}: Processed ({bytes_len} bytes)")

    return {
        "event_logs": event_logs,
        "terminated_prematurely": terminated_prematurely,
        "valid_packets_processed": valid_packets,
        "total_bytes_ingested": total_bytes,
        "blocked_packets": blocked_count,
    }


def main() -> None:
    blocked = {"198.51.100.12", "203.0.113.5"}
    sample_packets = [
        {"packet_id": 101, "source_ip": "192.168.1.10", "payload_bytes": 1024, "status_code": 200, "is_malicious": False},
        {"packet_id": 102, "source_ip": "198.51.100.12", "payload_bytes": 512, "status_code": 403, "is_malicious": False},
        {"packet_id": 103, "source_ip": "192.168.1.15", "payload_bytes": 0, "status_code": 200, "is_malicious": False},
        {"packet_id": 104, "source_ip": "192.168.1.20", "payload_bytes": 2048, "status_code": 200, "is_malicious": False},
        {"packet_id": 105, "source_ip": "10.0.0.99", "payload_bytes": 8192, "status_code": 500, "is_malicious": True},
        {"packet_id": 106, "source_ip": "192.168.1.25", "payload_bytes": 1024, "status_code": 200, "is_malicious": False},
    ]

    res = filter_packets(sample_packets, blocked)

    for log in res["event_logs"]:
        print(log)

    print("Summary Report:")
    print(f"- Ingestion Terminated Prematurely: {res['terminated_prematurely']}")
    print(f"- Valid Packets Processed: {res['valid_packets_processed']}")
    print(f"- Total Bytes Ingested: {res['total_bytes_ingested']:,} bytes")
    print(f"- Blocked Packets: {res['blocked_packets']}")


if __name__ == "__main__":
    main()
