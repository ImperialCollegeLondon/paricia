# -*- coding: utf-8 -*-
from django import forms
from estacion.models import Estacion
from variable.models import Variable, Unidad
from medicion.models import Medicion
from django.db.models import Max, Min, Avg, Count, Sum
from django.db.models.functions import (
    ExtractYear, ExtractMonth, ExtractDay, ExtractHour)
import plotly.offline as opy
import plotly.graph_objs as go
import datetime, calendar

from django.db import connection


# cursor = connection.cursor()

class MedicionSearchForm(forms.Form):
    FRECUENCIA = (
        ('0', 'Minima'),
        ('1', '5 Minutos'),
        ('2', 'Horario'),
        ('3', 'Diario'),
        ('4', 'Mensual'),
    )
    estacion = forms.ModelChoiceField(
        queryset=Estacion.objects.order_by('est_id').all())
    variable = forms.ModelChoiceField(
        queryset=Variable.objects.order_by('var_id').all())

    inicio = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio(dd/mm/yyyy)")
    fin = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Fin(dd/mm/yyyy)")
    frecuencia = forms.ChoiceField(choices=FRECUENCIA)

    # saber si hay datos
    def exists(self, form):
        # print self.estacion
        estacion = form.cleaned_data['estacion']
        variable = form.cleaned_data['variable']
        fecha_inicio = form.cleaned_data['inicio']
        fecha_fin = form.cleaned_data['fin']
        frecuencia = form.cleaned_data['frecuencia']
        # filtrar los datos por estacion, variable y rango de fechas
        consulta = (Medicion.objects.filter(est_id=estacion)
                    .filter(var_id=variable)
                    .filter(med_fecha__range=[fecha_inicio, fecha_fin]).exists())
        return consulta


class ComparacionForm(forms.Form):
    FRECUENCIA = (
        ('1', '5 Minutos'),
        ('2', 'Horario'),
        ('3', 'Diario'),
        ('4', 'Mensual'),
    )
    estacion01 = forms.ModelChoiceField(required=False,
                                        queryset=Estacion.objects.order_by('est_id').all(), label='Primera Estación')
    estacion02 = forms.ModelChoiceField(required=False,
                                        queryset=Estacion.objects.order_by('est_id').all(), label='Segunda Estación')
    estacion03 = forms.ModelChoiceField(required=False,
                                        queryset=Estacion.objects.order_by('est_id').all(), label='Tercera Estación')
    variable = forms.ModelChoiceField(required=False,
                                      queryset=Variable.objects.order_by('var_id').all(), label='Variable')
    inicio = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio(dd/mm/yyyy)")
    fin = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Fin(dd/mm/yyyy)")
    # tiempo=forms.IntegerField(max_value=60,min_value=5,label="Tiempo en Minutos",help_text="Valor entre 5 y 60")
    frecuencia = forms.ChoiceField(choices=FRECUENCIA)


class VariableForm(forms.Form):
    FRECUENCIA = (
        ('1', '5 Minutos'),
        ('2', 'Horario'),
        ('3', 'Diario'),
        ('4', 'Mensual'),
    )
    estacion01 = forms.ModelChoiceField(required=False,
                                        queryset=Estacion.objects.order_by('est_id').all(), label='Primera Estación')
    variable01 = forms.ModelChoiceField(required=False,
                                        queryset=Variable.objects.order_by('var_id').all(), label='Primera Variable')
    estacion02 = forms.ModelChoiceField(required=False,
                                        queryset=Estacion.objects.order_by('est_id').all(), label='Segunda Estación')
    variable02 = forms.ModelChoiceField(required=False,
                                        queryset=Variable.objects.order_by('var_id').all(), label='Segunda Variable')
    inicio = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio(dd/mm/yyyy)")
    fin = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Fin(dd/mm/yyyy)")
    # tiempo=forms.IntegerField(max_value=60,min_value=5,label="Tiempo en Minutos",help_text="Valor entre 5 y 60")
    frecuencia = forms.ChoiceField(choices=FRECUENCIA)
