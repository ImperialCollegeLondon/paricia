# -*- coding: utf-8 -*-
from django import forms
from estacion.models import Estacion
from variable.models import Variable
from medicion.models import CurvaDescarga

from datetime import datetime


class SearchForm(forms.Form):
    TIPO_VALOR = (
        ('valor', 'valor'),
        ('maximo', 'máximo'),
        ('minimo', 'mínimo'),
    )
    estacion1 = forms.ModelChoiceField(queryset=Estacion.objects.order_by('est_id').all(), label= "Primera Estaciòn",
                                       widget=forms.Select(attrs={"onChange":'cambio()'}))
    estacion2 = forms.ModelChoiceField(queryset=Estacion.objects.order_by('est_id').all(), label= "Segunda Estaciòn",
                                       widget=forms.Select(attrs={"onChange":'cambio()'}))
    inicio = forms.DateField(input_formats=['%d-%m-%Y'], label="Fecha de Inicio(dd/mm/yyyy)" )
    fin = forms.DateField(input_formats=['%d-%m-%Y'], label="Fecha de Fin(dd/mm/yyyy)" )
    FRECUENCIAS = ((1,'Horario'),(2,'Diario'),(3,'Mensual'))
    frecuencia = forms.ChoiceField(choices=FRECUENCIAS,label="Frecuencia")
    def getValidate(self):
        print( self.estacion1)


class SelecEstForm(forms.Form):
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.filter(tipo_id__in=[1,2]).order_by('est_id'), label="Estacion meteorológica")
    inicio = forms.DateField(input_formats=['%d-%m-%Y'], label="Fecha de Inicio(dd/mm/yyyy)" )
    fin = forms.DateField(input_formats=['%d-%m-%Y'], label="Fecha de Fin(dd/mm/yyyy)" )


class IndPrecipForm(forms.Form):
    fechf = datetime.strptime("31/12/2010", '%d/%m/%Y')
    estacion = forms.ModelChoiceField(initial = 1,queryset=Estacion.objects.filter(tipo_id__in=[1,2]).order_by('est_id'), label="Estacion meteorológica")
    inicio = forms.DateField(input_formats=['%d-%m-%Y'], label="Fecha de Inicio(dd/mm/yyyy)")
    fin = forms.DateField(input_formats=['%d-%m-%Y'], label="Fecha de Fin(dd/mm/yyyy)")


class IndCaudForm(forms.Form):
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.filter(tipo_id__in=[3]).order_by('est_id'), label="Estacion hidrológicas")
    inicio = forms.DateField(input_formats=['%d-%m-%Y'], label="Fecha de Inicio(dd/mm/yyyy)" )
    fin = forms.DateField(input_formats=['%d-%m-%Y'], label="Fecha de Fin(dd/mm/yyyy)" )


class SelecCaudalForm(forms.Form):
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.filter(tipo_id__exact=3).order_by('est_id'), label="Estacion Hidrológica")
    inicio = forms.DateField(input_formats=['%d-%m-%Y'], label="Fecha de Inicio(dd/mm/yyyy)" )
    fin = forms.DateField(input_formats=['%d-%m-%Y'], label="Fecha de Fin(dd/mm/yyyy)" )
    FRECUENCIAS = ( (1, 'Horario'), (2, 'Diario'))
    frecuencia = forms.ChoiceField(choices=FRECUENCIAS, label="Frecuencia")


class CuvarCaudalMultiestacionForm(forms.Form):
    estacion = forms.MultipleChoiceField(choices=[], label="Estación", widget=forms.CheckboxSelectMultiple)
    inicio = forms.DateField(
        input_formats=['%d-%m-%Y'], label="Inicio", required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    fin = forms.DateField(
        input_formats=['%d-%m-%Y'], label="Fin", required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

    def __init__(self, *args, **kwargs):
        super(CuvarCaudalMultiestacionForm, self).__init__(*args, **kwargs)
        estaciones = Estacion.objects.filter(tipo_id__exact=3, influencia_km__gt=0).order_by('est_codigo', '-est_externa')
        lista = []
        for e in estaciones:
            lista.append([e.est_id, e.est_codigo])
            #print([e.est_id, e.est_codigo])
        self.fields['estacion'].choices = lista


class IntensidadDuracionMultiestacionForm(forms.Form):
    estacion = forms.MultipleChoiceField(choices=[], label="Estación", widget=forms.CheckboxSelectMultiple)
    inicio = forms.DateField(
        input_formats=['%Y-%m-%d'], label="Inicio", required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    fin = forms.DateField(
        input_formats=['%Y-%m-%d'], label="Fin", required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

    def __init__(self, *args, **kwargs):
        super(IntensidadDuracionMultiestacionForm, self).__init__(*args, **kwargs)
        estaciones = Estacion.objects.filter(tipo_id__in=[1, 2]).order_by('est_codigo')
        lista = []
        for e in estaciones:
            lista.append([e.est_id, e.est_codigo])
        self.fields['estacion'].choices = lista
