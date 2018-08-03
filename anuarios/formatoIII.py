# -*- coding: utf-8 -*-

from anuarios.models import TemperaturaAire
from django.db import connection
from home.functions import dictfetchall


def matrizIII(estacion, variable, periodo):
    datos = []
    tabla = "tai.m" + periodo
    cursor = connection.cursor()
    # promedio mensual
    sql = "SELECT avg(med_valor) as media, date_part('month',med_fecha) as mes "
    sql += "FROM " + tabla + " "
    sql += "WHERE est_id_id=" + str(estacion.est_id) + " "
    sql += "GROUP BY mes ORDER BY mes"
    cursor.execute(sql)
    med_avg = dictfetchall(cursor)
    # datos diarios máximos
    sql = "SELECT max(med_maximo) as maximo,  max(med_valor) as valor, "
    sql += "date_part('month',med_fecha) as mes, "
    sql += "date_part('day',med_fecha) as dia "
    sql += "FROM " + tabla + " "
    sql += "WHERE est_id_id=" + str(estacion.est_id) + " "
    sql += "GROUP BY mes,dia ORDER BY mes,dia"
    cursor.execute(sql)
    datos_diarios_max = dictfetchall(cursor)
    # mínimos absolutos
    sql = "SELECT min(med_maximo) as minimo,  min(med_valor) as valor, "
    sql += "date_part('month',med_fecha) as mes, "
    sql += "date_part('day',med_fecha) as dia "
    sql += "FROM " + tabla + " "
    sql += "WHERE est_id_id=" + str(estacion.est_id) + " "
    sql += "GROUP BY mes,dia ORDER BY mes,dia"
    cursor.execute(sql)
    datos_diarios_min = dictfetchall(cursor)
    max_abs, max_dia, maximo = maximostai(datos_diarios_max)
    min_abs, min_dia, minimo = minimostai(datos_diarios_min)
    for item in med_avg:
        mes = int(item.get('mes'))
        obj_tai = TemperaturaAire()
        obj_tai.est_id = estacion
        obj_tai.tai_periodo = periodo
        obj_tai.tai_maximo_abs = max_abs[mes - 1]
        obj_tai.tai_maximo_dia = max_dia[mes - 1]
        obj_tai.tai_maximo = maximo[mes - 1]
        obj_tai.tai_minimo_abs = min_abs[mes - 1]
        obj_tai.tai_minimo_dia = min_dia[mes - 1]
        obj_tai.tai_minimo = minimo[mes - 1]
        obj_tai.tai_promedio = item.get('media')
        obj_tai.tai_mes = mes
        datos.append(obj_tai)
    cursor.close()
    return datos


def maximostai(datos_diarios_max):
    # retorna maxima temp mensual y en que dia sucedio y media mensual de las maximas
    max_abs = []
    maxdia = []
    avgmax = []
    for i in range(1, 13):
        val_max_abs = []
        val_maxdia = []
        for fila in datos_diarios_max:
            mes = int(fila.get('mes'))
            dia = int(fila.get('dia'))
            if mes == i:
                val_max_abs.append(get_maximo(fila))
                val_maxdia.append(dia)
        if len(val_max_abs) > 0:
            max_abs.append(max(val_max_abs))
            maxdia.append(val_maxdia[val_max_abs.index(max(val_max_abs))])
            avgmax.append(sum(val_max_abs) / len(val_max_abs))
        else:
            max_abs.append(0)
            maxdia.append(0)
            avgmax.append(0)
    return max_abs, maxdia, avgmax


def minimostai(datos_diarios_min):
    # retorna minima temp mensual y en que dia sucedio y media mensual de las minimas
    min_abs = []
    mindia = []
    avgmin = []
    for i in range(1, 13):
        val_min_abs = []
        val_mindia = []
        for fila in datos_diarios_min:
            mes = int(fila.get('mes'))
            dia = int(fila.get('dia'))
            if mes == i:
                val_min_abs.append(get_minimo(fila))
                val_mindia.append(dia)
        if len(val_min_abs) > 0:
            min_abs.append(min(val_min_abs))
            mindia.append(val_mindia[val_min_abs.index(min(val_min_abs))])
            avgmin.append(sum(val_min_abs) / (len(val_min_abs)))
        else:
            min_abs.append(0)
            mindia.append(0)
            avgmin.append(0)
    return min_abs, mindia, avgmin


def get_maximo(fila):
    if fila.get('maximo') is None:
        return fila.get('valor')
    return fila.get('maximo')


def get_minimo(fila):
    if fila.get('minimo') is None:
        return fila.get('valor')
    return fila.get('minimo')