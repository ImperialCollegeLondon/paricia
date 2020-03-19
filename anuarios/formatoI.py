# -*- coding: utf-8 -*-

from anuarios.models import PresionAtmosferica, HumedadSuelo, TemperaturaAgua, Caudal, NivelAgua
from django.db import connection
from home.functions import dictfetchall
from anuarios.anuario import Anuarios
from math import isnan


class FormatoI(Anuarios):
    maximo = 0
    minimo = 0
    promedio = 0

    def consulta(self, estacion, variable, periodo,tipo):
        cursor = connection.cursor()
        tabla = 'validacion_' + str(variable.var_modelo)
        sql = "SELECT "
        if tipo == 'maixmo':
            sql += "max(valor) as valor, "
        elif tipo == 'minimo':
            sql += "min(valor) as valor, "
        else:
            sql += "avg(valor) as valor, "

        sql += "date_part('month',fecha) as mes "
        sql += "FROM " + tabla + " "
        sql += "WHERE estacion_id=" + str(estacion.est_id) + " and valor!='NaN'::numeric "
        sql += "and date_part('year',fecha)=" + str(periodo)
        # if variable.var_id == 8:
        # sql += " and maximo!=0 and minimo!=0 and valor!=0 "
        if variable.var_id == 6 or variable.var_id == 8:
            sql += " and (maximo!=0 or minimo!=0 or valor!=0) "
        sql += "GROUP BY mes ORDER BY mes"








    def matriz(self, estacion, variable, periodo):
        pass


def matrizI(estacion, variable, periodo, tipo):
    datos = []
    cursor = connection.cursor()
    # tabla = variable.var_codigo + '.m' + periodo
    if tipo == 'validado':
        tabla = 'validacion_' + str(variable.var_modelo)
    else:
        tabla = 'medicion_' + str(variable.var_modelo)
    # máximos absolutos y máximos promedio
    sql = "SELECT max(maximo) as maximo,  max(valor) as valor, "
    sql += "date_part('month',fecha) as mes "
    sql += "FROM " + tabla + " "
    sql += "WHERE estacion_id=" + str(estacion.est_id) + " and valor!='NaN'::numeric "
    sql += "and date_part('year',fecha)=" + str(periodo)
    # if variable.var_id == 8:
        # sql += " and maximo!=0 and minimo!=0 and valor!=0 "
    if variable.var_id == 6 or variable.var_id == 8:
        sql += " and (maximo!=0 or minimo!=0 or valor!=0) "
    sql += "GROUP BY mes ORDER BY mes"
    print(sql)
    cursor.execute(sql)
    med_max = dictfetchall(cursor)
    # mínimos absolutos y mínimos promedio
    sql = "SELECT min(minimo) as minimo,  min(valor) as valor, "
    sql += "date_part('month',fecha) as mes "
    sql += "FROM " + tabla + " "
    sql += "WHERE estacion_id=" + str(estacion.est_id) + " and valor!='NaN'::numeric "
    sql += "and date_part('year',fecha)=" + str(periodo)
    # if variable.var_id == 8:
        # sql += " and maximo!=0 and minimo!=0 and valor!=0 "
    if variable.var_id == 6 or variable.var_id == 8:
        sql += " and (maximo!=0 or minimo!=0 or valor!=0) "
    sql += "GROUP BY mes ORDER BY mes"
    print(sql)
    cursor.execute(sql)
    med_min = dictfetchall(cursor)
    # valores promedio mensuales
    sql = "SELECT avg(valor) as valor, date_part('month',fecha) as mes "
    sql += "FROM " + tabla + " "
    sql += "WHERE estacion_id=" + str(estacion.est_id) + " and valor!='NaN'::numeric "
    sql += "and date_part('year',fecha)=" + str(periodo)
    # if variable.var_id == 8:
        # sql += " and maximo!=0 and minimo!=0 and valor!=0 "
    if variable.var_id == 6 and variable.var_id == 8:
        sql += " and (maximo!=0 or minimo!=0 or valor!=0) "
    sql += "GROUP BY mes ORDER BY mes"
    cursor.execute(sql)
    print(sql)
    med_avg = dictfetchall(cursor)

    for item_max, item_min, item_avg in zip(med_max, med_min, med_avg):
        mes = int(item_avg.get('mes'))
        if variable.var_id == 6:
            obj_hsu = HumedadSuelo()
            obj_hsu.est_id = estacion
            obj_hsu.hsu_periodo = periodo
            obj_hsu.hsu_mes = mes
            obj_hsu.hsu_maximo = get_maximo(item_max)
            obj_hsu.hsu_minimo = get_minimo(item_min)
            obj_hsu.hsu_promedio = get_promedio(item_avg)
            datos.append(obj_hsu)
        elif variable.var_id == 8:
            obj_pat = PresionAtmosferica()
            obj_pat.est_id = estacion
            obj_pat.pat_periodo = periodo
            obj_pat.pat_mes = mes
            obj_pat.pat_maximo = get_maximo(item_max)
            obj_pat.pat_minimo = get_minimo(item_min)
            obj_pat.pat_promedio = get_promedio(item_avg)
            datos.append(obj_pat)
        elif variable.var_id == 9:
            obj_tag = TemperaturaAgua()
            obj_tag.est_id = estacion
            obj_tag.tag_periodo = periodo
            obj_tag.tag_mes = mes
            obj_tag.tag_maximo = get_maximo(item_max)
            obj_tag.tag_minimo = get_minimo(item_min)
            obj_tag.tag_promedio = get_promedio(item_avg)
            datos.append(obj_tag)
        elif variable.var_id == 10:
            obj_cau = Caudal()
            obj_cau.est_id = estacion
            obj_cau.cau_periodo = periodo
            obj_cau.cau_mes = mes
            obj_cau.cau_maximo = get_maximo(item_max)
            obj_cau.cau_minimo = get_minimo(item_min)
            obj_cau.cau_promedio = get_promedio(item_avg)
            datos.append(obj_cau)
        elif variable.var_id == 11:
            obj_nag = NivelAgua()
            obj_nag.est_id = estacion
            obj_nag.nag_periodo = periodo
            obj_nag.nag_mes = mes
            obj_nag.nag_maximo = get_maximo(item_max)
            obj_nag.nag_minimo = get_minimo(item_min)
            obj_nag.nag_promedio = get_promedio(item_avg)
            datos.append(obj_nag)
    cursor.close()
    return datos


'''def get_maximo(item_max):
    print(item_max)
    if isnan(item_max.get('maximo')):
        return round(item_max.get('valor'), 2)
    return round(item_max.get('maximo'), 2)


def get_minimo(item_min):
    if isnan(item_min.get('minimo')):
        return round(item_min.get('valor'), 2)
    return round(item_min.get('minimo'), 2)


def get_promedio(item_avg):
    if isnan(item_avg.get('valor')):
        return 0
    return round(item_avg.get('valor'), 2)'''


def get_maximo(item_max):
    try:

        if isnan(item_max.get('maximo')):
            if isnan(item_max.get('valor')):
                return 0
            else:
                return round(item_max.get('valor'), 2)
        return round(item_max.get('maximo'), 2)
    except TypeError:
        if item_max.get('maximo') is None:
            if item_max.get('valor') is None:
                return 0
            else:
                return round(item_max.get('valor'), 2)
        return round(item_max.get('maximo'), 2)


def get_minimo(item_min):
    print(item_min)
    try:
        if isnan(item_min.get('minimo')):
            if isnan(item_min.get('valor')):
                return 0
            else:
                return round(item_min.get('valor'), 2)
        return round(item_min.get('minimo'), 2)
    except TypeError:
        if item_min.get('minimo') is None:
            if item_min.get('valor') is None:
                return 0
            else:
                return round(item_min.get('valor'), 2)
        return round(item_min.get('minimo'), 2)


def get_promedio(item_avg):
    if item_avg.get('valor') is None:
        return 0
    return round(item_avg.get('valor'), 2)
