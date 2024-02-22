from decimal import Decimal

import pandas as pd


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
