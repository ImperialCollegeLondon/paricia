# -*- coding: utf-8 -*-

from django import forms
from anuarios.models import Viento
from reportes.titulos import Titulos


# clase para anuario de la variable VVI y DVI
class TypeV(Titulos):
    @staticmethod
    def matriz(estacion, variable, periodo):
        datos = list(Viento.objects.filter(est_id=estacion)
                     .filter(vie_periodo=periodo).order_by('vie_mes'))
        return datos

    def tabla_excel(self, ws, estacion, variable, periodo):
        fila = 5
        col_fin = 22
        col = 1

        ws.merge_cells(start_row=fila, start_column=col, end_row=fila, end_column=col_fin)
        subtitle = ws.cell(row=fila, column=col)
        subtitle.value = "Viento - Valores Medios Mensuales de Velocidad y Dirección de Viento "
        self.set_style(cell=subtitle, font='font_bold_10', alignment='center',
                       border='border_thin', fill='light_salmon')

        fila += 1

        ws.merge_cells(start_row=fila, start_column=col, end_row=fila + 1, end_column=col)
        cell = ws.cell(row=fila, column=col)
        cell.value = "MES"
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')

        col = 2

        ws.merge_cells(start_row=fila, start_column=col, end_row=fila, end_column=col + 1)
        cell = ws.cell(row=fila, column=col)
        cell.value = "Norte"
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')
        cell = ws.cell(row=fila, column=col+1)
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')

        col = 4

        ws.merge_cells(start_row=fila, start_column=col, end_row=fila, end_column=col + 1)
        cell = ws.cell(row=fila, column=col)
        cell.value = "NorEste"
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')
        cell = ws.cell(row=fila, column=col + 1)
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')

        col = 6

        ws.merge_cells(start_row=fila, start_column=col, end_row=fila, end_column=col + 1)
        cell = ws.cell(row=fila, column=col)
        cell.value = "Este"
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')
        cell = ws.cell(row=fila, column=col + 1)
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')

        col = 8

        ws.merge_cells(start_row=fila, start_column=col, end_row=fila, end_column=col + 1)
        cell = ws.cell(row=fila, column=col)
        cell.value = "SurEste"
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')
        cell = ws.cell(row=fila, column=col + 1)
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')

        col = 10

        ws.merge_cells(start_row=fila, start_column=col, end_row=fila, end_column=col + 1)
        cell = ws.cell(row=fila, column=col)
        cell.value = "Sur"
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')
        cell = ws.cell(row=fila, column=col + 1)
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')

        col = 12

        ws.merge_cells(start_row=fila, start_column=col, end_row=fila, end_column=col + 1)
        cell = ws.cell(row=fila, column=col)
        cell.value = "SurOeste"
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')
        cell = ws.cell(row=fila, column=col + 1)
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')

        col = 14

        ws.merge_cells(start_row=fila, start_column=col, end_row=fila, end_column=col + 1)
        cell = ws.cell(row=fila, column=col)
        cell.value = "Oeste"
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')
        cell = ws.cell(row=fila, column=col + 1)
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')

        col = 16

        ws.merge_cells(start_row=fila, start_column=col, end_row=fila, end_column=col + 1)
        cell = ws.cell(row=fila, column=col)
        cell.value = "NorOeste"
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')
        cell = ws.cell(row=fila, column=col + 1)
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')

        col = 18
        cell = ws.cell(row=fila, column=col)
        cell.value = "Calma"
        self.set_style(cell=cell, font='font_10', alignment='wrap',
                       border='border_thin')

        col = 19
        cell = ws.cell(row=fila, column=col)
        cell.value = "N°"
        self.set_style(cell=cell, font='font_10', alignment='wrap',
                       border='border_thin')

        col = 20

        ws.merge_cells(start_row=fila, start_column=col, end_row=fila, end_column=col + 1)
        cell = ws.cell(row=fila, column=col)
        cell.value = "Velocidad Mayor"
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')
        cell = ws.cell(row=fila, column=col + 1)
        self.set_style(cell=cell, font='font_10', alignment='center',
                       border='border_thin')

        col = 22
        cell = ws.cell(row=fila, column=col)
        cell.value = "Velocidad Media"
        self.set_style(cell=cell, font='font_10', alignment='wrap',
                       border='border_thin')

        fila = 7
        for i in range(2, 18, 2):
            cell = ws.cell(row=fila, column=i)
            cell.value = "m/s"
            self.set_style(cell=cell, font='font_10', alignment='wrap',
                           border='border_thin')

            cell = ws.cell(row=fila, column=i+1)
            cell.value = "%"
            self.set_style(cell=cell, font='font_10', alignment='wrap',
                           border='border_thin')

        col = 18
        cell = ws.cell(row=fila, column=col)
        cell.value = "%"
        self.set_style(cell=cell, font='font_10', alignment='wrap',
                       border='border_thin')

        col = 19
        cell = ws.cell(row=fila, column=col)
        cell.value = "Obs"
        self.set_style(cell=cell, font='font_10', alignment='wrap',
                       border='border_thin')

        col = 20
        cell = ws.cell(row=fila, column=col)
        cell.value = "m/s"
        self.set_style(cell=cell, font='font_10', alignment='wrap',
                       border='border_thin')

        col = 21
        cell = ws.cell(row=fila, column=col)
        cell.value = "DIR"
        self.set_style(cell=cell, font='font_10', alignment='wrap',
                       border='border_thin')

        col = 22
        cell = ws.cell(row=fila, column=col)
        cell.value = "Km/h"
        self.set_style(cell=cell, font='font_10', alignment='wrap',
                       border='border_thin')

        fila = 8

        matriz = self.matriz(estacion, variable, periodo)

        for item in matriz:
            col = 1
            cell = ws.cell(row=fila, column=col)
            cell.value = self.get_mes_anio(item.vie_mes)
            self.set_style(cell=cell, font='font_10', alignment='left',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_vel_N
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_por_N
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_vel_NE
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_por_NE
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_vel_E
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_por_E
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_vel_SE
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_por_SE
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_vel_S
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_por_S
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_vel_SO
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_por_SO
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_vel_O
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_por_O
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_vel_NO
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_por_NO
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_calma
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_obs
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_vel_max
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_vel_dir
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')
            col += 1
            cell = ws.cell(row=fila, column=col)
            cell.value = item.vie_vel_med
            self.set_style(cell=cell, font='font_10', alignment='center',
                           border='border_thin')

            fila += 1









