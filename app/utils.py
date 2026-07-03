"""
Shared application helpers.
"""
import os
from datetime import datetime, timedelta, timezone

# Display timezone offset from UTC, in hours. The system stores naive local
# timestamps; keeping the offset in one place (overridable via the
# TZ_OFFSET_HOURS environment variable) avoids the hard-coded "+2 hours"
# arithmetic that was previously scattered across modules.
LOCAL_UTC_OFFSET_HOURS = float(os.environ.get('TZ_OFFSET_HOURS', 2))


def now_local() -> datetime:
    """
    Current timestamp in the configured local timezone, returned naive
    (tzinfo stripped) to match how the ORM columns store datetimes.
    """
    return (datetime.now(timezone.utc)
            + timedelta(hours=LOCAL_UTC_OFFSET_HOURS)).replace(tzinfo=None)
