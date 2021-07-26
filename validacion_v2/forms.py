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

from django.forms import ModelForm, Form, ModelChoiceField, DateTimeField
from django.forms import ModelForm
from validacion.models import Validacion
from estacion.models import Estacion
from variable.models import Variable


class BorrarForm(Form):
    estacion = ModelChoiceField(queryset=Estacion.objects.order_by('est_id').all(), empty_label="Estación")
    variable = ModelChoiceField(queryset=Variable.objects.order_by('var_id').all(), empty_label="Variable")
    inicio = DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], label="Fecha de Inicio")
    fin = DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], label="Fecha de Fin")
