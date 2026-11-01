"""
Topic 10: Break, Continue and Pass
Example 02: Using `continue` to Skip Invalid or Ignored Records in a Pipeline

Demonstrates how `continue` skips the rest of the current iteration and jumps
straight to the next item in the loop.
"""


def process_sensor_readings(raw_lines: list[str]) -> list[float]:
    valid_celsius: list[float] = []

    for line_no, raw in enumerate(raw_lines, start=1):
        cleaned = raw.strip()

        # Skip empty lines or comment lines starting with '#'
        if not cleaned or cleaned.startswith("#"):
            continue

        # Skip corrupted sensor error markers
        if cleaned == "ERR_SENSOR_TIMEOUT":
            print(f"  [Line {line_no}] Skipping sensor timeout warning.")
            continue

        reading = float(cleaned)
        valid_celsius.append(reading)
        print(f"  [Line {line_no}] Recorded valid temperature: {reading:.1f} C")

    return valid_celsius


def main() -> None:
    log_feed = [
        "# Weather Station Batch 01",
        "24.5",
        "",
        "ERR_SENSOR_TIMEOUT",
        "26.0",
        "# Mid-day calibration",
        "27.5",
    ]
    print("=== Sensor Data Pipeline (continue in action) ===")
    valid = process_sensor_readings(log_feed)
    print(f"\nValid Readings Collected ({len(valid)}): {valid}")
    print(f"Average Temperature: {sum(valid) / len(valid):.2f} C")


if __name__ == "__main__":
    main()
