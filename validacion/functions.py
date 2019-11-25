# -*- coding: utf-8 -*-
from validacion.models import *
from frecuencia.models import Frecuencia
from medicion.models import Medicion
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




def generar_validacion(form):
    validaciones = []
    estacion = form.cleaned_data['est_id']
    variable = form.cleaned_data['var_id']
    obj_estacion = Estacion.objects.get(est_id=estacion)
    obj_variable = Variable.objects.get(var_id=variable)
    consulta = Validacion.objects.filter(est_id=estacion) \
                   .filter(var_id=variable).order_by('-val_fecha')[:1]
    if consulta.exists():
        fecha_ini = consulta[0].val_fecha
    else:
        frecuencia = Frecuencia.objects.filter(est_id=estacion) \
                         .filter(var_id=variable).order_by('fre_fecha_ini')[:1]
        # print frecuencia[0].fre_fecha_ini
        fecha_ini = frecuencia[0].fre_fecha_ini
    # fecha_ini=date(2017,1,1)
    mediciones = Medicion.objects.filter(est_id=estacion) \
                     .filter(var_id=variable).values('med_fecha').reverse()[:1]
    fecha_fin = mediciones[0].get('med_fecha')
    fechas = list(Frecuencia.objects.filter(est_id=estacion) \
                  .filter(var_id=variable).order_by('fre_fecha_ini'))
    i = 0
    # frecuencia por defecto
    val_frecuencia = 5
    rango = (fecha_fin - fecha_ini).days
    for item in range(30):
        val_fecha = fecha_ini + timedelta(days=item)
        if len(fechas) > 1:
            if val_fecha >= fechas[i].get('fre_fecha_fin') and i < fechas.count():
                i += 1
            val_frecuencia = fechas[i].fre_valor
        else:
            val_frecuencia = fechas[i].fre_valor
        val_num_dat = Medicion.objects.filter(est_id=estacion) \
            .filter(var_id=variable).filter(med_fecha=val_fecha).count()
        val_fre_reg = (60 / val_frecuencia) * 24
        val_porcentaje = float(val_num_dat) / val_fre_reg * 100

        obj_validacion = Validacion(var_id=obj_variable, est_id=obj_estacion,
                                    val_fecha=val_fecha, val_num_dat=val_num_dat, val_fre_reg=val_fre_reg,
                                    val_porcentaje=val_porcentaje)
        validaciones.append(obj_validacion)
        # obj_validacion.save()

    return validaciones

def guardar_validacion(datos):
    for item in datos:
        item.save()

