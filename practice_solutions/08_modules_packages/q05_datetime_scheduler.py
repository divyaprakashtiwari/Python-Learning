"""
Topic 08 - Modules and Packages: Question 5
Problem: Global Event Scheduler using Python datetime, timedelta, and timezone awareness.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List


class GlobalEventScheduler:
    """Manages multi-region timestamp conversion, formatting, and countdown intervals."""

    def parse_server_timestamp(self, iso_str: str) -> datetime:
        """Parses UTC string in %Y-%m-%d %H:%M:%S format attaching explicit timezone awareness."""
        try:
            parsed = datetime.strptime(iso_str, "%Y-%m-%d %H:%M:%S")
            return parsed.replace(tzinfo=timezone.utc)
        except ValueError:
            raise ValueError("Malformed timestamp format; expected YYYY-MM-DD HH:MM:SS")

    def format_regional_display(
        self,
        dt: datetime,
        fmt_string: str = "%A, %d %B %Y at %I:%M %p (%Z)"
    ) -> str:
        """Formats datetime according to the specified regional format string."""
        return dt.strftime(fmt_string)

    def convert_utc_to_timezones(
        self,
        utc_dt: datetime,
        regions: Dict[str, float]
    ) -> Dict[str, str]:
        """Converts aware UTC datetime across regional hour offsets (supporting fractional hours)."""
        conversions = {}
        for region_code, hour_offset in regions.items():
            total_minutes = int(hour_offset * 60)
            target_tz = timezone(timedelta(minutes=total_minutes))
            converted_dt = utc_dt.astimezone(target_tz)
            conversions[region_code] = self.format_regional_display(converted_dt)
        return conversions

    def generate_maintenance_checkpoints(
        self,
        start_dt: datetime,
        maintenance_dt: datetime,
        step_hours: int = 12
    ) -> List[Dict[str, Any]]:
        """Generates stepping countdown checkpoints until target maintenance timestamp."""
        if maintenance_dt <= start_dt:
            raise ValueError("Maintenance time must be in the future")

        checkpoints = []
        current = start_dt
        step_delta = timedelta(hours=step_hours)

        while current < maintenance_dt:
            time_left = maintenance_dt - current
            checkpoints.append({
                "checkpoint": current.strftime("%Y-%m-%d %H:%M:%S UTC"),
                "days_remaining": time_left.days,
                "total_hours_remaining": round(time_left.total_seconds() / 3600.0, 1)
            })
            current += step_delta

        return checkpoints


# Verification & Execution
scheduler = GlobalEventScheduler()
event_utc = scheduler.parse_server_timestamp("2026-10-31 18:30:00")
display_utc = scheduler.format_regional_display(event_utc)

print(f"UTC Scheduled Time: {display_utc}")

regions = {"US_EAST": -5.0, "INDIA_IST": 5.5, "JAPAN_JST": 9.0}
regional_times = scheduler.convert_utc_to_timezones(event_utc, regions)

print("Regional Broadcasts:")
for reg, time_str in regional_times.items():
    offset_val = regions[reg]
    sign = "+" if offset_val >= 0 else ""
    print(f"- {reg} (UTC{sign}{offset_val}): {time_str}")

now_utc = scheduler.parse_server_timestamp("2026-10-30 06:30:00")
checkpoints = scheduler.generate_maintenance_checkpoints(now_utc, event_utc, step_hours=12)

print(f"\nMaintenance Checkpoints (Step = 12h):")
for idx, cp in enumerate(checkpoints, 1):
    print(f"{idx}. {cp['checkpoint']} | Total Hours Left: {cp['total_hours_remaining']} | Days: {cp['days_remaining']}")
