# -*- coding: utf-8 -*-
from validacion.models import Validacion
from frecuencia.models import Frecuencia

from estacion.models import Estacion
from variable.models import Variable
from datetime import datetime, timedelta, date
from django.db import models


class consulta(models.Model):
    fecha_inicio = models.DateTimeField(primary_key=True)
    fecha_fin = models.DateTimeField()
    validado = models.BooleanField()


def periodos_validacion(est_id, var_id):
    sql = """
    WITH 
    fechas AS (
    SELECT m.fecha, 
        EXISTS (SELECT v.fecha FROM validacion_%%var_id%% v WHERE v.estacion_id = %%est_id%% AND v.fecha = m.fecha) AS validado
        FROM medicion_%%var_id%% m WHERE m.estacion = %%est_id%%
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
    result = consulta.objects.raw(sql)
    return result


def guardar_validacion(datos):
    for item in datos:
        item.save()
