# -*- coding: utf-8 -*-
from django.forms import ModelForm, Form, ModelChoiceField, DateTimeField
from django.forms import ModelForm
from validacion.models import Validacion
from estacion.models import Estacion
from variable.models import Variable


class BorrarForm(Form):
    estacion = ModelChoiceField(queryset=Estacion.objects.order_by('est_id').all())
    variable = ModelChoiceField(queryset=Variable.objects.order_by('var_id').all())
    inicio = DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], label="Fecha de Inicio(yyyy-mm-dd HH:MM:SS)")
    fin = DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], label="Fecha de Fin(yyyy-mm-dd HH:MM:SS)")
