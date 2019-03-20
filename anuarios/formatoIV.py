# -*- coding: utf-8 -*-
from medicion.models import Medicion

from anuarios.models import HumedadAire
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count
from django.db.models.functions import (
    ExtractYear, ExtractMonth, ExtractDay, ExtractHour)
from django.db import connection
from home.functions import dictfetchall


def matrizIV(estacion, variable, periodo):
    datos = []
    tabla = "hai.m" + periodo
    tabla = 'medicion_' + str(variable.var_modelo)
    cursor = connection.cursor()
    # promedio mensual
    sql = "SELECT avg(med_valor) as media, date_part('month',med_fecha) as mes "
    sql += "FROM " + tabla + " "
    sql += "WHERE est_id_id=" + str(estacion.est_id) + " and med_valor!='NaN'::numeric "
    sql += "GROUP BY mes ORDER BY mes"
    print(sql)
    cursor.execute(sql)
    med_avg = dictfetchall(cursor)
    # datos diarios máximos
    sql = "SELECT max(med_maximo) as maximo,  max(med_valor) as valor, "
    sql += "date_part('month',med_fecha) as mes, "
    sql += "date_part('day',med_fecha) as dia "
    sql += "FROM " + tabla + " "
    sql += "WHERE est_id_id=" + str(estacion.est_id) + " and med_valor!='NaN'::numeric "
    sql += "GROUP BY mes,dia ORDER BY mes,dia"
    print(sql)
    cursor.execute(sql)
    datos_diarios_max = dictfetchall(cursor)
    # mínimos absolutos
    sql = "SELECT min(med_minimo) as minimo,  min(med_valor) as valor, "
    sql += "date_part('month',med_fecha) as mes, "
    sql += "date_part('day',med_fecha) as dia "
    sql += "FROM " + tabla + " "
    sql += "WHERE est_id_id=" + str(estacion.est_id) + " and med_valor!='NaN'::numeric "
    sql += "GROUP BY mes,dia ORDER BY mes,dia"
    print(sql)
    cursor.execute(sql)
    datos_diarios_min = dictfetchall(cursor)

    maximo, maximo_dia = maximoshai(datos_diarios_max)
    minimo, minimo_dia = minimoshai(datos_diarios_min)
    for item in med_avg:
        mes = int(item.get('mes'))
        obj_hai = HumedadAire()
        obj_hai.est_id = estacion
        obj_hai.hai_periodo = periodo
        obj_hai.hai_mes = mes
        if maximo[mes-1] > 100:
            maximo[mes-1] = 100
        obj_hai.hai_maximo = maximo[mes - 1]
        obj_hai.hai_maximo_dia = maximo_dia[mes - 1]
        obj_hai.hai_minimo = minimo[mes - 1]
        obj_hai.hai_minimo_dia = minimo_dia[mes - 1]
        if item.get('media')>100:
            obj_hai.hai_promedio = 100
        else:
            obj_hai.hai_promedio = item.get('media')
        datos.append(obj_hai)
    cursor.close()
    return datos


def maximoshai(datos_diarios_max):
    # retorna maxima humedad mensual y en que dia sucedio
    max_abs = []
    maxdia = []
    for i in range(1, 13):
        val_max_abs = []
        val_maxdia = []
        for fila in datos_diarios_max:
            mes = int(fila.get('mes'))
            dia = int(fila.get('dia'))
            if mes == i:
                val_max_abs.append(get_maximo(fila))
                val_maxdia.append(dia)
        print(val_max_abs)
        if len(val_max_abs) > 0:
            max_abs.append(max(val_max_abs))
            maxdia.append(val_maxdia[val_max_abs.index(max(val_max_abs))])
        else:
            max_abs.append(0)
            maxdia.append(0)
    return max_abs, maxdia


def minimoshai(datos_diarios_min):
    # retorna minima humedad mensual y en que dia sucedio
    min_abs = []
    mindia = []
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
        else:
            min_abs.append(0)
            mindia.append(0)
    return min_abs, mindia


def get_maximo(fila):
    if fila.get('maximo') is None:
        if fila.get('valor') is None:
            return 0
        return fila.get('valor')
    return fila.get('maximo')


def get_minimo(fila):
    if fila.get('minimo') is None:
        if fila.get('valor') is None:
            return 100
        return fila.get('valor')
    return fila.get('minimo')