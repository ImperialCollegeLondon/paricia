# -*- coding: utf-8 -*-
from django import forms
from estacion.models import Estacion
from variable.models import Variable
from medicion.models import CurvaDescarga


class SearchForm(forms.Form):
    TIPO_VALOR = (
        ('valor', 'valor'),
        ('maximo', 'máximo'),
        ('minimo', 'mínimo'),
    )
    estacion1 = forms.ModelChoiceField(queryset=Estacion.objects.order_by('est_id').all(), label= "Primera Estaciòn")
    estacion2 = forms.ModelChoiceField(queryset=Estacion.objects.order_by('est_id').all(), label= "Segunda Estaciòn")
    inicio = forms.DateField(input_formats=['%Y-%m-%d'], label="Fecha de Inicio(yyyy-mm-dd)")
    fin = forms.DateField(input_formats=['%Y-%m-%d'], label="Fecha de Fin(yyyy-mm-dd)")
