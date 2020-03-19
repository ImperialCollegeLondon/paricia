# -*- coding: utf-8 -*-

from django import forms
from estacion.models import Estacion
from variable.models import Variable


class PorcentajeHorarioForm(forms.Form):
    estacion = forms.ModelChoiceField(
        queryset=Estacion.objects.filter(est_externa=False).order_by('est_codigo'))
    variable = forms.ModelChoiceField(
        queryset=Variable.objects.order_by('var_id').all())
    inicio = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio", required=False,
                             widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'dd/mm/yy'}))
    fin = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Fin", required=False,
                          widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'dd/mm/yy'}))
