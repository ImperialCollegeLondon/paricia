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

import datetime

import plotly.graph_objs as go
import plotly.offline as opy
from django.db import connection, models

## Various functions to report and select periods of validated data.
## Nothing about validating data here, all handled by calling processes in scripts/plpgsql.


class consulta_validados(models.Model):
    fecha_inicio = models.DateTimeField(primary_key=True)
    fecha_fin = models.DateTimeField()
    validado = models.BooleanField()

    class Meta:
        ### Para que no se cree en la migracion
        managed = False


def periodos_validacion(est_id, var_id):
    sql = """
    WITH 
    fechas AS (
    SELECT m.fecha, 
        EXISTS (SELECT v.fecha FROM validacion_var%%var_id%%validado v WHERE v.estacion_id = %%est_id%% AND v.fecha = m.fecha) AS validado
        FROM medicion_var%%var_id%%medicion m WHERE m.estacion_id = %%est_id%%
    ),
    fechas_cambio AS (
        SELECT fecha, validado, CASE WHEN validado != lag(validado) OVER (ORDER BY fecha ASC) THEN lag(fecha) OVER (ORDER BY fecha ASC) END AS fecha_bloque_anterior FROM fechas
    ),
    fechas_union AS (
        (SELECT fi.fecha, fi.validado, NULL AS fecha_bloque_anterior FROM fechas fi ORDER BY fi.fecha ASC LIMIT 1)
        UNION
        (SELECT * FROM fechas_cambio WHERE fecha_bloque_anterior IS NOT NULL)
        UNION
        (SELECT '9999-12-31' AS fecha, ff.validado, ff.fecha AS fecha_bloque_anterior FROM fechas ff ORDER BY ff.fecha DESC LIMIT 1)
    ),
    reporte AS (
        SELECT fecha AS fecha_inicio, lead(fecha_bloque_anterior) OVER (ORDER BY fecha ASC) AS fecha_fin, validado AS validado FROM fechas_union
    )
    SELECT * FROM reporte WHERE fecha_fin IS NOT NULL;
    """
    sql = sql.replace("%%var_id%%", str(var_id)).replace("%%est_id%%", str(est_id))
    result = consulta_validados.objects.raw(sql)
    return result


def periodos_validacion_profundidad(est_id, var_id, profundidad):
    sql = """
    WITH 
    fechas AS (
        SELECT m.fecha, 
            EXISTS (
                SELECT v.fecha FROM validacion_var%%var_id%%validado v 
                WHERE v.estacion_id = m.estacion_id AND v.fecha = m.fecha AND v.profundidad = m.profundidad
                ) AS validado
        FROM medicion_var%%var_id%%medicion m WHERE m.estacion_id = %%est_id%%  AND m.profundidad = %%profundidad%%
    ),
    fechas_cambio AS (
        SELECT 
            fecha, 
            validado, 
            CASE WHEN validado != lag(validado) OVER (ORDER BY fecha ASC) 
                THEN lag(fecha) OVER (ORDER BY fecha ASC) END AS fecha_bloque_anterior 
        FROM fechas
    ),
    fechas_union AS (
        (SELECT fi.fecha, fi.validado, NULL AS fecha_bloque_anterior FROM fechas fi ORDER BY fi.fecha ASC LIMIT 1)
        UNION
        (SELECT * FROM fechas_cambio WHERE fecha_bloque_anterior IS NOT NULL)
        UNION
        (SELECT '9999-12-31' AS fecha, ff.validado, ff.fecha AS fecha_bloque_anterior FROM fechas ff ORDER BY ff.fecha DESC LIMIT 1)
    ),
    reporte AS (
        SELECT 
            fecha AS fecha_inicio, 
            lead(fecha_bloque_anterior) OVER (ORDER BY fecha ASC) AS fecha_fin, 
            validado AS validado 
        FROM fechas_union
    )
    SELECT * FROM reporte WHERE fecha_fin IS NOT NULL;
    """
    sql = (
        sql.replace("%%var_id%%", str(var_id))
        .replace("%%est_id%%", str(est_id))
        .replace("%%profundidad%%", str(profundidad))
    )
    result = consulta_validados.objects.raw(sql)
    return result


# ########################################################################################################
# Generado a partir de modulo Calidad de agua


class ReporteValidacion(models.Model):
    numero_fila = models.BigAutoField(primary_key=True)
    seleccionado = models.BigIntegerField()
    fecha = models.DateTimeField()
    valor_seleccionado = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    valor = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    variacion_consecutiva = models.DecimalField(
        max_digits=14, decimal_places=6, null=True
    )
    comentario = models.CharField(max_length=350)
    class_fila = models.CharField(max_length=30)
    class_fecha = models.CharField(max_length=30)
    class_validacion = models.CharField(max_length=30)
    class_valor = models.CharField(max_length=30)
    class_variacion_consecutiva = models.CharField(max_length=30)
    class_stddev_error = models.CharField(max_length=30)
    feha_error = models.CharField(max_length=30)

    class Meta:
        ### Para que no se cree en la migracion
        managed = False


def xstr(s):
    return "" if s is None else str(s)


def reporte_validacion(form):
    est_id = form.cleaned_data["estacion"].est_id
    var_id = form.cleaned_data["variable"].var_id
    inicio = datetime.datetime.combine(
        form.cleaned_data["inicio"], datetime.time(0, 0, 0, 0)
    )
    fin = datetime.datetime.combine(
        form.cleaned_data["fin"], datetime.time(23, 59, 59, 999999)
    )
    query = "select * FROM reporte_validacion_var" + str(var_id) + "(%s, %s, %s);"
    consulta = ReporteValidacion.objects.raw(query, [est_id, inicio, fin])
    html = ""
    for row in consulta:
        html += (
            '<tr id="'
            + str(row.numero_fila)
            + '" class="'
            + str(row.class_fila)
            + '" >'
        )
        html += (
            '    <td class="col1 '
            + str(row.class_fecha)
            + '">'
            + str(row.fecha)
            + "</td>"
        )
        html += (
            '    <td class="col2 '
            + str(row.class_validacion)
            + '">'
            + xstr(row.valor_seleccionado)
            + "</td>"
        )
        html += (
            '    <td class="col3 '
            + str(row.class_valor)
            + '">'
            + xstr(row.valor)
            + "</td>"
        )
        html += (
            '    <td class="col4 '
            + str(row.class_variacion_consecutiva)
            + '">'
            + xstr(row.variacion_consecutiva)
            + "</td>"
        )
        html += '    <td class="col5 ' + str(row.class_stddev_error) + '"></td>'
        html += '    <td class="col6 comentario" >' + xstr(row.comentario) + "</td>"
        html += "</tr>"
    return html


def reporte_validacion_profundidad(variable_id, estacion_id, profundidad, inicio, fin):
    fin = datetime.datetime.combine(fin, datetime.time(23, 59, 59, 999999))
    query = (
        "select * FROM reporte_validacion_profundidad_var"
        + str(variable_id)
        + "(%s, %s, %s, %s);"
    )
    consulta = ReporteValidacion.objects.raw(
        query, [estacion_id, profundidad, inicio, fin]
    )
    return consulta


def grafico(consulta, variable, estacion):
    valor = []
    fecha = []
    if len(consulta) < 1:
        return '<div><h1 style="background-color : red">No hay datos</h1></div>'
    else:
        for fila in consulta:
            if not fila.seleccionado:
                continue
            if fila.class_fecha == "fecha salto":
                valor.append(None)
                fecha.append(fila.fecha - datetime.timedelta(minutes=1))
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


def grafico2(consulta, variable, estacion):
    valor = []
    fecha = []
    if len(consulta) < 1:
        return '<div><h1 style="background-color : red">No hay datos</h1></div>'
    else:
        for fila in consulta:
            if not fila.seleccionado:
                continue
            if fila.class_fecha == "fecha salto":
                valor.append(None)
                fecha.append(fila.fecha - datetime.timedelta(minutes=1))
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


def borrar_crudos(estacion_id, var_id, inicio, fin):
    filas_crudo = 0
    sql = "DELETE FROM medicion_var1medicion WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s;"
    sql = sql.replace("var1", "var" + str(var_id))
    with connection.cursor() as cursor:
        cursor.execute(sql, [estacion_id, inicio, fin])
        filas_crudo = cursor.rowcount
    return filas_crudo


def borrar_validados(estacion_id, var_id, inicio, fin):
    filas_validado = 0
    sql = "DELETE FROM validacion_var1validado WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s;"
    sql = sql.replace("var1", "var" + str(var_id))
    with connection.cursor() as cursor:
        cursor.execute(sql, [estacion_id, inicio, fin])
        filas_validado = cursor.rowcount

    filas_horario = 0
    sql = "DELETE FROM horario_var1horario WHERE estacion_id = %s AND fecha >= date_trunc('hour', %s) AND fecha <= date_trunc('hour', %s);"
    sql = sql.replace("var1", "var" + str(var_id))
    with connection.cursor() as cursor:
        cursor.execute(sql, [estacion_id, inicio, fin])
        filas_horario = cursor.rowcount

    filas_diario = 0
    sql = "DELETE FROM diario_var1diario WHERE estacion_id = %s AND fecha >= date_trunc('day', %s) AND fecha <= date_trunc('day', %s);"
    sql = sql.replace("var1", "var" + str(var_id))
    with connection.cursor() as cursor:
        cursor.execute(sql, [estacion_id, inicio, fin])
        filas_diario = cursor.rowcount

    filas_mensual = 0
    sql = "DELETE FROM mensual_var1mensual WHERE estacion_id = %s AND fecha >= date_trunc('month', %s) AND fecha <= date_trunc('month', %s);"
    sql = sql.replace("var1", "var" + str(var_id))
    with connection.cursor() as cursor:
        cursor.execute(sql, [estacion_id, inicio, fin])
        filas_mensual = cursor.rowcount

    return filas_validado, filas_horario, filas_diario, filas_mensual


def borrar_crudos_profundidad(estacion_id, profundidad, var_id, inicio, fin):
    filas_crudo = 0
    sql = "DELETE FROM medicion_var1medicion WHERE estacion_id = %s AND profundidad = %s AND fecha >= %s AND fecha <= %s;"
    sql = sql.replace("var1", "var" + str(var_id))
    with connection.cursor() as cursor:
        cursor.execute(sql, [estacion_id, profundidad, inicio, fin])
        filas_crudo = cursor.rowcount
    return filas_crudo


def borrar_validados_profundidad(estacion_id, profundidad, var_id, inicio, fin):
    filas_validado = 0
    sql = "DELETE FROM validacion_var1validado WHERE estacion_id = %s AND profundidad = %s AND fecha >= %s AND fecha <= %s;"
    sql = sql.replace("var1", "var" + str(var_id))
    with connection.cursor() as cursor:
        cursor.execute(sql, [estacion_id, profundidad, inicio, fin])
        filas_validado = cursor.rowcount

    filas_horario = 0
    sql = "DELETE FROM horario_var1horario WHERE estacion_id = %s AND profundidad = %s AND fecha >= date_trunc('hour', %s) AND fecha <= date_trunc('hour', %s);"
    sql = sql.replace("var1", "var" + str(var_id))
    with connection.cursor() as cursor:
        cursor.execute(sql, [estacion_id, profundidad, inicio, fin])
        filas_horario = cursor.rowcount

    filas_diario = 0
    sql = "DELETE FROM diario_var1diario WHERE estacion_id = %s AND profundidad = %s AND fecha >= date_trunc('day', %s) AND fecha <= date_trunc('day', %s);"
    sql = sql.replace("var1", "var" + str(var_id))
    with connection.cursor() as cursor:
        cursor.execute(sql, [estacion_id, profundidad, inicio, fin])
        filas_diario = cursor.rowcount

    filas_mensual = 0
    sql = "DELETE FROM mensual_var1mensual WHERE estacion_id = %s AND profundidad = %s AND fecha >= date_trunc('month', %s) AND fecha <= date_trunc('month', %s);"
    sql = sql.replace("var1", "var" + str(var_id))
    with connection.cursor() as cursor:
        cursor.execute(sql, [estacion_id, profundidad, inicio, fin])
        filas_mensual = cursor.rowcount

    return filas_validado, filas_horario, filas_diario, filas_mensual


def profundidades(estacion_id, variable_id):
    if variable_id is None:
        variable_id = 101

    sql = (
        "SELECT DISTINCT(profundidad) FROM medicion_var"
        + str(variable_id)
        + "medicion "
    )

    if estacion_id is not None:
        sql = sql + " WHERE estacion_id = " + str(estacion_id)

    sql = sql + " ORDER BY profundidad;"
    lista = {}
    with connection.cursor() as cursor:
        cursor.execute(sql, [])
        for row in cursor:
            val = row[0]
            lista[val] = "%.2f" % (val / 100.0) + " m"

    return lista
