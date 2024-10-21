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
