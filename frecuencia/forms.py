# -*- coding: utf-8 -*-

from django import forms
from frecuencia.models import Frecuencia
from estacion.models import Estacion
from formato.models import Variable


class FrecuenciaSearchForm(forms.Form):
    variable = forms.ModelChoiceField(label="Variable",required=False,queryset=Variable.objects.order_by('var_id').all())
    estacion = forms.ModelChoiceField(label="Estacion",required=False,queryset=Estacion.objects.order_by('est_id').all())
    lista = []

    def filtrar(self, form):
        var_id = form.cleaned_data['variable']
        est_id = form.cleaned_data['estacion']
        if var_id and est_id:
            lista = Frecuencia.objects.filter(
                var_id=var_id
            ).filter(
                est_id=est_id
            )
        elif var_id is None and est_id:
            lista = Frecuencia.objects.filter(
                est_id=est_id
            )
        elif est_id is None and var_id:
            lista = Frecuencia.objects.filter(
                var_id=var_id
            )
        else:
            lista = Frecuencia.objects.all()
        return lista
