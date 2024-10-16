from django.utils import timezone


def to_local_time(utc_time: timezone.datetime) -> timezone.datetime:
    """Converts a UTC time to a local time.

    Args:
        utc_time: UTC time.

    Returns:
        Local time.
    """
    tz = timezone.get_current_timezone()
    return utc_time.astimezone(tz)


def to_utc_time(local_time: timezone.datetime) -> timezone.datetime:
    """Converts a local time to a UTC time.

    The time is ensured to be in the local timezone if naive.

    Args:
        local_time: Local time.

    Returns:
        UTC time.
    """
    if local_time.tzinfo is None:
        tz = timezone.get_current_timezone()
        local_time = local_time.replace(tzinfo=tz)
    return local_time.astimezone(timezone.utc)
