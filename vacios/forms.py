# -*- coding: utf-8 -*-

# from django.forms import ModelForm
from django import forms
from vacios.models import Vacios
from estacion.models import Estacion
from formato.models import Variable


class VaciosSearchForm(forms.Form):
    estacion = forms.ModelChoiceField(required=False,
                                      queryset=Estacion.objects.order_by('est_id').all())
    variable = forms.ModelChoiceField(required=False,
                                      queryset=Variable.objects.order_by('var_id').all())
    lista = []

    def filtrar(self, form):
        variable = form.cleaned_data['variable']
        estacion = form.cleaned_data['estacion']
        if variable and estacion:
            lista = Vacios.objects.filter(
                var_id=variable
            ).filter(
                est_id=estacion
            )
        elif variable is None and estacion:
            lista = Vacios.objects.filter(
                est_id=estacion
            )
        elif estacion is None and variable:
            lista = Vacios.objects.filter(
                var_id=variable
            )
        else:
            lista = Vacios.objects.all()
        return lista
