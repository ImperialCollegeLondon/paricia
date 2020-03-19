# -*- coding: utf-8 -*-

from django import forms
from anuarios.models import RadiacionMaxima, RadiacionMinima
from reportes.titulos import Titulos


# clase para anuario de la variable RAD
class TypeVI(Titulos):

    @staticmethod
    def matriz(estacion, variable, periodo):
        datos = {}
        rad_min = list(RadiacionMinima.objects.filter(est_id=estacion)
                       .filter(rad_periodo=periodo))
        rad_max = list(RadiacionMaxima.objects.filter(est_id=estacion)
                       .filter(rad_periodo=periodo))
        if rad_min and rad_max:
            datos = {
                'rad_max': rad_max,
                'rad_min': rad_min
            }

        return datos

    def tabla_excel(self, ws, estacion, variable, periodo, tipo):
        col_fin = 17
        col = 1
        if tipo == 'maxima':
            fila = 5
            ws.merge_cells(start_row=fila, start_column=col, end_row=fila, end_column=col_fin)
            subtitle = ws.cell(row=fila, column=col)
            subtitle.value = "Radiación Solar - Valores máximos, mínimos medios horarios"
            self.set_style(cell=subtitle, font='font_bold_10', alignment='center',
                           fill='light_salmon')
            self.bordes_celdas(ws, fila, col, fila, col_fin)
        else:
            fila = 20

        fila += 1
        ws.merge_cells(start_row=fila, start_column=col, end_row=fila, end_column=col_fin)
        subtitle = ws.cell(row=fila, column=col)
        if tipo == 'maxima':
            subtitle.value = "Radiacion Máxima Horaria W/m2"
        else:
            subtitle.value = "Radiacion Mínima Horaria W/m2"
        self.set_style(cell=subtitle, font='font_bold_10', alignment='center')
        self.bordes_celdas(ws, fila, col, fila, col_fin)

        fila += 1
        cell = ws.cell(row=fila, column=col)
        cell.value = "Mes/Hora"
        self.set_style(cell=cell, font='font_10', alignment='wrap',
                       border='border_thin')

        for i in range(2, 16):
            cell = ws.cell(row=fila, column=i)
            cell.value = str(i+3)
            self.set_style(cell=cell, font='font_10', alignment='wrap',
                           border='border_thin')

        col = 16
        cell = ws.cell(row=fila, column=col)
        cell.value = "Máxima"
        self.set_style(cell=cell, font='font_10', alignment='wrap',
                       border='border_thin')

        col = 17
        cell = ws.cell(row=fila, column=col)
        cell.value = "Hora"
        self.set_style(cell=cell, font='font_10', alignment='wrap',
                       border='border_thin')

        fila += 1
        matriz = self.matriz(estacion, variable, periodo)

        if tipo == 'maxima':
            informacion = matriz['rad_max']
        else:
            informacion = matriz['rad_min']

        for item in informacion:
            col = 1
            cell = ws.cell(row=fila, column=col)
            cell.value = self.get_mes_anio(item.rad_mes)
            self.set_style(cell=cell, font='font_10', alignment='left',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.rad_5
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')

            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.rad_6
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')

            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.rad_7
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')

            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.rad_8
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')

            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.rad_9
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')

            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.rad_10
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')

            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.rad_11
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')

            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.rad_12
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')

            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.rad_13
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')

            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.rad_14
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')

            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.rad_15
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')

            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.rad_16
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')

            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.rad_17
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')

            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.rad_18
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')

            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.rad_max
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')

            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.rad_hora
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')

            fila += 1
