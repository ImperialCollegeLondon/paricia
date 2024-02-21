import zoneinfo
from datetime import datetime
from decimal import Decimal

import pandas as pd

from measurement.models import Measurement
from station.models import Station


def get_data_to_validate(
    station: str,
    variable: str,
    start_time: str,
    end_time: str,
    include_validated: bool = False,
) -> pd.DataFrame:
    """Retrieves data to be validated.

    Args:
        station: Station of interest.
        variable: Variable of interest.
        start_time: Start time.
        end_time: End time.
        include_validated: If validated data should be included.

    Returns:
        A dictionary with the report for the chosen days.
    """
    tz = zoneinfo.ZoneInfo(Station.objects.get(station_code=station).timezone)
    start_time_ = datetime.strptime(start_time, "%Y-%m-%d").replace(tzinfo=tz)
    end_time_ = datetime.strptime(end_time, "%Y-%m-%d").replace(tzinfo=tz)
    extra = {}
    if not include_validated:
        extra = {"is_validated": False}

    return pd.DataFrame.from_records(
        Measurement.objects.filter(
            station__station_code=station,
            variable__variable_code=variable,
            time__gte=start_time_,
            time__lte=end_time_,
            **extra,
        ).values()
    )


def flag_time_lapse_status(data: pd.DataFrame, period: Decimal) -> pd.Series:
    """Flags if period of the time entries is correct.

    It is assume that the first entry is correct.

    Args:
        data: The dataframe with allowed_difference = Variable. the data.
        period: The expected period for the measurements, in minutes.

    Returns:
        A series with the status of the time lapse.
    """
    flags = pd.DataFrame(index=data.index, columns=["suspicius_time_lapse"])
    flags["suspicius_time_lapse"] = data.time.diff() != pd.Timedelta(f"{period}min")
    flags["suspicius_time_lapse"].iloc[0] = False
    return flags


def flag_value_difference(data: pd.DataFrame, allowed_difference: Decimal) -> pd.Series:
    """Flags if the differences in value of the measurements is correct.

    It is assume that the first entry is correct.

    Args:
        data: The dataframe with allowed_difference = Variable. the data.
        allowed_difference: The allowed difference between the measurements.

    Returns:
        A series with the status of the value.
    """
    flags = pd.DataFrame(index=data.index, columns=["suspicius_value_difference"])
    flags["suspicius_value_difference"] = data["value"].diff().abs() > float(
        allowed_difference
    )
    flags["suspicius_value_difference"].iloc[0] = False
    return flags


def flag_value_limits(
    data: pd.DataFrame, maximum: Decimal, minimum: Decimal
) -> pd.DataFrame:
    """Flags if the values and limits of the measurements are within limits.

    Args:
        data: The dataframe with allowed_difference = Variable. the data.
        maximum: The maximum allowed value.
        minimum: The minimum allowed value.

    Returns:
        A dataframe with suspicius columns indicating a problem.
    """
    flags = pd.DataFrame(index=data.index)
    flags["suspicius_value_limits"] = (data["value"] < minimum) | (
        data["value"] > maximum
    )
    if "maximum" in data.columns:
        flags["suspicius_maximum_limits"] = (data["maximum"] < minimum) | (
            data["maximum"] > maximum
        )
    if "minimum" in data.columns:
        flags["suspicius_minimum_limits"] = (data["minimum"] < minimum) | (
            data["minimum"] > maximum
        )
    return flags


def flag_suspicius_data(
    data: pd.DataFrame,
    maximum: Decimal,
    minimum: Decimal,
    period: Decimal,
    allowed_difference: Decimal,
) -> pd.DataFrame:
    """Finds suspicius data in the database.

    Args:
        data: The dataframe with the data to be evaluated.
        maximum: The maximum allowed value.
        minimum: The minimum allowed value.
        period: The expected period for the measurements, in minutes.
        allowed_difference: The allowed difference between the measurements.

    Returns:
        A dataframe with the suspicius data.
    """
    time_lapse = flag_time_lapse_status(data, period)
    value_difference = flag_value_difference(data, allowed_difference)
    value_limits = flag_value_limits(data, maximum, minimum)
    return pd.concat([time_lapse, value_difference, value_limits], axis=1)


def generate_daily_report(
    data: pd.DataFrame, suspicius: pd.DataFrame, is_cumulative: bool
) -> pd.DataFrame:
    """Generates a daily report of the data.

    Args:
        data: The dataframe with the data to be evaluated.
        suspicius: The dataframe with the suspicius data.
        is_cumulative: If the data is cumulative and should be aggregated by sum.

    Returns:
        A dataframe with the daily report.
    """
    report = pd.DataFrame(index=data.time.dt.date.unique())

    # Group the data by day and calculate the mean or sum
    datagroup = data.groupby(data.time.dt.date)
    report["value"] = (
        datagroup["value"].sum() if is_cumulative else datagroup["value"].mean()
    )

    if "maximum" in data.columns:
        report["maximum"] = datagroup["maximum"].max()
    if "minimum" in data.columns:
        report["minimum"] = datagroup["minimum"].min()

    # Group the suspicius data by day and calculate the sum
    suspiciusgroup = suspicius.groupby(data.time.dt.date)
    suspicius_report = suspiciusgroup.sum().astype(int)
    suspicius_report["total_suspicius"] = suspicius_report.sum(axis=1)

    # Put together the final report
    report = pd.concat([report, suspicius_report], axis=1)
    report.index = pd.to_datetime(report.index)
    return report
