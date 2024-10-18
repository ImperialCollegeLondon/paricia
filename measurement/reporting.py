import zoneinfo
from datetime import datetime
from functools import lru_cache

import pandas as pd

from importing.models import DataImport
from measurement.models import Measurement, Report
from station.models import Station
from variable.models import Variable


def calculate_reports(
    data: pd.DataFrame, station: str, variable: str, operation: str
) -> pd.DataFrame:
    """Calculates the report for the chosen days.

    Args:
        data: The dataframe with the data.
        station: The name of the station.
        variable: The name of the variable.
        operation: Aggregation operation to perform on the data when calculating the
            report.

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

    # Get the right data_import for each period. We use the mode to get the most common
    # data_import value in the period.
    def mode(x: pd.Series) -> str | None:
        modes = x.mode()
        return modes[0] if not modes.empty else None

    cols2 = ["time", "data_import_id"]
    hourly["data_import_id"] = data[cols2].resample("H", on="time").agg(mode)
    daily["data_import_id"] = data[cols2].resample("D", on="time").agg(mode)
    monthly["data_import_id"] = data[cols2].resample("MS", on="time").agg(mode)

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
    data_import_avail = "data_import_id" in data_.columns
    Report.objects.bulk_create(
        [
            Report(
                data_import=DataImport.objects.get(pk=row["data_import_id"])
                if data_import_avail and not pd.isna(row["data_import_id"])
                else None,
                station=Station.objects.get(station_code=row["station"]),
                variable=Variable.objects.get(variable_code=row["variable"]),
                time=time,
                value=row["value"],
                maximum=row.get("maximum", None),
                minimum=row.get("minimum", None),
                report_type=row["report_type"],
            )
            for time, row in data_.iterrows()
        ]
    )


@lru_cache
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

    if report_type == "measurement":
        data = pd.DataFrame.from_records(
            Measurement.objects.filter(
                station__station_code=station,
                variable__variable_code=variable,
                time__gte=start_time_,
                time__lte=end_time_,
            ).values()
        )
        raw_cols = [col for col in data.columns if col.startswith("raw_")]
        normal = [col.strip("raw_") for col in raw_cols]
        data = data.drop(columns=normal).rename(columns=dict(zip(raw_cols, normal)))

    elif report_type == "validated":
        data = pd.DataFrame.from_records(
            Measurement.objects.filter(
                station__station_code=station,
                variable__variable_code=variable,
                time__gte=start_time_,
                time__lte=end_time_,
                is_validated=True,
                is_active=True,
            ).values()
        )
        raw_cols = [col for col in data.columns if col.startswith("raw_")]
        data = data.drop(columns=raw_cols)

    else:
        data = pd.DataFrame.from_records(
            Report.objects.filter(
                station__station_code=station,
                variable__variable_code=variable,
                time__gte=start_time_,
                time__lte=end_time_,
                report_type=report_type,
            ).values()
        )

    data = data.rename(columns={"station_id": "station", "variable_id": "variable"})
    if not data.empty:
        data = data.sort_values("time")

    return data


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

    start_time_, end_time_ = reformat_dates(station, start_time, end_time)
    data = get_data_to_report(station, variable, start_time_, end_time_)
    report = calculate_reports(data, station, variable, operation)
    remove_report_data_in_range(station, variable, start_time_, end_time_)
    save_report_data(report)
