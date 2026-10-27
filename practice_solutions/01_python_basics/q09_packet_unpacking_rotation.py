"""
Topic 01 - Python Basics & Variables
Practice Question 9 Solution: Starred Unpacking & Simultaneous Variable Rotation

Problem Statement:
1. Starred expression unpacking on telemetry packets:
   header, timestamp, *sensor_readings, checksum = packet
2. Perform a 3-way circular rotation on (state_x, state_y, state_z) in a single
   simultaneous assignment: state_x gets z, state_y gets x, state_z gets y.
3. Validate checksum: int(sum(sensor_readings)) % 256 == checksum.
"""

from typing import Any


def process_packet(packet: list[Any]) -> dict[str, Any]:
    """Unpacks a telemetry packet using starred expressions and validates checksum."""
    if len(packet) < 3:
        raise ValueError("Packet must contain at least header, 1 reading, and checksum.")

    # Starred unpacking
    header, timestamp, *sensor_readings, checksum = packet

    # Checksum validation: whole-number integer sum % 256
    calc_sum = int(sum(sensor_readings)) % 256
    is_valid = calc_sum == checksum

    return {
        "header": header,
        "timestamp": timestamp,
        "sensor_readings": sensor_readings,
        "checksum": checksum,
        "calculated_checksum": calc_sum,
        "is_valid": is_valid,
    }


def rotate_states(x: Any, y: Any, z: Any) -> tuple[Any, Any, Any]:
    """Performs a 3-way circular rotation without temporary variables.

    state_x receives state_z's value,
    state_y receives state_x's value,
    state_z receives state_y's value.
    """
    x, y, z = z, x, y
    return x, y, z


def main() -> None:
    sample_packet = [170, 1714000000, 24.5, 26.1, 23.8, 25.0, 18.2, 117]
    state_x, state_y, state_z = 10, 20, 30

    packet_info = process_packet(sample_packet)
    new_x, new_y, new_z = rotate_states(state_x, state_y, state_z)

    print(f"{'Unpacked Header':<22}: {packet_info['header']}")
    print(f"{'Unpacked Timestamp':<22}: {packet_info['timestamp']}")
    print(
        f"{'Sensor Readings Count':<22}: {len(packet_info['sensor_readings'])} readings -> {packet_info['sensor_readings']}"
    )
    print(f"{'Checksum':<22}: {packet_info['checksum']}")
    print(
        f"{'Checksum Match':<22}: {packet_info['is_valid']} "
        f"(Calculated: {packet_info['calculated_checksum']} == Expected: {packet_info['checksum']})"
    )
    print(f"Rotated States       : state_x = {new_x}, state_y = {new_y}, state_z = {new_z}")


if __name__ == "__main__":
    main()
