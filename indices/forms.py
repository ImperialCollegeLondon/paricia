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
from medicion.models import CurvaDescarga
from validacion.models import Var1Validado
from datetime import date

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
    inicio = forms.DateField(widget=forms.TextInput(attrs={'autocomplete': 'off'}),input_formats=['%Y-%m-%d'], label="Fecha de Inicio(yyyy-mm-dd)" )
    fin = forms.DateField(widget=forms.TextInput(attrs={'autocomplete': 'off'}),input_formats=['%Y-%m-%d'], label="Fecha de Fin(yyyy-mm-dd)" )
    FRECUENCIAS = ((1,'Horario'),(2,'Diario'),(3,'Mensual'))
    frecuencia = forms.ChoiceField(choices=FRECUENCIAS,label="Frecuencia")
    def getValidate(self):
        print( self.estacion1)

#intensidad duracion
class SelecEstForm(forms.Form):
    today = date.today()
    ch = [tuple([a,a]) for a in range(2000,today.year+1)]
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.filter(tipo_id__in=[1,2]).order_by('est_id'), empty_label="Estación")
    #inicio = forms.DateField(input_formats=['%Y-%m-%d'], label="Fecha de Inicio(dd/mm/yyyy)" )
    anio = forms.ChoiceField(label="Año  ",choices=ch )

class IntensidadDuracionMultiestacionForm(forms.Form):
    #print("multiestacion ::::")
    estacion = forms.MultipleChoiceField(choices=[], label="Estación", widget=forms.CheckboxSelectMultiple)
    today = date.today()
    ch = [tuple([a, a]) for a in range(2000, today.year + 1)]
    anio = forms.ChoiceField(label="Año  ", choices=ch)

    def __init__(self, *args, **kwargs):
        super(IntensidadDuracionMultiestacionForm, self).__init__(*args, **kwargs)
        estaciones = Estacion.objects.filter(tipo_id__in=[1, 2]).order_by('est_codigo')
        lista = []
        for e in estaciones:
            lista.append([e.est_id, e.est_codigo])
        self.fields['estacion'].choices = lista


class IndPrecipForm(forms.Form):
    fechf = datetime.strptime("31/12/2010", '%d/%m/%Y')
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.filter(tipo_id__in = (1,2)).order_by('est_id'), empty_label="Estación")
    inicio = forms.DateField(widget=forms.TextInput(attrs={'autocomplete': 'off'}),input_formats=['%Y-%m-%d'], label="Fecha de Inicio(yyyy-mm-dd)")
    fin = forms.DateField(widget=forms.TextInput(attrs={'autocomplete': 'off'}),input_formats=['%Y-%m-%d'], label="Fecha de Fin(yyyy-mm-dd)")


class IndCaudForm(forms.Form):
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.filter(tipo_id__exact = 3 ).order_by('est_id'), empty_label="Estación")
    inicio = forms.DateField(widget=forms.TextInput(attrs={'autocomplete': 'off'}),input_formats=['%Y-%m-%d'], label="Fecha de Inicio(yyyy-mm-dd)" )
    fin = forms.DateField(widget=forms.TextInput(attrs={'autocomplete': 'off'}),input_formats=['%Y-%m-%d'], label="Fecha de Fin(yyyy-mm-dd)" )


class SelecCaudalForm(forms.Form):
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.filter(tipo_id__exact = 3 ).order_by('est_id'), empty_label="Estación")
    inicio = forms.DateField(widget=forms.TextInput(attrs={'autocomplete': 'off'}),input_formats=['%Y-%m-%d'], label="Fecha de Inicio(yyyy-mm-dd)" )
    fin = forms.DateField(widget=forms.TextInput(attrs={'autocomplete': 'off'}),input_formats=['%Y-%m-%d'], label="Fecha de Fin(yyyy-mm-dd)" )
    FRECUENCIAS = ( (1, 'Horario'), (2, 'Diario'))
    frecuencia = forms.ChoiceField(choices=FRECUENCIAS, label="Frecuencia")


class CuvarCaudalMultiestacionForm(forms.Form):
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
        super(CuvarCaudalMultiestacionForm, self).__init__(*args, **kwargs)
        estaciones = Estacion.objects.filter(tipo_id__exact=3, influencia_km__gt=0).order_by('est_codigo')
        lista = []
        for e in estaciones:
            lista.append([e.est_id, e.est_codigo])
            #print([e.est_id, e.est_codigo])
        self.fields['estacion'].choices = lista
