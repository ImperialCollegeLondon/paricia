# -*- coding: utf-8 -*-
from django.forms import ModelForm, Form, ModelChoiceField, DateTimeField
from django.forms import ModelForm
from validacion.models import Validacion
from estacion.models import Estacion
from station.models import Station
from variable.models import Variable

from django import forms
from estacion.models import Tipo



class DailyValidationForm(forms.Form):
    station = forms.ModelChoiceField(
        queryset=Station.objects.order_by('station_code'),
        empty_label="Station"
    )
    variable = forms.ModelChoiceField(
        queryset=Variable.objects.order_by('variable_code'),
        empty_label="Variable"
    )
    start_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        label="Start date",
        required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'off'}),
    )
    end_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        label="End date",
        required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'off'}),
    )
    minimum = forms.DecimalField(required=False)
    maximum = forms.DecimalField(required=False)
    #revalidar = forms.BooleanField(label="Revalidar", help_text='Marcar si deseas borrar la última validacion')
    def __init__(self, *args, **kwargs):
        super(DailyValidationForm, self).__init__(*args, **kwargs)
        self.fields['station'].widget.attrs['placeholder'] = self.fields['station'].label

class ValidacionSearchForm(forms.Form):
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.order_by('est_codigo').filter(est_externa=False, tipo__in=(1,2,3)), empty_label="Estación")
    variable = forms.ModelChoiceField(queryset=Variable.objects.order_by('var_id').exclude(var_id='10'), empty_label="Variable")
    inicio = forms.DateField(widget=forms.TextInput(attrs={'autocomplete': 'off'}), input_formats=['%Y-%m-%d'], label="Fecha de Inicio", required=True)
    fin = forms.DateField(widget=forms.TextInput(attrs={'autocomplete': 'off'}), input_formats=['%Y-%m-%d'], label="Fecha de Fin", required=True)
    limite_inferior = forms.IntegerField(required=False)
    limite_superior = forms.IntegerField(required=False)
    #revalidar = forms.BooleanField(label="Revalidar", help_text='Marcar si deseas borrar la última validacion')
    def __init__(self, *args, **kwargs):
        super(ValidacionSearchForm, self).__init__(*args, **kwargs)
        self.fields['estacion'].widget.attrs['placeholder'] = self.fields['estacion'].label

#
# class BorrarForm(Form):
#     estacion = ModelChoiceField(queryset=Estacion.objects.order_by('est_id').all(), empty_label="Estación")
#     variable = ModelChoiceField(queryset=Variable.objects.order_by('var_id').all(), empty_label="Variable")
#     inicio = DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], label="Fecha de Inicio")
#     fin = DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], label="Fecha de Fin")
