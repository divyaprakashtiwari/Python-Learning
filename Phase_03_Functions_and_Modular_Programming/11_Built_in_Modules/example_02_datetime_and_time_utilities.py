"""
Phase 3 - Topic 11: Built-in Modules
Example 02: Dates, Times, Timezones & Performance Timers (`datetime`, `time`)

Demonstrates:
  - Creating timezone-aware UTC datetimes (`datetime`, `timezone.utc`)
  - Date arithmetic with `timedelta` (adding days/hours, computing differences)
  - Formatting (`strftime`) and parsing (`strptime` / `fromisoformat`) ISO-8601 strings
"""

from datetime import datetime, timedelta, timezone


def main() -> None:
    print("=== 1. Timezone-Aware Datetimes & `timedelta` Arithmetic ===")
    # Fixed deterministic timestamp for reproducible learning output
    ist_tz = timezone(timedelta(hours=5, minutes=30), name="IST")
    deploy_time_utc = datetime(2026, 11, 4, 10, 30, 0, tzinfo=timezone.utc)
    deploy_time_ist = deploy_time_utc.astimezone(ist_tz)

    print(f"  Deploy Time (UTC) : {deploy_time_utc.isoformat()}")
    print(f"  Deploy Time (IST) : {deploy_time_ist.isoformat()}")

    sla_deadline = deploy_time_ist + timedelta(days=7, hours=4)
    print(f"  SLA Deadline (+7d 4h) : {sla_deadline.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    print("\n=== 2. Parsing Dates & Computing Duration Between Events ===")
    incident_start = datetime.fromisoformat("2026-11-04T14:15:00+05:30")
    incident_resolved = datetime.fromisoformat("2026-11-04T16:02:30+05:30")
    downtime: timedelta = incident_resolved - incident_start
    total_minutes = downtime.total_seconds() / 60.0
    print(f"  Downtime Duration : {downtime} ({total_minutes:.1f} minutes)")


if __name__ == "__main__":
    main()
