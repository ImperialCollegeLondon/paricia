########################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos
# (iMHEA)basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#           Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS),
#           Ecuador.
#           Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones
#  creadoras, ya sea en uso total o parcial del código.
########################################################################################

import os
import shutil
import time
import zoneinfo
from datetime import datetime
from logging import getLogger
from numbers import Number
from typing import Any, Optional

import numpy as np
import pandas as pd
from django.apps import apps
from django.db import transaction

from djangomain.settings import BASE_DIR
from formatting.models import Association, Classification, Format
from importing.models import DataImportFull, DataImportTemp
from measurement.models import Measurement, StripLevelReading, WaterLevel
from variable.models import Variable

unix_epoch = np.datetime64(0, "s")
one_second = np.timedelta64(1, "s")


def validate_dates(data_import):
    """
    Verify if there already exists data for the dates of the data being imported.
    Args:
        data_import: DataImportFull or DataImportTemp object.
    Returns:
        tuple of:
            result: (list of dicts): one per classification for this file format of
            summary:
                dict containing information on the variable, the end date and whether
                the data exists.
            overwrite: (bool) True if any of the data already exists.
    """
    start_date = data_import.start_date
    end_date = data_import.end_date
    file_format = data_import.format_id
    station = data_import.station
    classifications = list(Classification.objects.filter(format=file_format))

    overwrite = False
    result = []
    for classification in classifications:
        # variable_code is used to select the measurmenet class
        var_code = str(classification.variable.variable_code)
        last_upload_date = get_last_uploaded_date(station.station_id, var_code)

        # Check if data exists between dates
        model = apps.get_model("measurement", var_code)
        query = model.timescale.filter(
            time__range=[start_date, end_date], station_id=station.station_id
        )
        exists = True if query else False
        overwrite = overwrite or exists
        summary = {
            "variable_id": classification.variable.variable_id,
            "variable_code": classification.variable.variable_code,
            "variable_name": classification.variable.name,
            "last_upload_date": last_upload_date,
            "exists": exists,
        }
        result.append(summary)
    return result, overwrite


def get_last_uploaded_date(station_id: int, var_code: str) -> Optional[datetime]:
    """Get the last date that data uploaded for a given station ID and variable code.

    Args:
        station_id: The station ID.
        var_code: The variable code.

    Returns:
        The last date that data was uploaded for the given station ID and variable code
        or None if no data was found.
    """
    query = (
        Measurement.timescale.filter(
            station__station_id=station_id, variable__variable_code=var_code
        )
        .order_by("time")
        .last()
    )
    if query:
        return query.time

    return None


def read_file_excel(file_path: str, file_format: Format) -> pd.DataFrame:
    """Reads an Excel file into a pandas DataFrame.

    Args:
        file_path: The path to the file to be read.
        file_format: The file format.

    Returns:
        A pandas DataFrame containing the data from the file.
    """
    firstline = file_format.first_row if file_format.first_row else 0
    skipfooter = file_format.footer_rows if file_format.footer_rows else 0
    return pd.read_excel(
        file_path,
        header=None,
        skiprows=firstline - 1,
        skipfooter=skipfooter,
        engine=None,
        error_bad_lines=False,
        index_col=None,
    )


def read_file_csv(source_file: Any, file_format: Format) -> pd.DataFrame:
    """Reads a CSV file into a pandas DataFrame.

    Args:
        source_file: Stream of data to be parsed.
        file_format: The file format.

    Returns:
        A pandas DataFrame containing the data from the file.
    """
    firstline = file_format.first_row if file_format.first_row else 0
    skipfooter = file_format.footer_rows if file_format.footer_rows else 0
    delimiter = file_format.delimiter.character

    skiprows: int | list[int] = firstline - 1
    if not isinstance(source_file, str):
        # The file was uploaded as binary
        lines = len(source_file.readlines())
        source_file.seek(0)
        skiprows = [i for i in range(0, firstline - 1)] + [
            i - 1 for i in range(lines, lines - firstline, -1)
        ]
        skipfooter = 0

    # Deal with the delimiter
    if "\\x" in delimiter:
        delim_hexcode = delimiter.replace("\\x", "")
        delim_intcode = eval("0x" + delim_hexcode)
        delimiter = chr(delim_intcode)
    elif delimiter == " ":
        delimiter = "\s+"  # This is a regex for whitespace

    return pd.read_csv(
        source_file,
        sep=delimiter,
        header=None,
        index_col=False,
        skiprows=skiprows,
        skipfooter=skipfooter,
        encoding="ISO-8859-1",
    )


def process_datetime_columns(
    data: pd.DataFrame, file_format: Format, timezone: str
) -> pd.DataFrame:
    """Process the datetime columns in a DataFrame.

    Args:
        data: The DataFrame to process.
        file_format: The file format.
        timezone: The timezone to use.

    Returns:
        The DataFrame with the datetime columns processed.
    """
    tz = zoneinfo.ZoneInfo(timezone)
    dt_format = file_format.datetime_format
    if file_format.date_column == file_format.time_column:
        data["date"] = pd.Series(
            [
                standardise_datetime(row, dt_format).replace(tzinfo=tz)
                for row in data[file_format.date_column - 1].values
            ],
            index=data.index,
        )
    else:
        cols = file_format.datetime_columns(file_format.delimiter.character)
        data["datetime_str"] = data[cols].agg(
            lambda row: " ".join([r.astype(str) for r in row]), axis=1
        )
        data["date"] = data["datime_str"].apply(
            lambda row: standardise_datetime(row, dt_format).replace(tzinfo=tz)
        )
        data.drop(columns=["datetime_str"], inplace=True)

    return data.sort_values("date").reset_index(drop=True)


def read_data_to_import(source_file: Any, file_format: Format, timezone: str):
    """Reads the data from file into a pandas DataFrame.

    Works out what sort of file is being read and adds standardised columns for
    datetime.

    Args:
        source_file: Stream of data to be parsed.
        file_format: Format of the data to be parsed.
        timezone: Timezone name, eg. 'America/Chicago'.

    Returns:
        Pandas.DataFrame with raw data read and extra column(s) for datetime
        correctly parsed.
    """
    if file_format.extension.value in ["xlsx", "xlx"]:
        data = read_file_excel(source_file, file_format)
    else:
        data = read_file_csv(source_file, file_format)

    return process_datetime_columns(data, file_format, timezone)


def standardise_datetime(date_time, datetime_format) -> datetime:
    """
    Returns a datetime object in the case that date_time is not already in that form.
    Args:
        date_time: The date_time to be transformed.
        datetime_format: The format that date_time is in (to be passed to
            datetime.strptime()).
    """

    if isinstance(date_time, datetime):
        return date_time
    elif isinstance(date_time, np.datetime64):
        date_time = datetime.utcfromtimestamp(
            float((date_time - unix_epoch) / one_second)
        )
        return date_time
    elif isinstance(date_time, str):
        pass

    elif isinstance(date_time, list):
        date_time = " ".join(date_time)

    elif isinstance(date_time, pd.Series):
        date_time = " ".join([str(val) for val in list(date_time[:])])

    else:
        date_time = ""

    # Now try converting the resulting string into a datetime obj
    try:
        _date_time = datetime.strptime(date_time, datetime_format)
    except:
        # TODO: Fix bare except statement
        _date_time = None
    return _date_time


def save_temp_data_to_permanent(data_import_temp):
    """
    Function to pass the temporary import to the final table. Uses the data_import_temp
    object only to get all required information from its fields.
    This function carries out the following steps:
    1.  Bulk delete of existing data between two times on a given measurement table for
    the station in question.
    2.  Bulk create to add the new data from the uploaded file.
    Steps 1. and 2. are carried out for each columns (variable) in the uploaded file.
    Args: data_import_id (int): DataImportTemp ID
    Returns: None
    """
    file_format = data_import_temp.format
    station = data_import_temp.station
    file_path = str(BASE_DIR) + "/data/media/" + str(data_import_temp.file)

    all_data = construct_matrix(file_path, file_format, station)
    for var_code, table in all_data.items():
        table = table.where((pd.notnull(table)), None)
        records = table.to_dict("records")
        Model = apps.get_model("measurement", var_code)

        # Delete existing data between the date ranges
        Model.timescale.filter(
            time__range=[data_import_temp.start_date, data_import_temp.end_date],
            station_id=station.station_id,
        ).delete()

        # The following is a hack to account for the different possible name of the
        # fields that the models might have. Will be made "nicer" at some point.
        # This should always work as a measurement model should always have one and only
        # one of "value", "average", "sum" fields.
        value_field = (
            set([field.name for field in Model._meta.fields])
            .intersection(["value", "average", "sum"])
            .pop()
        )

        # Bulk add new data
        # TODO improve this logic to cope with variables that might have max/min
        # AND depth.
        if "maximum" in table.columns:
            model_instances = [
                Model(
                    {
                        "time": record["date"],
                        value_field: record["value"],
                        "station_id": record["station_id"],
                        "maximum": record["maximum"],
                        "minimum": record["minimum"],
                    },
                )
                for record in records
            ]
        elif "depth" in [f.name for f in Model._meta.fields]:
            model_instances = [
                Model(
                    {
                        "time": record["date"],
                        value_field: record["value"],
                        "depth": record["depth"],
                        "station_id": record["station_id"],
                    },
                )
                for record in records
            ]
        else:
            model_instances = [
                Model(
                    {
                        "time": record["date"],
                        value_field: record["value"],
                        "station_id": record["station_id"],
                    },
                )
                for record in records
            ]
        Model.objects.bulk_create(model_instances)


def construct_matrix(matrix_source, file_format, station):
    """
    Construct the "matrix" or results table. Does various cleaning / simple
    transformations depending on the date format, type of data (accumulated,
    incremental...) and deals with NANs.
    Args:
        matrix_source: raw data file path
        file_format: a formatting.Format object.
    Returns: Dict of dataframes for results (one for each variable type in the raw data
        file).
    TODO: Probably refactor into smaller chunks.
    """

    # Get the "preformatted matrix" sorted by date col
    matrix = read_data_to_import(matrix_source, file_format, station.timezone)
    # Find start and end dates from top and bottom row
    start_date = matrix.loc[0, "date"]
    end_date = matrix.loc[matrix.shape[0] - 1, "date"]

    classifications = list(Classification.objects.filter(format=file_format))
    variables_data = {}
    for classification in classifications:
        columns = []
        columns.append(("date", "date"))

        # Validation of values
        columns.append((classification.value - 1, "value"))
        if classification.value_validator_column:
            matrix.loc[
                matrix[classification.value_validator_column - 1]
                != classification.value_validator_text,
                classification.value - 1,
            ] = np.nan

        # Validation of maximum
        if classification.maximum:
            columns.append((classification.maximum - 1, "maximum"))
        if classification.maximum_validator_column:
            matrix.loc[
                matrix[classification.maximum_validator_column - 1]
                != classification.maximum_validator_text,
                classification.maximum - 1,
            ] = np.nan

        # Validation of minimum
        if classification.minimum:
            columns.append((classification.minimum - 1, "minimum"))
        if classification.minimum_validator_column:
            matrix.loc[
                matrix[classification.minimum_validator_column - 1]
                != classification.minimum_validator_text,
                classification.minimum - 1,
            ] = np.nan

        data = matrix.loc[:, [v[0] for v in columns]]
        data.rename(columns=dict(columns), inplace=True)

        # More data cleaning, column by column, deal with decimal comma vs point.
        for col in data:
            if col == "date":
                continue
            if classification.decimal_comma:
                data[col] = pd.Series(
                    [standardise_float_comma(val) for val in data[col].values],
                    index=matrix.index,
                )
            else:
                data[col] = pd.Series(
                    [standardise_float(val) for val in data[col].values],
                    index=matrix.index,
                )

        # Eliminate NAs
        data_columns = [column[1] for column in columns if column[1] != "date"]
        data = data.dropna(axis=0, how="all", subset=data_columns)

        # Deal with cumulative and incremental data
        if classification.accumulate:
            # assumes that if incremental it only works with VALUE
            # (MAXIMUM and MINIMUM are excluded)
            if classification.incremental:
                data["value"] = data["value"].diff()
                data.loc[data["value"] < 0, "value"] = np.nan
                data = data.dropna()
            data["date"] = data["date"].apply(
                lambda x: x.replace(
                    minute=int(x.minute / 5) * 5, second=0, microsecond=0, nanosecond=0
                )
            )
            data["date"] = data["date"] + pd.Timedelta(minutes=5)
            count = data.groupby("date")["value"].sum().to_frame()
            data = count["value"] * float(classification.resolution)

            start_date = start_date.replace(
                minute=int(start_date.minute / 5) * 5,
                second=0,
                microsecond=0,
                nanosecond=0,
            ) + pd.Timedelta(minutes=5)
            end_date = end_date.replace(
                minute=int(end_date.minute / 5) * 5,
                second=0,
                microsecond=0,
                nanosecond=0,
            ) + pd.Timedelta(minutes=5)
            table = pd.date_range(
                start_date, end_date, freq="5min", name="date"
            ).to_frame()
            data = pd.concat([table, data], axis=1)
            data = data.fillna(0)

        # Deal with non cumulative but incremental data
        else:
            if classification.incremental:
                data["value"] = data["value"].diff()
                data.loc[data["value"] < 0, "value"] = np.nan
                data = data.dropna()
            if classification.resolution:
                data["value"] = data["value"] * float(classification.resolution)
        data["station_id"] = station.station_id
        # Add the data to the main dict
        variables_data[classification.variable.variable_code] = data

    return variables_data


def standardise_float(val_str):
    """
    Removes commas from strings representing numbers that use a full stop as a decimal
    separator.
    TODO: Fix bare except statement.
    Args: val_str: string or Number-like
    Returns: val_num: float or None
    """
    if isinstance(val_str, Number):
        return float(val_str)
    try:
        val_str = val_str.replace(",", "")
        val_num = float(val_str)
    except:
        val_num = None
    return val_num


def standardise_float_comma(val_str):
    """
    For strings representing numbers that use a comma as a decimal separator:
    (i) Removes full stops
    (ii) Replaces commas for full stops
    TODO: Fix bare except statement.
    Args: val_str: string or Number-like
    Returns: val_num: float or None
    """
    if isinstance(val_str, Number):
        return float(val_str)
    try:
        val_str = val_str.replace(".", "")
        val_str = val_str.replace(",", ".")
        val_num = float(val_str)
    except:
        val_num = None
    return val_num


def insert_level_rule(data_import, level_rule):
    """
    Calculates uncertainty based on difference between a level_rule object's value
    and the water level measurement, saving a new "StripLevelReading" object.
    TODO: What exactly does this do? What is the nivelagua (level_rule?) and why is it
    used in this way?
    Args:
        data_import: DataImportFull or DataImportTemp object.
        level_rule: TODO: ??
    Returns:
        None
    """

    water_level_measurements = WaterLevel.objects.filter(
        station_id=data_import.station_id, date=data_import.end_date
    )
    water_level = None
    for i in water_level_measurements:
        water_level = i
    if water_level is None:
        return False
    try:
        uncertainty = float(level_rule["value"]) - float(water_level.value)
    # TODO: Fix bare except
    except:
        return False
    StripLevelReading(
        station_id=data_import.station_id_id,
        data_import_date=data_import.date,
        data_start_date=data_import.start_date,
        date=data_import.end_date,
        calibrated=level_rule["calibrated"],
        value=float(level_rule["value"]),
        uncertainty=uncertainty,
        comments=level_rule["comments"],
    ).save()


def query_formats(station):
    """
    Return dict of file formats associated with a given station in the form
    {format_id: format_name, ...}.
    """

    association = list(Association.objects.filter(station=station))
    results = {}
    for item in association:
        results[item.format.format_id] = item.format.name
    return results
