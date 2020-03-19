# -*- coding: utf-8 -*-
from estacion.models import Estacion
from variable.models import Variable, Unidad

from registro.models import LogMedicion
import datetime
from django.db import connection
from django.contrib.auth.models import User
from django.db import models
import plotly.offline as opy
import plotly.graph_objs as go
from reportes.functions import get_elemento_data_json, get_layout_grafico, datos_instantaneos


class ReporteValidacion(models.Model):
    numero_fila = models.BigAutoField(primary_key=True)
    seleccionado = models.BooleanField()
    fecha = models.DateTimeField()
    valor_seleccionado = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    valor = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    variacion_consecutiva = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    comentario = models.CharField(max_length=350)
    class_fila = models.CharField(max_length=30)
    class_fecha = models.CharField(max_length=30)
    class_validacion = models.CharField(max_length=30)
    class_valor = models.CharField(max_length=30)
    class_variacion_consecutiva = models.CharField(max_length=30)
    class_stddev_error = models.CharField(max_length=30)


def reporte_validacion(estacion, variable, inicio, final):
    print("Inicio Reporte Validacion: ", datetime.datetime.now())
    est_id = estacion.est_id
    var_id = variable.var_modelo
    fin = datetime.datetime.combine(final, datetime.time(23, 59, 59, 999999))
    query = "select * FROM reporte_validacion_" + str(var_id).lower() + "(%s, %s, %s);"
    print(query, est_id, inicio, fin)
    consulta = ReporteValidacion.objects.raw(query, [est_id, inicio, fin])
    print("Fin Reporte Validacion: ", datetime.datetime.now())
    return consulta


# funcion para registrar los cambios en la tabla medicion
def guardar_log(accion, medicion, user):
    logmedicion = LogMedicion()
    logmedicion.medicion = medicion.med_id
    logmedicion.variable = medicion.var_id
    logmedicion.estacion = medicion.est_id
    logmedicion.marca = medicion.mar_id
    logmedicion.med_fecha = medicion.med_fecha
    logmedicion.med_valor = medicion.med_valor
    logmedicion.med_maximo = medicion.med_maximo
    logmedicion.med_minimo = medicion.med_minimo
    logmedicion.usuario = user
    logmedicion.log_accion = accion
    if accion == "Modificar":
        logmedicion.log_mensaje = "Valores Modificados"
    else:
        logmedicion.log_mensaje = "Valores Eliminados"
    logmedicion.save()


# Grafico para la validacion de datos
def grafico_validacion(variable, estacion, fecha_inicio, fecha_fin):

    # informacion = datos_instantaneos(estacion, variable, fecha_inicio, fecha_fin)
    informacion = reporte_validacion(estacion, variable, fecha_inicio, fecha_fin)
    tiempo = []
    valor = []
    for fila in informacion:
        if not fila.seleccionado:
            continue
        if fila.class_fecha == 'fecha salto':
            valor.append(None)
            tiempo.append(fila.fecha - datetime.timedelta(minutes=1))
        valor.append(fila.valor)
        tiempo.append(fila.fecha)

    if variable.var_id == 1:
        data_valor = get_elemento_data_json('bar', tiempo, valor, 'Valor', '#1660A7')
    else:
        data_valor = get_elemento_data_json('scatter', tiempo, valor, 'Media', '#1660A7')

    titulo_grafico = variable.var_nombre + " " + estacion.est_codigo
    titulo_yaxis = variable.var_nombre + " (" + variable.uni_id.uni_sigla + ")"

    data = [data_valor]

    layout = get_layout_grafico(titulo_grafico, titulo_yaxis, fecha_inicio, fecha_fin)

    grafico_div = dict(
        data=data,
        layout=layout,
    )

    return grafico_div


'''def grafico(form,valores, maximos_abs, minimos_abs, tiempo):
    estacion = form.cleaned_data['estacion']
    variable = form.cleaned_data['variable']
    div = ""
    if len(valores) > 0:
        if variable.var_id == 1:
            tra_pro = go.Bar(
                x=tiempo,
                y=valores,
            )
            data = [tra_pro]
        else:
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
            data = [tra_max_abs, tra_prom, tra_min_abs]

        layout = go.Layout(
            title=estacion.est_codigo + " " + estacion.est_nombre,
            yaxis=dict(title=variable.var_nombre),
        )
        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')
    return div'''


def titulo_unidad(variable):
    uni = list(Unidad.objects.filter(uni_id=variable.uni_id.uni_id).values())
    return uni[0].get('uni_sigla')


class Analisis(object):
    med_id = 0
    var_id = 0
    fecha = ""
    hora = ""
    valor = 0
    valor_error = False
    resta = 0
    resta_error = "Normal"
    variabilidad = 0
    var_error = False
