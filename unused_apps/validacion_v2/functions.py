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

import json
from ctypes import c_int
from datetime import datetime, time, timedelta
from decimal import Decimal

import plotly.graph_objs as go
import plotly.offline as opy
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection, models
from django.http import HttpResponse

from home.functions import dictfetchall
from medicion.functions import ValidationReport
from validacion_v2.abstract import (
    ReporteCrudos,
    ReporteDiario,
    ReporteDiarioPrecipitacion,
)
from variable.models import Variable


class ReporteValidaciong(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateTimeField()
    # valor_seleccionado = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    valor = models.DecimalField(max_digits=14, decimal_places=6)
    # nuevo valor
    n_valor = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    validado = models.BooleanField()
    # variacion_consecutiva = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    seleccionado = models.BooleanField()
    estado = models.BooleanField()
    feha_error = models.CharField(max_length=30)
    valor_error = models.BooleanField()
    stddev_error = models.BooleanField()
    comentario = models.CharField(max_length=350)
    # class_fila = models.CharField(max_length=30)
    # class_fecha = models.CharField(max_length=30)
    # class_validacion = models.CharField(max_length=30)
    # class_valor = models.CharField(max_length=30)
    # class_variacion_consecutiva = models.CharField(max_length=30)
    # class_stddev_error = models.CharField(max_length=30)
    nivel = models.DecimalField(max_digits=14, decimal_places=6)
    caudal = models.DecimalField(max_digits=14, decimal_places=6)
    nivel_error = models.BooleanField()
    caudal_error = models.BooleanField()

    class Meta:
        ### Para que no se cree en la migracion
        managed = False


class Consulta(models.Model):
    fecha_inicio = models.DateTimeField(primary_key=True)
    fecha_fin = models.DateTimeField()
    validado = models.BooleanField()


# consultar datos diarios en un rango de fechas
# def reporte_diario(estacion, variable, inicio, final, var_maximo, var_minimo):
def reporte_diario(estacion, variable, inicio, final, var_maximo, var_minimo, data):
    """query daily data in a date range."""
    est_id = estacion.est_id
    modelo = normalize(variable.var_nombre).replace(" de ", "")
    modelo = modelo.replace(" ", "")
    var_id = variable.var_id
    fin = datetime.combine(final, time(23, 59, 59, 999999))
    if var_id == 1:
        query = (
            "select * FROM reporte_validacion_diario_precipitacion(%s, %s, %s, %s, %s);"
        )
        consulta = ReporteDiarioPrecipitacion.objects.raw(
            query, [est_id, inicio, fin, var_maximo, var_minimo]
        )
        print("En la consulta ", query)
    elif var_id == 4 or var_id == 5:
        query = "select * FROM reporte_validacion_diario_viento(%s, %s, %s, %s, %s);"
        consulta = ReporteDiarioPrecipitacion.objects.raw(
            query, [est_id, inicio, fin, var_maximo, var_minimo]
        )
    # elif var_id == 10 or var_id == 11:
    #    query = "select * FROM reporte_validacion_diario_agua(%s, %s, %s, %s, %s);"
    #    consulta = ReporteDiario.objects.raw(query, [est_id, inicio, fin, var_maximo, var_minimo])
    else:
        query = (
            "select * FROM reporte_validacion_diario_"
            + str(modelo).lower()
            + "(%s, %s, %s, %s, %s);"
        )
        # query = "select * FROM reporte_validacion_diario_var" + str(var_id) + "(%s, %s, %s, %s, %s);"
        consulta = ReporteDiario.objects.raw(
            query, [est_id, inicio, fin, var_maximo, var_minimo]
        )
    # print(query)
    # print(consulta)
    num_fecha = 0
    num_porcentaje = 0
    num_valor = 0
    num_maximo = 0
    num_minimo = 0
    conteo_variacion = 90
    mensaje = ""
    if var_id == 11:
        sql_curva = "select * from medicion_curvadescarga m where m.estacion_id = %%est_id%% and '%%fecha_ini%%' >= (select min(fecha) from medicion_curvadescarga mc where mc.estacion_id =  %%est_id%%);"
        sql_curva = (
            sql_curva.replace("%%est_id%%", str(est_id))
            .replace("%%fecha_ini%%", str(inicio))
            .replace("%%fecha_fin%%", str(fin))
        )
        cursor = connection.cursor()
        cursor.execute(sql_curva)
        d = dictfetchall(cursor)
        if len(d) == 0:
            mensaje = "<div class='alert alert-danger alert-dismissible' role='alert'> No existe la curva de descarga</div>"
        else:
            mensaje = "<div class='alert alert-success alert-dismissible' role='alert'> Existe la curva de descarga</div>"

    for fila in consulta:
        # print("valor de fila", fila.fecha)
        delattr(fila, "_state")
        fila.fecha = fila.fecha.strftime("%Y-%m-%d")
        # Aki el nuevo Valor
        if var_id == 4 or var_id == 5:
            fila.n_valor = 0
        else:
            fila.n_valor = fila.c_varia_err
        # print(fila.n_valor)
        if fila.porcentaje is None:
            return {
                "error": "La estación no tiene la frecuencia de registro asociada a esta variable. "
                "Por favor asigne esta información en la sección Administración/Frecuencia de Registro "
            }

        if fila.fecha_error == 2:
            num_fecha += 1
        if fila.fecha_error == 3:
            num_fecha += 1
        if fila.fecha_error == 0:
            num_fecha += 1
        # if fila.porcentaje < variable.umbral_completo:
        #     num_porcentaje += 1
        if fila.porcentaje < Decimal(100.0) - variable.vacios:
            num_porcentaje += 1
        # if var_id == 10 or var_id == 11:
        #    if fila.nivel_numero > 0:
        #        num_valor += 1
        else:
            if fila.valor_numero > 0:
                num_valor += 1

        # if var_id == 10 or var_id == 11:
        #    pass
        # elif var_id != 1:
        if var_id != 1:
            if fila.maximo_numero > 0:
                num_maximo += 1
            if fila.minimo_numero > 0:
                num_minimo += 1

        # lista_nueva = [dict(fila.__dict__) for fila in lista if fila['state']]

    result = {
        "estacion": [
            {
                "est_id": estacion.est_id,
                "est_nombre": estacion.est_nombre,
            }
        ],
        "variable": [
            {
                "var_id": variable.var_id,
                "var_nombre": variable.var_nombre,
                "var_maximo": variable.var_maximo,
                "var_minimo": variable.var_minimo,
            }
        ],
        "datos": [dict(fila.__dict__) for fila in consulta],
        "indicadores": [
            {
                "num_fecha": num_fecha,
                "num_porcentaje": num_porcentaje,
                "num_valor": num_valor,
                "num_maximo": num_maximo,
                "num_minimo": num_minimo,
                "num_dias": (final - inicio).days + 1,
            }
        ],
        "data": data,
        "curva": mensaje,
    }
    return data


# Consultar datos crudos y/o validados por estacion, variable y fecha de un día en específico


def consultar_diario(est_id, var_id, fecha_str, var_maximo, var_minimo):
    """Query raw and/or validated data by station, variable and date of a specific day."""
    inicio = datetime.strptime(fecha_str, "%Y-%m-%d")

    fin = datetime.combine(inicio.date(), time(23, 59, 59, 999999))
    variable = Variable.objects.get(var_id=var_id)
    # if variable.var_id == 1:
    #    query = "select * FROM reporte_validacion_precipitacion(%s, %s, %s, %s, %s);"
    # consulta = ReporteDiarioPrecipitacion.objects.raw(query, [est_id, inicio, fin, var_maximo, var_minimo])
    if variable.var_id == 4 or variable.var_id == 5:
        query = "select * FROM reporte_validacion_viento(%s, %s, %s, %s, %s);"
    # elif variable.var_id == 10 or variable.var_id == 11:
    #    query = "select * FROM reporte_validacion_agua(%s, %s, %s, %s, %s);"
    else:
        modelo = normalize(variable.var_nombre).replace(" de ", "")
        modelo = modelo.replace(" ", "")
        query = (
            "select * FROM reporte_validacion_"
            + str(modelo).lower()
            + "(%s, %s, %s, %s, %s);"
        )
        # query = "select * FROM reporte_validacion_var" + str(variable.var_id) + "(%s, %s, %s, %s, %s);"
    consulta = ReporteDiario.objects.raw(
        query, [est_id, inicio, fin, float(var_maximo), float(var_minimo)]
    )
    num_fecha = 0
    num_valor = 0
    num_maximo = 0
    num_minimo = 0
    num_stddev = 0
    print(consulta)
    for fila in consulta:
        delattr(fila, "_state")
        fila.n_valor = fila.variacion_consecutiva
        if fila.fecha_error == 2:
            num_fecha += 1
        if fila.fecha_error == 3:
            num_fecha += 1
        # if var_id == 10 or var_id == 11:
        #    if fila.nivel_error:
        #        num_valor += 1
        else:
            if fila.valor_error:
                num_valor += 1
        if var_id != 1:
            # if var_id == 10 or var_id == 11:
            #    pass
            # else:
            if fila.maximo_error:
                num_maximo += 1
            if fila.minimo_error:
                num_minimo += 1
        if fila.stddev_error:
            num_stddev += 1

    datos = [dict(fila.__dict__) for fila in consulta]
    num_datos = numero_datos_esperados(est_id, var_id, fecha_str)

    data = {
        "datos": datos,
        "indicadores": [
            {
                "num_fecha": num_fecha,
                "num_valor": num_valor,
                "num_valor1": num_valor,
                "num_maximo": num_maximo,
                "num_minimo": num_minimo,
                "num_stddev": num_stddev,
                "num_datos": num_datos,
            }
        ],
    }

    return data


# Obtener el número de datos esperados en un día
def numero_datos_esperados(est_id, var_id, fecha_str):
    """Get the expected number of data points in a day."""

    sql = """SELECT CAST(1440/f.fre_valor AS INT) ndatos FROM frecuencia_frecuencia f WHERE f.fre_valor <= 60
        and f.est_id_id = %%est_id%% AND f.var_id_id = %%var_id%%
        AND f.fre_fecha_ini <= '%%fecha%%'
        ORDER BY f.fre_fecha_ini DESC LIMIT 1
    """
    sql = (
        sql.replace("%%var_id%%", str(var_id))
        .replace("%%est_id%%", str(est_id))
        .replace("%%fecha%%", fecha_str)
    )

    cursor = connection.cursor()
    cursor.execute(sql)
    print(sql)
    datos = dictfetchall(cursor)
    cursor.close()

    print(datos[0].get("ndatos"))
    ndatos = datos[0].get("ndatos")

    return ndatos


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


# generar las condiciones para eliminar y/o anular los datos validados
def get_condiciones(cambios_lista):
    """generate the conditions to eliminate and/or annul the validated data."""

    fechas_condicion = []
    fechas_eliminar = []
    for fila in cambios_lista:
        if fila["validado"]:
            fechas_condicion.append("'" + fila["fecha"] + "'")
        if not fila["estado"]:
            fechas_eliminar.append("'" + fila["fecha"] + "'")

    fechas_condicion = set(fechas_condicion)
    fechas_eliminar = set(fechas_eliminar)

    where_fechas = ",".join(fechas_condicion)
    where_eliminar = ",".join(fechas_eliminar)

    condiciones = {"where_eliminar": where_eliminar, "where_fechas": where_fechas}
    return condiciones


# Pasar los datos crudos a validados
def pasar_crudos_validados(
    cambios_lista, variable, estacion_id, condiciones, limite_superior, limite_inferior
):
    """Convert raw data to validated data."""
    modelo = normalize(variable.var_nombre).replace(" de ", "")
    modelo = modelo.replace(" ", "")
    variable_nombre = modelo
    fecha_inicio_dato = cambios_lista[0]["fecha"]
    fecha_fin_dato = cambios_lista[-1]["fecha"]
    # where_fechas = condiciones.get('where_fechas')
    where_eliminar = condiciones.get("where_eliminar")

    if variable.var_id == 1:
        query = "select * FROM reporte_crudos_precipitacion(%s, %s, %s, %s, %s);"

    elif variable.var_id == 4 or variable.var_id == 5:
        query = "select * FROM reporte_crudos_viento(%s, %s, %s, %s, %s);"

    # elif variable.var_id == 10 or variable.var_id == 11:
    #    query = "select * FROM reporte_crudos_agua(%s, %s, %s, %s, %s);"
    else:
        query = (
            "select * FROM reporte_crudos_"
            + str(variable_nombre).lower()
            + "(%s, %s, %s, %s, %s);"
        )
        # query = "select * FROM reporte_crudos_var" + str(variable.var_id) + "(%s, %s, %s, %s, %s);"
    consulta = ReporteCrudos.objects.raw(
        query,
        [
            estacion_id,
            fecha_inicio_dato,
            fecha_fin_dato,
            limite_superior,
            limite_inferior,
        ],
    )
    for fila in consulta:
        delattr(fila, "_state")

    datos = [dict(fila.__dict__) for fila in consulta]
    data_json = json.dumps(datos, cls=DjangoJSONEncoder)
    with connection.cursor() as cursor:
        if variable.var_id == 4 or variable.var_id == 5:
            cursor.callproc("insertar_viento_validacion", [estacion_id, data_json])
        # elif variable.var_id == 10 or variable.var_id == 11:
        #    cursor.callproc('insertar_agua_validacion', [estacion_id, data_json])
        else:
            cursor.callproc(
                "insertar_" + str(variable_nombre).lower() + "_validacion",
                [estacion_id, data_json],
            )
            print(data_json)
            print(estacion_id)
        resultado = cursor.fetchone()[0]
        cursor.close()

    if len(where_eliminar) > 0:
        if variable.var_id == 4 or variable.var_id == 5:
            variable_nombre = "viento"
        # elif variable.var_id == 10 or variable.var_id == 11:
        #    variable_nombre = 'agua'

        if variable.var_id == 1:
            sql = """UPDATE validacion_var%%modelo%%validado SET valor = NULL WHERE estacion_id = %%est_id%%   
                    AND date_trunc('day',fecha) IN (%%condicion%%) """
        elif variable.var_id == 4 or variable.var_id == 5:
            sql = """UPDATE validacion_viento SET valor = NULL, maximo = NULL, minimo = NULL,         
                    direccion = null, categoria = null WHERE estacion_id = %%est_id%%   
                    AND date_trunc('day',fecha) IN (%%condicion%%);
                    UPDATE validacion_var4validado SET valor = NULL, maximo = NULL, minimo = NULL        
                    WHERE estacion_id = %%est_id%%   
                    AND date_trunc('day',fecha) IN (%%condicion%%);
                    UPDATE validacion_var5validado SET valor = NULL, maximo = NULL, minimo = NULL
                    WHERE estacion_id = %%est_id%%   
                    AND date_trunc('day',fecha) IN (%%condicion%%);"""
        # elif variable.var_id == 10 or variable.var_id == 11:
        #    sql = """UPDATE validacion_var%%modelo%%validado SET nivel = NULL, caudal = NULL
        #            WHERE estacion_id = %%est_id%% AND date_trunc('day',fecha) IN (%%condicion%%)"""
        else:
            sql = """UPDATE validacion_var%%modelo%%validado SET valor = NULL, maximo = NULL, minimo = NULL 
                    WHERE estacion_id = %%est_id%%   
                    AND date_trunc('day',fecha) IN (%%condicion%%)"""

        sql_modificar = (
            sql.replace("%%modelo%%", str(variable.var_id))
            .replace("%%est_id%%", str(estacion_id))
            .replace("%%condicion%%", where_eliminar)
        )
        print(sql_modificar)
        with connection.cursor() as cursor:
            cursor.execute(sql_modificar)
            cursor.close()

    return resultado


# Eliminar los datos de validados con basse a un rango de fechas
def eliminar_datos_validacion(cambios_lista, variable, estacion_id, condiciones):
    """Remove validated data based on a date range."""

    fecha_inicio_dato = cambios_lista[0]["fecha"]
    fecha_fin_dato = cambios_lista[-1]["fecha"]
    modelo = normalize(variable.var_nombre).replace(" de ", "")
    modelo = modelo.replace(" ", "")
    variable_nombre = modelo
    where_fechas = condiciones.get("where_fechas")

    if variable.var_id == 4 or variable.var_id == 5:
        variable_nombre = "viento"
    # elif variable.var_id == 10 or variable.var_id == 11:
    #    variable_nombre = 'agua'

    if len(where_fechas) > 0:
        sql_delete = """DELETE FROM validacion_var%%modelo%%validado WHERE estacion_id = %%est_id%% and 
            date_trunc('day',fecha)>='%%fecha_ini%%' and date_trunc('day',fecha)<='%%fecha_fin%%'
            and date_trunc('day',fecha) not in (%%condicion%%);"""
        if variable.var_id == 4 or variable.var_id == 5:
            sql_delete = """DELETE FROM validacion_viento WHERE estacion_id = %%est_id%% and 
            date_trunc('day',fecha)>='%%fecha_ini%%' and date_trunc('day',fecha)<='%%fecha_fin%%'
            and date_trunc('day',fecha) not in (%%condicion%%);
            DELETE FROM validacion_var4validado WHERE estacion_id = %%est_id%% and 
            date_trunc('day',fecha)>='%%fecha_ini%%' and date_trunc('day',fecha)<='%%fecha_fin%%'
            and date_trunc('day',fecha) not in (%%condicion%%);
            DELETE FROM validacion_var5validado WHERE estacion_id = %%est_id%% and 
            date_trunc('day',fecha)>='%%fecha_ini%%' and date_trunc('day',fecha)<='%%fecha_fin%%'
            and date_trunc('day',fecha) not in (%%condicion%%);
            """
    else:
        sql_delete = """DELETE FROM validacion_var%%modelo%%validado  WHERE estacion_id = %%est_id%% 
            and date_trunc('day',fecha)>='%%fecha_ini%%' and date_trunc('day',fecha)<='%%fecha_fin%%;'"""
        if variable.var_id == 4 or variable.var_id == 5:
            sql_delete = """DELETE FROM validacion_viento  WHERE estacion_id = %%est_id%% 
            and date_trunc('day',fecha)>='%%fecha_ini%%' and date_trunc('day',fecha)<='%%fecha_fin%%';
            DELETE FROM validacion_var4validado  WHERE estacion_id = %%est_id%% 
            and date_trunc('day',fecha)>='%%fecha_ini%%' and date_trunc('day',fecha)<='%%fecha_fin%%';
            DELETE FROM validacion_var5validado  WHERE estacion_id = %%est_id%% 
            and date_trunc('day',fecha)>='%%fecha_ini%%' and date_trunc('day',fecha)<='%%fecha_fin%%';
            """

    sql_delete = (
        sql_delete.replace("%%modelo%%", str(variable.var_id))
        .replace("%%est_id%%", str(estacion_id))
        .replace("%%fecha_ini%%", fecha_inicio_dato)
        .replace("%%fecha_fin%%", fecha_fin_dato)
        .replace("%%condicion%%", where_fechas)
    )

    with connection.cursor() as cursor:
        print(sql_delete)
        cursor.execute(sql_delete)

        cursor.close()

    resultado = True

    return resultado


def periodos_validacion(est_id, variable, inicio):
    anio = inicio.split("-")[0]
    modelo = str(variable.var_id)
    sql = """
    WITH 
    fechas AS (
    SELECT m.fecha, 
        EXISTS (SELECT v.fecha FROM validacion_var%%var_id%%validado v 
        WHERE v.estacion_id = %%est_id%% AND v.fecha = m.fecha) AS validado
        FROM medicion_var%%var_id%%medicion m WHERE m.estacion_id = %%est_id%% AND date_part('year',fecha) = %%inicio%%
    ),
    fechas_cambio AS (
        SELECT fecha, validado, CASE WHEN validado != lag(validado) OVER (ORDER BY fecha ASC) THEN lag(fecha) 
        OVER (ORDER BY fecha ASC) END AS fecha_bloque_anterior FROM fechas
    ),
    fechas_union AS (
        (SELECT fi.fecha, fi.validado, NULL AS fecha_bloque_anterior FROM fechas fi ORDER BY fi.fecha ASC LIMIT 1)
        UNION
        (SELECT * FROM fechas_cambio WHERE fecha_bloque_anterior IS NOT NULL)
        UNION
        (SELECT '9999-12-31' AS fecha, ff.validado, ff.fecha AS fecha_bloque_anterior 
        FROM fechas ff ORDER BY ff.fecha DESC LIMIT 1)
    ),
    reporte AS (
        SELECT fecha AS fecha_inicio, lead(fecha_bloque_anterior) OVER (ORDER BY fecha ASC) AS fecha_fin, 
        validado AS validado FROM fechas_union
    )
    SELECT * FROM reporte WHERE fecha_fin IS NOT NULL;
    """

    sql = (
        sql.replace("%%var_id%%", str(modelo))
        .replace("%%est_id%%", str(est_id))
        .replace("%%inicio%%", anio)
    )
    print(sql)
    result = Consulta.objects.raw(sql)
    return result


def periodos_validacion2(est_id, variable, inicio):
    anio = inicio.split("-")[0]
    if anio == "None":
        anio = "1000"
    modelo = str(variable.var_id)

    sql = """
    WITH 
    fechas AS (
    SELECT m.fecha, 
        EXISTS (SELECT v.fecha FROM validacion_var%%var_id%%validado v 
        WHERE v.estacion_id = %%est_id%% AND v.fecha = m.fecha) AS validado
        FROM medicion_var%%var_id%%medicion m WHERE m.estacion_id = %%est_id%% AND date_part('year',fecha) >= %%inicio%%
    ),
    fechas_cambio AS (
        SELECT fecha, validado, CASE WHEN validado != lag(validado) OVER (ORDER BY fecha ASC) THEN lag(fecha) 
        OVER (ORDER BY fecha ASC) END AS fecha_bloque_anterior FROM fechas
    ),
    fechas_union AS (
        (SELECT fi.fecha, fi.validado, NULL AS fecha_bloque_anterior FROM fechas fi ORDER BY fi.fecha ASC LIMIT 1)
        UNION
        (SELECT * FROM fechas_cambio WHERE fecha_bloque_anterior IS NOT NULL)
        UNION
        (SELECT '9999-12-31' AS fecha, ff.validado, ff.fecha AS fecha_bloque_anterior 
        FROM fechas ff ORDER BY ff.fecha DESC LIMIT 1)
    ),
    reporte AS (
        SELECT fecha AS fecha_inicio, lead(fecha_bloque_anterior) OVER (ORDER BY fecha ASC) AS fecha_fin, 
        validado AS validado FROM fechas_union
    )
    SELECT * FROM reporte WHERE fecha_fin IS NOT NULL;
    """
    sql = (
        sql.replace("%%var_id%%", str(modelo))
        .replace("%%est_id%%", str(est_id))
        .replace("%%inicio%%", anio)
    )
    # print(sql)
    result = Consulta.objects.raw(sql)
    return result


def reporte_validacion(form, inicio, fin):
    est_id = form.cleaned_data["estacion"].est_id
    var_id = form.cleaned_data["variable"].var_id
    var_nombre = form.cleaned_data["variable"].var_nombre
    modelo = normalize(var_nombre).replace(" de ", "")
    modelo = modelo.replace(" ", "")

    if var_id == 1:
        query = "select * FROM reporte_validacion_precipitacion(%s, %s, %s, %s, %s);"
    elif var_id == 4 or var_id == 5:
        query = "select * FROM reporte_validacion_viento(%s, %s, %s, %s, %s);"
    # elif var_id == 10 or var_id == 11:
    #     query = "select * FROM reporte_validacion_agua(%s, %s, %s,%s, %s);"
    else:
        query = (
            "select * FROM reporte_validacion_"
            + str(modelo).lower()
            + "(%s, %s, %s,%s, %s);"
        )
    consulta = ReporteValidaciong.objects.raw(
        query,
        [
            est_id,
            inicio,
            fin,
            form.cleaned_data["limite_superior"],
            form.cleaned_data["limite_inferior"],
        ],
    )
    return consulta


def grafico(consulta, variable, estacion, inicio, fin):
    valor = []
    fecha = []
    print(consulta)
    if len(consulta) < 1:
        return '<div><h1 style="background-color : red">No hay datos</h1></div>'
    else:
        for fila in consulta:
            if not fila.seleccionado:
                continue
            if fila.fecha_error > 1:
                valor.append(None)
                fecha.append(fila.fecha - timedelta(minutes=1))
            else:
                # if variable.var_id == 10:
                #     valor.append(fila.caudal)
                #     fecha.append(fila.fecha)
                # elif variable.var_id == 11:
                #     valor.append(fila.nivel)
                #     fecha.append(fila.fecha)
                # else:
                valor.append(fila.valor)
                fecha.append(fila.fecha)
        # TODO : esta implementación se la puede mejorar:
        #             1) integrando el valor de frecuencia en el reporte final POSTGRES
        #             2) Pasando el gráfico como tabla javascript/json y usando DataTables.js
        periodo = 1440
        for i in range(0, int(len(fecha) / 4)):
            periodoi = fecha[i + 1] - fecha[i]
            periodoi = round(periodoi.days * 1440 + periodoi.seconds / 60.0)
            periodoN_i = fecha[-(i + 1)] - fecha[-(i + 2)]
            periodoN_i = round(periodoN_i.days * 1440 + periodoN_i.seconds / 60.0)
            if periodoi == periodoN_i:
                periodo = periodoi
                break
            periodo = min(periodo, periodoi, periodoN_i)
        # print(fecha)
        intervalo = fecha[-1] - fecha[0]
        ndatos_esperado = (
            (intervalo.days * 1440 + intervalo.seconds / 60.0) / periodo
        ) + 1
        if variable.es_acumulada:
            trace = go.Bar(
                x=fecha,
                y=valor,
                width=60000 * periodo,
                marker=dict(
                    line=dict(width=0.3, color="rgb(0,0,0)"),
                ),
            )
            data = [trace]
        else:
            trace2 = go.Scatter(
                x=fecha,
                y=valor,
                mode="lines+markers",
                connectgaps=False,
                line=dict(
                    color=("rgb(22, 96, 167)"),
                ),
                marker=dict(
                    size=2,
                    color="rgb(11, 48, 83)",
                ),
            )
            data = [trace2]

        shapes = []
        pixels_por_dato = 1.0
        layout = go.Layout(
            autosize=True,
            width=160 + int(ndatos_esperado * pixels_por_dato),
            height=300,
            title=estacion.est_codigo,
            yaxis=dict(
                title=variable.var_nombre + " [" + variable.uni_id.uni_sigla + "]"
            ),
            shapes=shapes,
            margin=dict(b=20, t=40, pad=4),
        )
        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type="div")
        return div
