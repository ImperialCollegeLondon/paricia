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
from variable.models import Variable
from cruce.models import Cruce


class AnuarioForm(forms.Form):
    YEAR = (
        ('2007', '2007'),
        ('2008', '2008'),
        ('2009', '2009'),
        ('2010', '2010'),
        ('2011', '2011'),
        ('2012', '2012'),
        ('2013', '2013'),
        ('2014', '2014'),
        ('2015', '2015'),
        ('2016', '2016'),
        ('2017', '2017'),
        ('2018', '2018'),
        ('2019', '2019'),
        ('2020', '2020'),
    )

    estacion = forms.ModelChoiceField(required=False,
                                      queryset=Estacion.objects.order_by('est_id').all(), empty_label='Estación')
    variable = forms.ModelChoiceField(required=False,
                                      queryset=Variable.objects.filter(var_id__in = (1,2,3,4,5,6,7,8,9,10,11) ).order_by('var_id'), empty_label='Variable')
    periodo = forms.ChoiceField(required=False, choices=YEAR, label='Año')

    
    tipo = forms.ChoiceField(required=False, choices=(('validado', 'validado'), ('crudo', 'crudo')),
                             label="Tipo de Dato")
