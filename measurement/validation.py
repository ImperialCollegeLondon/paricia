import zoneinfo
from datetime import datetime

import pandas as pd

from measurement.models import Measurement
from station.models import Station


def get_data_to_validate(
    station: str, variable: str, start_time: str, end_time: str
) -> pd.DataFrame:
    """Retrieves data to be validated.

    Args:
        station: Station of interest.
        variable: Variable of interest.
        start_time: Start time.
        end_time: End time.

    Returns:
        A dictionary with the report for the chosen days.
    """
    tz = zoneinfo.ZoneInfo(Station.objects.get(station_code=station).timezone)
    start_time_ = datetime.strptime(start_time, "%Y-%m-%d").replace(tzinfo=tz)
    end_time_ = datetime.strptime(end_time, "%Y-%m-%d").replace(tzinfo=tz)
    data = pd.DataFrame.from_records(
        Measurement.objects.filter(
            station__station_code=station,
            variable__variable_code=variable,
            time__gte=start_time_,
            time__lte=end_time_,
            is_validated=False,
        ).values()
    )
    return data
