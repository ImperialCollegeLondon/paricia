import calendar
from datetime import date, datetime, time
from threading import Thread
from typing import Tuple, Union, overload, Sequence
from decimal import Decimal

import numpy as np
import pandas as pd
from django.apps import apps
from django.db.models import BooleanField, Value

from station.models import DeltaT, Station
from variable.models import Variable

threads_report_calculation = []

ALLOWED_FIELDS = ("sum", "minimum", "maximum", "average", "value")


@overload
def set_time_limits(start_time: str, end_time: str) -> Tuple[str, str]:
    ...


def set_time_limits(
    start_time: datetime, end_time: datetime
) -> Tuple[datetime, datetime]:
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


def daily_validation(station, variable, start_time, end_time, minimum, maximum):
    """
    Returns a daily report and time series for Validation interface.
    It builds the dictionary response for main Validation interface:
    It contains:
        daily report, indicators, time series for plot, variable and station information
    """
    num_value = None
    num_maximum = None
    num_minimum = None
    num_days = None

    report, selected, measurement, validated = daily_report(
        station, variable, start_time, end_time, minimum, maximum
    )
    value_columns = list(measurement.columns.to_numpy())
    value_columns.remove("time")

    num_date = len(
        report[report["date_error"].ne(1) & ~report["date_error"].isna()].index
    )
    num_percentage = len(report[report["percentage_error"].eq(True)])

    if "sum" in value_columns:
        num_value = len(
            report[
                report["percentage_error"].eq(False)
                & ~report["suspicious_sums_count"].isna()
            ]
        )
    if "average" in value_columns:
        num_value = len(
            report[
                report["percentage_error"].eq(False)
                & ~report["suspicious_averages_count"].isna()
            ]
        )
    if "value" in value_columns:
        num_value = len(
            report[
                report["percentage_error"].eq(False)
                & ~report["suspicious_values_count"].isna()
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
    providing as output the original dataframe with  the selected entries labelled and
    also the selected entries themselves as a separate dataframe.

    Args:
        joined: The data frame with all the data.

    Returns:
        The joined dataframe with the selected entries labelled and the dataframe only
        with the selected entries.
    """
    selected = joined.drop_duplicates("time_truncated", keep="first")
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
            if old in col:
                df.rename(columns={col: col.replace(old, new)}, inplace=True)


def verify_validated(
    validated: pd.DataFrame, measurement: pd.DataFrame
) -> pd.Series:
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
    ]

    selected_full.reset_index(inplace=True, drop=True)
    selected_full.insert(0, "id", selected_full.index)
    selected.reset_index(inplace=True, drop=True)
    selected.insert(0, "id", selected.index)

    return measurement, validated, selected_full, selected, tx_period, value_fields


def daily_report(station, variable, start_time, end_time, minimum, maximum):
    """
    Calculate daily report that will be send to main Validation interface
    It's built from basic_calculations function
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

    daily_group_all = selected_full.groupby("date")
    daily_group = selected.groupby("date")

    if "sum" in value_fields:
        principal_field = "sum"
    elif "average" in value_fields:
        principal_field = "average"
    else:
        principal_field = "value"

    # daily = daily_group[principal_field].count()
    daily = daily_group_all[principal_field].count()
    daily = daily.reset_index(name="data_count")

    if "sum" in value_fields:
        daily["sum"] = daily_group["sum"].sum(min_count=1).to_numpy()
    if "average" in value_fields or "value" in value_fields:
        daily["average"] = daily_group["average"].mean().to_numpy()
    if "maximum" in value_fields:
        daily["maximum"] = daily_group["maximum"].max().to_numpy()
    if "minimum" in value_fields:
        daily["minimum"] = daily_group["minimum"].min().to_numpy()
    daily["all_validated"] = daily_group["is_validated"].all().to_numpy()

    # TODO Create a "period" table for storing the period for every station
    # TODO Maybe program for dynamic periods. This happens when a station change the period
    expected_data_count = 24 * 60 / tx_period
    daily["percentage"] = (daily["data_count"] / expected_data_count) * 100.0
    # TODO "is_null" could be removed and use "percentage_error" instead
    daily["is_null"] = daily["percentage"] < (100.0 - float(variable.null_limit))
    daily["percentage_error"] = ~daily["percentage"].between(
        100.0 - float(variable.null_limit), 100.0
    )

    # TODO: change variable_maximun and variable_minimum to apply for PARICIA context
    if "sum" in value_fields:
        daily["suspicious_sums_count"] = daily_group["suspicious_sum"].sum().to_numpy()
    if "average" in value_fields or "value" in value_fields:
        daily["suspicious_averages_count"] = (
            daily_group["suspicious_average"].sum().to_numpy()
        )
    if "maximum" in value_fields:
        daily["suspicious_maximums_count"] = (
            daily_group["suspicious_maximum"].sum().to_numpy()
        )
    if "minimum" in value_fields:
        daily["suspicious_minimums_count"] = (
            daily_group["suspicious_minimum"].sum().to_numpy()
        )

    # Calculating consecutive differences and check for errors.
    # 'time_lapse_status' set to:
    #                               0 if 'time_lapse' < 'period'
    #                               1 if 'time_lapse' == 'period'
    #                               2 if 'time_lapse' > 'period'
    #

    daily["value_difference_error_count"] = (
        daily_group_all["value_difference_error"].sum(numeric_only=False).to_numpy()
    )

    # # Generate a sequence of days following in the calendar to compare with data in database and note voids
    # # TODO Analizar que esto pudiera ser incluído en la primera generación de daily
    # calendar_day_seq = pd.DataFrame(
    #     pd.date_range(start=start_time, end=end_time).date,
    #     columns=['date']
    # )
    # daily = calendar_day_seq.merge(daily, on='date', how='left')

    if daily.empty:
        daily = df = pd.DataFrame(
            columns=[
                "id",
                "date",
                "data_count",
                "average",
                "maximum",
                "minimum",
                "all_validated",
                "percentage",
                "is_null",
                "suspicious_averages_count",
                "suspicious_maximums_count",
                "suspicious_minimums_count",
                "value_difference_error_count",
                "day_interval",
                "date_error",
                "extra_data_count",
                "historic_diary_avg",
                "state",
                "average_error",
                "maximum_error",
                "minimum_error",
            ]
        )
        return daily, selected[["time", "value"]]

    daily["day_interval"] = (daily["date"] - daily["date"].shift(1)).dt.days
    daily["day_interval"][0] = 1
    daily["date_error"] = np.where(daily["day_interval"].gt(1), 3, 1)
    # TODO hacer un groupby de repeated_values_count por día, para pasar el valor total de repetidos por día
    #      posiblemente convenga hacer un solo cálculo arriba

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
    extra_data_daily = extra_data_daily_group["extra_values_count"].sum()
    extra_data_daily = extra_data_daily.reset_index(name="extra_data_count")
    daily = daily.merge(extra_data_daily, on="date", how="left")
    daily["extra_data_count"].fillna(0, inplace=True)

    # TODO the following line makes an override of "date_error"
    #           Discuss if the team are agree
    daily["date_error"] = daily["extra_data_count"]
    month_day_tuples = tuple(
        list(
            zip(
                pd.DatetimeIndex(daily["date"]).month,
                pd.DatetimeIndex(daily["date"]).day,
            )
        )
    )
    Daily = apps.get_model(app_label="daily", model_name=variable.variable_code)
    historic_diary = Daily.objects.filter(station_id=station.station_id).extra(
        where=["(date_part('month', time), date_part('day', time)) in %s"],
        params=[month_day_tuples],
    )
    historic_diary = pd.DataFrame(list(historic_diary.values()))

    if not historic_diary.empty:
        historic_diary["month-day"] = (
            pd.DatetimeIndex(historic_diary["time"]).month.astype(str)
            + "-"
            + pd.DatetimeIndex(historic_diary["time"]).day.astype(str)
        )
        historic_diary_group = historic_diary.groupby(["month-day"])
        if "sum" in value_fields:
            historic_field = "sum"
        elif "average" in value_fields:
            historic_field = "average"
        else:
            historic_field = "value"
        try:
            daily["historic_diary_avg"] = (
                historic_diary_group[historic_field].mean().to_numpy()
            )
        except:
            daily["historic_diary_avg"] = np.nan
    else:
        daily["historic_diary_avg"] = np.nan

    daily["state"] = True
    daily["data_count"].fillna(0, inplace=True)
    daily["percentage"].fillna(0, inplace=True)
    if "sum" in value_fields:
        daily["suspicious_sums_count"].fillna(0, inplace=True)
    if "average" in value_fields:
        daily["suspicious_averages_count"].fillna(0, inplace=True)
    if "maximum" in value_fields:
        daily["suspicious_maximums_count"].fillna(0, inplace=True)
    if "minimum" in value_fields:
        daily["suspicious_minimums_count"].fillna(0, inplace=True)
    daily["value_difference_error_count"].fillna(0, inplace=True)
    daily["historic_diary_avg"].fillna("", inplace=True)

    ##
    # TODO check, maybe it's not needed anymore
    if "sum" in value_fields:
        daily["sum_error"] = np.where(
            daily["suspicious_sums_count"].gt(0),
            True,
            False,
        )
    if "average" in value_fields:
        daily["average_error"] = np.where(
            daily["suspicious_averages_count"].gt(0),
            True,
            False,
        )
    if "maximum" in value_fields:
        daily["maximum_error"] = np.where(
            daily["suspicious_maximums_count"].gt(0),
            True,
            False,
        )
    if "minimum" in value_fields:
        daily["minimum_error"] = np.where(
            daily["suspicious_minimums_count"].gt(0),
            True,
            False,
        )
    #
    ##

    Measurement = apps.get_model(
        app_label="measurement", model_name=variable.variable_code
    )

    if "sum" in value_fields:
        decimal_places = Measurement._meta.get_field("sum").decimal_places
    elif "average" in value_fields:
        decimal_places = Measurement._meta.get_field("average").decimal_places
    elif "value" in value_fields:
        decimal_places = Measurement._meta.get_field("value").decimal_places
    else:
        decimal_places = 2

    if "sum" in value_fields:
        daily["sum"] = daily["sum"].astype(np.float64).round(decimal_places)
    if "average" in value_fields:
        daily["average"] = daily["average"].astype(np.float64).round(decimal_places)
    if "maximum" in value_fields:
        daily["maximum"] = daily["maximum"].astype(np.float64).round(decimal_places)
    if "minimum" in value_fields:
        daily["minimum"] = daily["minimum"].astype(np.float64).round(decimal_places)
    daily["percentage"] = daily["percentage"].astype(np.float64).round(1)

    daily.index.name = "id"
    daily.reset_index(inplace=True)
    ## TODO Eliminar o corregir ids -> id
    #
    # daily.rename(columns={'id':'ids',}, inplace=True)
    daily["ids"] = daily["id"]
    #
    ##
    for _f in value_fields:
        daily[_f].fillna("", inplace=True)
    _selected = selected[["time"] + value_fields]
    _measurement = measurement[["time"] + value_fields]
    _validated = validated[["time"] + value_fields]
    return daily, _selected, _measurement, _validated


def detail_list(station_id, variable_id, date, minimum, maximum):
    """
    Return the datailed information of a day.
    It is requested when a user wants to see the detailed info of an especific day from the Validation interface
    """
    start_time = datetime.strptime(date, "%Y-%m-%d")
    end_time = datetime.combine(start_time.date(), time(23, 59, 59, 999999))
    station = Station.objects.get(station_id=station_id)
    variable = Variable.objects.get(variable_id=variable_id)

    (
        measurement,
        validated,
        selected_full,
        selected,
        tx_period,
        value_fields,
    ) = preprocessing(station, variable, start_time, end_time, minimum, maximum)

    if "average" in value_fields:
        value_column = "average"
    elif "sum" in value_fields:
        value_column = "sum"
    elif "value" in value_fields:
        value_column = "value"

    if (
        "average" in value_fields
        and "maximum" in value_fields
        and "minimum" in value_fields
    ):
        selected_full["state"] = ~(
            selected_full["average"].isna()
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
    #######
    selected_full["n_valor"] = selected_full["value_difference"]
    _selected = selected_full[selected_full["is_selected"] == True]
    num_date = len(_selected[_selected["time_lapse_status"] != 1].index)

    # Only take into account 'value_error' when there's no error in timestamp lapse
    _selected_NO_TIMELAPSE_ERROR = _selected[_selected["time_lapse_status"] == 1]

    indicators = {}
    if "sum" in value_fields:
        num_sum = len(
            _selected_NO_TIMELAPSE_ERROR[
                _selected_NO_TIMELAPSE_ERROR["suspicious_sum"] == True
            ].index
        )
        indicators["num_sum"] = num_sum
    if "average" in value_fields:
        num_average = len(
            _selected_NO_TIMELAPSE_ERROR[
                _selected_NO_TIMELAPSE_ERROR["suspicious_average"] == True
            ].index
        )
        indicators["num_average"] = num_average
    if "value" in value_fields:
        num_value = len(
            _selected_NO_TIMELAPSE_ERROR[
                _selected_NO_TIMELAPSE_ERROR["suspicious_value"] == True
            ].index
        )
        indicators["num_value"] = num_value
    if "maximum" in value_fields:
        num_maximum = len(_selected[_selected["suspicious_maximum"] == True].index)
        indicators["num_maximum"] = num_maximum
    if "minimum" in value_fields:
        num_minimum = len(_selected[_selected["suspicious_minimum"] == True].index)
        indicators["num_minimum"] = num_minimum

    num_stddev = len(_selected[_selected["stddev_error"] == True].index)

    # TODO check if this is expected number of data
    num_data = int(24 * (60 / tx_period))

    indicators = {
        **{
            "num_date": num_date,
            "num_stddev": num_stddev,
            "num_data": num_data,
        },
        **indicators,
    }

    data = {
        "series": report.to_dict(orient="records"),
        "indicators": indicators,
        "value_columns": value_fields,
    }

    return data


def get_conditions(changes_list):
    """
    Processes instructions about which days are going to be NULL (remove). The instructions comes from Validation user interface
    It's called by "save_to_validated" function
    """
    dates_condition = []
    dates_delete = []
    for row in changes_list:
        # TODO check "validado" has equivalence
        # if fila["validado"]:
        #     fechas_condicion.append("'" + fila["fecha"] + "'")
        if not row["state"]:
            dates_delete.append("'" + row["date"] + "'")

    dates_condition = set(dates_condition)
    dates_delete = set(dates_delete)

    where_dates = ",".join(dates_condition)
    where_delete = ",".join(dates_delete)

    conditions = {"where_delete": where_delete, "where_dates": where_dates}
    return conditions


def save_to_validated(changes_list, variable, station, conditions, minimum, maximum):
    """
    Processes the request from the user for saving data to "validated" tables.
    """
    Measurement = apps.get_model(
        app_label="measurement", model_name=variable.variable_code
    )
    Validated = apps.get_model(app_label="validated", model_name=variable.variable_code)

    # where_fechas = condiciones.get('where_fechas')
    start_date = changes_list[0]["date"]
    end_date = changes_list[-1]["date"]
    start_date, end_date = set_time_limits(start_date, end_date)

    # TODO se puede eliminar
    reporte_recibido = pd.DataFrame.from_records(changes_list)

    (
        measurement,
        validated,
        selected_full,
        selected,
        tx_period,
        value_fields,
    ) = preprocessing(station, variable, start_date, end_date, minimum, maximum)
    if len(conditions["where_delete"]) > 0:
        where_delete = conditions["where_delete"].replace("'", "").split(",")
        for _date in where_delete:
            _date = datetime.strptime(_date, "%Y-%m-%d").date()
            condition = selected["date"] == _date
            for c in value_fields:
                selected[c] = np.where(condition, None, selected[c])
    Validated.timescale.filter(
        time__range=[start_date, end_date],
        station_id=station.station_id,
    ).delete()

    model_instances = []
    for _, record in selected.iterrows():
        row = {"time": record["time"], "station_id": station.station_id}
        for c in value_fields:
            row[c] = record[c]
        model_instances.append(Validated(**row))

    insert_result = Validated.objects.bulk_create(model_instances)
    if len(insert_result) != len(selected):
        return False
    launch_report_calculations()
    return True


def save_detail_to_validated(data_list, variable, station):
    """
    Processes the request from the user to save "Detail of selected day" data.
    """
    start_time = data_list[0]["time"]
    end_time = data_list[-1]["time"]

    Validated = apps.get_model(app_label="validated", model_name=variable.variable_code)
    Validated.timescale.filter(
        time__range=[start_time, end_time],
        station_id=station.station_id,
    ).delete()

    columns = [c.name for c in Validated._meta.fields]
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
        model_instances.append(Validated(**record))

    # TODO Could send 'bulk_create' activity to a thread
    insert_result = Validated.objects.bulk_create(model_instances)
    result = False
    if len(insert_result) == len(model_instances):
        result = True
    return result


def data_report(temporality, station, variable, start_time, end_time):
    """
    Returns the data for plotting or downloading CSV
    Menu: Data -> Data report
    """
    start_time, end_time = set_time_limits(start_time, end_time)
    if temporality not in ["measurement", "validated", "hourly", "daily", "monthly"]:
        return None
    Data = apps.get_model(app_label=temporality, model_name=variable.variable_code)
    data = Data.objects.filter(
        station_id=station.station_id, time__gte=start_time, time__lte=end_time
    ).order_by("time")

    data_columns = [e.name for e in data.model._meta.fields]
    allowed_fields = ("sum", "average", "minimum", "maximum", "value")
    value_fields = [e for e in data_columns if e in allowed_fields]
    base_fields = [
        "time",
    ]
    fields = base_fields + value_fields
    df = pd.DataFrame.from_records(data.values(*fields))
    if df.empty:
        df = pd.DataFrame(columns=fields)
    return df


def dict_data_report(temporality, station, variable, start_time, end_time):
    """
    Prepares info and data for plotting
    Menu: Data -> Data report
    """
    df = data_report(temporality, station, variable, start_time, end_time)
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
        "series": df.fillna("").to_dict("list"),
        "temporality": temporality,
    }
    return response


def csv_data_report(temporality, station, variable, start_time, end_time):
    """
    Format data for dowloading
    Menu: Data -> Data report
    """
    df = data_report(temporality, station, variable, start_time, end_time)
    csv_response = df.to_csv(index=False)
    return csv_response


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
