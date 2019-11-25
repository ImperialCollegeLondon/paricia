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
    inicio = forms.DateField(input_formats=['%Y-%m-%d'], label="Fecha de Iniciodfdf(yyyy-mm-dd)")
    fin = forms.DateField(input_formats=['%Y-%m-%d'], label="Fecha de Fin(yyyy-mm-dd)")
    FRECUENCIAS = ((0,'Instantaneo'),(1,'Horario'),(2,'Diario'),(3,'Mensual'))
    frecuencia = forms.ChoiceField(choices=FRECUENCIAS,label="Frecuencia")
    def getValidate(self):
        print( self.estacion1)


class SelecEstForm(forms.Form):
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.filter(tipo_id__in=[1,2]).order_by('est_id'), label="Estacion meteorológica")
    inicio = forms.DateField(input_formats=['%Y-%m-%d'], label="Fecha de Iniciodfdf(yyyy-mm-dd)")
    fin = forms.DateField(input_formats=['%Y-%m-%d'], label="Fecha de Fin(yyyy-mm-dd)")


class SelecCaudalForm(forms.Form):
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.filter(tipo_id__exact=3).order_by('est_id'), label="Estacion Hidrológica")
    inicio = forms.DateField(input_formats=['%Y-%m-%d'], label="Fecha de Iniciodfdf(yyyy-mm-dd)")
    fin = forms.DateField(input_formats=['%Y-%m-%d'], label="Fecha de Fin(yyyy-mm-dd)")
    FRECUENCIAS = ( (1, 'Horario'), (2, 'Diario'))
    frecuencia = forms.ChoiceField(choices=FRECUENCIAS, label="Frecuencia")
