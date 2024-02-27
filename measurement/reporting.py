import zoneinfo
from datetime import datetime
from decimal import Decimal

import pandas as pd

from measurement.models import Measurement, Report
from station.models import DeltaT, Station
from variable.models import Variable


def calculate_reports(
    data: pd.DataFrame, station: str, variable: str, operation: str, period: Decimal
) -> pd.DataFrame:
    """Calculates the report for the chosen days.

    Args:
        data: The dataframe with the data.
        station: The name of the station.
        variable: The name of the variable.
        operation: Agreggation operation to perform on the data when calculating the
            report.
        period: The period of the data in minutes.

    Returns:
        A dataframe with the hourly, daily and monthly reports.
    """
    cols = ["time", "value"]
    if "maximum" in data.columns:
        cols.append("maximum")
    if "minimum" in data.columns:
        cols.append("minimum")

    # Calculate the reports
    hourly = data[cols].resample("H", on="time").agg(operation)
    daily = hourly.resample("D").agg(operation)
    monthly = daily.resample("MS").agg(operation)

    # Find the completeness of the data
    per_hour = 60 / period
    per_day = 24
    per_month = monthly.index.to_series().apply(
        lambda t: pd.Period(t, freq="S").days_in_month
    )
    hourly["completeness"] = (
        data[["time", "value"]].resample("H", on="time").count() / per_hour * 100
    )
    daily["completeness"] = hourly["value"].resample("D").count() / per_day * 100
    monthly["completeness"] = daily["value"].resample("MS").count() / per_month * 100

    # Put everything together
    hourly["report_type"] = "hourly"
    daily["report_type"] = "daily"
    monthly["report_type"] = "monthly"

    report = pd.concat([hourly, daily, monthly])
    report["station"] = station
    report["variable"] = variable

    return report


def reformat_dates(
    station: str,
    start_time: str,
    end_time: str,
) -> pd.Series:
    """Reformat dates so they have the right timezone and cover full days.

    The start date is always the first day of the first month and the end date is the
    last day of the last month. Times are set to 00:00:00 and 23:59:59, respectively,
    and the timezone is set to the station timezone.

    Args:
        station: Station of interest.
        variable: Variable of interest.
        start_time: Start time.
        end_time: End time.

    Returns:
        A series with the dates to be validated.
    """
    tz = zoneinfo.ZoneInfo(Station.objects.get(station_code=station).timezone)
    start_time_ = datetime.strptime(start_time, "%Y-%m-%d").replace(day=1, tzinfo=tz)
    end_time_ = (
        datetime.strptime(end_time, "%Y-%m-%d").replace(day=1, tzinfo=tz)
        + pd.DateOffset(months=1)
        - pd.DateOffset(seconds=1)
    )

    return start_time_, end_time_


def get_data_to_report(
    station: str,
    variable: str,
    start_time: datetime,
    end_time: datetime,
) -> pd.DataFrame:
    """Retrieves data to be reported about.

    It enforces to retrieve only active measurements and to use the station timezone.

    Args:
        station: Station of interest.
        variable: Variable of interest.
        start_time: Start time.
        end_time: End time.

    Returns:
        A dataframe with the data to report about.
    """
    tz = zoneinfo.ZoneInfo(Station.objects.get(station_code=station).timezone)

    return pd.DataFrame.from_records(
        Measurement.objects.filter(
            station__station_code=station,
            variable__variable_code=variable,
            time__gte=start_time.replace(tzinfo=tz),
            time__lte=end_time.replace(tzinfo=tz),
            is_active=True,
        ).values()
    )


def remove_report_data_in_range(
    station: str,
    variable: str,
    start_time: datetime,
    end_time: datetime,
) -> None:
    """Removes data in the range from the database.

    It enforces to use the station timezone.

    Args:
        station: Station of interest.
        variable: Variable of interest.
        start_time: Start time.
        end_time: End time.
    """
    tz = zoneinfo.ZoneInfo(Station.objects.get(station_code=station).timezone)

    Report.objects.filter(
        station__station_code=station,
        variable__variable_code=variable,
        time__gte=start_time.replace(tzinfo=tz),
        time__lte=end_time.replace(tzinfo=tz),
    ).delete()


def save_report_data(data: pd.DataFrame) -> None:
    """Saves the report data into the database.

    Before saving, the function removes maximum and minimum columns if they have all NaN
    and removes rows with NaN in the value column.

    Args:
        data: The dataframe with the report data.
    """
    data_ = data.dropna(axis=1, how="all").dropna(axis=0, subset=["value"])
    Report.objects.bulk_create(
        [
            Report(
                station=Station.objects.get(station_code=row["station"]),
                variable=Variable.objects.get(variable_code=row["variable"]),
                time=time,
                value=row["value"],
                maximum=row.get("maximum", None),
                minimum=row.get("minimum", None),
                completeness=row["completeness"],
                report_type=row["report_type"],
            )
            for time, row in data_.iterrows()
        ]
    )


def get_report_data_from_db(
    station: str,
    variable: str,
    start_time: str,
    end_time: str,
    report_type: str,
) -> pd.DataFrame:
    """Retrieves the report data from the database.

    Time is set to the station timezone and the time range is inclusive of both
    start and end times.

    Args:
        station: Station of interest.
        variable: Variable of interest.
        start_time: Start time.
        end_time: End time.
        report_type: Type of report to retrieve.

    Returns:
        A dataframe with the report data.
    """
    start_time_, end_time_ = reformat_dates(station, start_time, end_time)

    return pd.DataFrame.from_records(
        Report.objects.filter(
            station__station_code=station,
            variable__variable_code=variable,
            time__gte=start_time_,
            time__lte=end_time_,
            report_type=report_type,
        ).values()
    ).rename(columns={"station_id": "station", "variable_id": "variable"})


def launch_reports_calculation(
    station: str,
    variable: str,
    start_time: str,
    end_time: str,
) -> None:
    """Launches the calculation of the reports.

    Time is set to the station timezone and the time range is inclusive of both
    start and end times.

    Args:
        station: Station of interest.
        variable: Variable of interest.
        start_time: Start time.
        end_time: End time.
    """
    operation = (
        "sum" if Variable.objects.get(variable_code=variable).is_cumulative else "mean"
    )
    period = DeltaT.objects.get(station__station_code=station).delta_t
    start_time_, end_time_ = reformat_dates(station, start_time, end_time)
    data = get_data_to_report(station, variable, start_time_, end_time_)
    report = calculate_reports(data, station, variable, operation, period)
    remove_report_data_in_range(station, variable, start_time_, end_time_)
    save_report_data(report)
