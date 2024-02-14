import enum
import zoneinfo
from datetime import datetime

import numpy as np
import pandas as pd

from measurement.models import Measurement
from station.models import Station


class TimeLapseStatus(enum.Enum):
    OK = "ok"
    TOO_LARGE = "too_large"
    TOO_SMALL = "too_small"
    NAN = np.NAN

    @classmethod
    def evaluate(cls, value: float) -> "TimeLapseStatus":
        """Returns the status of the time lapse.

        Args:
            value (float): The value to evaluate.

        Returns:
            TimeLapseStatus: The associated time lapse status.
        """
        if np.isclose(value, 1):
            return cls.OK
        elif value > 1:
            return cls.TOO_LARGE
        elif value < 1:
            return cls.TOO_SMALL
        else:
            return cls.NAN


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


def flag_time_lapse_status(data: pd.DataFrame, period: float) -> pd.Series:
    """Verifies if period of the time entries is correct, labelling them appropriately.

    Args:
        data: The dataframe with all the data.
        period: The expected period for the measurements, in minutes.

    Returns:
        A series with the status of the time lapse.
    """
    return (data.time.diff().dt.total_seconds() / 60 / period).apply(
        TimeLapseStatus.evaluate
    )
