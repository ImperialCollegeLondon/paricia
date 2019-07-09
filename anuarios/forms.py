# -*- coding: utf-8 -*-

from django import forms
from estacion.models import Estacion
from variable.models import Variable
from cruce.models import Cruce


class AnuarioForm(forms.Form):
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

    estacion = forms.ModelChoiceField(required=False,
                                      queryset=Estacion.objects.order_by('est_id').all(), label='Estación')
    variable = forms.ModelChoiceField(required=False,
                                      queryset=Variable.objects.order_by('var_id').all(), label='Variable')
    periodo = forms.ChoiceField(required=False, choices=YEAR, label='Año')
