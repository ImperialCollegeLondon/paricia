from datetime import datetime
from decimal import Decimal

import pandas as pd
from django.utils import timezone

from measurement import reporting
from measurement.models import Measurement
from utilities.timezones import to_local_time
from variable.models import Variable


def get_data_to_validate(
    station: str,
    variable: str,
    start_time: str,
    end_time: str,
    is_validated: bool = False,
) -> pd.DataFrame:
    """Retrieves data to be validated.

    Args:
        station: Station of interest.
        variable: Variable of interest.
        start_time: Start time.
        end_time: End time.
        is_validated: Whether to retrieve validated or non-validated data.

    Returns:
        A dictionary with the report for the chosen days.
    """
    tz = timezone.get_current_timezone()
    start_time_ = datetime.strptime(start_time, "%Y-%m-%d").replace(tzinfo=tz)
    end_time_ = datetime.strptime(end_time, "%Y-%m-%d").replace(tzinfo=tz)

    df = pd.DataFrame.from_records(
        Measurement.objects.filter(
            station__station_code=station,
            variable__variable_code=variable,
            time__date__range=(start_time_.date(), end_time_.date()),
            is_validated=is_validated,
        ).values()
    )

    if df.empty:
        return df

    df["time"] = df["time"].dt.tz_convert(tz)
    return df.sort_values("time")


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
    allowed_difference: Decimal,
) -> pd.DataFrame:
    """Finds suspicious data in the database.

    Args:
        data: The dataframe with the data to be evaluated.
        maximum: The maximum allowed value.
        minimum: The minimum allowed value.
        allowed_difference: The allowed difference between the measurements.

    Returns:
        A dataframe with the suspicious data.
    """
    value_difference = flag_value_difference(data, allowed_difference)
    value_limits = flag_value_limits(data, maximum, minimum)
    return pd.concat([value_difference, value_limits], axis=1)


def flag_suspicious_daily_count(data: pd.Series, null_limit: Decimal) -> pd.DataFrame:
    """Finds suspicious records count for daily data.

    Args:
        data: The count of records per day.
        null_limit: The percentage of null data allowed.
    Returns:
        A dataframe with the suspicious data.
    """
    expected_data_count = data.mode().iloc[0]

    suspicious = pd.DataFrame(index=data.index)
    suspicious["daily_count_fraction"] = (data / expected_data_count).round(2)

    suspicious["suspicious_daily_count"] = (
        suspicious["daily_count_fraction"] < 1 - float(null_limit) / 100
    ) | (suspicious["daily_count_fraction"] > 1)

    return suspicious


def generate_daily_summary(
    data: pd.DataFrame,
    suspicious: pd.DataFrame,
    null_limit: Decimal,
    is_cumulative: bool,
) -> pd.DataFrame:
    """Generates a daily report of the data.

    Args:
        data: The dataframe with the data to be evaluated.
        suspicious: The dataframe with the suspicious data.
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
    count_report = flag_suspicious_daily_count(datagroup["value"].count(), null_limit)

    # Group the suspicious data by day and calculate the sum
    suspiciousgroup = suspicious.groupby(data.time.dt.date)
    suspicious_report = suspiciousgroup.sum().astype(int)
    suspicious_report["total_suspicious_entries"] = suspicious_report.sum(axis=1)

    # Put together the final report
    report = pd.concat([report, suspicious_report, count_report], axis=1)
    report = report.sort_index().reset_index().rename(columns={"index": "date"})
    report.date = pd.to_datetime(report.date)
    return report


def generate_validation_report(
    station: str,
    variable: str,
    start_time: str,
    end_time: str,
    maximum: Decimal,
    minimum: Decimal,
    is_validated: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generates a report of the data.

    Args:
        station: Station of interest.
        variable: Variable of interest.
        start_time: Start time.
        end_time: End time.
        maximum: The maximum allowed value.
        minimum: The minimum allowed value.
        is_validated: Whether to retrieve validated or non-validated data.

    Returns:
        A tuple with the summary report and the granular report.
    """
    var = Variable.objects.get(variable_code=variable)

    data = get_data_to_validate(station, variable, start_time, end_time, is_validated)
    if data.empty:
        return pd.DataFrame(), pd.DataFrame()

    suspicious = flag_suspicious_data(data, maximum, minimum, var.diff_error)
    summary = generate_daily_summary(
        data, suspicious, var.null_limit, var.is_cumulative
    )
    granular = pd.concat([data, suspicious], axis=1)
    return summary, granular


def save_validated_entries(data: pd.DataFrame) -> None:
    """Saves the validated data to the database.

    Only the data that is flagged as "validate?" will be saved. Possible updated fields
    are: value, maximum, minimum and is_active.

    Args:
        data: The dataframe with the validated data.
    """
    times: list[datetime] = []
    for _, row in data[data["validate?"]].iterrows():
        current = Measurement.objects.get(id=row["id"])
        times.append(current.time)

        update = {"is_validated": True, "is_active": not row["deactivate?"]}
        if current.value != row["value"]:
            update["value"] = row["value"]
        if "maximum" in row and current.maximum != row["maximum"]:
            update["maximum"] = row["maximum"]
        if "minimum" in row and current.minimum != row["minimum"]:
            update["minimum"] = row["minimum"]

        Measurement.objects.filter(id=row["id"]).update(**update)

    tz = timezone.get_current_timezone()
    station = current.station.station_code
    variable = current.variable.variable_code
    start_time = min(times).astimezone(tz).strftime("%Y-%m-%d")
    end_time = max(times).astimezone(tz).strftime("%Y-%m-%d")

    try:
        reporting.launch_reports_calculation(station, variable, start_time, end_time)
    except Exception as e:
        ids = data[data["validate?"]]["id"].tolist()
        reset_validated_entries(ids)
        raise e


def reset_validated_entries(ids: list) -> None:
    """Resets validation and activation status for the selected data.

    TODO: should this also reset any modified value, minimum or maximum entries?

    Args:
        ids (list): List of measurement ids to reset.
    """
    times: list[datetime] = []
    for _id in ids:
        current = Measurement.objects.get(id=_id)
        current.is_validated = False
        current.is_active = True
        current.save()
        times.append(current.time)

    station = current.station.station_code
    variable = current.variable.variable_code
    start_time, end_time = reporting.reformat_dates(
        to_local_time(min(times)).strftime("%Y-%m-%d"),
        to_local_time(max(times)).strftime("%Y-%m-%d"),
    )

    reporting.remove_report_data_in_range(station, variable, start_time, end_time)


def save_validated_days(data: pd.DataFrame) -> None:
    """Saves the validated days to the database and launches the report calculation.

    Only the data that is flagged as "validate?" will be saved. The only updated field
    is is_active. To update the value, maximum or minimum, use save_validated_entries.

    Args:
        data: The dataframe with the validated data.
    """
    tz = timezone.get_current_timezone()
    validate = data[data["validate?"]]
    for _, row in validate.iterrows():
        day = datetime.strptime(row["date"], "%Y-%m-%d").replace(tzinfo=tz)
        Measurement.objects.filter(
            station__station_code=row["station"],
            variable__variable_code=row["variable"],
            time__date=day.date(),
        ).update(is_validated=True, is_active=not row["deactivate?"])

    station = validate["station"].iloc[0]
    variable = validate["variable"].iloc[0]
    start_time = validate["date"].min()
    end_time = validate["date"].max()

    try:
        reporting.launch_reports_calculation(station, variable, start_time, end_time)
    except Exception as e:
        reset_validated_days(station, variable, start_time, end_time)
        raise e


def reset_validated_days(
    station: str, variable: str, start_date: str, end_date: str
) -> None:
    """Resets validation and active status for the selected data.

    It also deletes the associated report data.

    TODO: should this also reset any modified value, minimum or maximum entries?

    Args:
        station (str): Station code
        variable (str): Variable code
        start_date (str): Start date
        end_date (str): End date
    """
    tz = timezone.get_current_timezone()

    # To update we use the exact date range.
    start_date_ = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=tz)
    end_date_ = datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=tz)
    Measurement.objects.filter(
        station__station_code=station,
        variable__variable_code=variable,
        time__date__range=(start_date_.date(), end_date_.date()),
    ).update(is_validated=False, is_active=True)

    # To remove reports we use an extended date range to include the whole month.
    start_date_, end_date_ = reporting.reformat_dates(start_date, end_date)
    reporting.remove_report_data_in_range(station, variable, start_date_, end_date_)
