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
from datetime import datetime, timedelta
from numbers import Number

import numpy as np
import pandas as pd
from django.db import connection, transaction

from djangomain.settings import BASE_DIR
from formatting.models import Association, Classification
from importacion.models import DataImportFull, DataImportTemp
from medicion.models import Var11Medicion, Var14Medicion
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
        var_id = str(classification.variable.variable_id)
        station_id = str(station.station_id)
        last_upload_date = get_last_uploaded_date(station_id, var_id)
        exists = data_exists_between_dates(start_date, end_date, station_id, var_id)
        overwrite = overwrite or exists
        summary = {
            "variable_id": classification.variable.var_id,
            "variable_code": classification.variable.variable_code,
            "variable_name": classification.variable.name,
            "last_upload_date": last_upload_date,
            "exists": exists,
        }
        result.append(summary)
    return result, overwrite


def get_last_uploaded_date(station_id, var_id):
    """
    Retrieves the last date that data was uploaded for a given station ID and variable
    ID.
    TODO: this will likely need a lot of reworking once the Medicion module is
        overhauled.
    """
    print("last_date: " + str(time.ctime()))
    sql = "SELECT  date FROM medicion_var" + str(int(var_id)) + "medicion "
    sql += " WHERE station_id=" + str(int(station_id))
    sql += " ORDER BY date DESC LIMIT 1"
    with connection.cursor() as cursor:
        cursor.execute(sql)
        consulta = cursor.fetchone()
    if consulta:
        informacion = consulta[0]
    else:
        informacion = "No existen datos"
    return informacion


def data_exists_between_dates(start, end, station_id, var_id):
    """
    Checks whether there exists data for a given station and variable type between two
    dates.
        Returns: True if there exists data, else False.
    TODO: This will need reworking once Medicion module is overhauled.
    """

    sql = "SELECT id FROM medicion_var" + str(var_id) + "medicion "
    sql += " WHERE date >= %s  AND date <= %s AND station_id = %s "
    sql += " LIMIT 1;"
    query = globals()["Var" + str(var_id) + "Medicion"].objects.raw(
        sql, (start, end, station_id)
    )
    query = list(query)
    if len(query) > 0:
        return True
    return False


def preformat_matrix(source_file, file_format):
    """
    First step for importing data. Works out what sort of file is being read and adds
    standardised columns for date and datetime (str). This is used in construc_matrix.
    Args:
        source_file: path to (?) raw data file.
        file_format: formatting.Format object.
    Returns:
        Pandas.DataFrame with raw data read and extra column(s) for date and datetime
        (Str), which should be parsed correctly here.
    """
    firstline = file_format.first_row if file_format.first_row else 0
    skipfooter = file_format.footer_rows if file_format.footer_rows else 0

    if file_format.extension.value in ["xlsx", "xlx"]:
        # If in Excel format
        file = pd.read_excel(
            source_file,
            header=None,
            skiprows=firstline - 1,
            skipfooter=skipfooter,
            engine=None,
            error_bad_lines=False,
            index_col=None,
        )
    else:
        # Is not Excel format e.g. CSV
        engine = "c"
        if not isinstance(source_file, str):
            # The file was uploaded as binary
            lines = len(source_file.readlines())
            source_file.seek(0)
            skiprows = [i - 1 for i in range(1, firstline)] + [
                i - 1 for i in range(lines, lines - skipfooter, -1)
            ]
            skipfooter = 0
        else:
            # The file can be read as a string
            skiprows = firstline - 1
            if skipfooter > 0:
                engine = "python"

        # Deal with the delimiter
        delimiter = file_format.delimiter.character
        if "\\x" in delimiter:
            delim_hexcode = delimiter.replace("\\x", "")
            delim_intcode = eval("0x" + delim_hexcode)
            delimiter = chr(delim_intcode)

        if delimiter == " ":
            file = pd.read_csv(
                source_file,
                delim_whitespace=True,
                header=None,
                index_col=False,
                skiprows=skiprows,
                skipfooter=skipfooter,
                engine=engine,
                encoding="ISO-8859-1",
                error_bad_lines=False,
            )
        else:
            file = pd.read_csv(
                source_file,
                sep=delimiter,
                header=None,
                index_col=False,
                skiprows=skiprows,
                skipfooter=skipfooter,
                engine=engine,
                encoding="ISO-8859-1",
                error_bad_lines=False,
            )

    datetime_format = file_format.date.code + " " + file_format.time.code
    if file_format.date_column == file_format.time_column:
        file["date"] = pd.Series(
            [
                standardise_datetime(row, datetime_format)
                for row in file[file_format.date_column - 1].values
            ],
            index=file.index,
        )
    else:
        date_items = file_format.date.code.split(delimiter)
        date_cols = list(
            range(
                file_format.date_column - 1,
                file_format.date_column - 1 + len(date_items),
            )
        )
        time_items = file_format.time.code.split(delimiter)
        time_cols = list(
            range(
                file_format.for_col_hora - 1,
                file_format.for_col_hora - 1 + len(time_items),
            )
        )
        cols = date_cols + time_cols
        file["datetime_str"] = pd.Series(
            [" ".join(row.astype(str)) for row in file[cols].values],
            index=file.index,
        )
        file["date"] = pd.Series(
            [
                standardise_datetime(row, datetime_format)
                for row in file["datetime_str"].values
            ],
            index=file.index,
        )

    file = file.sort_values("date")
    file = file.reset_index(drop=True)

    # Conversion in case of UTC date file_format
    if file_format.utc_date:
        file["date"] = file["date"] - timedelta(hours=5)
    return file


def standardise_datetime(date_time, datetime_format):
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
        date_time = datetime.utcfromtimestamp((date_time - unix_epoch) / one_second)
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


def save_temp_data_to_permanent(imp_id, form):
    """
    Function to pass the temporary import to the final table.
    NOTE: Uses a lot of pure sql to insert the data, overwriting if it already exists.
        This could probably be rewritten in python and won't work after medicion has
        been overhauled anyway.
    TODO: Overall, this is an important function for importing but can probably be
        seriously simplified.
    """
    data_import_temp = DataImportTemp.objects.get(data_import_id=imp_id)
    file_format = data_import_temp.format
    station = data_import_temp.station
    file_path = str(BASE_DIR) + "/media/" + str(data_import_temp.file)

    all_data = construct_matrix(file_path, file_format, station)
    for var_id, table in all_data.items():
        table = table.where((pd.notnull(table)), None)
        data = list(table.itertuples(index=False, name=None))
        sql = """
WITH
data AS (
    SELECT DISTINCT u.date, u.valor, u.station_id
    FROM unnest(%s::fecha__valor__station_id[]) u
    ORDER BY u.date ASC
),
eliminar AS (
    DELETE FROM medicion_var1medicion
    WHERE station_id = (SELECT d.station_id FROM data d LIMIT 1)
    AND date >= (SELECT d.date FROM data d ORDER BY d.date ASC LIMIT 1)
    AND date <= (SELECT d.date FROM data d ORDER BY d.date DESC LIMIT 1)
    returning *
)
INSERT INTO medicion_var1medicion(date, valor, station_id)
SELECT d.date, d.valor, d.station_id
FROM data d
;
"""
        sql = sql.replace("var1", "var" + str(var_id))
        sql = sql.replace(
            "u.date, u.valor, u.station_id", "u." + ", u.".join(table.columns)
        )
        sql = sql.replace("fecha__valor__station_id", "__".join(table.columns))
        sql = sql.replace("date, valor, station_id", ", ".join(table.columns))
        sql = sql.replace(
            "d.date, d.valor, d.station_id", "d." + ", d.".join(table.columns)
        )

        with connection.cursor() as cursor:
            cursor.execute(
                sql,
                [
                    data,
                ],  # NOQA
            )

    final_file_path = str(data_import_temp.file).replace("files/tmp/", "files/")
    final_file_path_full = str(BASE_DIR) + "/media/" + final_file_path
    shutil.copy(file_path, final_file_path_full)
    data_import_full = DataImportFull(
        station=data_import_temp.station,
        format=data_import_temp.format,
        date=data_import_temp.date,
        start_date=data_import_temp.start_date,
        end_date=data_import_temp.end_date,
        file=final_file_path,
        observations=data_import_temp.observations,
        user=data_import_temp.user,
    )
    file_path_full = str(BASE_DIR) + "/media/" + str(data_import_temp.file)
    # Delete the temp object and save the full one
    with transaction.atomic():
        data_import_full.save()
        data_import_temp.delete()
    # Remove the temp file itself using os.remove...
    os.remove(file_path_full)
    return data_import_full.data_import_id


def construct_matrix(matrix_source, file_format, station):
    """
    Construct the "matrix" or results table. Does various cleaning / simple
    transformations depending on the date format, type of data (accumulated,
    incremental...) and deals with NANs.
    Args:
        matrix_source: raw data file (file path?)
        file_format: a formatting.Format object.
    Returns: Dict of dataframes for results (one for each variable type in the raw data
        file).
    TODO: Probably refactor into smaller chunks.
    """

    # Get the "preformatted matrix" sorted by date col
    matrix = preformat_matrix(matrix_source, file_format)
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
                data.loc[data["valor"] < 0, "valor"] = np.nan
                data = data.dropna()
            data["date"] = data["date"].apply(
                lambda x: x.replace(
                    minute=int(x.minute / 5) * 5, second=0, microsecond=0, nanosecond=0
                )
            )
            data["date"] = data["date"] + pd.Timedelta(minutes=5)
            count = data.groupby("date")["value"].sum().to_frame()
            data = count["value"] * float(classification.resolucion)

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
        variables_data[classification.variable_id] = data

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
    and the water level measurement, saving a new "Var14" object.
    TODO: What exactly does this do? What is the nivelagua (level_rule?) and why is it
    used in this way?
    Args:
        data_import: DataImportFull or DataImportTemp object.
        level_rule: TODO: ??
    Returns:
        None
    """

    water_level_measurements = Var11Medicion.objects.filter(
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
    Var14Medicion(
        station_id=data_import.station_id_id,
        fecha_importacion=data_import.imp_fecha,
        fecha_inicio=data_import.imp_fecha_ini,
        date=data_import.imp_fecha_fin,
        calibrado=level_rule["calibrated"],
        valor=float(level_rule["value"]),
        uncertainty=uncertainty,
        comentario=level_rule["comments"],
    ).save()


# consultar formatos por datalogger y estacion
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
