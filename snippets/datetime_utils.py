"""
Datetime Utilities timezone handling, parsing, formatting, deltas.

Datetime is notoriously confusing in Python. This file covers the
patterns you'll actually use, with proper timezone handling.

Key rule: Always store and transmit in UTC. Convert to local time only for display.
"""
from datetime import datetime, date, time, timedelta, timezone
from zoneinfo import ZoneInfo  # Python 3.9+ (backport: pip install backports.zoneinfo)


# =============================================================================
# CURRENT TIME always use timezone-aware datetimes
# =============================================================================

def current_times():
    """Get current time in different ways."""
    # Timezone-aware (CORRECT)
    now_utc = datetime.now(timezone.utc)
    now_ist = datetime.now(ZoneInfo("Asia/Kolkata"))
    now_est = datetime.now(ZoneInfo("America/New_York"))

    # Naive datetime (AVOID doesn't know its timezone)
    naive_now = datetime.now()  # Don't use this in production

    print(f"UTC:    {now_utc}")
    print(f"IST:    {now_ist}")
    print(f"EST:    {now_est}")
    print(f"Naive:  {naive_now} (avoid!)")

    return now_utc


# =============================================================================
# PARSING convert strings to datetime
# =============================================================================

def parse_datetimes():
    """Parse datetime strings in various formats."""
    # ISO 8601 (most common in APIs)
    iso_str = "2024-06-15T10:30:00+05:30"
    dt = datetime.fromisoformat(iso_str)  # Python 3.7+
    print(f"ISO 8601: {iso_str} → {dt}")

    # strptime parse with format string
    formats = [
        ("2024-06-15", "%Y-%m-%d"),
        ("15/06/2024", "%d/%m/%Y"),
        ("Jun 15, 2024 3:30 PM", "%b %d, %Y %I:%M %p"),
        ("2024-06-15 10:30:00", "%Y-%m-%d %H:%M:%S"),
        ("20240615", "%Y%m%d"),
    ]

    for date_str, fmt in formats:
        parsed = datetime.strptime(date_str, fmt)
        print(f"  '{date_str}' ({fmt}) → {parsed}")

    # Unix timestamp
    timestamp = 1718433000
    from_ts = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    print(f"\n  Unix {timestamp} → {from_ts}")

    return dt


# =============================================================================
# FORMATTING convert datetime to strings
# =============================================================================

def format_datetimes():
    """Format datetimes for display and APIs."""
    dt = datetime(2024, 6, 15, 10, 30, 0, tzinfo=ZoneInfo("Asia/Kolkata"))

    # Common formats
    formats = {
        "ISO 8601": dt.isoformat(),
        "Date only": dt.strftime("%Y-%m-%d"),
        "Readable": dt.strftime("%B %d, %Y at %I:%M %p"),
        "Short": dt.strftime("%d %b %Y"),
        "US style": dt.strftime("%m/%d/%Y"),
        "Time only": dt.strftime("%H:%M:%S %Z"),
        "RFC 2822": dt.strftime("%a, %d %b %Y %H:%M:%S %z"),
        "Filename safe": dt.strftime("%Y%m%d_%H%M%S"),
    }

    print("Formatting datetime:")
    for name, formatted in formats.items():
        print(f"  {name:15} → {formatted}")

    # To Unix timestamp
    timestamp = int(dt.timestamp())
    print(f"  {'Unix timestamp':15} → {timestamp}")


# =============================================================================
# TIMEZONE CONVERSIONS
# =============================================================================

def timezone_conversions():
    """Convert between timezones."""
    # Start with UTC
    utc_time = datetime(2024, 6, 15, 12, 0, 0, tzinfo=timezone.utc)
    print(f"UTC:       {utc_time}")

    # Convert to other zones
    zones = {
        "IST": "Asia/Kolkata",
        "EST": "America/New_York",
        "PST": "America/Los_Angeles",
        "JST": "Asia/Tokyo",
        "GMT": "Europe/London",
    }

    for label, zone_name in zones.items():
        local_time = utc_time.astimezone(ZoneInfo(zone_name))
        print(f"  {label}: {local_time.strftime('%Y-%m-%d %H:%M %Z')}")

    # Make a naive datetime timezone-aware
    naive = datetime(2024, 6, 15, 10, 30)
    aware = naive.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
    print(f"\n  Naive → Aware: {naive} → {aware}")

    # Convert aware to UTC
    in_utc = aware.astimezone(timezone.utc)
    print(f"  IST → UTC: {aware} → {in_utc}")


# =============================================================================
# TIMEDELTA arithmetic with dates and times
# =============================================================================

def time_arithmetic():
    """Date/time arithmetic with timedelta."""
    now = datetime.now(timezone.utc)

    # Basic arithmetic
    tomorrow = now + timedelta(days=1)
    next_week = now + timedelta(weeks=1)
    two_hours_ago = now - timedelta(hours=2)
    in_90_minutes = now + timedelta(minutes=90)

    print("Time arithmetic:")
    print(f"  Now:            {now.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Tomorrow:       {tomorrow.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Next week:      {next_week.strftime('%Y-%m-%d %H:%M')}")
    print(f"  2 hours ago:    {two_hours_ago.strftime('%Y-%m-%d %H:%M')}")
    print(f"  In 90 minutes:  {in_90_minutes.strftime('%Y-%m-%d %H:%M')}")

    # Difference between two datetimes
    start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end = datetime(2024, 12, 31, tzinfo=timezone.utc)
    diff = end - start

    print(f"\n  Days in 2024: {diff.days}")
    print(f"  Total seconds: {diff.total_seconds():,.0f}")

    # Business days calculation
    def add_business_days(start_date: date, days: int) -> date:
        """Add business days (skip weekends)."""
        current = start_date
        added = 0
        while added < days:
            current += timedelta(days=1)
            if current.weekday() < 5:  # Mon-Fri
                added += 1
        return current

    today = date.today()
    five_biz_days = add_business_days(today, 5)
    print(f"\n  Today: {today}")
    print(f"  +5 business days: {five_biz_days}")


# =============================================================================
# RELATIVE TIME "2 hours ago", "in 3 days"
# =============================================================================

def relative_time(dt: datetime, now: datetime = None) -> str:
    """Convert datetime to human-readable relative time.

    Like: "2 hours ago", "in 3 days", "just now"
    """
    if now is None:
        now = datetime.now(timezone.utc)

    diff = now - dt
    seconds = abs(diff.total_seconds())
    is_past = diff.total_seconds() > 0

    if seconds < 60:
        text = "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        text = f"{minutes} minute{'s' if minutes != 1 else ''}"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        text = f"{hours} hour{'s' if hours != 1 else ''}"
    elif seconds < 604800:
        days = int(seconds / 86400)
        text = f"{days} day{'s' if days != 1 else ''}"
    elif seconds < 2592000:
        weeks = int(seconds / 604800)
        text = f"{weeks} week{'s' if weeks != 1 else ''}"
    else:
        months = int(seconds / 2592000)
        text = f"{months} month{'s' if months != 1 else ''}"

    if text == "just now":
        return text
    return f"{text} ago" if is_past else f"in {text}"


# =============================================================================
# DATE RANGES AND PERIODS
# =============================================================================

def date_ranges():
    """Generate date ranges for reporting."""
    today = date.today()

    # This week (Monday to Sunday)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # This month
    start_of_month = today.replace(day=1)
    if today.month == 12:
        end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)

    # Last N days
    def last_n_days(n: int) -> list[date]:
        return [today - timedelta(days=i) for i in range(n - 1, -1, -1)]

    print("Date ranges:")
    print(f"  This week: {start_of_week} to {end_of_week}")
    print(f"  This month: {start_of_month} to {end_of_month}")
    print(f"  Last 7 days: {last_n_days(7)[0]} to {last_n_days(7)[-1]}")


if __name__ == "__main__":
    print("=" * 60)
    print("Datetime Utils Demo")
    print("=" * 60)

    print("\n--- Current Time ---")
    current_times()

    print("\n--- Parsing ---")
    parse_datetimes()

    print("\n--- Formatting ---")
    format_datetimes()

    print("\n--- Timezone Conversions ---")
    timezone_conversions()

    print("\n--- Time Arithmetic ---")
    time_arithmetic()

    print("\n--- Relative Time ---")
    now = datetime.now(timezone.utc)
    test_times = [
        now - timedelta(seconds=30),
        now - timedelta(minutes=45),
        now - timedelta(hours=3),
        now - timedelta(days=2),
        now + timedelta(hours=5),
    ]
    for t in test_times:
        print(f"  {t.strftime('%H:%M')} → {relative_time(t, now)}")

    print("\n--- Date Ranges ---")
    date_ranges()
