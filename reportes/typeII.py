# -*- coding: utf-8 -*-

import plotly.offline as opy
import plotly.graph_objs as go
from reportes.titulos import Titulos
from anuarios.models import Precipitacion
from django.db.models import Avg, Max, Min
from django.db.models import FloatField
import calendar


# clase para anuario de la variable PRE
class TypeII(Titulos):
    def consulta(self, estacion, periodo):
        # annotate agrupa los valores en base a un campo y a una operacion
        informacion = list(Precipitacion.objects.filter(est_id=estacion).filter(pre_periodo=periodo).order_by('pre_id'))
        return informacion

    def datos_historicos(self, estacion, periodo, parametro):
        consulta = Precipitacion.objects.filter(est_id=estacion)
        consulta= consulta.exclude(pre_periodo=periodo).values('pre_mes')
        if parametro == 'promedio':
            informacion = list(
                consulta
                .annotate(valor=Avg('pre_suma')).order_by('pre_mes')
            )
        elif parametro == 'maximo':
            informacion = list(
                consulta
                .annotate(valor=Max('pre_suma', output_field=FloatField())-Avg('pre_suma'))
                .order_by('pre_mes')
            )
        else:
            informacion = list(
                consulta
                .annotate(valor=Avg('pre_suma')-Min('pre_suma', output_field=FloatField()))
                .order_by('pre_mes')
            )
        datos = []
        for item in informacion:
            datos.append(item['valor'])
        return datos

    def matriz(self, estacion, periodo):
        datos = self.consulta(estacion, periodo)
        return datos

    def grafico(self, estacion, variable, periodo):
        datos = self.consulta(estacion, periodo)
        if datos:
            historicos = self.datos_historicos(estacion, periodo, 'promedio')
            max_historico = self.datos_historicos(estacion, periodo, 'maximo')
            min_historico = self.datos_historicos(estacion, periodo, 'minimo')

            meses = []
            mensual_simple = []
            for item in datos:
                meses.append(str(calendar.month_abbr[item.pre_mes]))
                mensual_simple.append(item.pre_suma)
            trace1 = go.Bar(
                x=meses,
                y=mensual_simple,
                name='Precipitacion (mm)'
            )
            trace2 = go.Bar(
                x=meses,
                y=historicos,
                name='Pre. Historica (mm)',
                error_y=dict(
                    type='data',
                    symmetric=False,
                    array=max_historico,
                    arrayminus=min_historico
                )
            )
            data = go.Data([trace1, trace2])
            layout = go.Layout(
                title=str(self.titulo_grafico(variable)) + str(" (") + str(self.titulo_unidad(variable)) + str(")"))
            figure = go.Figure(data=data, layout=layout)
            div = opy.plot(figure, auto_open=False, output_type='div')
            return div
        return False
