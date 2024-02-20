import enum
import zoneinfo
from datetime import datetime
from decimal import Decimal

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


class ValueStatus(enum.Enum):
    OK = "ok"
    TOO_LARGE = "too_large"
    NAN = np.NAN

    @classmethod
    def evaluate(cls, value: float, allowed_difference: Decimal) -> "ValueStatus":
        """Returns the status of the value.

        Args:
            value (float): The value to evaluate.

        Returns:
            ValueStatus: The associated value status.
        """
        val = abs(value)
        diff = float(allowed_difference)
        if val <= diff:
            return cls.OK
        elif val > diff:
            return cls.TOO_LARGE
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
    """Flags if period of the time entries is correct.

    Args:
        data: The dataframe with all the data.
        period: The expected period for the measurements, in minutes.

    Returns:
        A series with the status of the time lapse.
    """
    flags = pd.DataFrame(index=data.index, columns=["suspicius_time_lapse"])
    flags["suspicius_time_lapse"] = data.time.diff() == pd.Timedelta(f"{period}min")
    flags["suspicius_time_lapse"][0] = True
    return flags


def flag_value_difference(data: pd.DataFrame, allowed_difference: Decimal) -> pd.Series:
    """Flags if the differences in value of the measurements is correct.

    Args:
        data: The dataframe with all the data.
        allowed_difference: The allowed difference between the measurements.

    Returns:
        A series with the status of the value.
    """
    flags = pd.DataFrame(index=data.index, columns=["suspicius_value_difference"])
    flags["suspicius_value_difference"] = (
        data["value"].diff().abs() > allowed_difference
    )
    flags["suspicius_value_difference"][0] = True
    return flags


def flag_value_limits(
    data: pd.DataFrame, maximum: Decimal, minimum: Decimal
) -> pd.DataFrame:
    """Flags if the values and limits of the measurements are within limits.

    Args:
        data: The dataframe with all the data.
        maximum: The maximum allowed value.
        minimum: The minimum allowed value.

    Returns:
        A dataframe with suspicius columns indicating a problem.
    """
    flags = pd.DataFrame(index=data.index)
    flags["suspicius_value"] = (data["value"] < minimum) | (data["value"] > maximum)
    if "maximum" in data.columns:
        flags["suspicius_maximum"] = (data["maximum"] < minimum) | (
            data["maximum"] > maximum
        )
    if "minimum" in data.columns:
        flags["suspicius_minimum"] = (data["minimum"] < minimum) | (
            data["minimum"] > maximum
        )
    return flags
