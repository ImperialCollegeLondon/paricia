# -*- coding: utf-8 -*-

from anuarios.models import Viento
from django.db import connection
from datetime import datetime


class VelocidaDireccion():
    velocidad = 0
    velocidad_max = 0
    direccion = 0

def matrizV_mensual(estacion, variable, periodo):
    
    tabla_velocidad = "medicion_velocidadviento" + periodo
    tabla_direccion = "medicin_direccionviento" + periodo

    cursor = connection.cursor()
    # velocidad media en m/s
    sql = "SELECT avg(med_valor) as valor, date_part('month',med_fecha) as mes "
    sql += "FROM " + tabla_velocidad + " "
    sql += "WHERE est_id_id=" + str(estacion.est_id) + " and med_valor!='NaN'::numeric "
    # sql += "AND date_part('month',med_fecha)=9 "
    sql += "GROUP BY mes ORDER BY mes"
    cursor.execute(sql)
    vel_media = dictfetchall(cursor)

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

    for item_calma, item_velocidad in zip(calma, vel_media):
        mes = int(item_velocidad.get('mes'))
        # lista de datos de la dirección de viento
        sql = "SELECT med_valor, med_fecha "
        sql += "FROM " + tabla_direccion + " "
        sql += "WHERE est_id_id=" + str(estacion.est_id) + " "
        sql += "AND date_part('month',med_fecha)=" + str(mes)+" "
        sql += "AND med_valor is not null AND med_valor<=360 "
        sql += "AND med_valor >=0 "
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
                vvi_max[0].append(get_maximo(item))
            elif item.direccion < 67.5:
                vvi[1].append(item.velocidad)
                vvi_max[1].append(get_maximo(item))
            elif item.direccion < 112.5:
                vvi[2].append(item.velocidad)
                vvi_max[2].append(get_maximo(item))
            elif item.direccion < 157.5:
                vvi[3].append(item.velocidad)
                vvi_max[3].append(get_maximo(item))
            elif item.direccion < 202.5:
                vvi[4].append(item.velocidad)
                vvi_max[4].append(get_maximo(item))
            elif item.direccion < 247.5:
                vvi[5].append(item.velocidad)
                vvi_max[5].append(get_maximo(item))
            elif item.direccion < 292.5:
                vvi[6].append(item.velocidad)
                vvi_max[6].append(get_maximo(item))
            elif item.direccion < 337.5:
                vvi[7].append(item.velocidad)
                vvi_max[7].append(get_maximo(item))
        maximos = []
        valores[mes - 1].append(mes)
        # recorro la matriz de datos en base al número de direcciones
        for j in range(8):
            if len(vvi[j]) > 0:
                vel_med = float(sum(vvi[j]) / len(vvi[j]))
                por_med = float(len(vvi[j])) / len(datos) * 100
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
        # porcentaje de calma
        if len(datos)>0:
            valor_calma = round(float(item_calma.get('calma')) / len(datos) * 100, 2)
        else:
            valor_calma = 0
        valores[mes - 1].append(valor_calma)
        # numero de observaciones
        valores[mes - 1].append(len(datos))
        # velocida maxima
        valores[mes - 1].append(round(max(maximos), 2))
        # dirección de la velocidad máxima
        valores[mes - 1].append(direcciones[maximos.index(max(maximos))])
        # velocidad media mensual
        valores[mes - 1].append(round(vel_media, 2))
    cursor.close()
    return valores


def get_maximo(item):
    if item.velocidad_max is None:
        if item.velocidad is None:
            return 0
        else:
            return item.velocidad
    return item.velocidad_max


def agrupar_viento(dat_dvi, dat_vvi):
    dvi_fecha = convertir_lista(dat_dvi, 'med_fecha')
    dvi_valor = convertir_lista(dat_dvi, 'med_valor')
    vvi_fecha = convertir_lista(dat_vvi, 'med_fecha')
    vvi_valor = convertir_lista(dat_vvi, 'med_valor')
    vvi_maximo = convertir_lista(dat_vvi, 'med_maximo')
    datos = []
    for item_fecha_vvi, item_valor_vvi, item_maximo_vvi in zip(vvi_fecha, vvi_valor, vvi_maximo):
        obj_viento = VelocidaDireccion()
        if item_fecha_vvi in dvi_fecha:
            item_fecha_dvi = dvi_fecha.index(item_fecha_vvi)
            obj_viento.velocidad = item_valor_vvi
            obj_viento.velocidad_max = item_maximo_vvi
            obj_viento.direccion = dvi_valor[item_fecha_dvi]
            datos.append(obj_viento)
    return datos


def convertir_lista(datos, indice):
    lista=[]
    for item in datos:
        lista.append(item.get(indice))
    return lista


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
