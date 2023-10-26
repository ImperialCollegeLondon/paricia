import calendar
from datetime import date, datetime, time
from threading import Thread
from typing import Tuple, Union, overload, Sequence, List, Dict, Any
from decimal import Decimal

import numpy as np
import pandas as pd
from django.apps import apps
from django.db.models import BooleanField, Value
import logging

from station.models import DeltaT, Station
from variable.models import Variable

threads_report_calculation = []

ALLOWED_FIELDS = ("sum", "minimum", "maximum", "average", "value")

logger = logging.getLogger(__name__)


@overload
def set_time_limits(start_time: str, end_time: str) -> Tuple[str, str]:
    ...


@overload
def set_time_limits(
    start_time: datetime, end_time: datetime
) -> Tuple[datetime, datetime]:
    ...


def set_time_limits(start_time, end_time):
    """Complete the datetime objects to cover a whole day.

    Completes the hour in start_date and end_date in order to have a whole day from the
    first hour (00:00:00) to the last hour of the day (23:59:59)

    Args:
        start_time: The start date, where the time will be set as 00:00:00
        end_time: The end date, where the time will be set as 00:00:00

    Returns:
        A tuple with the same objects updated
    """
    if isinstance(start_time, date):
        start_time = datetime.combine(start_time, time(0, 0, 0, 0))
    elif isinstance(start_time, str):
        start_time = start_time + " 00:00:00"

    if isinstance(end_time, date):
        end_time = datetime.combine(end_time, time(23, 59, 59, 999999))
    elif isinstance(end_time, str):
        end_time = end_time + " 23:59:59"

    return start_time, end_time


def daily_validation(
    station: Station,
    variable: Variable,
    start_time: Union[datetime, str],
    end_time: Union[datetime, str],
    minimum: Decimal,
    maximum: Decimal,
):
    """Generates a daily report and formats the data to be displayed in tables.

    Args:
        station: Station of interest.
        variable: Variable of interest.
        start_time: Start time.
        end_time: End time.
        maximum: Maximum value expected for the variable.
        minimum: Minimum value expected for the variable.

    Returns:
        A dictionary response for main Validation interface containing the daily report
        of values and statistics, indicators, time series for plot, variable and station
        information
    """
    num_maximum = None
    num_minimum = None

    report, selected, measurement, validated = daily_report(
        station, variable, start_time, end_time, minimum, maximum
    )
    value_columns = list(measurement.columns.to_numpy())
    value_columns.remove("time")

    for var in ("value", "average", "sum"):
        if var in value_columns:
            break

    num_date = len(
        report[report["date_error"].ne(1) & ~report["date_error"].isna()].index
    )
    num_percentage = len(report[report["percentage_error"].eq(True)])
    num_value = len(
        report[
            report["percentage_error"].eq(False)
            & ~report[f"suspicious_{var}s_count"].isna()
        ]
    )
    if "maximum" in value_columns:
        num_maximum = len(
            report[
                report["percentage_error"].eq(False)
                & ~report["suspicious_maximums_count"].isna()
            ]
        )
    if "minimum" in value_columns:
        num_minimum = len(
            report[
                report["percentage_error"].eq(False)
                & ~report["suspicious_minimums_count"].isna()
            ]
        )
    num_days = len(report.index)

    data = {
        "station": {
            "id": station.station_id,
            "name": station.station_name,
        },
        "variable": {
            "id": variable.variable_id,
            "name": variable.name,
            "maximum": variable.maximum,
            "minimum": variable.minimum,
            "unit_initials": variable.unit.initials,
            "is_cumulative": variable.is_cumulative,
        },
        "value_columns": value_columns,
        "data": report.fillna("").to_dict(orient="records"),
        "indicators": {
            "num_date": num_date,
            "num_percentage": num_percentage,
            "num_value": num_value,
            "num_maximum": num_maximum,
            "num_minimum": num_minimum,
            "num_days": num_days,
        },
        "series": {
            "selected": selected.fillna("").to_dict("list"),
            "measurement": measurement.fillna("").to_dict("list"),
            "validated": validated.fillna("").to_dict("list"),
        },
    }
    return data


def validated_to_df(
    station: Station,
    variable: Variable,
    start_time: datetime,
    end_time: datetime,
) -> pd.DataFrame:
    """Extracts validated data of a variable within date range into a dataframe.

    Also annotates the objects to indicate that they have been validated.

    Args:
        station: Station of interest.
        variable: Variable of interest.
        start_time: Start time.
        end_time: End time.

    Returns:
        A pandas Dataframe with the requested data.
    """
    validated = apps.get_model(app_label="validated", model_name=variable.variable_code)

    validated = (
        validated.objects.filter(
            station_id=station.station_id, time__gte=start_time, time__lte=end_time
        )
        .annotate(
            is_validated=Value(True, output_field=BooleanField()),
            exists_in_validated=Value(True, output_field=BooleanField()),
            null_value=Value(False, output_field=BooleanField()),
        )
        .order_by("time")
    )

    data_columns = [e.name for e in validated.model._meta.fields]
    value_fields = [e for e in data_columns if e in ALLOWED_FIELDS]
    base_fields = ["id", "time", "is_validated", "exists_in_validated", "null_value"]
    fields = base_fields + value_fields
    validated = pd.DataFrame.from_records(validated.values(*fields))

    if validated.empty:
        validated = pd.DataFrame(columns=fields)

    validated["time_truncated"] = validated["time"].values.astype("<M8[m]")

    return validated


def measurement_to_df(
    station: Station,
    variable: Variable,
    start_time: datetime,
    end_time: datetime,
) -> pd.DataFrame:
    """Extracts measurement data of a variable within date range into a dataframe.

    Also annotates the objects to indicate that they have not been validated.

    Args:
        station: Station of interest.
        variable: Variable of interest.
        start_time: Start time.
        end_time: End time.

    Returns:
        A pandas Dataframe with the requested data.
    """
    measurement = apps.get_model(
        app_label="measurement", model_name=variable.variable_code
    )

    measurement = (
        measurement.objects.filter(
            station_id=station.station_id, time__gte=start_time, time__lte=end_time
        )
        .annotate(
            is_validated=Value(False, output_field=BooleanField()),
        )
        .order_by("time")
    )

    data_columns = [e.name for e in measurement.model._meta.fields]
    value_fields = [e for e in data_columns if e in ALLOWED_FIELDS]
    base_fields = ["id", "time", "is_validated"]
    fields = base_fields + value_fields
    measurement = pd.DataFrame.from_records(measurement.values(*fields))

    if measurement.empty:
        measurement = pd.DataFrame(columns=fields)

    measurement["time_truncated"] = measurement["time"].values.astype("<M8[m]")

    return measurement


def join_data_and_preprocess(
    data: Sequence[pd.DataFrame], maximum: Decimal, minimum: Decimal, fields: Sequence
) -> pd.DataFrame:
    """Joins data frames and perform some validation of the data limits.

    Args:
        data: List of data frames to join and pre-process together.
        maximum: Maximum value expected for the variable.
        minimum: Minimum value expected for the variable.
        fields: Data fields that are expected in this data.

    Returns:
        The joint data frame.
    """
    joined = pd.concat(data).sort_values(
        by=["time_truncated", "is_validated", "id"], ascending=[True, False, False]
    )
    joined["date"] = pd.to_datetime(joined["time"]).dt.date
    joined.rename(columns={"id": "db_row_id"}, inplace=True)
    joined.reset_index(drop=True, inplace=True)
    joined.index.name = "id_joined"
    joined.reset_index(inplace=True)

    joined["suspicious_value"] = np.where(
        (joined["value"] < minimum) | (joined["value"] > maximum), True, False
    )
    if "maximum" in fields:
        joined["suspicious_maximum"] = np.where(
            (joined["maximum"] < minimum) | (joined["maximum"] > maximum), True, False
        )
    if "minimum" in fields:
        joined["suspicious_minimum"] = np.where(
            (joined["minimum"] < minimum) | (joined["minimum"] > maximum), True, False
        )

    return joined


def select_values(joined: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Select the first values with a given time, labelling them in the dataframe.

    When the times are truncated to the appropriate resolution, several entries might
    have the same time. This function selects only the first of such duplicated entries,
    providing as output the original dataframe with the selected entries labelled and
    also the selected entries themselves as a separate dataframe.

    Args:
        joined: The data frame with all the data.

    Returns:
        The joined dataframe with the selected entries labelled and the dataframe only
        with the selected entries.
    """
    selected = joined.drop_duplicates("time_truncated", keep="first").copy()
    selected.reset_index(drop=True, inplace=True)
    selected["is_selected"] = True
    joined = joined.merge(
        selected[["id_joined", "is_selected"]],
        on="id_joined",
        how="left",
        indicator=False,
    )
    joined["is_selected"].fillna(False, inplace=True)
    return joined, selected


def verify_time_lapse_status(
    joined: pd.DataFrame, selected: pd.DataFrame, period: float
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Verifies if period of the time entries is correct, labelling them appropriately.

    Args:
        joined: The full dataframe with the joined data.
        selected: The subset of the selected data.
        period: The expected period for the measurements.

    Returns:
        Both input arrays with updated columns:
            - time_lapse: with the time separation between entries.
            - time_lapse_status: flag that indicates if the period is correct (1), too
                small (0) or too large (2)
            - lagged_value: with the variable value of the next record, used to identify
                suspicious changes in value.
    """
    selected["time_lapse"] = selected["time_truncated"] - selected[
        "time_truncated"
    ].shift(1)
    selected["time_lapse"] = selected["time_lapse"].dt.total_seconds() / 60
    selected["time_lapse_status"] = 1
    selected.loc[selected["time_lapse"] < period, "time_lapse_status"] = 0
    selected.loc[selected["time_lapse"] > period, "time_lapse_status"] = 2

    selected["lagged_value"] = np.where(
        selected["time_lapse_status"].le(1),
        selected["value"].shift(1),
        np.nan,
    )

    joined = joined.merge(
        selected[["time_truncated", "time_lapse", "time_lapse_status", "lagged_value"]],
        on="time_truncated",
        how="left",
        indicator=False,
    )

    return joined, selected


def flag_value_difference_error(
    joined: pd.DataFrame, diff_error: Decimal
) -> pd.DataFrame:
    """Identifies suspicious values based on the difference with the lagged ones.

    Args:
        joined: The full dataframe with the joined data.
        diff_error: The value difference allowed for this variable.

    Returns:
        The input arrays with two new columns:
            - value_difference: With the difference in values.
            - value_difference_error: Flag indicating if the difference is significant.
    """
    joined["value_difference"] = joined["value"] - joined["lagged_value"]
    joined["value_difference_error"] = joined["value_difference"].abs().gt(diff_error)
    return joined


def normalize_column_names(data: Sequence[pd.DataFrame], old: str, new: str) -> None:
    """Switch column names between two patterns.

    Used to normalize dataframes to a common column names pattern before a calculation
    and returning them to the correct names afterward.

    Args:
        data: List of dataframes to be normalized.
        old: The string to be looked for in the column names.
        new: The replacement.
    """
    for df in data:
        for col in list(df):
            if old in col and col not in ("value_difference_error", "value_difference"):
                df.rename(columns={col: col.replace(old, new)}, inplace=True)


def verify_validated(validated: pd.DataFrame, measurement: pd.DataFrame) -> pd.Series:
    """Labels those entries in measurement that have already been validated.

    Args:
        validated: Dataframe with validated data.
        measurement: Dataframe with raw measurements.

    Returns:
        A series with flags indicating which entries have already been validated.
    """
    matches_time = pd.merge(
        measurement, validated, on=["time_truncated"], how="outer", indicator=True
    )
    return matches_time["_merge"] == "both"


def preprocessing(
    station: Station,
    variable: Variable,
    start_time: Union[datetime, str],
    end_time: Union[datetime, str],
    minimum: Decimal,
    maximum: Decimal,
):
    """Returns sub-hourly tables with some validation information

    It is used in main report for Validation interface, and it is also called for
    "save_to_validated" function/request.

    Args:
        station: Station of interest.
        variable: Variable of interest.
        start_time: Start time.
        end_time: End time.
        maximum: Maximum value expected for the variable.
        minimum: Minimum value expected for the variable.

    Returns:
        Returns a tuple with the following Dataframes and processed data:
            - measurement: DataFrame with the raw measurement data in the interval.
            - validated: Dataframe with the validated data in the interval.
            - selected_full: All validated data and that still to be validated,
                without duplicate timestamps.
            - selected: Selected data without duplicate time stamps.
            - tx_period (Decimal): The expected period for the measurements.
            - value_fields: Data fields that are expected in this data.
    """
    tx_period = DeltaT.objects.get(station__station_id=station.station_id).delta_t

    validated = validated_to_df(station, variable, start_time, end_time)
    measurement = measurement_to_df(station, variable, start_time, end_time)
    measurement["exists_in_validated"] = verify_validated(validated, measurement)

    value_fields = [v for v in validated.columns if v in ALLOWED_FIELDS]
    if "sum" in value_fields:
        normalize_column_names([measurement, validated], "sum", "value")
    elif "average" in value_fields:
        normalize_column_names([measurement, validated], "average", "value")

    joined = join_data_and_preprocess(
        [validated, measurement], maximum, minimum, value_fields
    )
    joined, selected = select_values(joined)
    joined, selected = verify_time_lapse_status(joined, selected, tx_period)
    joined = flag_value_difference_error(joined, variable.diff_error)

    if "sum" in value_fields:
        normalize_column_names(
            [measurement, validated, joined, selected], "value", "sum"
        )
    elif "average" in value_fields:
        normalize_column_names(
            [measurement, validated, joined, selected], "value", "average"
        )

    # Final Filter: If a data is already validated, do not show "Measurement" values for that timestamp
    selected_full = joined.loc[
        (joined["is_validated"] & joined["exists_in_validated"])
        | (~joined["is_validated"] & ~joined["exists_in_validated"])
    ].copy()

    selected_full.reset_index(inplace=True, drop=True)
    selected_full.insert(0, "id", selected_full.index)
    selected.reset_index(inplace=True, drop=True)
    selected.insert(0, "id", selected.index)

    return measurement, validated, selected_full, selected, tx_period, value_fields


def create_daily_df(
    selected: pd.DataFrame,
    selected_full: pd.DataFrame,
    principal_field: str,
    maximum: bool,
    minimum: bool,
    tx_period: Decimal,
    null_limit: Decimal,
) -> pd.DataFrame:
    """Summarises the data available in daily entries.

    Args:
        selected: Selected data without duplicate time stamps.
        selected_full: All validated data and that still to be validated,
            without duplicate timestamps.
        principal_field: Principal field with the value (value, average or sum),
            depending on what is relevant for the magnitude.
        maximum: If there is a maximum field.
        minimum: If there is a minimum field.
        tx_period: Expected period of the measurements.
        null_limit: The max % of null values data. Cumulative values are not deemed
            trustworthy if the number of missing values in a given period > null_limit.

    Returns:
        Dataframe with the report for the chosen days.
    """
    daily_group_all = selected_full.groupby("date")
    daily_group = selected.groupby("date")

    daily = daily_group_all[principal_field].count()
    daily = daily.reset_index(name="data_count")

    # Calculate daily principal magnitude
    if principal_field == "sum":
        daily[principal_field] = (
            daily_group[principal_field].sum(min_count=1).to_numpy()
        )
    else:
        daily[principal_field] = daily_group[principal_field].mean().to_numpy()

    daily[f"suspicious_{principal_field}s_count"] = (
        daily_group[f"suspicious_{principal_field}"].sum().to_numpy()
    )

    # And daily maximum and minimum
    if maximum:
        daily["maximum"] = daily_group["maximum"].max().to_numpy()
        daily[f"suspicious_maximums_count"] = (
            daily_group[f"suspicious_maximum"].sum().to_numpy()
        )
    if minimum:
        daily["minimum"] = daily_group["minimum"].min().to_numpy()
        daily[f"suspicious_minimums_count"] = (
            daily_group[f"suspicious_minimum"].sum().to_numpy()
        )

    daily["all_validated"] = daily_group["is_validated"].all().to_numpy()

    # TODO Create a "period" table for storing the period for every station
    # TODO Maybe program for dynamic periods. This happens when a station change the period
    expected_data_count = 24 * 60 / tx_period
    daily["percentage"] = (daily["data_count"] / expected_data_count) * 100.0
    daily["percentage_error"] = ~daily["percentage"].between(
        100.0 - float(null_limit), 100.0
    )
    daily["value_difference_error_count"] = (
        daily_group_all["value_difference_error"].sum(numeric_only=False).to_numpy()
    )

    daily["day_interval"] = (daily["date"] - daily["date"].shift(1)).dt.days
    daily.loc[0, "day_interval"] = 1
    daily["date_error"] = np.where(daily["day_interval"].gt(1), 3, 1)
    # TODO hacer un groupby de repeated_values_count por día, para pasar el valor total de repetidos por día
    #      posiblemente convenga hacer un solo cálculo arriba
    # TODO explain what the error numbers mean. 1 = OK, but what 3 means?

    return daily


def calculate_extra_data_daily(
    validated: pd.DataFrame, measurement: pd.DataFrame
) -> pd.DataFrame:
    """Calculate extra data inputs in the daily report.

    Args:
        validated: Dataframe with the validated data in the interval.
        measurement: DataFrame with the raw measurement data in the interval.

    Returns:
        Dataframe with the extra entries per date.
    """
    repeated_in_validated = validated.groupby(["time_truncated"])[
        "time_truncated"
    ].count()
    repeated_in_validated = repeated_in_validated.reset_index(
        name="repeated_in_validated"
    )
    repeated_in_validated["repeated_in_validated"] = np.where(
        repeated_in_validated["repeated_in_validated"].gt(0),
        repeated_in_validated["repeated_in_validated"] - 1,
        0,
    )

    repeated_in_measurement = measurement.groupby(["time_truncated"])[
        "time_truncated"
    ].count()
    repeated_in_measurement = repeated_in_measurement.reset_index(
        name="repeated_in_measurement"
    )
    repeated_in_measurement["repeated_in_measurement"] = np.where(
        repeated_in_measurement["repeated_in_measurement"].gt(0),
        repeated_in_measurement["repeated_in_measurement"] - 1,
        0,
    )
    extra_data_count = pd.merge(
        repeated_in_validated,
        repeated_in_measurement,
        on=["time_truncated"],
        how="outer",
        indicator=False,
    )
    extra_data_count.fillna(0, inplace=True)
    extra_data_count.sort_values(by=["time_truncated"], inplace=True)
    extra_data_count["extra_values_count"] = (
        extra_data_count["repeated_in_validated"]
        + extra_data_count["repeated_in_measurement"]
    )
    extra_data_count["date"] = pd.to_datetime(
        extra_data_count["time_truncated"]
    ).dt.date

    extra_data_daily_group = extra_data_count[
        extra_data_count["extra_values_count"] > 0
    ].groupby("date")

    return (
        extra_data_daily_group["extra_values_count"]
        .sum()
        .reset_index(name="extra_data_count")
    )


def daily_report(
    station: Station,
    variable: Variable,
    start_time: Union[datetime, str],
    end_time: Union[datetime, str],
    minimum: Decimal,
    maximum: Decimal,
):
    """Calculate daily report that will be sent to main Validation interface.

    Args:
        station: Station of interest.
        variable: Variable of interest.
        start_time: Start time.
        end_time: End time.
        maximum: Maximum value expected for the variable.
        minimum: Minimum value expected for the variable.
    """
    start_time, end_time = set_time_limits(start_time, end_time)
    (
        measurement,
        validated,
        selected_full,
        selected,
        tx_period,
        value_fields,
    ) = preprocessing(station, variable, start_time, end_time, minimum, maximum)

    if selected.empty:
        raise ValueError(
            f"No data for variable {variable.name} in the selected ranges."
        )

    if "sum" in value_fields:
        principal_field = "sum"
    elif "average" in value_fields:
        principal_field = "average"
    else:
        principal_field = "value"

    # Create a summary of daily data
    daily = create_daily_df(
        selected,
        selected_full,
        principal_field,
        "maximum" in value_fields,
        "minimum" in value_fields,
        tx_period,
        variable.null_limit,
    )

    # Ensure no nans are present
    daily = daily.merge(
        calculate_extra_data_daily(validated, measurement), on="date", how="left"
    )
    daily["extra_data_count"].fillna(0, inplace=True)
    daily["state"] = True
    daily["data_count"].fillna(0, inplace=True)
    daily["percentage"].fillna(0, inplace=True)
    daily[f"suspicious_{principal_field}s_count"].fillna(0, inplace=True)
    daily["value_difference_error_count"].fillna(0, inplace=True)
    if "maximum" in value_fields:
        daily["suspicious_maximums_count"].fillna(0, inplace=True)
    if "minimum" in value_fields:
        daily["suspicious_minimums_count"].fillna(0, inplace=True)

    # TODO the following line makes an override of "date_error"
    #           Discuss if the team are agree
    daily["date_error"] = daily["extra_data_count"]

    # Round to appropriate decimal places
    decimal_places = (
        apps.get_model(app_label="measurement", model_name=variable.variable_code)
        ._meta.get_field(principal_field)
        .decimal_places
    )
    daily[principal_field] = (
        daily[principal_field].astype(np.float64).round(decimal_places)
    )
    if "maximum" in value_fields:
        daily["maximum"] = daily["maximum"].astype(np.float64).round(decimal_places)
    if "minimum" in value_fields:
        daily["minimum"] = daily["minimum"].astype(np.float64).round(decimal_places)
    daily["percentage"] = daily["percentage"].astype(np.float64).round(1)

    # Final touches and extracting relevant parts from other dataframes
    daily.index.name = "id"
    daily.reset_index(inplace=True)
    return (
        daily,
        selected[["time"] + value_fields],
        measurement[["time"] + value_fields],
        validated[["time"] + value_fields],
    )


def detail_list(
    station: Station,
    variable: Variable,
    date_of_interest: datetime,
    minimum: Decimal,
    maximum: Decimal,
):
    """Return the detailed information of a day.

    It is requested when a user wants to see the detailed info of a specific day from
    the Validation interface.

    Args:
        station: Station of interest.
        variable: Variable of interest.
        date_of_interest: Date to find out detailed information about.
        minimum: Minimum value.
        maximum: Maximum value.

    Returns:
        A dictionary response for the detailed day table containing the report
        of values and statistics, indicators, time series for plot, etc.
    """
    start_time, end_time = set_time_limits(date_of_interest, date_of_interest)

    (
        measurement,
        validated,
        selected_full,
        selected,
        tx_period,
        value_fields,
    ) = preprocessing(station, variable, start_time, end_time, minimum, maximum)

    for value_column in ("value", "average", "sum"):
        if value_column in value_fields:
            break

    # TODO: What's state and what it is used for?
    if "maximum" in value_fields and "minimum" in value_fields:
        selected_full["state"] = ~(
            selected_full[value_column].isna()
            & selected_full["maximum"].isna()
            & selected_full["minimum"].isna()
        )
    else:
        selected_full["state"] = ~(selected_full[value_column].isna())

    # Basic statistics
    mean = selected[value_column].mean(skipna=True)
    std_dev = selected[value_column].astype(float).std(skipna=True)
    stddev_inf_limit = mean - (std_dev * float(variable.outlier_limit))
    stddev_sup_limit = mean + (std_dev * float(variable.outlier_limit))
    selected_full["stddev_error"] = ~selected_full[value_column].between(
        stddev_inf_limit, stddev_sup_limit
    )
    selected_full["comment"] = ""
    selected_full.fillna("", inplace=True)

    # Select the columns that will be output.
    # TODO: Maybe worth including some damage control if not all columns are present.
    columns = [
        "id",
        "id_joined",
        "time",
        "is_validated",
        "is_selected",
        "state",
        "time_lapse_status",
        "stddev_error",
        "comment",
        "value_difference",
        "value_difference_error",
    ]
    suspicious_columns = ["suspicious_" + col for col in value_fields]
    report = selected_full[columns + value_fields + suspicious_columns]

    for col in value_fields:
        report.rename(
            columns={
                "suspicious_" + col: col + "_error",
            },
            inplace=True,
        )

    # TODO: What's the purpose of duplicating this? Why not just renaming the column?
    selected_full["n_valor"] = selected_full["value_difference"]

    _selected = selected_full[selected_full["is_selected"]]

    # Only account for value errors when there's no error in timestamp lapse
    _selected_no_error = _selected[_selected["time_lapse_status"] == 1]

    # JSON cannot encode numpy.int64, so all need to be transformed to int.
    indicators = {
        # Number of dates with timestamp lapse errors
        "num_date": int((_selected["time_lapse_status"] != 1).sum()),
        "num_stddev": int(_selected["stddev_error"].sum()),
        "num_data": int(24 * (60 / tx_period)),
        f"num_{value_column}": int(
            _selected_no_error[f"suspicious_{value_column}"].sum()
        ),
    }
    if "maximum" in value_fields:
        indicators["num_maximum"] = int(_selected["suspicious_maximum"].sum())
    if "minimum" in value_fields:
        indicators["num_minimum"] = int(_selected["suspicious_minimum"].sum())

    return {
        "series": report.to_dict(orient="records"),
        "indicators": indicators,
        "value_columns": value_fields,
    }


def get_conditions(changes_list: List[Dict[str, Any]]) -> List[date]:
    """Processes instructions about which days are going to be NULL (remove).

    The instructions come from Validation user. It's called by "save_to_validated"
    function.

    Args:
        changes_list: Complete list of records to consider.

    Returns:
        A list of the dates that need deleting.
    """
    return [
        datetime.strptime(row["date"], "%Y-%m-%d").date()
        for row in changes_list
        if not row["state"]
    ]


def save_to_validated(
    variable: Variable,
    station: Station,
    to_delete: List[date],
    start_date: Union[datetime, str],
    end_date: Union[datetime, str],
    minimum: Decimal,
    maximum: Decimal,
):
    """Processes the request from the user for saving data to "validated" tables.

    All the records in the range are selected. Then, those labelled to delete are set
    their relevant magnitudes to None. The old records in that time range are deleted
    and the new, possibly updated records, in that range, are saved.

    After all is done, the creation of the reports is launched.

    Args:
        station: Station of interest.
        variable: Variable of interest.
        to_delete: List of dates to delete from the validation.
        start_date: Start date.
        end_date: End date.
        maximum: Maximum value expected for the variable.
        minimum: Minimum value expected for the variable.

    Returns:
        True if the data saving to validation succeeds.
    """
    validated = apps.get_model(app_label="validated", model_name=variable.variable_code)

    start_date, end_date = set_time_limits(start_date, end_date)
    _, _, _, selected, _, value_fields = preprocessing(
        station, variable, start_date, end_date, minimum, maximum
    )

    for d in to_delete:
        selected.loc[selected.date == d, value_fields] = None

    validated.timescale.filter(
        time__range=[start_date, end_date],
        station_id=station.station_id,
    ).delete()

    selected["station_id"] = station.station_id
    insert_result = validated.objects.bulk_create(
        [
            validated(**record.to_dict())
            for _, record in selected[["time", "station_id"] + value_fields].iterrows()
        ]
    )

    if len(insert_result) != len(selected):
        return False

    launch_report_calculations()
    return True


def save_detail_to_validated(
    data_list: List[Dict[str, Any]], variable: Variable, station: Station
) -> bool:
    """Processes the request from the user to save "Detail of selected day" data.

    in summary, all the data in the selected time range already in the validated
    table is deleted and the new data is inserted. If the entry was not selected, then
    its entry in the table only has "None" values.

    # TODO Why do we store empty values when not selected? Why not simply skip the
    # TODO record altogether?

    Args:
        data_list: List with the information of the records to update.
        variable: The variable to update.
        station: The station this records relate to.

    Returns:
        True if the selected data is inserted successfully in the database.
    """
    start_time = data_list[0]["time"]
    end_time = data_list[-1]["time"]

    validated = apps.get_model(app_label="validated", model_name=variable.variable_code)
    validated.timescale.filter(
        time__range=[start_time, end_time],
        station_id=station.station_id,
    ).delete()

    columns = [c.name for c in validated._meta.fields]
    allowed_fields = ("sum", "average", "minimum", "maximum", "value")
    value_columns = [c for c in columns if c in allowed_fields]
    model_instances = []
    for row in data_list:
        record = {
            "time": row["time"],
            "station_id": station.station_id,
            "used_for_hourly": False,
        }
        if not row["is_selected"]:
            for c in value_columns:
                record[c] = None
        else:
            for c in value_columns:
                record[c] = row[c]
        model_instances.append(validated(**record))

    insert_result = validated.objects.bulk_create(model_instances)
    return len(insert_result) == len(model_instances)


def data_report(
    temporality: str,
    station: Station,
    variable: Variable,
    start_time: str,
    end_time: str,
) -> pd.DataFrame:
    """Returns the data that will be downloaded or plotted.

    Args:
        temporality: The temporality of the data to plot (measurement, validated,
            hourly, daily, monthly)
        station: The station the data is related to.
        variable: The variable to get information for.
        start_time: The start date and time.
        end_time: The final date and time.

    Returns:
        Dataframe with the relevant data.
    """
    valid = ("measurement", "validated", "hourly", "daily", "monthly")
    if temporality not in valid:
        raise ValueError(
            f"Invalid temporality: {temporality}. Valid values are: {', '.join(valid)}"
        )

    start_time, end_time = set_time_limits(start_time, end_time)
    data = (
        apps.get_model(app_label=temporality, model_name=variable.variable_code)
        .objects.filter(
            station_id=station.station_id, time__gte=start_time, time__lte=end_time
        )
        .order_by("time")
    )

    data_columns = [e.name for e in data.model._meta.fields]
    allowed_fields = ("sum", "average", "minimum", "maximum", "value")
    fields = ["time"] + [e for e in data_columns if e in allowed_fields]

    df = pd.DataFrame.from_records(data.values(*fields))
    if df.empty:
        df = pd.DataFrame(columns=fields)
    return df


def dict_data_report(
    temporality: str,
    station: Station,
    variable: Variable,
    start_time: str,
    end_time: str,
) -> Dict[str, Any]:
    """Prepares info and data for plotting

    Args:
        temporality: The temporality of the data to plot (measurements, validated,
            hourly, daily, monthly)
        station: The station the data is related to.
        variable: The variable to get information for.
        start_time: The start date and time.
        end_time: The final date and time.

    Returns:
        Dictionary with all the relevant information required for plotting, to be used
        by the JS side of the front end.
    """
    logger.warning(temporality)
    response = {
        "station": {
            "id": station.station_id,
            "code": station.station_code,
        },
        "variable": {
            "id": variable.variable_id,
            "name": variable.name,
            "maximum": variable.maximum,
            "minimum": variable.minimum,
            "unit_initials": variable.unit.initials,
            "is_cumulative": variable.is_cumulative,
        },
        "series": data_report(temporality, station, variable, start_time, end_time)
        .fillna("")
        .to_dict("list"),
        "temporality": temporality,
    }
    return response


def csv_data_report(
    temporality: str,
    station: Station,
    variable: Variable,
    start_time: str,
    end_time: str,
) -> str:
    """Prepares info and data for exporting as CSV.

    Args:
        temporality: The temporality of the data to plot (measurements, validated,
            hourly, daily, monthly)
        station: The station the data is related to.
        variable: The variable to get information for.
        start_time: The start date and time.
        end_time: The final date and time.

    Returns:
        Data in CSV format as a string.
    """
    return data_report(temporality, station, variable, start_time, end_time).to_csv(
        index=False
    )


def calculate_reports(variable):
    """
    Launch hourly, daily, monthly calculations for a given variable
    It's called by the main thread.
    """
    global threads_report_calculation
    threads_report_calculation.append(variable.variable_id)
    calculate_hourly(variable)
    calculate_daily(variable)
    calculate_monthly(variable)
    threads_report_calculation.remove(variable.variable_id)


def thread_launch_report_calculations():
    """
    Thread that launch report calculations for every variable
    """
    global threads_report_calculation
    variables = Variable.objects.all()
    for variable in variables:
        if not variable.automatic_report:
            continue
        attempt = 0
        while variable.variable_id in threads_report_calculation:
            time.sleep(10)
            attempt = attempt + 1
            if attempt > 5:
                break
        calculate_reports(variable)


def launch_report_calculations():
    """
    Triggers Report calculations (hourly, daily, monthly) using thread in backgroud
    """
    global threads_report_calculation
    if len(threads_report_calculation) > 0:
        return
    t = Thread(target=thread_launch_report_calculations, args=())
    t.start()


def calculate_hourly(variable):
    """
    Calculate hourly data from validated data for a specific variable
    It iterates for every validated record that has "used_for_hourly = False"
    """
    Validated = apps.get_model(app_label="validated", model_name=variable.variable_code)
    Hourly = apps.get_model(app_label="hourly", model_name=variable.variable_code)
    register_exists = True
    while register_exists:
        register = Validated.objects.filter(used_for_hourly=False).first()
        if not register:
            register_exists = False
            return False

        start_of_hour = datetime.combine(
            register.time, time(register.time.hour, 0, 0, 0)
        )
        end_of_hour = datetime.combine(
            register.time, time(start_of_hour.hour, 59, 59, 999999)
        )
        validated_block = Validated.objects.filter(
            station_id=register.station_id,
            time__gte=start_of_hour,
            time__lte=end_of_hour,
        )
        data_columns = [e.name for e in validated_block.model._meta.fields]
        allowed_fields = ("sum", "value", "average")
        value_fields = [e for e in data_columns if e in allowed_fields]
        base_fields = [
            "time",
        ]
        fields = base_fields + value_fields
        block = pd.DataFrame.from_records(validated_block.values(*fields))
        if block.empty:
            continue

        if "sum" in fields:
            result = block["sum"].sum()
            count = block["sum"].count()
        elif "average" in fields:
            result = block["average"].mean(skipna=True)
            count = block["average"].count()
        else:
            result = block["value"].mean(skipna=True)
            count = block["value"].count()

        try:
            delta_t = DeltaT.objects.get(station__station_id=register.station_id)
        except:
            return False

        completeness = (count / (60 / delta_t.delta_t)) * 100.0
        if completeness < (100.0 - float(variable.null_limit)):
            result = None

        Hourly.objects.filter(
            time=start_of_hour, station_id=register.station_id
        ).delete()

        record = {
            "time": start_of_hour,
            "station_id": register.station_id,
            "used_for_daily": False,
            "completeness": completeness,
        }
        if "sum" in fields:
            record["sum"] = result
        elif "average" in fields:
            record["average"] = result
        else:
            record["value"] = result
        hourly = Hourly(**record)
        hourly.save()
        validated_block.update(used_for_hourly=True)
    return True


def calculate_daily(variable):
    """
    Calculate daily data from hourly data for an especific variable
    It iterates for every hourly record that has "used_for_daily = False"
    """
    Hourly = apps.get_model(app_label="hourly", model_name=variable.variable_code)
    Daily = apps.get_model(app_label="daily", model_name=variable.variable_code)
    register_exists = True
    while register_exists:
        register = Hourly.objects.filter(used_for_daily=False).first()
        if not register:
            register_exists = False
            return

        start_of_day = datetime.combine(register.time, time(0, 0, 0, 0))
        end_of_day = datetime.combine(register.time, time(23, 59, 59, 999999))
        hourly_block = Hourly.objects.filter(
            station_id=register.station_id, time__gte=start_of_day, time__lte=end_of_day
        )
        data_columns = [e.name for e in hourly_block.model._meta.fields]
        allowed_fields = ("sum", "average", "value")
        value_fields = [e for e in data_columns if e in allowed_fields]
        base_fields = [
            "time",
        ]
        fields = base_fields + value_fields
        block = pd.DataFrame.from_records(hourly_block.values(*fields))
        if block.empty:
            continue

        if "sum" in fields:
            result = block["sum"].sum()
            count = block["sum"].count()
        elif "average" in fields:
            result = block["average"].mean(skipna=True)
            count = block["average"].count()
        else:
            result = block["value"].mean(skipna=True)
            count = block["value"].count()

        completeness = (count / 24) * 100.0
        if completeness < (100.0 - float(variable.null_limit)):
            result = None
        Daily.objects.filter(time=start_of_day, station_id=register.station_id).delete()
        record = {
            "time": start_of_day,
            "station_id": register.station_id,
            "used_for_monthly": False,
            "completeness": completeness,
        }
        if "sum" in fields:
            record["sum"] = result
        elif "average" in fields:
            record["average"] = result
        else:
            record["value"] = result
        daily = Daily(**record)
        daily.save()
        hourly_block.update(used_for_daily=True)


def calculate_monthly(variable):
    """
    Calculate monthly data from daily data for an especific variable
    It iterates for every daily row that has "used_for_monthly = False"
    """
    Daily = apps.get_model(app_label="daily", model_name=variable.variable_code)
    Monthly = apps.get_model(app_label="monthly", model_name=variable.variable_code)
    register_exists = True
    while register_exists:
        register = Daily.objects.filter(used_for_monthly=False).first()
        if not register:
            register_exists = False
            return

        start_of_month = datetime(register.time.year, register.time.month, 1, 0, 0)
        last_day = calendar.monthrange(register.time.year, register.time.month)[1]
        end_of_month = datetime(
            register.time.year, register.time.month, last_day, 23, 59
        )
        daily_block = Daily.objects.filter(
            station_id=register.station_id,
            time__gte=start_of_month,
            time__lte=end_of_month,
        )
        data_columns = [e.name for e in daily_block.model._meta.fields]
        allowed_fields = ("sum", "minimum", "maximum", "average", "value")
        value_fields = [e for e in data_columns if e in allowed_fields]
        base_fields = [
            "time",
        ]
        fields = base_fields + value_fields
        block = pd.DataFrame.from_records(daily_block.values(*fields))
        if block.empty:
            continue
        if "sum" in fields:
            result = block["sum"].sum()
            count = block["sum"].count()
        elif "average" in fields:
            result = block["average"].mean(skipna=True)
            count = block["average"].count()
        else:
            result = block["value"].mean(skipna=True)
            count = block["value"].count()
        completeness = (count / last_day) * 100.0
        if completeness < (100.0 - float(variable.null_limit)):
            result = None
        Monthly.objects.filter(
            time=start_of_month, station_id=register.station_id
        ).delete()
        record = {
            "time": start_of_month,
            "station_id": register.station_id,
            "completeness": completeness,
        }
        if "sum" in fields:
            record["sum"] = result
        elif "average" in fields:
            record["average"] = result
        else:
            record["value"] = result
        monthly = Monthly(**record)
        monthly.save()
        daily_block.update(used_for_monthly=True)
