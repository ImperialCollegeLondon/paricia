# -*- coding: utf-8 -*-

from horario.models import *
from django.db import connection
from home.functions import dictfetchall


def get_porcentaje_registro(form):
    estacion = form.cleaned_data['estacion']
    variable = form.cleaned_data['variable']
    fecha_ini = form.cleaned_data['inicio']
    fecha_fin = form.cleaned_data['fin']
    tabla = 'horario_' + str(variable.var_modelo)
    cursor = connection.cursor()

    sql = """
    WITH 
    horarios AS (SELECT * FROM horario_%%var_id%% WHERE estacion_id = %%est_id%% 
    AND fecha >'%%inicio%%' and fecha<'%%fin%%'),
    reporte_css as(
        Select *, 
        case when h.valor is null then 'error' else 'normal' end as class_valor,
        case when h.completo_mediciones <= 70 then 'error' else 'normal' end as class_porcentaje
        from horarios h
    )
    Select rf.fecha, rf.valor, rf.class_valor, rf.completo_mediciones, rf.class_porcentaje from reporte_css rf
    """

    sql = sql.replace("%%var_id%%", variable.var_modelo).replace("%%est_id%%", str(estacion.est_id)).\
        replace("%%inicio%%", str(fecha_ini)).replace("%%fin%%", str(fecha_fin))
    print(sql)
    cursor.execute(sql)
    datos = dictfetchall(cursor)
    cursor.close()
    return datos


