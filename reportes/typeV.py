# -*- coding: utf-8 -*-

from django import forms
from anuarios.models import Viento
from reportes.titulos import Titulos


# clase para anuario de la variable VVI y DVI
class TypeV(Titulos):

    def matriz(self, estacion, variable, periodo):
        datos = list(Viento.objects.filter(est_id=estacion)
                     .filter(vie_periodo=periodo).order_by('vie_mes'))
        return datos
