import zoneinfo
from datetime import datetime
from decimal import Decimal

import pandas as pd

from measurement.models import Measurement
from station.models import DeltaT, Station
from variable.models import Variable


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
    flags = pd.DataFrame(index=data.index, columns=["suspicious_time_lapse"])
    flags["suspicious_time_lapse"] = data.time.diff() != pd.Timedelta(f"{period}min")
    flags["suspicious_time_lapse"].iloc[0] = False
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
    flags = pd.DataFrame(index=data.index, columns=["suspicious_value_difference"])
    flags["suspicious_value_difference"] = data["value"].diff().abs() > float(
        allowed_difference
    )
    flags["suspicious_value_difference"].iloc[0] = False
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
        A dataframe with suspicious columns indicating a problem.
    """
    flags = pd.DataFrame(index=data.index)
    flags["suspicious_value_limits"] = (data["value"] < minimum) | (
        data["value"] > maximum
    )
    if "maximum" in data.columns:
        flags["suspicious_maximum_limits"] = (data["maximum"] < minimum) | (
            data["maximum"] > maximum
        )
    if "minimum" in data.columns:
        flags["suspicious_minimum_limits"] = (data["minimum"] < minimum) | (
            data["minimum"] > maximum
        )
    return flags


def flag_suspicious_data(
    data: pd.DataFrame,
    maximum: Decimal,
    minimum: Decimal,
    period: Decimal,
    allowed_difference: Decimal,
) -> pd.DataFrame:
    """Finds suspicious data in the database.

    Args:
        data: The dataframe with the data to be evaluated.
        maximum: The maximum allowed value.
        minimum: The minimum allowed value.
        period: The expected period for the measurements, in minutes.
        allowed_difference: The allowed difference between the measurements.

    Returns:
        A dataframe with the suspicious data.
    """
    time_lapse = flag_time_lapse_status(data, period)
    value_difference = flag_value_difference(data, allowed_difference)
    value_limits = flag_value_limits(data, maximum, minimum)
    return pd.concat([time_lapse, value_difference, value_limits], axis=1)


def flag_suspicious_daily_count(
    data: pd.Series, period: Decimal, null_limit: Decimal
) -> pd.DataFrame:
    """Finds suspicious records count for daily data.

    Args:
        data: The count of records per day.
        period: The expected period for the measurements, in minutes.
        null_limit: The percentage of null data allowed.

    Returns:
        A dataframe with the suspicious data.
    """
    expected_data_count = 24 * 60 / float(period)
    suspicious = pd.DataFrame(index=data.index)
    suspicious["daily_count_fraction"] = (data / expected_data_count).round(2)
    suspicious["suspicious_daily_count"] = ~suspicious["daily_count_fraction"].between(
        1 - float(null_limit) / 100, 1
    ) | (suspicious["daily_count_fraction"] > 1)

    return suspicious


def generate_daily_summary(
    data: pd.DataFrame,
    suspicious: pd.DataFrame,
    period: Decimal,
    null_limit: Decimal,
    is_cumulative: bool,
) -> pd.DataFrame:
    """Generates a daily report of the data.

    Args:
        data: The dataframe with the data to be evaluated.
        suspicious: The dataframe with the suspicious data.
        period: The expected period for the measurements, in minutes.
        null_limit: The percentage of null data allowed.
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

    # Count the number of entries per day and flag the suspicious ones
    count_report = flag_suspicious_daily_count(
        datagroup["value"].count(), period, null_limit
    )

    # Group the suspicious data by day and calculate the sum
    suspiciousgroup = suspicious.groupby(data.time.dt.date)
    suspicious_report = suspiciousgroup.sum().astype(int)
    suspicious_report["total_suspicious_entries"] = suspicious_report.sum(axis=1)

    # Put together the final report
    report = pd.concat([report, suspicious_report, count_report], axis=1)
    report.index = pd.to_datetime(report.index)
    return report


def generate_validation_report(
    station: str,
    variable: str,
    start_time: str,
    end_time: str,
    maximum: Decimal,
    minimum: Decimal,
    include_validated: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generates a report of the data.

    Args:
        station: Station of interest.
        variable: Variable of interest.
        start_time: Start time.
        end_time: End time.
        maximum: The maximum allowed value.
        minimum: The minimum allowed value.
        include_validated: If validated data should be included.

    Returns:
        A tuple with the summary report and the granular report.
    """
    period = DeltaT.objects.get(station__station_code=station).delta_t
    var = Variable.objects.get(variable_code=variable)

    data = get_data_to_validate(
        station, variable, start_time, end_time, include_validated
    )
    suspicious = flag_suspicious_data(data, maximum, minimum, period, var.diff_error)
    summary = generate_daily_summary(
        data, suspicious, period, var.null_limit, var.is_cumulative
    )
    granular = pd.concat([data, suspicious], axis=1)
    return summary, granular