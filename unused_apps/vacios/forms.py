# -*- coding: utf-8 -*-

################################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos (iMHEA)
# basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#         Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS), Ecuador.
#         Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones creadoras,
#              ya sea en uso total o parcial del código.


from django import forms

from estacion.models import Estacion
from formato.models import Variable


class VaciosSearchForm(forms.Form):
    estacion = forms.ModelChoiceField(
        required=False, queryset=Estacion.objects.order_by("est_id").all()
    )
    variable = forms.ModelChoiceField(
        required=False, queryset=Variable.objects.order_by("var_id").all()
    )
