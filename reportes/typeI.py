# -*- coding: utf-8 -*-
from anuarios.models import HumedadSuelo
from anuarios.models import PresionAtmosferica
from anuarios.models import TemperaturaAgua
from anuarios.models import Caudal
from anuarios.models import NivelAgua
import plotly.offline as opy
import plotly.graph_objs as go
from reportes.titulos import Titulos
import calendar

# clase para anuario de las las variables HSU, PAT, TAG, CAU, NAG
class TypeI(Titulos):
    def consulta(self, estacion, variable, periodo):
        if variable == 6:
            informacion = list(HumedadSuelo.objects.filter(est_id=estacion).filter(hsu_periodo=periodo))
        elif variable == 8:
            informacion = list(PresionAtmosferica.objects.filter(est_id=estacion).filter(pat_periodo=periodo))
        elif variable == 9:
            informacion = list(TemperaturaAgua.objects.filter(est_id=estacion).filter(tag_periodo=periodo))
        elif variable == 10:
            informacion = list(Caudal.objects.filter(est_id=estacion).filter(cau_periodo=periodo))
        elif variable == 11:
            informacion = list(NivelAgua.objects.filter(est_id=estacion).filter(nag_periodo=periodo))
        return informacion

    def matriz(self, estacion, variable, periodo):
        datos = self.consulta(estacion, variable, periodo)
        return datos

    def grafico(self, estacion, variable, periodo):
        datos = self.consulta(estacion, variable, periodo)
        if len(datos)>0:
            meses = []
            max_simple = []
            min_simple = []
            avg_simple = []
            for item in datos:
                if variable == 6:
                    meses.append(str(calendar.month_abbr[item.hsu_mes]))
                    max_simple.append(item.hsu_maximo)
                    min_simple.append(item.hsu_minimo)
                    avg_simple.append(item.hsu_promedio)
                elif variable == 8:
                    meses.append(str(calendar.month_abbr[item.pat_mes]))
                    max_simple.append(item.pat_maximo)
                    min_simple.append(item.pat_minimo)
                    avg_simple.append(item.pat_promedio)
                elif variable == 9:
                    meses.append(str(calendar.month_abbr[item.tag_mes]))
                    max_simple.append(item.tag_maximo)
                    min_simple.append(item.tag_minimo)
                    avg_simple.append(item.tag_promedio)
                elif variable == 10:
                    meses.append(str(calendar.month_abbr[item.cau_mes]))
                    max_simple.append(item.cau_maximo)
                    min_simple.append(item.cau_minimo)
                    avg_simple.append(item.cau_promedio)
                elif variable == 11:
                    meses.append(str(calendar.month_abbr[item.nag_mes]))
                    max_simple.append(item.nag_maximo)
                    min_simple.append(item.nag_minimo)
                    avg_simple.append(item.nag_promedio)

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
