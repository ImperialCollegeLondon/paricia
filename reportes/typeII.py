# -*- coding: utf-8 -*-

import plotly.offline as opy
import plotly.graph_objs as go
from reportes.titulos import Titulos
from anuarios.models import Precipitacion

import datetime, calendar


# clase para anuario de la variable PRE
class TypeII(Titulos):
    def consulta(self, estacion, periodo):
        # annotate agrupa los valores en base a un campo y a una operacion
        informacion = list(Precipitacion.objects.filter(est_id=estacion).filter(pre_periodo=periodo))
        return informacion

    def matriz(self, estacion, variable, periodo):
        datos = self.consulta(estacion, periodo)
        return datos

    def grafico(self, estacion, variable, periodo):
        datos = self.consulta(estacion, periodo)
        meses = []
        mensual_simple = []
        for item in datos:
            # meses.append(item.pre_mes)
            meses.append(str(calendar.month_abbr[item.pre_mes]))
            mensual_simple.append(item.pre_suma)
        trace1 = go.Bar(
            x=meses,
            y=mensual_simple,
            name='Precipitacion (mm)'
        )
        data = go.Data([trace1])
        layout = go.Layout(
            title=str(self.titulo_grafico(variable)) + str(" (") + str(self.titulo_unidad(variable)) + str(")"))
        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')
        print(div)
        return div
