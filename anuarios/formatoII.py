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

from anuarios.models import Var1Anuarios as Precipitacion
from django.db import connection
from home.functions import dictfetchall
from math import isnan


def get_precipitacion(estacion, variable, periodo, tipo):

    if tipo == 'validado':
        tabla = 'validacion_var' + str(variable) + 'validado'
    else:
        tabla = 'medicion_var' + str(variable)+ 'medicion'
    cursor = connection.cursor()
    datos = []
    # valores de precipitación mensual
    sql = "SELECT sum(valor) as suma, date_part('month',fecha) as mes "
    sql += "FROM " + tabla + " "
    sql += "WHERE estacion_id=" + str(estacion.est_id) + " "
    sql += "and date_part('year',fecha)=" + str(periodo)
    sql += "GROUP BY mes ORDER BY mes"
    cursor.execute(sql)
    med_mensual = dictfetchall(cursor)
    # datos diarios
    sql = "SELECT sum(valor) as valor, date_part('month',fecha) as mes, "
    sql += "date_part('day',fecha) as dia "
    sql += "FROM " + tabla + " "
    sql += "WHERE estacion_id=" + str(estacion.est_id) + " "
    sql += "and date_part('year',fecha)=" + str(periodo)
    sql += "GROUP BY mes,dia ORDER BY mes,dia"
    cursor.execute(sql)
    datos_diarios = dictfetchall(cursor)
    # Número de datos por mes
    sql = "SELECT date_part('month',fecha) as mes, count(*) as valor  "
    sql += "FROM " + tabla + " "
    sql += "WHERE estacion_id=" + str(estacion.est_id) + " "
    sql += "and date_part('year',fecha)=" + str(periodo)
    sql += "GROUP BY mes ORDER BY mes"
    cursor.execute(sql)
    num_registros = dictfetchall(cursor)

    max24h, maxdia, totdias = maximospre(datos_diarios)
    for item in med_mensual:
        mes = int(item.get('mes'))
        obj_precipitacion = Precipitacion()
        obj_precipitacion.est_id = estacion
        obj_precipitacion.pre_periodo = periodo
        obj_precipitacion.pre_mes = mes
        if item.get('suma') is not None:
            obj_precipitacion.pre_suma = item.get('suma')
        else:
            obj_precipitacion.pre_suma = 0
        obj_precipitacion.pre_maximo = max24h[mes - 1]
        obj_precipitacion.pre_maximo_dia = maxdia[mes - 1]
        obj_precipitacion.pre_dias = totdias[mes - 1]
        datos.append(obj_precipitacion)
    cursor.close()
    return datos


def maximospre(datos_diarios):
    # retorna maxima precipitacion mensual y en que dia sucedio y cuantos dias hubo precipitacion
    max24H = []
    maxdia = []
    totdias = []

    for i in range(1, 13):
        val_max24h = []
        val_maxdia = []
        # val_totdias = []
        for fila in datos_diarios:
            mes = int(fila.get('mes'))
            if mes == i:
                val_max24h.append(get_valor(fila))
                val_maxdia.append(int(fila.get('dia')))
        # contar dias con lluvia en la variable count
        count = 0
        for j in val_max24h:
            if j > 0:
                count += 1
        if len(val_max24h) > 0:
            max24H.append(max(val_max24h))
            maxdia.append(val_maxdia[val_max24h.index(max(val_max24h))])
        else:
            max24H.append(0)
            maxdia.append(0)
        totdias.append(count)
    return max24H, maxdia, totdias


def get_valor(fila):
    try:
        if isnan(fila.get('valor')):
            return 0
        return fila.get('valor')
    except TypeError:
        if fila.get('valor') is None:
            return 0
        return fila.get('valor')
