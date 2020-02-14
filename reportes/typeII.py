# -*- coding: utf-8 -*-

import plotly.offline as opy
import plotly.graph_objs as go
from reportes.titulos import Titulos
from anuarios.models import Precipitacion
from django.db.models import Avg, Max, Min
from django.db.models import FloatField
import calendar

from openpyxl.chart import BarChart, Series, Reference

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
                .annotate(valor=Max('pre_suma', output_field=FloatField())-Avg('pre_suma', output_field=FloatField()))
                .order_by('pre_mes')
            )
        else:
            informacion = list(
                consulta
                .annotate(valor=Avg('pre_suma', output_field=FloatField())-Min('pre_suma', output_field=FloatField()))
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
            data = [trace1, trace2]
            layout = go.Layout(
                title=str(self.titulo_grafico(variable)) + str(" (") + str(self.titulo_unidad(variable)) + str(")"))
            figure = go.Figure(data=data, layout=layout)
            div = opy.plot(figure, auto_open=False, output_type='div')
            return div
        return False

    def tabla_excel(self, ws, estacion, periodo):
        fila = 5
        col_fin = 11

        ws.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=col_fin)
        subtitle = ws.cell(row=fila, column=1)
        subtitle.value = "PRECIPITACIÓN - VALORES MENSUALES Y MÁXIMOS DIARIOS"
        self.set_style(cell=subtitle, font='font_bold_10', alignment='center',
                       border='border_thin', fill='light_salmon')
        fila += 1

        ws.merge_cells(start_row=fila, start_column=1, end_row=fila+2, end_column=1)
        cell = ws.cell(row=fila, column=1)
        cell.value = "MES"
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')

        ws.merge_cells(start_row=fila, start_column=8, end_row=fila + 2, end_column=8)
        cell = ws.cell(row=fila, column=8)
        cell.value = "Cantidad de días con precipitación"
        self.set_style(cell=cell, font='font_8', alignment='wrap',
                       border='border_thin')

        ws.merge_cells(start_row=fila, start_column=2, end_row=fila, end_column=7)
        cell = ws.cell(row=fila, column=2)
        cell.value = "Precipitación (mm)"
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')
        fila += 1
        ws.merge_cells(start_row=fila, start_column=2, end_row=fila+1, end_column=2)
        cell = ws.cell(row=fila, column=2)
        cell.value = "Mensual"
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')

        ws.merge_cells(start_row=fila, start_column=3, end_row=fila + 1, end_column=3)
        cell = ws.cell(row=fila, column=3)
        cell.value = "Medía Histórica"
        self.set_style(cell=cell, font='font_10', alignment='wrap',
                       border='border_thin')

        ws.merge_cells(start_row=fila, start_column=4, end_row=fila + 1, end_column=4)
        cell = ws.cell(row=fila, column=4)
        cell.value = "Máximo Histórica"
        self.set_style(cell=cell, font='font_10', alignment='wrap',
                       border='border_thin')

        ws.merge_cells(start_row=fila, start_column=5, end_row=fila + 1, end_column=5)
        cell = ws.cell(row=fila, column=5)
        cell.value = "Mínimo Histórica"
        self.set_style(cell=cell, font='font_10', alignment='wrap',
                       border='border_thin')

        ws.merge_cells(start_row=fila, start_column=6, end_row=fila, end_column=7)
        cell = ws.cell(row=fila, column=6)
        cell.value = "Máxima en"
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')

        fila += 1

        cell = ws.cell(row=fila, column=6)
        cell.value = "24H"
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')

        cell = ws.cell(row=fila, column=7)
        cell.value = "Día"
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')

        matriz = self.matriz(estacion, periodo)
        fila += 1

        for item in matriz:
            cell = ws.cell(row=fila, column=1)
            cell.value = self.get_mes_anio(item.pre_mes)
            self.set_style(cell=cell, font='font_10', alignment='left',
                           border='border_thin')
            cell = ws.cell(row=fila, column=2)
            cell.value = item.pre_suma
            self.set_style(cell=cell, font='font_10', alignment='left',
                           border='border_thin')

            cell = ws.cell(row=fila, column=6)
            cell.value = item.pre_maximo
            self.set_style(cell=cell, font='font_10', alignment='left',
                           border='border_thin')

            cell = ws.cell(row=fila, column=7)
            cell.value = item.pre_maximo_dia
            self.set_style(cell=cell, font='font_10', alignment='left',
                           border='border_thin')

            cell = ws.cell(row=fila, column=8)
            cell.value = item.pre_dias
            self.set_style(cell=cell, font='font_10', alignment='left',
                           border='border_thin')

            fila += 1
        historicos = self.datos_historicos(estacion, periodo, 'promedio')
        max_historico = self.datos_historicos(estacion, periodo, 'maximo')
        min_historico = self.datos_historicos(estacion, periodo, 'minimo')

        fila = 9
        for (item_his, item_max, item_min) in zip(historicos, max_historico, min_historico):
            cell = ws.cell(row=fila, column=3)
            cell.value = round(item_his, 1)
            self.set_style(cell=cell, font='font_10', alignment='wrap',
                           border='border_thin')

            cell = ws.cell(row=fila, column=4)
            cell.value = round(item_max, 1)
            self.set_style(cell=cell, font='font_10', alignment='wrap',
                           border='border_thin')

            cell = ws.cell(row=fila, column=5)
            cell.value = round(item_min, 1)
            self.set_style(cell=cell, font='font_10', alignment='wrap',
                           border='border_thin')
            fila += 1





    def grafico_excel(self, ws, estacion, periodo):
        chart1 = BarChart()
        chart1.type = "col"
        chart1.style = 10
        chart1.title = "Distribución temporal de Precipitación (mm)" + str(periodo)
        chart1.y_axis.title = 'Precipitación (mm)'
        chart1.x_axis.title = 'Meses'

        data = Reference(ws, min_col=2, min_row=9, max_row=20, max_col=8)
        cats = Reference(ws, min_col=1, min_row=9, max_row=20)
        chart1.add_data(data, titles_from_data=True)
        chart1.set_categories(cats)
        chart1.shape = 4
        ws.add_chart(chart1, "A10")




