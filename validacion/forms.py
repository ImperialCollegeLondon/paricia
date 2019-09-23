# -*- coding: utf-8 -*-
from django.forms import ModelForm, Form, ModelChoiceField, DateTimeField
from django.forms import ModelForm
from validacion.models import Validacion
from estacion.models import Estacion
from variable.models import Variable


class ValidacionProcess(ModelForm):
    class Meta:
        model = Validacion
        fields = ['var_id', 'est_id']



class ConsultaValidacionForm(Form):
    estacion = ModelChoiceField(required=False, queryset=Estacion.objects.order_by('est_id').all())
    variable = ModelChoiceField(required=False, queryset=Variable.objects.order_by('var_id').all())

    def filtrar(self, form):
        estacion_ = form.cleaned_data['estacion']
        variable_ = form.cleaned_data['variable']

        if estacion_ and variable_:
            lista = Validacion.objects.filter(est_id=estacion_).filter(var_id=variable_)
        elif (estacion_ != None and estacion_ != '') and (variable_ == None or variable_ == ''):
            lista = Validacion.objects.filter(est_id=estacion_)
        elif (variable_ != ""  and variable_ != None) and (estacion_ == None or estacion_ == '' ):
            lista = Validacion.objects.filter(var_id=variable_)
        else:
            lista = Validacion.objects.all()
        return lista


class BorrarForm(Form):
    estacion = ModelChoiceField(queryset=Estacion.objects.order_by('est_id').all())
    variable = ModelChoiceField(queryset=Variable.objects.order_by('var_id').all())
    inicio = DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], label="Fecha de Inicio(yyyy-mm-dd HH:MM:SS)")
    fin = DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], label="Fecha de Fin(yyyy-mm-dd HH:MM:SS)")