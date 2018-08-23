# -*- coding: utf-8 -*-

from anuarios.models import PresionAtmosferica, HumedadSuelo, TemperaturaAgua, Caudal, NivelAgua
from django.db import connection
from home.functions import dictfetchall


def matrizI(estacion, variable, periodo):
    datos = []
    cursor = connection.cursor()
    tabla = variable.var_codigo + '.m' + periodo
    # máximos absolutos y máximos promedio
    sql = "SELECT max(med_maximo) as maximo,  max(med_valor) as valor, "
    sql += "date_part('month',med_fecha) as mes "
    sql += "FROM " + tabla + " "
    sql += "WHERE est_id_id=" + str(estacion.est_id) + " "
    if variable.var_id == 8:
        sql += " and med_maximo!=0 and med_minimo!=0 and med_valor!=0 "
    sql += "GROUP BY mes ORDER BY mes"
    cursor.execute(sql)
    med_max = dictfetchall(cursor)
    # mínimos absolutos y mínimos promedio
    sql = "SELECT min(med_maximo) as minimo,  min(med_valor) as valor, "
    sql += "date_part('month',med_fecha) as mes "
    sql += "FROM " + tabla + " "
    sql += "WHERE est_id_id=" + str(estacion.est_id) + " "
    if variable.var_id == 8:
        sql += " and med_maximo!=0 and med_minimo!=0 and med_valor!=0 "
    sql += "GROUP BY mes ORDER BY mes"
    cursor.execute(sql)
    med_min = dictfetchall(cursor)
    # valores promedio mensuales
    sql = "SELECT avg(med_valor) as valor, date_part('month',med_fecha) as mes "
    sql += "FROM " + tabla + " "
    sql += "WHERE est_id_id=" + str(estacion.est_id) + " "
    if variable.var_id == 8:
        sql += " and med_maximo!=0 and med_minimo!=0 and med_valor!=0 "
    sql += "GROUP BY mes ORDER BY mes"
    cursor.execute(sql)
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


def get_maximo(item_max):
    if item_max.get('maximo') is None:
        return round(item_max.get('valor'), 2)
    return round(item_max.get('maximo'), 2)


def get_minimo(item_min):
    if item_min.get('minimo') is None:
        return round(item_min.get('valor'), 2)
    return round(item_min.get('minimo'), 2)


def get_promedio(item_avg):
    if item_avg.get('valor') is None:
        return 0
    return round(item_avg.get('valor'), 2)