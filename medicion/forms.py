# -*- coding: utf-8 -*-
from django import forms
from estacion.models import Estacion
from variable.models import Variable
from medicion.models import CurvaDescarga


class ValidacionSearchForm(forms.Form):
    TIPO_VALOR = (
        ('valor', 'valor'),
        ('maximo', 'máximo'),
        ('minimo', 'mínimo'),
    )
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.order_by('est_id').all())
    variable = forms.ModelChoiceField(queryset=Variable.objects.order_by('var_id').all())
    inicio = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio(yyyy-mm-dd)")
    fin = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Fin(yyyy-mm-dd)")
    #valor = forms.ChoiceField(choices=TIPO_VALOR)


class MedicionSearchForm(forms.Form):
    TIPO_VARIABLE = (
        ('valor', 'valor'),
        ('maximo', 'maximo'),
        ('minimo', 'minimo'),
    )
    estacion = forms.ModelChoiceField(
        queryset=Estacion.objects.order_by('est_id').all())
    variable = forms.ModelChoiceField(
        queryset=Variable.objects.order_by('var_id').all())
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

class MedicionConsultaForm(forms.Form):
    estacion = forms.ModelChoiceField(
        queryset=Estacion.objects.order_by('est_id').all())
    variable = forms.ModelChoiceField(
        queryset=Variable.objects.order_by('var_id').all())
    inicio = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio(dd/mm/yyyy)")
    fin = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Fin(dd/mm/yyyy)")


class CurvaDescargaSearchForm(forms.Form):
    lista = []
    estacion = forms.ModelChoiceField(required=False, queryset=Estacion.objects.order_by('est_codigo').all())

    def filtrar(self, form):
        if form.cleaned_data['estacion']:
            lista = CurvaDescarga.objects.filter(estacion=form.cleaned_data['estacion'])
        else:
            lista = CurvaDescarga.objects.all()
        return lista


class BorrarForm(forms.Form):
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.order_by('est_id').all())
    variable = forms.ModelChoiceField(queryset=Variable.objects.order_by('var_id').all())
    inicio = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], label="Fecha de Inicio(yyyy-mm-dd HH:MM:SS)")
    fin = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], label="Fecha de Fin(yyyy-mm-dd HH:MM:SS)")