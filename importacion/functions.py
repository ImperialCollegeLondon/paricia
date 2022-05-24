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

unix_epoch = np.datetime64(0, "s")
one_second = np.timedelta64(1, "s")


def validar_fechas(data_import):
    """
    Verify if the data to be imported exists.
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
    sql = "SELECT  fecha FROM medicion_var" + str(int(var_id)) + "medicion "
    sql += " WHERE station_id=" + str(int(station_id))
    sql += " ORDER BY fecha DESC LIMIT 1"
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
    sql += " WHERE fecha >= %s  AND fecha <= %s AND station_id = %s "
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

    all_data = construir_matriz(file_path, file_format, station)
    for var_id, table in all_data.items():
        table = table.where((pd.notnull(table)), None)
        data = list(table.itertuples(index=False, name=None))
        sql = """
WITH
data AS (
    SELECT DISTINCT u.fecha, u.valor, u.station_id
    FROM unnest(%s::fecha__valor__station_id[]) u
    ORDER BY u.fecha ASC
),
eliminar AS (
    DELETE FROM medicion_var1medicion
    WHERE station_id = (SELECT d.station_id FROM data d LIMIT 1)
    AND fecha >= (SELECT d.fecha FROM data d ORDER BY d.fecha ASC LIMIT 1)
    AND fecha <= (SELECT d.fecha FROM data d ORDER BY d.fecha DESC LIMIT 1)
    returning *
)
INSERT INTO medicion_var1medicion(fecha, valor, station_id)
SELECT d.fecha, d.valor, d.station_id
FROM data d
;
"""
        sql = sql.replace("var1", "var" + str(var_id))
        sql = sql.replace(
            "u.fecha, u.valor, u.station_id", "u." + ", u.".join(table.columns)
        )
        sql = sql.replace("fecha__valor__station_id", "__".join(table.columns))
        sql = sql.replace("fecha, valor, station_id", ", ".join(table.columns))
        sql = sql.replace(
            "d.fecha, d.valor, d.station_id", "d." + ", d.".join(table.columns)
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


def construir_matriz(matriz_src, formato, station):
    # TODO : Eliminar validar_datalogger, validar acumulado
    # determinar si debemos restar 5 horas a la fecha del archivo
    # cambiar_fecha = validar_datalogger(formato.mar_id)
    cambiar_fecha = False

    # Preformato entrega matriz ordenada por fecha
    matriz = preformat_matrix(matriz_src, formato)
    fecha_ini = matriz.loc[0, "fecha"]
    fecha_fin = matriz.loc[matriz.shape[0] - 1, "fecha"]

    clasificacion = list(Classification.objects.filter(for_id=formato.for_id))
    datos_variables = {}
    for var in clasificacion:
        columnas = []
        columnas.append(("fecha", "fecha"))
        ##
        columnas.append((var.cla_valor - 1, "valor"))
        if var.col_validador_valor:
            # matriz[var.cla_valor - 1][matriz[var.col_validador_valor - 1] != var.txt_validador_valor] = np.nan
            matriz.loc[
                matriz[var.col_validador_valor - 1] != var.txt_validador_valor,
                var.cla_valor - 1,
            ] = np.nan
        ##
        if var.cla_maximo:
            columnas.append((var.cla_maximo - 1, "maximo"))
        if var.col_validador_maximo:
            # matriz[var.cla_maximo - 1][matriz[var.col_validador_maximo - 1] != var.txt_validador_maximo] = np.nan
            matriz.loc[
                matriz[var.col_validador_maximo - 1] != var.txt_validador_maximo,
                var.cla_maximo - 1,
            ] = np.nan
        ##
        if var.cla_minimo:
            columnas.append((var.cla_minimo - 1, "minimo"))
        if var.col_validador_minimo:
            # matriz[var.cla_minimo - 1][matriz[var.col_validador_minimo - 1] != var.txt_validador_minimo] = np.nan
            matriz.loc[
                matriz[var.col_validador_minimo - 1] != var.txt_validador_minimo,
                var.cla_minimo - 1,
            ] = np.nan
        ##

        datos = matriz.loc[:, [v[0] for v in columnas]]
        datos.rename(columns=dict(columnas), inplace=True)

        for col in datos:
            if col == "fecha":
                continue

            if var.coma_decimal:
                datos[col] = pd.Series(
                    [numero_coma_decimal(val) for val in datos[col].values],
                    index=matriz.index,
                )
            else:
                datos[col] = pd.Series(
                    [numero_punto_decimal(val) for val in datos[col].values],
                    index=matriz.index,
                )

        ## Eliminar NAs
        columnas_datos = [columna[1] for columna in columnas if columna[1] != "fecha"]
        datos = datos.dropna(axis=0, how="all", subset=columnas_datos)

        if var.acumular:
            # Se asume que si es incremental solo trabaja con VALOR (Se excluye MAXIMO y MINIMO)
            if var.incremental:
                datos["valor"] = datos["valor"].diff()
                # datos['valor'][datos['valor'] < 0] = np.nan
                datos.loc[datos["valor"] < 0, "valor"] = np.nan
                datos = datos.dropna()
            datos["fecha"] = datos["fecha"].apply(
                lambda x: x.replace(
                    minute=int(x.minute / 5) * 5, second=0, microsecond=0, nanosecond=0
                )
            )
            datos["fecha"] = datos["fecha"] + pd.Timedelta(minutes=5)
            cuenta = datos.groupby("fecha")["valor"].sum().to_frame()
            datos = cuenta["valor"] * float(var.resolucion)

            fecha_ini = fecha_ini.replace(
                minute=int(fecha_ini.minute / 5) * 5,
                second=0,
                microsecond=0,
                nanosecond=0,
            ) + pd.Timedelta(minutes=5)
            fecha_fin = fecha_fin.replace(
                minute=int(fecha_fin.minute / 5) * 5,
                second=0,
                microsecond=0,
                nanosecond=0,
            ) + pd.Timedelta(minutes=5)
            tabla = pd.date_range(
                fecha_ini, fecha_fin, freq="5min", name="fecha"
            ).to_frame()
            datos = pd.concat([tabla, datos], axis=1)
            datos = datos.fillna(0)
        else:
            if var.incremental:
                datos["valor"] = datos["valor"].diff()
                # datos['valor'][datos['valor'] < 0] = np.nan
                datos.loc[datos["valor"] < 0, "valor"] = np.nan
                datos = datos.dropna()
            if var.resolucion:
                datos["valor"] = datos["valor"] * float(var.resolucion)
        datos["station_id"] = station.station_id
        datos_variables[var.var_id_id] = datos
    return datos_variables


def numero_punto_decimal(val_str):
    if isinstance(val_str, Number):
        return float(val_str)
    try:
        val_str = val_str.replace(",", "")
        val_num = float(val_str)
    except:
        val_num = None
    return val_num


def numero_coma_decimal(val_str):
    if isinstance(val_str, Number):
        return float(val_str)
    try:
        val_str = val_str.replace(".", "")
        val_str = val_str.replace(",", ".")
        val_num = float(val_str)
    except:
        val_num = None
    return val_num


def insertar_nivel_regleta(importacion, nivelregleta):
    nivelagua_mediciones = Var11Medicion.objects.filter(
        station_id=importacion.station_id_id, fecha=importacion.imp_fecha_fin
    )
    nivelagua = None
    for i in nivelagua_mediciones:
        nivelagua = i
    if nivelagua is None:
        return False
    try:
        incertidumbre = float(nivelregleta["valor"]) - float(nivelagua.valor)
    except:
        return False
    Var14Medicion(
        station_id=importacion.station_id_id,
        fecha_importacion=importacion.imp_fecha,
        fecha_inicio=importacion.imp_fecha_ini,
        fecha=importacion.imp_fecha_fin,
        calibrado=nivelregleta["calibrado"],
        valor=float(nivelregleta["valor"]),
        incertidumbre=incertidumbre,
        comentario=nivelregleta["comentario"],
    ).save()


# consultar formatos por datalogger y estacion
def consultar_formatos(station):
    asociacion = list(Association.objects.filter(station=station))
    lista = {}
    for item in asociacion:
        lista[item.for_id.for_id] = item.for_id.for_nombre
    return lista


def get_modelo(var_id):
    variable = Variable.objects.get(var_id=var_id)
    modelo = globals()[variable.var_modelo]
    return modelo
