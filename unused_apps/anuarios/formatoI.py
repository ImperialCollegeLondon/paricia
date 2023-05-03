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

from math import isnan

from django.db import connection

from anuarios.anuario import Anuarios
from anuarios.models import Var6Anuarios as HumedadSuelo
from anuarios.models import Var8Anuarios as PresionAtmosferica
from anuarios.models import Var9Anuarios as TemperaturaAgua
from anuarios.models import Var10Anuarios as Caudal
from anuarios.models import Var11Anuarios as NivelAgua
from home.functions import dictfetchall


class FormatoI(Anuarios):
    maximo = 0
    minimo = 0
    promedio = 0

    def consulta(self, estacion, variable, periodo, tipo):
        cursor = connection.cursor()
        tabla = "validacion_var" + str(variable) + "validado"
        sql = "SELECT "
        if tipo == "maixmo":
            sql += "max(valor) as valor, "
        elif tipo == "minimo":
            sql += "min(valor) as valor, "
        else:
            sql += "avg(valor) as valor, "

        sql += "date_part('month',fecha) as mes "
        sql += "FROM " + tabla + " "
        sql += (
            "WHERE estacion_id=" + str(estacion.est_id) + " and valor!='NaN'::numeric "
        )
        sql += "and date_part('year',fecha)=" + str(periodo)
        # if variable == 8:
        # sql += " and maximo!=0 and minimo!=0 and valor!=0 "
        if variable == 6 or variable == 8:
            sql += " and (maximo!=0 or minimo!=0 or valor!=0) "
        sql += "GROUP BY mes ORDER BY mes"
        cursor.close()

    def matriz(self, estacion, variable, periodo):
        pass


def matrizI(estacion, variable, periodo, tipo):
    datos = []
    cursor = connection.cursor()
    # tabla = variable.var_codigo + '.m' + periodo
    if tipo == "validado":
        tabla = "validacion_var" + str(variable) + "validado"
    else:
        tabla = "medicion_var" + str(variable) + "medicion"
    # máximos absolutos y máximos promedio
    sql = "SELECT max(max_abs) as maximo,  max(valor) as valor, "
    # sql = "SELECT max(maximo) as maximo,  max(valor) as valor, "
    sql += "date_part('month',fecha) as mes "
    # sql += "FROM " + tabla + " "
    sql += "FROM mensual_var" + str(variable) + "mensual "
    sql += "WHERE estacion_id=" + str(estacion.est_id) + " and valor!='NaN'::numeric "
    sql += "and date_part('year',fecha)=" + str(periodo) + " "
    sql += (
        "and vacios < (SELECT v.vacios FROM variable_variable v WHERE v.var_id = "
        + str(variable)
        + ") "
    )
    # if variable == 8:
    # sql += " and maximo!=0 and minimo!=0 and valor!=0 "
    if variable == 6 or variable == 8:
        # sql += " and (maximo!=0 or minimo!=0 or valor!=0) "
        sql += " and (max_abs!=0 or min_abs!=0 or valor!=0) "
    sql += "GROUP BY mes ORDER BY mes"
    cursor.execute(sql)
    med_max = dictfetchall(cursor)
    # mínimos absolutos y mínimos promedio
    # sql = "SELECT min(minimo) as minimo,  min(valor) as valor, "
    sql = "SELECT min(min_abs) as minimo,  min(valor) as valor, "
    sql += "date_part('month',fecha) as mes "
    # sql += "FROM " + tabla + " "
    sql += "FROM mensual_var" + str(variable) + "mensual "
    sql += "WHERE estacion_id=" + str(estacion.est_id) + " and valor!='NaN'::numeric "
    sql += "and date_part('year',fecha)=" + str(periodo) + " "
    sql += (
        "and vacios < (SELECT v.vacios FROM variable_variable v WHERE v.var_id = "
        + str(variable)
        + ") "
    )
    # if variable == 8:
    # sql += " and maximo!=0 and minimo!=0 and valor!=0 "
    if variable == 6 or variable == 8:
        # sql += " and (maximo!=0 or minimo!=0 or valor!=0) "
        sql += " and (max_abs!=0 or min_abs!=0 or valor!=0) "
    sql += "GROUP BY mes ORDER BY mes"
    cursor.execute(sql)
    med_min = dictfetchall(cursor)
    # valores promedio mensuales
    sql = "SELECT avg(valor) as valor, date_part('month',fecha) as mes "
    # sql += "FROM " + tabla + " "
    sql += "FROM mensual_var" + str(variable) + "mensual "
    sql += "WHERE estacion_id=" + str(estacion.est_id) + " and valor!='NaN'::numeric "
    sql += "and date_part('year',fecha)=" + str(periodo) + " "
    sql += (
        "and vacios < (SELECT v.vacios FROM variable_variable v WHERE v.var_id = "
        + str(variable)
        + ") "
    )
    # if variable == 8:
    # sql += " and maximo!=0 and minimo!=0 and valor!=0 "
    if variable == 6 and variable == 8:
        # sql += " and (maximo!=0 or minimo!=0 or valor!=0) "
        sql += " and (max_abs!=0 or min_abs!=0 or valor!=0) "
    sql += "GROUP BY mes ORDER BY mes"
    cursor.execute(sql)
    med_avg = dictfetchall(cursor)

    for item_max, item_min, item_avg in zip(med_max, med_min, med_avg):
        mes = int(item_avg.get("mes"))
        if variable == 6:
            obj_hsu = HumedadSuelo()
            obj_hsu.est_id = estacion
            obj_hsu.hsu_periodo = periodo
            obj_hsu.hsu_mes = mes
            obj_hsu.hsu_maximo = get_maximo(item_max)
            obj_hsu.hsu_minimo = get_minimo(item_min)
            obj_hsu.hsu_promedio = get_promedio(item_avg)
            datos.append(obj_hsu)
        elif variable == 8:
            obj_pat = PresionAtmosferica()
            obj_pat.est_id = estacion
            obj_pat.pat_periodo = periodo
            obj_pat.pat_mes = mes
            obj_pat.pat_maximo = get_maximo(item_max)
            obj_pat.pat_minimo = get_minimo(item_min)
            obj_pat.pat_promedio = get_promedio(item_avg)
            datos.append(obj_pat)
        elif variable == 9:
            obj_tag = TemperaturaAgua()
            obj_tag.est_id = estacion
            obj_tag.tag_periodo = periodo
            obj_tag.tag_mes = mes
            obj_tag.tag_maximo = get_maximo(item_max)
            obj_tag.tag_minimo = get_minimo(item_min)
            obj_tag.tag_promedio = get_promedio(item_avg)
            datos.append(obj_tag)
        elif variable == 10:
            obj_cau = Caudal()
            obj_cau.est_id = estacion
            obj_cau.cau_periodo = periodo
            obj_cau.cau_mes = mes
            obj_cau.cau_maximo = get_maximo(item_max)
            obj_cau.cau_minimo = get_minimo(item_min)
            obj_cau.cau_promedio = get_promedio(item_avg)
            datos.append(obj_cau)
        elif variable == 11:
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
    try:
        if isnan(item_max.get("maximo")):
            if isnan(item_max.get("valor")):
                return 0
            else:
                return round(item_max.get("valor"), 2)
        return round(item_max.get("maximo"), 2)
    except TypeError:
        if item_max.get("maximo") is None:
            if item_max.get("valor") is None:
                return 0
            else:
                return round(item_max.get("valor"), 2)
        return round(item_max.get("maximo"), 2)


def get_minimo(item_min):
    try:
        if isnan(item_min.get("minimo")):
            if isnan(item_min.get("valor")):
                return 0
            else:
                return round(item_min.get("valor"), 2)
        return round(item_min.get("minimo"), 2)
    except TypeError:
        if item_min.get("minimo") is None:
            if item_min.get("valor") is None:
                return 0
            else:
                return round(item_min.get("valor"), 2)
        return round(item_min.get("minimo"), 2)


def get_promedio(item_avg):
    if item_avg.get("valor") is None:
        return 0
    return round(item_avg.get("valor"), 2)
