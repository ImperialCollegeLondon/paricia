# -*- coding: utf-8 -*-
from django import forms
from estacion.models import Estacion
from variable.models import Variable
from medicion.models import Medicion


class MedicionSearchForm(forms.Form):
    TIPO_VARIABLE = (
        ('valor', 'valor'),
        ('maximo', 'maximo'),
        ('minimo', 'minimo'),
    )
    estacion = forms.ModelChoiceField(
        queryset=Estacion.objects.order_by('est_id').all())
    variable = forms.ModelChoiceField(
        queryset=Variable.objects.filter(var_id__in=[1, 2, 3, 6, 8]).order_by('var_id').all())
    inicio = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio(dd/mm/yyyy)")
    fin = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Fin(dd/mm/yyyy)")
    valor = forms.ChoiceField(choices=TIPO_VARIABLE)


class FilterDeleteForm(forms.Form):
    estacion = forms.ModelChoiceField(
        queryset=Estacion.objects.order_by('est_id').all())
    variable = forms.ModelChoiceField(
        queryset=Variable.objects.order_by('var_id').all())
    fec_ini = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio(dd/mm/yyyy)")
    hor_ini = forms.TimeField(input_formats=['%H:%M:%S'], label="Hora de Inicio(HH:MM:SS)")
    fec_fin = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Fin(dd/mm/yyyy)")
    hor_fin = forms.TimeField(input_formats=['%H:%M:%S'], label="Hora de Fin(HH:MM:SS)")
