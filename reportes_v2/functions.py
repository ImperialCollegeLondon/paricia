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


from datetime import date, datetime

import plotly.graph_objs as go
import plotly.offline as opy
import requests

from cruce.models import Cruce
from estacion.models import Estacion
from reportes_v2.consultas.functions import datos_instantaneos
from reportes_v2.typeI import TypeI
from reportes_v2.typeII import TypeII
from reportes_v2.typeIII import TypeIII
from reportes_v2.typeIV import TypeIV
from reportes_v2.typeV import TypeV
from reportes_v2.typeVI import TypeVI
from variable.models import Variable

from .consultas.functions import (
    datos_5minutos,
    datos_diarios,
    datos_horarios,
    datos_mensuales,
)


def consultar_datos(form):
    estacion = form.cleaned_data["estacion"]
    variable = form.cleaned_data["variable"]
    fecha_inicio = form.cleaned_data["inicio"]
    fecha_fin = form.cleaned_data["fin"]
    frecuencia = form.cleaned_data["frecuencia"]
    informacion = dict()
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
        informacion = datos_mensuales(estacion, variable, fecha_inicio, fecha_fin)
    tiempo = informacion["tiempo"]
    valor = informacion["valor"]
    max_abs = informacion["max_abs"]
    min_abs = informacion["min_abs"]
    max_pro = informacion["max_pro"]
    min_pro = informacion["min_pro"]
    if len(valor) > 0 and valor.count(None) != len(tiempo):

        if frecuencia == str(0):
            data_valor = get_trace_minimo(tiempo, valor, "Valor", "#1660A7")
            data_maximo = get_elemento_data(
                variable, tiempo, max_abs, "Maximo", "#32CD32"
            )
            data_minimo = get_elemento_data(
                variable, tiempo, min_abs, "Minimo", "#CD0C18"
            )
        else:
            data_valor = get_elemento_data(
                variable, tiempo, valor, "Promedio", "#1660A7"
            )
            if max_abs.count(None) <= max_pro.count(None):
                data_maximo = get_elemento_data(
                    variable, tiempo, max_abs, "Maximo Absoluto", "#32CD32"
                )
            else:
                data_maximo = get_elemento_data(
                    variable, tiempo, max_pro, "Maximo Promedio", "#90EE90"
                )
            if min_abs.count(None) <= min_pro.count(None):
                data_minimo = get_elemento_data(
                    variable, tiempo, min_abs, "Minimo Absoluto", "#CD0C18"
                )
            else:
                data_minimo = get_elemento_data(
                    variable, tiempo, min_pro, "Minimo Promedio", "#FF8C00"
                )

        titulo_grafico = (
            variable.var_nombre
            + " "
            + str(titulo_frecuencia(frecuencia))
            + " "
            + estacion.est_codigo
        )
        titulo_yaxis = variable.var_nombre + " (" + variable.uni_id.uni_sigla + ")"
        layout = get_layout_grafico(
            titulo_grafico, titulo_yaxis, fecha_inicio, fecha_fin
        )

        if frecuencia == str(0) or variable.var_id == 1:
            data = get_data_graph(data_valor)
        else:
            data = get_data_graph(data_valor, data_maximo, data_minimo)

        figure = go.Figure(data=data, layout=layout)

        div = opy.plot(
            figure, auto_open=False, output_type="div", include_plotlyjs=False
        )

        grafico = dict(grafico=div)

    else:
        grafico = dict(mensaje="No existe informacion para la consulta")
    return grafico


# funcion para consultar datos pra usuarios
def consultar_datos_usuario(form):
    estacion = form.cleaned_data["estacion"]
    variable = form.cleaned_data["variable"]
    fecha_inicio = form.cleaned_data["inicio"]
    fecha_fin = form.cleaned_data["fin"]
    frecuencia = form.cleaned_data["frecuencia"]
    informacion = dict()
    if fecha_inicio is None:
        fecha_inicio = estacion.est_fecha_inicio
    if fecha_fin is None:
        fecha_fin = date.today()
    if frecuencia == str(0):
        informacion = datos_instantaneos(estacion, variable, fecha_inicio, fecha_fin)
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
    if frecuencia == str(0) or variable.var_id != 1:
        data_valor = get_elemento_data_json(
            "scatter", tiempo, valor, "Valor", "#1660A7"
        )
    else:
        data_valor = get_elemento_data_json("bar", tiempo, valor, "Promedio", "#1660A7")

    if max_abs.count(None) <= max_pro.count(None):
        data_maximo = get_elemento_data_json(
            "scatter", tiempo, max_abs, "Maximo Absoluto", "#32CD32"
        )
    else:
        data_maximo = get_elemento_data_json(
            "scatter", tiempo, max_pro, "Maximo Promedio", "#90EE90"
        )
    if min_abs.count(None) <= min_pro.count(None):
        data_minimo = get_elemento_data_json(
            "scatter", tiempo, min_abs, "Minimo Absoluto", "#CD0C18"
        )
    else:
        data_minimo = get_elemento_data_json(
            "scatter", tiempo, min_pro, "Minimo Promedio", "#FF8C00"
        )

    titulo_grafico = (
        variable.var_nombre
        + " "
        + str(titulo_frecuencia(frecuencia))
        + " "
        + estacion.est_codigo
    )
    titulo_yaxis = variable.var_nombre + " (" + variable.uni_id.uni_sigla + ")"
    layout = get_layout_grafico(titulo_grafico, titulo_yaxis, fecha_inicio, fecha_fin)
    if variable.var_id == 1:
        data = get_data_graph(data_valor)
    else:
        data = get_data_graph(data_valor, data_maximo, data_minimo)

    grafico = dict(
        data=data,
        layout=layout,
    )
    return grafico


# graficar valores a la minima frecuencia
def get_trace_minimo(tiempo, valor, nombre, color, tipo=None):
    if tipo:
        elemento = {
            "type": "scatter",
            "x": tiempo,
            "y": valor,
            "name": nombre,
            "line": {
                "color": color,
            },
        }

    else:
        elemento = go.Scattergl(
            x=tiempo,
            y=valor,
            name=nombre,
            mode="lines",
            marker=dict(color=color, line=dict(width=1, color="rgb(0,0,0)")),
        )
    return elemento


# trazo para la comparación de variables
def get_trace(variable, tiempo, valor, nombre):
    type_graph = "scatter"
    if variable.var_id == 1:
        type_graph = "bar"
        elemento = dict(
            type=type_graph,
            x=tiempo,
            y=valor,
            name=nombre,
            marker=dict(color="#1660A7"),
        )
    else:
        elemento = dict(
            type=type_graph,
            x=tiempo,
            y=valor,
            name=nombre,
            line=dict(color="#ff881e"),
            yaxis="y2",
            xaxis="x",
            position=0.85,
        )
    return elemento


def filtrar(estacion, periodo):
    # estacion = form.cleaned_data['estacion']
    # periodo = form.cleaned_data['anio']
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
    variables = list(Cruce.objects.filter(est_id=estacion))

    obj_typeI = TypeI()
    obj_typeII = TypeII()
    obj_typeIII = TypeIII()
    obj_typeIV = TypeIV()
    obj_typeV = TypeV()
    obj_typeVI = TypeVI()

    matriz = []

    for item in variables:

        variable = item.var_id

        if variable.var_id in typeI:
            matriz = obj_typeI.matriz(estacion, variable, periodo)
            grafico = obj_typeI.grafico(estacion, variable, periodo)
        elif variable.var_id in typeII:
            matriz = obj_typeII.matriz(estacion, variable, periodo)
            grafico = obj_typeII.grafico(estacion, variable, periodo)
        elif variable.var_id in typeIII:
            matriz = obj_typeIII.matriz(estacion, variable, periodo)
            grafico = obj_typeIII.grafico(estacion, variable, periodo)
        elif variable.var_id in typeIV:
            matriz = obj_typeIV.matriz(estacion, variable, periodo)
            grafico = obj_typeIV.grafico(estacion, variable, periodo)
        elif variable.var_id in typeV:
            matriz = obj_typeV.matriz(estacion, variable, periodo)
        elif variable.var_id in typeVI:
            matriz = obj_typeVI.matriz(estacion, variable, periodo)
        if len(matriz) > 0:
            context.update({str(variable.var_id) + "_matriz": matriz})
        if grafico:
            context.update({str(variable.var_id) + "_grafico": grafico})
    if len(context) == 0:
        context.update({"mensaje": "No existen datos para la consulta"})
    return context


# comparar tres estaciones en la misma vaiable
def comparar(form):
    lista_estaciones = form.cleaned_data["estacion"]
    variable = form.cleaned_data["variable"]
    fecha_inicio = form.cleaned_data["inicio"]
    fecha_fin = form.cleaned_data["fin"]
    frecuencia = form.cleaned_data["frecuencia"]

    data = []

    for est_id in lista_estaciones:
        estacion = Estacion.objects.get(est_id=est_id)
        # frecuencia horaria
        if frecuencia == str(2):
            informacion = datos_horarios(estacion, variable, fecha_inicio, fecha_fin)
        # frecuencia diaria
        elif frecuencia == str(3):
            informacion = datos_diarios(estacion, variable, fecha_inicio, fecha_fin)
        # frecuencia mensual
        elif frecuencia == str(4):
            informacion = datos_mensuales(estacion, variable, fecha_inicio, fecha_fin)
        if variable.var_id == 1:
            trace = get_elemento_data_json(
                "bar", informacion["tiempo"], informacion["valor"], estacion.est_codigo
            )
        else:
            trace = get_elemento_data_json(
                "scatter",
                informacion["tiempo"],
                informacion["valor"],
                estacion.est_codigo,
            )
        data.append(trace)

    titulo = "Comparación de Estaciones"
    titulo_yaxis = (
        variable.var_nombre + str(" (") + variable.uni_id.uni_sigla + str(")")
    )
    layout = get_layout_grafico(titulo, titulo_yaxis, fecha_inicio, fecha_fin)
    # data = get_data_graph(trace0, trace1, trace2)
    grafico = dict(
        data=data,
        layout=layout,
    )
    return grafico


# funcion para comparar dos variables entre dos estaciones
def comparar_variables(form):
    estacion01 = form.cleaned_data["estacion01"]
    estacion02 = form.cleaned_data["estacion02"]
    variable01 = form.cleaned_data["variable01"]
    variable02 = form.cleaned_data["variable02"]
    fecha_inicio = form.cleaned_data["inicio"]
    fecha_fin = form.cleaned_data["fin"]
    frecuencia = form.cleaned_data["frecuencia"]
    parametro = form.cleaned_data["parametro"]
    info_est01 = dict()
    info_est02 = dict()
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
            title=variable02.var_nombre
            + str(" (")
            + variable02.uni_id.uni_sigla
            + str(")"),
            autorange="reversed",
            overlaying="y",
            side="right",
        ),
        yaxis2=dict(
            title=variable01.var_nombre
            + str(" (")
            + variable01.uni_id.uni_sigla
            + str(")"),
        ),
        xaxis=dict(
            # rangeslider={},
            type="date",
        ),
        grid=dict(rows=2, columns=1),
        legend=dict(
            # yanchor='bottom'
            orientation="h"
        ),
    )
    data = list([trace01, trace02])
    grafico = dict(
        data=data,
        layout=layout,
    )
    return grafico


# funcion para procesar los datos del web service del INAMHI
def procesar_json_inamhi(form):
    estacion = form.cleaned_data["estacion"]
    parametro = form.cleaned_data["parametro"]
    frecuencia = form.cleaned_data["frecuencia"]
    inicio = form.cleaned_data["inicio"]
    fin = form.cleaned_data["fin"]

    fecha_inicio = datetime(inicio.year, inicio.month, inicio.day, 0, 0, 0)
    fecha_fin = datetime(fin.year, fin.month, fin.day, 23, 59, 59, 999999)
    # formato url web service INAMHI
    url_base = "http://186.42.174.236:8090/"
    url_base += frecuencia + "/"
    url_base += str(estacion.identificador) + "/"
    url_base += fecha_inicio.strftime("%Y-%m-%d %H:%M:%S") + "/"
    url_base += fecha_fin.strftime("%Y-%m-%d %H:%M:%S") + "/"
    url_base += estacion.transmision + "/"
    url_base += parametro.parametro

    # url_base += '171481m'
    # obtener respuesta del web service
    response = requests.get(url_base, auth=("FONAG", "fOnAg2018"))
    print(url_base)
    data = response.json()
    tiempo = []
    valores = []
    if len(data) > 0:
        # print(data)
        for variable in data:
            fecha = datetime.strptime(variable["fechaTomaDelDato"], "%Y-%m-%d %H:%M:%S")

            if len(variable["dataJSON"]) > 0:

                if variable["dataJSON"][0]["valor"] is not None:
                    valores.append(variable["dataJSON"][0]["valor"])
                    tiempo.append(fecha)
            else:
                valores.append(None)
        if valores.count(None) == len(data):
            mensaje = dict(mensaje="No existen datos para la consulta")
            return mensaje

        titulo = parametro.nombre + " " + estacion.codigo + " " + estacion.nombre
        titulo_yaxis = parametro.nombre + " (" + parametro.estadistico + ")"
        layout = get_layout_grafico(titulo, titulo_yaxis, fecha_inicio, fecha_fin)
        # trace_valor = get_trace_minimo(tiempo, valores, 'Valor', '#1660A7')
        if parametro.parametro == "171481h" and frecuencia == "data1h":
            trace_valor = get_elemento_data_json(
                "bar", tiempo, valores, parametro.nombre, color="#1660A7"
            )
        else:
            trace_valor = get_elemento_data_json(
                "scatter", tiempo, valores, parametro.nombre, color="#1660A7"
            )
        data = get_data_graph(trace_valor)

        grafico = dict(
            data=data,
            layout=layout,
        )

        return grafico
    else:
        mensaje = dict(
            mensaje="No existen datos para la consulta. Intente cambiando la frecuencia"
        )
        return mensaje


def get_elemento_data_json(type_graph, tiempo, valor, nombre, color=None):
    if color is None:
        elemento = {"type": type_graph, "x": tiempo, "y": valor, "name": nombre}
    else:
        elemento = {
            "type": type_graph,
            "x": tiempo,
            "y": valor,
            "name": nombre,
            "line": {
                "color": color,
            },
        }
    return elemento


# trace para graficar los porcentajes de error
def get_error_valor(fecha, valor, texto, variable):
    elemento = dict(
        type="scatter",
        x=fecha,
        y=valor,
        mode="markers",
        text=texto,
        name="periodo con vacios >" + str(100 - variable.umbral_completo) + "%",
        showlegend=True,
        marker=dict(color="#dc3545", line=dict(width=3), size=12, symbol="circle-open"),
    )
    return elemento


# trace para gráficar los valores de velocidad y viento
def get_radar_chart(valor, color, nombre, hovertext):
    puntos_cardinales = ["Norte", "N-E", "Este", "S-E", "Sur", "S-O", "Oeste", "N-O"]
    elemento = dict(
        r=valor,
        theta=puntos_cardinales,
        name=nombre,
        marker=dict(color=color),
        type="barpolar",
        hovertext=hovertext,
        hovertemplate="%{hovertext}%"
        # thetaunit='degrees',
    )
    """
    mode='markers',
        marker=dict(
            color='rgb(217,95,2)',
            size=10,
            line=dict(
                color='white'
            )
        )"""
    return elemento


def get_segundo_eje(tiempo, valor, titulo):
    elemento = dict(
        type="scatter",
        x=tiempo,
        y=valor,
        name=titulo,
        # line=dict(color="#ff881e"),
        yaxis="y2",
        # xaxis='x',
        # position=0.85
    )
    return elemento


def get_elemento_data(variable, tiempo, valor, nombre, color=None):
    if variable.var_id == 1:
        elemento = go.Bar(x=tiempo, y=valor, name=nombre)
    else:
        elemento = go.Scattergl(
            x=tiempo,
            y=valor,
            name=nombre,
            mode="lines",
            line=dict(
                color=color,
            ),
        )

    return elemento


# crear el gráfico con cualquier tipo de datos
def get_grafico(layout, data):
    figure = go.Figure(data=data, layout=layout)
    div = opy.plot(figure, auto_open=False, output_type="div", include_plotlyjs=False)
    grafico = dict(grafico=div)
    return grafico


# crear el estilo del grafico
def get_layout_grafico(titulo, titulo_yaxis, fecha_inicio, fecha_fin):
    boton_dia = dict(count=1, label="1dia", step="day", stepmode="backward")
    boton_mes = dict(count=1, label="1mes", step="month", stepmode="backward")
    boton_6meses = dict(count=6, label="6meses", step="month", stepmode="backward")
    boton_all = dict(step="all")
    botones = list()

    botones.append(boton_dia)
    botones.append(boton_mes)
    botones.append(boton_all)

    layout = {
        "title": titulo,
        "yaxis": dict(title=titulo_yaxis),
        "xaxis": dict(
            range=list([fecha_inicio, fecha_fin]),
            rangeselector=dict(buttons=botones),
            rangeslider={"range": [fecha_inicio, fecha_fin]},
            type="date",
        ),
    }
    return layout


def get_layout_grafico_viento(titulo):

    layout = dict(
        title=titulo,
        # font=dict(size=16),
        legend=dict(font=dict(size=16)),
        polar=dict(
            barmode="overlay",
            bargap=0,
            radialaxis=dict(ticksuffix="%", angle=45, dtick=10),
            angularaxis=dict(direction="clockwise"),
        ),
        annotations=[
            dict(
                text="Los grupos fueron calculados con los percentiles 10, 50 y 80",
                x=0.8,
                y=0.05,
                yref="paper",
                xref="paper",
                xanchor="left",
                yanchor="bottom",
                showarrow=False,
                font=dict(color="teal", size=10),
            )
        ],
        # paper_bgcolor='rgb(255, 255, 255)',
    )
    """
    layout = dict(
        polar=dict(
            domain=dict(
                x=[0, 0.46],
                y=[1, 1]
            ),
            barmode="overlay",
            bargap=0,
            radialaxis=dict(ticksuffix="%", angle=45, dtick=10),
            angularaxis=dict(direction="clockwise")
        ),
        polar2=dict(
            domain=dict(
                x=[0.54, 1],
                y=[1, 1]
            ),
            barmode="overlay",
            bargap=0,
            radialaxis=dict(ticksuffix="m/s", angle=45, dtick=1),
            angularaxis=dict(direction="clockwise")
        ),
        showlegend=False,
    )
    """

    return layout


# Layout para graficar nivel y caudal en dos ejes
def get_layout_grafico_agua(titulo, titulo_nivel, titulo_caudal):
    layout = dict(
        title=titulo,
        yaxis=dict(titulo=titulo_nivel),
        yaxis2=dict(title=titulo_caudal, overlaying="y", side="right"),
    )
    return layout


def get_data_graph(trace_valor, trace_maximo=None, trace_minimo=None):

    if trace_maximo is None or trace_minimo is None:
        data = [trace_valor]
    else:
        data = [trace_valor, trace_maximo, trace_minimo]

    return data


# Función para consultar las estaciones por variable
def mapa_estaciones_variable(var_id, privado):
    variable = Variable.objects.get(var_id=var_id)
    if privado is True:
        """estaciones = Estacion.objects.filter(
        est_id__in=Cruce.objects.filter(var_id=var_id).order_by().values('est_id_id').distinct()).order_by('est_codigo')"""
        estaciones = (
            Cruce.objects.filter(var_id=var_id)
            .order_by("est_id__est_codigo")
            .distinct()
        )
    else:
        """estaciones = Estacion.objects.filter(
        est_id__in=Cruce.objects.filter(var_id=var_id).order_by().values('est_id_id').distinct(),
        est_externa=False)"""
        estaciones = (
            Cruce.objects.filter(var_id=var_id, est_id__est_externa=False)
            .order_by("est_id")
            .distinct()
        )

    features = []
    """
    for item in estaciones:
        fila = dict(
            type='Feature',
            geometry=dict(
                type='Point',
                coordinates=[float(item.est_longitud), float(item.est_latitud)]
            ),
            properties=dict(
                id=item.est_id.est_id,
                codigo=item.est_codigo,
                nombre=item.est_nombre,
                tipo=item.tipo.tip_nombre,
                latitud=item.est_latitud,
                longitud=item.est_longitud,
                altura=item.est_altura
            )

        )

        features.append(fila)
    """

    for item in estaciones:
        fila = dict(
            type="Feature",
            geometry=dict(
                type="Point",
                coordinates=[
                    float(item.est_id.est_longitud),
                    float(item.est_id.est_latitud),
                ],
            ),
            properties=dict(
                id=item.est_id.est_id,
                codigo=item.est_id.est_codigo,
                nombre=item.est_id.est_nombre,
                tipo=item.est_id.tipo.tip_nombre,
                latitud=item.est_id.est_latitud,
                longitud=item.est_id.est_longitud,
                altura=item.est_id.est_altura,
                variable=item.var_id.var_id,
            ),
        )

        features.append(fila)

    datos = dict(type="FeatureCollection", features=features)

    return datos


def titulo_frecuencia(frecuencia):
    nombre = []
    if frecuencia == "0":
        nombre = "Instantanea"
    elif frecuencia == "1":
        nombre = "Horaria"
    elif frecuencia == "2":
        nombre = "Diaria"
    elif frecuencia == "3":
        nombre = "Mensual"
    return nombre