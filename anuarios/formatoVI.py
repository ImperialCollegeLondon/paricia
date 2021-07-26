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

from estacion.models import Estacion
from anuarios.models import Var7Anuarios as RadiacionSolar, RadiacionMaxima, RadiacionMinima
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count
from django.db.models.functions import (
    ExtractYear, ExtractMonth, ExtractDay, ExtractHour)
from datetime import datetime
from django.db import connection


class Radiacion(object):
    # matriz multidimensionall de 17 columnas por 12 filas
    maximo = [[0 for x in range(17)] for y in range(12)]
    minimo = [[0 for x in range(17)] for y in range(12)]


def matrizVI(estacion, variable, periodo, tipo):
    datos = []
    obj_rad = Radiacion()
    obj_rad.maximo = rad_max(estacion, variable, periodo, tipo)
    obj_rad.minimo = rad_min(estacion, variable, periodo, tipo)
    datos = obj_rad
    return datos


# consulta de radiacion maxima
def rad_max(estacion, variable, periodo, tipo):
    # consulta de maximos agrupados por hora y por mes
    # tabla = variable.var_codigo + ".m" + periodo
    if tipo == 'validado':
        tabla = 'validacion_var' + str(variable) + 'validado'
    else:
        tabla = 'medicion_var' + str(variable)+ 'medicion'
    cursor = connection.cursor()
    # select max(valor) as valor, date_part('month',fecha) as mes, date_part('hour',fecha) as hora
    # from rad.m2016 where estacion_id=12
    # and valor<=1400 and date_part('hour',fecha)>=5
    # and date_part('hour',fecha)<=18
    # group by mes, hora
    # order by mes, hora
    sql = "SELECT max(max_abs) as valor, date_part('month',fecha) as mes, "
    sql += "date_part('hour',fecha) as hora "
    #sql += "from " + tabla + " "
    sql += "FROM horario_var" + str(variable) + "horario "
    sql += "WHERE estacion_id=" + str(estacion.est_id) + " and valor<=1400 "
    sql += "and date_part('hour',fecha)>=5 "
    sql += "and date_part('hour',fecha)<=18 "
    sql += "and date_part('year',fecha)=" + str(periodo) + " "
    #sql += "and completo_mediciones >= 80"
    sql += "GROUP BY mes,hora ORDER BY mes,hora"
    print (sql)
    cursor.execute(sql)
    datos = dictfetchall(cursor)
    radiacion = [[0] for i in range(12)]
    obj_rad_max = RadiacionMaxima()
    for fila in datos:
        mes = int(fila.get('mes')) - 1
        radiacion[mes].append(round(fila.get('valor'), 2))
    for item in range(12):
        radiacion[item].append(max(radiacion[item]))
        radiacion[item].append(radiacion[item].index(max(radiacion[item])) + 4)
        radiacion[item][0] = item + 1
    cursor.close()
    return radiacion


def rad_min(estacion, variable, periodo, tipo):
    # tabla = variable.var_codigo + ".m" + periodo
    tabla = 'medicion_var' + str(variable)+ 'medicion'
    cursor = connection.cursor()
    sql = "SELECT min(min_abs) as valor, date_part('month',fecha) as mes, "
    sql += "date_part('hour',fecha) as hora  "
    #sql += "from " + tabla + " "
    sql += "FROM horario_var" + str(variable) + "horario "
    sql += "WHERE estacion_id=" + str(estacion.est_id) + " and valor<=1400 "
    sql += "and date_part('hour',fecha)>=5 "
    sql += "and date_part('hour',fecha)<=18 "
    sql += "and date_part('year',fecha)=" + str(periodo)+ " "
    #sql += "and completo_mediciones >= 80"
    sql += "GROUP BY mes,hora ORDER BY mes,hora"
    print(sql)
    cursor.execute(sql)
    datos = dictfetchall(cursor)
    radiacion = [[0] for i in range(12)]
    for fila in datos:
        mes = int(fila.get('mes')) - 1
        radiacion[mes][0] = mes + 1
        radiacion[mes].append(round(fila.get('valor'), 2))
    for item in range(12):
        radiacion[item].append(min(radiacion[item]))
        radiacion[item].append(radiacion[item].index(min(radiacion[item])) + 4)
    cursor.close()
    return radiacion


def datos_radiacion_maxima(datos, estacion, periodo):
    lista = []
    for fila in datos.maximo:
        if len(fila) > 3:
            obj_rad_max = RadiacionMaxima()
            obj_rad_max.est_id = estacion
            obj_rad_max.rad_periodo = periodo
            obj_rad_max.rad_mes = fila[0]
            obj_rad_max.rad_5 = fila[1]
            obj_rad_max.rad_6 = fila[2]
            obj_rad_max.rad_7 = fila[3]
            obj_rad_max.rad_8 = fila[4]
            obj_rad_max.rad_9 = fila[5]
            obj_rad_max.rad_10 = fila[6]
            obj_rad_max.rad_11 = fila[7]
            obj_rad_max.rad_12 = fila[8]
            obj_rad_max.rad_13 = fila[9]
            obj_rad_max.rad_14 = fila[10]
            obj_rad_max.rad_15 = fila[11]
            obj_rad_max.rad_16 = fila[12]
            obj_rad_max.rad_17 = fila[13]
            obj_rad_max.rad_18 = fila[14]
            obj_rad_max.rad_max = fila[15]
            obj_rad_max.rad_hora = fila[16]
            obj_rad_max.save()



def datos_radiacion_minimo(datos, estacion, periodo):
    lista = []
    for fila in datos.minimo:
        if len(fila) > 3:
            obj_rad_min = RadiacionMinima()
            obj_rad_min.est_id = estacion
            obj_rad_min.rad_periodo = periodo
            obj_rad_min.rad_mes = fila[0]
            obj_rad_min.rad_5 = fila[1]
            obj_rad_min.rad_6 = fila[2]
            obj_rad_min.rad_7 = fila[3]
            obj_rad_min.rad_8 = fila[4]
            obj_rad_min.rad_9 = fila[5]
            obj_rad_min.rad_10 = fila[6]
            obj_rad_min.rad_11 = fila[7]
            obj_rad_min.rad_12 = fila[8]
            obj_rad_min.rad_13 = fila[9]
            obj_rad_min.rad_14 = fila[10]
            obj_rad_min.rad_15 = fila[11]
            obj_rad_min.rad_16 = fila[12]
            obj_rad_min.rad_17 = fila[13]
            obj_rad_min.rad_18 = fila[14]
            obj_rad_min.rad_max = fila[15]
            obj_rad_min.rad_hora = fila[16]
            obj_rad_min.save()


def dictfetchall(cursor):
    # Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
