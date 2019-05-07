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
    # frecuencia minima
    if frecuencia == str(0):
        informacion = datos_instantaneos(estacion, variable, fecha_inicio, fecha_fin)
    # frecuencia de 5 minutos
    elif frecuencia == str(1):
        informacion = datos_5minutos(estacion, variable, fecha_inicio, fecha_fin)
    # frecuencia horaria
    elif frecuencia == str(2):
        informacion = datos_horarios(estacion, variable, fecha_inicio, fecha_fin)
    # frecuencia diaria
    elif frecuencia == str(3):
        informacion = datos_diarios(estacion, variable, fecha_inicio, fecha_fin)
        # frecuencia mensual
    elif frecuencia == str(4):
        informacion = datos_mensuales(estacion, variable,fecha_inicio, fecha_fin)
    tiempo = informacion["tiempo"]
    valor = informacion["valor"]
    max_abs = informacion["max_abs"]
    min_abs = informacion["min_abs"]
    max_pro = informacion["max_pro"]
    min_pro = informacion["min_pro"]
    if len(valor) > 0 and valor.count(None) != len(tiempo):

        if frecuencia == str(0):
            data_valor = get_trace_minimo(tiempo, valor, 'Valor', '#1660A7')
            data_maximo = get_elemento_data(variable, tiempo, max_abs, 'Maximo', '#32CD32')
            data_minimo = get_elemento_data(variable, tiempo, min_abs, 'Minimo', '#CD0C18')
        else:
            data_valor = get_elemento_data(variable, tiempo, valor, 'Promedio', '#1660A7')
            if max_abs.count(None) <= max_pro.count(None):
                data_maximo = get_elemento_data(variable, tiempo, max_abs, 'Maximo Absoluto', '#32CD32')
            else:
                data_maximo = get_elemento_data(variable, tiempo, max_pro, 'Maximo Promedio', '#90EE90')
            if min_abs.count(None) <= min_pro.count(None):
                data_minimo = get_elemento_data(variable, tiempo, min_abs, 'Minimo Absoluto', '#CD0C18')
            else:
                data_minimo = get_elemento_data(variable, tiempo, min_pro, 'Minimo Promedio', '#FF8C00')

        titulo_grafico = variable.var_nombre + " " + str(titulo_frecuencia(frecuencia)) + " " + estacion.est_codigo
        titulo_yaxis = variable.var_nombre + " (" + variable.uni_id.uni_sigla + ")"
        layout = get_layout_grafico(titulo_grafico, titulo_yaxis, fecha_inicio, fecha_fin)

        if frecuencia == str(0) or variable.var_id == 1:
            data = get_data_graph(data_valor)
        else:
            data = get_data_graph(data_valor, data_maximo, data_minimo)

        figure = go.Figure(data=data, layout=layout)

        div = opy.plot(figure, auto_open=False, output_type='div', include_plotlyjs=False)

        grafico = dict(grafico=div)

    else:
        grafico = dict(mensaje="No existe informacion para la consulta")
    return grafico


# funcion para consultar datos pra usuarios
def consultar_datos_usuario(form):
    estacion = form.cleaned_data['estacion']
    variable = form.cleaned_data['variable']
    fecha_inicio = form.cleaned_data['inicio']
    fecha_fin = form.cleaned_data['fin']
    frecuencia = form.cleaned_data['frecuencia']
    if fecha_inicio is None:
        fecha_inicio = estacion.est_fecha_inicio
    if fecha_fin is None:
        fecha_fin = date.today()

    if frecuencia == str(1):
        informacion = datos_horarios(estacion, variable, fecha_inicio, fecha_fin)
        # frecuencia diaria
    elif frecuencia == str(2):
        informacion = datos_diarios(estacion, variable, fecha_inicio, fecha_fin)
        # frecuencia mensual
    elif frecuencia == str(3):
        informacion = datos_mensuales(estacion, variable, fecha_inicio, fecha_fin)
    tiempo = informacion["tiempo"]
    valor = informacion["valor"]
    max_abs = informacion["max_abs"]
    min_abs = informacion["min_abs"]
    max_pro = informacion["max_pro"]
    min_pro = informacion["min_pro"]

    data_valor = get_elemento_data_json(variable, tiempo, valor, 'Promedio', '#1660A7')
    if max_abs.count(None) <= max_pro.count(None):
        data_maximo = get_elemento_data_json(variable, tiempo, max_abs, 'Maximo Absoluto', '#32CD32')
    else:
        data_maximo = get_elemento_data_json(variable, tiempo, max_pro, 'Maximo Promedio', '#90EE90')
    if min_abs.count(None) <= min_pro.count(None):
        data_minimo = get_elemento_data_json(variable, tiempo, min_abs, 'Minimo Absoluto', '#CD0C18')
    else:
        data_minimo = get_elemento_data_json(variable, tiempo, min_pro, 'Minimo Promedio', '#FF8C00')

    titulo_grafico = variable.var_nombre + " " + str(titulo_frecuencia(frecuencia)) + " " + estacion.est_codigo
    titulo_yaxis = variable.var_nombre + " (" + variable.uni_id.uni_sigla + ")"
    layout = get_layout_grafico(titulo_grafico, titulo_yaxis, fecha_inicio, fecha_fin)
    if variable.var_id != 1:
        grafico = {
            'data': [
                data_valor,
                data_maximo,
                data_minimo
            ],
            'layout': layout

        }
    else:
        grafico = {
            'data': [
                data_valor
            ],
            'layout': layout
        }
    return grafico


# graficar valores a la minima frecuencia
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


# trazo para la comparación de variables
def get_trace(variable, tiempo, valor, nombre):
    type_graph = 'scatter'
    if variable.var_id == 1:
        type_graph = 'bar'
        elemento = dict(
            type=type_graph,
            x=tiempo,
            y=valor,
            name=nombre,
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


# comparar tres estaciones en la misma vaiable
def comparar(form):
    estacion01 = form.cleaned_data['estacion01']
    estacion02 = form.cleaned_data['estacion02']
    estacion03 = form.cleaned_data['estacion03']
    variable = form.cleaned_data['variable']
    fecha_inicio = form.cleaned_data['inicio']
    fecha_fin = form.cleaned_data['fin']
    frecuencia = form.cleaned_data['frecuencia']
    # frecuencia 5 minutos
    if frecuencia == str(1):
        info_esta01 = datos_5minutos(estacion01, variable, fecha_inicio, fecha_fin)
        info_esta02 = datos_5minutos(estacion02, variable, fecha_inicio, fecha_fin)
        info_esta03 = datos_5minutos(estacion03, variable, fecha_inicio, fecha_fin)
    # frecuencia horaria
    elif frecuencia == str(2):
        info_esta01 = datos_horarios(estacion01, variable, fecha_inicio, fecha_fin)
        info_esta02 = datos_horarios(estacion02, variable, fecha_inicio, fecha_fin)
        info_esta03 = datos_horarios(estacion03, variable, fecha_inicio, fecha_fin)
    # frecuencia diaria
    elif frecuencia == str(3):
        info_esta01 = datos_diarios(estacion01, variable, fecha_inicio, fecha_fin)
        info_esta02 = datos_diarios(estacion02, variable, fecha_inicio, fecha_fin)
        info_esta03 = datos_diarios(estacion03, variable, fecha_inicio, fecha_fin)
    # frecuencia mensual
    elif frecuencia == str(4):
        info_esta01 = datos_mensuales(estacion01, variable, fecha_inicio, fecha_fin)
        info_esta02 = datos_mensuales(estacion02, variable, fecha_inicio, fecha_fin)
        info_esta01 = datos_mensuales(estacion03, variable, fecha_inicio, fecha_fin)
    time01 = info_esta01["tiempo"]
    time02 = info_esta02["tiempo"]
    time03 = info_esta03["tiempo"]
    val01 = info_esta01["valor"]
    val02 = info_esta02["valor"]
    val03 = info_esta03["valor"]
    trace0 = get_elemento_data(variable, time01, val01, estacion01.est_codigo)
    trace1 = get_elemento_data(variable, time02, val02, estacion02.est_codigo)
    trace2 = get_elemento_data(variable, time03, val03, estacion03.est_codigo)

    titulo = "Comparación de Estaciones"
    titulo_yaxis = variable.var_nombre + str(" (") + variable.uni_id.uni_sigla + str(")")
    layout = get_layout_grafico(titulo, titulo_yaxis, fecha_inicio, fecha_fin)
    data = get_data_graph(trace0, trace1, trace2)
    grafico = get_grafico(layout, data)
    return grafico


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
    if frecuencia == str(1):
        info_est01 = datos_5minutos(estacion01, variable01, fecha_inicio, fecha_fin)
        info_est02 = datos_5minutos(estacion02, variable02, fecha_inicio, fecha_fin)
    # frecuencia horaria
    elif frecuencia == str(2):
        info_est01 = datos_horarios(estacion01, variable01, fecha_inicio, fecha_fin)
        info_est02 = datos_horarios(estacion02, variable02, fecha_inicio, fecha_fin)
    # frecuencia diaria
    elif frecuencia == str(3):
        info_est01 = datos_diarios(estacion01, variable01, fecha_inicio, fecha_fin)
        info_est02 = datos_diarios(estacion02, variable02, fecha_inicio, fecha_fin)
    # frecuencia mensual
    elif frecuencia == str(4):
        info_est01 = datos_mensuales(estacion01, variable01, fecha_inicio, fecha_fin)
        info_est02 = datos_mensuales(estacion02, variable02, fecha_inicio, fecha_fin)

    time01 = info_est01["tiempo"]
    time02 = info_est02["tiempo"]
    val01 = info_est01["valor"]
    max01 = info_est01["max_abs"]
    max_pro01 = info_est01["max_pro"]
    min01 = info_est01["min_abs"]
    min_pro01 = info_est01["min_abs"]
    val02 = info_est02["valor"]
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

    titulo_grafico = "Comparacion Variables"
    layout = dict(
        title=titulo_grafico,
        yaxis=dict(
            title=variable02.var_nombre + str(" (") + variable02.uni_id.uni_sigla + str(")"),
            autorange='reversed',
            overlaying='y',
            side='right',
        ),
        yaxis2=dict(
            title=variable01.var_nombre + str(" (") + variable01.uni_id.uni_sigla + str(")"),

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


def get_elemento_data_json(variable, tiempo, valor, nombre, color):
    type_graph = 'scatter'
    if variable.var_id == 1:
        type_graph = 'bar'
    elemento = {
        'type': type_graph,
        'x': tiempo,
        'y': valor,
        'name': nombre,
        'line': {
            'color': color,
        }
    }
    return elemento


def get_elemento_data(variable, tiempo, valor, nombre, color=None):
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


# crear el gráfico con cualquier tipo de datos
def get_grafico(layout, data):
    figure = go.Figure(data=data, layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div', include_plotlyjs=False)
    grafico = dict(grafico=div)
    return grafico


# crear el estilo del grafico
def get_layout_grafico(titulo, titulo_yaxis, fecha_inicio, fecha_fin):
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
    botones.append(boton_mes)
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
        data = [trace_valor]
    else:
        data = [trace_valor, trace_maximo, trace_minimo]

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


