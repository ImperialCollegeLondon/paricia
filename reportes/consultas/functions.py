# -*- coding: utf-8 -*-

from medicion.models import Medicion
from estacion.models import Estacion
from variable.models import Variable
import plotly.offline as opy
import plotly.graph_objs as go
from datetime import timedelta, datetime
from django.db import connection
from math import ceil


suma = 'sum(med_valor) as valor '
promedio = 'avg(med_valor) as valor '
max_abs = 'max(med_maximo) as max_abs '
max_pro = 'max(med_valor) as max_pro '
min_abs = 'min(med_minimo) as min_abs  '
min_pro = 'min(med_valor) as min_pro '
coma = ', '
group_order = 'GROUP BY fecha ORDER BY fecha'
var_max_min = [2, 3, 4, 6, 8, 9, 10, 11]

def grafico(form):
    estacion = form.cleaned_data['estacion']
    variable = form.cleaned_data['variable']
    fecha_inicio = form.cleaned_data['inicio']
    fecha_fin = form.cleaned_data['fin']
    frecuencia = form.cleaned_data['frecuencia']
    div = ""
    # frecuencia instantanea
    if (frecuencia == str(0)):
        valores, maximos_abs, minimos_abs, tiempo = datos_instantaneos(estacion, variable, fecha_inicio, fecha_fin)
        maximos_pro = []
        minimos_pro = []
    # frecuencia 5 minutos
    elif (frecuencia == str(1)):
        valores, maximos_abs, maximos_pro, minimos_abs, minimos_pro, tiempo = datos_5minutos(estacion, variable, fecha_inicio, fecha_fin)
    # frecuencia horaria
    elif (frecuencia == str(2)):
        valores, maximos_abs, maximos_pro, minimos_abs, minimos_pro, tiempo = datos_horarios(estacion, variable, fecha_inicio, fecha_fin)
    # frecuencia diaria
    elif (frecuencia == str(3)):
        valores, maximos_abs, maximos_pro, minimos_abs, minimos_pro, tiempo = datos_diarios(estacion, variable, fecha_inicio, fecha_fin)
    # frecuencia mensual
    elif (frecuencia == str(4)):
        valores, maximos_abs, maximos_pro, minimos_abs, minimos_pro, tiempo = datos_mensuales(estacion, variable, fecha_inicio, fecha_fin)
    else:
        valores, maximos, minimos, tiempo = datos_instantaneos(estacion, variable, fecha_inicio, fecha_fin)
    if len(valores) > 0:
        if variable.var_id == 1:
            tra_pro = go.Bar(
                x=tiempo,
                y=valores,
            )
            data = go.Data([tra_pro])
        elif frecuencia == str(0):
            tra_prom = go.Scatter(
                x=tiempo,
                y=valores,
                name='Valor',
                mode='lines',
                line=dict(
                    color='#1660A7',
                )
            )
            tra_max_abs = go.Scatter(
                x=tiempo,
                y=maximos_abs,
                name='Máximo',
                mode='lines',
                line=dict(
                    color='#32CD32',
                )
            )
            tra_min_abs = go.Scatter(
                x=tiempo,
                y=minimos_abs,
                name='Mínimo',
                mode='lines',
                line=dict(
                    color='#CD0C18',
                )
            )
            data = go.Data([tra_max_abs, tra_prom, tra_min_abs])
        else:
            tra_prom = go.Scatter(
                x=tiempo,
                y=valores,
                name='Media',
                mode='lines',
                line=dict(
                    color='#1660A7',
                )
            )
            if len(maximos_abs) != maximos_abs.count(None) and len(maximos_pro) != maximos_pro.count(None):
                tra_max_abs = go.Scatter(
                    x=tiempo,
                    y=maximos_abs,
                    name='Máximo Absoluto',
                    mode='lines',
                    line=dict(
                        color='#32CD32',
                    )
                )
                tra_max_pro = go.Scatter(
                    x=tiempo,
                    y=maximos_pro,
                    name='Máximo del Promedio',
                    mode='lines',
                    visible="legendonly",
                    line=dict(
                        color='#90EE90',
                    )
                )
            elif len(maximos_abs) == maximos_abs.count(None) and len(maximos_pro) != maximos_pro.count(None):
                tra_max_abs = []
                tra_max_pro = go.Scatter(
                    x=tiempo,
                    y=maximos_pro,
                    name='Máximo del Promedio',
                    mode='lines',
                    line=dict(
                        color='#90EE90',
                    )
                )
            if len(minimos_abs) != minimos_abs.count(None) and len(minimos_pro) != minimos_pro.count(None):
                tra_min_abs = go.Scatter(
                    x=tiempo,
                    y=minimos_abs,
                    name='Mínimo Absoluto',
                    mode='lines',
                    line=dict(
                        color='#CD0C18',
                    )
                )
                tra_min_pro = go.Scatter(
                    x=tiempo,
                    y=minimos_pro,
                    name='Mínimo del  Promedio',
                    mode='lines',
                    visible="legendonly",
                    line=dict(
                        color='#FF8C00',
                    )
                )
            elif len(minimos_abs) == minimos_abs.count(None) and len(minimos_pro) != minimos_pro.count(None):
                tra_min_abs = []
                tra_min_pro = go.Scatter(
                    x=tiempo,
                    y=minimos_pro,
                    name='Mínimo del Promedio',
                    mode='lines',
                    line=dict(
                        color='#FF8C00',
                    )
                )
            if len(tra_max_abs) > 0 and len(tra_min_abs) > 0:
                data = go.Data([tra_max_abs, tra_max_pro, tra_prom, tra_min_abs, tra_min_pro])
            else:
                data = go.Data([tra_max_pro, tra_prom, tra_min_pro])
        layout = go.Layout(
            title=variable.var_nombre + " " + str(titulo_frecuencia(frecuencia)) + " " + estacion.est_codigo,
            yaxis=dict(title=variable.var_nombre + " (" + variable.uni_id.uni_sigla + ")"),
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
                sql += 'med_estado is not False and '
                sql += 'med_fecha>=\'' + str(fecha_inicio) + '\' order by med_fecha'
            elif str(year) == year_fin:
                sql = 'SELECT * FROM ' + tabla + ' WHERE '
                sql += 'est_id_id=' + str(estacion.est_id) + ' and '
                sql += 'med_estado is not False and '
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
        frecuencia.append(fila.med_fecha)
    return valor, maximo, minimo, frecuencia


def datos_5minutos(estacion, variable, fecha_inicio, fecha_fin):
    datos = armar_consulta(estacion, variable, 1, fecha_inicio, fecha_fin)
    valor = []
    maximo_abs = []
    maximo_pro = []
    minimo_abs = []
    minimo_pro = []
    frecuencia = []
    intervalo = timedelta(minutes=5)
    fecha = datetime.combine(fecha_inicio, datetime.min.time())
    int_5minutos = ((fecha_fin - fecha_inicio).days + 1) * 288
    num_datos = len(datos)
    item = 0
    for dia in range(int_5minutos):
        if item < num_datos:
            fecha_datos = datos[item].get('fecha')
            if fecha_datos == fecha:
                valor.append(datos[item].get('valor'))
                maximo_abs.append(datos[item].get('max_abs'))
                maximo_pro.append(datos[item].get('max_pro'))
                minimo_abs.append(datos[item].get('min_abs'))
                minimo_pro.append(datos[item].get('min_pro'))
                item += 1
            else:
                valor.append(None)
                maximo_abs.append(None)
                maximo_pro.append(None)
                minimo_abs.append(None)
                minimo_pro.append(None)
            frecuencia.append(fecha)
            fecha += intervalo

    return valor, maximo_abs, maximo_pro, minimo_abs, minimo_pro, frecuencia


def datos_horarios(estacion, variable, fecha_inicio, fecha_fin):
    datos = armar_consulta(estacion,variable,2,fecha_inicio,fecha_fin)
    valor = []
    maximos_abs = []
    maximos_pro = []
    minimos_abs = []
    minimos_pro = []
    frecuencia = []
    intervalo = timedelta(hours=1)
    fecha = datetime.combine(fecha_inicio, datetime.min.time())
    int_horas = ((fecha_fin - fecha_inicio).days + 1) * 24
    num_datos = len(datos)
    item = 0
    for dia in range(int_horas):
        if item < num_datos:
            fecha_datos = datos[item].get('fecha')
            if fecha_datos == fecha:
                valor.append(datos[item].get('valor'))
                maximos_abs.append(datos[item].get('max_abs'))
                maximos_pro.append(datos[item].get('max_pro'))
                minimos_abs.append(datos[item].get('min_abs'))
                minimos_pro.append(datos[item].get('min_pro'))
                item += 1
            else:
                valor.append(None)
                maximos_abs.append(None)
                maximos_pro.append(None)
                minimos_abs.append(None)
                minimos_pro.append(None)
            frecuencia.append(fecha)
            fecha += intervalo
    return valor, maximos_abs, maximos_pro, minimos_abs, minimos_pro, frecuencia


def datos_diarios(estacion, variable, fecha_inicio, fecha_fin):
    datos = armar_consulta(estacion,variable,3,fecha_inicio,fecha_fin)
    valor = []
    # maximos absolutos
    maximos_abs = []
    maximos_pro = []
    minimos_abs = []
    minimos_pro = []
    frecuencia = []
    intervalo = timedelta(days=1)
    fecha = fecha_inicio
    int_dias = (fecha_fin - fecha_inicio).days + 1
    num_datos = len(datos)
    item = 0
    for dia in range(int_dias):
        if item < num_datos:
            fecha_datos = datos[item].get('fecha').date()
            if fecha_datos == fecha:
                valor.append(datos[item].get('valor'))
                maximos_abs.append(datos[item].get('max_abs'))
                maximos_pro.append(datos[item].get('max_pro'))
                minimos_abs.append(datos[item].get('min_abs'))
                minimos_pro.append(datos[item].get('min_pro'))
                item += 1
            else:
                valor.append(None)
                maximos_abs.append(None)
                maximos_pro.append(None)
                minimos_abs.append(None)
                minimos_pro.append(None)
            frecuencia.append(fecha)
            fecha += intervalo
    return valor, maximos_abs,maximos_pro, minimos_abs, minimos_pro, frecuencia


def datos_mensuales(estacion, variable, fecha_inicio, fecha_fin):
    datos = armar_consulta(estacion, variable, 4, fecha_inicio, fecha_fin)
    valor = []
    maximo_abs = []
    maximo_pro = []
    minimo_abs = []
    minimo_pro = []
    frecuencia = []
    fecha = fecha_inicio.replace(day=1)
    intervalo = timedelta(days=30)
    dias = float((fecha_fin - fecha_inicio).days)
    meses = int(ceil(dias / 30))
    num_datos = len(datos)
    item = 0
    for mes in range(meses):
        if item < num_datos:
            fecha_datos = datos[item].get('fecha').date()
            if fecha == fecha_datos:
                valor.append(datos[item].get('valor'))
                maximo_abs.append(datos[item].get('max_abs'))
                maximo_pro.append(datos[item].get('max_pro'))
                minimo_abs.append(datos[item].get('min_abs'))
                minimo_pro.append(datos[item].get('min_pro'))
                item += 1
            else:
                valor.append(None)
                maximo_abs.append(None)
                maximo_pro.append(None)
                minimo_abs.append(None)
                minimo_pro.append(None)
            frecuencia.append(fecha)
            intervalo = dias_mes(fecha.month, fecha.year)
            fecha += timedelta(days=intervalo)

    return valor, maximo_abs, maximo_pro, minimo_abs, minimo_pro, frecuencia


def armar_consulta(estacion, variable, frecuencia, fecha_inicio, fecha_fin):
    year_ini = fecha_inicio.strftime('%Y')
    year_fin = fecha_fin.strftime('%Y')
    var_cod = variable.var_codigo
    cursor = connection.cursor()
    datos = []
    filtro_completo = 'est_id_id=' + str(estacion.est_id) + ' and med_fecha>=\'' + str(fecha_inicio) + '\' and '
    filtro_completo += 'med_fecha<=\'' + str(fecha_fin) + '\' and med_estado is not False '
    filtro_mayor = 'est_id_id=' + str(estacion.est_id) + ' and med_fecha>=\'' + str(fecha_inicio) + '\' and '
    filtro_mayor += 'med_estado is not False '
    filtro_menor = 'est_id_id=' + str(estacion.est_id) + ' and '
    filtro_menor += 'med_fecha<=\'' + str(fecha_fin) + '\' and med_estado is not False '
    filtro_simple = 'est_id_id=' + str(estacion.est_id) + ' and med_estado is not False '
    if frecuencia == 1:
        fecha = 'to_timestamp(floor((extract(\'epoch\' '
        fecha += 'from med_fecha) / 300 )) * 300)'
        fecha += 'AT TIME ZONE \'UTC5\' as fecha, '
    elif frecuencia == 2:
        fecha = 'date_trunc(\'hour\',med_fecha) as fecha, '
    elif frecuencia == 3:
        fecha = 'date_trunc(\'day\',med_fecha) as fecha, '
    elif frecuencia == 4:
        fecha = 'date_trunc(\'month\',med_fecha) as fecha, '
    if year_ini == year_fin:
        tabla = var_cod + '.m' + year_ini
        if variable.var_id == 1:
            sql = 'SELECT ' + fecha + suma
            sql += 'FROM ' + tabla + ' WHERE '
            sql += filtro_completo + group_order
        else:
            sql = 'SELECT ' + fecha
            sql += promedio + coma + max_abs + coma + max_pro + coma + min_abs + coma + min_pro
            sql += 'FROM ' + tabla + ' WHERE '
            sql += filtro_completo + group_order
        cursor.execute(sql)
        datos = dictfetchall(cursor)
    else:
        range_year = range(int(year_ini), int(year_fin) + 1)
        for year in range_year:
            tabla = var_cod + '.m' + str(year)
            if str(year) == year_ini:
                if variable.var_id == 1:
                    sql = 'SELECT ' + fecha + suma
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += filtro_mayor + group_order
                else:
                    sql = 'SELECT ' + fecha
                    sql += promedio + coma + max_abs + coma + max_pro + coma + min_abs + coma + min_pro
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += filtro_mayor + group_order
            elif str(year) == year_fin:
                if variable.var_id == 1:
                    sql = 'SELECT ' + fecha + suma
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += filtro_menor + group_order
                else:
                    sql = 'SELECT ' + fecha
                    sql += promedio + coma + max_abs + coma + max_pro + coma + min_abs + coma + min_pro
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += filtro_menor + group_order
            else:
                if variable.var_id == 1:
                    sql = 'SELECT ' + fecha + suma
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += filtro_simple + group_order
                else:
                    sql = 'SELECT ' + fecha
                    sql += promedio + coma + max_abs + coma + max_pro + coma + min_abs + coma + min_pro
                    sql += 'FROM ' + tabla + ' WHERE '
                    sql += filtro_simple + group_order
            cursor.execute(sql)
            datos.extend(dictfetchall(cursor))
    cursor.close()
    return datos


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
    fecha_ini = datetime.strptime(fec_ini, '%Y-%m-%d %H:%M:%S')
    fecha_fin = datetime.strptime(fec_fin, '%Y-%m-%d %H:%M:%S')
    datos = []
    estacion = Estacion.objects.get(est_id=est_id)
    variable = Variable.objects.get(var_id=var_id)
    val, max_abs, max_pro, min_abs, min_pro, time = \
        datos_horarios(estacion, variable, fecha_ini, fecha_fin)
    if len(val) > 0:
        for item_val, item_max_abs, item_max_pro, item_min_abs, item_min_pro, item_time \
                in zip(val, max_abs, max_pro, min_abs, min_pro, time):
            if item_time>=fecha_ini and item_time<=fecha_fin:
                dato = {
                    'fecha': item_time,
                    'valor': item_val,
                    'maximo_absoluto': item_max_abs,
                    'minimo_absolulo': item_min_abs,
                    'maximo_promedio': item_max_pro,
                    'minimo_promedio': item_min_pro,
                }
                datos.append(dato)
    else:
        datos = {
            'mensaje': 'no hay datos'
        }
    return datos
