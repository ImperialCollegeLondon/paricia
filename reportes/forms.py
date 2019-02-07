# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from estacion.models import Estacion
from medicion.models import Medicion
from variable.models import Variable, Unidad
from cruce.models import Cruce


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
        ('2017', '2018'),
    )
    lista = []
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.order_by('est_id').all(), label='Estación')
    anio = forms.ChoiceField(choices=YEAR, label='Año')
