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
from frecuencia.models import Frecuencia


class CrearFrecuenciaForm(forms.ModelForm):
    fre_fecha_ini = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'],
                                        label="Fecha de Inicio(yyyy-mm-dd HH:MM:SS)")
    fre_fecha_fin = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'],
                                        label="Fecha de Fin(yyyy-mm-dd HH:MM:SS)",
                                        required=False)

    class Meta:
        model = Frecuencia
        fields = ['est_id', 'var_id', 'fre_valor', 'fre_fecha_ini', 'fre_fecha_fin']