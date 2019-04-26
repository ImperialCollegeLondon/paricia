# -*- coding: utf-8 -*-

from reportes.typeI import TypeI
from reportes.typeII import TypeII
from reportes.typeIII import TypeIII
from reportes.typeIV import TypeIV
from reportes.typeV import TypeV
from reportes.typeVI import TypeVI
from cruce.models import Cruce
from reportes.consultas.functions import datos_instantaneos

from datetime import timedelta, datetime, date
import plotly.offline as opy

import plotly.graph_objs as go

import requests
from plotly import tools
import json


from .consultas.functions import (datos_diarios, datos_5minutos, datos_horarios, datos_mensuales)


def consultar_datos(form):
    estacion = form.cleaned_data['estacion']
    variable = form.cleaned_data['variable']
    fecha_inicio = form.cleaned_data['inicio']
    fecha_fin = form.cleaned_data['fin']
    frecuencia = form.cleaned_data['frecuencia']
    if fecha_inicio is None:
        fecha_inicio = estacion.est_fecha_inicio
    if fecha_fin is None:
        fecha_fin = date.today()
    if frecuencia == str(0):
        valores, maximos_abs, minimos_abs, tiempo = datos_instantaneos(estacion, variable, fecha_inicio, fecha_fin)
        maximos_pro = []
        minimos_pro = []
    elif frecuencia == str(1):
        valores, maximos_abs, maximos_pro, minimos_abs, minimos_pro, tiempo = datos_5minutos(estacion, variable, fecha_inicio, fecha_fin)
    # frecuencia horaria
    elif frecuencia == str(2):
        valores, maximos_abs, maximos_pro, minimos_abs, minimos_pro, tiempo = datos_horarios(estacion, variable, fecha_inicio, fecha_fin)
    # frecuencia diaria
    elif frecuencia == str(3):
        valores, maximos_abs, maximos_pro, minimos_abs, minimos_pro, tiempo = datos_diarios(estacion, variable, fecha_inicio, fecha_fin)
        # frecuencia mensual
    elif frecuencia == str(4):
        valores, maximos_abs, maximos_pro, minimos_abs, minimos_pro, tiempo = datos_mensuales(estacion, variable,fecha_inicio, fecha_fin)
    print(len(valores))

    if frecuencia == str(0):
        data_valor = get_trace_minimo(tiempo, valores, 'Valor', '#1660A7')
        data_maximo = get_elemento_data(variable, tiempo, maximos_abs, 'Maximo', '#32CD32')
        data_minimo = get_elemento_data(variable, tiempo, minimos_abs, 'Minimo', '#CD0C18')
    else:
        data_valor = get_elemento_data(variable, tiempo, valores, 'Promedio', '#1660A7')
        if maximos_abs.count(None) <= maximos_pro.count(None):
            data_maximo = get_elemento_data(variable, tiempo, maximos_abs, 'Maximo Absoluto', '#32CD32')
        else:
            data_maximo = get_elemento_data(variable, tiempo, maximos_pro, 'Maximo Promedio', '#90EE90')
        if minimos_abs.count(None) <= minimos_pro.count(None):
            data_minimo = get_elemento_data(variable, tiempo, minimos_abs, 'Minimo Absoluto', '#CD0C18')
        else:
            data_minimo = get_elemento_data(variable, tiempo, minimos_pro, 'Minimo Promedio', '#FF8C00')
    boton_dia = dict(count=1,
                     label='1dia',
                     step='day',
                     stepmode='backward')
    boton_mes = dict(count=1,
                     label='1mes',
                     step='month',
                     stepmode='backward')
    boton_6meses = dict(count=6,
                        label='6meses',
                        step='month',
                        stepmode='backward')
    boton_all = dict(step='all')
    botones = list()
    if frecuencia == str(0) or frecuencia == str(1) or frecuencia == str(2):
        botones.append(boton_dia)
    botones.append(boton_mes)
    if frecuencia == str(3) or frecuencia == str(4):
        botones.append(boton_6meses)
    botones.append(boton_all)

    titulo_grafico = variable.var_nombre + " " + str(titulo_frecuencia(frecuencia)) + " " + estacion.est_codigo
    layout = {
        'title': titulo_grafico,
        'yaxis': dict(title=variable.var_nombre + " (" + variable.uni_id.uni_sigla + ")"),
        'xaxis': dict(

            range=list([fecha_inicio, fecha_fin]),
            rangeselector=dict(
                buttons=botones
            ),
            rangeslider={'range': [fecha_inicio, fecha_fin]},
            type='date',

        )

    }

    if frecuencia == str(0):
        data = go.Data([data_valor])
    else:
        if variable.var_id != 1:
            '''grafico = {
                'data': [
                    data_valor,
                    data_maximo,
                    data_minimo
                ],
                'layout': layout
    
            }'''
            data = go.Data([data_valor,data_maximo,data_minimo])
        else:

            '''grafico = {
                'data': [
                    data_valor
                ],
                'layout': layout
            }'''

            data = go.Data([data_valor])

    figure = go.Figure(data=data, layout=layout)

    div = opy.plot(figure, auto_open=False, output_type='div', include_plotlyjs=False)

    grafico = dict(grafico=div)

    return grafico


def get_elemento_data(variable, tiempo, valor, nombre, color):
    '''type_graph = 'scatter'
    if variable.var_id == 1:
        type_graph = 'bar'
    elemento = {
        'type': type_graph,
        'x': tiempo,
        'y': valor,
        'name': nombre,
        'line': {
            'color': color,
        },
    }'''
    if variable.var_id == 1:
        elemento = go.Bar(
            x=tiempo,
            y=valor,
            name=nombre
        )
    else:
        elemento = go.Scattergl(
            x=tiempo,
            y=valor,
            name=nombre,
            mode='lines',
            line=dict(
                color=color,

            )
        )

    return elemento


def get_trace_minimo(tiempo, valor, nombre, color):
    elemento = go.Scattergl(
        x=tiempo,
        y=valor,
        name=nombre,
        mode='lines',
        marker=dict(
            color=color,
            line=dict(
                width=1,
                color='rgb(0,0,0)')
        )
    )
    return elemento


def get_trace(variable, tiempo, valor, nombre):
    type_graph = 'scatter'
    if variable.var_id == 1:
        type_graph = 'bar'
        elemento = dict(
            type=type_graph,
            x=tiempo,
            y=valor,
            name=nombre,
            # yaxis='y2',
            # xaxis='x2',
            marker=dict(color="#1660A7")
        )
    else:
        elemento = dict(
            type=type_graph,
            x=tiempo,
            y=valor,
            name=nombre,
            line=dict(color="#ff881e"),
            yaxis='y2',
            xaxis='x',

        )
    return elemento


def filtrar(form):
    context = {}
    # humedadsuelo,presionatmosferica,temperaturaagua,caudal,nivelagua
    typeI = [6, 8, 9, 10, 11]
    # precipitacion
    typeII = [1]
    # temperaturaaire
    typeIII = [2]
    # humedadaire
    typeIV = [3]
    # direccion y velocidad
    typeV = [4, 5]
    # radiacion
    typeVI = [7]
    variables = list(Cruce.objects
                     .filter(est_id=form.cleaned_data['estacion'])
                     .values('var_id')
                     )
    obj_typeI = TypeI()
    obj_typeII = TypeII()
    obj_typeIII = TypeIII()
    obj_typeIV = TypeIV()
    obj_typeV = TypeV()
    obj_typeVI = TypeVI()
    estacion = form.cleaned_data['estacion']
    periodo = form.cleaned_data['anio']

    for item in variables:
        if item.get('var_id') in typeI:
            matriz = obj_typeI.matriz(form.cleaned_data['estacion'], item.get('var_id'), form.cleaned_data['anio'])
            grafico = obj_typeI.grafico(form.cleaned_data['estacion'], item.get('var_id'), form.cleaned_data['anio'])
        elif item.get('var_id') in typeII:
            matriz = obj_typeII.matriz(estacion, periodo)
            grafico = obj_typeII.grafico(estacion, item.get('var_id'), periodo)
        elif item.get('var_id') in typeIII:
            matriz = obj_typeIII.matriz(form.cleaned_data['estacion'], item.get('var_id'), form.cleaned_data['anio'])
            grafico = obj_typeIII.grafico(form.cleaned_data['estacion'], item.get('var_id'), form.cleaned_data['anio'])
        elif item.get('var_id') in typeIV:
            matriz = obj_typeIV.matriz(form.cleaned_data['estacion'], item.get('var_id'), form.cleaned_data['anio'])
            grafico = obj_typeIV.grafico(form.cleaned_data['estacion'], item.get('var_id'), form.cleaned_data['anio'])
        elif item.get('var_id') in typeV:
            matriz = obj_typeV.matriz(form.cleaned_data['estacion'], item.get('var_id_id'), form.cleaned_data['anio'])
        elif item.get('var_id') in typeVI:
            matriz = obj_typeVI.matriz(form.cleaned_data['estacion'], str(item.get('var_id')),form.cleaned_data['anio'])
        if len(matriz) > 0:
            context.update({str(item.get('var_id')) + '_matriz': matriz})
        if grafico:
            context.update({str(item.get('var_id')) + '_grafico': grafico})
    if len(context) == 0:
        context.update({'mensaje':'No existen datos para la consulta'})
    return context


def comparar(form):
    estacion01 = form.cleaned_data['estacion01']
    estacion02 = form.cleaned_data['estacion02']
    estacion03 = form.cleaned_data['estacion03']
    variable = form.cleaned_data['variable']
    fecha_inicio = form.cleaned_data['inicio']
    fecha_fin = form.cleaned_data['fin']
    frecuencia = form.cleaned_data['frecuencia']
    # frecuencia 5 minutos
    if (frecuencia == str(1)):
        val01, max01, max_pro01, min01, min_pro01, time01 = datos_5minutos(estacion01, variable, fecha_inicio, fecha_fin)
        val02, max02, max_pro02, min02, min_pro02, time02 = datos_5minutos(estacion02, variable, fecha_inicio, fecha_fin)
        val03, max03, max_pro03, min03, min_pro03, time03 = datos_5minutos(estacion03, variable, fecha_inicio, fecha_fin)
    # frecuencia horaria
    elif (frecuencia == str(2)):
        val01, max01, max_pro01, min01, min_pro01, time01 = datos_horarios(estacion01, variable, fecha_inicio, fecha_fin)
        val02, max02, max_pro02, min02, min_pro02, time02 = datos_horarios(estacion02, variable, fecha_inicio, fecha_fin)
        val03, max03, max_pro03, min03, min_pro03, time03 = datos_horarios(estacion03, variable, fecha_inicio, fecha_fin)
    # frecuencia diaria
    elif (frecuencia == str(3)):
        val01, max01, max_pro01, min01, min_pro01, time01 = datos_diarios(estacion01, variable, fecha_inicio, fecha_fin)
        val02, max02, max_pro02, min02, min_pro02, time02 = datos_diarios(estacion02, variable, fecha_inicio, fecha_fin)
        val03, max03, max_pro03, min03, min_pro03, time03 = datos_diarios(estacion03, variable, fecha_inicio, fecha_fin)
    # frecuencia mensual
    elif (frecuencia == str(4)):
        val01, max01, max_pro01, min01, min_pro01, time01 = datos_mensuales(estacion01, variable, fecha_inicio, fecha_fin)
        val02, max02, max_pro02, min02, min_pro02, time02 = datos_mensuales(estacion02, variable, fecha_inicio, fecha_fin)
        val03, max03, max_pro03, min03, min_pro03, time03 = datos_mensuales(estacion03, variable, fecha_inicio, fecha_fin)
    trace0 = trace_graph(variable, estacion01, time01, val01)
    trace1 = trace_graph(variable, estacion02, time02, val02)
    trace2 = trace_graph(variable, estacion03, time03, val03)
    data = go.Data([trace0, trace1, trace2])
    layout = go.Layout(
        title="Comparación de Estaciones",
        yaxis=dict(title=variable.var_nombre + \
                         str(" (") + variable.uni_id.uni_sigla + str(")")),
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1d',
                         step='day',
                         stepmode='today'),
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


# funcion para comparar dos variables entre dos estaciones
def comparar_variables(form):
    estacion01 = form.cleaned_data['estacion01']
    estacion02 = form.cleaned_data['estacion02']
    variable01 = form.cleaned_data['variable01']
    variable02 = form.cleaned_data['variable02']
    fecha_inicio = form.cleaned_data['inicio']
    fecha_fin = form.cleaned_data['fin']
    frecuencia = form.cleaned_data['frecuencia']
    parametro = form.cleaned_data['parametro']
    if (frecuencia == str(1)):
        val01, max01, max_pro01, min01, min_pro01, time01 = datos_5minutos(estacion01, variable01, fecha_inicio,
                                                                           fecha_fin)
        val02, max02, max_pro02, min02, min_pro02, time02 = datos_5minutos(estacion02, variable02, fecha_inicio,
                                                                           fecha_fin)
    # frecuencia horaria
    elif (frecuencia == str(2)):
        val01, max01, max_pro01, min01, min_pro01, time01 = datos_horarios(estacion01, variable01, fecha_inicio,
                                                                           fecha_fin)
        val02, max02, max_pro02, min02, min_pro02, time02 = datos_horarios(estacion02, variable02, fecha_inicio,
                                                                           fecha_fin)
    # frecuencia diaria
    elif (frecuencia == str(3)):
        val01, max01, max_pro01, min01, min_pro01, time01 = datos_diarios(estacion01, variable01, fecha_inicio,
                                                                          fecha_fin)
        val02, max02, max_pro02, min02, min_pro02, time02 = datos_diarios(estacion02, variable02, fecha_inicio,
                                                                          fecha_fin)
    # frecuencia mensual
    elif (frecuencia == str(4)):
        val01, max01, max_pro01, min01, min_pro01, time01 = datos_mensuales(estacion01, variable01, fecha_inicio,
                                                                            fecha_fin)
        val02, max02, max_pro02, min02, min_pro02, time02 = datos_mensuales(estacion02, variable02, fecha_inicio,
                                                                            fecha_fin)

    # trace01 = get_trace(variable01, time01, val01, variable01.var_nombre)
    trace02 = get_trace(variable02, time02, val02, variable02.var_nombre)
    if parametro == str(1):
        trace01 = get_trace(variable01, time01, val01, variable01.var_nombre)
    elif parametro == str(2):
        if max01.count(None) <= max_pro01.count(None):
            trace01 = get_trace(variable01, time01, max01, variable01.var_nombre)
        else:
            trace01 = get_trace(variable01, time01, max_pro01, variable01.var_nombre)
    else:
        if min01.count(None) <= min_pro01.count(None):
            trace01 = get_trace(variable01, time01, min01, variable01.var_nombre)
        else:
            trace01 = get_trace(variable01, time01, min_pro01, variable01.var_nombre)
    print(parametro, type(parametro))

    titulo_grafico = "Comparacion Variables"

    '''layout = dict(
        title=titulo_grafico,
        yaxis=dict(
            title=variable01.var_nombre + str(" (") + variable01.uni_id.uni_sigla + str(")"),
        ),
        yaxis2=dict(
            title=variable02.var_nombre + str(" (") + variable02.uni_id.uni_sigla + str(")"),
            titlefont=dict(
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            ),
            overlaying='y',
            side='right',
            autorange='reversed'

        ),
        xaxis=dict(
            # rangeslider={},
            # type='date',
        ),
        height=500
        

    )'''
    layout = dict(
        title=titulo_grafico,
        yaxis=dict(
            title=variable01.var_nombre + str(" (") + variable01.uni_id.uni_sigla + str(")"),
            autorange='reversed',
            overlaying='y',
            side='right',
        ),
        yaxis2=dict(
            title=variable02.var_nombre + str(" (") + variable02.uni_id.uni_sigla + str(")"),

        ),
        xaxis=dict(
            rangeslider={},
            type='date',
        ),
        grid=dict(rows=2, columns=1),
        legend=dict(yanchor='bottom')

    )
    data = list([trace01, trace02])
    grafico = dict(
        data=data,
        layout=layout,

    )
    return grafico


# funcion para procesar los datos del web service del INAMHI
def procesar_json_inamhi(form):
    estacion = form.cleaned_data['estacion']
    parametro = form.cleaned_data['parametro']
    frecuencia = form.cleaned_data['frecuencia']
    inicio = form.cleaned_data['inicio']
    fin = form.cleaned_data['fin']

    fecha_inicio = datetime(inicio.year, inicio.month, inicio.day, 0, 0, 0)
    fecha_fin = datetime(fin.year, fin.month, fin.day, 23, 59, 59, 999999)
    # formato url web service INAMHI
    url_base = 'http://186.42.174.236:8090/'
    url_base += frecuencia + '/'
    url_base += str(estacion.identificador) + '/'
    url_base += fecha_inicio.strftime("%Y-%m-%d %H:%M:%S") + '/'
    url_base += fecha_fin.strftime("%Y-%m-%d %H:%M:%S") + '/'
    url_base += estacion.transmision + '/'
    url_base += parametro.parametro
    # url_base += '171481m'
    # obtener respuesta del web service
    response = requests.get(url_base, auth=('FONAG', 'fOnAg2018'))
    data = response.json()
    tiempo = []
    valores = []
    if len(data) > 0:
        # print(data)
        for item in data:
            fecha = datetime.strptime(item['fechaTomaDelDato'], '%Y-%m-%d %H:%M:%S')
            tiempo.append(fecha)
            if len(item['dataJSON']) > 0:
                # print(item['dataJSON'][0]['valor'], type(item['dataJSON'][0]['valor']))
                valores.append(item['dataJSON'][0]['valor'])
            else:
                valores.append(None)
        if valores.count(None) == len(data):
            mensaje = dict(mensaje='No existen datos para la consulta')
            return mensaje
        titulo = parametro.nombre + " " + estacion.codigo + " " + estacion.nombre
        titulo_yaxis = parametro.nombre + " (" + parametro.estadistico + ")"

        layout = get_layout_grafico(titulo, titulo_yaxis, fecha_inicio, fecha_fin)

        trace_valor = get_trace_minimo(tiempo, valores, 'Valor', '#1660A7')
        data = get_data_graph(trace_valor)
        grafico = get_grafico(layout, data)

        return grafico
    else:
        mensaje = dict(mensaje='No existen datos para la consulta. Intente cambiando la frecuencia')
        return mensaje


def trace_graph(variable, estacion, tiempo, valor):
    if variable.var_id == 1:
        trace = go.Bar(
            x=tiempo,
            y=valor,
            name=estacion.est_codigo,

        )
    else:
        trace = go.Scatter(
            x=tiempo,
            y=valor,
            name=estacion.est_codigo,
            mode='lines',
            #yaxis='y2'
        )
    return trace


def get_grafico(layout, data):
    figure = go.Figure(data=data, layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div', include_plotlyjs=False)
    grafico = dict(grafico=div)
    return grafico


def get_layout_grafico(titulo,titulo_yaxis, fecha_inicio, fecha_fin):
    boton_dia = dict(count=1,
                     label='1dia',
                     step='day',
                     stepmode='backward')
    boton_mes = dict(count=1,
                     label='1mes',
                     step='month',
                     stepmode='backward')
    boton_6meses = dict(count=6,
                        label='6meses',
                        step='month',
                        stepmode='backward')
    boton_all = dict(step='all')
    botones = list()

    botones.append(boton_dia)
    botones.append(boton_all)

    layout = {
        'title': titulo,
        'yaxis': dict(title=titulo_yaxis),
        'xaxis': dict(
            range=list([fecha_inicio, fecha_fin]),
            rangeselector=dict(
                buttons=botones
            ),
            rangeslider={'range': [fecha_inicio, fecha_fin]},
            type='date',

        )

    }
    return layout


def get_data_graph(trace_valor, trace_maximo=None, trace_minimo=None):

    if trace_maximo is None or trace_minimo is None:
        data = go.Data([trace_valor])
    else:
        data = go.Data([trace_valor, trace_maximo, trace_minimo])

    return data


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


