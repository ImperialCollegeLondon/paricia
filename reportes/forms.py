# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from estacion.models import Estacion, Inamhi
from variable.models import Parametro


class AnuarioForm(ModelForm):
    class Meta:
        model = Estacion
        fields = ['est_id']

    # ESTACION = lista_estaciones()
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
    )
    lista = []
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.order_by('est_id').all(), label='Estación')
    anio = forms.ChoiceField(choices=YEAR, label='Año')


class InamhiForm(forms.Form):
    lista_frecuencia = (
        ('storage', 'minuto'),
        ('data1h', 'horario')
    )
    parametros_widget = forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'dd/mm/yy'})
    format_input = ['%d/%m/%Y']
    lbl_inicio = 'Fecha de Inicio'
    lbl_fin = 'Fecha de Fin'
    consulta_estacion = Inamhi.objects.order_by('codigo').all()
    consulta_parametro = Parametro.objects.order_by('id').all()
    # atributos del formulario
    estacion = forms.ModelChoiceField(queryset=consulta_estacion, label='Estacion')
    frecuencia = forms.ChoiceField(choices=lista_frecuencia, label="Frecuencia")
    parametro = forms.ModelChoiceField(queryset=consulta_parametro, label='Parametro')
    inicio = forms.DateField(input_formats=format_input, label=lbl_inicio, widget=parametros_widget)
    fin = forms.DateField(input_formats=format_input, label=lbl_fin, widget=parametros_widget)


