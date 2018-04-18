# -*- coding: utf-8 -*-
from estacion.models import Estacion
from variable.models import Variable, Unidad
from medicion.models import Medicion
from django.db.models import Max, Min, Avg, Count, Sum
from django.db.models.functions import (
    ExtractYear, ExtractMonth, ExtractDay, ExtractHour)
import plotly.offline as opy
import plotly.graph_objs as go
import calendar
from datetime import timedelta, datetime
from django.db import connection
from math import ceil
import time


def grafico(form):
    estacion = form.cleaned_data['estacion']
    variable = form.cleaned_data['variable']
    fecha_inicio = form.cleaned_data['inicio']
    fecha_fin = form.cleaned_data['fin']
    frecuencia = form.cleaned_data['frecuencia']
    div = ""
    # frecuencia instantanea
    if (frecuencia == str(0)):
        valores, maximos, minimos, tiempo = datos_instantaneos(estacion, variable, fecha_inicio, fecha_fin)
    # frecuencia 5 minutos
    elif (frecuencia == str(1)):
        valores, maximos, minimos, tiempo = datos_5minutos(estacion, variable, fecha_inicio, fecha_fin)
    # frecuencia horaria
    elif (frecuencia == str(2)):
        valores, maximos, minimos, tiempo = datos_horarios(estacion, variable, fecha_inicio, fecha_fin)
    # frecuencia diaria
    elif (frecuencia == str(3)):
        valores, maximos, minimos, tiempo = datos_diarios(estacion, variable, fecha_inicio, fecha_fin)
    # frecuencia mensual
    elif (frecuencia == str(4)):
        valores, maximos, minimos, tiempo = datos_mensuales(estacion, variable, fecha_inicio, fecha_fin)
    else:
        valores, maximos, minimos, tiempo = datos_instantaneos(estacion, variable, fecha_inicio, fecha_fin)
    if len(valores) > 0:
        if variable.var_id == 1:
            trace = go.Bar(
                x=tiempo,
                y=valores,
                name='Precipitacion (mm)'
            )
            data = go.Data([trace])
        elif variable.var_id in [2, 3, 6, 8, 9, 10, 11]:
            print(len(maximos))
            trace0 = go.Scatter(
                x=tiempo,
                y=maximos,
                name='Max',
                mode='lines',
                line=dict(
                    color=('rgb(205, 12, 24)'),
                )
            )
            trace1 = go.Scatter(
                x=tiempo,
                y=minimos,
                name='Min',
                mode='lines',
                line=dict(
                    color=('rgb(50, 205, 50)'),
                )
            )
            trace2 = go.Scatter(
                x=tiempo,
                y=valores,
                name='Media',
                mode='lines',
                line=dict(
                    color=('rgb(22, 96, 167)'),
                )
            )
            data = go.Data([trace0, trace1, trace2])
        else:
            trace = go.Scatter(
                x=tiempo,
                y=valores,
                name='Valor',
                mode='lines',
                line=dict(
                    color=('rgb(205, 12, 24)'),
                )
            )
            data = go.Data([trace])
        layout = go.Layout(
            title=variable.var_nombre + \
                  " " + str(titulo_frecuencia(frecuencia)) + \
                  " " + estacion.est_codigo,
            yaxis=dict(title=variable.var_nombre + \
                             str(" (") + variable.uni_id.uni_sigla + str(")")),
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='1y',
                             step='year',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(),
                type='date'
            )
        )

        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')
    return div


def datos_instantaneos(estacion, variable, fecha_inicio, fecha_fin):
    year_ini = fecha_inicio.strftime('%Y')
    year_fin = fecha_fin.strftime('%Y')
    var_cod = variable.var_codigo
    if year_ini == year_fin:
        tabla = var_cod + '.m' + year_ini
        sql = 'SELECT * FROM ' + tabla + ' WHERE '
        sql += 'est_id_id=' + str(estacion.est_id) + ' and '
        sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' and '
        sql += 'med_fecha<=\'' + str(fecha_fin) + '\' order by med_fecha'
        consulta = list(Medicion.objects.raw(sql))
    else:
        range_year = range(int(year_ini), int(year_fin) + 1)
        consulta = []
        for year in range_year:
            tabla = var_cod + '.m' + str(year)
            if str(year) == year_ini:
                sql = 'SELECT * FROM ' + tabla + ' WHERE '
                sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                sql += 'and med_estado is not False and '
                sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' order by med_fecha'
            elif str(year) == year_fin:
                sql = 'SELECT * FROM ' + tabla + ' WHERE '
                sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                sql += 'and med_estado is not False and '
                sql += 'med_fecha<=\'' + str(fecha_fin) + ' 23:59:59 \' order by med_fecha'
            else:
                sql = 'SELECT * FROM ' + tabla + ' WHERE '
                sql += 'med_estado is not False and '
                sql += 'est_id_id=' + str(estacion.est_id) + ' order by med_fecha'
            consulta.extend(list(Medicion.objects.raw(sql)))
    valor = []
    maximo = []
    minimo = []
    frecuencia = []
    for fila in consulta:
        if fila.med_valor is not None:
            valor.append(fila.med_valor)
        else:
            valor.append(None)
        if fila.med_maximo is not None:
            maximo.append(fila.med_maximo)
        else:
            maximo.append(None)
        if fila.med_minimo is not None:
            minimo.append(fila.med_minimo)
        else:
            minimo.append(None)
        # frecuencia.append(datetime.combine(fila['med_fecha'],fila['med_hora']))
        frecuencia.append(fila.med_fecha)
    return valor, maximo, minimo, frecuencia


def datos_5minutos(estacion, variable, fecha_inicio, fecha_fin):
    year_ini = fecha_inicio.strftime('%Y')
    year_fin = fecha_fin.strftime('%Y')
    var_cod = variable.var_codigo
    cursor = connection.cursor()
    datos = []
    if year_ini == year_fin:
        tabla = var_cod + '.m' + year_ini
        if variable.var_id == 1:
            sql = 'SELECT sum(med_valor) as valor, '
            sql += 'to_timestamp(floor((extract(\'epoch\' '
            sql += 'from med_fecha) / 300 )) * 300)'
            sql += 'AT TIME ZONE \'UTC5\' as interval_alias '
            sql += 'FROM ' + tabla + ' WHERE '
            sql += 'est_id_id=' + str(estacion.est_id) + ' and '
            sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' and '
            sql += 'med_fecha<=\'' + str(fecha_fin) + ' 23:59:59\' '
            sql += 'and med_estado is not False '
            sql += 'GROUP BY interval_alias '
            sql += 'ORDER BY interval_alias'
        elif variable.var_id in [2, 3, 6, 8, 9, 10, 11]:
            sql = 'SELECT avg(med_valor) as valor, '
            sql += 'max(med_maximo) as maximo, '
            sql += 'min(med_minimo) as minimo, '
            sql += 'to_timestamp(floor((extract(\'epoch\' '
            sql += 'from med_fecha) / 300 )) * 300)'
            sql += 'AT TIME ZONE \'UTC5\' as interval_alias '
            sql += 'FROM ' + tabla + ' WHERE '
            sql += 'est_id_id=' + str(estacion.est_id) + ' and '
            sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' and '
            sql += 'med_fecha<=\'' + str(fecha_fin) + ' 23:59:59\' '
            sql += 'and med_estado is not False '
            sql += 'GROUP BY interval_alias '
            sql += 'ORDER BY interval_alias'
        else:
            sql = 'SELECT avg(med_valor) as valor, '
            sql += 'to_timestamp(floor((extract(\'epoch\' '
            sql += 'from med_fecha) / 300 )) * 300)'
            sql += 'AT TIME ZONE \'UTC5\' as interval_alias '
            sql += 'FROM ' + tabla + ' WHERE '
            sql += 'est_id_id=' + str(estacion.est_id) + ' and '
            sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' and '
            sql += 'med_fecha<=\'' + str(fecha_fin) + ' 23:59:59\'  '
            sql += 'and med_estado is not False '
            sql += 'GROUP BY interval_alias '
            sql += 'ORDER BY interval_alias'
        cursor.execute(sql)
        datos = dictfetchall(cursor)
    else:
        range_year = range(int(year_ini), int(year_fin) + 1)
        consulta = []
        for year in range_year:
            tabla = var_cod + '.m' + str(year)
            if str(year) == year_ini:
                if variable.var_id == 1:
                    sql = 'SELECT sum(med_valor) as valor, '
                    sql += 'to_timestamp(floor((extract(\'epoch\' '
                    sql += 'from med_fecha) / 300 )) * 300)'
                    sql += 'AT TIME ZONE \'UTC5\' as interval_alias '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY interval_alias '
                    sql += 'ORDER BY interval_alias'
                elif variable.var_id in [2, 3, 6, 8, 9, 10, 11]:
                    sql = 'SELECT avg(med_valor) as valor, '
                    sql += 'max(med_maximo) as maximo, '
                    sql += 'min(med_minimo) as minimo, '
                    sql += 'to_timestamp(floor((extract(\'epoch\' '
                    sql += 'from med_fecha) / 300 )) * 300)'
                    sql += 'AT TIME ZONE \'UTC5\' as interval_alias '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY interval_alias '
                    sql += 'ORDER BY interval_alias'
                    print(sql)
                else:
                    sql = 'SELECT avg(med_valor) as valor, '
                    sql += 'to_timestamp(floor((extract(\'epoch\' '
                    sql += 'from med_fecha) / 300 )) * 300)'
                    sql += 'AT TIME ZONE \'UTC5\' as interval_alias '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY interval_alias '
                    sql += 'ORDER BY interval_alias'
            elif str(year) == year_fin:
                if variable.var_id == 1:
                    sql = 'SELECT sum(med_valor) as valor, '
                    sql += 'to_timestamp(floor((extract(\'epoch\' '
                    sql += 'from med_fecha) / 300 )) * 300)'
                    sql += 'AT TIME ZONE \'UTC5\' as interval_alias '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha<=\'' + str(fecha_fin) + ' 23:59:59\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY interval_alias '
                    sql += 'ORDER BY interval_alias'
                elif variable.var_id in [2, 3, 6, 8, 9, 10, 11]:
                    sql = 'SELECT avg(med_valor) as valor, '
                    sql += 'max(med_maximo) as maximo, '
                    sql += 'min(med_minimo) as minimo, '
                    sql += 'to_timestamp(floor((extract(\'epoch\' '
                    sql += 'from med_fecha) / 300 )) * 300)'
                    sql += 'AT TIME ZONE \'UTC5\' as interval_alias '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha<=\'' + str(fecha_fin) + ' 23:59:59\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY interval_alias '
                    sql += 'ORDER BY interval_alias'
                else:
                    sql = 'SELECT avg(med_valor) as valor, '
                    sql += 'to_timestamp(floor((extract(\'epoch\' '
                    sql += 'from med_fecha) / 300 )) * 300)'
                    sql += 'AT TIME ZONE \'UTC5\' as interval_alias '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha<=\'' + str(fecha_fin) + ' 23:59:59\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY interval_alias '
                    sql += 'ORDER BY interval_alias'
            else:
                sql = 'SELECT * FROM ' + tabla + ' WHERE '
                sql += 'est_id_id=' + str(estacion.est_id) + ' order by med_fecha'
                if variable.var_id == 1:
                    sql = 'SELECT sum(med_valor) as valor, '
                    sql += 'to_timestamp(floor((extract(\'epoch\' '
                    sql += 'from med_fecha) / 300 )) * 300)'
                    sql += 'AT TIME ZONE \'UTC5\' as interval_alias '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY interval_alias '
                    sql += 'ORDER BY interval_alias'
                elif variable.var_id in [2, 3, 6, 8, 9, 10, 11]:
                    sql = 'SELECT avg(med_valor) as valor, '
                    sql = 'max(med_maximo) as maximo, '
                    sql = 'min(med_minimo) as minimo, '
                    sql += 'to_timestamp(floor((extract(\'epoch\' '
                    sql += 'from med_fecha) / 300 )) * 300)'
                    sql += 'AT TIME ZONE \'UTC5\' as interval_alias '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY interval_alias '
                    sql += 'ORDER BY interval_alias'
                else:
                    sql = 'SELECT avg(med_valor) as valor, '
                    sql += 'to_timestamp(floor((extract(\'epoch\' '
                    sql += 'from med_fecha) / 300 )) * 300)'
                    sql += 'AT TIME ZONE \'UTC5\' as interval_alias '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY interval_alias '
                    sql += 'ORDER BY interval_alias'
            cursor.execute(sql)
            datos.extend(dictfetchall(cursor))

    valor = []
    maximo = []
    minimo = []
    frecuencia = []
    intervalo = timedelta(minutes=5)
    fecha = datetime.combine(fecha_inicio, datetime.min.time())
    int_dias = ((fecha_fin - fecha_inicio).days + 1) * 288
    num_datos = len(datos)
    item = 0
    for dia in range(int_dias):
        if item < num_datos:
            fecha_datos = datos[item].get('interval_alias')
            if fecha_datos == fecha:
                valor.append(datos[item].get('valor'))
                maximo.append(datos[item].get('maximo'))
                minimo.append(datos[item].get('minimo'))
                # frecuencia.append(fecha_datos)
                # fecha+=intervalo
                item += 1
            else:
                valor.append(None)
                maximo.append(None)
                minimo.append(None)
            frecuencia.append(fecha)
            fecha += intervalo
    cursor.close()
    return valor, maximo, minimo, frecuencia


def datos_horarios(estacion, variable, fecha_inicio, fecha_fin):
    year_ini = fecha_inicio.strftime('%Y')
    year_fin = fecha_fin.strftime('%Y')
    var_cod = variable.var_codigo
    cursor = connection.cursor()
    datos = []
    if year_ini == year_fin:
        tabla = var_cod + '.m' + year_ini
        if variable.var_id == 1:
            sql = 'SELECT '
            sql += 'date_part(\'year\', med_fecha) as anio, '
            sql += 'date_part(\'month\', med_fecha) as mes, '
            sql += 'date_part(\'day\',med_fecha) as dia, '
            sql += 'date_part(\'hour\',med_fecha) as hora, '
            sql += 'sum(med_valor) as valor '
            sql += 'FROM ' + tabla + ' WHERE '
            sql += 'est_id_id=' + str(estacion.est_id) + ' and '
            sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' and '
            sql += 'med_fecha<=\'' + str(fecha_fin) + '\''
            sql += 'and med_estado is not False '
            sql += 'GROUP BY anio, mes, dia, hora '
            sql += 'ORDER BY anio, mes, dia, hora '
        elif variable.var_id in [2, 3, 6, 8, 9, 10, 11]:
            sql = 'SELECT '
            sql += 'date_part(\'year\', med_fecha) as anio, '
            sql += 'date_part(\'month\', med_fecha) as mes, '
            sql += 'date_part(\'day\',med_fecha) as dia, '
            sql += 'date_part(\'hour\',med_fecha) as hora, '
            sql += 'avg(med_valor) as valor, '
            sql += 'max(med_maximo) as maximo, '
            sql += 'min(med_minimo) as minimo '
            sql += 'FROM ' + tabla + ' WHERE '
            sql += 'est_id_id=' + str(estacion.est_id) + ' and '
            sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' and '
            sql += 'med_fecha<=\'' + str(fecha_fin) + '\''
            sql += 'and med_estado is not False '
            sql += 'GROUP BY anio, mes, dia, hora '
            sql += 'ORDER BY anio, mes, dia, hora'
            print(sql)
        else:
            sql = 'SELECT '
            sql += 'date_part(\'year\', med_fecha) as anio, '
            sql += 'date_part(\'month\', med_fecha) as mes, '
            sql += 'date_part(\'day\',med_fecha) as dia, '
            sql += 'date_part(\'hour\',med_fecha) as hora, '
            sql += 'avg(med_valor) as valor '
            sql += 'FROM ' + tabla + ' WHERE '
            sql += 'est_id_id=' + str(estacion.est_id) + ' and '
            sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' and '
            sql += 'med_fecha<=\'' + str(fecha_fin) + '\' '
            sql += 'and med_estado is not False '
            sql += 'GROUP BY anio, mes, dia, hora '
            sql += 'ORDER BY anio, mes, dia, hora'
        cursor.execute(sql)
        datos = dictfetchall(cursor)
    else:
        range_year = range(int(year_ini), int(year_fin) + 1)
        for year in range_year:
            tabla = var_cod + '.m' + str(year)
            if str(year) == year_ini:
                if variable.var_id == 1:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'date_part(\'day\',med_fecha) as dia, '
                    sql += 'date_part(\'hour\',med_fecha) as hora, '
                    sql += 'sum(med_valor) as valor '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes, dia, hora '
                    sql += 'ORDER BY anio, mes, dia, hora'
                elif variable.var_id in [2, 3, 6, 8, 9, 10, 11]:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'date_part(\'day\',med_fecha) as dia, '
                    sql += 'date_part(\'hour\',med_fecha) as hora, '
                    sql += 'avg(med_valor) as valor, '
                    sql += 'max(med_maximo) as maximo, '
                    sql += 'min(med_minimo) as minimo '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes, dia, hora '
                    sql += 'ORDER BY anio, mes, dia, hora'
                else:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'date_part(\'day\',med_fecha) as dia, '
                    sql += 'date_part(\'hour\',med_fecha) as hora, '
                    sql += 'avg(med_valor) as valor '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes, dia, hora '
                    sql += 'ORDER BY anio, mes, dia, hora'
            elif str(year) == year_fin:
                if variable.var_id == 1:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'date_part(\'day\',med_fecha) as dia, '
                    sql += 'date_part(\'hour\',med_fecha) as hora, '
                    sql += 'sum(med_valor) as valor '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha<=\'' + str(fecha_fin) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes, dia, hora '
                    sql += 'ORDER BY anio, mes, dia, hora'
                elif variable.var_id in [2, 3, 6, 8, 9, 10, 11]:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'date_part(\'day\',med_fecha) as dia, '
                    sql += 'date_part(\'hour\',med_fecha) as hora, '
                    sql += 'avg(med_valor) as valor, '
                    sql += 'max(med_maximo) as maximo, '
                    sql += 'min(med_minimo) as minimo '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha<=\'' + str(fecha_fin) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes, dia, hora '
                    sql += 'ORDER BY anio, mes, dia, hora'
                else:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'date_part(\'day\',med_fecha) as dia, '
                    sql += 'date_part(\'hour\',med_fecha) as hora, '
                    sql += 'avg(med_valor) as valor '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha<=\'' + str(fecha_fin) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes, dia, hora '
                    sql += 'ORDER BY anio, mes, dia, hora'
            else:
                if variable.var_id == 1:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'date_part(\'day\',med_fecha) as dia, '
                    sql += 'date_part(\'hour\',med_fecha) as hora, '
                    sql += 'sum(med_valor) as valor '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes, dia, hora '
                    sql += 'ORDER BY anio, mes, dia, hora'
                elif variable.var_id in [2, 3, 6, 8, 9, 10, 11]:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'date_part(\'day\',med_fecha) as dia, '
                    sql += 'date_part(\'hour\',med_fecha) as hora, '
                    sql += 'avg(med_valor) as valor, '
                    sql += 'max(med_maximo) as maximo, '
                    sql += 'min(med_minimo) as minimo '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes, dia, hora '
                    sql += 'ORDER BY anio, mes, dia, hora'
                else:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'date_part(\'day\',med_fecha) as dia, '
                    sql += 'date_part(\'hour\',med_fecha) as hora, '
                    sql += 'avg(med_valor) as valor '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes, dia, hora '
                    sql += 'ORDER BY anio, mes, dia, hora'
            cursor.execute(sql)
            datos.extend(dictfetchall(cursor))
    valor = []
    maximo = []
    minimo = []
    frecuencia = []
    intervalo = timedelta(hours=1)
    fecha = datetime.combine(fecha_inicio, datetime.min.time())
    int_dias = ((fecha_fin - fecha_inicio).days + 1) * 24
    num_datos = len(datos)
    item = 0
    for dia in range(int_dias):
        if item < num_datos:
            fecha_str = (str(int(datos[item].get('anio'))) + "-" +
                         str(int(datos[item].get('mes'))) + "-" +
                         str(int(datos[item].get('dia'))) + " " +
                         str(int(datos[item].get('hora'))))
            fecha_datos = datetime.strptime(fecha_str, '%Y-%m-%d %H')
            # fecha_datos=datetime.combine(fecha,hora)
            if fecha_datos == fecha:
                valor.append(datos[item].get('valor'))
                maximo.append(datos[item].get('maximo'))
                minimo.append(datos[item].get('minimo'))
                # frecuencia.append(fecha_datos)
                # fecha+=intervalo
                item += 1
            else:
                valor.append(None)
                maximo.append(None)
                minimo.append(None)
            frecuencia.append(fecha)
            fecha += intervalo
    return valor, maximo, minimo, frecuencia


def datos_diarios(estacion, variable, fecha_inicio, fecha_fin):
    year_ini = fecha_inicio.strftime('%Y')
    year_fin = fecha_fin.strftime('%Y')
    var_cod = variable.var_codigo
    cursor = connection.cursor()
    datos = []
    if year_ini == year_fin:
        tabla = var_cod + '.m' + year_ini
        if variable.var_id == 1:
            sql = 'SELECT '
            sql += 'date_part(\'year\', med_fecha) as anio, '
            sql += 'date_part(\'month\', med_fecha) as mes, '
            sql += 'date_part(\'day\',med_fecha) as dia, '
            sql += 'sum(med_valor) as valor '
            sql += 'FROM ' + tabla + ' WHERE '
            sql += 'est_id_id=' + str(estacion.est_id) + ' and '
            sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' and '
            sql += 'med_fecha<=\'' + str(fecha_fin) + '\' '
            sql += 'and med_estado is not False '
            sql += 'GROUP BY anio, mes, dia '
            sql += 'ORDER BY anio, mes, dia'
        elif variable.var_id in [2, 3, 6, 8, 9, 10, 11]:
            sql = 'SELECT '
            sql += 'date_part(\'year\', med_fecha) as anio, '
            sql += 'date_part(\'month\', med_fecha) as mes, '
            sql += 'date_part(\'day\',med_fecha) as dia, '
            sql += 'avg(med_valor) as valor, '
            sql += 'max(med_maximo) as maximo, max(med_valor) as maximo2, '
            sql += 'min(med_minimo) as minimo, min(med_valor) as minimo2 '
            sql += 'FROM ' + tabla + ' WHERE '
            sql += 'est_id_id=' + str(estacion.est_id) + ' and '
            sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' and '
            sql += 'med_fecha<=\'' + str(fecha_fin) + '\' '
            sql += 'and med_estado is not False '
            sql += 'GROUP BY anio, mes, dia '
            sql += 'ORDER BY anio, mes, dia'
            print(sql)
        else:
            sql = 'SELECT '
            sql += 'date_part(\'year\', med_fecha) as anio, '
            sql += 'date_part(\'month\', med_fecha) as mes, '
            sql += 'date_part(\'day\',med_fecha) as dia, '
            sql += 'avg(med_valor) as valor, '
            sql += 'max(med_valor) as maximo, '
            sql += 'min(med_valor) as minimo '
            sql += 'FROM ' + tabla + ' WHERE '
            sql += 'est_id_id=' + str(estacion.est_id) + ' and '
            sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' and '
            sql += 'med_fecha<=\'' + str(fecha_fin) + '\' '
            sql += 'and med_estado is not False '
            sql += 'GROUP BY anio, mes, dia '
            sql += 'ORDER BY anio, mes, dia'
        cursor.execute(sql)
        datos = dictfetchall(cursor)
    else:
        range_year = range(int(year_ini), int(year_fin) + 1)
        for year in range_year:
            tabla = var_cod + '.m' + str(year)
            if str(year) == year_ini:
                if variable.var_id == 1:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'date_part(\'day\',med_fecha) as dia, '
                    sql += 'sum(med_valor) as valor '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes, dia '
                    sql += 'ORDER BY anio, mes, dia'
                elif variable.var_id in [2, 3, 6, 8, 9, 10, 11]:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'date_part(\'day\',med_fecha) as dia, '
                    sql += 'avg(med_valor) as valor, '
                    sql += 'max(med_maximo) as maximo, max(med_valor) as maximo2, '
                    sql += 'min(med_minimo) as minimo, min(med_valor) as minimo2 '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes, dia '
                    sql += 'ORDER BY anio, mes, dia'
                else:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'date_part(\'day\',med_fecha) as dia, '
                    sql += 'avg(med_valor) as valor, '
                    sql += 'max(med_valor) as maximo, '
                    sql += 'min(med_valor) as minimo '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes, dia '
                    sql += 'ORDER BY anio, mes, dia'
            elif str(year) == year_fin:
                if variable.var_id == 1:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'date_part(\'day\',med_fecha) as dia, '
                    sql += 'sum(med_valor) as valor '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha<=\'' + str(fecha_fin) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes, dia '
                    sql += 'ORDER BY anio, mes, dia'
                elif variable.var_id in [2, 3, 6, 8, 9, 10, 11]:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'date_part(\'day\',med_fecha) as dia, '
                    sql += 'avg(med_valor) as valor, '
                    sql += 'max(med_maximo) as maximo, max(med_valor) as maximo2, '
                    sql += 'min(med_minimo) as minimo, min(med_valor) as minimo2 '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha<=\'' + str(fecha_fin) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes, dia '
                    sql += 'ORDER BY anio, mes, dia'
                else:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'date_part(\'day\',med_fecha) as dia, '
                    sql += 'avg(med_valor) as valor, '
                    sql += 'max(med_valor) as maximo, '
                    sql += 'min(med_valor) as minimo '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha<=\'' + str(fecha_fin) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes, dia '
                    sql += 'ORDER BY anio, mes, dia'
            else:
                if variable.var_id == 1:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'date_part(\'day\',med_fecha) as dia, '
                    sql += 'sum(med_valor) as valor '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes, dia '
                    sql += 'ORDER BY anio, mes, dia'
                elif variable.var_id in [2, 3, 6, 8, 9, 10, 11]:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'date_part(\'day\',med_fecha) as dia, '
                    sql += 'avg(med_valor) as valor, '
                    sql += 'max(med_maximo) as maximo, max(med_valor) as maximo2, '
                    sql += 'min(med_minimo) as minimo, min(med_valor) as minimo2 '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes, dia '
                    sql += 'ORDER BY anio, mes, dia'
                else:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'date_part(\'day\',med_fecha) as dia, '
                    sql += 'avg(med_valor) as valor, '
                    sql += 'max(med_valor) as maximo, '
                    sql += 'min(med_valor) as minimo '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes, dia '
                    sql += 'ORDER BY anio, mes, dia'
            cursor.execute(sql)
            datos.extend(dictfetchall(cursor))
    valor = []
    maximo = []
    minimo = []
    frecuencia = []
    intervalo = timedelta(days=1)
    fecha = fecha_inicio
    int_dias = (fecha_fin - fecha_inicio).days + 1
    num_datos = len(datos)
    item = 0
    for dia in range(int_dias):
        if item < num_datos:
            fecha_str = (str(int(datos[item].get('anio'))) + "-" +
                         str(int(datos[item].get('mes'))) + "-" +
                         str(int(datos[item].get('dia'))))
            fecha_datos = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            if fecha_datos == fecha:
                valor.append(datos[item].get('valor'))
                if datos[item].get('maximo') is not None:
                    maximo.append(datos[item].get('maximo'))
                elif datos[item].get('maximo2') is not None:
                    maximo.append(datos[item].get('maximo2'))
                if datos[item].get('minimo'):
                    minimo.append(datos[item].get('minimo'))
                elif datos[item].get('minimo2'):
                    minimo.append(datos[item].get('minimo2'))
                # frecuencia.append(fecha_datos)
                # fecha+=intervalo
                item += 1
            else:
                valor.append(None)
                maximo.append(None)
                minimo.append(None)
            frecuencia.append(fecha)
            fecha += intervalo
    return valor, maximo, minimo, frecuencia


def datos_mensuales(estacion, variable, fecha_inicio, fecha_fin):
    year_ini = fecha_inicio.strftime('%Y')
    year_fin = fecha_fin.strftime('%Y')
    var_cod = variable.var_codigo
    cursor = connection.cursor()
    datos = []
    if year_ini == year_fin:
        tabla = var_cod + '.m' + year_ini
        if variable.var_id == 1:
            sql = 'SELECT '
            sql += 'date_part(\'year\', med_fecha) as anio, '
            sql += 'date_part(\'month\', med_fecha) as mes, '
            sql += 'sum(med_valor) as valor '
            sql += 'FROM ' + tabla + ' WHERE '
            sql += 'est_id_id=' + str(estacion.est_id) + ' and '
            sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' and '
            sql += 'med_fecha<=\'' + str(fecha_fin) + '\' '
            sql += 'and med_estado is not False '
            sql += 'GROUP BY anio, mes '
            sql += 'ORDER BY anio, mes'
        elif variable.var_id in [2, 3, 6, 8, 9, 10, 11]:
            sql = 'SELECT '
            sql += 'date_part(\'year\', med_fecha) as anio, '
            sql += 'date_part(\'month\', med_fecha) as mes, '
            sql += 'avg(med_valor) as valor, '
            sql += 'max(med_maximo) as maximo, '
            sql += 'min(med_minimo) as minimo '
            sql += 'FROM ' + tabla + ' WHERE '
            sql += 'est_id_id=' + str(estacion.est_id) + ' and '
            sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' and '
            sql += 'med_fecha<=\'' + str(fecha_fin) + '\' '
            sql += 'and med_estado is not False '
            sql += 'GROUP BY anio, mes '
            sql += 'ORDER BY anio, mes'
            print(sql)
        else:
            sql = 'SELECT '
            sql += 'date_part(\'year\', med_fecha) as anio, '
            sql += 'date_part(\'month\', med_fecha) as mes, '
            sql += 'avg(med_valor) as valor '
            sql += 'FROM ' + tabla + ' WHERE '
            sql += 'est_id_id=' + str(estacion.est_id) + ' and '
            sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' and '
            sql += 'med_fecha<=\'' + str(fecha_fin) + '\' '
            sql += 'and med_estado is not False '
            sql += 'GROUP BY anio, mes '
            sql += 'ORDER BY anio, mes'
        cursor.execute(sql)
        datos = dictfetchall(cursor)
    else:
        range_year = range(int(year_ini), int(year_fin) + 1)
        for year in range_year:
            tabla = var_cod + '.m' + str(year)
            if str(year) == year_ini:
                if variable.var_id == 1:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'sum(med_valor) as valor '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes '
                    sql += 'ORDER BY anio, mes'
                elif variable.var_id in [2, 3, 6, 8, 9, 10, 11]:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'avg(med_valor) as valor, '
                    sql += 'max(med_maximo) as maximo, '
                    sql += 'min(med_minimo) as minimo '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes '
                    sql += 'ORDER BY anio, mes'
                else:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'avg(med_valor) as valor '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes '
                    sql += 'ORDER BY anio, mes'
            elif str(year) == year_fin:
                if variable.var_id == 1:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'sum(med_valor) as valor '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha<=\'' + str(fecha_fin) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes '
                    sql += 'ORDER BY anio, mes'
                elif variable.var_id in [2, 3, 6, 8, 9, 10, 11]:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'avg(med_valor) as valor, '
                    sql += 'max(med_maximo) as maximo, '
                    sql += 'min(med_minimo) as minimo '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha<=\'' + str(fecha_fin) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes '
                    sql += 'ORDER BY anio, mes'
                else:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'avg(med_valor) as valor '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                    sql += 'med_fecha<=\'' + str(fecha_fin) + '\' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes '
                    sql += 'ORDER BY anio, mes'
            else:
                if variable.var_id == 1:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'sum(med_valor) as valor '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes '
                    sql += 'ORDER BY anio, mes'
                elif variable.var_id in [2, 3, 6, 8, 9, 10, 11]:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'avg(med_valor) as valor, '
                    sql += 'max(med_maximo) as maximo, '
                    sql += 'min(med_minimo) as minimo '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes '
                    sql += 'ORDER BY anio, mes'
                else:
                    sql = 'SELECT '
                    sql += 'date_part(\'year\', med_fecha) as anio, '
                    sql += 'date_part(\'month\', med_fecha) as mes, '
                    sql += 'avg(med_valor) as valor '
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += 'est_id_id=' + str(estacion.est_id) + ' '
                    sql += 'and med_estado is not False '
                    sql += 'GROUP BY anio, mes '
                    sql += 'ORDER BY anio, mes'
            cursor.execute(sql)
            datos.extend(dictfetchall(cursor))
    valor = []
    maximo = []
    minimo = []
    frecuencia = []
    fecha = fecha_inicio.replace(day=1)
    intervalo = timedelta(days=30)
    dias = float((fecha_fin - fecha_inicio).days)
    meses = int(ceil(dias / 30))
    print(meses)
    num_datos = len(datos)
    item = 0
    for mes in range(meses):
        if item < num_datos:
            fecha_str = (str(int(datos[item].get('anio'))) + "-" +
                         str(int(datos[item].get('mes'))))
            fecha_datos = datetime.strptime(fecha_str, '%Y-%m').date()
            if fecha == fecha_datos:
                valor.append(datos[item].get('valor'))
                maximo.append(datos[item].get('maximo'))
                minimo.append(datos[item].get('minimo'))
                item += 1
            else:
                valor.append(None)
                maximo.append(None)
                minimo.append(None)
            fecha_str = str(calendar.month_abbr[fecha.month]) + " " + str(fecha.year)
            frecuencia.append(fecha)
            intervalo = dias_mes(fecha.month, fecha.year)
            fecha += timedelta(days=intervalo)

    return valor, maximo, minimo, frecuencia
    # fecha_str = str(calendar.month_abbr[fila.get('month')])+" "+str(fila.get('year'))


def dias_mes(month, year):
    dias = 30
    if month <= 7:
        if month % 2 == 0 and month != 2:
            dias = 30
        elif month % 2 == 0 and month == 2:
            if year % 4 == 0:
                dias = 29
            else:
                dias = 28
        else:
            dias = 31
    else:
        if month % 2 == 0:
            dias = 31
        else:
            dias = 30
    return dias


def titulo_frecuencia(frecuencia):
    nombre = []
    if frecuencia == '0':
        nombre = 'Instantanea'
    if frecuencia == '1':
        nombre = '5 Minutos'
    elif frecuencia == '2':
        nombre = 'Horaria'
    elif frecuencia == '3':
        nombre = 'Diaria'
    elif frecuencia == '4':
        nombre = 'Mensual'
    return nombre


def dictfetchall(cursor):
    # Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def datos_horarios_json(est_id, var_id, fec_ini, fec_fin):
    consulta = (Medicion.objects.filter(est_id=est_id)
                .filter(var_id=var_id).filter(med_fecha__range=[fec_ini, fec_fin]))
    consulta = consulta.annotate(year=ExtractYear('med_fecha'),
                                 month=ExtractMonth('med_fecha'),
                                 day=ExtractDay('med_fecha'),
                                 hour=ExtractHour('med_fecha')
                                 ).values('year', 'month', 'day', 'hour')
    if (var_id == 1):
        consulta = list(consulta.annotate(valor=Sum('med_valor')).
                        values('valor', 'year', 'month', 'day', 'hour').
                        order_by('year', 'month', 'day', 'hour'))
    else:
        consulta = list(consulta.annotate(valor=Avg('med_valor'),
                                          maximo=Max('med_maximo'), minimo=Min('med_minimo')).
                        values('valor', 'maximo', 'minimo', 'year', 'month', 'day', 'hour').
                        order_by('year', 'month', 'day', 'hour'))
    datos = []
    if len(consulta) > 0:
        for fila in consulta:
            fecha_str = (str(fila.get('year')) + ":" +
                         str(fila.get('month')) + ":" + str(fila.get('day')))
            fecha = datetime.strptime(fecha_str, '%Y:%m:%d').date()
            hora = datetime.time(fila.get('hour'))
            fecha_hora = datetime.combine(fecha, hora)
            dato = {
                'fecha': fecha_hora,
                'valor': fila.get('valor'),
                'maximo': fila.get('maximo'),
                'minimo': fila.get('minimo'),
            }
            datos.append(dato)
    else:
        datos = {
            'mensaje': 'no hay datos'
        }
    return datos
