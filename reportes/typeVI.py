# -*- coding: utf-8 -*-

from django import forms
from anuarios.models import RadiacionMaxima, RadiacionMinima
from reportes.titulos import Titulos


# clase para anuario de la variable RAD
class TypeVI(Titulos):

    def matriz(self, estacion, variable, periodo):
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
