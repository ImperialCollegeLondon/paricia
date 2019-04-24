# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from estacion.models import Estacion


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
    )
    lista = []
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.order_by('est_id').all(), label='Estación')
    anio = forms.ChoiceField(choices=YEAR, label='Año')


class InamhiForm(forms.Form):
    lista_estaciones = (
        ('63777','M50024 Iñaquito')
    )
    lista_transmision = (
        ('GPFT', 'GPFT')
    )
    parametros_widget = forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'dd/mm/yy'})
    format_input = ['%d/%m/%Y']
    lbl_inicio = 'Fecha de Inicio'
    lbl_fin = 'Fecha de Fin'
    estacion=forms.ChoiceField(choices=lista_estaciones,label='Estacion')
    inicio = forms.DateField(input_formats=format_input, label=lbl_inicio, widget=parametros_widget)
    fin = forms.DateField(input_formats=format_input, label=lbl_fin, widget=parametros_widget)
    transmision=forms.ChoiceField(choices=lista_transmision,label='Transmisión')

