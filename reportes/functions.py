# -*- coding: utf-8 -*-

from reportes.typeI import TypeI
from reportes.typeII import TypeII
from reportes.typeIII import TypeIII
from reportes.typeIV import TypeIV
from reportes.typeV import TypeV
from reportes.typeVI import TypeVI
from cruce.models import Cruce
from estacion.models import Estacion
from medicion.models import Medicion
import datetime
import plotly.offline as opy
import plotly.graph_objs as go

from django.db import connection

from .consultas.functions import (datos_diarios, datos_5minutos, datos_horarios, datos_mensuales)


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

    for item in variables:
        if item.get('var_id') in typeI:
            matriz = obj_typeI.matriz(form.cleaned_data['estacion'], item.get('var_id'), form.cleaned_data['anio'])
            grafico = obj_typeI.grafico(form.cleaned_data['estacion'], item.get('var_id'), form.cleaned_data['anio'])
            context.update({str(item.get('var_id')) + '_matriz': matriz})
            context.update({str(item.get('var_id')) + '_grafico': grafico})
        elif item.get('var_id') in typeII:
            matriz = obj_typeII.matriz(form.cleaned_data['estacion'], item.get('var_id'), form.cleaned_data['anio'])
            grafico = obj_typeII.grafico(form.cleaned_data['estacion'], item.get('var_id'), form.cleaned_data['anio'])
            context.update({str(item.get('var_id')) + '_matriz': matriz})
            context.update({str(item.get('var_id')) + '_grafico': grafico})
        elif item.get('var_id') in typeIII:
            matriz = obj_typeIII.matriz(form.cleaned_data['estacion'], item.get('var_id'), form.cleaned_data['anio'])
            grafico = obj_typeIII.grafico(form.cleaned_data['estacion'], item.get('var_id'), form.cleaned_data['anio'])
            context.update({str(item.get('var_id')) + '_matriz': matriz})
            context.update({str(item.get('var_id')) + '_grafico': grafico})
        elif item.get('var_id') in typeIV:
            matriz = obj_typeIV.matriz(form.cleaned_data['estacion'], item.get('var_id'), form.cleaned_data['anio'])
            grafico = obj_typeIV.grafico(form.cleaned_data['estacion'], item.get('var_id'), form.cleaned_data['anio'])
            context.update({str(item.get('var_id')) + '_matriz': matriz})
            context.update({str(item.get('var_id')) + '_grafico': grafico})
        elif item.get('var_id') in typeV:
            matriz = obj_typeV.matriz(form.cleaned_data['estacion'], item.get('var_id_id'), form.cleaned_data['anio'])
            context.update({str(item.get('var_id')) + '_matriz': matriz})
        elif item.get('var_id') in typeVI:
            matriz = obj_typeVI.matriz(form.cleaned_data['estacion'], str(item.get('var_id')),form.cleaned_data['anio'])
            context.update({str(item.get('var_id')) + '_matriz': matriz})
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
        val01, max01, min01, time01 = datos_5minutos(estacion01, variable, fecha_inicio, fecha_fin)
        val02, max02, min02, time02 = datos_5minutos(estacion02, variable, fecha_inicio, fecha_fin)
        val03, max03, min03, time03 = datos_5minutos(estacion03, variable, fecha_inicio, fecha_fin)
    # frecuencia horaria
    elif (frecuencia == str(2)):
        val01, max01, min01, time01 = datos_horarios(estacion01, variable, fecha_inicio, fecha_fin)
        val02, max02, min02, time02 = datos_horarios(estacion02, variable, fecha_inicio, fecha_fin)
        val03, max03, min03, time03 = datos_horarios(estacion03, variable, fecha_inicio, fecha_fin)
    # frecuencia diaria
    elif (frecuencia == str(3)):
        val01, max01, min01, time01 = datos_diarios(estacion01, variable, fecha_inicio, fecha_fin)
        val02, max02, min02, time02 = datos_diarios(estacion02, variable, fecha_inicio, fecha_fin)
        val03, max03, min03, time03 = datos_diarios(estacion03, variable, fecha_inicio, fecha_fin)
    # frecuencia mensual
    elif (frecuencia == str(4)):
        val01, max01, min01, time01 = datos_mensuales(estacion01, variable, fecha_inicio, fecha_fin)
        val02, max02, min02, time02 = datos_mensuales(estacion02, variable, fecha_inicio, fecha_fin)
        val03, max03, min03, time03 = datos_mensuales(estacion03, variable, fecha_inicio, fecha_fin)
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


def comparar_variable(form):
    estacion01 = form.cleaned_data['estacion01']
    estacion02 = form.cleaned_data['estacion02']
    variable01 = form.cleaned_data['variable01']
    variable02 = form.cleaned_data['variable02']
    fecha_inicio = form.cleaned_data['inicio']
    fecha_fin = form.cleaned_data['fin']
    frecuencia = form.cleaned_data['frecuencia']
    # frecuencia 5 minutos
    if (frecuencia == str(1)):
        val01, max01, min01, time01 = datos_5minutos(estacion01, variable01, fecha_inicio, fecha_fin)
        val02, max02, min02, time02 = datos_5minutos(estacion02, variable02, fecha_inicio, fecha_fin)
    # frecuencia horaria
    elif (frecuencia == str(2)):
        val01, max01, min01, time01 = datos_horarios(estacion01, variable01, fecha_inicio, fecha_fin)
        val02, max02, min02, time02 = datos_horarios(estacion02, variable02, fecha_inicio, fecha_fin)
    # frecuencia diaria
    elif (frecuencia == str(3)):
        val01, max01, min01, time01 = datos_diarios(estacion01, variable01, fecha_inicio, fecha_fin)
        val02, max02, min02, time02 = datos_diarios(estacion02, variable02, fecha_inicio, fecha_fin)
    # frecuencia mensual
    elif (frecuencia == str(4)):
        val01, max01, min01, time01 = datos_mensuales(estacion01, variable01, fecha_inicio, fecha_fin)
        val02, max02, min02, time02 = datos_mensuales(estacion02, variable02, fecha_inicio, fecha_fin)
    trace0 = trace_graph(variable01, estacion01, time01, val01)
    trace1 = trace_graph(variable02, estacion02, time02, val02)
    data = go.Data([trace0, trace1])
    layout = go.Layout(
        title="Comparación de Variables",
        yaxis=dict(
            title=variable01.var_nombre + \
                  str(" (") + variable01.uni_id.uni_sigla + str(")")
        ),
        yaxis2=dict(
            title=variable02.var_nombre + \
                  str(" (") + variable02.uni_id.uni_sigla + str(")"),
            titlefont=dict(
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            ),
            overlaying='y',
            side='right'
        ),
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
            yaxis='y2'
        )
    return trace
