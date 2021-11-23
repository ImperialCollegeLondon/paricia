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

from anuarios.models import Var3Anuarios as HumedadAire
from django.db import connection
from home.functions import dictfetchall
from math import isnan
from variable.models import Variable


def matrizIV(estacion, variable, periodo, tipo):
    datos = []
    # tabla = "hai.m" + periodo
    if tipo == 'validado':
        tabla = 'validacion_var' + str(variable) + 'validado'
    else:
        tabla = 'medicion_var' + str(variable)+ 'medicion'
    cursor = connection.cursor()
    variable_obj = Variable.objects.get(pk=variable)
    vacios = variable_obj.vacios
    # promedio mensual
    sql = "SELECT avg(valor) as media, date_part('month',fecha) as mes "
    #sql += "FROM " + tabla + " "
    sql += "FROM mensual_var" + str(variable) + "mensual "
    sql += "WHERE estacion_id=" + str(estacion.est_id) + " and valor!='NaN'::numeric "
    sql += "and date_part('year',fecha)=" + str(periodo) + " "
    sql += "and vacios < %s"
    sql += "GROUP BY mes ORDER BY mes"
    cursor.execute(sql, [vacios, ])
    med_avg = dictfetchall(cursor)
    # datos diarios máximos
    #sql = "SELECT max(maximo) as maximo,  max(valor) as valor, "
    sql = "SELECT max(max_abs) as maximo,  max(valor) as valor, "
    sql += "date_part('month',fecha) as mes, "
    sql += "date_part('day',fecha) as dia "
    #sql += "FROM " + tabla + " "
    sql += "FROM diario_var" + str(variable) + "diario "
    sql += "WHERE estacion_id=" + str(estacion.est_id) + " and valor!='NaN'::numeric "
    sql += "and date_part('year',fecha)=" + str(periodo) + " "
    sql += "and vacios < %s"
    sql += "GROUP BY mes,dia ORDER BY mes,dia"
    cursor.execute(sql, [vacios,])
    datos_diarios_max = dictfetchall(cursor)
    # mínimos absolutos
    sql = "SELECT min(min_abs) as minimo,  min(valor) as valor, "
    #sql = "SELECT min(minimo) as minimo,  min(valor) as valor, "
    sql += "date_part('month',fecha) as mes, "
    sql += "date_part('day',fecha) as dia "
    #sql += "FROM " + tabla + " "
    sql += "FROM diario_var" + str(variable) + "diario "
    sql += "WHERE estacion_id=" + str(estacion.est_id) + " and valor!='NaN'::numeric "
    sql += "and date_part('year',fecha)=" + str(periodo)+" "
    sql += "and valor > 0 "
    sql += "and vacios < %s"
    sql += "GROUP BY mes,dia ORDER BY mes,dia"
    cursor.execute(sql, [vacios,])
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
        if item.get('media') > 100:
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
            # print(fila)
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
    try:

        if isnan(fila.get('maximo')):
            if isnan(fila.get('valor')):
                return 0
            else:
                return round(fila.get('valor'), 2)
        return round(fila.get('maximo'), 2)
    except TypeError:
        if fila.get('maximo') is None:
            if fila.get('valor') is None:
                return 0
            else:
                return round(fila.get('valor'), 2)
        return round(fila.get('maximo'), 2)


def get_minimo(fila):
    try:
        if isnan(fila.get('minimo')):
            if isnan(fila.get('valor')):
                return 0
            else:
                return round(fila.get('valor'), 2)
        return round(fila.get('minimo'), 2)
    except TypeError:
        if fila.get('minimo') is None:
            if fila.get('valor') is None:
                return 0
            else:
                return round(fila.get('valor'), 2)
        return round(fila.get('minimo'), 2)
