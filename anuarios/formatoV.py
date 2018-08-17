# -*- coding: utf-8 -*-

from anuarios.models import Viento
from django.db import connection
from datetime import datetime


class VelocidaDireccion():
    velocidad = 0
    velocidad_max = 0
    direccion = 0

def matrizV_mensual(estacion, variable, periodo):
    tabla_velocidad = "vvi.m" + periodo
    tabla_direccion = "dvi.m" + periodo

    cursor = connection.cursor()
    # velocidad media en m/s
    sql = "SELECT avg(med_valor) as valor, date_part('month',med_fecha) as mes "
    sql += "FROM " + tabla_velocidad + " "
    sql += "WHERE est_id_id=" + str(estacion.est_id) + " "
    sql += "GROUP BY mes ORDER BY mes"

    cursor.execute(sql)
    vel_media = dictfetchall(cursor)

    # numero de registros por mes en velocidad
    sql = "SELECT count(med_valor) as obs, date_part('month',med_fecha) as mes "
    sql += "FROM " + tabla_velocidad + " "
    sql += "WHERE est_id_id=" + str(estacion.est_id) + " "
    sql += "GROUP BY mes ORDER BY mes"
    cursor.execute(sql)
    num_obs = dictfetchall(cursor)
    # numero de registros menores a 0.5 en velocidad
    sql = "SELECT count(med_valor) as calma, date_part('month',med_fecha) as mes "
    sql += "FROM " + tabla_velocidad + " "
    sql += "WHERE est_id_id=" + str(estacion.est_id) + " and med_valor<0.5 "
    sql += "GROUP BY mes ORDER BY mes"
    cursor.execute(sql)
    calma = dictfetchall(cursor)
    if len(calma) == 0:
        # numero de registros menores o igual a 0.5 en velocidad
        sql = "SELECT count(med_valor) as calma, date_part('month',med_fecha) as mes "
        sql += "FROM " + tabla_velocidad + " "
        sql += "WHERE est_id_id=" + str(estacion.est_id) + " and med_valor<0.6"
        sql += "GROUP BY mes ORDER BY mes"
        cursor.execute(sql)
        calma = dictfetchall(cursor)
    direcciones = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]
    valores = [[] for y in range(12)]
    num_total_obs=get_total_obs(num_obs)
    for item_obs, item_calma, item_velocidad in zip(num_obs, calma, vel_media):
        mes = int(item_obs.get('mes'))
        # lista de datos de la dirección de viento
        sql = "SELECT med_valor, med_fecha "
        sql += "FROM " + tabla_direccion + " "
        sql += "WHERE est_id_id=" + str(estacion.est_id) + " "
        sql += "AND date_part('month',med_fecha)=" + str(mes)+" "
        sql += "AND med_valor is not null "
        sql += "ORDER BY med_fecha"
        cursor.execute(sql)
        dat_dvi = dictfetchall(cursor)
        # lista de datos de velocidad del viento
        sql = "SELECT med_valor,med_maximo, med_fecha "
        sql += "FROM " + tabla_velocidad + " "
        sql += "WHERE est_id_id=" + str(estacion.est_id) + " "
        sql += "AND date_part('month',med_fecha)=" + str(mes)+" "
        sql += "AND med_valor is not null "
        sql += "ORDER BY med_fecha"
        cursor.execute(sql)
        dat_vvi = dictfetchall(cursor)
        vvi = [[0 for x in range(0)] for y in range(8)]
        vvi_max = [[0 for x in range(0)] for y in range(8)]
        datos = agrupar_viento(dat_dvi, dat_vvi)
        for item in datos:
            if item.direccion < 22.5 or item.direccion > 337.5:
                vvi[0].append(item.velocidad)
                vvi_max[0].append(item.velocidad_max)
            elif item.direccion < 67.5:
                vvi[1].append(item.velocidad)
                vvi_max[1].append(item.velocidad_max)
            elif item.direccion < 112.5:
                vvi[2].append(item.velocidad)
                vvi_max[2].append(item.velocidad_max)
            elif item.direccion < 157.5:
                vvi[3].append(item.velocidad)
                vvi_max[3].append(item.velocidad_max)
            elif item.direccion < 202.5:
                vvi[4].append(item.velocidad)
                vvi_max[4].append(item.velocidad_max)
            elif item.direccion < 247.5:
                vvi[5].append(item.velocidad)
                vvi_max[5].append(item.velocidad_max)
            elif item.direccion < 292.5:
                vvi[6].append(item.velocidad)
                vvi_max[6].append(item.velocidad_max)
            elif item.direccion < 337.5:
                vvi[7].append(item.velocidad)
                vvi_max[7].append(item.velocidad_max)
        maximos = []
        valores[mes - 1].append(mes)
        # recorro la matriz de datos en base al número de direcciones
        for j in range(8):
            if len(vvi[j]) > 0:
                vel_med = float(sum(vvi[j]) / len(vvi[j]))
                por_med = float(len(vvi[j])) / item_obs.get('obs') * 100
            else:
                vel_med = 0.0
                por_med = 0.0
            # promedio de velocidades medias por direccion
            valores[mes - 1].append(round(vel_med, 2))
            # porcentaje por direccion
            valores[mes - 1].append(round(por_med, 2))
            # maximos por direcciion
            if len(vvi_max[j]) > 0:
                maximos.append(max(vvi_max[j]))
            else:
                maximos.append(float(0))
        # velocidad media en km/h
        vel_media = item_velocidad.get('valor')*36/10
        valor_calma = round(float(item_calma.get('calma')) / item_obs.get('obs') * 100, 2)
        valores[mes - 1].append(valor_calma)
        valores[mes - 1].append(item_obs.get('obs'))
        valores[mes - 1].append(round(max(maximos), 2))
        valores[mes - 1].append(direcciones[maximos.index(max(maximos))])
        valores[mes - 1].append(round(vel_media, 2))
    cursor.close()
    return valores


def get_maximo(fila):
    if fila.get('med_maximo') is None:
        if fila.get('med_valor') is None:
            return 0
        else:
            return fila.get('med_valor')
    return fila.get('med_maximo')

def get_total_obs(num_obs):
    suma=0
    for item_obs in num_obs:
        suma += item_obs.get('obs')
    return suma


def agrupar_viento(dat_dvi, dat_vvi):
    len_dvi = len(dat_dvi)
    len_vvi = len(dat_vvi)

    if len_dvi == len_vvi:
        longitud =len_dvi
    else:
        if len_vvi > len_dvi:
            vvi = True
            longitud =len_vvi
        else:
            vvi = False
            longitud = len_dvi
    datos = []
    i = 0  # velocidad
    j = 0  # direccion
    for item in range(longitud):
        obj_viento = VelocidaDireccion()
        if dat_vvi[i].get('med_fecha') == dat_dvi[j].get('med_fecha'):
            obj_viento.velocidad = dat_vvi[i].get('med_valor')
            obj_viento.velocidad_max = get_maximo(dat_vvi[i])
            obj_viento.direccion = dat_dvi[j].get('med_valor')
            datos.append(obj_viento)
            i += 1
            j += 1
        else:
            if vvi:
                i += 1
            else:
                j += 1
    return datos



def datos_viento(datos, estacion, periodo):
    lista = []
    for fila in datos:
        if len(fila) > 0:
            obj_viento = Viento()
            obj_viento.est_id = estacion
            obj_viento.vie_periodo = periodo
            obj_viento.vie_mes = fila[0]
            obj_viento.vie_vel_N = fila[1]
            obj_viento.vie_por_N = fila[2]
            obj_viento.vie_vel_NE = fila[3]
            obj_viento.vie_por_NE = fila[4]
            obj_viento.vie_vel_E = fila[5]
            obj_viento.vie_por_E = fila[6]
            obj_viento.vie_vel_SE = fila[7]
            obj_viento.vie_por_SE = fila[8]
            obj_viento.vie_vel_S = fila[9]
            obj_viento.vie_por_S = fila[10]
            obj_viento.vie_vel_SO = fila[11]
            obj_viento.vie_por_SO = fila[12]
            obj_viento.vie_vel_O = fila[13]
            obj_viento.vie_por_O = fila[14]
            obj_viento.vie_vel_NO = fila[15]
            obj_viento.vie_por_NO = fila[16]
            obj_viento.vie_calma = fila[17]
            obj_viento.vie_obs = fila[18]
            obj_viento.vie_vel_max = fila[19]
            obj_viento.vie_vel_dir = fila[20]
            obj_viento.vie_vel_med = fila[21]
            lista.append(obj_viento)
    return lista


def dictfetchall(cursor):
    # Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
