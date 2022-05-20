# -*- coding: utf-8 -*-

################################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos (iMHEA)
# basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#         Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS), Ecuador.
#         Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones creadoras,
#              ya sea en uso total o parcial del código.

import io
import os
import shutil
import time
from datetime import datetime, timedelta
from numbers import Number

import numpy as np
import pandas as pd
from django.db import connection, transaction

from djangomain.settings import BASE_DIR
from formato.models import Association, Clasification, Date, Hora
from importacion.models import Importacion, ImportacionTemp
from medicion.models import (
    Var1Medicion,
    Var2Medicion,
    Var3Medicion,
    Var4Medicion,
    Var5Medicion,
    Var6Medicion,
    Var7Medicion,
    Var8Medicion,
    Var9Medicion,
    Var10Medicion,
    Var11Medicion,
    Var12Medicion,
    Var13Medicion,
    Var14Medicion,
    Var15Medicion,
    Var16Medicion,
    Var17Medicion,
    Var18Medicion,
    Var19Medicion,
    Var20Medicion,
    Var21Medicion,
    Var22Medicion,
    Var23Medicion,
    Var24Medicion,
)

unix_epoch = np.datetime64(0, "s")
one_second = np.timedelta64(1, "s")

# verificar si existen los datos
def validar_fechas(importacion):
    fecha_ini = importacion.imp_fecha_ini
    fecha_fin = importacion.imp_fecha_fin
    for_id_id = importacion.for_id_id
    estacion = importacion.est_id
    clasificacion = list(Clasification.objects.filter(for_id=for_id_id))

    sobrescribe = False
    result = []
    for fila in clasificacion:
        var_id = str(fila.var_id.var_id)
        est_id = str(estacion.est_id)
        ultima_fecha = ultima_fecha_cargada(est_id, var_id)
        existe = existe_fechas(fecha_ini, fecha_fin, est_id, var_id)
        sobrescribe = sobrescribe or existe
        resumen = {
            "var_id": fila.var_id.var_id,
            "var_cod": fila.var_id.var_codigo,
            "var_nombre": fila.var_id.var_nombre,
            "ultima_fecha": ultima_fecha,
            "existe": existe,
        }
        result.append(resumen)
    return result, sobrescribe


def ultima_fecha_cargada(est_id, var_id):
    print("ultima_fecha: " + str(time.ctime()))
    sql = "SELECT  fecha FROM medicion_var" + str(int(var_id)) + "medicion "
    sql += " WHERE estacion_id=" + str(int(est_id))
    sql += " ORDER BY fecha DESC LIMIT 1"
    with connection.cursor() as cursor:
        cursor.execute(sql)
        consulta = cursor.fetchone()
    if consulta:
        informacion = consulta[0]
    else:
        informacion = "No existen datos"
    return informacion


def existe_fechas(ini, fin, est_id, var_id):
    sql = "SELECT id FROM medicion_var" + str(var_id) + "medicion "
    sql += " WHERE fecha >= %s  AND fecha <= %s AND estacion_id = %s "
    sql += " LIMIT 1;"
    query = globals()["Var" + str(var_id) + "Medicion"].objects.raw(
        sql, (ini, fin, est_id)
    )
    consulta = list(query)
    if len(consulta) > 0:
        return True
    return False


def preformato_matriz(archivo_src, formato):
    firstline = formato.for_fil_ini if formato.for_fil_ini else 0
    skipfooter = formato.for_fil_cola if formato.for_fil_cola else 0

    if formato.ext_id.ext_valor in ["xlsx", "xlx"]:
        # Es formato excel
        archivo = pd.read_excel(
            archivo_src,
            header=None,
            skiprows=firstline - 1,
            skipfooter=skipfooter,
            engine=None,
            error_bad_lines=False,
            index_col=None,
        )
    else:
        # No es formato excel
        engine = "c"
        if not isinstance(archivo_src, str):
            # El archivo se cargó como binario
            lines = len(archivo_src.readlines())
            archivo_src.seek(0)
            skiprows = [i - 1 for i in range(1, firstline)] + [
                i - 1 for i in range(lines, lines - skipfooter, -1)
            ]
            skipfooter = 0
        else:
            # El archivo es pasado como una cadena de texto
            skiprows = firstline - 1
            if skipfooter > 0:
                engine = "python"

        delimitador = formato.del_id.del_caracter
        if "\\x" in delimitador:
            delim_hexcode = delimitador.replace("\\x", "")
            delim_intcode = eval("0x" + delim_hexcode)
            delimitador = chr(delim_intcode)

        if delimitador == " ":
            archivo = pd.read_csv(
                archivo_src,
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
            archivo = pd.read_csv(
                archivo_src,
                sep=delimitador,
                header=None,
                index_col=False,
                skiprows=skiprows,
                skipfooter=skipfooter,
                engine=engine,
                encoding="ISO-8859-1",
                error_bad_lines=False,
            )

    formatofechahora = formato.fec_id.fec_codigo + " " + formato.hor_id.hor_codigo
    if formato.for_col_fecha == formato.for_col_hora:
        # TODO añadir column from a array para evitar usar pd.Series y que tenga TYPE DATETIMTE.DATETIME
        archivo["fecha"] = pd.Series(
            [
                verificar_fechahora(row, formatofechahora)
                for row in archivo[formato.for_col_fecha - 1].values
            ],
            index=archivo.index,
        )
    else:
        items_fecha = formato.fec_id.fec_codigo.split(delimitador)
        cols_fecha = list(
            range(
                formato.for_col_fecha - 1, formato.for_col_fecha - 1 + len(items_fecha)
            )
        )
        items_hora = formato.hor_id.hor_codigo.split(delimitador)
        cols_hora = list(
            range(formato.for_col_hora - 1, formato.for_col_hora - 1 + len(items_hora))
        )
        cols = cols_fecha + cols_hora
        # TODO añadir column from a array para evitar usar pd.Series y que tenga TYPE DATETIMTE.DATETIME
        archivo["fechahora_str"] = pd.Series(
            [" ".join(row.astype(str)) for row in archivo[cols].values],
            index=archivo.index,
        )
        archivo["fecha"] = pd.Series(
            [
                verificar_fechahora(row, formatofechahora)
                for row in archivo["fechahora_str"].values
            ],
            index=archivo.index,
        )

    archivo = archivo.sort_values("fecha")
    archivo = archivo.reset_index(drop=True)

    ### Conversión en caso de formato de fecha UTC
    if formato.es_fecha_utc == True:
        archivo["fecha"] = archivo["fecha"] - timedelta(hours=5)
    return archivo


def verificar_fechahora(fechahora, formatofechahora):
    if isinstance(fechahora, datetime):
        return fechahora
    elif isinstance(fechahora, np.datetime64):
        fechahora = datetime.utcfromtimestamp((fechahora - unix_epoch) / one_second)
        return fechahora
    elif isinstance(fechahora, str):
        pass
        # valores = fechahora.split(" ")
        # valores = list(filter(None, valores))
        # fechahora_str = valores[0].strip('\"') + ' ' + valores[1].strip('\"')

    elif isinstance(fechahora, list):
        fechahora = " ".join(fechahora)

    elif isinstance(fechahora, pd.Series):
        fechahora = " ".join([str(val) for val in list(fechahora[:])])

    else:
        fechahora = ""

    try:
        _fechahora = datetime.strptime(fechahora, formatofechahora)
    except:
        _fechahora = None
    return _fechahora


# Esta funcion pasa la importación temporal a final
def guardar_datos__temp_a_final(imp_id, form):
    importaciontemp = ImportacionTemp.objects.get(imp_id=imp_id)
    formato = importaciontemp.for_id
    estacion = importaciontemp.est_id
    ruta = str(BASE_DIR) + "/media/" + str(importaciontemp.imp_archivo)

    datos = construir_matriz(ruta, formato, estacion)
    for var_id, tabla in datos.items():
        tabla = tabla.where((pd.notnull(tabla)), None)
        data = list(tabla.itertuples(index=False, name=None))
        sql = """
WITH
data AS (
    SELECT DISTINCT u.fecha, u.valor, u.estacion_id 
    FROM unnest(%s::fecha__valor__estacion_id[]) u
    ORDER BY u.fecha ASC
),
eliminar AS (
    DELETE FROM medicion_var1medicion
    WHERE estacion_id = (SELECT d.estacion_id FROM data d LIMIT 1)
    AND fecha >= (SELECT d.fecha FROM data d ORDER BY d.fecha ASC LIMIT 1) 
    AND fecha <= (SELECT d.fecha FROM data d ORDER BY d.fecha DESC LIMIT 1) 
    returning *
)
INSERT INTO medicion_var1medicion(fecha, valor, estacion_id)
SELECT d.fecha, d.valor, d.estacion_id 
FROM data d
;
"""
        sql = sql.replace("var1", "var" + str(var_id))
        sql = sql.replace(
            "u.fecha, u.valor, u.estacion_id", "u." + ", u.".join(tabla.columns)
        )
        sql = sql.replace("fecha__valor__estacion_id", "__".join(tabla.columns))
        sql = sql.replace("fecha, valor, estacion_id", ", ".join(tabla.columns))
        sql = sql.replace(
            "d.fecha, d.valor, d.estacion_id", "d." + ", d.".join(tabla.columns)
        )

        with connection.cursor() as cursor:
            cursor.execute(
                sql,
                [
                    data,
                ],
            )

    ruta_final = str(importaciontemp.imp_archivo).replace("archivos/tmp/", "archivos/")
    ruta_final_full = str(BASE_DIR) + "/media/" + ruta_final
    shutil.copy(ruta, ruta_final_full)
    importacion = Importacion(
        est_id=importaciontemp.est_id,
        for_id=importaciontemp.for_id,
        imp_fecha=importaciontemp.imp_fecha,
        imp_fecha_ini=importaciontemp.imp_fecha_ini,
        imp_fecha_fin=importaciontemp.imp_fecha_fin,
        imp_archivo=ruta_final,
        imp_observacion=importaciontemp.imp_observacion,
        usuario=importaciontemp.usuario,
    )
    ruta_original_full = str(BASE_DIR) + "/media/" + str(importaciontemp.imp_archivo)
    with transaction.atomic():
        importacion.save()
        importaciontemp.delete()
    os.remove(ruta_original_full)
    return importacion.imp_id


def construir_matriz(matriz_src, formato, estacion):
    # TODO : Eliminar validar_datalogger, validar acumulado
    # determinar si debemos restar 5 horas a la fecha del archivo
    # cambiar_fecha = validar_datalogger(formato.mar_id)
    cambiar_fecha = False

    # Preformato entrega matriz ordenada por fecha
    matriz = preformato_matriz(matriz_src, formato)
    fecha_ini = matriz.loc[0, "fecha"]
    fecha_fin = matriz.loc[matriz.shape[0] - 1, "fecha"]

    clasificacion = list(Clasification.objects.filter(for_id=formato.for_id))
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
        datos["estacion_id"] = estacion.est_id
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
        estacion_id=importacion.est_id_id, fecha=importacion.imp_fecha_fin
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
        estacion_id=importacion.est_id_id,
        fecha_importacion=importacion.imp_fecha,
        fecha_inicio=importacion.imp_fecha_ini,
        fecha=importacion.imp_fecha_fin,
        calibrado=nivelregleta["calibrado"],
        valor=float(nivelregleta["valor"]),
        incertidumbre=incertidumbre,
        comentario=nivelregleta["comentario"],
    ).save()


# consultar formatos por datalogger y estacion
def consultar_formatos(estacion):
    asociacion = list(Association.objects.filter(est_id=estacion))
    lista = {}
    for item in asociacion:
        lista[item.for_id.for_id] = item.for_id.for_nombre
    return lista


#
# def procesar_archivo_automatico(archivo, formato, estacion):
#     datos = construir_matriz(archivo, formato, estacion)
#     return datos
#
#

# # verficar vacios
# def verificar_vacios(fecha_archivo, fecha_datos):
#     estado = False
#     vacios = []
#     # fecha_datos=list(medicion)[0].get('med_fecha').date()
#     if isinstance(fecha_datos, str):
#         estado = False
#     else:
#         intervalo = timedelta(days=1)
#         fecha_datos += intervalo
#         if fecha_datos >= fecha_archivo:
#             estado = False
#         else:
#             estado = True
#     return estado
#
#
# # def guardar_vacios(informacion, estacion, observacion, fecha_archivo):
# #     variable = Variable.objects.get(var_id=informacion.get('var_id'))
# #     vacio = Vacios(est_id=estacion, var_id=variable,
# #                    vac_fecha_ini=informacion.get('ultima_fecha').date(),
# #                    vac_hora_ini=informacion.get('ultima_fecha').time(),
# #                    vac_fecha_fin=fecha_archivo.date(),
# #                    vac_hora_fin=fecha_archivo.time(),
# #                    vac_observacion=observacion)
# #     vacio.save()
#
#
#
#
# # eliminar informacion en caso de existir
# def eliminar_datos(informacion, importacion):
#     fecha_ini = importacion.imp_fecha_ini
#     fecha_fin = importacion.imp_fecha_fin
#     fec_ini = str(fecha_ini)
#     fec_fin = str(fecha_fin)
#     year_ini = fecha_ini.strftime('%Y')
#     year_fin = fecha_fin.strftime('%Y')
#     est_id = str(importacion.est_id.est_id)
#     var_cod = informacion.get('var_cod')
#     var_id = informacion.get('var_id')
#     if year_ini == year_fin:
#         sql = 'DELETE FROM  medicion_var' + str(var_id) + 'medicion '
#         sql += ' WHERE estacion_id=' + str(est_id)
#         sql += '  AND fecha>=\'' + fec_ini + '\''
#         sql += '  AND fecha<=\'' + fec_fin + '\''
#         with connection.cursor() as cursor:
#             cursor.execute(sql)
#     else:
#         range_year = range(int(year_ini), int(year_fin) + 1)
#         for year in range_year:
#             if str(year) == year_ini:
#                 sql = 'DELETE FROM  medicion_var' + str(var_id) + 'medicion '
#                 sql += ' WHERE estacion_id=' + str(est_id)
#                 sql += '   AND fecha>=\'' + fec_ini + '\''
#
#             elif str(year) == year_fin:
#                 sql = 'DELETE FROM  medicion_var' + str(var_id) + 'medicion '
#                 sql += ' WHERE estacion_id=' + str(est_id)
#                 sql += '   AND fecha<=\'' + fec_fin + '\''
#
#             else:
#                 sql = 'DELETE FROM  medicion_var' + str(var_id) + 'medicion '
#                 sql += ' WHERE estacion_id=' + str(est_id)
#             with connection.cursor() as cursor:
#                 cursor.execute(sql)
#
#
#
# # validar si son datalogger VAISALA para restar 5 horas
# def validar_datalogger(marca):
#     try:
#         if marca.mar_nombre == 'VAISALA':
#             return True
#     except:
#         pass
#     return False
#
#
# def validar_acumulado(marca):
#     try:
#         if marca.mar_nombre == 'HOBO':
#             return True
#     except:
#         pass
#     return False
#
#
# # convertir fecha y hora a DATETIME
# def formato_fecha(formato, valores, cambiar_fecha):
#     if formato.for_col_fecha == formato.for_col_hora:
#         separar = valores[formato.for_col_fecha - 1].split(" ")
#         fecha_str = separar[0]
#         hora_str = separar[1]
#         if len(separar) == 3:
#             hora_str += ' ' + separar[2]
#     else:
#         ## TODO incluir código original para comparación de eficiencia
#         fecha_str = ''
#         items_fecha = formato.fec_id.fec_codigo.split(formato.del_id.del_caracter)
#         for shift in range(len(items_fecha)):
#             fecha_str = fecha_str + ' ' + valores[formato.for_col_fecha - 1 + shift ]
#         fecha_str = fecha_str.strip()
#
#         # hora_str = valores[formato.for_col_hora - 1]
#         hora_str = ''
#         items_hora = formato.hor_id.hor_codigo.split(formato.del_id.del_caracter)
#         for shift in range(len(items_hora)):
#             hora_str = hora_str + ' ' + valores[formato.for_col_hora - 1 + shift]
#         hora_str = hora_str.strip()
#
#     fecha_str = fecha_str.strip('\"')
#     hora_str = hora_str.strip('\"')
#
#     fechahora_str = fecha_str + ' ' + hora_str
#     formato_str = formato.fec_id.fec_codigo + ' ' + formato.hor_id.hor_codigo
#     try:
#         fecha_hora = datetime.strptime(fechahora_str, formato_str)
#     except:
#         fecha_hora = None
#
#     if cambiar_fecha:
#         intervalo = timedelta(hours=5)
#         fecha_hora -= intervalo
#     return fecha_hora
#
#
# def cambiar_formato_fecha(formato, fecha_str):
#     con_fecha = list(Fecha.objects.exclude(fec_id=formato.fec_id.fec_id))
#     for fila in con_fecha:
#         try:
#             fecha = datetime.strptime(fecha_str, fila.fec_codigo)
#             formato.fec_id = fila
#             formato.save()
#             break
#         except ValueError:
#             pass
#     return fecha
#
#
# # busca un formato de hora para registro del archivo
# def cambiar_formato_hora(formato, hora_str):
#     con_hora = list(Hora.objects.exclude(hor_id=formato.hor_id.hor_id))
#     for fila in con_hora:
#         try:
#             hora = datetime.strptime(hora_str, fila.hor_codigo)
#             formato.hor_id = fila
#             formato.save()
#             break
#         except ValueError:
#             pass
#     return hora
#
#

#
#
#
#
# # # obtener la fecha incial y final del archivo en base al formato
# # def get_fechas_archivo(archivo, formato, form):
# #     # cambiar_fecha = validar_datalogger(formato.mar_id)
# #     # TODO se podría usar las funciones de: construir_matrix2
# #     cambiar_fecha = False
# #     if formato.ext_id.ext_valor in ['xlsx', 'xlx']:
# #         book = xlrd.open_workbook(file_contents=archivo.read())
# #         sheet = book.sheet_by_index(0)
# #         nfila = sheet.nrows
# #         if formato.for_col_fecha != formato.for_col_hora:
# #             return form
# #         fechahora_ini = sheet.cell(formato.for_fil_ini - 1, formato.for_col_fecha - 1).value
# #         if formato.for_fil_cola:
# #             pos_fin = nfila - 1 - formato.for_fil_cola
# #         else:
# #             pos_fin = nfila - 1
# #         fechahora_fin = sheet.cell(pos_fin, formato.for_col_fecha - 1).value
# #         if type(fechahora_ini) is float:
# #             form.instance.imp_fecha_ini = datetime(*xlrd.xldate_as_tuple(fechahora_ini, book.datemode))
# #             form.instance.imp_fecha_fin = datetime(*xlrd.xldate_as_tuple(fechahora_fin, book.datemode))
# #             return form
# #         else:
# #             linea_ini = fechahora_ini
# #             linea_fin = fechahora_fin
# #     else:
# #         datos = archivo.readlines()
# #         linea_ini = datos[formato.for_fil_ini - 1].decode("utf-8", "ignore")
# #         if formato.for_fil_cola:
# #             pos_fin = len(datos) - 1 - formato.for_fil_cola
# #         else:
# #             pos_fin = len(datos) - 1
# #         linea_fin = datos[pos_fin].decode("utf-8", "ignore")
# #     print (type(linea_ini), type(formato.del_id.del_caracter))
# #     valores_ini = linea_ini.split(formato.del_id.del_caracter)
# #     valores_ini = list(filter(None, valores_ini))
# #     print (type(valores_ini))
# #     valores_fin = linea_fin.split(formato.del_id.del_caracter)
# #     valores_fin = list(filter(None, valores_fin))
# #     form.instance.imp_fecha_ini = formato_fecha(formato, valores_ini, cambiar_fecha)
# #     form.instance.imp_fecha_fin = formato_fecha(formato, valores_fin, cambiar_fecha)
# #     return form
#
#
# def valid_number(val_str):
#     val_num = None
#     try:
#         if isinstance(val_str, Number):
#             val_num = float(val_str)
#         elif val_str == "":
#             val_num = None
#         else:
#             val_str.replace(",", ".")
#             val_num = float(val_str)
#     except:
#         val_num = None
#     return val_num
#
#


def get_modelo(var_id):
    variable = Variable.objects.get(var_id=var_id)
    modelo = globals()[variable.var_modelo]
    return modelo
