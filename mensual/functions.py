# -*- coding: utf-8 -*-

from mensual.models import *
from django.db import connection
from home.functions import dictfetchall


def get_frecuencia_registro(form):
    estacion = form.cleaned_data['estacion']
    variable = form.cleaned_data['variable']
    periodo = form.cleaned_data['periodo']
    # tabla = "pre.m" + periodo
    tabla = 'mensual_' + str(variable.var_modelo)
    cursor = connection.cursor()
    # promedio  de la frecuencia de registro registro
    sql = "SELECT date_part('month',fecha) as mes, completo_mediciones "
    sql += "FROM " + tabla + " "
    sql += "WHERE estacion_id=" + str(estacion.est_id) + " "
    sql += "and date_part('year',fecha)=" + str(periodo)
    sql += "ORDER BY mes"
    cursor.execute(sql)
    datos = dictfetchall(cursor)
    return datos


