"""
Topic 08: Modules and Packages - Question 05: datetime Module

A comprehensive collection of 10 standalone, runnable exercises exploring
Python's standard library `datetime` module, timezone awareness, arithmetic with
`timedelta`, string parsing and formatting (strptime/strftime), ISO 8601, and scheduling.

Questions Covered:
 1. Core Classes: date, time, datetime, timedelta, and timezone representations.
 2. String Formatting with strftime(): Date directives (%Y, %m, %d, %H, %M, %S, %A).
 3. Parsing with strptime() & fromisoformat(): Ingesting RFC 3339 / ISO 8601 strings.
 4. Time Arithmetic with timedelta: Offsets, rolling deadlines, and date differences.
 5. Timezone Awareness: Naive vs Aware datetimes and UTC conversions with astimezone().
 6. Unix Epoch Timestamps: fromtimestamp() and .timestamp() conversions.
 7. Datetime Sorting & Comparison: Range overlaps and chronological sorting.
 8. Calendar Week Metrics: weekday(), isoweekday(), and isocalendar() year/week numbers.
 9. Benchmarking: High-precision time.perf_counter() vs wall-clock datetime.
10. Advanced Project: Meeting Room Availability & Recurring Schedule Conflict Engine.
"""

from datetime import date, datetime, time as dtime, timedelta, timezone
import time
from typing import Any


# ==============================================================================
# Question 1: Core Datetime Classes
# ==============================================================================
def exercise_q1_core_datetime_classes() -> None:
    """
    Demonstrate creating instances of date, time, datetime, and timedelta.
    """
    print("=== Q1: Core Datetime Classes ===")

    # 1. date: year, month, day
    d = date(2026, 10, 18)
    assert d.year == 2026 and d.month == 10 and d.day == 18

    # 2. time: hour, minute, second, microsecond
    t = dtime(14, 30, 45, 500000)
    assert t.hour == 14 and t.minute == 30 and t.second == 45 and t.microsecond == 500000

    # 3. datetime: combined date and time
    dt = datetime(2026, 10, 18, 14, 30, 45)
    assert dt.date() == d
    assert dt.time() == dtime(14, 30, 45)

    # 4. timedelta: duration
    delta = timedelta(days=2, hours=3, minutes=15)
    assert delta.total_seconds() == (2 * 86400) + (3 * 3600) + (15 * 60)

    print(f"  Date:      {d}")
    print(f"  Time:      {t}")
    print(f"  Datetime:  {dt}")
    print(f"  Timedelta: {delta} ({delta.total_seconds():,.0f} seconds)")


# ==============================================================================
# Question 2: String Formatting with strftime()
# ==============================================================================
def exercise_q2_strftime_formatting() -> None:
    """
    Demonstrate formatting datetime objects into custom display strings using strftime().
    """
    print("\n=== Q2: String Formatting with strftime() ===")

    dt = datetime(2026, 10, 18, 9, 5, 2)

    # ISO date
    iso_date = dt.strftime("%Y-%m-%d")
    assert iso_date == "2026-10-18"

    # Human readable formatted string
    human_str = dt.strftime("%A, %B %d, %Y at %I:%M:%S %p")
    assert "October 18, 2026" in human_str
    assert "09:05:02 AM" in human_str

    print(f"  ISO format:    {iso_date}")
    print(f"  Human format:  {human_str}")


# ==============================================================================
# Question 3: Parsing with strptime() & fromisoformat()
# ==============================================================================
def exercise_q3_parsing_strings() -> None:
    """
    Demonstrate converting raw text strings into strongly-typed datetime objects
    using strptime() and fromisoformat().
    """
    print("\n=== Q3: Parsing with strptime() & fromisoformat() ===")

    # 1. strptime with explicit format string
    date_str = "18/10/2026 15:45:00"
    parsed_dt = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
    assert parsed_dt.year == 2026
    assert parsed_dt.month == 10
    assert parsed_dt.day == 18
    assert parsed_dt.hour == 15

    # 2. fromisoformat (standard ISO 8601 / RFC 3339)
    iso_str = "2026-10-18T15:45:00Z"
    iso_dt = datetime.fromisoformat(iso_str)
    assert iso_dt.year == 2026
    assert iso_dt.tzinfo == timezone.utc

    print(f"  Parsed via strptime:     {parsed_dt}")
    print(f"  Parsed via fromisoformat: {iso_dt} (tz={iso_dt.tzinfo})")


# ==============================================================================
# Question 4: Time Arithmetic with timedelta
# ==============================================================================
def exercise_q4_timedelta_arithmetic() -> None:
    """
    Demonstrate time arithmetic: adding durations, subtracting dates to obtain
    durations, and computing sliding expiration windows.
    """
    print("\n=== Q4: Time Arithmetic with timedelta ===")

    start_date = datetime(2026, 10, 18, 10, 0, 0)

    # Add 14 days and 6 hours
    deadline = start_date + timedelta(days=14, hours=6)
    assert deadline == datetime(2026, 11, 1, 16, 0, 0)

    # Difference between two datetimes yields a timedelta
    completion = datetime(2026, 10, 20, 13, 30, 0)
    elapsed = completion - start_date
    assert elapsed.days == 2
    assert elapsed.seconds == (3 * 3600) + (30 * 60)
    assert elapsed.total_seconds() == 185400.0

    print(f"  Start:    {start_date}")
    print(f"  Deadline: {deadline}")
    print(f"  Elapsed:  {elapsed} ({elapsed.total_seconds() / 3600:.1f} hours)")


# ==============================================================================
# Question 5: Timezone Awareness (Naive vs Aware)
# ==============================================================================
def exercise_q5_timezone_awareness() -> None:
    """
    Demonstrate the distinction between naive datetimes (no tzinfo) and aware
    datetimes (has tzinfo), and convert across timezones using astimezone().
    """
    print("\n=== Q5: Timezone Awareness (Naive vs Aware) ===")

    # 1. Naive datetime
    naive = datetime(2026, 10, 18, 12, 0, 0)
    assert naive.tzinfo is None

    # 2. Aware UTC datetime
    utc_now = datetime.now(timezone.utc)
    assert utc_now.tzinfo is timezone.utc

    # 3. Fixed offset timezone: e.g. IST (UTC+05:30)
    ist_tz = timezone(timedelta(hours=5, minutes=30), name="IST")
    ist_dt = utc_now.astimezone(ist_tz)

    assert ist_dt.tzinfo == ist_tz
    # The physical point in time is identical, so difference in seconds is 0
    assert (ist_dt - utc_now).total_seconds() == 0.0

    # Subtracting naive and aware raises TypeError
    try:
        _ = utc_now - naive
        assert False
    except TypeError as exc:
        assert "can't subtract offset-naive and offset-aware datetimes" in str(exc)

    print(f"  UTC Aware: {utc_now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"  IST Aware: {ist_dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")


# ==============================================================================
# Question 6: Unix Epoch Timestamps
# ==============================================================================
def exercise_q6_epoch_timestamps() -> None:
    """
    Convert between POSIX epoch timestamps (seconds since Jan 1 1970 UTC)
    and datetime objects.
    """
    print("\n=== Q6: Unix Epoch Timestamps ===")

    known_epoch = 1792320000.0  # Approx October 2026

    # Epoch float -> UTC datetime
    utc_dt = datetime.fromtimestamp(known_epoch, tz=timezone.utc)
    assert utc_dt.year == 2026

    # UTC datetime -> Epoch float
    epoch_back = utc_dt.timestamp()
    assert epoch_back == known_epoch

    print(f"  Epoch:    {known_epoch}")
    print(f"  DateTime: {utc_dt}")
    print(f"  Roundtrip verified: {epoch_back == known_epoch}")


# ==============================================================================
# Question 7: Datetime Sorting & Comparison
# ==============================================================================
def exercise_q7_sorting_and_comparison() -> None:
    """
    Demonstrate that datetimes are naturally orderable and sortable.
    """
    print("\n=== Q7: Datetime Sorting & Comparison ===")

    timestamps = [
        datetime(2026, 10, 18, 14, 0),
        datetime(2026, 10, 15, 9, 30),
        datetime(2026, 10, 20, 18, 0),
        datetime(2026, 10, 18, 10, 15),
    ]

    sorted_dates = sorted(timestamps)
    assert sorted_dates[0] == datetime(2026, 10, 15, 9, 30)
    assert sorted_dates[-1] == datetime(2026, 10, 20, 18, 0)

    # Range check
    window_start = datetime(2026, 10, 18, 0, 0)
    window_end = datetime(2026, 10, 18, 23, 59)

    events_in_day = [dt for dt in timestamps if window_start <= dt <= window_end]
    assert len(events_in_day) == 2

    print(f"  Sorted chronological dates: {[d.strftime('%m-%d %H:%M') for d in sorted_dates]}")
    print(f"  Events within single-day window: {len(events_in_day)}")


# ==============================================================================
# Question 8: Calendar Week Metrics
# ==============================================================================
def exercise_q8_calendar_week_metrics() -> None:
    """
    Demonstrate weekday() (Monday is 0, Sunday is 6), isoweekday() (Monday is 1, Sunday is 7),
    and isocalendar() (year, week_number, weekday).
    """
    print("\n=== Q8: Calendar Week Metrics ===")

    # Sunday, October 18, 2026
    dt = date(2026, 10, 18)

    # weekday(): 0 = Mon, 6 = Sun
    assert dt.weekday() == 6

    # isoweekday(): 1 = Mon, 7 = Sun
    assert dt.isoweekday() == 7

    # isocalendar(): namedtuple (year, week, weekday)
    iso_cal = dt.isocalendar()
    assert iso_cal.year == 2026
    assert isinstance(iso_cal.week, int)
    assert iso_cal.weekday == 7

    print(f"  Date: {dt} (Sunday)")
    print(f"  dt.weekday():     {dt.weekday()} (0-indexed)")
    print(f"  dt.isoweekday():  {dt.isoweekday()} (1-indexed)")
    print(f"  dt.isocalendar(): Year={iso_cal.year}, Week={iso_cal.week}, Day={iso_cal.weekday}")


# ==============================================================================
# Question 9: High-Precision Benchmarking (perf_counter vs datetime)
# ==============================================================================
def exercise_q9_benchmarking_durations() -> None:
    """
    Demonstrate why `time.perf_counter()` is used for measuring elapsed code execution
    time (monotonic, high-resolution), while `datetime` is used for wall-clock timestamps.
    """
    print("\n=== Q9: High-Precision Benchmarking ===")

    # time.perf_counter() is monotonic (immune to system clock adjustments / daylight savings)
    t0 = time.perf_counter()
    # Lightweight workload
    _ = sum(i * i for i in range(50000))
    t1 = time.perf_counter()

    elapsed_seconds = t1 - t0
    assert elapsed_seconds > 0.0

    print(f"  Monotonic execution duration: {elapsed_seconds * 1000:.3f} ms")


# ==============================================================================
# Question 10: Advanced Project - Meeting Room Availability & Conflict Engine
# ==============================================================================
class MeetingScheduleEngine:
    """
    Calculates time overlaps and checks availability for meeting rooms across timezones.
    """

    def __init__(self) -> None:
        # room_name -> list of (start_dt_utc, end_dt_utc, title)
        self.bookings: dict[str, list[tuple[datetime, datetime, str]]] = {}

    def book_room(self, room: str, start: datetime, end: datetime, title: str) -> bool:
        """
        Books a room if no collision occurs. Converts inputs to UTC first.
        """
        if end <= start:
            raise ValueError("Meeting end time must be strictly after start time")

        # Normalize to UTC
        start_utc = start.astimezone(timezone.utc)
        end_utc = end.astimezone(timezone.utc)

        existing = self.bookings.setdefault(room, [])

        # Check for overlap: Overlap occurs if (start < existing_end) and (end > existing_start)
        for e_start, e_end, e_title in existing:
            if start_utc < e_end and end_utc > e_start:
                # Collision detected!
                return False

        existing.append((start_utc, end_utc, title))
        return True

    def get_room_schedule(self, room: str) -> list[tuple[str, str, str]]:
        existing = sorted(self.bookings.get(room, []), key=lambda x: x[0])
        return [
            (
                s.strftime("%H:%M UTC"),
                e.strftime("%H:%M UTC"),
                title,
            )
            for s, e, title in existing
        ]


def exercise_q10_meeting_scheduler() -> None:
    """
    Test MeetingScheduleEngine handling bookings and detecting conflicts.
    """
    print("\n=== Q10: Meeting Room Availability & Conflict Engine ===")

    engine = MeetingScheduleEngine()

    # Slot 1: 10:00 to 11:30 UTC
    m1_start = datetime(2026, 10, 18, 10, 0, tzinfo=timezone.utc)
    m1_end = datetime(2026, 10, 18, 11, 30, tzinfo=timezone.utc)
    ok1 = engine.book_room("Boardroom_A", m1_start, m1_end, "Quarterly Review")
    assert ok1 is True

    # Slot 2 (Conflict!): 11:00 to 12:00 UTC overlaps with Slot 1
    m2_start = datetime(2026, 10, 18, 11, 0, tzinfo=timezone.utc)
    m2_end = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
    ok2 = engine.book_room("Boardroom_A", m2_start, m2_end, "Conflicting Sync")
    assert ok2 is False  # Rejected due to collision

    # Slot 3 (Clean): 11:30 to 12:30 UTC directly adjacent to Slot 1
    m3_start = datetime(2026, 10, 18, 11, 30, tzinfo=timezone.utc)
    m3_end = datetime(2026, 10, 18, 12, 30, tzinfo=timezone.utc)
    ok3 = engine.book_room("Boardroom_A", m3_start, m3_end, "Project Standup")
    assert ok3 is True

    # Different room (Clean): 10:00 to 11:00 in Room B
    ok4 = engine.book_room("Room_B", m1_start, m2_start, "Design Review")
    assert ok4 is True

    schedule_a = engine.get_room_schedule("Boardroom_A")
    assert len(schedule_a) == 2
    assert schedule_a[0][2] == "Quarterly Review"
    assert schedule_a[1][2] == "Project Standup"

    print("  Meeting Bookings for Boardroom_A:")
    for start, end, title in schedule_a:
        print(f"    - {start} to {end}: {title}")
    print("  Conflict detection correctly prevented overlapping booking.")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_core_datetime_classes()
    exercise_q2_strftime_formatting()
    exercise_q3_parsing_strings()
    exercise_q4_timedelta_arithmetic()
    exercise_q5_timezone_awareness()
    exercise_q6_epoch_timestamps()
    exercise_q7_sorting_and_comparison()
    exercise_q8_calendar_week_metrics()
    exercise_q9_benchmarking_durations()
    exercise_q10_meeting_scheduler()

    print("\nAll 10 datetime questions executed and asserted successfully!")
