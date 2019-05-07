# -*- coding: utf-8 -*-

from anuarios.models import HumedadAire
import plotly.offline as opy
import plotly.graph_objs as go
from reportes.titulos import Titulos
import calendar

# clase para anuario de la variable HAI
class TypeIV(Titulos):

    def consulta(self, estacion, periodo):
        # annotate agrupa los valores en base a un campo y a una operacion
        informacion = list(HumedadAire.objects.filter(est_id=estacion).filter(hai_periodo=periodo))
        return informacion

    def matriz(self, estacion, variable, periodo):
        datos = self.consulta(estacion, periodo)
        return datos

    def grafico(self, estacion, variable, periodo):
        datos = self.consulta(estacion, periodo)
        if datos:
            meses = []
            max_simple = []
            min_simple = []
            avg_simple = []
            for item in datos:
                meses.append(str(calendar.month_abbr[item.hai_mes]))
                max_simple.append(item.hai_maximo)
                min_simple.append(item.hai_minimo)
                avg_simple.append(item.hai_promedio)
            trace0 = go.Scatter(
                x=meses,
                y=max_simple,
                name='Max',
                line=dict(
                    color=('rgb(22, 96, 167)'),
                    width=4)
            )
            trace1 = go.Scatter(
                x=meses,
                y=min_simple,
                name='Min',
                line=dict(
                    color=('rgb(205, 12, 24)'),
                    width=4, )
            )
            trace2 = go.Scatter(
                x=meses,
                y=avg_simple,
                name='Media',
                line=dict(
                    color=('rgb(50, 205, 50)'),
                    width=4, )
            )
            data = [trace0, trace1, trace2]
            layout = go.Layout(
                title=str(self.titulo_grafico(variable)) + str(" (") + str(self.titulo_unidad(variable)) + str(")"))
            figure = go.Figure(data=data, layout=layout)
            div = opy.plot(figure, auto_open=False, output_type='div')
            return div
        return False
