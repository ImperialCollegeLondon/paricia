# -*- coding: utf-8 -*-
from django.db import connection
from datetime import timedelta

def consultar_dias(form):
    cursor = connection.cursor()
    estacion = form.cleaned_data['estacion']
    variable = form.cleaned_data['variable']
    fecha_ini = form.cleaned_data['inicio']
    fecha_fin = form.cleaned_data['fin']
    year_ini = fecha_ini.strftime('%Y')
    year_fin = fecha_fin.strftime('%Y')
    var_cod = variable.var_codigo
    datos=[]
    if year_ini == year_fin:
        tabla = var_cod + '.m' + year_ini
        sql = 'SELECT date_trunc(\'day\',med_fecha) as fecha from ' + tabla + ' '
        sql += 'where est_id_id=' + str(estacion.est_id) + ' and '
        sql += 'med_fecha>=\'' + str(fecha_ini) + '\' and '
        sql += 'med_fecha<=\'' + str(fecha_fin) + ' 23:59:59\' '
        sql += 'group by fecha order by fecha'
        cursor.execute(sql)
        datos = dictfetchall(cursor)
    else:
        range_year = range(int(year_ini), int(year_fin) + 1)
        for year in range_year:
            tabla = var_cod + '.m' + str(year)
            if str(year) == year_ini:
                sql = 'SELECT date_trunc(\'day\',med_fecha) as fecha from ' + tabla + ' '
                sql += 'where est_id_id=' + str(estacion.est_id) + ' and '
                sql += 'med_fecha>=\'' + str(fecha_ini) + '\' and '
                sql += 'group by fecha order by fecha'
            elif str(year) == year_fin:
                sql = 'SELECT date_trunc(\'day\',med_fecha) as fecha from ' + tabla + ' '
                sql += 'where est_id_id=' + str(estacion.est_id) + ' and '
                sql += 'med_fecha<=\'' + str(fecha_fin) + ' 23:59:59\' '
                sql += 'group by fecha order by fecha'
            else:
                sql = 'SELECT date_trunc(\'day\',med_fecha) from ' + tabla + ' '
                sql += 'where est_id_id=' + str(estacion.est_id)
                sql += 'group by fecha order by fecha'
            cursor.execute(sql)
            datos.extend(dictfetchall(cursor))
    return datos


def dias_sin_datos(datos, form):
    fecha_ini = form.cleaned_data['inicio']
    fecha_fin = form.cleaned_data['fin']
    intervalo = timedelta(days=1)
    int_dias = (fecha_fin - fecha_ini).days + 1
    item = 0
    fecha = fecha_ini
    datos_sin = []
    for dia in range(int_dias):
        if fecha == datos[item].get('fecha').date():
            item += 1
        else:
            datos_sin.append({'fecha_sin': fecha})
        fecha += intervalo
    return datos_sin


def dictfetchall(cursor):
    # Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]