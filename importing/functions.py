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
import zoneinfo
from datetime import datetime
from logging import getLogger
from numbers import Number
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from django.conf import settings
from django.core.exceptions import ValidationError

from formatting.models import Classification, Format
from measurement.models import Measurement

unix_epoch = np.datetime64(0, "s")
one_second = np.timedelta64(1, "s")


def validate_dates(data_import):
    """Verify if there already exists data for the dates of the data being imported.

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

        # Check if data exists between dates)
        query = Measurement.timescale.filter(
            time__range=[start_date, end_date],
            station_id=station.station_id,
            variable_id=classification.variable.variable_id,
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


def get_last_uploaded_date(station_id: int, var_code: str) -> datetime | None:
    """Get the last date of uploaded data for a given station ID and variable code.

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
    if not isinstance(source_file, str | Path):
        # The file was uploaded as binary
        lines = len(source_file.readlines())
        source_file.seek(0)
        skiprows = [i for i in range(0, firstline - 1)] + [
            i - 1 for i in range(lines, lines - skipfooter, -1)
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
                for row in data.iloc[:, file_format.date_column - 1].values
            ],
            index=data.index,
        )
    else:
        cols = file_format.datetime_columns(file_format.delimiter.character)
        data["datetime_str"] = data.iloc[:, cols].agg(
            lambda row: " ".join([str(r) for r in row]), axis=1
        )
        data["date"] = data["datetime_str"].apply(
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


def standardise_datetime(date_time: Any, datetime_format: str) -> datetime:
    """Returns a datetime object in the case that date_time is not already in that form.

    Args:
        date_time: The date_time to be transformed.
        datetime_format: The format that date_time is in (to be passed to
            datetime.strptime()).

    Returns:
        A datetime object or None if date_time is not in a recognised format.
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
    except Exception as e:
        getLogger().error(f"Error parsing date: {date_time} - {e}")
        raise e
    return _date_time


def save_temp_data_to_permanent(data_import_temp):
    """Function to pass the temporary import to the final table.

    Uses the data_import_temp object only to get all required information from its
    fields.

    This function carries out the following steps:

    - Bulk delete of existing data between two times on a given measurement table for
    the station in question.
    - Bulk create to add the new data from the uploaded file.

    Args:
        data_import_temp: DataImportTemp object.
    """
    file_format = data_import_temp.format
    station = data_import_temp.station

    file_path = Path(settings.MEDIA_ROOT) / Path(str(data_import_temp.file))

    all_data = construct_matrix(file_path, file_format, station)
    if not all_data:
        msg = "No data to import. Is the chosen format correct?"
        getLogger().error(msg)
        raise ValidationError(msg)

    must_cols = ["station_id", "variable_id", "date", "value"]
    for table in all_data:
        cols = [
            c for c in table.columns if c in Measurement._meta.fields or c in must_cols
        ]
        table = (
            table[cols]
            .dropna(axis=0, subset=must_cols)
            .rename(columns={"date": "time"})
        )
        records = table.to_dict("records")
        variable_id = table["variable_id"].iloc[0]

        # Delete existing data between the date ranges
        Measurement.timescale.filter(
            time__range=[data_import_temp.start_date, data_import_temp.end_date],
            station_id=station.station_id,
            variable_id=variable_id,
        ).delete()

        # Bulk add new data
        model_instances = [Measurement(**record) for record in records]

        # Call the clean method. List comprehension is faster
        [instance.clean() for instance in model_instances]

        # WARNING: This is a bulk insert, so it will not call the save()
        # method nor send the pre_save or post_save signals for each instance.
        Measurement.objects.bulk_create(model_instances)


def construct_matrix(matrix_source, file_format, station) -> list[pd.DataFrame]:
    """Construct the "matrix" or results table. Does various cleaning / simple
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
    start_date = matrix["date"].iloc[0]
    end_date = matrix["date"].iloc[-1]

    classifications = list(Classification.objects.filter(format=file_format))
    to_ingest = []
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

        data = matrix.loc[:, [v[0] for v in columns]].rename(columns=dict(columns))

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
        data["variable_id"] = classification.variable.variable_id

        # Add the data to the main list
        to_ingest.append(data)

    return to_ingest


def standardise_float(val_str):
    """Removes commas from strings for numbers that use a period as a decimal separator.

    Args: val_str: string or Number-like
    Returns: val_num: float or None
    """
    if isinstance(val_str, Number):
        return float(val_str)
    try:
        val_str = val_str.replace(",", "")
        val_num = float(val_str)
    except ValueError:
        val_num = None
    return val_num


def standardise_float_comma(val_str):
    """For strings representing numbers that use a comma as a decimal separator:
    (i) Removes full stops
    (ii) Replaces commas for full stops
    Args: val_str: string or Number-like
    Returns: val_num: float or None
    """
    if isinstance(val_str, Number):
        return float(val_str)
    try:
        val_str = val_str.replace(".", "")
        val_str = val_str.replace(",", ".")
        val_num = float(val_str)
    except ValueError:
        val_num = None
    return val_num
